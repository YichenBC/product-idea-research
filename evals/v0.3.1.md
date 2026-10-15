# v0.3.1 live research and iteration

Date: **2026-10-15 (Asia/Shanghai)**. [v0.3 acceptance](v0.3.md) ·
[v0.2](v0.2.md) · [v0.1 history](v0.1.md).

This round used **real public sources**, not authored social fixtures. It is one
bounded live forward evaluation plus one independent offline follow-up, not a
statistical research benchmark or a paired comparison against Atypica.

## What actually ran

1. An independent research agent used the shared skill on a realistic request:
   find small-language AI-video opportunities a solo builder can deliver with agents.
   Sources were saved incrementally. It read 22 social/community families and
   official pages for seven alternatives, then synthesized three roles and three
   Q&A turns per role. The first report was frozen before parent corrections.
2. The parent independently read three additional social cases and one human-service
   case, reviewed evidence and narrowed the leading proposed product. The final
   study contains **25 accessible social families**, seven software/platform
   alternatives and a human-service example. Fifty records include supplementary
   excerpts and five unavailable records; these are not fifty customer needs.
3. A separate agent used the revised skill on frozen real material, with a narrower
   Web-product decision request, **no browsing and no new interviews**. It excluded
   all stored simulated interviews, retained access gaps, distinguished Enterprise
   API access from UI pricing, and treated switching/payment as unverified.
   [Inspect its report and replay inputs](live-forward/README.md).
4. That forward run exposed two report presentation defects. After correction,
   rerendering preserved the ledger and all twelve prior exported files byte-for-byte
   (SHA-256 comparison), with correct social coverage and normal finding paragraphs.

[Final Chinese research report and evidence](../examples/small-language-video/README.md).
The live and follow-up agents ran in the Codex host with its available tools. This
is **not** a fresh standalone Codex CLI or Claude Code model execution. The earlier
v0.3 standalone Codex run remains separately documented.

## Changes driven by observed behavior

| Observed issue | Correction | Verification |
|---|---|---|
| All material groups included vendor pages and failed retrievals; the count could be mistaken for social coverage | Add citable source/material/social counts to audit, retain legacy field for compatibility; show separate labeled counts in reports | Tests failed for missing fields first, then passed; final live report shows 25 social families, follow-up shows 22 |
| Long finding paragraphs were rendered as giant headings | Short numbered headings with escaped body paragraphs; anchors unchanged | Failing HTML/Markdown regression first, then passing tests and independent rerender |
| Precise competitor details sometimes lived only in context, not their cited excerpt | Remove unsupported precision in the final report; skill now prioritizes decisive excerpt conditions within quote limits | Semantic review found and removed exact language-count and source-direction overclaims |
| Model/plan/channel differences and internally conflicting official prices repeatedly required manual reconciliation | Competitor guidance now explicitly checks feature × version × direction × plan × UI/API and retains conflicting quotations | Independent follow-up recognized Enterprise API gate and unresolved unit economics |

The first researcher already handled many plan/version distinctions correctly;
that guidance change consolidates observed useful practice, not a claim that all
of those distinctions were missed. Structural citation validation never proves
semantic entailment; independent review still found wording that needed narrowing.

## Verification

- **54 tests and 10 subtests passed** locally, including audit selection/grouping,
  accessible versus blocked material, empty studies, safe rendering and snapshots.
- Independent Python review approved both audit and renderer changes; HTML/Markdown
  escaping, Chinese labels and existing citation anchors were checked.
- Skill frontmatter/reference validation passed. Wheel build and fresh installation
  are part of release verification; both host skill destinations use the same files.
- Browser inspection confirmed the final report renders Chinese text, coverage and
  ordinary finding paragraphs. Source text was not executed.

## Limits

X, Xiaohongshu and Pantip bodies were unavailable. English-language discussions
predominate; there is no representative native-language market survey. Official
pages are vendor claims, not product trials. Pricing conflicts and actual API costs
remain unresolved. No real interviews, paid pilots, customer uploads or audio/video
quality tests were conducted. All proposed prices, cost budgets and success/stop
thresholds are research hypotheses.

Claude Code skill installation is checked; actual Claude model behavior remains
unverified. No evidence establishes superiority over Atypica or validated profit.
