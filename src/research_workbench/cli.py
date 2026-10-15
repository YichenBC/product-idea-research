"""Command line interface; all results and failures are JSON."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import NoReturn

from . import __version__, store, validation as v
from .install import install
from .audit import audit
from .render import render
from .types import JSONObject, Study


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.exit(2, json.dumps({'error': {'code': 'usage_error', 'message': message}}, ensure_ascii=True) + '\n')


def parser() -> Parser:
    p = Parser(prog='research-workbench')
    p.add_argument('--version', action='version', version=__version__)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Create a local study')
    init.add_argument('directory', type=Path)
    init.add_argument('--title', required=True)
    ingest = sub.add_parser('ingest', help='Atomically ingest immutable records')
    ingest.add_argument('directory', type=Path)
    ingest.add_argument('--file', required=True, type=Path)
    status = sub.add_parser('status', help='Describe a checkpoint')
    status.add_argument('directory', type=Path)
    status.add_argument('--json', action='store_true')
    check = sub.add_parser('check', help='Validate a study and optional report draft')
    check.add_argument('directory', type=Path)
    check.add_argument('--report', type=Path)
    evidence = sub.add_parser('audit', help='Explain evidence coverage and duplication')
    evidence.add_argument('directory', type=Path)
    evidence.add_argument('--report', type=Path)
    output = sub.add_parser('render', help='Create an immutable report snapshot')
    output.add_argument('directory', type=Path)
    output.add_argument('--report', required=True, type=Path)
    output.add_argument('--format', choices=('both', 'md', 'html'), default='both')
    inst = sub.add_parser('install', help='Install packaged skill')
    inst.add_argument('--target', required=True, choices=('codex', 'claude'))
    inst.add_argument('--scope', required=True, choices=('user', 'project'))
    inst.add_argument('--directory', type=Path)
    inst.add_argument('--dry-run', action='store_true')
    return p


def status(state: Study) -> JSONObject:
    rec = state['recipe']
    return {'ok': True, 'title': state['title'], 'revision': state['revision'],
            'recipe_id': rec['id'] if rec else None, 'personas': len(state['personas']),
            'planned_personas': rec['persona_count'] if rec else None,
            'interviews': len(state['interviews']),
            'interviewed_personas': len({i['persona_id'] for i in state['interviews']}),
            'brief_id': state['brief']['id'] if state.get('brief') else None,
            'sources': len(state.get('sources', [])), 'runs': len(state.get('runs', [])),
            'modules': dict(sorted(Counter(r['module'] for r in state.get('runs', [])).items()))}


def execute(args: argparse.Namespace) -> JSONObject:
    if args.command == 'install':
        return install(args.target, args.scope, args.directory, args.dry_run)
    if args.command == 'init':
        return status(store.initialize(args.directory, args.title))
    if args.command == 'ingest':
        return status(store.ingest(args.directory, store.read_json(args.file)))
    if args.command == 'render':
        return render(args.directory, store.read_json(args.report), args.format)
    with store.lock(args.directory):
        state = store.load(args.directory)
        draft = None
        if args.command in ('check', 'audit') and args.report:
            draft = store.read_json(args.report)
            v.report(draft, state)
        if args.command == 'audit':
            return audit(state, draft)
        return status(state)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = execute(args)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (v.WorkbenchError, OSError, UnicodeError, RecursionError, ValueError) as exc:
        print(json.dumps({'error': {'code': 'validation_error' if isinstance(exc, v.WorkbenchError) else 'io_error',
                                    'message': str(exc)}}, ensure_ascii=True), file=sys.stderr)
        return 1
