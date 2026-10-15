# Modular research, conclusions first

Research Workbench helps a coding agent answer a question and deliver an actionable
report. Users choose the work: start from an idea, a competitor, public discussions,
provided materials or a user-defined interview method. Run one module or combine
several; never invent unperformed research to fill report sections.

| Module | Contribution | v0.2 behavior |
|---|---|---|
| Social research | Tasks, friction, workarounds, satisfaction, buying signals | Host collects public/supplied material; preserves exact excerpts and discussion context |
| Competitor research | Existing tools, indirect/manual alternatives, constraints | Dated source-backed comparisons; claims and unknowns distinguished |
| Simulated interviews | Assumptions, objections and conditional preferences | User-defined method and synthetic roles; generated answers remain hypothetical |
| Synthesis | Decision, disagreement, implications and next test | One main report from selected runs; linked evidence companion |

Supplied-material analysis uses the same source ledger and relevant research module;
it does not require browsing. A later module can extend saved work. Report-only
requests reuse it. Shared persona libraries and dedicated bulk platform adapters
remain outside v0.2.

## Division of responsibility

The skill directs research and reasoning using available host tools. The CLI does
not browse or run a model: it stores immutable evidence, validates exact references,
audits coverage/duplicates and creates frozen exports. This makes the workflow
portable without pretending every host has the same social-platform access.

The main report answers the question; detailed methods, source excerpts, role cards
and transcripts belong in the evidence companion. External statements, researcher
inference and simulation retain different meanings in a combined report.

## Atypica as a reference

Atypica's orchestration of research methods, personas and interviews informed the
design. Earlier hands-on evaluation exercised its research flow; final report
generation did not complete, so we do not claim to reproduce an inspected final
layout or its proprietary persona data.

This project's target is a stronger fit for coding-agent users who want explicit
module selection, inspectable local evidence, resumable files and reproducible
exports. Those are testable workflow properties, not a claim of superior prediction
accuracy, research validity or platform data coverage. See the evaluation record
for measured outcomes and remaining gaps.
