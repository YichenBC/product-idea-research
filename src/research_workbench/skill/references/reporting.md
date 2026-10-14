# Report from the actual transcripts

Use the data contract for report JSON. The CLI supplies the layout, synthetic
notice, role table, method, full transcript appendix and internal source links.
You supply the meaning: concise summary, findings, limitations and next steps.

For each finding:

1. Identify one concrete hypothesis, disagreement or constraint.
2. Cite one-based turn numbers from the selected interviews that actually support it.
3. Add counterevidence references where the simulated answers disagree.
4. State its limits, including relevant role assumptions. Never mark a simulated
   quote as a real customer observation or measured willingness to pay.

Use `kind: simulation` for every finding. No percentages of synthetic respondents
as evidence of demand. No “validated market” conclusion from role play. A useful
next step is a question or experiment to conduct with real users, not a claim
that it has already been conducted. Do not automatically contact anyone.

Set `study_revision` from the current saved study. `complete` means the requested
persona count was interviewed, not that the business idea was verified. `partial`
is honest when a role failed, scope was narrowed, or interviews remain unfinished.
Explain partial coverage in the limitations. More than one interview with one role
still counts as one role.

Choose only relevant interview IDs for this report revision. Old records remain
in the study. Rendering writes a new numbered output directory and frozen JSON
snapshots; it never overwrites an earlier report.

Example grounded-in-transcript phrasing: “The simulated approver questioned whether
notifications justified adopting another app (i-2, turn 3). A real interview should
test whether missed changes are frequent enough to matter.”

For a report-only request, reuse saved interviews and avoid changing the recipe or
generating new roles. If a stale revision error occurs, reread the changed study and
reconcile the draft rather than merely changing its revision number blindly.
