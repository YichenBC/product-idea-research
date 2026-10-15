# Demand discovery development checkpoint

Status: implementation reviewed; second live forward evaluation interrupted by host account usage limit. This is not a release acceptance or a superiority claim. Last published version remains v0.3.1.

## Completed

- Added optional immutable demand cards with seven field-level stated/inferred/unknown claims, exact source references, disposition and task cluster.
- Added source parent references, cycle/family validation, explicit report/opportunity need selection, pool command and HTML/Markdown/JSON/CSV exports.
- Canonical X status identity; pool merges supplied groups connected by duplicate canonical URLs and retains reported_families.
- Added discovery/access skill references and routing. Browser fallback actually read X originals/replies and a LinkedIn post with three comments; no X or LinkedIn MCP integration was installed.
- Independent Python review approved after fixing family double-counting. Malformed input and export-failure review found no further actionable defects.
- Independent baseline completed: 13 Reddit original posts, 65 individually retained comments, three task domains, exact source URLs and read manifest. Structural checks passed. Baseline used initial skill instructions; code was being edited concurrently, so this is not a pinned-binary benchmark.
- Attempted to resume the prior Atypica study through its documented API. Response: saved_no_ai / quota_exceeded. Existing report generation remains failed. Do not treat unavailable quota as a quality win.

## Local evaluation artifacts (ignored; not publication-ready)

- `.eval-runs/discovery-baseline/`: completed frozen baseline, evidence-batch.json, runs-batch.json, provenance.json, read-manifest.json, execution-notes.md, study/reports/001.
- `.eval-runs/discovery-forward/`: incomplete study and raw search/page returns only. Agent reported eight new post bodies and approximately eighty visible comments before interruption; those are NOT audited completion counts. No finished new-source batch, demand cards or final report yet.
- `.eval-runs/discovery-comparison/browser-sources.json`: six parent-read X/LinkedIn sources and one partial run, with short excerpts and access boundaries. No full-thread completeness claim.
- `.eval-runs/discovery-comparison/atypica-scouts.json`: historical API scouting outputs for scoped source review. Private API state and tokens must not be published.

## Resume without redoing completed work

1. Read frozen baseline and raw forward materials; verify actual body/comment contents, source locators and duplicate identities. Complete at least twelve new posts and seventy relevant comments in the forward study, saving batches and explicit provenance.
2. Run the revised skill independently when delegation is available again. Ingest browser-sources.json as parent-read evidence, not as the evaluator's own browser activity. Produce field-level needs and a selected report through pool/check/audit/render.
3. Review top conclusions and rejected signals against original sources; check source-to-task fit, dates, promotion/resolution, buyer versus vendor roles and whether payments/frequencies are actually supported. Fix observed errors, preserve initial outputs, rerun focused cases.
4. Build a transparent capability comparison against Atypica's documented Product R&D workflow and historical actual outputs. Its new execution is quota-blocked. Historical known-error regression is not a blind or same-budget accuracy benchmark. Record untested platform/persona/host features explicitly.
5. Update both READMEs, data-contract consistency, version, evaluation record and reusable public example only after acceptance. Build and smoke-test installations for Codex and Claude Code; do not equate installation with actual Claude model behavior.
6. Publish reviewed, verified changes to GitHub under existing user authorization. Keep unrelated main-checkout household/report.html edit untouched. Do not publish raw browsing captures, credentials, unrelated profile information or private API state.

The user's target remains real demand discovery, not merely report generation. Goal is unfinished; account usage limit must not be represented as achievement or as user-requested pause.

## Resume result — 2026-10-16

The interrupted forward run finished: 12 new posts / 78 retained comments, 27 cards.
All 106 non-unknown fields received independent semantic review; citation corrections
were appended and the original report stayed frozen. The final main example adds
Xiaohongshu holdout and Subtitle Edit official evidence: 31 selected cards / 187 sources.
A fresh independent request used the revised skill on 4 new posts / 24 comments and
6 official pages, producing 10 selected cards after self-review with `pool --review`.
See [current evaluation](../../evals/README.md) and
[final report](../../examples/demand-discovery/README.md) for counts, replays and limits.
The initial “unfinished” status above describes the saved checkpoint, not current output.
