"""Inspectable demand pool; classifications remain researcher judgments."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import io

from . import validation as v
from .audit import canonical_url
from .types import JSONObject, Study

CLAIM_FIELDS = ('actor', 'trigger', 'outcome', 'workaround', 'friction', 'frequency', 'payment')
DISPOSITIONS = ('candidate', 'resolved', 'promotion', 'adjacent', 'unclear')


def validate_need(value: JSONObject, runs: dict, sources: dict) -> None:
    v.obj(value, ('id', 'run_id', 'cluster', 'disposition', 'summary', 'claims',
                  'counterevidence', 'limitations'), 'need')
    v.identifier(value['id'], 'need.id')
    v.identifier(value['run_id'], 'need.run_id')
    v.require(value['run_id'] in runs, 'need.run_id: unknown run')
    run = runs[value['run_id']]
    v.require(run['module'] == 'social', 'need.run_id: social run required')
    for key in ('cluster', 'summary'):
        v.string(value[key], f'need.{key}')
    v.require(value['disposition'] in DISPOSITIONS, 'need.disposition: invalid disposition')
    eligible = {key: sources[key] for key in run['source_ids']}
    v.obj(value['claims'], CLAIM_FIELDS, 'need.claims')
    all_support = []
    for field, claim in value['claims'].items():
        v.obj(claim, ('text', 'basis', 'support'), f'need.claims.{field}')
        v.string(claim['text'], f'need.claims.{field}.text')
        v.require(claim['basis'] in ('stated', 'inferred', 'unknown'), 'need.claim.basis: invalid basis')
        v.references(claim['support'], 'need.claim.support', {}, eligible,
                     0 if claim['basis'] == 'unknown' else 1)
        v.require(claim['basis'] != 'unknown' or not claim['support'],
                  'need.claim: unknown must not claim source support')
        all_support.extend(claim['support'])
    v.require(bool(all_support), 'need: at least one source-backed claim required')
    v.references(value['counterevidence'], 'need.counterevidence', {}, eligible, 0)
    v.strings(value['limitations'], 'need.limitations', 1)


def family_count(items: list[JSONObject]) -> int:
    """Unify supplied families joined by the same canonical material URL."""
    parents = {s['group_id']: s['group_id'] for s in items}
    def root(group: str) -> str:
        while parents[group] != group:
            parents[group] = parents[parents[group]]
            group = parents[group]
        return group
    urls = {}
    for s in items:
        if s['url'] is not None:
            url = canonical_url(s['url'])
            if url in urls:
                parents[root(s['group_id'])] = root(urls[url])
            else:
                urls[url] = s['group_id']
    return len({root(group) for group in parents})


def pool(state: Study, report: JSONObject | None = None, *, review: bool = False) -> JSONObject:
    v.study(state)
    if report is not None:
        v.report(report, state)
    selected = None if report is None else set(report.get('need_ids', []))
    needs = [n for n in state.get('needs', []) if selected is None or n['id'] in selected]
    sources = {s['id']: s for s in state.get('sources', [])}
    clusters = defaultdict(list)
    for n in needs:
        clusters[n['cluster']].append(n)
    rows = []
    for cluster, items in sorted(clusters.items()):
        ids = {ref['source_id'] for n in items for c in n['claims'].values() for ref in c['support']}
        rows.append({'cluster': cluster, 'need_ids': [n['id'] for n in items],
                     'discussion_families': family_count([sources[i] for i in ids]),
                     'reported_families': len({sources[i]['group_id'] for i in ids}),
                     'source_ids': sorted(ids),
                     'dispositions': dict(sorted(Counter(n['disposition'] for n in items).items()))})
    result = {'ok': True, 'revision': state['revision'], 'needs': needs, 'clusters': rows,
            'coverage': {'needs': len(needs), 'clusters': len(rows),
                         'dispositions': dict(sorted(Counter(n['disposition'] for n in needs).items()))},
            'limitations': ['Need cards and clusters are researcher interpretations, not verified customers.',
                            'Several needs may come from one conversation; counts are not market demand.',
                            'Source-backed fields still require semantic review.']}
    if review:
        excerpts = {(s['id'], e['id']): e for s in sources.values() for e in s['excerpts']}

        def evidence(refs: list[JSONObject]) -> list[JSONObject]:
            return [ref | {'text': excerpts[(ref['source_id'], ref['excerpt_id'])]['text'],
                           'locator': excerpts[(ref['source_id'], ref['excerpt_id'])]['locator'],
                           'url': sources[ref['source_id']]['url']}
                    for ref in refs]

        result['claim_review'] = [
            {'id': n['id'], 'summary': n['summary'], 'disposition': n['disposition'],
             'claims': {field: {'text': c['text'], 'basis': c['basis'],
                                'evidence': evidence(c['support'])}
                        for field, c in n['claims'].items()},
             'counterevidence': evidence(n['counterevidence'])}
            for n in needs]
    return result


def csv_text(result: JSONObject) -> str:
    """Flat reusable export, safe to open in common spreadsheets."""
    def safe(value: str) -> str:
        # Spreadsheet applications may ignore initial whitespace before formulas.
        return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n')) else value
    out = io.StringIO(newline='')
    writer = csv.writer(out)
    writer.writerow(['id', 'cluster', 'disposition', 'summary'] +
                    [part for key in CLAIM_FIELDS for part in (key, key + '_basis', key + '_sources')] +
                    ['counterevidence', 'limitations'])
    for n in result['needs']:
        row = [n['id'], n['cluster'], n['disposition'], n['summary']]
        for key in CLAIM_FIELDS:
            c = n['claims'][key]
            row.extend([c['text'], c['basis'], '; '.join(r['source_id'] + ':' + r['excerpt_id'] for r in c['support'])])
        row.extend(['; '.join(r['source_id'] + ':' + r['excerpt_id'] for r in n['counterevidence']),
                    '; '.join(n['limitations'])])
        writer.writerow([safe(item) for item in row])
    return out.getvalue()
