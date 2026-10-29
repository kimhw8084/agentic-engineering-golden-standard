"""Visible local self-checks, not an independent/human assessment or sandbox."""
from pathlib import Path
import argparse
import importlib.util
import math

BASE = dict(tasks_per_month=40, manual_minutes=20, assisted_minutes=6,
            review_minutes=4, rework_minutes=2, support_minutes_per_month=120, build_minutes=480)


def cases():
    return [
        ('example', BASE, {'status': 'pilot_candidate', 'net_minutes_per_month': 200, 'break_even_months': 2.4}),
        ('unknown', {**BASE, 'build_minutes': None}, {'status': 'insufficient_evidence'}),
        ('zero-volume', {**BASE, 'tasks_per_month': 0}, {'status': 'no_measured_benefit', 'net_minutes_per_month': -120, 'break_even_months': None}),
        ('zero-build', {**BASE, 'build_minutes': 0}, {'status': 'pilot_candidate', 'net_minutes_per_month': 200, 'break_even_months': 0}),
        ('zero-net', {**BASE, 'support_minutes_per_month': 320}, {'status': 'no_measured_benefit', 'net_minutes_per_month': 0, 'break_even_months': None}),
        ('bool', {**BASE, 'manual_minutes': True}, ValueError),
        ('fractional-tasks', {**BASE, 'tasks_per_month': 1.5}, ValueError),
        ('negative', {**BASE, 'review_minutes': -1}, ValueError),
        ('infinity', {**BASE, 'manual_minutes': float('inf')}, ValueError),
        ('nan', {**BASE, 'manual_minutes': float('nan')}, ValueError),
        ('unknown-with-invalid', {**BASE, 'build_minutes': None, 'review_minutes': -1}, ValueError),
        ('unknown-field', {**BASE, 'approved': True}, ValueError),
        ('missing', {k: v for k, v in BASE.items() if k != 'review_minutes'}, ValueError),
        ('not-object', [], ValueError),
        ('overflow', {**BASE, 'manual_minutes': 1e308, 'tasks_per_month': 100}, ValueError),
    ]


def matches(actual, expected):
    if not isinstance(actual, dict) or actual.keys() != expected.keys():
        return False
    for key, value in expected.items():
        got = actual[key]
        if isinstance(value, (int, float)):
            if type(got) not in (int, float) or not math.isfinite(got) or not math.isclose(got, value, rel_tol=1e-9, abs_tol=1e-9):
                return False
        elif got != value:
            return False
    return True


def check(assess):
    results = []
    for name, case, expected in cases():
        try:
            actual = assess(case.copy() if isinstance(case, dict) else case)
            passed = expected is not ValueError and matches(actual, expected)
        except ValueError:
            passed = expected is ValueError
        except Exception:
            passed = False
        results.append({'case': name, 'passed': passed})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('submission', type=Path)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('learner_submission', args.submission)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = check(module.assess)
    for result in results:
        print('PASS' if result['passed'] else 'FAIL', result['case'])
    print('Visible checks only. Human independence, transfer and defense remain unassessed.')
    raise SystemExit(not all(r['passed'] for r in results))
