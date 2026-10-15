# One report from the selected research

Answer the user's question first. Synthesize across modules by decision or finding,
not by recounting tool calls or writing one interview recap per persona. Include
only research actually performed. A competitor report is complete without social
listening or simulation; a combined report does not need equal space for each.

Read [data contract](data-contract.md) for JSON. Select relevant `run_ids` and
`interview_ids`; older corrections and unrelated stored sources remain archived.
Use the latest study revision only after reading changes. A report-only request
reuses saved materials without browsing or generating new interviews.

## Evidence and disagreement

For each finding choose the smallest well-supported statement and exact excerpt
or one-based interview turn. Read each referenced passage in context, including
surrounding objections. Valid references are not proof of semantic support.

- `source`: what the source actually reports/claims; external material only.
- `inference`: your interpretation from external material; explain the reasoning
  and what could disprove it, not only the conclusion.
- `simulation`: hypothetical interview conclusions; interview support only.
- `mixed`: external sources plus synthetic interviews. Name which part is observed
  as a source statement and which part is simulated. Agreement from a simulated
  role does not independently corroborate an external claim.

Counterevidence can reference either type but never changes what supports the
claim. Surface satisfaction, cheap alternatives and rejection conditions. If the
materials disagree, explain plausible task/plan/time/context differences only as
inferences, or leave the conflict unresolved. Do not average incompatible claims.
Search snippets/unavailable content cannot support report claims. Vendor marketing
cannot establish real user success; a user complaint cannot prove a product lacks
a feature. Repeated authors/comments or copied sources are not independent samples.

## Main report and appendices

Write a brief summary with the answer, its practical implication and the largest
uncertainty. Then a few useful findings, optional `comparisons` and `opportunities`,
next steps and concise limitations. In longer studies, merge repetitive findings
instead of making the reader sort through hundreds of observations. Keep source
material, collection queries, role cards and full Q&A in the evidence companion;
the renderer links to exact passages. Do not put filenames, ingestion counts or
validation mechanics in the substantive summary.

Use comparison rows for externally supported alternatives. Use opportunity rows
only when the user needs choices to pursue. Their priorities are reasoned judgments,
not model probabilities. `test_now` means worth a real test, not validated demand.
Every next step should answer an unresolved decision: who to reach, what real task
to inspect/compare, what observable result would support or stop the idea. Do not
send outreach or run a purchase automatically.

Keep relevant caveats without repeating the same simulation disclaimer in every
sentence. Local evidence coverage belongs in the scope summary; unknown population
prevalence, self-report and model role-play remain different limitations.

## Completion and quality pass

`complete` is coverage of the selected bounded work, never a validated market.
All selected runs must be complete, and selected interviews must cover the recipe's
planned roles. User-requested but unperformed work remains a partial run/report;
do not quietly exclude it from selection to obtain a green completion status.
When retrieval is completely blocked, partial reports can have no findings and
should explain the specific gap and next collection step instead of inventing data.

Before export:

1. Check every significant sentence against its cited excerpt/turn, preserving
   date, role, plan, units and source's qualification. Remove unsupported precision.
2. Recheck the strongest proposed opportunity against the closest alternative
   and the original authors' later clarifications. Look beyond the excerpt selected
   on the first pass; record new evidence if it changes the interpretation.
3. Review counterevidence and source independence. Look for the strongest reason
   the proposed opportunity would fail or the existing alternative would suffice.
4. Check the requested scope: languages, platforms, counts, modules and exclusions.
5. Run `check` and `audit`. Resolve validation errors; inspect duplicate/coverage
   diagnostics and state unresolved gaps. These commands cannot judge truth.
6. Render a new numbered snapshot. Do not edit an exported report by hand while
   leaving its saved draft inconsistent; revise the draft and render again.

Return a short answer and the main report links using the absolute paths from
`render.artifacts`. The CLI returns only the formats actually generated; use
`report_md` / `report_html` and their `evidence_*` companions as available. Mention only material access or
validation limits; details remain available behind the source links. Preserve the
whole export folder when sharing a report with its evidence companion.
