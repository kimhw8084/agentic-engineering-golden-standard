#!/usr/bin/env python3
"""Opt-in, no-overwrite skill/command installer for a brownfield repository.

Default mode is read-only. Copies only missing skills, commands, agents,
guidance documents, academy and templates. Never overwrites AGENTS.md,
opencode.json, source code, fixtures, secrets or model configuration. Does not require GitHub access.
"""
from pathlib import Path
import argparse
import json
import shutil

SRC = Path(__file__).resolve().parents[1]


def retrofit(target: Path, apply: bool = False) -> dict:
    target = target.resolve()
    if not target.is_dir():
        raise ValueError('Target must exist and be a directory')
    if target == SRC or SRC in target.parents:
        raise ValueError('Target must be a separate repository')
    manifest = []
    folders = [SRC / '.opencode' / component for component in ('skills', 'commands', 'agents')]
    folders += [SRC / component for component in ('docs', 'academy', 'templates')]
    for folder in folders:
        for file in sorted(p for p in folder.rglob('*') if p.is_file()):
            relative = file.relative_to(SRC)
            dest = target / relative
            # Refuse directory and dangling-file symlinks before any mkdir/copy.
            # This is a single-process installer, not a defense against concurrent
            # hostile filesystem replacement between check and copy.
            parts = [target.joinpath(*relative.parts[:i]) for i in range(1, len(relative.parts) + 1)]
            if any(p.is_symlink() for p in parts):
                status = 'skip-symlink'
            elif dest.exists():
                status = 'skip-existing'
            elif apply:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
                status = 'copied'
            else:
                status = 'would-copy'
            manifest.append({'path': str(relative), 'status': status})
    return {'target': str(target), 'mode': 'apply' if apply else 'dry-run',
            'note': 'Review copied files and existing AGENTS.md/config manually; never overwrite existing files.',
            'files': manifest}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Path to an EXISTING project directory')
    parser.add_argument('--apply', action='store_true', help='Explicitly install new files only')
    args = parser.parse_args()
    print(json.dumps(retrofit(Path(args.target), args.apply), indent=2))


if __name__ == '__main__':
    main()
