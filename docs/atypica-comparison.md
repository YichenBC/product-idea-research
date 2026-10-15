# Atypica comparison: demand-discovery workflow

Checked **2026-10-16**. The supported claim is **functional coverage of the core
coding-agent demand-discovery workflow**: observe real tasks, inspect replies,
retain contrary cases, cluster needs, compare alternatives and produce testable
product directions. This is narrower than equal platform coverage, persona fidelity,
research speed or measured accuracy. It is not a claim of overall superiority.

Atypica describes qualitative observation, hypothesis synthesis and returning to
social material for counterevidence in its [Scout documentation](https://atypica.ai/features/scout-agent).
Its [Product R&D documentation](https://atypica.ai/features/product-rnd-agent)
connects user tasks and competitor context to concepts and validation plans, and
explicitly treats the result as ideas to test. Those documented operations are the
comparison target; not an invented requirement that every complaint become a product.

## Concrete coverage

| Operation | Product Idea Research execution evidence | Boundary |
|---|---|---|
| Start without a product idea | Independent live run collected tasks across video, freelance delivery and small sellers before creating 27 cards / 11 clusters | Convenience sample, not representative demand measurement |
| Read original posts and replies | 25 Reddit originals and 143 retained comments across baseline + new collection; parent-read X/LinkedIn and Xiaohongshu supplements | Host web/browser access; no bundled X/LinkedIn MCP or guaranteed platform access |
| Return to evidence and revise | Read author follow-ups, free/sufficient alternatives and promotions; independent semantic audit corrected exact citations; current Subtitle Edit docs narrowed the subtitle opportunity | Review is required; first draft was not error-free |
| Preserve usable need structure | Field-level actor/trigger/outcome/workaround/friction/frequency/payment, stated/inferred/unknown, parent references, discussion families and candidate/resolved/promotion/adjacent/unclear | A structured card is an interpretation, not an independently verified customer |
| Produce a commercial decision | Final report selects two narrow delivery experiments, with alternatives, costs as hypotheses, buyer routes and go/stop conditions | No customer acquisition, completed payment or profitability validation |
| Inspect and continue locally | Immutable records/snapshots, exact claim-to-excerpt review, selected report, linked need pool/evidence and CSV/JSON; public offline replay | These are demonstrated local design properties, not proof Atypica lacks similar capabilities |
| Choose modules | Social-only holdout ran with no personas/interviews; earlier standalone competitor, simulation and combined evaluations remain linked in evaluation history | Same skill installed for both hosts; current model-level evaluation ran in Codex |
| Personas and simulated interviews | Previously evaluated custom-method roles and interviews can be combined with sourced research | No shared persona population, longitudinal calibration or proof synthetic answers predict real people |
| Cross-domain inspiration | Discovery can retain adjacent tasks and new-capability hypotheses | No dedicated comparative evaluation of creative cross-domain concept quality |
| Hosted research infrastructure | Not implemented | No built-in social index, hosted research UI, team workspace or background research service |

The [final report and need pool](../examples/demand-discovery/README.md),
[protocol](../evals/discovery-protocol.md) and [evaluation record](../evals/README.md)
make the coverage claim inspectable. Exact quotation support is a deliberate product
feature: `pool --review` exposes the actual cited passage so an agent can catch a
claim that points at the right post but the wrong excerpt. It does not certify truth.

## Hands-on Atypica comparison limits

Earlier authorized API trials exercised research planning, scouting and interview
orchestration. A final report did not complete because of timeout/quota. Retrying the
existing discovery study on 2026-10-16 returned `saved_no_ai / quota_exceeded`, so
there is **no fresh successful paired final-report comparison**. That failure is
not counted as an advantage for this project. Credentials, session state and API
responses remain private.

Historical scouting outputs supplied known context-regression cases: an Arabic
customer-service chatbot complaint used as video/dubbing evidence, AI film
production spend used as course/localization-update spend, and a paid promotion
for a partial-edit solution presented as an unresolved repair demand. These were
checked against their source contexts where accessible; they are purposively
chosen known cases, not an accuracy benchmark. Sources include the
[chatbot post](https://x.com/shahzad_jamil79/status/2107790403365638647),
[film-production post](https://x.com/_GAi92/status/2108670873251266938) and
[partial-edit promotion](https://x.com/HighSignal_AI/status/2110042437070606345).
Undocumented original links in other summaries remain unverifiable, not presumed fabricated.

Atypica also documents [MCP integration](https://atypica.ai/features/mcp-integration).
MCP availability is therefore not a differentiator by itself. This release actually
used the host browser when no relevant X/LinkedIn connector was available. An
installed profile-search tool would not establish comment access.

## What would justify a stronger claim

Equal or better accuracy would require fresh matched tasks and accessible outputs
from both products, a shared evidence budget and an independent review of claims,
missed needs and false opportunities. Broad product parity would additionally need
platform/persona/hosted-workflow evaluations. Neither is established here. The
release is usable for the scoped demand-discovery job, with transparent evidence
and review; it is not a certified replacement for every Atypica feature.
