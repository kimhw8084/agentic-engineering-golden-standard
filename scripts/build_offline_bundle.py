"""Package one clean Git commit; uses only Python standard library and local Git."""
from pathlib import Path, PurePosixPath
from hashlib import sha256
import argparse
from io import BytesIO
import json
import subprocess
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build_bundle(root: Path, destination: Path) -> Path:
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    if git('status', '--porcelain', '--untracked-files=normal').strip():
        raise ValueError('Commit/reconcile all changes first; only a clean committed snapshot is packaged')
    commit = git('rev-parse', 'HEAD').decode().strip()
    source = zipfile.ZipFile(BytesIO(git('archive', '--format=zip', commit)))
    files = {}
    for entry in source.infolist():
        if entry.is_dir():
            continue
        if entry.filename == 'TRANSFER_MANIFEST.json':
            raise ValueError('TRANSFER_MANIFEST.json is reserved for generated snapshot metadata')
        path = PurePosixPath(entry.filename)
        if (path.is_absolute() or '..' in path.parts or '\\' in entry.filename
                or ':' in entry.filename or (entry.external_attr >> 16) & 0o170000 == 0o120000):
            raise ValueError(f'Unsafe/symlink archive entry: {entry.filename}')
        files[entry.filename] = source.read(entry)
    version = tomllib.loads(files['pyproject.toml'].decode())['project']['version']
    manifest = {'format_version': 1, 'standard_version': version, 'snapshot_commit': commit,
                'scope': 'Synthetic reference snapshot; no model binaries, credentials or enterprise approval.',
                'files': {name: sha256(data).hexdigest() for name, data in sorted(files.items())}}
    prefix = f'golden-standard-{version}-{commit[:7]}'
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f'{prefix}.zip'
    if archive.exists():
        raise ValueError(f'Refusing to overwrite {archive}')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
        for name, data in sorted(files.items()):
            output.writestr(f'{prefix}/{name}', data)
        output.writestr(f'{prefix}/TRANSFER_MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
    archive.with_suffix('.zip.sha256').write_text(f'{sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'out/transfer')
    args = parser.parse_args()
    print(build_bundle(ROOT, args.output))
