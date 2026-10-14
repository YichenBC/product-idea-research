"""Install the packaged skill without overwriting local modifications."""

from __future__ import annotations

from importlib.resources import files
from importlib.resources.abc import Traversable
import os
from pathlib import Path
import shutil
import tempfile

from . import store
from .types import JSONObject, PathInput
from .validation import require


def resource_files(root: Traversable, prefix: str = '') -> dict[str, bytes]:
    result = {}
    for item in root.iterdir():
        name = prefix + item.name
        if item.is_dir():
            result.update(resource_files(item, name + '/'))
        else:
            result[name] = item.read_bytes()
    return result


def install(target: str, scope: str, directory: PathInput | None = None,
            dry_run: bool = False) -> JSONObject:
    require(not (scope == 'user' and directory is not None), '--directory is only valid for project scope')
    base = Path.home() if scope == 'user' else Path(directory or Path.cwd())
    destination = base / ('.agents' if target == 'codex' else '.claude') / 'skills' / 'research-workbench'
    expected = resource_files(files('research_workbench').joinpath('skill'))
    require('SKILL.md' in expected, 'Packaged skill is missing SKILL.md')

    def inspect() -> bool:
        require(not destination.is_symlink(), f'Installation conflict: {destination} is a symlink')
        if not destination.exists():
            return False
        require(destination.is_dir(), f'Installation conflict: {destination} is not a directory')
        actual = {}
        for p in destination.rglob('*'):
            require(not p.is_symlink(), f'Installation conflict: symlink {p}')
            if p.is_file():
                actual[p.relative_to(destination).as_posix()] = p.read_bytes()
        require(actual == expected, f'Installation conflict: differing files in {destination}')
        return True

    if dry_run:
        exists = inspect()
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with store.lock(destination.parent):
            exists = inspect()
            if not exists:
                temporary = Path(tempfile.mkdtemp(prefix='.install-', dir=destination.parent))
                try:
                    for name, content in expected.items():
                        output = temporary / name
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_bytes(content)
                    require(not destination.exists(), f'Installation conflict: {destination}')
                    os.rename(temporary, destination)
                finally:
                    if temporary.exists():
                        shutil.rmtree(temporary)
    return {'ok': True, 'destination': str(destination.resolve()), 'dry_run': dry_run,
            'action': 'unchanged' if exists else 'install'}
