"""Shared boundary types; runtime validators enforce the detailed JSON schema."""

from os import PathLike
from typing import Any, TypeAlias

JSONValue: TypeAlias = 'None | bool | int | float | str | list[JSONValue] | dict[str, JSONValue]'
# Validated records are heterogeneous. Their field-level contracts live in
# validation.py, avoiding a second, independently maintained schema hierarchy.
JSONObject: TypeAlias = dict[str, Any]
Study: TypeAlias = JSONObject
PathInput: TypeAlias = str | PathLike[str]
