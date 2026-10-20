"""Portable, deterministic evidence retrieval benchmark."""
from pathlib import Path
import json
import statistics
from time import perf_counter
from golden.retrieval import Evidence, EvidenceIndex


def fixture_eval(records_path: Path, cases_path: Path, top_k: int = 3) -> dict:
    records = [Evidence.from_dict(x) for x in json.loads(records_path.read_text())]
    cases = json.loads(cases_path.read_text())
    index = EvidenceIndex(records)
    latencies = []
    rr = []
    matched = 0
    unauthorized = 0
    details = []
    for case in cases:
        start = perf_counter()
        roles = frozenset(case['roles'])
        hits = index.search(case['question'], roles, top_k=top_k)
        elapsed_ms = (perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
        got = [h.record.record_id for h in hits]
        expected = case.get('expected', [])
        found = next((i + 1 for i, rid in enumerate(got) if rid in expected), None)
        hit = bool(found) if expected else not bool(got)
        matched += int(hit)
        rr.append((1 / found) if found else (1.0 if not expected and not got else 0.0))
        # An isolated test for accidental cross-role data exposure.
        visible_ids = {r.record_id for r in records if r.permitted_roles & roles}
        leaked = any(rid not in visible_ids for rid in got)
        unauthorized += int(leaked)
        details.append({'case': case['id'], 'passed': hit and not leaked, 'rank': found,
                        'got': got, 'expected': expected, 'leak': leaked})
    return {'cases': len(cases), 'hit_at_k': round(matched / len(cases), 3),
            'mrr_at_k': round(statistics.mean(rr), 3),
            'unauthorized_cases': unauthorized,
            'latency_ms_p50': round(statistics.median(latencies), 4),
            'latency_ms_max': round(max(latencies), 4), 'results': details,
            'disclaimer': 'Synthetic tiny-fixture lexical retrieval only; not production RAG/LLM accuracy.'}
