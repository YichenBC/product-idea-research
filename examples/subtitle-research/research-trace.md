# Live research trace — 2026-10-15

This study ran before the rename from Research Workbench; the tool name below
has been updated for readability, without changing the observations.

Scope: independent use of the packaged product-idea-research skill for a Chinese research request about small-team translated-subtitle review. No API keys, login, trials, purchases, outreach or publication. Only this evaluation directory was written. This is an actual bounded web study, not a code review.

## What I actually did

1. Read SKILL.md and social, competitors, method, data-contract, reporting references. Ran CLI --help, then init.
2. Used the available `web__run` tool for 13 literal search queries saved under the two runs. Searches were in English to find workflow discussions, with specific Welsh and Arabic/bilingual queries; no Chinese-language production-team source was found/read in this pass.
3. Opened discussion URLs, then used find/open for relevant body sections. Clicked four Reddit comment timestamps to obtain actual comment permalinks. Did not assume every collapsed reply was read. The 8 eligible discussion families are s1–s8; six are Reddit, one GitHub issue and one Adobe Community post. s2 has no replies returned. All eligible sources conservatively use `excerpt` access, not `full`.
4. Read official Subtitle Edit main-branch documentation, Amara Plus support, and Premiere Translate captions documentation. No product was tested. Searched OOONA and Aegisub too; only selected genuinely read official pages support comparisons.
5. Saved immutable brief, source batch, recipe and role cards before generating interviews. Saved each 3-turn interview separately, then module runs. Revision is 6. Three rounds means three sequential interviewer/respondent Q&A turns per role, not three separate real interviews.
6. Wrote a Chinese combined report with source statements, inferences and simulation findings separated. Exactly two opportunity rows, one `test_now` for a real workflow test and one `watch`. No market-size, conversion, willingness-to-pay or model-accuracy estimate.
7. Ran check and audit. Both succeeded. Audit reported 11 excerpt-access sources and 6 unavailable, no mechanical duplicates, with an expected ineligible-sources warning for the 6 failures. The CLI's 17 `discussion_families` includes official documents and inaccessible leads; the substantive report explicitly says 8 accessible discussion families and does not use 17 as a customer count.

## Access failures / friction

- Reddit r78gpp (translated scripts to SRT) and l136n6 (Korean editing workflow): open returned TimeoutError. 1dfo3aj (Arabic documentary editing) returned Internal Error. Their search summaries were not promoted to evidence; b1–b3 preserve the URLs and failure descriptions.
- OOONA product overview: search returned extensive snippets, open returned Internal Error. OOONA User Configuration: initial open reported 400 lines but relevant body text was not displayed; find returned no matching text; subsequent open returned Internal Error. OOONA Compare: open returned only serverDuration/correlation metadata. All treated conservatively as unavailable b4–b6. Chose Premiere as third accessible official alternative instead of padding the count.
- Web open sometimes returned long navigation chrome, and bounded windows often omitted the target text. find and targeted open exposed the actual paragraphs (notably Premiere at L1792–1830). Source locators preserve the relevant section/lines; line numbers are retrieval locators, not immutable website anchors.
- Reddit source updates yielded different line counts across tool calls. Saved exact bounded excerpts with discussion/comment URLs and contextual limits, rather than claiming a full archived page.
- Historical GitHub issue was closed as completed; report retains it as a counterexample to treating an old request as an unsolved 2026 gap.
- Small-agency post initially used “translations” loosely but later said “No translation thankfully.” This correction is preserved and the report treats it as adjacent same-language captioning workflow, not direct translation-team proof.
- Non-Reddit saved excerpts were kept short (under 25 English words per webpage); only short relevant source passages were saved. No large full-page copies.

## Workflow evaluation observations

Worked: CLI init/ingest were straightforward; all batches validated first try; recipe-before-interviews and immutable records kept assumptions explicit. `check` resolved all report references; `audit` made access exclusions visible. No CLI/runtime errors before rendering.

Friction: documenting original post plus comment in a single source requires prose context and excerpt locators rather than separate per-excerpt authors/types. This is workable and avoids inflating discussion count. Coverage diagnostics aggregate official documents and blocked leads as families, so human-readable scope must explain the denominator. `check` is structural and cannot catch an overbroad claim or a misread access result; manual entailment review remains necessary.

The parent requested rendering once the concurrent renderer was ready, plus social-only and competitor-only snapshots from the same saved evidence. These are report selections, not new research or regenerated source records. Original combined draft and original exports are preserved for independent review.

## Render completion

- Combined check/audit/render succeeded: reports/001.
- Social-only check/audit/render succeeded: reports/002, selected 8 eligible discussion sources plus 3 access failures; no interviews selected.
- Competitor-only check/audit/render succeeded: reports/003, selected 3 eligible official sources plus 3 access failures; no interviews selected.
- One agent-authored shell invocation accidentally appended `/product-idea-research --help` to the executable path and failed with `not a directory` (exit 127) after the competitor check had already passed. This was a command typo, not a CLI failure; the intended competitor audit/render was then run normally. No record or report was lost.
- No research records changed while deriving module-only drafts. The initial combined report remains preserved as reports/001.

Post-render artifact inspection: all three snapshots contain report/evidence Markdown and HTML plus study.json/report.json. Checked every main-report evidence anchor against its evidence companion in both formats: no broken anchors. Combined has 9 findings/2 interviews, social-only 5 findings/0 interviews, competitor-only 1 finding/0 interviews. Skimmed combined report Markdown; the scope caveat and evidence-type labels render as intended. No browser visual inspection was performed.

## Independent evidence-review correction — revision 7

The independent review found substantive omissions in the initial report, not merely formatting problems. Historical reports/001–003 and their original drafts are retained unchanged for inspection.

- Amara: the initial extraction omitted notes, member activity and version comparison/rollback, all directly relevant to the proposed opportunity. The original comparison also overstated a recommendation that another member review as a requirement. The executing agent reopened the Plus URL and the old tool ref; both failed via Freshworks OAuth redirect (500/non-retryable); find returned no matching text. No login or workaround bypass was attempted. A separate study-team evidence reviewer had successfully opened this original page in the current review round as `turn137view0` (645 lines). Their original-page excerpts and surrounding context were supplied to this agent with exact locators. New source `c2-details` explicitly attributes that successful retrieval to the reviewer, and `b7-amara-reread` preserves this agent's failed request.
- Added exactly 6 new quoted words from the original Plus page: the 2-word notes label and the 4-word compare/rollback heading. Verified original c2 19 + new c2-details 6 = 25 total words. c2, c2-details and b7 share c2-family and the original URL; duplicate-URL warning is expected, not independent corroboration.
- As a public cross-check the executing agent searched the three additional exact queries saved in the corrected competitor run, then successfully opened https://sites.google.com/amara.org/supportandresources/amara-teams/amara-community-teams (`turn145view0`, 390 lines). Read L271–289 optional Review and L321–351 activity, notes, comparison and rollback. This is explicitly a Community page with public-facing conditions (L26–29); its conditions were not applied to Plus. No extra quote record was created from this cross-check.
- s6: personally opened https://www.reddit.com/r/SubtitleEdit/comments/1uavdit/comment/oss8nkz/ (`turn142view1`) and read the parent and follow-up. L105–106 confirms two tracks were a styling workaround in DaVinci Resolve, while one English-top/Mandarin-bottom file would be ideal. New `s6-clarification` shares s6-family and corrects the older context. The report no longer treats two single-language deliverables as an immutable goal or treats the bilingual suggestion as a misunderstanding.
- s5: personally reopened the Welsh thread and read L156–164 and L230–234 (`turn143view2`). Added `s5-counterpoint` sharing s5-family: standard writing can also help learning; the original poster acknowledged that value while citing their level. The report now treats literal/dialect transcription as an option to test, never a universal pedagogical rule.

Appended new immutable source records and `run-social-corrected` / `run-competitor-corrected`; existing study records unchanged. The two synthetic role cards and interviews were intentionally not rewritten. Corrected findings and limitations say the coordinator's two-single-language-files assumption is a hypothetical scenario, not the fully clarified s6 user's goal; the original simulation did not assess Amara's newly extracted features and cannot establish a gap.

The former `test_now` delivery-review prototype opportunity is downgraded to `watch`: first investigate whether real teams still have specific recurring obstacles after accounting for Amara's notes/comparison/rollback and existing SOP workflows. Both opportunity rows now remain observation questions. Summary contains substantive conclusions; counts and method scope are in limitations and renderer metadata.

Corrected drafts: report-corrected.json, report-social-corrected.json, report-competitor-corrected.json. All passed check/audit/render at revision 7; logs saved beside drafts. Corrected snapshots: reports/004 (combined), /005 (social only), /006 (competitor only). Both standalone reports select no interviews. Audit warnings are expected same-page rereads plus unavailable source records. All main-report evidence anchors were checked in Markdown and HTML; no broken anchors. No browser visual inspection or new product test was performed. Ready for another independent evidence review before public example use.
