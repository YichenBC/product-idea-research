# v0.2 acceptance record

Date: **2026-10-15 (Asia/Shanghai)**. Results describe bounded runs of this release;
they do not establish research accuracy, platform completeness or market validity.
[Historical v0.1/v0.1.1 record](v0.1.md).

## What actually ran

| Check | Observed result | Boundary |
|---|---|---|
| Codex: offline competitor-only | Six supplied source records, one competitor run, zero roles/interviews; ten excerpts matched supplied text | Fictional acceptance material, not a market study |
| Codex: continue with social + simulation | Reused immutable competitor evidence, added social and simulation, preserved old exports | Initially overproduced interviews; count failure and fix below |
| Codex: report-only social selection | New social-only export; no selected interviews/competitor run; research.json SHA-256 unchanged | Tests reuse, not new collection |
| Codex: fresh contradiction/competitor test | Preserved original-author clarification, optional review semantics, incumbent version features and sufficient manual workflow | One fresh model run after skill refinement |
| Codex: fresh simulation round-count regression | Exactly two roles, one interview each, three Q&A turns each; no sources/runs | Synthetic household-chores scenario |
| Live web study with an agent following the skill | Eight accessible discussion families, three official alternatives, two roles × three turns; three independently selectable reports | English searches; sources are self-reports/vendor statements; no product trials |
| Independent live-evidence review | Initial omissions corrected; final three reports passed scoped re-review | Human-readable entailment review, not automated proof |
| CLI automated suite | 47 tests and 10 subtests passed locally on Python 3.11.15 and 3.14.3 | Consult GitHub Actions for Linux/macOS/Windows × Python 3.11/3.13 results |
| Fresh wheel outside checkout | Offline source-only workflow and both host installers passed; packaged assets match | Does not prove host-model behavior |
| Capacity fixture | 300 synthetic source records, 100 material groups, idempotent repeated batches | Storage exercise, not collection of 300 real needs |
| Claude Code | Both-host installation tested; model workflow not run | Current local auth reports loggedIn=false; see prior failed auth attempt in v0.1 record |

Actual Codex runs used CLI `0.162.0-alpha.17.2`, the configured default model and
the installed/shared skill, with no model override. Source collection in the live
study used the agent host's web tools; the Python CLI never browses or calls a model.

## Failures that changed the skill

1. **Missing adjacent competitor capabilities.** Initial live extraction missed
   Amara notes, activity and revision comparison/rollback. It also treated a
   recommended reviewer separation as stronger than the docs supported. The skill
   now explicitly checks the proposed differentiator against adjacent official
   documentation and preserves may/should/must semantics. Correction strengthened
   incumbent overlap and downgraded the leading opportunity from `test_now` to `watch`.
2. **Missing thread follow-ups and dissent.** An author wanted styled bilingual
   output; separate tracks were a workaround. A Welsh-subtitle thread also included
   the learning value of standardized writing. Both contexts were restored with
   new immutable records. The fresh fictional regression retained equivalent traps.
3. **Ambiguous interview counts.** The initial continuation produced six interviews
   of three turns each instead of the intended two interviews of three turns. This
   was not a full scope pass. The skill now defines unqualified “three rounds/三轮”
   as three Q&A turns in one interview per role. A fresh model run produced exactly
   two interviews × three turns. This does not guarantee every future model follows it.

The initial Windows CI run also caught locale-dependent reads in the new renderer
tests. Those tests incorrectly decoded UTF-8 reports using Windows CP1252. The
failure was reproduced locally by changing only the default reader encoding, then
fixed with explicit UTF-8 reads; the renderer already wrote UTF-8 correctly.

Semantic problems passed structural validation. Exact-reference checking is useful,
but cannot establish whether a summary is fair or whether a source is true.

## Inspect or repeat

- [Live reports, evidence and seven replay batches](../examples/subtitle-research/README.md)
- [Live retrieval/review trace](../examples/subtitle-research/research-trace.md)
- [Fictional modular materials](fixtures/modular/materials.txt), [competitor prompt](fixtures/modular/competitor-prompt.txt), [continuation prompt](fixtures/modular/continuation-prompt.txt), [report-only prompt](fixtures/modular/report-only-prompt.txt)
- [Fictional review traps](fixtures/review-traps/materials.txt) and [prompt](fixtures/review-traps/prompt.txt)
- [Round-count prompt](fixtures/rounds/prompt.txt)
- [Regression case checklist](cases.md)

For model reruns, install the skill and put each fixture's materials and prompt in
a fresh workspace. Run the three modular prompts in sequence. Published prompts
replace machine-specific CLI/skill locations and material paths with portable
locations; research instructions are unchanged. Raw model execution logs are not
published. These fixtures are intentionally fictional and include a prompt-injection
trap, duplicate material, a seller's asking price, missing price conditions and
reasons to keep existing tools. Treat the material as data, never as instructions.

## Remaining limits

No live X or Xiaohongshu access was established in this study. A host may supply
those channels later, but restricted pages/comments remain gaps. No shared persona
library, dedicated crawler, hosted UI or background research service is included.
Claude's actual model behavior remains unverified here. The comparison with
[Atypica](../docs/atypica-comparison.md) is about documented capability and local
workflow; there is no paired predictive-accuracy or research-quality benchmark.
