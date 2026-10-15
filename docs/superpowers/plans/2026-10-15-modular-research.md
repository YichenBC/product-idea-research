# Modular Research Implementation Plan

> **For agentic workers:** Use subagent-driven-development for implementation and independent review. User authorized continued implementation and publication.

**Goal:** Ship independently usable social and competitor research and unified evidence-backed reports with optional simulated interviews.

**Architecture:** Extend immutable schema_version 1 with brief/sources/runs and exact excerpt citations. Skill orchestrates host tools; CLI validates, audits, stores and renders. Preserve existing simulation behavior and historical snapshots.

**Tech Stack:** Python >=3.11, standard library runtime; pytest/build dev; portable Markdown skill.

## Task 1 — Ledger, validation and audit

Files: validation.py, new research_validation.py and audit.py if needed, store.py, cli.py; tests/test_research.py. Keep small helper boundaries rather than one huge validator. Contract is fully specified in ../specs/2026-10-15-modular-research.md.

- [x] Add failing CLI tests for social-only source ingestion and report validation, legacy loading, combination, partial blocked run, mixed citation type rules, canonical duplicates, invalid URL/date/access/ref, atomic rejection and complete checks.
- [x] Run `uv run python -m pytest tests/test_research.py -q`; verify expected failures from missing new behavior.
- [x] Implement additive records, immutable merge and validators; add audit command and coverage status. Import shared validators without circular module initialization errors. No network code.
- [x] Run new tests and existing suite. Audit must distinguish selected sources from archived records, and never interpret duplicates as independent people.
- [x] Independent spec review followed by Python quality/security review; fix findings before renderer integration.

## Task 2 — Unified report

Files: render.py (split helper file if needed), tests/test_research_render.py, tests/test_recovery.py if additional failure paths.

- [x] Test social-only and competitor-only render, mixed references, no false synthetic banner, exact excerpt links, external URL escaping, MD+HTML/single formats, optional comparison/opportunity tables and partial zero-finding output.
- [x] Implement selected runs/sources, conclusion-first overview, finding classification, comparison/opportunity presentation and source appendix. Preserve pure simulation tests and atomic write behavior.
- [x] Verify every emitted local anchor resolves; reject active content via data validators/escaping. Test frozen snapshot after source/run corrections.
- [x] Independent spec and Python reviews.

## Task 3 — Skill and documentation

Files: skill/SKILL.md, references/social.md, competitors.md, reporting.md, method.md, data-contract.md; docs/contract.md, README.md, README.zh-CN.md, docs/product-direction.md, docs/installation.md as needed.

- [x] Route explicit standalone, combined, supplied-material, resume and report-only requests. No mandatory all-module funnel. Honor user's research budget/volume and permissions.
- [x] Define useful queries and sampling, thread/comment context, promotion/selection bias, alternative satisfaction, payer signals, grouped dedup, platform restrictions and offline fallback. Source evidence means retrieved content, not a verified world fact.
- [x] Define comparable competitor dimensions, current dated pricing constraints, primary source claims vs real observations, unknown cells and manual/do-nothing alternatives.
- [x] Show minimal valid JSON examples, exact CLI commands, audit and synthesis rules. Update install/version docs. Keep canonical contract and packaged copy identical.
- [x] Validate skill frontmatter and packaged files.

## Task 4 — Behavioral acceptance and release

Files: evals/*, examples/modular/*, version files, CI as needed.

- [x] Run live research on a concrete public topic using the new skill and record queries/access outcomes and excerpts. Save standalone reports and a combined report. Evaluate citations against actual accessed source content.
- [x] Independently forward-test no-network supplied materials, explicit single module, combined scope, resume/report-only and contradictory evidence. Fix demonstrated failures, rerun affected cases.
- [x] Produce readable reproducible public examples without keys/private data/full copyrighted article copies. Publish honest capability comparison with Atypica based on prior actual evaluation; do not claim unmeasured predictive superiority.
- [x] Run `uv run python -m pytest -q`, `uv build`, install wheel outside checkout and install skill for both host directories. Verify git diff and source package.
- [ ] Commit/merge/push, wait for Linux/macOS/Windows CI, release v0.2.0 with artifacts/checksums and actual evaluation limits. No additional permission required under existing user authorization.
