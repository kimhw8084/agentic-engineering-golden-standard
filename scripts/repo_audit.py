#!/usr/bin/env python3
"""Metadata-only reconnaissance: read filenames, never file contents.

This is NOT a security audit, proprietary code analysis, or secrets scanner.
"""
from pathlib import Path
import argparse
import json
from collections import Counter

EXCLUDED = {'.git', '.venv', 'node_modules', '__pycache__', '.next', 'dist', 'build', '.pytest_cache'}


def inventory(target: Path, max_files=10000) -> dict:
    target = target.resolve()
    if not target.is_dir():
        raise ValueError('Target must be existing directory')
    extensions = Counter()
    count = 0
    hit_limit = False
    # Symlink directory traversal is disabled, files are never opened.
    for folder, dirs, files in __import__('os').walk(target, followlinks=False):
        dirs[:] = [d for d in dirs if d not in EXCLUDED and not (Path(folder) / d).is_symlink()]
        for name in files:
            if (Path(folder) / name).is_symlink():
                continue
            count += 1
            extensions[Path(name).suffix.lower() or '(none)'] += 1
            if count >= max_files:
                hit_limit = True
                break
        if hit_limit:
            break
    checkpoints = ['AGENTS.md', 'opencode.json', 'pyproject.toml', 'requirements.txt',
                   '.github/workflows', 'tests', 'docs']
    return {'directory': str(target), 'files_counted': count,
            'truncated': hit_limit, 'extensions': dict(extensions.most_common(20)),
            'checkpoint_presence': {x: (target / x).exists() for x in checkpoints},
            'notes': ['No file contents or credentials read', 'Does not prove any feature works',
                      'Review Git, tests, source integrations manually in authorized environment']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()
    print(json.dumps(inventory(Path(args.target)), indent=2))
