"""Deterministic evidence coverage and duplication diagnostics, never a truth score."""

from __future__ import annotations

from collections import Counter, defaultdict
import unicodedata
from urllib.parse import unquote_plus, urlsplit, urlunsplit

from .types import JSONObject, Study
from . import validation as v


def canonical_url(url: str) -> str:
    """Drop known tracking keys while retaining paths, semantic queries and fragments."""
    v.source_url(url)
    parts = urlsplit(url)
    host = parts.hostname.lower()
    if ':' in host:  # Preserve valid IPv6 authority syntax.
        host = f'[{host}]'
    port = parts.port
    if port is not None and not ((parts.scheme == 'http' and port == 80) or
                                 (parts.scheme == 'https' and port == 443)):
        host += f':{port}'
    # Sort raw components: decoding/re-encoding values can silently conflate
    # distinct URLs (invalid percent bytes, literal pluses, or bare flags).
    components = []
    semantic_keys = []
    for component in parts.query.split('&'):
        key = unquote_plus(component.partition('=')[0])
        tracking_key = key.lower()
        if not tracking_key.startswith('utm_') and tracking_key not in ('fbclid', 'gclid'):
            components.append(component)
            semantic_keys.append(key)
    # Repeated keys may have first/last-value semantics, including encoded keys.
    if len(semantic_keys) == len(set(semantic_keys)):
        components.sort()
    return urlunsplit((parts.scheme.lower(), host, parts.path, '&'.join(components), parts.fragment))


def coverage(sources: list[JSONObject], runs: list[JSONObject], interviews: list[JSONObject]) -> JSONObject:
    """Count material/discussion families, without estimating independent people."""
    return {'sources': len(sources), 'runs': len(runs), 'interviews': len(interviews),
            'personas': len({i['persona_id'] for i in interviews}),
            'source_ids': [s['id'] for s in sources], 'run_ids': [r['id'] for r in runs],
            'interview_ids': [i['id'] for i in interviews],
            'discussion_families': len({s['group_id'] for s in sources}),
            'groups': dict(sorted(Counter(s['group_id'] for s in sources).items())),
            'access': dict(sorted(Counter(s['access'] for s in sources).items())),
            'platforms': dict(sorted(Counter(s['platform'] for s in sources).items())),
            'modules': dict(sorted(Counter(r['module'] for r in runs).items()))}


def audit(state: Study, report: JSONObject | None = None) -> JSONObject:
    """Explain stored and selected coverage, preserving all original records."""
    v.study(state)
    if report is not None:
        v.report(report, state)
    sources = state.get('sources', [])
    runs = state.get('runs', [])
    interviews = state['interviews']
    selected_runs = runs if report is None else [r for r in runs if r['id'] in report.get('run_ids', [])]
    source_ids = {s['id'] for s in sources} if report is None else {i for r in selected_runs for i in r['source_ids']}
    selected_sources = [s for s in sources if s['id'] in source_ids]
    selected_interviews = interviews if report is None else [i for i in interviews if i['id'] in report['interview_ids']]
    urls: dict[str, list[str]] = defaultdict(list)
    excerpts: dict[str, list[JSONObject]] = defaultdict(list)
    for source in selected_sources:
        if source['url'] is not None:
            urls[canonical_url(source['url'])].append(source['id'])
        for excerpt in source['excerpts']:
            normalized = ' '.join(unicodedata.normalize('NFKC', excerpt['text']).casefold().split())
            excerpts[normalized].append({'source_id': source['id'], 'excerpt_id': excerpt['id']})
    duplicate_urls = [{'canonical_url': url, 'source_ids': ids,
                       'selected_source_ids': [ident for ident in ids if ident in source_ids]}
                      for url, ids in sorted(urls.items()) if len(ids) > 1]
    duplicate_excerpts = [{'references': refs, 'selected_references': [r for r in refs if r['source_id'] in source_ids]}
                          for text, refs in sorted(excerpts.items()) if len(refs) > 1]
    incomplete = [r['id'] for r in selected_runs if r['status'] != 'complete']
    warnings: list[JSONObject] = []
    if incomplete:
        warnings.append({'code': 'incomplete_runs', 'run_ids': incomplete,
                         'message': 'Partial runs retain their stated collection limitations.'})
    if duplicate_urls:
        warnings.append({'code': 'duplicate_urls', 'message': 'URL variants may refer to the same material; records were not merged.'})
    if duplicate_excerpts:
        warnings.append({'code': 'duplicate_excerpts', 'message': 'Repeated excerpt text is not independent corroboration.'})
    inaccessible = [s['id'] for s in selected_sources if s['access'] in ('snippet', 'unavailable')]
    if inaccessible:
        warnings.append({'code': 'ineligible_sources', 'source_ids': inaccessible,
                         'message': 'Snippet and unavailable sources cannot support findings.'})
    if selected_runs and not any(s['access'] in ('full', 'excerpt') for s in selected_sources):
        warnings.append({'code': 'no_source_evidence', 'message': 'Selected research has no eligible excerpt evidence.'})
    return {'ok': True, 'revision': state['revision'], 'scope': 'report' if report is not None else 'stored',
            'stored': coverage(sources, runs, interviews),
            'selected': coverage(selected_sources, selected_runs, selected_interviews),
            'duplicate_urls': duplicate_urls, 'duplicate_excerpts': duplicate_excerpts,
            'incomplete_runs': incomplete,
            'selected_incomplete_runs': [r['id'] for r in selected_runs if r['status'] != 'complete'],
            'warnings': warnings,
            'limitations': ['Discussion/material families are not people or a representative demand estimate.',
                            'Validation and coverage cannot establish claim entailment or evidence independence.']}
