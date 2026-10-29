from http.client import HTTPConnection
import json
from pathlib import Path
import re
import sqlite3
from tempfile import TemporaryDirectory
from threading import Thread
import time
import unittest
from unittest.mock import patch

from golden.pilot_control import ControlStore
from scripts.investigation_app import make_server


class BrowserBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=ControlStore(Path(self.tmp.name)/'db.sqlite','synthetic-operator-token-0123456789')
        self.server=make_server(self.store)
        self.thread=Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.close)
        status,body,headers=self.request('GET','/')
        self.assertEqual(status,200)
        self.assertIn("frame-ancestors 'none'",headers['Content-Security-Policy'])
        self.token=re.search(r"const token='([^']+)'",body.decode())[1]

    def close(self):
        self.server.shutdown();self.server.server_close();self.server.pool.shutdown(wait=True)
        self.thread.join(2)

    def request(self,method,path,data=None,headers=None):
        connection=HTTPConnection('127.0.0.1',self.server.server_port,timeout=3)
        try:
            connection.request(method,path,body=json.dumps(data) if data is not None else None,headers=headers or {})
            response=connection.getresponse()
            return response.status,response.read(),dict(response.getheaders())
        finally:connection.close()

    def test_no_terminal_api_journey_revision_unknown_and_denied(self):
        headers={'X-Pilot-Token':self.token,'Idempotency-Key':'journey'}
        status,body,_=self.request('POST','/api/jobs',{'revision':'r2','parameter':'sample_count'},headers)
        self.assertEqual(status,202);ident=json.loads(body)['id']
        for _ in range(50):
            status,body,_=self.request('GET','/api/jobs/'+ident,headers=headers)
            result=json.loads(body)
            if result['state'] not in ('queued','running'):break
            time.sleep(.01)
        self.assertEqual(result['state'],'succeeded')
        self.assertEqual(result['result']['status'],'partial')
        self.assertEqual(result['result']['request']['revision'],'r2')
        self.assertTrue(result['artifact_hash'])
        # Exact retry replays the same job rather than creating another read.
        _,retry,_=self.request('POST','/api/jobs',{'revision':'r2','parameter':'sample_count'},headers)
        self.assertEqual(json.loads(retry)['id'],ident)

    def test_cross_origin_host_forgery_token_and_identity_fields_denied(self):
        request={'revision':'r1','parameter':'sample_count'}
        for headers in [{},{'X-Pilot-Token':'forged'},
                        {'X-Pilot-Token':self.token,'Origin':'https://attacker.invalid'},
                        {'X-Pilot-Token':self.token,'Host':'attacker.invalid'}]:
            status,_,_=self.request('POST','/api/jobs',request,headers)
            self.assertEqual(status,403)
        status,_,_=self.request('GET','/',headers={'Host':'lookalike.local'})
        self.assertEqual(status,403)
        status,_,_=self.request('POST','/api/jobs',{**request,'roles':['admin']},
                                {'X-Pilot-Token':self.token,'Idempotency-Key':'x'})
        self.assertEqual(status,400)

    def test_operator_stop_cannot_be_overridden_from_browser(self):
        self.store.stop('synthetic-operator-token-0123456789','HTTP drill')
        status,_,_=self.request('POST','/api/jobs',{'revision':'r1','parameter':'sample_count'},
                               {'X-Pilot-Token':self.token,'Idempotency-Key':'x'})
        self.assertEqual(status,409)
        status,_,_=self.request('POST','/api/resume',{}, {'X-Pilot-Token':self.token})
        self.assertEqual(status,404)
        self.assertEqual(self.store.inventory('synthetic-operator-token-0123456789')['operations'],[])

    def test_supervisor_failure_denies_admission_without_fallback(self):
        with patch.object(self.store,'submit',side_effect=sqlite3.OperationalError('synthetic outage')):
            status,_,_=self.request('POST','/api/jobs',{'revision':'r1','parameter':'sample_count'},
                                   {'X-Pilot-Token':self.token,'Idempotency-Key':'outage'})
        self.assertEqual(status,503)
        self.assertEqual(self.store.inventory('synthetic-operator-token-0123456789')['operations'],[])
