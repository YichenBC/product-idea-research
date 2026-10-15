# Translated-subtitle review: a bounded live study

Date: **2026-10-15**. Chinese reports from actual public web research using the
packaged skill, followed by an independent evidence review and an immutable correction.
These are selected public excerpts and synthetic role-play, not real customer interviews.

| Report | Scope |
|---|---|
| [Combined](combined/report.md) / [HTML](combined/report.html) | Social + competitors + two simulated roles, three Q&A turns each |
| [Social only](social/report.md) / [HTML](social/report.html) | Discussion evidence; no interviews selected |
| [Competitors only](competitor/report.md) / [HTML](competitor/report.html) | Official alternative documentation; no interviews selected |

The main report says to investigate further before building a generic review SaaS.
It preserves existing alternatives and does not treat complaints or role-play as
proof of willingness to pay. Each report links to its evidence companion.

Eight accessible discussion families (six Reddit, one GitHub issue, one Adobe
Community) and three official alternatives were examined. The corrected ledger
has 21 source records and four run records, including failed access and rereads;
**21 records do not mean 21 customers or independent sources**. No products were
installed or trialed. Searches in this pass were English-language; this is not a
representative multilingual market survey. No platform API, paid account or key
was used.

## Why the correction matters

The first pass missed Amara's notes/version features and an original poster's
later clarification. Independent review caught both. New source/run IDs preserve
the original evidence; revision 7 corrects the report and downgrades the leading
opportunity to `watch`. The old simulated interviews remain unchanged and their
now-incomplete assumptions are stated explicitly. See the [research trace](research-trace.md)
for retrieval outcomes and review changes. The public snapshots are the corrected
exports; the trace describes earlier local exports, which are not bundled here.

## Replay without browsing or model calls

From the repository root after installing the CLI:

```bash
product-idea-research init studies/subtitle-replay --title "Translated-subtitle review"
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/brief.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/sources.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/roles.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/interview-template.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/interview-coordinator.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/runs.json
product-idea-research ingest studies/subtitle-replay --file examples/subtitle-research/inputs/correction-batch.json
product-idea-research check studies/subtitle-replay --report examples/subtitle-research/combined-draft.json
product-idea-research audit studies/subtitle-replay --report examples/subtitle-research/combined-draft.json
product-idea-research render studies/subtitle-replay --report examples/subtitle-research/combined-draft.json
product-idea-research render studies/subtitle-replay --report examples/subtitle-research/social-draft.json
product-idea-research render studies/subtitle-replay --report examples/subtitle-research/competitor-draft.json
```

Use a new study directory. The seven batches recreate revision 7; repeating an
identical batch is a no-op. Duplicate URL warnings for deliberate rereads and
unavailable-source warnings are expected. Replay validates and renders saved
material; it does not refresh websites or reproduce stochastic model reasoning.
Keep each exported directory together when sharing HTML or Markdown.
