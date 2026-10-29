#!/usr/bin/env python3
"""Lightweight structure and frontmatter check without external dependencies."""
from pathlib import Path
import json
import re
import sys
import tomllib

# Support both direct script invocation and python -m scripts.verify_standard.
if __package__:
    from .skill_manifest import manifest_errors
else:
    from skill_manifest import manifest_errors

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('AGENTS.md', 'README.md', 'docs/ARCHITECTURE.md',
            'docs/DEFINITION_OF_DONE.md', 'academy/README.md',
            'scripts/retrofit.py', 'tests/test_change.py', 'tests/test_retrieval.py',
            '.github/CODEOWNERS', 'CHANGELOG.md', 'docs/GOVERNANCE.md', 'docs/GLOSSARY.md',
            'docs/V1_GAP_MATRIX.md', 'docs/MIGRATION_V2.md', 'docs/RUNTIME_CONTRACTS.md',
            'docs/AGENT_PATTERNS.md', 'docs/CONTEXT_ENGINEERING.md', 'docs/TOOL_TRUST.md',
            'docs/PRODUCT_DELIVERY.md', 'docs/SKILL_PUBLICATION.md', 'docs/V2_VERIFICATION.md')
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def verify() -> list[str]:
    errors = [f'missing {p}' for p in REQUIRED if not (ROOT / p).is_file()]
    version = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['version']
    package_version = re.search(r'^__version__ = "([^"]+)"',
                                (ROOT / 'golden/__init__.py').read_text(), flags=re.M)
    if not package_version or package_version.group(1) != version:
        errors.append('package version differs from pyproject.toml')
    if f'## {version}' not in (ROOT / 'CHANGELOG.md').read_text():
        errors.append('version missing from changelog')
    errors.extend(manifest_errors(ROOT))
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
