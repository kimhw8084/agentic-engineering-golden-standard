from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.retrofit import retrofit
from scripts.repo_audit import inventory

class BrownfieldTests(unittest.TestCase):
    def test_dry_run_does_not_change_target(self):
        with TemporaryDirectory() as temp:
            t=Path(temp)
            result=retrofit(t)
            self.assertTrue(all(x['status']=='would-copy' for x in result['files']))
            self.assertEqual(list(t.iterdir()), [])

    def test_apply_does_not_overwrite(self):
        with TemporaryDirectory() as temp:
            t=Path(temp)
            file=t/'.opencode/commands/golden-audit.md'
            file.parent.mkdir(parents=True)
            file.write_text('already customized')
            result=retrofit(t,apply=True)
            self.assertEqual(file.read_text(),'already customized')
            self.assertIn('skip-existing', {r['status'] for r in result['files']})
            self.assertIn('copied', {r['status'] for r in result['files']})

    def test_inventory_never_reads_contents(self):
        with TemporaryDirectory() as temp:
            (Path(temp)/'very_sensitive.txt').write_text('DO NOT READ')
            result=inventory(Path(temp))
            self.assertEqual(result['files_counted'],1)
            self.assertNotIn('DO NOT READ',repr(result))

if __name__ == '__main__':unittest.main()
