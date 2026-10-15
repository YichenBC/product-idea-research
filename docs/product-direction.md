# Research first, conclusions first

Research Workbench is intended to help a coding agent answer a research question
and deliver an actionable report. Simulated interviews are one method available
within that work, not the definition of the product.

The modular design allows starting from an idea, a competitor, public discussions,
provided materials or a user-defined interview method. Users can request one module
or a combination; a report should never invent unperformed research just to fill
sections.

| Module | Question it contributes to | Shipping status |
|---|---|---|
| Social research | What problems and alternatives appear in public discussions? | Planned |
| Competitor research | How do existing solutions work and where are their limits? | Planned |
| Supplied-material analysis | What does existing feedback or research support? | Planned |
| Simulated interviews | What assumptions, objections and trade-offs should be tested? | Implemented |

## Report contract

The main report answers the research question: conclusions, meaningful disagreement,
implications, actions and unresolved questions. It briefly discloses its scope and
evidence limits. It does not reproduce every step of the research process.

Detailed methods, role cards, transcripts and other source material belong in a
separate evidence companion. Links let readers inspect support without forcing
everyone to read the full interview. The current renderer implements this division
for simulated interviews; the other modules will contribute their own conclusions
and source types when implemented.

Synthetic material remains labeled as simulation even when summarized. A polished
report must not give hypothetical statements the status of real customer evidence.

## Design influence

Atypica's orchestration of research methods, personas and interviews informed the
design. During the earlier evaluation, final report generation did not complete,
so this project does not claim to reproduce an inspected Atypica report layout or
its proprietary persona data. This is an independent implementation of the
research workflow and the user's desired conclusion-first delivery.
