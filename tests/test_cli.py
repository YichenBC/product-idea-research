import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def batch():
    return {
        'recipe': {'id': 'r1', 'question': 'Test <script>alert(1)</script>', 'method': 'Compare roles',
                   'dimensions': [{'name': 'role', 'values': ['user', 'buyer']}],
                   'constraints': ['No browsing'], 'persona_count': 2, 'language': 'en'},
        'personas': [{'id': 'p1', 'label': 'User', 'recipe_id': 'r1', 'traits': {'role': 'user'},
                      'attributes': [{'name': 'workflow', 'value': '[click](https://evil.test)',
                                      'basis': 'assumed', 'rationale': 'Scenario'}]}],
        'interviews': [{'id': 'i1', 'persona_id': 'p1', 'synthetic': True,
                        'turns': [{'question': 'Why?', 'answer': '<img src=x onerror=alert(1)>', 'assumptions': ['Assumption']},
                                  {'question': 'Alternative?', 'answer': 'Existing sheet', 'assumptions': []}]}]}


def report():
    return {'title': 'Test report', 'study_revision': 1, 'status': 'partial', 'summary': 'Hypothesis',
            'interview_ids': ['i1'], 'findings': [{'id': 'f1', 'kind': 'simulation', 'statement': 'May be useful',
             'support': [{'interview_id': 'i1', 'turn': 1}], 'counterevidence': [{'interview_id': 'i1', 'turn': 2}],
             'limitations': ['Synthetic']}], 'next_steps': ['Ask real users'], 'limitations': ['Not validation']}


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.study = self.root / 'study'
        self.env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, code=0):
        p = subprocess.run([sys.executable, '-m', 'research_workbench', *map(str, args)],
                           cwd=self.root, env=self.env, text=True, capture_output=True)
        self.assertEqual(p.returncode, code, p.stdout + p.stderr)
        self.assertNotIn('Traceback', p.stderr)
        return json.loads(p.stdout if code == 0 else p.stderr)

    def write(self, name, value):
        p = self.root / name
        p.write_text(json.dumps(value), encoding='utf-8')
        return p

    def initialize(self):
        self.cli('init', self.study, '--title', 'Study')

    def ingest(self, data=None):
        return self.cli('ingest', self.study, '--file', self.write('batch.json', data or batch()))

    def ready(self):
        self.initialize()
        self.ingest()
        return self.write('report.json', report())


class CLI(Harness):
    def test_initial_checkpoint_and_idempotency(self):
        self.initialize()
        self.cli('check', self.study)
        self.assertEqual(self.cli('status', self.study)['revision'], 0)
        self.ingest()
        before = (self.study / 'research.json').read_bytes()
        self.ingest()
        self.assertEqual(before, (self.study / 'research.json').read_bytes())
        self.assertEqual(self.cli('status', self.study, '--json')['revision'], 1)
        self.cli('ingest', self.study, '--file', self.write('empty.json', {'personas': []}))
        self.assertEqual(before, (self.study / 'research.json').read_bytes())

    def test_failed_batch_is_all_or_nothing(self):
        self.ready()
        before = (self.study / 'research.json').read_bytes()
        b = batch()
        b['personas'][0]['id'] = 'p2'
        b['interviews'][0]['id'] = 'i2'
        b['interviews'][0]['persona_id'] = 'missing'
        self.cli('ingest', self.study, '--file', self.write('bad.json', b), code=1)
        self.assertEqual(before, (self.study / 'research.json').read_bytes())

    def test_nested_invalid_contracts_are_structured_errors(self):
        self.initialize()
        mutations = [
            lambda b: b['recipe'].update(persona_count=True),
            lambda b: b['recipe']['dimensions'][0].update(extra='x'),
            lambda b: b['personas'][0]['attributes'][0].update(basis='observed'),
            lambda b: b['personas'][0].update(traits={'role': []}),
            lambda b: b['interviews'][0].update(synthetic=1),
            lambda b: b['interviews'][0]['turns'][0].update(extra='x'),
            lambda b: b['personas'][0].update(id='r1'),
            lambda b: b['recipe'].update(language=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                b = batch()
                mutate(b)
                result = self.cli('ingest', self.study, '--file', self.write('bad.json', b), code=1)
                self.assertIn('error', result)
        self.assertEqual(self.cli('status', self.study)['revision'], 0)

    def test_conflicting_immutable_record(self):
        self.ready()
        b = batch()
        b['personas'][0]['label'] = 'Changed'
        self.cli('ingest', self.study, '--file', self.write('bad.json', b), code=1)

    def test_report_completeness_staleness_and_reference_validation(self):
        rp = self.ready()
        self.cli('check', self.study, '--report', rp)
        for mutate in [lambda r: r.update(status='complete'), lambda r: r.update(study_revision=0),
                       lambda r: r['findings'][0]['support'][0].update(turn=True),
                       lambda r: r['findings'][0]['support'][0].update(turn=3),
                       lambda r: r['findings'][0]['support'][0].update(interview_id='missing'),
                       lambda r: r['findings'][0].update(kind='observed'),
                       lambda r: r.update(unknown=1)]:
            r = report()
            mutate(r)
            self.cli('check', self.study, '--report', self.write('bad-report.json', r), code=1)

    def test_render_escaped_transcripts_and_immutable_snapshots(self):
        rp = self.ready()
        self.cli('render', self.study, '--report', rp)
        first = self.study / 'reports' / '001'
        old = {p.name: p.read_bytes() for p in first.iterdir()}
        html = (first / 'report.html').read_text(encoding='utf-8')
        md = (first / 'report.md').read_text(encoding='utf-8')
        self.assertNotIn('<script>', html)
        self.assertNotIn('<img src=', html)
        self.assertIn('&lt;img', html)
        self.assertIn('Existing sheet', html)
        self.assertIn('href="#turn-', html)
        self.assertNotIn('[click](https://evil.test)', md)
        self.assertIn('Existing sheet', md)
        self.cli('render', self.study, '--report', rp, '--format', 'md')
        self.assertTrue((self.study / 'reports' / '002' / 'report.md').exists())
        self.assertFalse((self.study / 'reports' / '002' / 'report.html').exists())
        self.assertEqual(old, {p.name: p.read_bytes() for p in first.iterdir()})

    def test_malformed_json_and_missing_study(self):
        p = self.root / 'broken.json'
        p.write_text('{broken', encoding='utf-8')
        self.initialize()
        self.cli('ingest', self.study, '--file', p, code=1)
        self.cli('status', self.root / 'missing', code=1)
        self.cli('init', self.study, '--title', 'Again', code=1)
        self.cli('init', self.root / 'empty', '--title', ' ', code=1)

    def test_installer_dry_run_idempotency_and_conflict(self):
        for target, dirname in [('codex', '.agents'), ('claude', '.claude')]:
            args = ['install', '--target', target, '--scope', 'project', '--directory', self.root]
            self.cli(*args, '--dry-run')
            path = self.root / dirname / 'skills' / 'research-workbench'
            self.assertFalse(path.exists())
            self.cli(*args)
            self.assertTrue((path / 'SKILL.md').exists())
            self.cli(*args)
            (path / 'SKILL.md').write_text('changed', encoding='utf-8')
            self.cli(*args, code=1)
            self.assertEqual((path / 'SKILL.md').read_text(encoding='utf-8'), 'changed')
        self.cli('install', '--target', 'codex', '--scope', 'user', '--directory', self.root, code=1)

class AdditionalCLI(Harness):
    def test_invalid_noop_does_not_bypass_strict_types(self):
        self.ready()
        b = batch()
        b['interviews'][0]['synthetic'] = 1
        self.cli('ingest', self.study, '--file', self.write('bad-noop.json', b), code=1)

    def test_duplicate_json_keys_and_nonfinite_numbers(self):
        self.initialize()
        path = self.root / 'bad.json'
        for text in ['{"personas":[],"personas":[]}', '{"recipe":NaN}', '[]', 'null', '42']:
            path.write_text(text, encoding='utf-8')
            self.cli('ingest', self.study, '--file', path, code=1)

    def test_complete_report_and_snapshot_does_not_change_after_append(self):
        self.ready()
        b = batch()
        b.pop('recipe')
        b['personas'][0]['id'] = 'p2'
        b['personas'][0]['traits']['role'] = 'buyer'
        b['interviews'][0]['id'] = 'i2'
        b['interviews'][0]['persona_id'] = 'p2'
        self.ingest(b)
        r = report()
        r.update(study_revision=2, status='complete', interview_ids=['i1', 'i2'])
        rp = self.write('complete.json', r)
        self.cli('render', self.study, '--report', rp)
        snapshot = self.study / 'reports' / '001' / 'study.json'
        old = snapshot.read_bytes()
        extra = copy.deepcopy(b['interviews'][0])
        extra['id'] = 'i3'
        self.ingest({'interviews': [extra]})
        self.assertEqual(snapshot.read_bytes(), old)
        self.assertEqual(json.loads(old)['revision'], 2)
        self.cli('render', self.study, '--report', rp, code=1)
        self.assertFalse((self.study / 'reports' / '002').exists())

    def test_concurrent_ingests_preserve_both_writes(self):
        self.ready()
        commands = []
        for n in (2, 3):
            item = copy.deepcopy(batch()['interviews'][0])
            item['id'] = f'i{n}'
            path = self.write(f'b{n}.json', {'interviews': [item]})
            commands.append(subprocess.Popen([sys.executable, '-m', 'research_workbench', 'ingest',
                            str(self.study), '--file', str(path)], cwd=self.root,
                            env=self.env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for process in commands:
            out, err = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, out + err)
        state = json.loads((self.study / 'research.json').read_text(encoding='utf-8'))
        self.assertEqual(state['revision'], 3)
        self.assertEqual({i['id'] for i in state['interviews']}, {'i1', 'i2', 'i3'})

    def test_chinese_builtin_labels(self):
        self.initialize()
        b = batch()
        b['recipe']['language'] = 'zh-CN'
        self.ingest(b)
        self.cli('render', self.study, '--report', self.write('r.json', report()))
        html = (self.study / 'reports' / '001' / 'report.html').read_text(encoding='utf-8')
        self.assertIn('完整模拟访谈', html)
        self.assertIn('合成研究', html)
        self.assertIn('lang="zh"', html)

    def test_corrected_persona_retains_history_and_selected_active_cards(self):
        self.ready()
        b = batch()
        b['personas'][0]['id'] = 'p2'
        b['personas'][0]['label'] = 'Second active persona'
        b['interviews'][0]['id'] = 'i2'
        b['interviews'][0]['persona_id'] = 'p2'
        self.ingest(b)
        r = report()
        r.update(study_revision=2, status='complete', interview_ids=['i1', 'i2'])
        self.cli('render', self.study, '--report', self.write('before.json', r))
        old = (self.study / 'reports' / '001' / 'study.json').read_bytes()
        correction = batch()
        correction['personas'][0]['id'] = 'p3'
        correction['personas'][0]['label'] = 'Corrected active persona'
        correction['interviews'][0]['id'] = 'i3'
        correction['interviews'][0]['persona_id'] = 'p3'
        self.ingest(correction)
        r.update(study_revision=3, interview_ids=['i2', 'i3'])
        r['findings'][0]['support'][0]['interview_id'] = 'i3'
        r['findings'][0]['counterevidence'][0]['interview_id'] = 'i3'
        self.cli('render', self.study, '--report', self.write('after.json', r))
        self.assertEqual((self.study / 'reports' / '001' / 'study.json').read_bytes(), old)
        html = (self.study / 'reports' / '002' / 'report.html').read_text(encoding='utf-8')
        self.assertIn('Corrected active persona', html)
        self.assertNotIn('User (p1)', html)
        state = json.loads((self.study / 'reports' / '002' / 'study.json').read_text(encoding='utf-8'))
        self.assertEqual(len(state['personas']), 3)

    def test_ascii_terminal_can_initialize_non_ascii_title(self):
        self.env['PYTHONIOENCODING'] = 'ascii'
        result = self.cli('init', self.study, '--title', '排班研究')
        self.assertEqual(result['title'], '排班研究')
        self.assertEqual(self.cli('status', self.study)['title'], '排班研究')

    def test_partial_report_cannot_select_more_than_planned_personas(self):
        self.ready()
        for number in (2, 3):
            b = batch()
            b['personas'][0]['id'] = f'p{number}'
            b['interviews'][0]['id'] = f'i{number}'
            b['interviews'][0]['persona_id'] = f'p{number}'
            self.ingest(b)
        r = report()
        r.update(study_revision=3, interview_ids=['i1', 'i2', 'i3'])
        self.cli('check', self.study, '--report', self.write('excess.json', r), code=1)
        r['interview_ids'] = ['i1', 'i2']
        self.cli('check', self.study, '--report', self.write('partial.json', r))

    def test_usage_errors_are_json(self):
        self.cli('ingest', code=2)
        self.cli('invalid-command', code=2)


if __name__ == '__main__':
    unittest.main()
