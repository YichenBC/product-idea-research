# Construct roles and interview them

## Interpret the user's method

Separate the research question from the concept being tested. Translate the
chosen method into named dimensions, explicit allowed values, constraints and
the requested role count. Do not expand every combination unless requested.
For example, “frontline vs approver, stable vs changing timetable” may need four
combinations, or just two contrasting roles if that is what the user asked for.
Include a satisfied user or a rejection case when it serves the research question;
do not manufacture negativity solely to fill a slot.

If the user supplies a concept without a method, state a compact coverage choice
such as “compare the person doing the task with the person approving a change.”
The choice is a scenario assumption, not a statement about the actual market.
Works for household, hobby, consumer and organizational contexts. Do not invent
business budgets for consumer roles or infer demographic traits from language.

## Role cards

Give each role an inspectable label. Traits use the recipe's dimensions. Attributes
describe task, current workflow, desired outcome, authority, constraints, current
alternative, acceptance/rejection conditions and unknowns as relevant. More fields
are not automatically better. Include only attributes that change the discussion.

Every attribute in v0.1 is `assumed` or `unknown`, with an explanation of why it
was included. Do not decorate cards with fabricated age, biography or purchasing
history. If the user supplies grounded material, this release can rehearse a
scenario informed by it, but cannot record that as a verified persona database.
State this limit rather than silently relabeling source evidence as a fact.

Before interviewing, check:

- All requested roles/dimensions are covered, or missing combinations are disclosed.
- The person's authority, constraints and workflow are compatible.
- Cards differ in decision-relevant ways, not just name or tone.
- The proposed tool is not assumed to be needed by everyone.

## Interview protocol

The same Agent may take interviewer and respondent turns. Separate their voices
in the structured transcript; no subagent, extra model, persona service or network
is required. Multiple synthetic respondents are not independent empirical samples.

Start with a concrete task under the card's assumptions. Follow up on what the
answer actually says. A useful sequence is current workflow → breakdown or
sufficiency → trade-off → rejection threshold → real-world question to investigate.
Adapt this to the user's method rather than forcing a questionnaire.

Ask neutral questions. “How would you handle a last-minute change?” is better than
“Would our AI save you hours?” Allow “the current solution is fine” and “unknown.”
If a question calls for historical usage, actual spending or a measured quantity
not provided, say that the simulation does not establish it. New scenario details
go in that turn's `assumptions`, not disguised as past experience.

Prefer conditional answers (“in this scenario, I would…”) over invented testimony.
When a role changes its stance, the follow-up should expose why; do not quietly
change its authority or constraints. Preserve counterarguments in the transcript.

## Example user methods

- “Compare a solo shop owner and a supervisor who needs approval; two roles.”
- “Use jobs-to-be-done questions for three types of travelers; no demographics.”
- “Use these two role descriptions exactly, and challenge our onboarding idea.”
- “Only create the personas for now.” → save the recipe and cards, then stop.

User scope wins over finishing every workflow step. A checkpoint is a valid
deliverable, and later messages can continue to interviews or reports.
