"""Strict validation for JSON records; no input prose is executed."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date
import re
from typing import Any
from urllib.parse import urlsplit

from .types import JSONObject, Study


class WorkbenchError(Exception):
    """An actionable input or filesystem error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WorkbenchError(message)


def obj(value: Any, keys: Iterable[str], path: str, optional: Iterable[str] = ()) -> None:
    require(isinstance(value, dict), f'{path}: expected an object')
    missing = set(keys) - value.keys()
    extra = value.keys() - set(keys) - set(optional)
    require(not missing, f'{path}: missing fields {sorted(missing)}')
    require(not extra, f'{path}: unknown fields {sorted(extra)}')


def string(value: Any, path: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f'{path}: expected nonempty text')
    require(not any(0xD800 <= ord(char) <= 0xDFFF for char in value), f'{path}: invalid Unicode surrogate')


def identifier(value: Any, path: str) -> None:
    require(isinstance(value, str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', value) is not None,
            f'{path}: invalid ID')


def integer(value: Any, path: str, low: int = 0, high: int | None = None) -> None:
    require(type(value) is int and value >= low and (high is None or value <= high),
            f'{path}: expected integer >= {low}' + (f' and <= {high}' if high is not None else ''))


def array(value: Any, path: str, minimum: int = 0) -> None:
    require(isinstance(value, list) and len(value) >= minimum, f'{path}: expected list with >= {minimum} items')


def strings(value: Any, path: str, minimum: int = 0, unique: bool = False) -> None:
    array(value, path, minimum)
    for i, item in enumerate(value):
        string(item, f'{path}[{i}]')
    if unique:
        require(len(set(value)) == len(value), f'{path}: duplicate values')


def recipe(value: Any) -> None:
    obj(value, ('id', 'question', 'method', 'dimensions', 'constraints', 'persona_count', 'language'), 'recipe')
    identifier(value['id'], 'recipe.id')
    for key in ('question', 'method', 'language'):
        string(value[key], f'recipe.{key}')
    strings(value['constraints'], 'recipe.constraints')
    integer(value['persona_count'], 'recipe.persona_count', 1, 30)
    array(value['dimensions'], 'recipe.dimensions', 1)
    names = []
    for dim in value['dimensions']:
        obj(dim, ('name', 'values'), 'dimension')
        string(dim['name'], 'dimension.name')
        strings(dim['values'], 'dimension.values', 1, unique=True)
        names.append(dim['name'])
    require(len(set(names)) == len(names), 'recipe.dimensions: duplicate names')


def persona(value: Any, rec: JSONObject) -> None:
    obj(value, ('id', 'label', 'recipe_id', 'traits', 'attributes'), 'persona')
    identifier(value['id'], 'persona.id')
    string(value['label'], 'persona.label')
    require(value['recipe_id'] == rec['id'], 'persona.recipe_id: unknown recipe')
    dimensions = {d['name']: d['values'] for d in rec['dimensions']}
    obj(value['traits'], dimensions, 'persona.traits')
    for key, val in value['traits'].items():
        string(val, f'persona.traits.{key}')
        require(val in dimensions[key], f'persona.traits.{key}: undeclared option')
    array(value['attributes'], 'persona.attributes', 1)
    names = []
    for attr in value['attributes']:
        obj(attr, ('name', 'value', 'basis', 'rationale'), 'attribute')
        for key in ('name', 'value', 'rationale'):
            string(attr[key], f'attribute.{key}')
        require(attr['basis'] in ('assumed', 'unknown'), 'attribute.basis: expected assumed or unknown')
        names.append(attr['name'])
    require(len(set(names)) == len(names), 'persona.attributes: duplicate names')


def interview(value: Any, personas: Mapping[str, JSONObject]) -> None:
    obj(value, ('id', 'persona_id', 'synthetic', 'turns'), 'interview')
    identifier(value['id'], 'interview.id')
    identifier(value['persona_id'], 'interview.persona_id')
    require(value['persona_id'] in personas, 'interview.persona_id: unknown persona')
    require(value['synthetic'] is True, 'interview.synthetic: must be true')
    array(value['turns'], 'interview.turns', 2)
    for turn in value['turns']:
        obj(turn, ('question', 'answer', 'assumptions'), 'turn')
        string(turn['question'], 'turn.question')
        string(turn['answer'], 'turn.answer')
        strings(turn['assumptions'], 'turn.assumptions')


def brief(value: Any) -> None:
    obj(value, ('id', 'question', 'language', 'constraints'), 'brief')
    identifier(value['id'], 'brief.id')
    for key in ('question', 'language'):
        string(value[key], f'brief.{key}')
    strings(value['constraints'], 'brief.constraints')


def source_url(value: Any, path: str = 'source.url') -> None:
    """Validate a link without fetching or rewriting it."""
    string(value, path)
    require(not any(c.isspace() or ord(c) < 32 or 127 <= ord(c) <= 159 or c == chr(92)
                    for c in value), f'{path}: whitespace, controls and backslashes are forbidden')
    try:
        parts = urlsplit(value)
        require(parts.scheme in ('http', 'https') and bool(parts.hostname),
                f'{path}: expected http/https URL with a host')
        require(parts.username is None and parts.password is None, f'{path}: userinfo is forbidden')
        # Accessing port also validates malformed/non-numeric/out-of-range ports.
        _ = parts.port
    except ValueError as exc:
        raise WorkbenchError(f'{path}: invalid URL: {exc}') from exc


def iso_date(value: Any, path: str) -> None:
    string(value, path)
    require(re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value) is not None,
            f'{path}: expected YYYY-MM-DD')
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise WorkbenchError(f'{path}: invalid calendar date') from exc


def source(value: Any) -> None:
    obj(value, ('id', 'title', 'url', 'platform', 'source_type', 'published_at', 'accessed_at',
                'language', 'access', 'group_id', 'context', 'excerpts', 'limitations'), 'source')
    identifier(value['id'], 'source.id')
    for key in ('title', 'platform', 'language', 'group_id', 'context'):
        string(value[key], f'source.{key}')
    require(value['source_type'] in ('post', 'comment', 'review', 'official', 'article', 'provided'),
            'source.source_type: invalid type')
    require(value['access'] in ('full', 'excerpt', 'snippet', 'unavailable'), 'source.access: invalid access')
    if value['url'] is None:
        require(value['source_type'] == 'provided', 'source.url: required except for provided material')
    else:
        source_url(value['url'])
    if value['published_at'] is not None:
        iso_date(value['published_at'], 'source.published_at')
    iso_date(value['accessed_at'], 'source.accessed_at')
    strings(value['limitations'], 'source.limitations', 1 if value['access'] == 'unavailable' else 0)
    array(value['excerpts'], 'source.excerpts', 1 if value['access'] in ('full', 'excerpt') else 0)
    require(value['access'] != 'unavailable' or not value['excerpts'],
            'source.excerpts: unavailable sources cannot have excerpts')
    ids: set[str] = set()
    for excerpt in value['excerpts']:
        obj(excerpt, ('id', 'text', 'locator'), 'excerpt')
        identifier(excerpt['id'], 'excerpt.id')
        require(excerpt['id'] not in ids, 'source.excerpts: duplicate ID')
        ids.add(excerpt['id'])
        string(excerpt['text'], 'excerpt.text')
        string(excerpt['locator'], 'excerpt.locator')


def run(value: Any, sources: Mapping[str, JSONObject], has_brief: bool) -> None:
    obj(value, ('id', 'module', 'status', 'objective', 'method', 'queries', 'source_ids', 'limitations'), 'run')
    identifier(value['id'], 'run.id')
    require(has_brief, 'run: brief required')
    require(value['module'] in ('social', 'competitor'), 'run.module: expected social or competitor')
    require(value['status'] in ('partial', 'complete'), 'run.status: expected partial or complete')
    for key in ('objective', 'method'):
        string(value[key], f'run.{key}')
    strings(value['queries'], 'run.queries')
    strings(value['source_ids'], 'run.source_ids', unique=True)
    require(set(value['source_ids']) <= sources.keys(), 'run.source_ids: unknown source')
    strings(value['limitations'], 'run.limitations', 1 if value['status'] == 'partial' else 0)
    if value['status'] == 'complete':
        require(any(sources[i]['access'] in ('full', 'excerpt') for i in value['source_ids']),
                'run: complete requires at least one full/excerpt source')


def study(value: Any) -> None:
    obj(value, ('schema_version', 'title', 'revision', 'recipe', 'personas', 'interviews'), 'study',
        optional=('created_at', 'updated_at', 'brief', 'sources', 'runs'))
    require(type(value['schema_version']) is int and value['schema_version'] == 1, 'study: unsupported schema_version')
    string(value['title'], 'study.title')
    integer(value['revision'], 'study.revision')
    for key in ('created_at', 'updated_at'):
        if key in value:
            string(value[key], f'study.{key}')
    for key in ('personas', 'interviews', 'sources', 'runs'):
        array(value.get(key, []), f'study.{key}')
    ids: set[str] = set()

    def register(record: JSONObject) -> None:
        require(record['id'] not in ids, f'duplicate entity ID: {record["id"]}')
        ids.add(record['id'])

    if value.get('brief') is not None:
        brief(value['brief'])
        register(value['brief'])
    rec = value['recipe']
    if rec is None:
        require(not value['personas'] and not value['interviews'], 'study: recipe required before records')
    else:
        recipe(rec)
        register(rec)
    people = {}
    for item in value['personas']:
        persona(item, rec)
        register(item)
        people[item['id']] = item
    for item in value['interviews']:
        interview(item, people)
        register(item)
    sources = {}
    for item in value.get('sources', []):
        source(item)
        register(item)
        sources[item['id']] = item
    for item in value.get('runs', []):
        run(item, sources, value.get('brief') is not None)
        register(item)


def reference(value: Any, interviews: Mapping[str, JSONObject], sources: Mapping[str, JSONObject]) -> str:
    """Validate one reference against eligible selected records; return support type."""
    require(isinstance(value, dict), 'reference: expected an object')
    if 'interview_id' in value:
        obj(value, ('interview_id', 'turn'), 'reference')
        identifier(value['interview_id'], 'reference.interview_id')
        require(value['interview_id'] in interviews, 'reference: interview is not selected')
        integer(value['turn'], 'reference.turn', 1, len(interviews[value['interview_id']]['turns']))
        return 'simulation'
    obj(value, ('source_id', 'excerpt_id'), 'reference')
    identifier(value['source_id'], 'reference.source_id')
    identifier(value['excerpt_id'], 'reference.excerpt_id')
    require(value['source_id'] in sources, 'reference: source is not selected')
    item = sources[value['source_id']]
    require(item['access'] in ('full', 'excerpt'), 'reference: source requires full/excerpt access')
    require(value['excerpt_id'] in {e['id'] for e in item['excerpts']}, 'reference: unknown excerpt')
    return 'source'


def references(value: Any, path: str, interviews: Mapping[str, JSONObject],
               sources: Mapping[str, JSONObject], minimum: int = 1) -> set[str]:
    array(value, path, minimum)
    return {reference(ref, interviews, sources) for ref in value}


def report(value: Any, state: Study) -> None:
    obj(value, ('title', 'study_revision', 'status', 'summary', 'interview_ids', 'findings', 'next_steps', 'limitations'),
        'report', optional=('run_ids', 'comparisons', 'opportunities'))
    for key in ('title', 'summary'):
        string(value[key], f'report.{key}')
    integer(value['study_revision'], 'report.study_revision')
    require(value['study_revision'] == state['revision'], 'report: stale study_revision')
    require(value['status'] in ('partial', 'complete'), 'report.status: expected partial or complete')
    strings(value['interview_ids'], 'report.interview_ids', unique=True)
    strings(value.get('run_ids', []), 'report.run_ids', unique=True)
    selected = set(value['interview_ids'])
    selected_runs = set(value.get('run_ids', []))
    require(bool(selected or selected_runs), 'report: select at least one run or interview')
    all_interviews = {i['id']: i for i in state['interviews']}
    all_runs = {r['id']: r for r in state.get('runs', [])}
    require(selected <= all_interviews.keys(), 'report.interview_ids: unknown interview')
    require(selected_runs <= all_runs.keys(), 'report.run_ids: unknown run')
    interviews = {i: all_interviews[i] for i in selected}
    runs = [r for r in state.get('runs', []) if r['id'] in selected_runs]
    source_ids = {i for r in runs for i in r['source_ids']}
    sources = {s['id']: s for s in state.get('sources', []) if s['id'] in source_ids}
    if selected:
        covered = {i['persona_id'] for i in interviews.values()}
        require(state['recipe'] is not None and len(covered) <= state['recipe']['persona_count'],
                'report: selected persona coverage exceeds planned count')
        if value['status'] == 'complete':
            require(len(covered) == state['recipe']['persona_count'],
                    'report: complete requires planned persona coverage')
    if value['status'] == 'complete':
        require(all(r['status'] == 'complete' for r in runs), 'report: complete requires all selected runs complete')
    strings(value['next_steps'], 'report.next_steps')
    strings(value['limitations'], 'report.limitations', 1)
    array(value['findings'], 'report.findings', 1 if value['status'] == 'complete' else 0)
    if not value['findings']:
        require(not interviews and not any(s['access'] in ('full', 'excerpt') for s in sources.values()),
                'report.findings: empty only when selected collection has no eligible evidence')
    ids: set[str] = set()
    for finding in value['findings']:
        obj(finding, ('id', 'kind', 'statement', 'support', 'counterevidence', 'limitations'), 'finding')
        identifier(finding['id'], 'finding.id')
        require(finding['id'] not in ids, 'report.findings: duplicate ID')
        ids.add(finding['id'])
        require(finding['kind'] in ('simulation', 'source', 'inference', 'mixed'), 'finding.kind: invalid kind')
        string(finding['statement'], 'finding.statement')
        strings(finding['limitations'], 'finding.limitations', 1)
        support = references(finding['support'], 'finding.support', interviews, sources)
        references(finding['counterevidence'], 'finding.counterevidence', interviews, sources, 0)
        expected = {'simulation'} if finding['kind'] == 'simulation' else {'source'}
        if finding['kind'] == 'mixed':
            expected = {'simulation', 'source'}
        require(support == expected, f'finding.support: incompatible with {finding["kind"]} kind')
    array(value.get('comparisons', []), 'report.comparisons')
    for comparison in value.get('comparisons', []):
        obj(comparison, ('alternative', 'category', 'dimension', 'assessment', 'support', 'limitations'), 'comparison')
        for key in ('alternative', 'dimension', 'assessment'):
            string(comparison[key], f'comparison.{key}')
        require(comparison['category'] in ('direct', 'indirect', 'manual', 'do_nothing'), 'comparison.category: invalid category')
        strings(comparison['limitations'], 'comparison.limitations', 1)
        require(references(comparison['support'], 'comparison.support', interviews, sources) == {'source'},
                'comparison.support: source references required')
    array(value.get('opportunities', []), 'report.opportunities')
    for opportunity in value.get('opportunities', []):
        obj(opportunity, ('title', 'audience', 'problem', 'alternative', 'proposal', 'priority', 'rationale',
                          'support', 'risks', 'validation'), 'opportunity')
        for key in ('title', 'audience', 'problem', 'alternative', 'proposal', 'rationale', 'validation'):
            string(opportunity[key], f'opportunity.{key}')
        require(opportunity['priority'] in ('test_now', 'watch', 'drop'), 'opportunity.priority: invalid priority')
        strings(opportunity['risks'], 'opportunity.risks', 1)
        support = references(opportunity['support'], 'opportunity.support', interviews, sources)
        require(opportunity['priority'] != 'test_now' or 'source' in support,
                'opportunity.support: test_now requires source support')
