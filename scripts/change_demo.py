#!/usr/bin/env python3
"""Synthetic in-memory workflow demonstration; NEVER production execution."""
import json
from golden.change import ChangeRun

run = ChangeRun('SYNTH-RUN-001')
run.evidence_ready()
run.set_draft({'change_id': 'SYNTH-001', 'system': 'DEMO_METROLOGY', 'revision': 'r2',
               'parameter': 'sample_count', 'value': 15})
run.validate(frozenset({'DEMO_METROLOGY'}))
run.review('fixture-independent-reviewer', is_independent=True)
exported = run.export()
print(json.dumps({'status': run.status, 'review_basis': 'unverified_caller_assertion',
                  'limitations': 'In memory, one-shot transitions, mutable events; no authenticated approval or audit integrity.',
                  'exported_local_draft': exported,
                  'events': run.events}, indent=2))
