# Product Idea Research

**Find product needs in real posts and comments, then decide what is worth testing.**

A shared skill for **Codex and Claude Code**, with a small local Python CLI. Run
social research, competitor research or simulated interviews independently—or
combine them into one conclusion-first report. Start with an idea, a competitor,
an audience with no idea yet, links, exported feedback or a research method. Continue a saved study without
repeating completed work.

The agent uses its available browsing and model tools. The CLI preserves evidence,
checks exact citations, flags duplicates and exports Markdown plus standalone HTML.
No separate model API key, Atypica subscription, server or persona database required.
Your usual coding-agent usage still applies.

[中文](README.zh-CN.md) · [Data contract](docs/contract.md) ·
[Evaluation record](evals/README.md) · [Product scope](docs/product-direction.md)

## What you can ask

| Request | Result |
|---|---|
| “Find needs in these communities and their comments; no idea yet, no interviews.” | A sourced need pool, task clusters, rejected signals and a product shortlist |
| “Compare these products for this workflow.” | Sourced comparison, plan/price conditions, unknowns and task-specific recommendation |
| “Use my method to synthesize two roles and interview them. No browsing.” | Hypothetical objections, trade-offs and real-world questions to test |
| “Combine social signals, alternatives and a concept stress test.” | One report separating external statements, inference and simulation |
| “Use this feedback export offline.” | Analysis from supplied material with local provenance |
| “Add a competitor refresh to this study” / “Just update the report.” | New immutable iteration or synthesis using existing evidence |

Research is general across work and everyday life. A module is a choice, not a
mandatory stage. Explicit counts, methods, network restrictions and exclusions
are respected. A blocked requested channel remains a documented gap.

Previously **Research Workbench**. Existing users: follow the [rename migration](docs/installation.md#rename-from-research-workbench-v02-and-earlier) before installing; the old CLI remains a compatibility alias.

## Install

Requires Python 3.11+, Git, and Codex or Claude Code with terminal/file access.
Live research also needs the host's available search/browser tools or supplied
materials; this package does not provide proprietary social-platform access.

```bash
git clone https://github.com/YichenBC/product-idea-research.git
cd product-idea-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .

# Choose either or both; existing differing skills are never overwritten.
product-idea-research install --target codex --scope user
product-idea-research install --target claude --scope user
```

On Windows activate with `.venv\Scripts\Activate.ps1`. Keep the environment active
when launching your agent, or use `pipx install .` / `uv tool install .`. No PyPI
publication is required. Restart a running agent if it has not discovered the skill.
For project-only installation add `--scope project --directory /path/to/project`
instead of `--scope user`. Codex receives `.agents/skills/product-idea-research/`;
Claude Code receives `.claude/skills/product-idea-research/`. Both use the same package.
See [updates/uninstall](docs/installation.md).

## Use it

In Codex invoke `$product-idea-research`; in Claude Code invoke `/product-idea-research`.
For example:

> Research whether a small Web product could help video teams review translated
> subtitles. Look at public discussions and competing tools, include reasons the
> existing workflow is sufficient, then stress-test the concept with two simulated
> roles. Produce one Chinese report with a narrow opportunity and the next real test.

Or run a single module:

> Only compare the tools I linked for a two-person team. Use official docs and
> pricing, explain unknowns, and don't generate personas or conduct interviews.

Or offline:

> Analyze this exported feedback without browsing. Keep contradictory statements.
> Do not fabricate missing context; give me a report and a next validation step.

## Live examples

[Small-language AI video](examples/small-language-video/README.md): 25 real social/community families, seven software/platform alternatives, human-service counterexamples and a Chinese opportunity report. Includes disclosed access gaps and [evaluation-driven improvements](evals/README.md).

[Subtitle research](examples/subtitle-research/README.md): [combined report](examples/subtitle-research/combined/report.md), [social only](examples/subtitle-research/social/report.md), [competitors only](examples/subtitle-research/competitor/report.md). Includes evidence, review corrections and offline replay inputs.

## What gets saved

```text
studies/topic/
  research.json          # brief, sources, runs, optional needs/personas/interviews
  ...draft JSON files... # generated by your agent
  reports/001/
    report.md
    report.html          # conclusions; no scripts or remote assets
    evidence.md
    evidence.html        # source excerpts, methods, role cards and complete Q&A
    study.json           # frozen evidence snapshot
    report.json          # frozen report draft
    needs.md / .html      # optional: selected demand cards with field-level citations
    needs.json / .csv     # optional: reusable pool and flat table
```

For demand discovery, each card records actor, trigger, outcome, workaround, friction,
frequency and payment as **stated / inferred / unknown**. Keep solved cases and
promotion in the pool; a complaint is not automatically a product opportunity.

The main report presents conclusions, meaningful disagreement, optional competitor
and opportunity tables, next actions and limits. Exact citations open the evidence
companion. External statements, interpretation and simulation are distinguished;
simulated answers never become proof of real demand. Share the entire export folder
to preserve links. Re-rendering creates a new numbered snapshot.

## CLI

| Command | Purpose |
|---|---|
| `init` | Create a local study without overwriting one |
| `ingest` | Atomically save immutable JSON records |
| `status` | Show stored module/source/interview coverage |
| `check` | Validate types, references, selected evidence and completeness |
| `audit` | Inspect access depth, discussion groups and duplicate evidence |
| `pool` | Inspect selected needs; `--review` joins each claim to its exact cited excerpts |
| `render` | Export report, evidence, selected need pool and frozen JSON |
| `install` | Install the shared skill for either host |

`audit` is a coverage diagnostic, not a truth score. A citation to a search snippet
is rejected; multiple comments from a thread are not counted as independent people.
The host must still verify that each excerpt supports its interpretation.

## Replay a fixture without a model

This replays the original hand-authored simulation example:

```bash
product-idea-research init studies/demo --title "Scheduling concept"
product-idea-research ingest studies/demo --file examples/scheduling/batch.json
product-idea-research check studies/demo --report examples/scheduling/report-draft.json
product-idea-research render studies/demo --report examples/scheduling/report-draft.json
```

[Scheduling report](examples/scheduling/report.md) ·
[Prior live Codex simulation](examples/household/report.md).
The CLI does not generate research; new content comes from the skill in your agent.

## Boundaries

- No guaranteed access to Reddit, X, Xiaohongshu or any login-gated platform. The
  agent discovers available MCP/browser routes and tests post and comment access
  separately. It records partial access; supplied material works offline.
- Public posts remain self-report; vendor pages remain vendor claims. Neither
  source count nor role-play estimates willingness to pay or market prevalence.
- No automatic outreach, publication, private-data upload or paid product trials.
- Shared persona libraries, dedicated platform crawlers and a hosted research UI
  are not included. Role attributes remain assumed/unknown.
- `complete` means declared research coverage, not validated demand. Structural
  validation cannot prove truth, source independence or semantic entailment.
- Storage/rendering are local. Prompts and research still pass through your host's
  configured model/tools; local storage does not imply offline model inference.

## Develop

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

Runtime is Python standard library only. The canonical skill is packaged from
`src/product_idea_research/skill/`; keep its data-contract reference identical to
`docs/contract.md`. See [contributing](CONTRIBUTING.md) and [eval cases](evals/cases.md).
MIT licensed. Fictional fixtures and any live-source examples are labeled separately.

## Latest demand-discovery evaluation

[Real posts, comments and product opportunities](examples/demand-discovery/README.md):
31 selected need cards, real Reddit/X/LinkedIn/Xiaohongshu material, independent
semantic review, preserved first output and reproducible corrections.
[Evaluation](evals/README.md) · [Atypica comparison and boundaries](docs/atypica-comparison.md).
