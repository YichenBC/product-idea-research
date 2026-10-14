# v0.1 data and CLI contract

This release supports method → synthetic personas → simulated interviews → report.
No crawler, persona library, independent LLM runtime, or demand-validation claim.
All text fields are plain text, not executable HTML/Markdown. UTF-8 JSON.
Unknown fields are errors (except arbitrary keys in persona `traits`). IDs match
`[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}` and are unique across all entity types.

## Commands

`research-workbench init DIR --title TEXT`

`research-workbench ingest DIR --file BATCH.json`

`research-workbench status DIR [--json]`

`research-workbench check DIR [--report REPORT.json]`

`research-workbench render DIR --report REPORT.json [--format both|md|html]`

`research-workbench install --target codex|claude --scope user|project [--directory DIR] [--dry-run]`

All successful commands emit JSON (status --json is a convenience alias).
Errors emit structured JSON to stderr with exit code 1; argparse usage errors use 2.
Install project scope uses --directory or cwd; user scope uses the actual home and
rejects --directory. Copy the same packaged skill into `.agents/skills/research-workbench`
for Codex and `.claude/skills/research-workbench` for Claude. Existing identical
installation is a no-op; differing files are a conflict, never silently overwritten.

## Study and ingestion

`research.json` stores schema_version=1, title, revision (starts at 0),
recipe (null initially), personas=[], interviews=[]. Additional internal timestamps
are allowed in the study format only. Batch keys are recipe, personas, interviews;
each optional, at least one required. Recipe is immutable once set. Persona and
interview records are immutable; same ID + same content is a no-op, conflicting
content is an error. New records append. Entire batch validates against merged
state before atomic replacement, under an exclusive write lock. Empty/no-op batches
must not increment revision. Incomplete studies are valid checkpoint states.
Corrections use new persona/interview IDs (or a new study for a revised recipe).
Report chooses the interview IDs relevant to that iteration; older records remain.

### Recipe

```json
{
  "id": "recipe-1",
  "question": "Which scheduling trade-offs should we test with real users?",
  "method": "Contrast user vs approver and fixed vs variable shifts.",
  "dimensions": [
    {"name": "role", "values": ["user", "approver"]},
    {"name": "schedule", "values": ["fixed", "variable"]}
  ],
  "constraints": ["No browsing", "Include someone satisfied with spreadsheets"],
  "persona_count": 4,
  "language": "en"
}
```

question/method/language and dimension names/values are nonempty strings.
Dimensions is a nonempty list with unique names and unique nonempty values.
persona_count is an integer 1–30 (not bool); constraints is a list of nonempty strings.

### Persona

```json
{
  "id": "p-1",
  "label": "Fixed-shift employee",
  "recipe_id": "recipe-1",
  "traits": {"role": "user", "schedule": "fixed"},
  "attributes": [
    {"name": "workflow", "value": "Checks next week's rota on a shared sheet", "basis": "assumed", "rationale": "Scenario assumption for this simulation"},
    {"name": "budget", "value": "Unknown", "basis": "unknown", "rationale": "No buyer data supplied"}
  ]
}
```

All recipe dimensions must be present in traits with values from the declared
options; no undeclared dimensions. A persona has at least one attribute, names
unique, all values/rationales nonempty. v0.1 allows only assumed/unknown basis:
these are synthetic role cards, not evidence-backed biographies. Distinct personas
may share dimension combinations but should differ meaningfully in their attributes.
Personas can be saved incrementally; additional cards allow corrections using new
IDs while preserving older interviews. The report selects the active interview/card
set; unused cards remain archived in the study snapshot. Never force missing data
into fabricated observations. Evidence-backed attributes will be a later feature.

### Interview

```json
{
  "id": "i-1",
  "persona_id": "p-1",
  "synthetic": true,
  "turns": [
    {"question": "How would you check a shift change?", "answer": "In this scenario I would check the shared sheet.", "assumptions": ["The sheet is accessible on a phone"]},
    {"question": "What could make that sufficient without another app?", "answer": "A stable rota and clear change notifications would be sufficient.", "assumptions": []}
  ]
}
```

At least two nonempty question/answer turns, assumptions is a list of nonempty
strings (may be empty). References must resolve. synthetic must be exactly true.
Stored personas are immutable, so interview references pin exact role cards.

### Report draft (separate file, supplied to check/render)

```json
{
  "title": "Scheduling concept: simulation findings",
  "study_revision": 3,
  "status": "partial",
  "summary": "A hypothesis to investigate, not a demand validation result.",
  "interview_ids": ["i-1"],
  "findings": [
    {"id": "f-1", "kind": "simulation", "statement": "Notification clarity may matter more than replacing a sheet.", "support": [{"interview_id": "i-1", "turn": 2}], "counterevidence": [], "limitations": ["One synthetic role; no real customer evidence"]}
  ],
  "next_steps": ["Observe real scheduling changes with consenting users"],
  "limitations": ["All personas and answers are AI simulations"]
}
```

status is partial or complete. kind is always simulation. summary/title nonempty.
At least one finding, each with nonempty statement, >=1 valid support, optional
empty counterevidence (same reference schema), >=1 limitation. Report has >=1
limitation; next_steps is a string list. All referenced interviews must be selected
in interview_ids (nonempty unique). turn is a one-based integer (not bool).
Report study_revision must equal current study revision. Complete requires exactly
recipe.persona_count distinct personas covered by selected interviews. Partial may
cover fewer (or the same number when the study is incomplete for another reason);
neither status permits exceeding the planned number in the selected report.
Multiple interviews for one persona count as one persona. Finding IDs unique in report.
There is no structural way to validate prose truthfulness; the skill and reviewer
must verify that cited turns actually support each statement.

## Rendering and recovery

Render validates first, freezes a coherent study + report snapshot, and creates a
new reports/NNN directory containing report.md and/or report.html, study.json and
report.json. Never overwrite previous reports. If interrupted during rendering,
no final report directory should appear; intermediate study records remain usable.
Hold the study lock during snapshot/render commit to prevent races.

Include a prominent synthetic-research notice, method, actual/planned persona
counts, completion status, role cards and assumptions, findings with links to
specific interview turns, counterevidence, limitations, real-world next steps,
and full transcripts. All user strings are escaped for both HTML and Markdown.
HTML is self-contained with inline CSS and no external assets/scripts. Its links
use generated internal IDs only. Display language follows recipe.language for
built-in labels (zh* Chinese, otherwise English); content is supplied by the Agent.
Reports are local; render never uploads, publishes, or runs code from input.

## Verification targets

CLI subprocess E2E; idempotency; all-or-nothing failed batch; invalid enum/type,
unknown fields and missing refs; partial checkpoints; incorrect completeness;
stale revision; safe HTML and Markdown; immutable snapshots; install idempotency
and conflict; wheel includes skill; run outside source checkout. Test real behavior,
not specific prose wording. Runtime standard library only, Python >=3.11.
