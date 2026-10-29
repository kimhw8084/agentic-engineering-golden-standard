"""Local synthetic supervisor: durable admission, cancellation and result fencing.

SQLite and an operator capability live OUTSIDE model/user input. This is not SSO,
a distributed executor, a protected audit sink or a rollback mechanism. A process
with database/OS-owner access can bypass it. Never attach external-effect tools.
"""
from contextlib import contextmanager
from hashlib import sha256
import hmac
import json
from pathlib import Path
import sqlite3
import time
from uuid import uuid4

from golden.change import canonical_hash


class Stopped(ValueError):
    pass


class ControlStore:
    def __init__(self, path, bootstrap_token=None):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.tx() as db:
            schema = '''
                CREATE TABLE IF NOT EXISTS control (
                    id INTEGER PRIMARY KEY CHECK(id=1), active INTEGER NOT NULL,
                    enabled INTEGER NOT NULL, epoch INTEGER NOT NULL, token_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY, owner TEXT NOT NULL, idem TEXT NOT NULL,
                    input_hash TEXT NOT NULL, request TEXT NOT NULL, epoch INTEGER NOT NULL,
                    state TEXT NOT NULL, deadline REAL NOT NULL,
                    result TEXT, artifact_hash TEXT, UNIQUE(owner,idem));
                CREATE TABLE IF NOT EXISTS operations (
                    id TEXT PRIMARY KEY, job TEXT NOT NULL, tool TEXT NOT NULL,
                    source_ref TEXT NOT NULL, state TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, at REAL NOT NULL,
                    kind TEXT NOT NULL, ref TEXT NOT NULL, detail TEXT NOT NULL);
            '''
            for statement in schema.split(';'):
                if statement.strip(): db.execute(statement)
            if db.execute('SELECT 1 FROM control').fetchone() is None:
                if not isinstance(bootstrap_token, str) or len(bootstrap_token) < 32:
                    raise ValueError('new store needs provisioned operator capability')
                db.execute('INSERT INTO control VALUES (1,1,1,0,?)', (self.digest(bootstrap_token),))

    @staticmethod
    def digest(token):
        return sha256(token.encode('utf-8')).hexdigest()

    @contextmanager
    def tx(self):
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback(); raise
        finally:
            db.close()

    def event(self, db, kind, ref, detail=None):
        db.execute('INSERT INTO events(at,kind,ref,detail) VALUES (?,?,?,?)',
                   (time.time(), kind, ref, json.dumps(detail or {}, sort_keys=True)))

    def admin(self, db, token):
        actual = db.execute('SELECT token_hash FROM control WHERE id=1').fetchone()[0]
        if not isinstance(token, str) or not hmac.compare_digest(actual, self.digest(token)):
            raise PermissionError('operator capability required')

    def fence(self, db, job=None):
        ctl = db.execute('SELECT * FROM control WHERE id=1').fetchone()
        if not ctl['active'] or not ctl['enabled']:
            raise Stopped('emergency stop or capability disabled')
        if job and (job['state'] != 'running' or job['epoch'] != ctl['epoch']
                    or time.time() >= job['deadline']):
            raise Stopped('job canceled, terminal or from an older epoch')
        return ctl

    def submit(self, request, owner, key):
        # Only the trusted server supplies owner. It is a synthetic session label.
        if not isinstance(key, str) or not 1 <= len(key) <= 100:
            raise ValueError('idempotency key required')
        encoded = json.dumps(request, sort_keys=True, allow_nan=False)
        digest = canonical_hash(request)
        with self.tx() as db:
            ctl = self.fence(db)
            row = db.execute('SELECT * FROM jobs WHERE owner=? AND idem=?', (owner,key)).fetchone()
            if row:
                if row['input_hash'] != digest:
                    raise ValueError('idempotency key conflicts with input')
                return row['id']
            if db.execute("SELECT COUNT(*) FROM jobs WHERE state IN ('queued','running')").fetchone()[0] >= 16:
                raise Stopped('queue capacity reached')
            ident = uuid4().hex
            db.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,NULL,NULL)',
                       (ident,owner,key,digest,encoded,ctl['epoch'],'queued',time.time()+10))
            self.event(db,'submitted',ident,{'input_hash': digest, 'epoch': ctl['epoch']})
            return ident

    def claim(self, ident):
        with self.tx() as db:
            ctl = self.fence(db)
            row = db.execute('SELECT * FROM jobs WHERE id=?', (ident,)).fetchone()
            if row is None or row['state'] != 'queued':
                raise Stopped('not queued')
            if row['epoch'] != ctl['epoch'] or time.time() >= row['deadline']:
                db.execute("UPDATE jobs SET state='canceled' WHERE id=?", (ident,))
                self.event(db,'expired_before_claim',ident)
                return None
            db.execute("UPDATE jobs SET state='running' WHERE id=?", (ident,))
            self.event(db,'claimed',ident)
            return json.loads(row['request'])

    def begin(self, ident, source_ref):
        with self.tx() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (ident,)).fetchone()
            if row is None:
                raise Stopped('unknown job')
            self.fence(db,row)
            if db.execute('SELECT 1 FROM operations WHERE job=?', (ident,)).fetchone():
                raise Stopped('one-read budget exhausted')
            op = uuid4().hex
            db.execute('INSERT INTO operations VALUES (?,?,?,?,?)',
                       (op,ident,'read_synthetic_snapshot',json.dumps(source_ref,sort_keys=True),'in_flight'))
            self.event(db,'read_admitted',op,source_ref)
            return op

    def check(self, ident):
        with self.tx() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (ident,)).fetchone()
            if row is None: raise Stopped('unknown job')
            self.fence(db,row)

    def read_returned(self, ident, op):
        # Keep the observation even after cancellation; never restore job state.
        with self.tx() as db:
            if db.execute('SELECT 1 FROM operations WHERE id=? AND job=?', (op,ident)).fetchone() is None:
                raise ValueError('unknown operation')
            self.event(db,'read_returned',op,{'job': ident})

    def finish(self, ident, result, op=None):
        encoded = json.dumps(result, sort_keys=True, allow_nan=False)
        with self.tx() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (ident,)).fetchone()
            try:
                if row is None: raise Stopped('unknown job')
                self.fence(db,row)
            except Stopped:
                self.event(db,'late_result_discarded',ident,{'operation': op})
                return False
            if op:
                operation = db.execute('SELECT * FROM operations WHERE id=? AND job=?', (op,ident)).fetchone()
                if operation is None or operation['state'] != 'in_flight':
                    raise Stopped('operation is not in flight')
                db.execute("UPDATE operations SET state='completed_read' WHERE id=?", (op,))
            db.execute("UPDATE jobs SET state='succeeded', result=?, artifact_hash=? WHERE id=?",
                       (encoded,canonical_hash(result),ident))
            self.event(db,'result_published',ident,{'artifact_hash': canonical_hash(result),'operation': op})
            return True

    def fail(self, ident, op=None):
        with self.tx() as db:
            db.execute("UPDATE jobs SET state='failed' WHERE id=? AND state='running'", (ident,))
            if op:
                db.execute("UPDATE operations SET state='failed_read' WHERE id=? AND state='in_flight'", (op,))
            self.event(db,'read_failed',ident,{'operation': op})

    def cancel(self, ident, owner):
        with self.tx() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=? AND owner=?', (ident,owner)).fetchone()
            if row is None: raise PermissionError('unknown job in this session')
            if row['state'] not in ('queued','running'):
                return 'already_terminal'
            db.execute("UPDATE jobs SET state='canceled' WHERE id=?", (ident,))
            db.execute("UPDATE operations SET state='unknown' WHERE job=? AND state='in_flight'", (ident,))
            self.event(db,'canceled',ident)
            return 'canceled'

    def stop(self, token, reason):
        if not isinstance(reason, str) or not reason.strip(): raise ValueError('reason required')
        with self.tx() as db:
            self.admin(db,token)
            db.execute('UPDATE control SET active=0, enabled=0, epoch=epoch+1 WHERE id=1')
            db.execute("UPDATE jobs SET state='canceled' WHERE state IN ('queued','running')")
            db.execute("UPDATE operations SET state='unknown' WHERE state='in_flight'")
            self.event(db,'emergency_stop','control',{'reason': reason})

    def reconcile(self, token, op, reason):
        if not isinstance(reason, str) or not reason.strip(): raise ValueError('review evidence required')
        with self.tx() as db:
            self.admin(db,token)
            changed = db.execute("UPDATE operations SET state='reconciled_read_only' WHERE id=? AND state='unknown'", (op,)).rowcount
            if changed != 1: raise ValueError('unknown operation required')
            self.event(db,'reconciled',op,{'basis': reason, 'scope': 'local read only; no external effects'})

    def resume(self, token, expected_epoch, reason):
        if type(expected_epoch) is not int or not isinstance(reason, str) or not reason.strip():
            raise ValueError('expected epoch and recovery basis required')
        with self.tx() as db:
            self.admin(db,token)
            ctl = db.execute('SELECT * FROM control WHERE id=1').fetchone()
            if ctl['active'] or ctl['epoch'] != expected_epoch:
                raise ValueError('recovery state conflict')
            if db.execute("SELECT 1 FROM operations WHERE state IN ('unknown','in_flight')").fetchone():
                raise ValueError('reconcile all uncertain operations first')
            # Recovery explicitly re-enables the sole synthetic read capability.
            db.execute('UPDATE control SET active=1, enabled=1, epoch=epoch+1 WHERE id=1')
            self.event(db,'authorized_recovery','control',{'basis': reason, 'prior_epoch': expected_epoch})

    def get(self, ident, owner):
        with self.tx() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=? AND owner=?', (ident,owner)).fetchone()
            if row is None: raise PermissionError('unknown job in this session')
            result = json.loads(row['result']) if row['result'] else None
            if result is not None and canonical_hash(result) != row['artifact_hash']:
                raise ValueError('stored artifact hash mismatch')
            return {'id': ident,'state': row['state'],'result': result,'artifact_hash': row['artifact_hash']}

    def inventory(self, token):
        with self.tx() as db:
            self.admin(db,token)
            ctl = dict(db.execute('SELECT active,enabled,epoch FROM control WHERE id=1').fetchone())
            return {'control': ctl,
                    'operations': [dict(r) for r in db.execute('SELECT * FROM operations ORDER BY rowid')],
                    'artifacts': [dict(r) for r in db.execute('SELECT id,state,artifact_hash FROM jobs ORDER BY rowid')],
                    'events': [dict(r) for r in db.execute('SELECT * FROM events ORDER BY seq')],
                    'limits': 'Local mutable SQLite evidence, not tamper-proof audit or employee authentication.'}
