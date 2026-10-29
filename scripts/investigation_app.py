"""Loopback-only synthetic product slice. Standard library; no uploaded data."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sqlite3
from urllib.parse import urlparse
import webbrowser

from golden import investigation
from golden.pilot_control import ControlStore, Stopped

PAGE = Path(__file__).resolve().parents[1]/'examples/manufacturing/app.html'


def run_job(store, ident, owner, reader=investigation.read_snapshot):
    op = None
    try:
        request = store.claim(ident)
    except Stopped:
        return  # Duplicate workers must not cancel the winner.
    if request is None: return
    try:
        status, snapshot, root = investigation.authorize(request)
        if status != 'allowed':
            store.finish(ident,{'status': status,'nodes': [],'edges': [],'unresolved': []})
            return
        op = store.begin(ident,{'path': snapshot['path'],'sha256': snapshot['sha256'],
                               'system': 'bundled synthetic specimen'})
        store.check(ident)
        data = reader(snapshot)
        store.read_returned(ident,op)
        store.check(ident)
        result = investigation.resolve(request,data,snapshot,root)
        store.finish(ident,result,op)
    except Stopped:
        # Late readers cannot publish, including after a stop followed by recovery.
        store.cancel(ident,owner)
    except (ValueError, OSError, SyntaxError, UnicodeError):
        store.fail(ident,op)


def make_server(store, port=0):
    token = secrets.token_urlsafe(32)  # Browser capability only; cannot administer.
    owner = secrets.token_hex(16)     # Synthetic session; never a claimed employee identity.
    pool = ThreadPoolExecutor(max_workers=2)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass  # No payload/token in console logs.

        def send(self, status, data, html=False):
            body = data.encode('utf-8') if html else json.dumps(data,allow_nan=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type','text/html; charset=utf-8' if html else 'application/json')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',f"default-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'; style-src 'unsafe-inline'; script-src 'nonce-{token}'")
            self.end_headers(); self.wfile.write(body)

        def boundary(self, api=False):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != f'127.0.0.1:{self.server.server_port}':
                raise PermissionError('loopback host required')
            if self.headers.get('Origin') not in (None,origin):
                raise PermissionError('cross-origin request denied')
            if api and not secrets.compare_digest(self.headers.get('X-Pilot-Token',''),token):
                raise PermissionError('browser capability required')

        def do_GET(self):
            try:
                self.boundary()
                path = urlparse(self.path).path
                if path == '/':
                    self.send(200,PAGE.read_text(encoding='utf-8').replace('@@TOKEN@@',token),html=True)
                elif path.startswith('/api/jobs/'):
                    self.boundary(api=True)
                    self.send(200,store.get(path.rsplit('/',1)[1],owner))
                else: self.send(404,{'error': 'not found'})
            except PermissionError: self.send(403,{'error': 'access denied'})
            except ValueError: self.send(409,{'error': 'artifact integrity failure; contact operator'})
            except sqlite3.Error: self.send(503,{'error': 'Supervisor unavailable; contact operator.'})

        def do_POST(self):
            try:
                self.boundary(api=True)
                length = int(self.headers.get('Content-Length','0'))
                if not 0 < length <= 4096: raise ValueError('body size')
                payload = json.loads(self.rfile.read(length))
                path = urlparse(self.path).path
                if path == '/api/jobs':
                    investigation.validate_request(payload)
                    ident = store.submit(payload,owner,self.headers.get('Idempotency-Key',''))
                    # Duplicate submissions can race to claim; only one succeeds.
                    pool.submit(run_job,store,ident,owner)
                    self.send(202,{'id': ident})
                elif path.startswith('/api/cancel/') and payload == {}:
                    state = store.cancel(path.rsplit('/',1)[1],owner)
                    self.send(200,{'state': state})
                else: self.send(404,{'error': 'not found'})
            except PermissionError: self.send(403,{'error': 'access denied'})
            except Stopped: self.send(409,{'error': 'Stopped, expired or full. Contact the local operator.'})
            except (ValueError, TypeError): self.send(400,{'error': 'Invalid request or conflicting retry key.'})
            except sqlite3.Error: self.send(503,{'error': 'Supervisor unavailable; no work authorized.'})

    server = ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.pool = pool
    return server


def recover_interrupted(store, token):
    inventory = store.inventory(token)
    if any(j['state'] in ('queued','running') for j in inventory['artifacts']):
        store.stop(token,'restart with interrupted work; operator reconciliation required')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=0)
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('--workspace',type=Path,default=Path('workspace'))
    args = parser.parse_args(); args.workspace.mkdir(exist_ok=True,parents=True)
    key = args.workspace/'pilot-operator.key'
    if not key.exists():
        fd = os.open(key,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(secrets.token_urlsafe(32))
    token = key.read_text(encoding='utf-8').strip()
    store = ControlStore(args.workspace/'pilot.sqlite',bootstrap_token=token)
    recover_interrupted(store,token)
    server = make_server(store,args.port)
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'Synthetic local pilot: {url}. Operator controls: see examples/manufacturing/README.md')
    if not args.no_browser: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally:
        store.stop(token,'local server shutdown')
        server.shutdown(); server.server_close(); server.pool.shutdown(wait=True)


if __name__ == '__main__': main()
