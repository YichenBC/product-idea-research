# Contributing

Keep changes focused on a reproducible user behavior. For a bug report, provide
the CLI version, OS/Python version, command, and a minimal synthetic JSON input.
Do not upload credentials, real customer transcripts or private research.

Run `python -m pip install -e '.[dev]'` and `python -m pytest -q`.
Add behavioral regression tests for data loss, invalid references, rendering or
installation bugs. For skill changes, also run a realistic agent task: a schema
test cannot tell whether a simulated interviewer asks useful follow-up questions.

The canonical skill is `src/research_workbench/skill/`. The same files are packaged
and installed for both hosts. Keep the bundled contract synchronized with
`docs/contract.md`; avoid platform-specific tool names in the shared instructions.

Do not introduce paid services or network access into the CLI without an explicit
design discussion. Persona libraries and source collectors are intentionally
outside v0.1. Keep generated research local by default.
