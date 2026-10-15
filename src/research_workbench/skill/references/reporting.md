# Report from the actual transcripts

Use the data contract for report JSON. The main report is a decision-oriented
deliverable: answer the user's research question first, then explain findings,
disagreements, implications and next steps. Summarize what the interviews imply;
do not organize the report as one interview recap per persona. Do not fill the
summary with execution counts, filenames, schema checks or other implementation
details. A short coverage statement is supplied by the renderer.

The CLI puts detailed methods, role cards and complete transcripts in a separate
evidence companion; findings link to its exact turns. You supply the concise
summary, synthesized findings, limitations and next steps. Keep the simulation
notice and relevant uncertainty, without repeating the same caveat in every
sentence. This release's interview conclusions are one input to the broader
research workbench; don't fabricate social or competitor research not performed.

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
