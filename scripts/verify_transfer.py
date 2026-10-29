"""Verify an extracted, immutable offline snapshot. No network or credentials."""
from pathlib import Path, PurePosixPath
from hashlib import sha256
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def verify_transfer(root: Path) -> list[str]:
    root = root.resolve()
    try:
        manifest = json.loads((root / 'TRANSFER_MANIFEST.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        return [f'manifest unreadable: {error}']
    if (not isinstance(manifest, dict) or manifest.get('format_version') != 1
            or not isinstance(manifest.get('files'), dict) or not manifest['files']):
        return ['invalid transfer manifest']
    errors = []
    for name, digest in manifest['files'].items():
        relative = PurePosixPath(name)
        if (not name or '\\' in name or ':' in name or relative.is_absolute()
                or '..' in relative.parts or str(relative) != name):
            errors.append(f'unsafe manifest path: {name}')
            continue
        path = root.joinpath(*relative.parts)
        if any(root.joinpath(*relative.parts[:i]).is_symlink()
               for i in range(1, len(relative.parts) + 1)):
            errors.append(f'symlink refused: {name}')
            continue
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append(f'invalid digest: {name}')
            continue
        try:
            if sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f'changed: {name}')
        except OSError:
            errors.append(f'missing/unreadable: {name}')
    # Intentional local results and learner work are outside the immutable snapshot.
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if (relative.parts[0] in {'out', 'results', 'workspace', '.git'}
                or '__pycache__' in relative.parts):
            continue
        name = relative.as_posix()
        if path.is_symlink():
            errors.append(f'unexpected symlink: {name}')
        elif path.is_file() and name not in manifest['files'] and name != 'TRANSFER_MANIFEST.json':
            errors.append(f'unexpected file: {name}')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = verify_transfer(args.root)
    for error in errors:
        print('ERROR', error)
    print(f'Transfer integrity: {"PASS" if not errors else "FAIL"} ({len(errors)} issues)')
    print('Checksums detect changes against this manifest; they do not authenticate publisher approval.')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
