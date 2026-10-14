"""Exercise failure boundaries against real files, with injected I/O failures."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from research_workbench import store
from research_workbench.install import install
from research_workbench.render import render
from test_cli import batch, report


class Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name) / 'study'
        store.initialize(self.directory, 'Recovery test')
        store.ingest(self.directory, batch())

    def tearDown(self):
        self.tmp.cleanup()

    def test_failed_atomic_replace_keeps_original_and_releases_lock(self):
        path = self.directory / 'research.json'
        original = path.read_bytes()
        b = batch()
        item = b['interviews'][0]
        item['id'] = 'i2'
        with patch('research_workbench.store.os.replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                store.ingest(self.directory, {'interviews': [item]})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(self.directory.glob('.research.json-*')), [])
        self.assertEqual(store.ingest(self.directory, {'interviews': [item]})['revision'], 2)

    def test_interrupted_render_has_no_final_directory(self):
        original = (self.directory / 'research.json').read_bytes()
        with patch('research_workbench.render.document', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                render(self.directory, report(), 'both')
        self.assertEqual(list((self.directory / 'reports').iterdir()), [])
        self.assertEqual((self.directory / 'research.json').read_bytes(), original)
        result = render(self.directory, report(), 'both')
        self.assertEqual(Path(result['directory']).name, '001')
        self.assertEqual(store.load(self.directory)['revision'], 1)

    def test_user_install_uses_home_and_preserves_identical_files(self):
        home = Path(self.tmp.name) / 'home'
        with patch('research_workbench.install.Path.home', return_value=home):
            first = install('codex', 'user')
            second = install('codex', 'user')
        destination = Path(first['destination'])
        self.assertEqual(destination, (home / '.agents' / 'skills' / 'research-workbench').resolve())
        self.assertEqual(second['action'], 'unchanged')
        self.assertTrue((destination / 'references' / 'data-contract.md').exists())


if __name__ == '__main__':
    unittest.main()
