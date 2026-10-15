# Data and CLI contract (v0.4, study schema 1)

Social research, competitor research and simulated interviews can run separately
or contribute to one report. The host collects/generates content; the CLI is
offline. No platform crawler, persona library or independent LLM runtime required.
All text fields are plain text, not executable HTML/Markdown. UTF-8 JSON.
Unknown fields are errors (except arbitrary keys in persona `traits`). IDs match
`[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}` and are unique across all entity types.

## Commands

`product-idea-research init DIR --title TEXT`

`product-idea-research ingest DIR --file BATCH.json`

`product-idea-research status DIR [--json]`

`product-idea-research check DIR [--report REPORT.json]`

`product-idea-research audit DIR [--report REPORT.json]`

`product-idea-research pool DIR [--report REPORT.json] [--review]`

`product-idea-research render DIR --report REPORT.json [--format both|md|html]`

`product-idea-research install --target codex|claude --scope user|project [--directory DIR] [--dry-run]`

Successful subcommands emit JSON (status --json is a convenience alias).
Top-level `--help` and `--version` emit plain text; do not JSON-decode them.
Errors emit structured JSON to stderr with exit code 1; argparse usage errors use 2.
Install project scope uses --directory or cwd; user scope uses the actual home and
rejects --directory. Copy the same packaged skill into `.agents/skills/product-idea-research`
for Codex and `.claude/skills/product-idea-research` for Claude. Existing identical
installation is a no-op; differing files are a conflict, never silently overwritten.

## Study and ingestion

`research.json` stores schema_version=1, title, revision (starts at 0),
recipe (null initially), personas=[], interviews=[], brief=null, sources=[], runs=[].
Legacy studies may omit brief/sources/runs; reads do not rewrite them. Additional
internal timestamps are allowed in the study format only. Batch keys are recipe,
personas, interviews, brief, sources, runs, needs;
each optional, at least one required. Recipe and brief are immutable once set. All records are immutable; same ID + same content is a no-op, conflicting
content is an error. New records append. Entire batch validates against merged
state before atomic replacement, under an exclusive write lock. Empty/no-op batches
must not increment revision. Incomplete studies are valid checkpoint states.
Corrections use new record IDs (or a new study for a revised overall question/recipe).
Reports select run and interview IDs for that iteration; older records remain.
Source excerpt IDs are unique within each source; all entity record IDs are unique
across brief, recipe, sources, runs, personas, interviews and needs.

### Shared brief, sources and module runs

A social/competitor run requires a brief. Sources may be checkpointed before a run.
A shared brief does not prescribe modules: later work can extend the study.
Pure simulation needs only its existing recipe, not a brief.

A complete minimal social batch (fictional example):

```json
{
  "brief": {
    "id": "brief-1",
    "question": "What creates scheduling handoff friction?",
    "language": "en",
    "constraints": ["Use the supplied fictional feedback only"]
  },
  "sources": [{
    "id": "source-1",
    "title": "Fictional team feedback",
    "url": null,
    "platform": "provided",
    "source_type": "provided",
    "published_at": null,
    "accessed_at": "2026-10-15",
    "language": "en",
    "access": "excerpt",
    "group_id": "feedback-session-1",
    "context": "Authored fixture, not a real customer interview.",
    "excerpts": [{"id": "e1", "text": "The sheet works; I just miss changes.", "locator": "feedback.txt line 1"}],
    "limitations": ["Fictional test material; no empirical demand evidence"]
  }],
  "runs": [{
    "id": "social-1",
    "module": "social",
    "status": "complete",
    "objective": "Analyze the supplied feedback",
    "method": "Read the provided line and identify task and current alternative",
    "queries": [],
    "source_ids": ["source-1"],
    "limitations": ["One fictional supplied record"]
  }]
}
```

Brief requires id/question/language/constraints. All strings nonempty; constraints
is a string list, possibly empty. Unlike the recipe, no persona dimensions/count.

Every source field shown is required:

| Field | Rules |
|---|---|
| id, title, platform, language, group_id, context | Nonempty text; id follows global ID rules |
| url | http/https with a host; null only for `provided`; no credentials, whitespace/control characters or backslash |
| source_type | `post`, `comment`, `review`, `official`, `article`, `provided` |
| published_at | Valid `YYYY-MM-DD` or null when unknown |
| accessed_at | Valid `YYYY-MM-DD`, actual retrieval date |
| access | `full`, `excerpt`, `snippet`, `unavailable` |
| excerpts | Objects with id (ID rules), text and locator; IDs unique within source |
| limitations | String list; >=1 when unavailable |

`full`/`excerpt` requires >=1 excerpt. `snippet` may contain excerpts but cannot
support report references. `unavailable` requires zero excerpts. Access depth is
reported by the host, not independently verified by the CLI. Context describes
which body/comment/parent was read. Keep excerpt text verbatim and short; paraphrase
in findings. `group_id` is a discussion/document family, not a customer identity.
The CLI never fetches URLs. Sources are immutable; re-reading a changed page uses a
new source ID, so citations continue to pin the original excerpt.

Runs have exactly the fields shown above. Module is `social` or `competitor`;
status is `partial` or `complete`; objective/method are nonempty. Queries and
limitations are string lists. source_ids is a unique string list resolving to
stored sources. Complete requires >=1 full/excerpt source. Partial requires >=1
limitation and may have no sources. Completion is research-scope coverage, not
proof of demand. Preserve queries actually used, not a retroactively ideal plan.

For completely blocked collection, save a partial run with source_ids=[] and a
specific access limitation. Sources can be ingested in batches; append the run
when ready. Identical repeated ingestion is a no-op.

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
unique, all values/rationales nonempty. Only assumed/unknown basis is allowed:
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

status is partial or complete. title/summary nonempty. All report fields in the
example are required. Optional fields are `run_ids`, `need_ids`, `comparisons`, `opportunities`.
Missing run_ids means []; interview_ids may be [] when >=1 run is selected.
Select at least one run or interview. IDs in each selection are unique and resolve.

References are strictly one of:

```json
{"interview_id": "i-1", "turn": 2}
```

```json
{"source_id": "source-1", "excerpt_id": "e1"}
```

Interview refs must select a report interview; turn is a one-based integer, not
bool. Source refs must belong to a selected run and select a saved excerpt in a
full/excerpt source. Sources that are only stored but not selected cannot support
this report. Search snippets and unavailable content are rejected as evidence.

Findings require unique id, kind, nonempty statement, >=1 support reference,
counterevidence list (possibly empty), >=1 limitation. Supported kinds:

| kind | Support rule | Meaning |
|---|---|---|
| simulation | Only interview refs | Generated hypothetical answers |
| source | Only source refs | What a source actually says/claims |
| inference | Only source refs | Researcher's interpretation of external material |
| mixed | Both types | External material combined with explicitly identified simulation |

Counterevidence can use either reference type; it does not upgrade support.
There is no structural way to validate prose truthfulness or entailment. The host
must check context, self-report, vendor claims and whether references support the
statement. `source` does not mean independently verified world fact.

At least one finding for a complete report. Partial may have zero findings only when no eligible external evidence or
interviews were selected (blocked/unusable collection), with limitations and
meaningful next steps. Every report
requires >=1 limitation; next_steps is a string list. study_revision equals the
current saved revision. Complete requires every selected run complete; if interviews
are selected it also requires exactly recipe.persona_count distinct personas covered.
Partial cannot exceed the planned persona count either. Unselected stored roles do
not force interviews into a source-only report. Multiple interviews for one persona
count as one role. Missing requested work must remain partial rather than being
silently dropped from selection.

For the minimal source batch above, a source-only report at revision 1 is:

```json
{
  "title": "Scheduling feedback review",
  "study_revision": 1,
  "status": "complete",
  "summary": "The supplied fictional feedback suggests investigating change visibility before replacing the sheet.",
  "interview_ids": [],
  "run_ids": ["social-1"],
  "findings": [{
    "id": "f-1", "kind": "source",
    "statement": "The supplied fictional speaker says the sheet works but changes are missed.",
    "support": [{"source_id": "source-1", "excerpt_id": "e1"}],
    "counterevidence": [],
    "limitations": ["Authored test fixture, not real user evidence"]
  }],
  "next_steps": ["Observe how a real team notices changes to its current schedule"],
  "limitations": ["This example demonstrates data flow, not validated demand"]
}
```

### Optional comparison and opportunity rows

`comparisons` is a list of objects, all fields required per row:

```json
{
  "alternative": "Existing spreadsheet",
  "category": "manual",
  "dimension": "Change visibility",
  "assessment": "The fictional feedback describes missed changes despite an otherwise sufficient sheet.",
  "support": [{"source_id": "source-1", "excerpt_id": "e1"}],
  "limitations": ["Single fictional scenario; no product test"]
}
```

Category is direct/indirect/manual/do_nothing. Nonempty text fields, >=1 source-only
support and >=1 limitation. No simulated proof of competitor capabilities.

`opportunities` is a list of objects, all fields required per row:

```json
{
  "title": "Change acknowledgment experiment",
  "audience": "Teams coordinating on a sheet",
  "problem": "Changes may be missed",
  "alternative": "Existing sheet and messages",
  "proposal": "Compare a notification linked to the existing sheet",
  "priority": "watch",
  "rationale": "The supplied fictional scenario suggests a question, not a real buyer need.",
  "support": [{"source_id": "source-1", "excerpt_id": "e1"}],
  "risks": ["Current chat notifications may already suffice"],
  "validation": "Observe real changes and compare whether an acknowledgment adds value"
}
```

Priority is test_now/watch/drop; all text nonempty; >=1 support reference and >=1
risk. `test_now` requires at least one source reference, but even real statements
are insufficient to establish demand. The host chooses and explains priorities;
the CLI does not compute a pseudo-scientific score. Mixed support must remain
clearly distinguished in the prose. Lists may be empty or omitted.

## Audit and coverage

`audit DIR` reports stored evidence coverage and run status. `audit DIR --report`
first validates the draft and restricts evidence diagnostics to selected runs and
interviews, while retaining stored totals for context. Coverage includes platform,
access depth and discussion group counts, not unique customers or market share.
Warnings cover duplicate canonical URLs, normalized duplicate excerpts and partial
runs. The JSON is diagnostic; no truth/quality score and no automatic deletion.

Both `stored` and `selected` include `citable_sources` (full/excerpt records),
`citable_material_families` (their distinct group IDs), `citable_social_families`
(those groups with a full/excerpt post, comment or review), and `source_types`
(all records by type). The legacy `discussion_families` counts **all** material
groups, including official documents and unavailable leads. Social counts depend
on supplied classifications/grouping and can include promotional posts; they are
not verified buyers. `provided` feedback exports remain material, not public social
threads, and need their sampling unit described by the researcher.

Canonical URL comparison normalizes scheme/hostname/default ports and query order,
removes utm_* / fbclid / gclid tracking parameters, and preserves meaningful query
values, paths and fragments. Queries with repeated semantic keys retain their
original order because first/last-value interpretation can change the resource. Similarity beyond these rules requires host review.

## Rendering and recovery

Render validates first, freezes a coherent study + report snapshot, and creates a
new reports/NNN directory containing report.md + evidence.md and/or report.html +
evidence.html, study.json and report.json. Never overwrite previous reports. If interrupted during rendering,
no final report directory should appear; intermediate study records remain usable.
Hold the study lock during snapshot/render commit to prevent races.

The main report leads with conclusions, findings, counterevidence and next steps,
plus a brief question/module-coverage/status statement and evidence limitations.
Only reports containing interviews carry a simulation notice. Findings distinguish
source statements, inference, simulation and mixed reasoning. Optional comparison
and opportunity tables summarize decisions. Detailed methods, queries, source
metadata/URLs/context/excerpts, role cards and complete transcripts appear only in
the evidence companion. Main-report citations link to generated relative paths
`evidence.md#...` or `evidence.html#...` pointing to exact turn anchors. Evidence
persona links are internal. Do not display internal revision/recipe IDs in the main
report. All user strings are escaped for both HTML and Markdown.
HTML is self-contained with inline CSS and no external assets/scripts. Citation
links use generated file paths and anchor IDs. Evidence appendices also contain
validated, escaped source URLs. Display language follows brief.language when a
brief exists, otherwise recipe.language for
built-in labels (zh* Chinese, otherwise English); content is supplied by the Agent.
Reports are local; render never uploads, publishes, or runs code from input.

## Verification targets

CLI subprocess E2E; idempotency; all-or-nothing failed batch; invalid enum/type,
unknown fields and missing refs; partial checkpoints; incorrect completeness;
stale revision; safe HTML and Markdown; immutable snapshots; install idempotency
and conflict; wheel includes skill; run outside source checkout. Test real behavior,
not specific prose wording. Runtime standard library only, Python >=3.11.

## Render result paths

`render` returns the absolute numbered export `directory` plus an `artifacts`
object mapping `report_md`, `report_html`, `evidence_md`, and `evidence_html` to
absolute file paths. Only the requested formats are present. These paths refer to
the published snapshot, not a temporary directory. Use them directly for local
file links; keep relative links inside the generated report/evidence pair unchanged.


## Demand discovery additions (v0.4)

Existing schema_version=1 remains compatible. `needs` is an optional study/batch
collection. `source.parent_source_id` is optional: it must identify another saved
source in the same group, with no parent cycles. It records ancestry, not guaranteed
parent reading; preserve access/limitations. Do not invent a parent or comment URL.

`product-idea-research pool DIR [--report REPORT.json]` returns need cards, clusters,
source-family counts and dispositions. Without --report all stored cards are shown,
including historical corrections; with --report only explicit `need_ids` are shown.
With `--review`, the result additionally contains `claim_review`: each selected
card's claims with basis and exact cited excerpt text, locator and source URL;
counterevidence is expanded the same way. Unknown claims have no evidence. This
read-only join helps semantic review; it does not certify entailment or alter
saved records. Without the flag, the output is unchanged.

A need has exactly these fields:

```json
{
  "id": "need-1", "run_id": "social-1", "cluster": "subtitle-handoff",
  "disposition": "candidate", "summary": "Deliver approved subtitles after a recut",
  "claims": {
    "actor": {"text": "Editor", "basis": "stated", "support": [{"source_id": "s1", "excerpt_id": "e1"}]},
    "trigger": {"text": "Unknown", "basis": "unknown", "support": []},
    "outcome": {"text": "Aligned subtitle delivery", "basis": "inferred", "support": [{"source_id": "s1", "excerpt_id": "e1"}]},
    "workaround": {"text": "Unknown", "basis": "unknown", "support": []},
    "friction": {"text": "Unknown", "basis": "unknown", "support": []},
    "frequency": {"text": "Unknown", "basis": "unknown", "support": []},
    "payment": {"text": "Unknown", "basis": "unknown", "support": []}
  },
  "counterevidence": [], "limitations": ["Single self-report; example schema only"]
}
```

`run_id` must select an existing social run. `cluster` is nonempty text, not an
algorithmic classification. Disposition is candidate/resolved/promotion/adjacent/unclear.
Each of the seven claims requires text, basis and support. Stated/inferred requires
at least one eligible full/excerpt reference in that run. Unknown requires no support.
At least one claim must be source-backed. Counterevidence uses the same source
reference format (possibly empty). Limitations requires at least one item. Synthetic
interviews never support need fields. Structure cannot verify whether the text is true.

Reports may specify `need_ids` (unique IDs of needs belonging to selected runs).
Opportunity cards may specify `need_ids`, which must be a subset of the report's
selection. Corrections use new IDs; select current cards to avoid counting history.
With nonempty need_ids, render exports needs.json, needs.csv, needs.md and/or needs.html
alongside existing outputs. CSV values beginning with formula markers receive an
apostrophe; JSON retains original text. Share the whole directory for working links.
