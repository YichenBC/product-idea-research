# Demand discovery iteration

The user explicitly requests autonomous development until Product Idea Research can be compared credibly with Atypica, with actual demand discovery from social posts and comments as the core. This iteration addresses the demonstrated gap: sources exist but individual needs, rejected signals and comment context disappear into a report.

## Design

Keep host-operated collection, rather than ship fragile credential-dependent scrapers or make a hosted vendor mandatory. Discover available MCP tools and browser sessions, test a real post plus reply access, then adapt collection to the supported route. Document connector limitations. A browser read is not an MCP integration.

Add an optional immutable `needs` collection to existing schema v1. A need belongs to a social run and a researcher-assigned task cluster. Seven field-level claims (actor, trigger, outcome, workaround, friction, frequency, payment) carry explicit stated/inferred/unknown basis and source excerpt references. Candidate/resolved/promotion/adjacent/unclear is the researcher's disposition, not a machine truth score. Corrections append new IDs; reports explicitly select need IDs.

Optional source `parent_source_id` connects comments to a saved parent in the same discussion family. Validate references and cycles without assuming every comment has an accessible parent. Canonical X status IDs prevent renamed handles from inflating duplicates. Do not infer customer identity from handles, counts or biographies.

`pool` returns structured need records, cluster membership and deduplicated discussion counts. `render` adds needs JSON/CSV/Markdown/HTML only when selected, using the same atomic snapshot and escaping as reports. Selected needs must belong to selected runs; opportunity cards may link selected need IDs. CSV formula prefixes are neutralized. Existing studies, commands and report-only tasks remain compatible.

## Acceptance and comparison

1. Write failing tests for atomic ingestion, missing/invalid/ineligible references, unknown versus source-backed claims, comment ancestry, selection isolation, duplicates and safe output. Implement and run full suite.
2. Test current skill independently on three real demand domains with comment targets; freeze its initial output. Update skill based on observed failures and rerun a fresh independent request. Keep acquisition counts separate from retained evidence and demand counts.
3. Review an Atypica historical output against its original sources, then review our output under identical interpretation criteria. Known historical errors are regression cases, not a blind superiority benchmark. New Atypica execution is currently quota-blocked; do not call this a win.
4. Actual browser access: X post bodies and LinkedIn post plus three comments were read on 2026-10-15. Exact field facts remain excerpt-grounded; enough text read does not imply all comments read. No new paid integrations, outreach, private uploads or purchases.
5. Review code independently, run live end-to-end study and publish only verified changes. Do not claim full platform parity or accuracy superiority without evidence.
