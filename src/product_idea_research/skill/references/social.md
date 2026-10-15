# Social research: statements in context

## Turn the question into a sampling plan

Identify the task, who performs/pays/approves it, the trigger, market/language and
what would change the user's decision. Do not assume those roles are separate or
that all tasks are business purchases. Build several search families:

- Doing the task: “how do you…”, “workflow”, “怎么做”, “求助”, task-specific verbs.
- Breakdown/workaround: “manually”, “export/import”, “takes hours”, “只能手动”.
- Alternatives and rejection: “alternative”, “switched back”, “good enough”,
  “不需要”, “替代”, “退款”, “弃用”.
- Buying/delivery: task requests, “looking for someone”, procurement constraints,
  project budgets, existing paid services. Keep asking price distinct from payment.

Use relevant public Reddit communities, X, Xiaohongshu, specialist forums, product
support communities, app reviews and task marketplaces. These are channel choices,
not guaranteed connectors. Use the host's available search/browser/API or supplied
exports. Follow the user's chosen channels; never silently substitute different
ones and imply coverage. Preserve actual queries and collection date in the run.
Search in the task's native vocabulary and requested languages. Use translation
for interpretation but retain a short original excerpt; language does not imply
nationality, geography or purchasing power.

Start with a small varied batch, inspect what it misses, then adjust queries.
Sample relevant low-engagement discussions too. Follow-up comments often explain
why a workaround works or why the proposed feature is unwanted. Record both the
post and the specific comment link when available. Read their parent context;
if unavailable, state that limitation. Before relying on a request as an unmet
need, look for later author clarifications, accepted solutions and resolved status.
Separate the desired outcome from the workaround first proposed: a requested
file format, feature or tool can change after replies explain alternatives. If
that later context cannot be read, qualify the task interpretation. A thread with many comments is one
conversation family, not that many independently sampled customers.

## Save evidence, not reconstructed testimony

For every useful item save a source record:

- `url`: original permalink; no invented links. For private/local exports use
  source_type `provided`, nullable URL and a meaningful locator.
- `access`: full means the source body was retrieved; excerpt means only a bounded
  passage was read; snippet means only search output; unavailable means no content.
  Reading a page body does not prove all its comments loaded. Explain scope in context.
- `excerpts`: short verbatim passages with locator (comment permalink, section,
  timestamp or supplied file line). Retain spelling, and avoid enough quotations
  to reconstruct protected articles. A paraphrase belongs in findings, not excerpts.
- `group_id`: stable family ID for the thread/document or known syndicated content;
  do not group unrelated people solely because they discuss the same topic.
- `context` and `limitations`: date uncertainty, promotion/affiliation, parent not
  read, author self-report, relevant selection effects or truncated content.
  `published_at` is null if unknown, not a search engine's crawl timestamp.

Inspect cross-posts, repeated phrasing, affiliate links, founder promotion and
hypothetical questions. These can be useful but are weaker evidence of customer
experience. Do not infer bot status or deceit without evidence. Dedup before
counting; `audit` flags mechanical duplicates but cannot detect every paraphrase.
A reported pain, an actual workaround, a claimed payment and a seller quotation
have different meanings even when they appear in the same thread.

Report collection coverage using `audit.selected.citable_social_families` for
accessible posts/comments/reviews, with vendor documents and blocked leads stated
separately. The legacy `discussion_families` field counts **all** material groups,
including official pages and inaccessible records. Neither count establishes
independent buyers: inspect supplied grouping, author roles and promotional context.
Provided feedback exports need their own described sampling unit rather than being
silently counted as public social threads.

## From materials to opportunities

Extract the decision-relevant chain: actor → trigger → desired task → current
solution → friction or satisfaction → constraint → proposed change. Preserve the
chain for each source before clustering. Cluster by task/constraint, not merely
shared keywords. Keep meaningful disagreements and identify the conditions that
could explain them. One source supports an illustrative case, not prevalence.

When asked for opportunities, use the optional `opportunities` report field:

- Name a specific audience and problem, with the current alternative.
- Suggest the smallest deliverable that addresses it. For a solo builder, inspect
  reachable buyers, acquisition route, feasible data/model access, integration,
  quality review, ongoing support and approximate cost assumptions. Avoid framing
  a new foundation model or inaccessible platform data as a weekend Web project.
- Rank `test_now`, `watch` or `drop`, explaining the trade-off in rationale. A few
  enthusiastic posts do not justify a revenue forecast. A simulation alone cannot
  support `test_now` in the CLI, and a real source is still not proof of demand.
- State risks and one real test with an observable success/stop condition. Prefer
  a buyer interview around an actual recent task, a sample deliverable, a manual
  service trial or a prototype comparison with the current workaround.

Do not turn every complaint into an app. “Already solved cheaply,” “infrequent,”
“buyer unreachable,” “platform-dependent” and “no observed switching reason” are
valid conclusions. If the user only asked for listening/reconnaissance, summarize
patterns rather than forcing a business ranking.

## Missing access and completion

After a blocked retrieval, use another authorized public route or a relevant
accessible source; do not repeatedly retry the same obstacle or bypass login.
Keep snippets as leads, record the gap, and request exported material only if it
is essential. Offline research can use provided materials with explicit provenance.
If none are available, save a partial run and a zero-finding report with limitations
and a concrete collection plan. Never simulate social posts to make up the count.

Complete means the declared bounded research scope was covered. If a requested
platform, volume, language or comment layer is missing, keep the run/report partial
and disclose it. A diverse sample is still a convenience sample, not a survey.
