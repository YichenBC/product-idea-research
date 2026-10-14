"""Strict validation for JSON records; no input prose is executed."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import re
from typing import Any

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


def study(value: Any) -> None:
    obj(value, ('schema_version', 'title', 'revision', 'recipe', 'personas', 'interviews'), 'study',
        optional=('created_at', 'updated_at'))
    require(type(value['schema_version']) is int and value['schema_version'] == 1, 'study: unsupported schema_version')
    string(value['title'], 'study.title')
    integer(value['revision'], 'study.revision')
    for key in ('created_at', 'updated_at'):
        if key in value:
            string(value[key], f'study.{key}')
    array(value['personas'], 'study.personas')
    array(value['interviews'], 'study.interviews')
    if value['recipe'] is None:
        require(not value['personas'] and not value['interviews'], 'study: recipe required before records')
        return
    rec = value['recipe']
    recipe(rec)
    ids = {rec['id']}
    people = {}
    for p in value['personas']:
        persona(p, rec)
        require(p['id'] not in ids, f'duplicate entity ID: {p["id"]}')
        ids.add(p['id'])
        people[p['id']] = p
    for item in value['interviews']:
        interview(item, people)
        require(item['id'] not in ids, f'duplicate entity ID: {item["id"]}')
        ids.add(item['id'])


def report(value: Any, state: Study) -> None:
    obj(value, ('title', 'study_revision', 'status', 'summary', 'interview_ids', 'findings', 'next_steps', 'limitations'), 'report')
    for key in ('title', 'summary'):
        string(value[key], f'report.{key}')
    integer(value['study_revision'], 'report.study_revision')
    require(value['study_revision'] == state['revision'], 'report: stale study_revision')
    require(value['status'] in ('partial', 'complete'), 'report.status: expected partial or complete')
    strings(value['interview_ids'], 'report.interview_ids', 1, unique=True)
    selected = set(value['interview_ids'])
    interviews = {i['id']: i for i in state['interviews']}
    require(selected <= interviews.keys(), 'report.interview_ids: unknown interview')
    covered = {interviews[i]['persona_id'] for i in selected}
    require(state['recipe'] is not None and len(covered) <= state['recipe']['persona_count'],
            'report: selected persona coverage exceeds planned count')
    if value['status'] == 'complete':
        require(state['recipe'] is not None and len(covered) == state['recipe']['persona_count'],
                'report: complete requires planned persona coverage')
    strings(value['next_steps'], 'report.next_steps')
    strings(value['limitations'], 'report.limitations', 1)
    array(value['findings'], 'report.findings', 1)
    ids = set()
    for finding in value['findings']:
        obj(finding, ('id', 'kind', 'statement', 'support', 'counterevidence', 'limitations'), 'finding')
        identifier(finding['id'], 'finding.id')
        require(finding['id'] not in ids, 'report.findings: duplicate ID')
        ids.add(finding['id'])
        require(finding['kind'] == 'simulation', 'finding.kind: must be simulation')
        string(finding['statement'], 'finding.statement')
        strings(finding['limitations'], 'finding.limitations', 1)
        for key, minimum in (('support', 1), ('counterevidence', 0)):
            array(finding[key], f'finding.{key}', minimum)
            for ref in finding[key]:
                obj(ref, ('interview_id', 'turn'), 'reference')
                identifier(ref['interview_id'], 'reference.interview_id')
                require(ref['interview_id'] in selected, 'reference: interview is not selected')
                integer(ref['turn'], 'reference.turn', 1, len(interviews[ref['interview_id']]['turns']))
