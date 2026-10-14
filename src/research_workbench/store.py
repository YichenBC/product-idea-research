"""Locked, atomic local study storage."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
import copy
import json
import os
from pathlib import Path
import tempfile
from typing import cast

from . import validation as v
from .types import JSONObject, JSONValue, PathInput, Study


def _pairs(pairs: Iterable[tuple[str, JSONValue]]) -> JSONObject:
    result = {}
    for key, val in pairs:
        v.require(key not in result, f'JSON: duplicate key {key}')
        result[key] = val
    return result


def read_json(path: PathInput) -> JSONValue:
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=_pairs,
                          parse_constant=lambda token: (_ for _ in ()).throw(v.WorkbenchError(f'JSON: invalid {token}')))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise v.WorkbenchError(f'Invalid JSON in {path}: {exc}') from exc


def write_json(path: PathInput, data: JSONValue) -> None:
    path = Path(path)
    fd, tmp = tempfile.mkstemp(prefix=f'.{path.name}-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def lock(directory: PathInput) -> Iterator[None]:
    """OS releases the exclusive advisory lock even after process termination."""
    path = Path(directory)
    v.require(path.is_dir(), f'Study directory does not exist: {path}')
    with (path / '.research.lock').open('a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.seek(0, 2)
            if handle.tell() == 0:
                handle.write(b'0')
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load(directory: PathInput) -> Study:
    result = read_json(Path(directory) / 'research.json')
    v.study(result)
    return cast(Study, result)


def initialize(directory: PathInput, title: str) -> Study:
    v.string(title, 'title')
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    with lock(path):
        v.require(not (path / 'research.json').exists(), 'Study already initialized')
        result = {'schema_version': 1, 'title': title, 'revision': 0,
                  'recipe': None, 'personas': [], 'interviews': []}
        write_json(path / 'research.json', result)
    return result


def ingest(directory: PathInput, batch: JSONValue) -> Study:
    v.obj(batch, (), 'batch', optional=('recipe', 'personas', 'interviews'))
    batch = cast(JSONObject, batch)
    v.require(bool(batch), 'batch: at least one field is required')
    with lock(directory):
        current = load(directory)
        merged = copy.deepcopy(current)
        if 'recipe' in batch:
            v.recipe(batch['recipe'])
            v.require(merged['recipe'] is None or merged['recipe'] == batch['recipe'], 'recipe: immutable conflict')
            merged['recipe'] = batch['recipe']
        for key in ('personas', 'interviews'):
            if key not in batch:
                continue
            v.array(batch[key], f'batch.{key}')
            records = {r['id']: r for r in merged[key]}
            for record in batch[key]:
                v.require(isinstance(record, dict), f'batch.{key}: expected objects')
                v.identifier(record.get('id'), f'batch.{key}.id')
                ident = record['id']
                if ident in records:
                    v.require(json.dumps(records[ident], sort_keys=True) == json.dumps(record, sort_keys=True),
                              f'{key}: immutable conflict for {ident}')
                else:
                    merged[key].append(record)
                    records[ident] = record
        v.study(merged)
        if merged != current:
            merged['revision'] += 1
            write_json(Path(directory) / 'research.json', merged)
        return merged
