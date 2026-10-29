# First unaided assessment

Purpose: observe schema validation, reasoning about missing evidence, test/debug ability
and business judgment before a larger agent exercise. Suggested time: 45-60 minutes.
Use synthetic data only. Python standard-library docs are allowed; AI-generated solutions
are not. Record hints/time/failures honestly. No score has been assigned to the learner.

Create your own `workspace/my_solution.py` with `assess(case: dict) -> dict`. No scaffold
solution is provided. Run the visible checks with:

```powershell
py -3 academy/assessment/check_submission.py workspace/my_solution.py
```

You are explicitly executing your own Python code, not sandboxed third-party submissions.
Visible checks establish only the declared contract; a separate assessor adds an unseen
case and observes implementation/defense before independent-mastery scoring.

## Contract

Input has exactly these fields: `tasks_per_month`, `manual_minutes`, `assisted_minutes`,
`review_minutes`, `rework_minutes`, `support_minutes_per_month`, `build_minutes`.
Reject nonobjects, missing/extra fields, negative/nonfinite/nonnumeric values and booleans
with ValueError. `tasks_per_month` must be an integer. Any value may be None to mean unknown;
first validate every known field, then return only `{'status': 'insufficient_evidence'}`
when any field is unknown. Do not replace unknowns with zero.

For fully known inputs compute monthly net capacity minutes as tasks times
`(manual - assisted - review - rework)`, less monthly support. Review/rework are incremental
and excluded from assisted_minutes; this definition prevents double counting. Return exactly:
`status`, `net_minutes_per_month`, `break_even_months`. Status is `pilot_candidate` when net
is positive, otherwise `no_measured_benefit`. Break-even is build_minutes/net only when
net > 0, otherwise None. Finite int/float inputs are accepted except integer-only task count.
Reject nonfinite computed results too. A pilot_candidate is not deployment authorization.

Example: 40 tasks/month; manual 20, assisted 6, review 4, rework 2; support 120/month;
build 480. Expected net 200 minutes/month, break-even 2.4 months. These are invented inputs,
not measured savings. Negative first-month net is possible after build effort.

## Defense and transfer

Explain why None differs from zero, why bool needs attention in Python, why finite inputs
may still overflow, and which cost is counted where. Compare an approved read-only export,
simple search/script and a live tool-using agent. Name missing evidence and the operator.

Transfer: change the setting from a metrology investigation summary to maintenance-manual
search. Which algorithm/contracts stay the same, and which error consequences/approvals
must change? Assessor adds a new input or constraint; record actual outcome, not confidence.

Use the academy's canonical 0-4 rubric, observed code/test/defense evidence and a dated
readiness snapshot. Passing visible tests alone does not establish independent mastery.
Schedule day 2/7/30 recall. Next deeper exercise: `academy/V2_INTEGRITY_EXERCISE.md`.
