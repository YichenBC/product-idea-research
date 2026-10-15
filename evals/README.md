# v0.3 acceptance record

Date: **2026-10-15 (Asia/Shanghai)**. The project is now **Product Idea Research**.
This record separates fresh renamed-package tests from earlier research evaluations.
[Prior v0.2 results and iterations](v0.2.md) · [v0.1/v0.1.1 history](v0.1.md).

## Fresh checks

| Check | Observed result | Boundary |
|---|---|---|
| Automated tests | 50 tests and 10 subtests passed locally | GitHub CI separately checks Linux/macOS/Windows and Python 3.11/3.13 |
| Fresh renamed wheel | New CLI and legacy CLI both report 0.3.0; new skill installs for both hosts | Installation does not prove host model behavior |
| Actual v0.2 → v0.3 upgrade | Uninstalled old package, installed new wheel; both commands checked and rendered an old study without changing its ledger | Follow migration order to avoid shared executable ownership |
| Existing customized skills | Legacy folders preserved byte-for-byte; installer reports migration warnings | Does not silently remove or merge user customizations |
| Fresh Codex combined study | Two selected modules, seven source records in four material groups, two roles × three Q&A turns, six findings and one suggested next experiment | Fictional supplied material; no live browsing |
| Evidence content review | Eight excerpts match supplied text; independent review found no substantive blockers | One bounded run, not a research-quality benchmark |
| Report delivery regression | Fresh Codex report-only run returned four existing absolute file links; ledger and all older exports unchanged | Same saved draft, no new research; report/evidence content byte-identical |
| Claude Code | Renamed skill installation passed; auth reports loggedIn=false | Actual model workflow remains unverified |

The actual model run used Codex CLI `0.162.0-alpha.17.2` with its configured default
model, a fresh installed wheel and workspace, and the renamed installed skill.
No model override, research-service key, new source collection or outreach was used.
[Inspect the generated report, material and prompt](../examples/combined-acceptance/README.md).

## Changes driven by this round

- **Actionable report links:** the actual Codex final answer shortened output links
  to relative paths despite the existing skill instruction. The CLI now returns
  exact absolute paths in `render.artifacts`, and the skill uses those values for
  delivery. Regression tests cover Markdown/HTML selection, Chinese/spaced paths,
  actual files and final publication rather than temporary locations.
- **Migration preservation:** new package/module/skill names are canonical; the old
  command and `python -m research_workbench` forward to the same implementation.
  The installer warns about legacy skills rather than overwriting customizations.
- **CI artifact selection:** independent review found that `--find-links` alone could
  choose a published package. CI now uses `--no-index` to test its local wheel.

The combined model run also encountered a draft-writing UTF-8 error and attempted
validation while the draft was absent. It repaired the write and completed without
parent intervention; this was not a first-attempt-perfect run. No general skill
rule was added for that single recovered execution error.

## Earlier evaluations already changed the product

The v0.2 live study and actual Codex cases exposed missed adjacent competitor
features, misread optional review, overlooked original-author follow-ups and dissent,
and ambiguous “three rounds” counts. The skill was refined and affected cases
were rerun before that release. The fresh v0.3 combined case again preserved those
distinctions and produced exactly two interviews of three Q&A turns each.

The live study remains available separately: [real public-source subtitle research](../examples/subtitle-research/README.md).
It covered eight accessible discussion families and three official alternatives;
it is not being relabeled as a new v0.3 live collection.

## Limits

No live X/Xiaohongshu access or real willingness to pay was established. Synthetic
roles are not customers. Claude's actual model behavior remains unverified. There
is no paired accuracy/quality benchmark proving superiority to Atypica. See the
[capability comparison](../docs/atypica-comparison.md) and [migration instructions](../docs/installation.md).
