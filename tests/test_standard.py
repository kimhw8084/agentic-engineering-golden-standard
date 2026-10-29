from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.skill_manifest import build_manifest, manifest_errors
from scripts import verify_standard


class PublicationTests(unittest.TestCase):
    def test_checked_in_standard_and_manifest(self):
        self.assertEqual(verify_standard.verify(), [])
        self.assertTrue(all('\\' not in name for name in build_manifest()['skills']))

    def test_missing_and_changed_skill_detected(self):
        import json
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'pyproject.toml').write_text('[project]\nversion="2.0.0"\n')
            skill = root / '.opencode/skills/example/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('first')
            manifest = root / '.opencode/skills-manifest.json'
            manifest.write_text(json.dumps(build_manifest(root)))
            self.assertEqual(manifest_errors(root), [])
            skill.write_text('poisoned')
            self.assertTrue(manifest_errors(root))
            skill.unlink()
            self.assertTrue(manifest_errors(root))
