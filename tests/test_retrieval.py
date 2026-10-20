import json
from pathlib import Path
import unittest
from golden.retrieval import Evidence, EvidenceIndex
from golden.eval import fixture_eval

ROOT = Path(__file__).resolve().parents[1]

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.records = [Evidence.from_dict(x) for x in json.loads((ROOT / 'examples/fixtures/evidence.json').read_text())]
        self.index = EvidenceIndex(self.records)

    def test_identifier_ranked_first(self):
        h = self.index.search('Explain JOB-1042 failure', frozenset({'engineer'}))
        self.assertEqual(h[0].record.record_id, 'JOB-1042')

    def test_roles_filter_before_scoring(self):
        h = self.index.search('EMAIL-SECRET budget', frozenset({'engineer'}))
        self.assertFalse(any(x.record.record_id == 'EMAIL-SECRET' for x in h))

    def test_no_roles_no_results(self):
        self.assertEqual(self.index.search('SOP-3', frozenset()), [])

    def test_blank_query(self):
        self.assertEqual(self.index.search('  ', frozenset({'engineer'})), [])

    def test_duplicate_id_fail(self):
        with self.assertRaises(ValueError): EvidenceIndex([self.records[0], self.records[0]])

    def test_unbounded_k_fail(self):
        with self.assertRaises(ValueError): self.index.search('job', frozenset({'engineer'}), 10000)

    def test_bad_input_fail(self):
        with self.assertRaises(ValueError): Evidence.from_dict({'record_id':'x'})

    def test_fixture_benchmark(self):
        result = fixture_eval(ROOT/'examples/fixtures/evidence.json', ROOT/'examples/fixtures/eval_cases.json')
        self.assertEqual(result['hit_at_k'], 1.0)
        self.assertEqual(result['unauthorized_cases'], 0)

if __name__ == '__main__': unittest.main()
