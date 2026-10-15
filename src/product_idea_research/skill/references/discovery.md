# Discover demand before proposing products

Use this reference when the user wants to find needs, sweep discussions/comments,
or build an opportunity pool. Do not require an idea or a persona first. An industry
or reachable audience is a starting lens, not a constraint to confirm one concept.

## Plan collection around tasks and access

First inspect actually available host connectors/MCP, search, browser sessions and
user-provided exports. Test one relevant original post **and its replies** before
promising a platform. A search tool failing does not establish that the browser
cannot read it. Conversely, a LinkedIn profile-search MCP does not imply post or
comment access. Do not install unknown servers, extract session cookies or purchase
API access just to satisfy a source count. See [access routes](access.md).

Use several distinct task families and search for actual attempts, abandonment,
manual work, paid delivery, alternatives and reasons a solution is sufficient.
Keep source languages and customer types varied where requested. For broad research,
start with a varied batch, then expand task clusters supported by concrete evidence
and seek contrary cases. Do not let the first plausible complaint anchor the study.

Read original post, parent context, relevant replies and author follow-up. Comments
may add a separate need, correct the task, reveal a sufficient solution or only say
"same". Preserve this distinction. Record reply locators and `parent_source_id` where
its saved parent is known. If only part of a thread is visible, say which part; a
visible reply count is not a count of comments read. Expand relevant collapsed
replies or load another page when tools allow it; record inaccessible branches.

For each collection batch record actual queries, platforms/routes, counts of post
bodies and individual comments read, retained source IDs and remaining gaps in the
run method/limitations. Counts must come from a saved item list, not estimates.
Distinguish leads found, bodies read, comments read, retained evidence, conversation
families, need cards and task clusters. They are different units. A requested volume
of hundreds should be collected in resumable batches; never turn hundreds of search
snippets into hundreds of validated demands. When access stalls, continue through
other authorized routes while leaving the unmet platform target explicit.

## Persist a need pool before a shortlist

Use `needs` records from [data contract](data-contract.md), not just report prose.
Save concrete task interpretations after their source batch and social run. Each
card includes actor, trigger, desired outcome, current workaround, remaining friction,
frequency and payment. Each field is `stated`, `inferred`, or `unknown`, with exact
excerpt references. If an excerpt does not contain a claimed amount/frequency/language,
mark it unknown or find the specific support; don't hide invented facts in context.
A quote's existence is not an entailment check.

Classify the signal as candidate, resolved, promotion, adjacent or unclear. This is
a researcher judgment. Keep useful rejected signals and why they were rejected; a
vendor may describe a real problem but is not independent buyer demand. A solved
case can still reveal a better experience hypothesis; explain the additional gap
rather than erasing the existing solution. Keep task category, language, workflow,
source date and commercial role aligned with the excerpt.

Cluster by desired outcome and constraint, not by shared product names. Keep multiple
independent cases as separate cards in one cluster, and repeated author replies as
one discussion family. A cluster with ten replies in one thread is not corroborated
by ten customers. Reusing the same source across cards does not add evidence.

Run `pool DIR --review` (add `--report FILE` for a selected snapshot) to inspect
each claim beside its exact cited text. Review all shortlisted cards and every
non-unknown payment/frequency field before reporting. A long source split into
excerpts can contain the right fact in a different excerpt: repair the specific
reference, narrow the claim, or mark it unknown. The command joins evidence; it
does not judge whether the claim follows from it. Append corrected cards with new
IDs and select those IDs in the next report, preserving the first output.
For a large pool, save the JSON to a file and inspect `claim_review` in batches;
truncated terminal/tool output does not count as reviewing the omitted claims.

Inspect both promising and rejected cards. Expand the leading
clusters using different queries/authors/channels; explain if no independent case
was found. Preserve singleton opportunities as hypotheses, without pretending that
repetition is necessary for every new experience or that a pain proves a business.

## Turn needs into testable opportunities

For shortlisted opportunities, connect `need_ids`, the strongest existing alternative,
why someone might switch, reachable buyer/channel, smallest sellable deliverable,
agent/human boundary, operating costs and the cheapest decisive experiment. Clearly
label proposed prices/costs and acquisition assumptions. Existing spend, a quote,
"would pay", free-only intent and completed payment are different observations.

Evaluate new possibilities too: what previously abandoned task becomes feasible
because a specific capability or cost changed? Keep this as a hypothesis and test
actual use/reuse before claiming a market. Simulations may reveal objections; they
never fill missing social evidence or payment fields.

Deliver a short decision report with a comparison table and a separately browsable
need pool. Render with explicit `need_ids`; the same immutable snapshot includes
needs HTML/Markdown/CSV/JSON and evidence links. Include reasons for exclusions and
unmet coverage. `check` verifies structure; personally review the top conclusions
against excerpts and full context before claiming that the research is complete.
