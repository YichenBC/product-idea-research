# v0.4.0: real demand discovery, reviewed and replayable

Date: **2026-10-16 (Asia/Shanghai)**.
[Protocol](discovery-protocol.md) · [v0.3.1](v0.3.1.md) · [v0.3](v0.3.md) ·
[v0.2](v0.2.md) · [v0.1](v0.1.md).

This round tests finding product needs in original posts and comments, not merely
formatting a report. The protocol was written before the resumed forward report,
after some collection already existed; it was not fully preregistered.

## Actual runs

| Run | Input and scope | Observable outcome |
|---|---|---|
| Previous-instruction baseline | 13 real Reddit posts / 65 comments | 12 prose demand items and 6 opportunities; no structured need ledger. CLI binary was not pinned while parent development continued, so this is not a controlled old-versus-new accuracy experiment |
| Independent forward run | Same raw evidence, no baseline report; 12 new originals / 78 retained comments, with permanent links; parent X/LinkedIn sources explicitly attributed | 27 cards / 11 clusters before shortlist; 13 candidate, 5 resolved, 4 promotion, 3 adjacent, 2 unclear; five opportunities, zero forced interviews |
| Independent Xiaohongshu holdout | Parent-read 2 posts / 27 comments; evaluator received 7 source records / 9 short excerpts, no prior conclusions, no browsing | Four cards: candidate, resolved, alternative, unclear recommendation. Conditional payment remained conditional; AI-written recap was not treated as measured performance; no personas/interviews |
| Reviewed combined report | All above plus six accessible official pages, including a parent recheck of Subtitle Edit | 31 selected cards / 14 clusters; 187 selected source records. Two narrow delivery tests, observation and rejection cases; overall partial coverage retained |

The final main study has 188 stored sources including one unavailable page and
40 stored cards including nine superseded versions. The report selects only the
31 current cards and 187 accessible sources. Its 30 social-origin conversation
families include two supplied-material families: CLI's narrower direct social
counter correctly reports 28. Neither count means independent paying customers.

[Final Chinese report, need pool, manifests and replay](../examples/demand-discovery/README.md).
[Xiaohongshu holdout report](discovery-round2/xhs-holdout/report.md).
No private API state, full browser captures or credentials are published.

## Semantic review and observed iteration

An independent reviewer inspected **all 27 cards / 106 non-unknown fields**,
including all 10 payment fields, both frequency fields, all 14 noncandidate cards,
five opportunities, five findings, three comparisons and one additional payment
case in the report. This is purposive exhaustive review of those artifacts, not
an estimate of market-research accuracy.

It found **nine groups of citation gaps** affecting **12 need fields and one
comparison**, plus two wording/context improvements. Examples: a mobile-inventory
payment claim pointed to excerpt 1 while conditional payment was in excerpt 3;
a maker's $20 proposed price and free-copy incentive were in separate excerpts;
“Not really” required its parent question to carry meaning. No reviewed error
required reversing the two leading product directions, but unresolved citations
still blocked acceptance.

[First report input](discovery-round2/first-report.json) and
[first frozen study](discovery-round2/first-study.json) are preserved.
[Full review ledger](discovery-round2/semantic-review.json) lists the denominators
and exact fields. Nine revised cards were appended with new IDs, one comparison
was repaired, and duration wording was narrowed. Existing records were not rewritten.

| Observed failure or friction | Change | Verification |
|---|---|---|
| Valid references could point to the wrong chunk of a long source | New read-only `pool --review` joins each field to exact excerpt text/locator/URL; discovery instructions require reviewing shortlisted and payment/frequency fields | Non-first and cross-source same-ID tests; independent Python review; revised field audit |
| Historical claims can survive after correction | Append corrected need IDs and select them per report | Frozen 001 hash check; nine replacement cards; selected report excludes old versions |
| Search retrieval failed for a competitor homepage | Followed the official repository to its current documentation | Four official pages read; subtitles scoped to source-language timeline mapping instead of generic audio alignment |
| Large review output was truncated; a helper tried JSON-decoding `--version` | Document file-based batched review and the plain-text top-level flag exception | Fresh agent successfully used a saved compact view and corrected its helper |
| Reply recommendations and “would pay” can inflate demand | Existing context/disposition workflow exercised on a separate real Chinese holdout | Resolved case, free alternative and unknown trial result retained; no invented payment or usage frequency |

The quotation helper makes review practical; it is not a semantic classifier and
does not promise that future first drafts will have no errors. Tool tests alone
would have missed the first draft's mistakes.

## Comparison and host scope

The demonstrated result supports **core demand-discovery workflow coverage**
relative to Atypica's documented Scout/Product R&D operations. See the
[capability-by-capability comparison](../docs/atypica-comparison.md).
Atypica's authorized retry returned `saved_no_ai / quota_exceeded`, preventing a
fresh matched output. Historical known context errors are regression examples,
not evidence of a measured accuracy win or overall product parity.

Live model executions used the Codex host and its available web/browser tools.
Claude Code currently reports no authenticated session: installation compatibility
can be checked, but this release does not claim a completed Claude model execution.
Public-source access varies by host; no dedicated X/LinkedIn MCP was installed.

## Scope still unproven

Hundreds of independent needs, representative Chinese/small-language audiences,
complete comment trees, real customer interviews and paid pilots are not established.
Sources are self-reports or vendor claims, not verified customers or product trials.
Synthetic roles remain optional and cannot supply missing payment evidence.

## Fresh request after the change

A separate independent agent then used the updated skill on **four new original
posts, 24 comments and six official pages** about independent content services.
It did not receive prior conclusions. It completed discovery plus competitors,
selected ten cards, and generated no synthetic interviews.
[Read the report, first/final inputs and replay](discovery-round2/fresh/README.md).

Using `pool --review`, it independently removed unsupported “free” wording and
product names carried only by context, changed a mixed finding to inference, and
corrected an ideal weekly workflow that had been phrased as observed frequency.
Three revised cards were appended; the first and intermediate outputs stayed intact.
The final report distinguishes an experiment worth trying from two directions to
watch/drop. This is evidence that the review step works on a fresh request, not
proof that the tool eliminates first-draft mistakes.

Across the main and fresh studies there are 209 retained social-origin records
(including replies and provided excerpts) and 11 distinct accessible official pages.
One official page appears in both studies. The 31 main and 10 fresh selected cards
are not 41 independent customers, and overlapping task ideas are not additive markets.

## Engineering and artifact checks

- 61 tests and 10 subtests passed locally; Python review approved the demand-ledger
  implementation and the exact-excerpt review addition.
- Skill validation passed; the wheel/sdist built. A fresh Python 3.11 environment
  installed the final wheel and identical packaged skills into both host locations.
- First report, revised main report, Xiaohongshu holdout and fresh-task final report replayed from public
  inputs. Main and fresh report/evidence/need exports matched published files byte-for-byte,
  and replay left study data unchanged.
- Browser inspection confirmed readable Chinese report text and a functioning
  report-to-need-pool link. CLI citation checks and immutable snapshot checks passed.
- Publication files were checked for credential patterns and temporary access tokens;
  private raw captures/API state were excluded. This is a scoped check, not a security certification.

Final fresh-task review inspected all 46 non-unknown fields in ten selected cards,
five findings, seven comparisons and three opportunities. It independently checked
all 24 comment permalinks and reopened six official pages; no selection-changing
unsupported claim remained in the reviewed scope. One original post’s exact date
could not be independently reproduced; its earlier reader attribution remains a
limitation, not an accuracy win. [Detailed review](discovery-round2/fresh-review.md).
