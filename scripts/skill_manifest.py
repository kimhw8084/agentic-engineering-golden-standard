"""Content-hashed skill publication manifest; no installation or external access."""
from pathlib import Path
import argparse
from hashlib import sha256
import json
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def build_manifest(root: Path = ROOT) -> dict:
    version = tomllib.loads((root / 'pyproject.toml').read_text())['project']['version']
    return {'manifest_version': 1, 'standard_version': version,
            'supporting_files': 'Pin all referenced guidance to the same reviewed Git commit.',
            'skills': {p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest()
                       for p in sorted((root / '.opencode/skills').glob('*/SKILL.md'))}}


def manifest_errors(root: Path = ROOT) -> list[str]:
    try:
        actual = json.loads((root / '.opencode/skills-manifest.json').read_text())
        return [] if actual == build_manifest(root) else ['skill manifest drift; review changes then regenerate']
    except (OSError, ValueError) as error:
        return [f'invalid skill manifest: {error}']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.write:
        (ROOT / '.opencode/skills-manifest.json').write_text(json.dumps(build_manifest(), indent=2) + '\n')
    errors = manifest_errors()
    print('\n'.join(errors) if errors else 'Skill manifest: PASS')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
