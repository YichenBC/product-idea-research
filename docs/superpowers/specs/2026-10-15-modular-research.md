# Modular research, v0.2

## Authorized outcome

Social research and competitor research run independently or together with simulated interviews. A user may enter with an idea, question, competitor, links, exported material, or an existing study. One conclusion-first report combines only the work requested/performed. Preserve Codex and Claude Code support, local-first storage and open-source publishing. Persona libraries and platform-specific bulk crawlers are separate future work.

## Architecture and alternatives

Keep host-agent research plus a deterministic Python standard-library CLI. Expanding the skill alone would leave mixed evidence unverifiable; adding a hosted autonomous crawler/model runtime would add credentials and platform maintenance without solving evidence quality. Extend the existing ledger, validation, auditing and rendering instead. Host browsing/search/provided exports supply material; no Atypica API dependency. Source text is untrusted data, not instructions.

## User-visible modules

- Social: scope/search plan; posts AND relevant comments/context; task/trigger/current workaround; satisfaction/rejection; buying signals with their exact meaning; cluster and rank actionable opportunities without pretending the sample is representative.
- Competitor: direct, indirect, manual and do-nothing alternatives; comparable dimensions; official claims versus firsthand feedback versus inspected behavior; pricing date/currency/unit/caps when known; missing information explicit.
- Interviews: existing user-method/persona/interview behavior; optionally informed by external material, but all generated responses remain synthetic and persona attributes assumed/unknown for this release.
- Synthesis: answer the question, resolve or preserve disagreement, compare alternatives, identify testable opportunities and real-world next actions. Single-module requests do not trigger other modules. Report-only does not browse or regenerate.

## Backward-compatible data additions

Keep schema_version 1, with optional `brief`, `sources`, `runs` fields. Missing new fields mean no such records; do not rewrite an old study merely by reading it. New init includes those empty fields. Existing recipe/personas/interviews and old report drafts still work unchanged. Each entity ID is globally unique. Brief and all new records are immutable, appended atomically under the existing lock. Corrections/new research iterations use new IDs and selected runs; old snapshots remain frozen.

`brief`: {id, question, language, constraints: string[]}. Immutable shared research question; a run has its own objective. No fixed module list: later modules can extend a study. A revised overall question uses a new study.

`source`: {id, title, url: string|null, platform, source_type, published_at: ISO date|null, accessed_at: ISO date, language, access, group_id, context, excerpts: [{id, text, locator}], limitations: string[]}.

- source_type enum: post, comment, review, official, article, provided.
- access enum: full, excerpt, snippet, unavailable. Full/excerpt requires >=1 excerpt. Snippet permits excerpts but cannot support findings. Unavailable requires zero excerpts and >=1 limitation. All other fields nonempty text except nullable URL/date and possibly empty limitations.
- URL is mandatory except for provided material. Allow only http/https, host present, no userinfo, whitespace/control characters or backslash; reject unsafe schemes. Never fetch URLs in CLI. Source excerpts are immutable with unique IDs within their source. A citation pins source_id + excerpt_id.
- group_id identifies a discussion/material family; comments/reposts from one discussion do not become independent customers. context explains parent discussion/read scope, not fabricated author biography. Dates are valid YYYY-MM-DD; not inferred from search crawl dates. Short quotations only; no bulk copying protected articles.

`run`: {id, module: social|competitor, status: partial|complete, objective, method, queries: string[], source_ids: string[], limitations: string[]}.

A run requires a brief, references stored sources (unique IDs). Complete requires >=1 source with full/excerpt access. Partial requires >=1 limitation and may have no sources (blocked search). Both are frozen snapshots. Completion means stated research scope covered, never product demand proven. Sources may be saved before runs for checkpointing.

## Report changes

Existing required fields stay. `interview_ids` can be empty when optional `run_ids` selects >=1 run; missing run_ids means []. Only selected runs' sources can be cited. Report complete requires all selected runs complete, plus existing planned persona coverage if interviews selected; unused stored recipe/personas do not force simulation. Partial may have no findings only when no eligible source evidence or interviews were selected (all collection blocked/unusable); complete requires >=1 finding. At least one run or interview must be selected.

References are strictly either {interview_id, turn} or {source_id, excerpt_id}. Source refs must select full/excerpt sources. Finding kind enum: simulation (interview support only), source (source support only), inference (source support only), mixed (both types in support). Counterevidence may use either eligible type but never upgrades support. Each finding retains >=1 support and >=1 limitation. Mixed findings must identify synthetic parts in prose. Structural validation cannot prove entailment.

Optional `comparisons`: [{alternative, category: direct|indirect|manual|do_nothing, dimension, assessment, support: source_refs[], limitations: string[]}]. Nonempty support and limitations; only sourced claims, no simulated proof of a competitor feature. Optional `opportunities`: [{title, audience, problem, alternative, proposal, priority: test_now|watch|drop, rationale, support: refs[], risks: string[], validation}]. Nonempty support and risks; source support required for test_now (not sufficient to establish demand). Ranking is a reasoned decision, not a fabricated score/probability.

## CLI and report behavior

Existing commands retained. Add `audit DIR [--report FILE]` returning structured coverage and warnings (not a truth score): source access/platform/group counts, duplicate canonical URLs, duplicate normalized excerpts, incomplete runs, selected versus stored records. Canonical URLs drop only known tracking keys (utm_*, fbclid, gclid), normalize scheme/host/default port and query ordering; preserve fragments, semantic query parameters and paths. Do not silently merge evidence or count unique customers.

Status includes sources/runs/module coverage. Check still validates; audit explains evidence gaps. Source-only report never says all research is synthetic. Main report: summary, selected module coverage, findings with source/simulation classification and exact links, optional comparison and opportunity tables, next steps and limitations. No process dump. Evidence companion: brief, run methods/queries/limitations, source metadata/URL/context/excerpts, selected role cards and complete simulated transcripts. All citations use generated local anchors, original source URLs appear only as validated escaped links in appendix. Old pure simulation rendering stays compatible. All exports atomically include frozen study/report JSON, MD/HTML documents and companions.

## Acceptance

1. Legacy tests and examples continue to work.
2. Social only and competitor only run with no recipe/personas/interviews; combination shares selected source evidence and simulation in one report.
3. Malformed/unsafe sources, dangling/unselected citations, snippet-as-evidence, synthetic-as-observation, incomplete-as-complete, duplicate IDs fail atomically.
4. Duplicate URL variants/excerpts and same-thread groups remain visible without inflating independent demand claims.
5. Offline/provided materials and completely blocked collection yield honest partial reports. Report-only and resume avoid unnecessary generation.
6. HTML/Markdown remain escaped, source links safe, every citation resolves, failed rendering publishes nothing, past snapshots stay unchanged.
7. Realistic live research plus independent skill evaluation covers standalone/combined/no-network/continuation and samples entailment, disconfirmation, provenance and actionability.
8. Publish only after review, local tests, wheel/skill installation checks and cross-platform CI. Record actual host validation and limitations; no untested superiority claims over Atypica.
