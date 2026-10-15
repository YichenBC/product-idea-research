"""Behavior contracts for the additive research ledger and evidence audit."""
import copy
import json
import subprocess
import sys

from test_cli import Harness, batch as simulation_batch, report as simulation_report


def source(ident='s1', **changes):
    result = {'id': ident, 'title': 'Scheduling discussion', 'url': 'https://example.com/thread?id=1',
              'platform': 'forum', 'source_type': 'post', 'published_at': '2026-10-01',
              'accessed_at': '2026-10-15', 'language': 'en', 'access': 'full', 'group_id': 'thread-1',
              'context': 'Post and replies read', 'excerpts': [{'id': 'e1', 'text': 'We use a spreadsheet.',
              'locator': 'Opening post'}], 'limitations': []}
    result.update(changes)
    return result


def research_batch(module='social'):
    return {'brief': {'id': 'b1', 'question': 'Where does scheduling fail?', 'language': 'en', 'constraints': []},
            'sources': [source()], 'runs': [{'id': 'run1', 'module': module, 'status': 'complete',
            'objective': 'Understand workarounds', 'method': 'Read discussions', 'queries': ['schedule workaround'],
            'source_ids': ['s1'], 'limitations': ['Convenience sample']}]}


def research_report():
    return {'title': 'Research', 'study_revision': 1, 'status': 'complete', 'summary': 'Test spreadsheet handoff',
            'interview_ids': [], 'run_ids': ['run1'], 'findings': [{'id': 'f1', 'kind': 'source',
            'statement': 'One source describes a spreadsheet.', 'support': [{'source_id': 's1', 'excerpt_id': 'e1'}],
            'counterevidence': [], 'limitations': ['One discussion']}], 'next_steps': ['Observe a real handoff'],
            'limitations': ['Not representative']}


class Research(Harness):
    def research_ready(self, data=None):
        self.initialize()
        return self.ingest(data or research_batch())

    def check_report(self, value, code=0):
        return self.cli('check', self.study, '--report', self.write('research-report.json', value), code=code)

    def test_social_and_competitor_without_simulation(self):
        self.initialize()
        state = json.loads((self.study / 'research.json').read_text(encoding='utf-8'))
        self.assertEqual((state['brief'], state['sources'], state['runs']), (None, [], []))
        status = self.ingest(research_batch())
        self.assertEqual((status['sources'], status['runs'], status['modules']), (1, 1, {'social': 1}))
        self.check_report(research_report())
        b = research_batch('competitor')
        b['runs'][0]['id'] = 'run2'
        status = self.ingest(b)
        self.assertEqual(status['modules'], {'social': 1, 'competitor': 1})
        r = research_report()
        r.update(study_revision=2, run_ids=['run2'])
        self.check_report(r)

    def test_blocked_partial_and_checkpointed_sources(self):
        self.initialize()
        b = research_batch()
        run = b['runs'][0]
        run.update(status='partial', source_ids=[], limitations=['No accessible results'])
        b['sources'] = []
        self.ingest(b)
        r = research_report()
        r.update(status='partial', findings=[])
        self.check_report(r)
        r['status'] = 'complete'
        self.check_report(r, 1)
        self.ingest({'sources': [source()]})
        r.update(study_revision=2, status='partial', findings=research_report()['findings'])
        self.check_report(r, 1)

    def test_bad_sources_are_atomic_structured_errors(self):
        self.initialize()
        bad = [(lambda s, url=url: s.update(url=url)) for url in
               ['javascript:alert(1)', 'file:///tmp/a', 'https://u:p@example.com', 'https:///missing',
                'https://example.com/a b', 'https://example.com/\\x', 'https://example.com/\n',
                'https://example.com:bad/x', 'https://[broken', None]]
        bad += [lambda s: s.update(published_at='2026-02-30'), lambda s: s.update(accessed_at='20261015'),
                lambda s: s.update(access=[]), lambda s: s.update(source_type={}),
                lambda s: s.update(excerpts=[]), lambda s: s.update(group_id=[]),
                lambda s: s['excerpts'].append(copy.deepcopy(s['excerpts'][0])),
                lambda s: s.update(access='unavailable'), lambda s: s.update(url=[]),
                lambda s: s.update(excerpts=[None])]
        before = (self.study / 'research.json').read_bytes()
        for mutate in bad:
            b = research_batch()
            mutate(b['sources'][0])
            self.cli('ingest', self.study, '--file', self.write('bad.json', b), code=1)
            self.assertEqual((self.study / 'research.json').read_bytes(), before)

    def test_provided_snippet_and_unavailable_material(self):
        self.initialize()
        b = research_batch()
        b['sources'][0].update(url=None, source_type='provided', published_at=None)
        self.ingest(b)
        self.check_report(research_report())
        for access in ('snippet', 'unavailable'):
            s = source(access, access=access, excerpts=[], limitations=['Only search preview available'])
            self.ingest({'sources': [s]})
            run = copy.deepcopy(b['runs'][0])
            run.update(id=access + '-run', source_ids=[access])
            self.cli('ingest', self.study, '--file', self.write('bad.json', {'runs': [run]}), code=1)
            run.update(status='partial')
            self.ingest({'runs': [run]})
            r = research_report()
            r.update(study_revision=self.cli('status', self.study)['revision'], status='partial', run_ids=[run['id']])
            r['findings'][0]['support'] = [{'source_id': access, 'excerpt_id': 'e1'}]
            self.check_report(r, 1)

    def test_run_validation_and_global_immutable_ids(self):
        self.research_ready()
        before = (self.study / 'research.json').read_bytes()
        bad = [dict(brief={**research_batch()['brief'], 'question': 'Changed'}),
               {'sources': [source(title='Changed')]},
               {'sources': [source('b1')]}, {'sources': [source('run1')]}]
        for change in [{'id': 'run2', 'source_ids': ['missing']}, {'id': 'run2', 'source_ids': ['s1', 's1']},
                       {'id': 'run2', 'source_ids': [[]]}, {'id': 'run2', 'module': {}},
                       {'id': 'run2', 'status': 'partial', 'limitations': []}]:
            run = research_batch()['runs'][0]
            run.update(change)
            bad.append({'runs': [run]})
        for value in bad:
            self.cli('ingest', self.study, '--file', self.write('bad.json', value), code=1)
            self.assertEqual((self.study / 'research.json').read_bytes(), before)
        self.ingest(research_batch())
        self.assertEqual((self.study / 'research.json').read_bytes(), before)

    def test_report_reference_and_kind_rules(self):
        self.research_ready()
        for kind in ('source', 'inference'):
            r = research_report()
            r['findings'][0]['kind'] = kind
            self.check_report(r)
        mutations = [lambda r: r.update(run_ids=[]), lambda r: r.update(run_ids=['missing']),
                     lambda r: r.update(run_ids=[{}]), lambda r: r.update(findings=[]),
                     lambda r: r['findings'][0].update(kind='simulation'),
                     lambda r: r['findings'][0].update(kind='mixed'),
                     lambda r: r['findings'][0].update(kind=[]),
                     lambda r: r['findings'][0]['support'][0].update(excerpt_id='missing'),
                     lambda r: r['findings'][0]['support'][0].update(source_id=[]),
                     lambda r: r['findings'][0]['support'][0].update(interview_id='i1', turn=1)]
        for mutate in mutations:
            r = research_report()
            mutate(r)
            self.check_report(r, 1)
        self.ingest(simulation_batch())
        r = research_report()
        r.update(study_revision=2)
        self.check_report(r)  # Unused recipe does not force simulation coverage.
        r.update(interview_ids=['i1'], status='partial')
        r['findings'][0].update(kind='mixed', statement='The source describes a sheet; the synthetic interview suggests handoff risk.')
        r['findings'][0]['support'].append({'interview_id': 'i1', 'turn': 1})
        self.check_report(r)
        for kind in ('simulation', 'source', 'inference'):
            r['findings'][0]['kind'] = kind
            self.check_report(r, 1)
        r['findings'][0].update(kind='source', support=[{'source_id': 's1', 'excerpt_id': 'e1'}],
                               counterevidence=[{'interview_id': 'i1', 'turn': 2}])
        self.check_report(r)
        r['status'] = 'complete'
        self.check_report(r, 1)

    def test_comparisons_and_opportunities_require_eligible_support(self):
        self.research_ready()
        r = research_report()
        refs = [{'source_id': 's1', 'excerpt_id': 'e1'}]
        r['comparisons'] = [{'alternative': 'Spreadsheet', 'category': 'manual', 'dimension': 'Handoff',
                            'assessment': 'Used today', 'support': refs, 'limitations': ['One source']}]
        r['opportunities'] = [{'title': 'Handoff', 'audience': 'Schedulers', 'problem': 'Manual handoff',
                              'alternative': 'Sheet', 'proposal': 'Test notifications', 'priority': 'test_now',
                              'rationale': 'Observed workaround', 'support': refs, 'risks': ['May be sufficient'],
                              'validation': 'Observe actual handoff'}]
        self.check_report(r)
        for section, field, value in [('comparisons', 'support', []), ('comparisons', 'category', []),
                                      ('opportunities', 'risks', []), ('opportunities', 'priority', {})]:
            changed = copy.deepcopy(r)
            changed[section][0][field] = value
            self.check_report(changed, 1)
        self.ingest(simulation_batch())
        r.update(study_revision=2, status='partial', interview_ids=['i1'])
        r['opportunities'][0]['support'] = [{'interview_id': 'i1', 'turn': 1}]
        self.check_report(r, 1)
        r['opportunities'][0]['priority'] = 'watch'
        self.check_report(r)
        r['comparisons'][0]['support'] = [{'interview_id': 'i1', 'turn': 1}]
        self.check_report(r, 1)

    def test_audit_distinguishes_stored_selected_and_discussion_families(self):
        b = research_batch()
        b['sources'] += [source('s2', url='HTTPS://EXAMPLE.COM:443/thread?utm_source=x&id=1',
                                excerpts=[{'id': 'e2', 'text': '  We  use a spreadsheet. ', 'locator': 'Reply'}]),
                         source('s3', url='https://example.com/thread?id=2#reply')]
        b['runs'][0]['source_ids'] = ['s1', 's2']
        self.research_ready(b)
        a = self.cli('audit', self.study, '--report', self.write('r.json', research_report()))
        self.assertEqual(a['stored']['sources'], 3)
        self.assertEqual(a['selected']['sources'], 2)
        self.assertEqual(a['selected']['discussion_families'], 1)
        self.assertEqual(a['selected']['access'], {'full': 2})
        self.assertEqual(a['selected']['platforms'], {'forum': 2})
        self.assertEqual(len(a['duplicate_urls']), 1)
        self.assertEqual(a['duplicate_urls'][0]['source_ids'], ['s1', 's2'])
        self.assertEqual(len(a['duplicate_excerpts']), 1)
        self.assertNotIn('customers', json.dumps(a))
        self.assertEqual(self.cli('audit', self.study)['stored']['sources'], 3)

    def test_legacy_load_does_not_rewrite(self):
        self.ready()
        path = self.study / 'research.json'
        state = json.loads(path.read_text(encoding='utf-8'))
        for key in ('brief', 'sources', 'runs'):
            state.pop(key, None)
        path.write_text(json.dumps(state), encoding='utf-8')
        old = path.read_bytes()
        self.cli('check', self.study, '--report', self.write('legacy.json', simulation_report()))
        self.cli('audit', self.study)
        self.assertEqual(path.read_bytes(), old)

    def test_concurrent_sources_and_runs_preserve_updates(self):
        self.research_ready()
        processes = []
        for n in (2, 3):
            b = research_batch()
            b['sources'][0]['id'] = f's{n}'
            b['runs'][0].update(id=f'run{n}', source_ids=[f's{n}'])
            file = self.write(f'parallel{n}.json', b)
            processes.append(subprocess.Popen([sys.executable, '-m', 'research_workbench', 'ingest',
                             str(self.study), '--file', str(file)], cwd=self.root, env=self.env,
                             text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for process in processes:
            out, err = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, out + err)
        self.assertEqual(self.cli('status', self.study)['sources'], 3)

    def test_report_audit_does_not_warn_about_unselected_records(self):
        b = research_batch()
        b['sources'].append(source('archived'))
        old_run = copy.deepcopy(b['runs'][0])
        old_run.update(id='old-run', status='partial', source_ids=['archived'])
        b['runs'].append(old_run)
        self.research_ready(b)
        a = self.cli('audit', self.study, '--report', self.write('r.json', research_report()))
        self.assertEqual(a['stored']['sources'], 2)
        self.assertEqual(a['selected']['sources'], 1)
        self.assertEqual(a['duplicate_urls'], [])
        self.assertEqual(a['duplicate_excerpts'], [])
        self.assertEqual(a['incomplete_runs'], [])
        self.assertEqual(a['warnings'], [])
        a = self.cli('audit', self.study)
        self.assertEqual(a['incomplete_runs'], ['old-run'])
        self.assertEqual(len(a['duplicate_urls']), 1)

    def test_canonical_urls_preserve_query_values_paths_and_fragments(self):
        from research_workbench.audit import canonical_url
        self.assertEqual(canonical_url('HTTPS://EXAMPLE.COM:443/path?b=2&utm_source=x&a=1#reply'),
                         'https://example.com/path?a=1&b=2#reply')
        self.assertEqual(canonical_url('http://[::1]:80/a?gclid=x&id=1'), 'http://[::1]/a?id=1')
        for a, b in [('?id=1', '?id=2'), ('?id=1#one', '?id=1#two'),
                     ('?id=%FF', '?id=%EF%BF%BD'), ('?flag', '?flag='),
                     ('?id=a%20b', '?id=a+b'), ('/one', '/two')]:
            self.assertNotEqual(canonical_url('https://example.com' + a),
                                canonical_url('https://example.com' + b))

    def test_runs_require_brief_but_sources_can_be_checkpointed_first(self):
        self.initialize()
        self.ingest({'sources': [source()]})
        self.cli('ingest', self.study, '--file', self.write('bad.json', {'runs': research_batch()['runs']}), code=1)
        self.ingest({'brief': research_batch()['brief'], 'runs': research_batch()['runs']})
        self.check_report({**research_report(), 'study_revision': 2})

    def test_nested_weird_json_values_never_escape_validation(self):
        from research_workbench import validation as v
        state = {'schema_version': 1, 'title': 'Stress test', 'revision': 1,
                 'recipe': None, 'personas': [], 'interviews': [], **research_batch()}
        r = research_report()

        def paths(value, prefix=()):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield prefix + (key,)
                    yield from paths(item, prefix + (key,))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    yield prefix + (index,)
                    yield from paths(item, prefix + (index,))

        for original, validate in ((state, v.study), (r, lambda value: v.report(value, state))):
            for path in paths(original):
                for replacement in (None, True, 1, 1.5, [], {}, ['x'], {'x': 'y'}):
                    changed = copy.deepcopy(original)
                    target = changed
                    for key in path[:-1]:
                        target = target[key]
                    target[path[-1]] = replacement
                    try:
                        validate(changed)
                    except v.WorkbenchError:
                        pass

    def test_audit_rejects_invalid_explicit_report_even_null(self):
        self.research_ready()
        for value in (None, [], {}, True, 5, 'report'):
            self.cli('audit', self.study, '--report', self.write('invalid-report.json', value), code=1)

    def test_empty_partial_findings_require_blocked_or_unusable_collection(self):
        self.research_ready()
        r = research_report()
        r.update(status='partial', findings=[])
        self.check_report(r, 1)
        self.ingest(simulation_batch())
        r.update(study_revision=2, run_ids=[], interview_ids=['i1'])
        self.check_report(r, 1)
        b = research_batch()
        b.pop('brief')
        b['sources'][0].update(id='snippet', access='snippet')
        b['runs'][0].update(id='blocked', status='partial', source_ids=['snippet'])
        self.ingest(b)
        r.update(study_revision=3, run_ids=['blocked'], interview_ids=[])
        self.check_report(r)
        r['interview_ids'] = ['i1']
        self.check_report(r, 1)

    def test_canonical_urls_preserve_repeated_semantic_key_order(self):
        from research_workbench.audit import canonical_url
        base = 'https://example.com/path?'
        for query, reverse in [('a=1&a=2', 'a=2&a=1'), ('a=1&%61=2', '%61=2&a=1')]:
            self.assertNotEqual(canonical_url(base + query), canonical_url(base + reverse))
        self.assertEqual(canonical_url(base + 'z=3&a=1&a=2&utm_source=x'), base + 'z=3&a=1&a=2')
        self.assertEqual(canonical_url(base + 'z=3&utm_source=x&utm_source=y&a=1'), base + 'a=1&z=3')
