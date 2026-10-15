"""Unified exports preserve selected evidence, readable decisions, and safe links."""
import copy
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote

from test_cli import Harness, batch as simulation_batch
from test_research import research_batch, research_report, source


class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag not in ('meta',):
            assert not any(k.startswith('on') for k in attrs), attrs


class ResearchRender(Harness):
    def prepare(self, data=None):
        self.initialize()
        self.ingest(data or research_batch())

    def export(self, value=None, kind='both'):
        result = self.cli('render', self.study, '--report', self.write('draft.json', value or research_report()),
                          '--format', kind)
        return Path(result['directory'])

    def assert_citations(self, directory, kind):
        main = (directory / f'report.{kind}').read_text(encoding='utf-8')
        evidence = (directory / f'evidence.{kind}').read_text(encoding='utf-8')
        anchors = Markup(evidence).ids
        self.assertEqual(len(anchors), len(set(anchors)))
        targets = re.findall(r'evidence\.' + kind + r'#([a-z0-9-]+)', main)
        self.assertTrue(targets)
        for target in targets:
            self.assertIn(target, anchors)
        for target in Markup(evidence).links:
            if target.startswith('#'):
                self.assertIn(target[1:], anchors)
        return main, evidence

    def test_standalone_modules_and_selected_coverage(self):
        for module in ('social', 'competitor'):
            with self.subTest(module=module):
                if module == 'social':
                    b = research_batch(module)
                    b['sources'].append(source('archived', title='UNSELECTED MATERIAL'))
                    b['sources'].append(source('reply', source_type='comment'))
                    b['runs'][0]['source_ids'].append('reply')
                    self.prepare(b)
                else:
                    b = research_batch(module)
                    b.pop('brief')
                    b['runs'][0]['id'] = 'competitor-run'
                    self.ingest(b)
                r = research_report()
                if module == 'competitor':
                    r.update(study_revision=2, run_ids=['competitor-run'])
                directory = self.export(r)
                for kind in ('md', 'html'):
                    main, evidence = self.assert_citations(directory, kind)
                    self.assertIn(module, main)
                    self.assertIn('Source', main)
                    self.assertIn('All material families', main)
                    self.assertNotIn('simulat', main.lower())
                    self.assertNotIn('Synthetic research', evidence)
                    self.assertNotIn('UNSELECTED MATERIAL', evidence)
                    self.assertNotIn('Read discussions', main)
                    self.assertIn('Read discussions', evidence)
                    self.assertIn('schedule workaround', evidence)
                    self.assertIn('Post and replies read', evidence)
                    self.assertIn('Opening post', evidence)
                    self.assertIn('2026', evidence)
                    self.assertIn('We use a spreadsheet', evidence)
                    self.assertLess(main.index('Test spreadsheet handoff'), main.index('Question'))
                    self.assertNotIn('https://example.com', main)
                self.assertEqual(json.loads((directory / 'report.json').read_text(encoding='utf-8')), r)

    def test_combined_classification_and_language_precedence(self):
        b = research_batch()
        b['brief']['language'] = 'zh-CN'
        b.update(simulation_batch())
        self.prepare(b)
        r = research_report()
        r.update(status='partial', interview_ids=['i1'])
        original = copy.deepcopy(r['findings'][0])
        r['findings'] = []
        for n, kind in enumerate(('source', 'inference', 'simulation', 'mixed')):
            f = copy.deepcopy(original)
            f.update(id=f'f{n}', kind=kind)
            if kind in ('simulation', 'mixed'):
                f['statement'] = 'Synthetic interview hypotheses alongside source material.'
                f['support'] = ([{'interview_id': 'i1', 'turn': 1}] if kind == 'simulation' else
                                f['support'] + [{'interview_id': 'i1', 'turn': 1}])
            f['counterevidence'] = [{'interview_id': 'i1', 'turn': 2}]
            r['findings'].append(f)
        directory = self.export(r)
        for kind in ('md', 'html'):
            main, evidence = self.assert_citations(directory, kind)
            for label in ('来源陈述', '推断', '模拟', '混合', '研究问题'):
                self.assertIn(label, main)
            self.assertIn('所有画像和访谈均为模拟', evidence)
            self.assertIn('完整模拟访谈', evidence)
            self.assertNotIn('Why?', main)
            self.assertIn('Why?', evidence)
            self.assertIn('Existing sheet', evidence)

    def test_tables_and_adversarial_source_text_and_urls(self):
        attack = '<script>alert(1)</script> [extra](https://evil.test) | "quoted"'
        url = 'https://example.com/a(1)[two]?q="x"&tag=<svg>&single=\'x\''
        b = research_batch('competitor')
        b['sources'][0].update(title=attack, url=url, context=attack,
                              excerpts=[{'id': 'e1', 'text': attack, 'locator': attack}])
        self.prepare(b)
        r = research_report()
        refs = [{'source_id': 's1', 'excerpt_id': 'e1'}]
        r['comparisons'] = [{'alternative': attack, 'category': 'manual', 'dimension': 'Handoff',
                            'assessment': 'Current behavior', 'support': refs, 'limitations': [attack]}]
        r['opportunities'] = [{'title': attack, 'audience': 'Schedulers', 'problem': 'Lost changes',
                              'alternative': 'Sheet', 'proposal': 'Test notifications', 'priority': 'test_now',
                              'rationale': 'Observed workaround', 'support': refs, 'risks': [attack],
                              'validation': 'Observe actual handoff'}]
        directory = self.export(r)
        for kind in ('md', 'html'):
            main, evidence = self.assert_citations(directory, kind)
            self.assertNotIn('<script>', main + evidence)
            self.assertIn('Current behavior', main)
            self.assertIn('Observe actual handoff', main)
            self.assertIn('Schedulers', main)
            self.assertIn('Lost changes', main)
            if kind == 'html':
                parsed = Markup(main + evidence)
                self.assertEqual(parsed.tags.count('table'), 2)
                self.assertEqual(parsed.tags.count('blockquote'), 1)
                self.assertNotIn('script', parsed.tags)
                self.assertNotIn('svg', parsed.tags)
                self.assertEqual([link for link in parsed.links if link.startswith('http')], [url])
            else:
                self.assertGreaterEqual(main.count('| --- |'), 2)
                self.assertNotIn("[extra](https://evil.test)", main + evidence)
                self.assertIn("> &#60;script&#62;", evidence)
                destinations = re.findall(r'\]\((https[^\s)]+)\)', evidence)
                self.assertEqual(len(destinations), 1)
                self.assertEqual(unquote(html.unescape(destinations[0])), url)
                self.assertNotRegex(destinations[0], r'[\[\]<>\"\']')

    def test_corrections_preserve_frozen_snapshots_and_selected_excerpts(self):
        self.prepare()
        first = self.export()
        frozen = {p.name: p.read_bytes() for p in first.iterdir()}
        b = research_batch()
        b.pop('brief')
        b['sources'][0].update(id='s2', excerpts=[{'id': 'fixed', 'text': 'Corrected archived reading', 'locator': 'Update'}])
        b['runs'][0].update(id='run2', source_ids=['s2'])
        self.ingest(b)
        r = research_report()
        r.update(study_revision=2, run_ids=['run2'])
        r['findings'][0]['support'] = [{'source_id': 's2', 'excerpt_id': 'fixed'}]
        for kind in ('md', 'html'):
            second = self.export(r, kind)
            self.assertEqual({p.name for p in second.iterdir()},
                             {f'report.{kind}', f'evidence.{kind}', 'report.json', 'study.json'})
            _, evidence = self.assert_citations(second, kind)
            self.assertIn('Corrected archived reading', evidence)
            self.assertNotIn('We use a spreadsheet', evidence)
            self.assertEqual(len(json.loads((second / 'study.json').read_text(encoding='utf-8'))['sources']), 2)
        self.assertEqual(frozen, {p.name: p.read_bytes() for p in first.iterdir()})

    def test_source_only_with_unused_simulation_and_blocked_collection(self):
        b = research_batch()
        b.update(simulation_batch())
        self.prepare(b)
        first = self.export()
        for kind in ('md', 'html'):
            self.assertNotIn('simulat', (first / f'report.{kind}').read_text(encoding='utf-8').lower())
            self.assertNotIn('Role cards', (first / f'evidence.{kind}').read_text(encoding='utf-8'))
        run = research_batch()['runs'][0]
        run.update(id='blocked', status='partial', source_ids=[], limitations=['Access blocked by login'])
        self.ingest({'runs': [run]})
        r = research_report()
        r.update(study_revision=2, status='partial', run_ids=['blocked'], findings=[],
                 limitations=['Access blocked by login'])
        second = self.export(r)
        for kind in ('md', 'html'):
            main = (second / f'report.{kind}').read_text(encoding='utf-8')
            evidence = (second / f'evidence.{kind}').read_text(encoding='utf-8')
            self.assertIn('No eligible evidence', main)
            self.assertIn('Access blocked by login', main)
            self.assertIn('Access blocked by login', evidence)
            self.assertIn('Observe a real handoff', main)

    def test_exact_excerpt_targets_follow_selection_order_and_deduplicate_sources(self):
        b = research_batch()
        b['sources'][0]['excerpts'].append({'id': 'reply', 'text': 'Exact second excerpt', 'locator': 'Comment 2'})
        b['sources'].append(source('s2', title='Other discussion', group_id='thread-2',
                                   excerpts=[{'id': 'other', 'text': 'Other exact excerpt', 'locator': 'Comment 1'}]))
        b['runs'][0]['source_ids'] = ['s2', 's1']
        b['runs'].append({**b['runs'][0], 'id': 'run2', 'module': 'competitor', 'source_ids': ['s1']})
        self.prepare(b)
        r = research_report()
        r['run_ids'] = ['run1', 'run2']
        r['findings'][0].update(support=[{'source_id': 's1', 'excerpt_id': 'reply'}],
                                counterevidence=[{'source_id': 's2', 'excerpt_id': 'other'}])
        directory = self.export(r)
        for kind in ('md', 'html'):
            main, evidence = self.assert_citations(directory, kind)
            self.assertIn(f'evidence.{kind}#source-2-excerpt-2', main)
            self.assertIn(f'evidence.{kind}#source-1-excerpt-1', main)
            self.assertIn('Source 2 · Excerpt 2', main)
            self.assertIn('Sources: 2', html.unescape(main))
            self.assertIn('All material families (including unread): 2', html.unescape(main))
            anchor_start = evidence.index('id="source-2-excerpt-2"')
            self.assertIn('Exact second excerpt', evidence[anchor_start:])
            self.assertEqual(evidence.count('Exact second excerpt'), 1)

    def test_ipv6_original_url_remains_usable_in_markdown(self):
        url = 'https://[::1]:8443/a[1](2)?x=3'
        b = research_batch()
        b['sources'][0]['url'] = url
        self.prepare(b)
        directory = self.export(kind='md')
        evidence = (directory / 'evidence.md').read_text(encoding='utf-8')
        destination = re.search(r'\]\((https[^\s)]+)\)', evidence).group(1)
        from urllib.parse import urlsplit
        self.assertEqual(urlsplit(html.unescape(destination)).hostname, '::1')
        self.assertEqual(unquote(html.unescape(destination)), url)

    def test_render_identifies_accessible_social_sample_separately(self):
        b = research_batch()
        b['sources'] += [source('reply', source_type='comment'),
                         source('docs', source_type='official', group_id='docs'),
                         source('blocked', access='unavailable', excerpts=[], group_id='blocked',
                                limitations=['Login required'])]
        b['runs'][0].update(source_ids=['s1', 'reply', 'docs', 'blocked'], status='partial')
        self.prepare(b)
        r = research_report()
        r['status'] = 'partial'
        directory = self.export(r)
        for kind in ('md', 'html'):
            main = html.unescape((directory / f'report.{kind}').read_text(encoding='utf-8'))
            self.assertIn('Readable social families: 1', main)
            self.assertIn('Readable material families: 2', main)
            self.assertIn('All material families (including unread): 3', main)

    def test_finding_statement_is_body_text_not_an_unbounded_heading(self):
        self.prepare()
        r = research_report()
        statement = 'A detailed finding. ' * 30
        r['findings'][0]['statement'] = statement
        directory = self.export(r)
        markup = (directory / 'report.html').read_text(encoding='utf-8')
        self.assertIn('<p>' + statement + '</p>', markup)
        self.assertIn('id="finding-1"', markup)
        self.assertNotIn(statement, ''.join(re.findall(r'<h3[^>]*>(.*?)</h3>', markup)))
        markdown = html.unescape((directory / 'report.md').read_text(encoding='utf-8'))
        self.assertIn(statement, markdown)
        self.assertFalse(any(statement in line for line in markdown.splitlines() if line.startswith('#')))

    def test_coverage_separates_read_sources_from_blocked_leads_and_notice_is_once(self):
        b = research_batch()
        b['sources'].append(source('blocked', access='unavailable', excerpts=[],
                                   group_id='blocked-family', limitations=['Login required']))
        b['runs'][0].update(source_ids=['s1', 'blocked'], status='partial')
        self.prepare(b)
        r = research_report()
        r['status'] = 'partial'
        r['findings'].append({**copy.deepcopy(r['findings'][0]), 'id': 'f2'})
        directory = self.export(r)
        for kind in ('md', 'html'):
            main = html.unescape((directory / f'report.{kind}').read_text(encoding='utf-8'))
            self.assertIn('Sources: 2', main)
            self.assertIn('Read sources (full / excerpt): 1', main)
            self.assertIn('Snippet / unavailable: 1', main)
            self.assertIn('All material families (including unread): 2', main)
            self.assertEqual(main.count('Source statements reflect saved material, not independently verified facts.'), 1)
            self.assertEqual(main.count('Evidence type: Source statement'), 2)
            self.assertEqual(main.count('One discussion'), 2)
