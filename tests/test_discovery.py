"""Behavior tests for evidence-backed demand cards and comment provenance."""
import copy
import json
from test_cli import Harness
from test_research import research_batch, research_report, source


def need(ident='n1'):
    claim = {'text': 'Uses a spreadsheet', 'basis': 'stated',
             'support': [{'source_id': 's1', 'excerpt_id': 'e1'}]}
    return {'id': ident, 'run_id': 'run1', 'cluster': 'handoff', 'disposition': 'candidate',
            'summary': 'Track a handoff',
            'claims': {key: copy.deepcopy(claim) for key in
                       ('actor', 'trigger', 'outcome', 'workaround', 'friction')} |
                      {key: {'text': 'Not reported', 'basis': 'unknown', 'support': []}
                       for key in ('frequency', 'payment')},
            'counterevidence': [], 'limitations': ['One unverified self-report']}


class Discovery(Harness):
    def ready(self):
        self.initialize()
        self.ingest(research_batch())

    def test_need_ingestion_is_immutable_and_pool_retains_dispositions(self):
        self.ready()
        self.ingest({'needs': [need(), need('n2') | {'disposition': 'resolved'}]})
        before = (self.study / 'research.json').read_bytes()
        self.ingest({'needs': [need()]})
        self.assertEqual(before, (self.study / 'research.json').read_bytes())
        result = self.cli('pool', self.study)
        self.assertEqual(len(result['needs']), 2)
        self.assertEqual(result['coverage']['dispositions'], {'candidate': 1, 'resolved': 1})
        self.assertEqual(result['clusters'][0]['discussion_families'], 1)
        self.cli('ingest', self.study, '--file', self.write('bad.json', {'needs': [need() | {'summary': 'rewrite'}]}), code=1)
        self.assertEqual(before, (self.study / 'research.json').read_bytes())

    def test_claims_reject_unbacked_stated_facts_and_unselected_sources(self):
        self.ready()
        before = (self.study / 'research.json').read_bytes()
        for mutate in (
            lambda n: n['claims']['payment'].update(basis='stated'),
            lambda n: n['claims']['actor'].update(support=[{'interview_id': 'fake', 'turn': 1}]),
            lambda n: n['claims']['actor'].update(support=[{'source_id': 'missing', 'excerpt_id': 'e1'}]),
            lambda n: n['claims']['actor'].update(basis='unknown'),
            lambda n: n.update(run_id='missing'),
            lambda n: n.update(disposition='validated'),
        ):
            n = need(); mutate(n)
            self.cli('ingest', self.study, '--file', self.write('bad.json', {'needs': [n]}), code=1)
            self.assertEqual(before, (self.study / 'research.json').read_bytes())
        self.ingest({'sources': [source('s2', access='snippet')]})
        b = research_batch()['runs'][0] | {'id': 'run2', 'source_ids': ['s1', 's2']}
        self.ingest({'runs': [b]})
        n = need() | {'run_id': 'run2'}
        n['claims']['actor']['support'][0]['source_id'] = 's2'
        self.cli('ingest', self.study, '--file', self.write('bad.json', {'needs': [n]}), code=1)

    def test_parent_reference_must_exist_share_family_and_be_acyclic(self):
        self.ready()
        self.ingest({'sources': [source('reply', source_type='comment', parent_source_id='s1')]})
        before = (self.study / 'research.json').read_bytes()
        for item in [source('bad', parent_source_id='missing'),
                     source('bad', parent_source_id='s1', group_id='other'),
                     source('bad', parent_source_id='bad')]:
            self.cli('ingest', self.study, '--file', self.write('bad.json', {'sources': [item]}), code=1)
            self.assertEqual(before, (self.study / 'research.json').read_bytes())
        self.cli('ingest', self.study, '--file', self.write('bad.json', {'sources': [
            source('a', parent_source_id='b'), source('b', parent_source_id='a')]}), code=1)

    def test_report_selection_and_csv_escape(self):
        self.ready()
        self.ingest({'needs': [need() | {'summary': '=HYPERLINK("bad")<script>evil</script>'}, need('n2')]})
        r = research_report() | {'study_revision': 2, 'need_ids': ['n1']}
        report_file = self.write('report.json', r)
        result = self.cli('render', self.study, '--report', report_file)
        from pathlib import Path
        out = Path(result['directory'])
        cards = json.loads((out / 'needs.json').read_text())
        self.assertEqual([n['id'] for n in cards['needs']], ['n1'])
        self.assertIn("'=HYPERLINK", (out / 'needs.csv').read_text())
        self.assertNotIn('<script>evil</script>', (out / 'needs.html').read_text())
        self.assertIn('needs.html', (out / 'report.html').read_text())
        self.assertEqual(len(self.cli('pool', self.study, '--report', report_file)['needs']), 1)
        r['need_ids'] = ['missing']
        self.cli('check', self.study, '--report', self.write('badreport.json', r), code=1)
        b = research_batch()['runs'][0] | {'id': 'run2'}
        self.ingest({'runs': [b]})
        r.update(study_revision=3, need_ids=['n1'], run_ids=['run2'])
        self.cli('check', self.study, '--report', self.write('badreport.json', r), code=1)

    def test_x_aliases_identify_one_status_not_all_authors_posts(self):
        from product_idea_research.audit import canonical_url
        self.assertEqual(canonical_url('https://twitter.com/old/status/123?s=20'),
                         canonical_url('https://x.com/new/status/123'))
        self.assertNotEqual(canonical_url('https://x.com/new/status/123'),
                            canonical_url('https://x.com/new/status/124'))

    def test_pool_merges_aliases_across_supplied_groups(self):
        self.initialize()
        b = research_batch()
        b['sources'][0].update(url='https://twitter.com/old/status/123', group_id='old-handle')
        b['sources'].append(source('s2', url='https://x.com/new/status/123', group_id='new-handle'))
        b['runs'][0]['source_ids'].append('s2')
        self.ingest(b)
        n2 = need('n2')
        for c in n2['claims'].values():
            for ref in c['support']:
                ref['source_id'] = 's2'
        self.ingest({'needs': [need(), n2]})
        cluster = self.cli('pool', self.study)['clusters'][0]
        self.assertEqual(cluster['reported_families'], 2)
        self.assertEqual(cluster['discussion_families'], 1)

    def test_review_joins_exact_excerpts_and_respects_report_selection(self):
        self.initialize()
        b = research_batch()
        b['sources'][0]['excerpts'].append({
            'id': 'e2', 'text': 'I might pay, but have not bought it.',
            'locator': 'Author follow-up'})
        self.ingest(b)
        card = need()
        card['claims']['payment'] = {
            'text': 'Conditional interest, no completed payment', 'basis': 'stated',
            'support': [{'source_id': 's1', 'excerpt_id': 'e2'}]}
        card['counterevidence'] = [{'source_id': 's1', 'excerpt_id': 'e1'}]
        self.ingest({'needs': [card, need('unselected')]})
        before = (self.study / 'research.json').read_bytes()
        draft = self.write('report.json', research_report() | {
            'study_revision': 2, 'need_ids': ['n1']})
        result = self.cli('pool', self.study, '--report', draft, '--review')
        self.assertEqual([n['id'] for n in result['claim_review']], ['n1'])
        review = result['claim_review'][0]
        self.assertEqual(review['claims']['payment']['evidence'][0]['text'],
                         'I might pay, but have not bought it.')
        self.assertEqual(review['claims']['payment']['evidence'][0]['locator'],
                         'Author follow-up')
        self.assertEqual(review['claims']['payment']['evidence'][0]['source_id'], 's1')
        self.assertEqual(review['claims']['frequency']['evidence'], [])
        self.assertEqual(review['counterevidence'][0]['text'],
                         b['sources'][0]['excerpts'][0]['text'])
        self.assertEqual(before, (self.study / 'research.json').read_bytes())
        self.assertNotIn('claim_review', self.cli('pool', self.study))
