"""Windows-friendly single entry point; no downloads, model calls or installation."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--transfer', action='store_true', help='Require packaged snapshot integrity check first')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise SystemExit('Python 3.11+ required; use approved internal provisioning, not this script.')
    checks = []
    if args.transfer:
        checks.append(['scripts/verify_transfer.py'])
    checks += [['scripts/verify_standard.py'], ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
               ['-m', 'scripts.evaluate_fixture', '--min-hit', '0.85'],
               ['-m', 'scripts.evaluate_fixture', '--cases', 'examples/fixtures/domain_cases.json', '--min-hit', '1.0'],
               ['-m', 'scripts.change_demo'], ['-m', 'scripts.trace_demo'],
               ['-m', 'scripts.evaluate_investigation', '--repeats', '5']]
    for check in checks:
        print('RUN', sys.executable, *check, flush=True)
        result = subprocess.run([sys.executable, *check], cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)
    print('Offline preflight: PASS. Synthetic reference checks only; no production authorization.')


if __name__ == '__main__':
    main()
