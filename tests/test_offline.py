from pathlib import Path
from tempfile import TemporaryDirectory
from hashlib import sha256
import json
import shutil
import subprocess
import unittest
import zipfile

from scripts.verify_transfer import verify_transfer
from scripts.build_offline_bundle import build_bundle
from academy.assessment.check_submission import check, matches


class TransferTests(unittest.TestCase):
    def snapshot(self, root):
        (root / 'example.txt').write_bytes(b'synthetic')
        manifest = {'format_version': 1, 'files': {'example.txt': sha256(b'synthetic').hexdigest()}}
        (root / 'TRANSFER_MANIFEST.json').write_text(json.dumps(manifest))

    def test_transfer_detects_changed_missing_and_unexpected_files(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.snapshot(root)
            self.assertEqual(verify_transfer(root), [])
            (root / 'example.txt').write_text('changed')
            self.assertIn('changed: example.txt', verify_transfer(root))
            (root / 'example.txt').unlink()
            self.assertIn('missing/unreadable: example.txt', verify_transfer(root))
            (root / 'unlisted.txt').write_text('unlisted')
            self.assertIn('unexpected file: unlisted.txt', verify_transfer(root))

    def test_unsafe_manifest_path_and_local_results(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.snapshot(root)
            (root / 'workspace').mkdir()
            (root / 'workspace/my_solution.py').write_text('# learner work')
            self.assertEqual(verify_transfer(root), [])
            for name in ('../outside', '/absolute', 'C:/drive', 'scripts\\redirect', './example.txt'):
                (root / 'TRANSFER_MANIFEST.json').write_text(json.dumps({'format_version': 1, 'files': {name: '0'*64}}))
                self.assertTrue(any('unsafe manifest path' in e for e in verify_transfer(root)))

    def test_bad_manifest_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertTrue(verify_transfer(root))
            (root / 'TRANSFER_MANIFEST.json').write_text('{')
            self.assertTrue(verify_transfer(root))

    def test_manifest_symlink_refused(self):
        with TemporaryDirectory() as tmp, TemporaryDirectory() as outside:
            root = Path(tmp)
            self.snapshot(root)
            (root / 'example.txt').unlink()
            external = Path(outside) / 'synthetic.txt'
            external.write_bytes(b'synthetic')
            try:
                (root / 'example.txt').symlink_to(external)
            except OSError as error:
                self.skipTest(f'Symlink creation unavailable on this host: {error}')
            self.assertTrue(any('symlink refused' in e for e in verify_transfer(root)))

    @unittest.skipUnless(shutil.which('git'), 'Publisher-only packaging test needs Git')
    def test_committed_package_roundtrip_and_dirty_refusal(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / 'source'
            root.mkdir()
            def git(*args):
                subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
            git('init')
            (root / 'pyproject.toml').write_text('[project]\nversion="2.0.0"\n')
            (root / 'synthetic.txt').write_text('example')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'synthetic')
            archive = build_bundle(root, Path(tmp)/'bundle')
            with zipfile.ZipFile(archive) as z:
                z.extractall(Path(tmp)/'extract')
            extracted = next((Path(tmp)/'extract').iterdir())
            self.assertEqual(verify_transfer(extracted), [])
            self.assertTrue(archive.with_suffix('.zip.sha256').is_file())
            with self.assertRaises(ValueError):
                build_bundle(root, Path(tmp)/'bundle')
            (root / 'synthetic.txt').write_text('dirty')
            with self.assertRaises(ValueError):
                build_bundle(root, Path(tmp)/'other')


class AssessmentRunnerTests(unittest.TestCase):
    def test_wrong_types_and_missing_result_fields_fail(self):
        self.assertFalse(matches({'n': True}, {'n': 1}))
        self.assertFalse(matches({'n': float('nan')}, {'n': 1}))
        self.assertFalse(matches({}, {'n': 1}))
        self.assertFalse(matches({'n': 0}, {'n': None}))

    def test_blanket_rejection_cannot_pass_visible_assessment(self):
        def reject(_):
            raise ValueError('always rejects')
        results = check(reject)
        self.assertFalse(all(r['passed'] for r in results))
        self.assertFalse(next(r['passed'] for r in results if r['case'] == 'example'))
