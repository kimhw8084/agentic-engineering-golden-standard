#!/usr/bin/env python3
"""Lightweight structure and frontmatter check without external dependencies."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('AGENTS.md', 'README.md', 'docs/ARCHITECTURE.md',
            'docs/DEFINITION_OF_DONE.md', 'academy/README.md',
            'scripts/retrofit.py', 'tests/test_change.py', 'tests/test_retrieval.py')
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def verify() -> list[str]:
    errors = [f'missing {p}' for p in REQUIRED if not (ROOT / p).is_file()]
    for file in (ROOT / '.opencode/skills').glob('*/SKILL.md'):
        text = file.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            errors.append(f'{file}: missing yaml frontmatter')
            continue
        head = text.split('---', 2)[1]
        name = re.search(r'^name:\s*(.+)$', head, flags=re.M)
        desc = re.search(r'^description:\s*(.+)$', head, flags=re.M)
        if not name or name.group(1).strip() != file.parent.name or not NAME_RE.fullmatch(file.parent.name):
            errors.append(f'{file}: name mismatch')
        if not desc or not (1 <= len(desc.group(1)) <= 1024):
            errors.append(f'{file}: invalid description')
    if not list((ROOT / '.opencode/skills').glob('*/SKILL.md')):
        errors.append('No OpenCode skills found')
    for f in (ROOT / 'opencode.json', ROOT / 'examples/fixtures/evidence.json',
              ROOT / 'examples/fixtures/eval_cases.json'):
        try:
            json.loads(f.read_text(encoding='utf-8'))
        except Exception as ex:
            errors.append(f'{f}: bad JSON: {ex}')
    return errors


if __name__ == '__main__':
    problems = verify()
    for problem in problems:
        print('ERROR', problem)
    print(f'Golden structure: {"PASS" if not problems else "FAIL"} ({len(problems)} issues)')
    sys.exit(bool(problems))
