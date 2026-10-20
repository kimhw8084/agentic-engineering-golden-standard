# Lecture 08 — Staff-level architecture, leadership and value engineering

## Staff engineering is leverage, not feature count
A higher-level engineer should produce systems that other teams can safely reuse, have a clear ownership model, improve decisions, and remain supportable after the original developer leaves. More abstract layers do not automatically mean more leverage. Prefer one narrow reusable contract over a universal framework without proven users.

## Tradeoffs as technical evidence
For a 1–3-person team, a modular monolith often reduces deployment, incident and operational overhead compared with distributed microservices. A graph database may help complex traversal workloads but a relational adjacency table can be simpler for early recipe/code relationships. Each architecture decision should identify a reversing signal: e.g., measured hot path or coordination bottleneck.

## Impact accounting
Use net active labor savings and quality changes. For N eligible cases/month, average manual active M minutes, assisted labor A, added review R and rework W, calculate `N*(M-A-R-W)/60` hours. Document how N was measured and whether the pilot group is representative. Scale to another fab group only after validating differences in permissions, integration contracts, process and support ownership.

## Governance and promotion/award evidence
Technical sponsors value reliable results, risk reduction, adoption and maintainability more than model novelty. Build quarterly review artifacts with actual baseline comparisons, verified source evidence, independent signoff, and evidence of other engineers successfully using the platform. Determine actual award criteria; never claim executive recognition or external hiring as guaranteed.

## Career interview translation
A strong narrative includes (a) hard problem, (b) your personal ownership, (c) architecture alternatives and tradeoffs, (d) tests, incident/reliability constraints, (e) measured business value, (f) what you would change. Synthetic public-safe reproductions can support technical depth without sharing proprietary information. Avoid conflating AI-generated implementations with personally demonstrated coding mastery.

## Independent lab
Write an ADR comparing two architecture variants of your real project. Build a one-page ROI experiment plan. Independently implement one critical data contract and defense test. Present a 10-minute mock staff-engineer design review where an interviewer asks about failure, load, isolation, cost, ownership and rollback. Record inaccuracies and a revision plan.

## Defense questions
What is the smallest primitive with multi-team reuse? How did you avoid false savings claims? What tradeoff did you reverse after observing production evidence? How does on-call ownership work? What critical code did you personally implement without AI?

**Mastery gate:** independently defend architecture and concrete results, with reviewer challenge and evidence—no credential shortcut.
