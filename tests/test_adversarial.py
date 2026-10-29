"""Cold counterexamples, including explicit tests of the teaching boundary."""
from copy import deepcopy
import unittest

from golden.change import ChangeRun, canonical_hash
from golden.retrieval import Evidence, EvidenceIndex
from golden.tools import ToolPolicy, ToolDenied
from scripts.trace_demo import DEFINITION


class AdversarialTests(unittest.TestCase):
    def test_string_scope_substring_cannot_authorize(self):
        policy = ToolPolicy('offline', 'lookup_synthetic', canonical_hash(DEFINITION),
                            frozenset({'evidence:read'}), frozenset({'synthetic'}))
        for scopes in ('not-evidence:read', ['evidence:read'], None, frozenset({1})):
            with self.subTest(scopes=scopes), self.assertRaises(ToolDenied):
                policy.check(server_id='offline', definition=DEFINITION,
                             actor_scopes=scopes, required_scope='evidence:read',
                             classification='synthetic', calls_used=0, remaining_ms=1)

    def test_malformed_evidence_fails_at_ingestion(self):
        valid = dict(record_id='X', source='synthetic', revision='r1', text='',
                     permitted_roles=['engineer'], timestamp='synthetic')
        for changes in ({'permitted_roles': 'engineer'}, {'revision': None},
                        {'text': []}, {'record_id': ' '}, {'extra': 'instruction'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                Evidence.from_dict({**valid, **changes})

    def test_caller_can_impersonate_role_in_teaching_index(self):
        index = EvidenceIndex([Evidence('X', 'demo', 'r1', 'secret',
                                       frozenset({'owner'}), 'synthetic')])
        self.assertEqual(index.search('secret', frozenset()), [])
        self.assertEqual(len(index.search('secret', frozenset({'owner'}))), 1)
        # Deliberately demonstrates an unresolved identity boundary, not an ACL claim.

    def test_recomputed_hashes_bypass_mutable_toy_not_security_boundary(self):
        run = ChangeRun('synthetic')
        run.evidence_ready()
        run.set_draft(dict(change_id='X', system='D', revision='r1', parameter='x', value=1))
        run.validate(frozenset({'D'})); run.review('author-asserted-other-name', True)
        run.draft['value'] = 99
        run.draft_hash = run.validated_hash = run.approval_hash = canonical_hash(run.draft)
        self.assertEqual(run.export()['value'], 99)

    def test_definition_pin_includes_nested_schema(self):
        policy = ToolPolicy('offline', 'lookup_synthetic', canonical_hash(DEFINITION),
                            frozenset({'evidence:read'}), frozenset({'synthetic'}))
        altered = deepcopy(DEFINITION); altered['input_schema'] = {'x': 'exfiltrate'}
        with self.assertRaises(ToolDenied):
            policy.check(server_id='offline', definition=altered,
                         actor_scopes=frozenset({'evidence:read'}), required_scope='evidence:read',
                         classification='synthetic', calls_used=0, remaining_ms=1)

    def test_legacy_retrieval_does_not_select_revision(self):
        index = EvidenceIndex([Evidence('X-old', 'demo', 'r1', 'sample_count',
                                       frozenset({'r'}), 'synthetic'),
                               Evidence('X-new', 'demo', 'r2', 'sample_count',
                                       frozenset({'r'}), 'synthetic')])
        self.assertEqual({h.record.revision for h in index.search('sample_count', frozenset({'r'}))},
                         {'r1', 'r2'})
