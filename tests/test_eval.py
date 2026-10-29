import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from golden.eval import fixture_eval

ROOT = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def evaluate(self, cases, repeats=1):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cases.json'
            path.write_text(json.dumps(cases))
            return fixture_eval(ROOT/'examples/fixtures/evidence.json', path, repeats=repeats)

    def test_recall_counts_all_expected_and_mrr_excludes_abstentions(self):
        result = self.evaluate([
            {'id': 'miss', 'question': 'zzzz', 'roles': ['engineer'], 'expected': ['VAL-02']},
            {'id': 'abstain', 'question': 'zzzz', 'roles': [], 'expected': []},
            {'id': 'partial', 'question': 'SOP-3', 'roles': ['engineer'], 'expected': ['SOP-3', 'VAL-02']},
        ], repeats=3)
        self.assertEqual(result['mrr_at_k'], 0.5)
        self.assertEqual(result['recall_at_k'], 0.25)
        self.assertEqual(result['abstention_accuracy'], 1)
        self.assertEqual(result['latency_samples'], 9)
        self.assertGreaterEqual(result['latency_ms_p95'], result['latency_ms_p50'])
        self.assertIsNone(result['unmeasured']['task_success'])

    def test_bad_evaluation_inputs_fail_before_scoring(self):
        valid = {'id': 'x', 'question': 'a', 'roles': [], 'expected': []}
        for cases in ([], [valid, valid], [{**valid, 'expected': ['VAL-02']}],
                      [{**valid, 'roles': 'engineer'}], [{**valid, 'expected': None}]):
            with self.subTest(cases=cases), self.assertRaises(ValueError):
                self.evaluate(cases)
        for repeats in (0, True, 1001):
            with self.assertRaises(ValueError):
                self.evaluate([valid], repeats)

    def test_provenance_changes_with_fixture(self):
        case = {'id': 'x', 'question': 'a', 'roles': [], 'expected': []}
        first = self.evaluate([case])['provenance']
        second = self.evaluate([{**case, 'question': 'b'}])['provenance']
        self.assertNotEqual(first['cases_sha256'], second['cases_sha256'])
        self.assertEqual(first['records_sha256'], second['records_sha256'])

    def test_domain_benchmark_no_leaks(self):
        result = fixture_eval(ROOT/'examples/fixtures/evidence.json',
                              ROOT/'examples/fixtures/domain_cases.json')
        self.assertEqual(result['unauthorized_cases'], 0)
        self.assertEqual(result['hit_at_k'], 1)

    def test_legacy_hit_pass_does_not_establish_complete_dependencies(self):
        result = self.evaluate([{'id': 'partial', 'question': 'SOP-3', 'roles': ['engineer'],
                                 'expected': ['SOP-3', 'VAL-02']}])
        self.assertEqual(result['hit_at_k'], 1)
        self.assertEqual(result['recall_at_k'], 0.5)
