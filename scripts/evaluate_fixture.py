#!/usr/bin/env python3
"""Run a deterministic fixture eval. Execute from repository root."""
import argparse
from pathlib import Path
import json
from golden.eval import fixture_eval


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-hit', type=float, default=0.75)
    parser.add_argument('--top-k', type=int, default=3)
    opts = parser.parse_args()
    result = fixture_eval(Path('examples/fixtures/evidence.json'),
                          Path('examples/fixtures/eval_cases.json'), opts.top_k)
    print(json.dumps(result, indent=2))
    if result['hit_at_k'] < opts.min_hit or result['unauthorized_cases']:
        raise SystemExit('Fixture evaluation threshold failed')


if __name__ == '__main__':
    main()
