# Engineering impact and executive evidence

## Primary outcome: net engineering hours saved

Per workflow class, use `N * (manual_active_minutes - AI_active_minutes - incremental_review_minutes - incremental_rework_minutes) / 60`, adjusted for tasks still requiring manual work. Estimate confidence intervals where viable. Report total case volumes, eligible percentage, adoption, user mix, quality changes, error costs and maintenance labor.

## Experiment

Before experimentation, select the opportunity using the decision protocol below. Prefer
the best supported net-value opportunity that can be operated with available staff; high
gross hours or an impressive demo alone do not establish ROI.

Prefer crossover of comparable work across participating engineers: manual baseline for controlled cases, AI-assisted for matched cases, alternate order to reduce learning effects. Capture active labor not elapsed calendar time; separate model latency and human wait. Log exceptions and exclusions. Avoid using confidential event samples in external publicity.

## Opportunity selection across fields

Compare a small candidate set with the same decision horizon, including doing nothing and
a deterministic/no-model improvement. Fill `templates/CHARTER.md`; label each input measured,
estimated or unknown with source/date. Do not convert unknowns into favorable scores.

| Decision input | Evidence to collect |
|---|---|
| Business outcome | Active labor, elapsed lead time, defect/rework rate, yield/throughput or service quality; baseline and accountable owner |
| Eligible demand | Actual task volume, qualifying fraction and observed/estimated adoption, not total employee headcount |
| Feasibility | Approved data access, source revisions/IDs, validators, usable interface and available operator |
| Net benefit | Assisted labor plus incremental review/rework, recurring support and infrastructure; confidence range |
| Downside | Consequence of wrong answer, leakage, stale evidence, outage and operator departure; deterministic acceptance/stop criteria |
| Time to evidence | Smallest reversible experiment, effort cap, reviewer and date for go/no-go |
| Transfer | Shared stable contract and a second plausible workflow; do not count unobserved reuse as realized value |

First gate on authorization, safety, truthful evidence and support ownership. Among feasible
candidates compare conservative net benefit, time to evidence and maintenance burden; record
why the chosen option beats the simpler alternative. If uncertainty changes the ranking,
run the cheapest discriminating measurement. Learning value selects an exercise or breaks
a close tie; it does not justify an unneeded production feature.

The hours formula above measures labor benefit. To estimate monetary ROI, use a stated
horizon and an owner-approved value basis: `(benefit - cost) / cost` when cost > 0. State
whether labor time is capacity released or actual cash savings. Include build/integration,
run, support and retirement costs; count review/rework once, either netted from benefit or
as cost. Report ranges and break-even assumptions. For zero/unknown cost, report net benefit
or unknown ROI rather than dividing or inventing precision. Do not monetize defect/yield
benefits without validated attribution, or add them to labor savings if they overlap.

## Organizations with limited internal tooling

Start with the systems and support capacity the team actually has. An approved versioned
export plus a local read-only analysis can establish value before a live connector; record
snapshot age, missing data and permission scope. No API does not justify scraping a private
system, shared credentials or weakening access controls. Shared employee services still
require real identity/authorization and a named operator before rollout.

Prefer one supported deployment path, explicit manual refresh/recovery and existing UI
integration over a new platform. Budget installation, training, access requests, correction,
support and handover. If no one can operate it, keep it an experiment or stop. A manual
fallback and a portable export of approved results reduce dependence on one engineer.

Synthetic semiconductor examples to evaluate, not asserted benefits: finding a validator
for one parameter, reconciling approved report revisions, preparing a cited investigation
summary. Compare each against better search/scripts/templates before choosing an agent.
Yield, scrap, process-window and equipment decisions need domain validation and existing
company controls; a faster generated answer does not prove production improvement.

Reuse the same decision table in other fields by changing the task, source owner, error
consequence and business measure. Preserve the engineering and authorization contracts.

## Quality / leadership

Track audit completeness, invalid draft rejection, critical citation accuracy, production incidents attributable to automation, user satisfaction with limitations, maintainability and cross-team reuse. Obtain actual company award criteria and sponsor; don't presume a President's Award is inevitable.

## Story to executives

**Baseline evidence** → **engineering solution** → **independent quality verification** → **net value with methodology** → **sustainable cross-team ownership**. Quarterly review with sponsor, engineering owner and security/operations stakeholders. Never annualize pilot hours without documenting usage and uncertainty.
