# Research Workbench

**Your research method → synthetic personas → simulated interviews → a traceable report.**

A shared skill for **Codex and Claude Code**, backed by a small local Python CLI.
The Agent creates the personas, asks follow-up questions and interprets answers.
The CLI saves checkpoints, checks references and exports Markdown and standalone HTML.

No persona database, external research service, additional model API key or server
is required. Your usual coding-agent usage still applies. This is a tool for
exploring hypotheses and rehearsing interviews, **not evidence that real customers
want a product or will pay for it**.

[中文说明](README.zh-CN.md) · [Example report](examples/scheduling/report.md) ·
[HTML report source (download to view)](examples/scheduling/report.html) ·
[Data contract](docs/contract.md) · [Evaluation record](evals/README.md)

## Install

Requires Python 3.11+, Git, and either Codex or Claude Code with terminal/file access.

```bash
git clone https://github.com/YichenBC/research-workbench.git
cd research-workbench
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .

# Choose one or both. No existing skill is overwritten.
research-workbench install --target codex --scope user
research-workbench install --target claude --scope user
```

Keep this environment activated when launching your coding agent so the CLI is
on PATH. Alternatively install the cloned project with `pipx install .` or
`uv tool install .` if you already use one of those tools. No PyPI release is
required. Restart an existing agent session if the installed skill is not discovered.

For a project-only installation:

```bash
research-workbench install --target codex --scope project --directory /path/to/project
research-workbench install --target claude --scope project --directory /path/to/project
```

Both receive the same packaged `SKILL.md` and references. Codex uses `.agents/skills/`;
Claude Code uses `.claude/skills/`. Add `--dry-run` to inspect the destination.
Identical installations are harmless to repeat; conflicts are reported.
For upgrading or uninstalling, see [installation notes](docs/installation.md).

## Use it in your agent

In Codex, invoke `$research-workbench`; in Claude Code, invoke `/research-workbench`.
Then give a question and a method, for example:

> Explore a shift-scheduling concept. Compare a frontline employee satisfied with
> a stable spreadsheet rota and a supervisor handling frequent changes. Create two
> personas, conduct three-turn simulated interviews, and produce an English report.
> Do not browse. Save to studies/scheduling.

Or use a completely different domain:

> Help me explore a group-travel planning idea. Use three contrasting approaches
> to planning rather than demographic stereotypes. Propose the role assumptions,
> simulate interviews and write a Chinese report. No browsing.

You can stop after persona creation, resume interviews later, or ask for a new
report from saved interviews. A user-specified method takes precedence over the
skill's suggested interview structure. Work and everyday-life scenarios are both
supported; roles do not need a business budget or procurement authority.

## What gets saved

```text
studies/scheduling/
  research.json          # recipe, immutable personas and interview checkpoints
  ...draft JSON files... # written by your Agent
  reports/001/
    report.md
    report.html          # self-contained; no scripts or remote assets
    study.json           # frozen study snapshot
    report.json          # frozen report draft
```

The report includes the method, role assumptions, findings, counterarguments,
links to exact interview turns, limitations, real-world next steps and full
transcripts. Every report carries a synthetic-research notice. A new render creates
a new numbered directory, preserving earlier reports.

## Replay the included example without a model

This replays a **hand-authored synthetic fixture**, not a fresh AI study:

```bash
research-workbench init studies/demo --title "Scheduling concept"
research-workbench ingest studies/demo --file examples/scheduling/batch.json
research-workbench check studies/demo --report examples/scheduling/report-draft.json
research-workbench render studies/demo --report examples/scheduling/report-draft.json
research-workbench status studies/demo --json
```

To create new content, use the skill in your Agent. The CLI by itself never
generates personas or responses. [Actual host evaluations](evals/README.md) are
documented separately from this deterministic example.

## CLI

| Command | Purpose |
|---|---|
| `init` | Create a study without overwriting one |
| `ingest` | Atomically save a recipe, persona cards or interviews from JSON |
| `status` | Show saved, planned and interviewed role counts |
| `check` | Validate structure, references, coverage and report revision |
| `render` | Create Markdown/HTML and frozen JSON snapshots |
| `install` | Install the shared skill for either host |

Run `research-workbench --help` or see the [full contract](docs/contract.md).
Input records are immutable. Re-ingesting identical records is a no-op; conflicting
content is rejected. Use new persona/interview IDs for corrections. A materially
different method starts a new study. Partial studies can be resumed without losing
the roles and interviews already saved.

## Scope and limits

- v0.1 implements the simulation workflow. Shared persona libraries, crawling,
  social listening and competitor-research modules are not shipped yet.
- Role attributes are explicitly `assumed` or `unknown`. Evidence-backed persona
  records will require a later data model; do not import real-user data as if
  this version verified it.
- `complete` means the requested role count was interviewed, not that a market or
  product was validated. Synthetic respondents are not a statistical sample.
- Structural checks catch broken citations and missing roles. They cannot decide
  whether prose is true or whether a cited turn really supports an interpretation.
- The CLI is local and offline. The coding agent still processes prompts through
  its configured model service. No automatic outreach or publishing is included.

## Develop

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

The canonical skill lives in `src/research_workbench/skill/` and ships inside the
Python package. Keep its data-contract reference synchronized with `docs/contract.md`.
See [contributing](CONTRIBUTING.md) and the [evaluation checklist](evals/cases.md).

MIT licensed. Examples are fictional, authored for this repository.
