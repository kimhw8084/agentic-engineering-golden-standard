"""Regressions for integrity defects observed in v1; original tests remain intact."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from golden.change import ChangeRun, GateError
from golden.retrieval import Evidence, EvidenceIndex
from scripts.retrofit import retrofit

VALID = {'change_id': 'TEST', 'system': 'DEMO', 'revision': 'r1', 'parameter': 'x', 'value': 2}


class IntegrityTests(unittest.TestCase):
    def drafted(self):
        run = ChangeRun('test')
        run.evidence_ready()
        run.set_draft(VALID)
        return run

    def test_serialization_failure_is_atomic(self):
        for value in (object(), float('nan')):
            run = self.drafted()
            before = (run.status, run.draft.copy(), run.draft_hash, list(run.events))
            with self.assertRaises((TypeError, ValueError)):
                run.set_draft({**VALID, 'value': value})
            self.assertEqual(before, (run.status, run.draft, run.draft_hash, run.events))

    def test_mutation_before_validation_rejected(self):
        run = self.drafted()
        run.draft['value'] = 3
        with self.assertRaises(GateError):
            run.validate(frozenset({'DEMO'}))
        self.assertEqual(run.status, 'drafted')

    def test_mutation_before_review_rejected(self):
        run = self.drafted()
        run.validate(frozenset({'DEMO'}))
        run.draft['value'] = 3
        with self.assertRaises(GateError):
            run.review('reviewer', True)
        self.assertEqual(run.status, 'validated')

    def test_review_assertion_is_strict_but_not_identity(self):
        run = self.drafted()
        run.validate(frozenset({'DEMO'}))
        for reviewer, flag in [(' ', True), ('r', 'true'), ('r', 1), (42, True)]:
            with self.assertRaises(GateError):
                run.review(reviewer, flag)
        run.review('any-caller-can-assert-this', True)
        self.assertEqual(run.events[-1]['review_basis'], 'unverified_caller_assertion')

    def test_export_is_one_shot_not_retry_idempotency(self):
        run = self.drafted()
        run.validate(frozenset({'DEMO'}))
        run.review('r', True)
        run.export()
        with self.assertRaises(GateError):
            run.export()

    def test_identifier_substring_has_no_exact_boost(self):
        records = [Evidence(i, 'demo', 'r1', '', frozenset({'r'}), 'synthetic')
                   for i in ('JOB-1', 'JOB-10')]
        hits = EvidenceIndex(records).search('JOB-10', frozenset({'r'}))
        self.assertEqual([h.record.record_id for h in hits], ['JOB-10'])

    def test_repeated_install_preserves_config_and_skills(self):
        with TemporaryDirectory() as tmp:
            target = Path(tmp)
            for name in ('AGENTS.md', 'opencode.json'):
                (target / name).write_text('custom')
            retrofit(target, apply=True)
            again = retrofit(target, apply=True)
            self.assertTrue(all(x['status'] == 'skip-existing' for x in again['files']))
            for name in ('AGENTS.md', 'opencode.json'):
                self.assertEqual((target / name).read_text(), 'custom')

    def test_install_refuses_symlink_directory_and_dangling_file(self):
        with TemporaryDirectory() as tmp, TemporaryDirectory() as outside:
            target, external = Path(tmp), Path(outside)
            (target / 'docs').symlink_to(external, target_is_directory=True)
            template = target / 'templates/ADR.md'
            template.parent.mkdir()
            template.symlink_to(external / 'missing')
            result = retrofit(target, apply=True)
            self.assertEqual(list(external.iterdir()), [])
            self.assertEqual(next(x['status'] for x in result['files']
                                  if x['path'] == 'templates/ADR.md'), 'skip-symlink')
