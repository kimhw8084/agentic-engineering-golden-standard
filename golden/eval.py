"""Portable, deterministic evidence retrieval benchmark."""
from pathlib import Path
import json
import statistics
from hashlib import sha256
from math import ceil
import platform
from time import perf_counter
from golden import __version__
from golden.retrieval import Evidence, EvidenceIndex


def fixture_eval(records_path: Path, cases_path: Path, top_k: int = 3, repeats: int = 1) -> dict:
    if type(repeats) is not int or not 1 <= repeats <= 1000:
        raise ValueError('repeats must be integer 1..1000')
    if type(top_k) is not int or not 1 <= top_k <= 100:
        raise ValueError('top_k must be integer 1..100')
    records_bytes, cases_bytes = records_path.read_bytes(), cases_path.read_bytes()
    records = [Evidence.from_dict(x) for x in json.loads(records_bytes)]
    cases = json.loads(cases_bytes)
    if not isinstance(cases, list) or not cases:
        raise ValueError('cases must be a nonempty list')
    case_ids = set()
    for case in cases:
        if (not isinstance(case, dict) or not isinstance(case.get('id'), str)
                or not case['id'].strip() or case['id'] in case_ids
                or not isinstance(case.get('question'), str)
                or not isinstance(case.get('slice', 'legacy'), str)
                or any(not isinstance(case.get(k), list)
                       or any(not isinstance(v, str) or not v for v in case[k])
                       for k in ('roles', 'expected'))):
            raise ValueError('invalid/duplicate case or missing roles/expected labels')
        case_ids.add(case['id'])
        visible = {r.record_id for r in records if r.permitted_roles & set(case['roles'])}
        if not set(case['expected']) <= visible:
            raise ValueError('expected evidence must exist and be visible to case roles')
    index = EvidenceIndex(records)
    latencies = []
    rr = []
    matched = 0
    unauthorized = 0
    details = []
    for case in cases:
        roles = frozenset(case['roles'])
        for _ in range(repeats):
            start = perf_counter()
            hits = index.search(case['question'], roles, top_k=top_k)
            latencies.append((perf_counter() - start) * 1000)
        got = [h.record.record_id for h in hits]
        expected = case.get('expected', [])
        found = next((i + 1 for i, rid in enumerate(got) if rid in expected), None)
        hit = bool(found) if expected else not bool(got)
        matched += int(hit)
        if expected:
            rr.append((1 / found) if found else 0.0)
        # An isolated test for accidental cross-role data exposure.
        visible_ids = {r.record_id for r in records if r.permitted_roles & roles}
        leaked = any(rid not in visible_ids for rid in got)
        unauthorized += int(leaked)
        details.append({'case': case['id'], 'slice': case.get('slice', 'legacy'),
                        'passed': hit and not leaked, 'rank': found,
                        'recall_at_k': len(set(got) & set(expected)) / len(set(expected)) if expected else None,
                        'precision_at_k': len(set(got) & set(expected)) / len(got) if expected and got else (0.0 if expected else None),
                        'got': got, 'expected': expected, 'leak': leaked})
    def mean(values):
        return round(statistics.mean(values), 4) if values else None
    negatives = [d for d in details if not d['expected']]
    slices = {s: {'cases': sum(d['slice'] == s for d in details),
                  'passed': sum(d['passed'] for d in details if d['slice'] == s)}
              for s in sorted({d['slice'] for d in details})}
    return {'cases': len(cases), 'hit_at_k': round(matched / len(cases), 3),
            'metric_note': 'hit_at_k retains legacy hit-or-correct-abstention rate; MRR/recall/precision use answerable cases only.',
            'mrr_at_k': mean(rr),
            'recall_at_k': mean([d['recall_at_k'] for d in details if d['expected']]),
            'precision_at_k': mean([d['precision_at_k'] for d in details if d['expected']]),
            'abstention_accuracy': mean([int(not d['got']) for d in negatives]),
            'unauthorized_cases': unauthorized,
            'latency_ms_p50': round(statistics.median(latencies), 4),
            'latency_ms_p95': round(sorted(latencies)[ceil(0.95 * len(latencies)) - 1], 4),
            'latency_ms_max': round(max(latencies), 4), 'latency_samples': len(latencies),
            'percentile_method': 'p50 median; p95 nearest-rank; query-only warm process, no index construction',
            'slices': slices, 'results': details,
            'provenance': {'records_sha256': sha256(records_bytes).hexdigest(),
                           'cases_sha256': sha256(cases_bytes).hexdigest(),
                           'implementation_sha256': {name: sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                                                     for name in ('eval.py', 'retrieval.py')},
                           'standard_version': __version__, 'python': platform.python_version(),
                           'top_k': top_k, 'repeats': repeats, 'model': None,
                           'trial_kind': 'deterministic retrieval, not repeated model trials'},
            'unmeasured': {'answer_correctness': None, 'citation_grounding': None, 'task_success': None,
                           'reason': 'No answer generator, model or end-to-end employee workflow invoked.'},
            'usage': {'retrieval_calls': len(latencies), 'external_tool_calls': 0,
                      'model_calls': 0, 'model_tokens': 0, 'model_cost': 0,
                      'cost_basis': 'No billed services invoked; local compute/labor cost not measured.'},
            'disclaimer': 'Synthetic tiny-fixture lexical retrieval only; not production RAG/LLM accuracy.'}
