# Combined model acceptance — fictional materials

This is actual Codex output using the installed **Product Idea Research v0.3.0**
skill and CLI on 2026-10-15. All supplied discussions and products are deliberately
fictional. This demonstrates behavior, not market research or demand validation.

[Chinese report](report.md) · [HTML](report.html) · [Evidence and full Q&A](evidence.md)

The fresh run combined social research, competitor research and two synthetic
roles with three Q&A turns each. It retained the original author's clarification,
optional review rather than mandatory approval, existing version-management
capabilities and sufficient manual alternatives. All eight saved excerpts match
the supplied material verbatim. The main report recommends further investigation
before building, without inferring real willingness to pay.

[Prompt](prompt.txt) · [Materials](materials.txt) · [Frozen study](study.json) ·
[Report draft](report.json)

To replay rendering, create a new study directory, copy `study.json` there as
`research.json`, and run `product-idea-research check DIR --report report.json`
followed by `product-idea-research render DIR --report report.json` using this
example's draft path. This does not rerun a model or browse websites. To repeat the
model evaluation, install the skill in a fresh workspace, copy materials.txt and
use prompt.txt; stochastic output may differ.

During the original run, a generated shell/Python draft-writing command failed
with a UTF-8 error. The agent then attempted validation before the draft existed,
received the missing-file error, repaired the write and completed validation and
rendering. The data ledger was not lost. The final answer used relative file links;
this prompted the absolute artifact-path improvement and separate delivery regression
documented in the [v0.3 acceptance record](../../evals/README.md). The report contents
were independently reviewed without a substantive blocker.
