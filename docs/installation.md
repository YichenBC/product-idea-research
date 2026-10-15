# Installation and updates

Use Python 3.11 or later. On systems where `python3` is older, choose an installed
newer Python explicitly (for example `python3.12 -m venv .venv`). The CLI runtime
uses only the standard library. Build tools and pytest are development dependencies.

The skill and CLI are versioned together. Install the Python package, then run
`product-idea-research install` for the desired host. A wheel installation includes
the skill; running from the source directory is not necessary.

| Host | User installation | Project installation |
|---|---|---|
| Codex | `~/.agents/skills/product-idea-research/` | `<project>/.agents/skills/product-idea-research/` |
| Claude Code | `~/.claude/skills/product-idea-research/` | `<project>/.claude/skills/product-idea-research/` |

`--directory` selects the project root and is only valid with `--scope project`.
Existing identical files produce a no-op; differing files produce a conflict.
The installer never edits other skills, agent settings, shell profiles or API keys.

## Rename from Research Workbench (v0.2 and earlier)

The public package, repository, command and skill are now `product-idea-research`.
The Python module is `product_idea_research`. The new package also provides the
old `research-workbench` command and `python -m research_workbench` as forwarding
entry points; internal legacy Python submodules are not a supported API.

For an existing checkout, update its remote and keep using the same local folder:

```bash
git remote set-url origin https://github.com/YichenBC/product-idea-research.git
git pull --ff-only
```

In the environment where the old package was installed, uninstall the old package
**before** installing the new one. Both distributions can otherwise own the old
command, and uninstalling either afterwards can remove that shared executable.

```bash
python -m pip uninstall research-workbench
python -m pip install .
```

For pipx/uv tool installations, uninstall the old tool with the same manager, then
install this checkout with `pipx install .` or `uv tool install .`.

Back up and move the old `research-workbench` skill folder outside the host's
skill-discovery directory, preserving any custom edits. Install the renamed skill
for your chosen host:

```bash
product-idea-research install --target codex --scope user
product-idea-research install --target claude --scope user
```

The installer reports a warning if it finds the old folder; it never deletes or
rewrites it. Restart the host if needed. New invocations are `$product-idea-research`
in Codex and `/product-idea-research` in Claude Code. Existing studies and report
snapshots require no data migration and remain readable.

## Update

Update the Python package from a reviewed repository revision. Back up the existing
installed `product-idea-research` skill folder outside the host's skill-discovery
directory, then run install again. This explicit procedure preserves custom edits
instead of silently replacing them. Do not leave an old copy with the same skill
name inside a discovered skills directory.

## Uninstall

Remove only the `product-idea-research` skill folder from the host/location where you
installed it. Uninstall the package using the same environment/tool used to install
it (`python -m pip uninstall product-idea-research`, `uv tool uninstall product-idea-research`,
or `pipx uninstall product-idea-research`). Your study folders are separate and remain.

## Troubleshooting

- **CLI not found:** activate the environment in the terminal used to launch the
  Agent, or make your pipx/uv tool executable directory available on PATH.
- **Skill not discovered:** verify the target directory and restart the agent session.
- **Invalid JSON:** use the packaged data-contract reference and inspect the error
  path. Do not add model commentary outside the JSON object.
- **ID conflict:** records are immutable; reuse identical content or create a new
  source/run/persona/interview ID. Revised overall questions or methods belong in a new study.
- **Stale report:** read the changed study and reconcile your findings, then use its
  current revision. A revision number is not a substitute for reviewing changes.
- **Permission denial:** ensure the host is allowed to write the chosen study
  directory and execute the installed CLI. The skill does not bypass host permissions.

## Research access

The CLI does not supply browser sessions or platform APIs. Live research uses the
host's authorized search/browser tools. If a platform is unavailable, keep a partial
run and its limitations, or use supplied exports. A “no browsing” request can be
fulfilled with saved/supplied materials; it does not require a network call.
