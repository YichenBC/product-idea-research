# Behavioral acceptance cases

Record host version, prompt, available tools, artifact checks and limitations.
Separate deterministic fixture replay from actual model-driven runs. Do not claim
that matching a schema proves research quality.

1. **Empty library, no network:** user specifies two roles and a three-turn
   interview method. Agent creates recipe/cards/transcripts/report and uses CLI.
   No persona service or browsing. All attributes assumed/unknown.
2. **Everyday-life domain:** use trip planning or household coordination; no invented
   employer, procurement budget, demographic identity or purchase history.
3. **Scope checkpoint:** user asks only for cards. Save them and stop. On a later
   request, reuse those cards and continue interviews.
4. **Report-only continuation:** use saved interviews, do not generate new roles.
   Report references specific turns; preserve the previous report snapshot.
5. **Partial coverage:** requested three roles, only two interviewed. A complete
   report is rejected; a partial one discloses missing coverage.
6. **No demand-validation leap:** satisfied alternative appears in interviews and
   is preserved in findings. No synthetic purchasing percentage or market claim.
7. **Corrupt/stale input:** invalid references and stale draft revision fail without
   changing saved study data or exposing raw tracebacks.
8. **Installed artifact:** install from a built wheel, outside the checkout, into
   both host skill locations. Replay example and inspect exported reports.

Human review: check question/answer continuity, decision-relevant role differences,
claim-to-turn support, unknowns and useful real-world follow-up questions. Record
observations rather than inventing a numeric quality score.
