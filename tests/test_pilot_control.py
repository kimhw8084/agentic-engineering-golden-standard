from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
from threading import Barrier, Event, Thread
import unittest
from unittest.mock import patch

from golden.pilot_control import ControlStore, Stopped
from scripts.investigation_app import run_job, recover_interrupted
from golden.investigation import read_snapshot

TOKEN='synthetic-operator-capability-0123456789'
REQUEST={'revision':'r1','parameter':'sample_count'}


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'control.sqlite'
        self.store=ControlStore(self.path,TOKEN)

    def submit(self,key='key'):
        return self.store.submit(REQUEST,'session',key)

    def test_idempotent_concurrent_submission_and_conflicting_input(self):
        barrier=Barrier(2)
        def submit(_): barrier.wait(); return self.submit()
        with ThreadPoolExecutor(2) as pool: ids=list(pool.map(submit,range(2)))
        self.assertEqual(ids[0],ids[1])
        with self.assertRaises(ValueError):
            self.store.submit({**REQUEST,'revision':'r2'},'session','key')
        # A second session has a separate key space and cannot fetch/cancel the first.
        with self.assertRaises(PermissionError): self.store.get(ids[0],'other')
        with self.assertRaises(PermissionError): self.store.cancel(ids[0],'other')

    def test_duplicate_worker_does_not_cancel_winner(self):
        ident=self.submit(); entered,release=Event(),Event()
        def reader(snapshot): entered.set(); self.assertTrue(release.wait(3)); return read_snapshot(snapshot)
        worker=Thread(target=run_job,args=(self.store,ident,'session',reader));worker.start()
        try:
            self.assertTrue(entered.wait(3))
            run_job(self.store,ident,'session')
            self.assertEqual(self.store.get(ident,'session')['state'],'running')
        finally: release.set();worker.join(3)
        self.assertFalse(worker.is_alive())
        self.assertEqual(self.store.get(ident,'session')['state'],'succeeded')
        self.assertEqual(len(self.store.inventory(TOKEN)['operations']),1)

    def test_stop_before_admission_prevents_reads_and_new_jobs(self):
        ident=self.submit(); self.store.stop(TOKEN,'fault drill')
        with self.assertRaises(Stopped): self.submit('new')
        with self.assertRaises(Stopped): self.store.claim(ident)
        self.assertEqual(self.store.inventory(TOKEN)['operations'],[])
        self.assertEqual(self.store.get(ident,'session')['state'],'canceled')

    def test_inflight_stop_separate_process_late_result_recovery(self):
        ident=self.submit(); entered,release=Event(),Event()
        def reader(snapshot): entered.set(); self.assertTrue(release.wait(5)); return read_snapshot(snapshot)
        worker=Thread(target=run_job,args=(self.store,ident,'session',reader));worker.start()
        try:
            self.assertTrue(entered.wait(3))
            key=Path(self.tmp.name)/'operator.key';key.write_text(TOKEN)
            process=subprocess.run([sys.executable,'-m','scripts.pilot_control','stop','--db',str(self.path),
                                    '--key-file',str(key),'--reason','separate process drill'],
                                   capture_output=True,text=True,timeout=5)
            self.assertEqual(process.returncode,0,process.stderr)
            state=self.store.inventory(TOKEN)
            self.assertEqual(state['control'],{'active':0,'enabled':0,'epoch':1})
            op=state['operations'][0]
            self.assertEqual(op['state'],'unknown')
            self.assertIn('examples/manufacturing/r1.py',op['source_ref'])
            with self.assertRaises(ValueError): self.store.resume(TOKEN,1,'review')
            self.store.reconcile(TOKEN,op['id'],'only bundled read; no external effects')
            self.store.resume(TOKEN,1,'authorized synthetic recovery')
            release.set();worker.join(3)
            self.assertFalse(worker.is_alive())
            self.assertIsNone(self.store.get(ident,'session')['result'])
            self.assertTrue(any(e['kind']=='read_returned' for e in self.store.inventory(TOKEN)['events']))
            new=self.submit('after-recovery');run_job(self.store,new,'session')
            self.assertEqual(self.store.get(new,'session')['state'],'succeeded')
        finally:release.set();worker.join(3)

    def test_cancel_and_publish_race_has_one_authoritative_outcome(self):
        for i in range(8):
            ident=self.submit(str(i));self.store.claim(ident)
            barrier=Barrier(2)
            def cancel(): barrier.wait();return self.store.cancel(ident,'session')
            def finish(): barrier.wait();return self.store.finish(ident,{'synthetic':True})
            with ThreadPoolExecutor(2) as pool:
                a=pool.submit(cancel);b=pool.submit(finish);cancel_result,finished=a.result(),b.result()
            result=self.store.get(ident,'session')
            self.assertIn((cancel_result,finished,result['state']),
                          [('canceled',False,'canceled'),('already_terminal',True,'succeeded')])

    def test_restart_persistence_wrong_operator_and_epoch(self):
        ident=self.submit();self.store.stop(TOKEN,'stop')
        reopened=ControlStore(self.path)
        for token in ('', 'claimed-admin',None):
            with self.assertRaises(PermissionError):reopened.resume(token,1,'recover')
        with self.assertRaises(ValueError):reopened.resume(TOKEN,0,'stale approval')
        self.assertEqual(reopened.get(ident,'session')['state'],'canceled')
        reopened.resume(TOKEN,1,'manual verification')
        self.assertEqual(reopened.submit(REQUEST,'session','key'),ident)

    def test_source_failure_stays_failure_not_no_dependency(self):
        ident=self.submit()
        def fail(_):raise OSError('synthetic source outage')
        run_job(self.store,ident,'session',fail)
        self.assertEqual(self.store.get(ident,'session')['state'],'failed')
        self.assertEqual(self.store.inventory(TOKEN)['operations'][0]['state'],'failed_read')

    def test_process_crash_leaves_reconcilable_intent_and_startup_stops(self):
        code = '''import sys,os
from golden.pilot_control import ControlStore
s=ControlStore(sys.argv[1])
j=s.submit({'revision':'r1','parameter':'sample_count'},'crashed','crash-key')
s.claim(j);s.begin(j,{'path':'examples/manufacturing/r1.py','system':'bundled synthetic'})
os._exit(17)
'''
        result=subprocess.run([sys.executable,'-c',code,str(self.path)],capture_output=True,text=True,timeout=5)
        self.assertEqual(result.returncode,17,result.stderr)
        restarted=ControlStore(self.path)
        recover_interrupted(restarted,TOKEN)
        state=restarted.inventory(TOKEN)
        self.assertEqual(state['operations'][0]['state'],'unknown')
        self.assertEqual(state['artifacts'][0]['state'],'canceled')
        with self.assertRaises(ValueError):restarted.resume(TOKEN,1,'cannot skip reconciliation')

    def test_deadline_and_single_read_budget(self):
        ident=self.submit();self.store.claim(ident)
        self.store.begin(ident,{'synthetic':True})
        with self.assertRaises(Stopped):self.store.begin(ident,{'synthetic':True})
        with patch('golden.pilot_control.time.time',return_value=10**12):
            with self.assertRaises(Stopped):self.store.check(ident)
            self.assertFalse(self.store.finish(ident,{'late':True}))

    def test_artifact_tampering_detected_and_event_rollback_atomic(self):
        ident=self.submit();self.store.claim(ident)
        with patch.object(self.store,'event',side_effect=RuntimeError('disk event failure')):
            with self.assertRaises(RuntimeError):self.store.finish(ident,{'ok':True})
        self.assertEqual(self.store.get(ident,'session')['state'],'running')
        self.store.finish(ident,{'ok':True})
        with self.store.tx() as db:db.execute('UPDATE jobs SET result=? WHERE id=?',('{"ok":false}',ident))
        with self.assertRaises(ValueError):self.store.get(ident,'session')
