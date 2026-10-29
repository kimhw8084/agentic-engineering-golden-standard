# Engineering Mastery Academy — learn through shipping

**Objective:** become capable of independently designing, coding, evaluating, debugging and defending high-value backend/AI platform systems using ongoing projects as the laboratory. This is not a credential or PhD-equivalent qualification.

## Eight conceptual modules

| Order | Lecture | Project work and independent laboratory |
|---|---|---|
| 1 | `01-algorithms.md` | Exact source lookup, complexity, ranking and graph traversal |
| 2 | `02-backend-and-databases.md` | Typed API, transactions, constraints and versioned source data |
| 3 | `03-distributed-systems.md` | Retries, idempotency, consistency, concurrency, event ordering |
| 4 | `04-retrieval-science.md` | Tokenization, BM25, ANN, embedding tradeoffs, recall/MRR/nDCG |
| 5 | `05-agents-and-context.md` | Agent control loop, bounded tools, state machines, context budgets |
| 6 | `06-testing-and-experimentation.md` | Ground truth, adversarial eval, scientific comparison, performance |
| 7 | `07-security-and-reliability.md` | Authentication, authorization, isolation, threat models, SLOs |
| 8 | `08-staff-architecture-and-impact.md` | ADRs, platform leverage, evidence-driven leadership, interviews |

**Work-integrated cadence:** For each actual change, choose one relevant lecture; spend 15 minutes on principles, 20–60 minutes on an unaided code/debug exercise, 10 minutes defending the tradeoff, then document objective evidence. A 12-month path is in `LEARNING_PATH.md`.

## Mastery rubric

- **0: Not assessed** — no evidence.
- **1: Conceptual** — explains with prompts/notes, cannot implement or debug independently.
- **2: Assisted** — codes and validates using AI; cannot reproduce independently yet.
- **3: Independent** — implements/debugs correctly unaided; passes adversarial tests and architecture defense.
- **4: Production and leadership** — independently owns real release/support, measures impact and explains tradeoffs under expert challenge.

A 4 is not a certification, hiring guarantee, academic degree or universal evaluation of seniority. Do not grade yourself based only on an agent's praise.

## Continuous interview readiness

Maintain `templates/READINESS_SNAPSHOT.md` as a dated evidence index, not a self-awarded
credential. Readiness is specific to a role family, level and interview format. The shared
core is coding, debugging, software/system design, agent/retrieval/evaluation judgment,
security/reliability and clear evidence-based communication. Keep breadth visible while
deepening one role-specific gap at a time; years on a calendar are not evidence.

| Reference role family | Existing foundation | Additional evidence to demonstrate |
|---|---|---|
| Applied agent / product engineer | Modules 01/02/04/05/06 | Independently implement a bounded workflow, evaluate answer quality and defend employee experience |
| Agent platform / backend engineer | Modules 01/02/03/05/07 | Concurrency, durable retries/cancel, API contracts, sandbox/resource boundaries and bottleneck diagnosis |
| Retrieval / evaluation engineer | Modules 04/06 | Ground truth, metric counterexamples, holdout contamination, judge calibration and uncertainty analysis |
| Reliability / security engineer | Modules 03/07 | Fault/abuse diagnosis, scope enforcement, recovery, incident evidence and operational tradeoffs |
| Architect / technical lead | Modules 02/03/07/08 | Defend alternatives, ownership, cost/value, migration and multi-team adoption under constraints |

These are local reference tracks, not exhaustive job requirements. Before a specific
interview, date and map the actual job description to observed evidence and missing skills.
Model training/research, ML math, distributed accelerator systems and specialist domains
may require substantial study beyond this academy. For example, the official
[Agent Infrastructure role](https://openai.com/careers/software-engineer-agent-infrastructure-san-francisco/)
describes training-scale systems and virtualization expertise (checked 2026-10-28); this
template's agent examples alone cannot demonstrate that depth.

After each meaningful change, update the relevant competency with an unaided implementation
or debug result, an architecture defense and a synthetic example outside the original
domain. Use the existing 0–4 rubric; record assessor, date, hints, failed cases and artifact
revision. AI-generated practice/results are assisted; only observed human performance
supports independent mastery. Stale evidence retains history but needs reassessment.

Suggested maintenance cadence: one short mixed-topic explanation/debug drill each week,
one unseen timed coding/system-design assessment monthly, plus day 2/7/30 recall after
new learning. These are local practice defaults, not validated guarantees. Before an
interview, produce a 90-second project explanation, a five-minute tradeoff/failure defense,
one executable unaided artifact and one source-approved impact story. If evidence is
missing, mark the gap and select the next exercise; never average away a critical gap.

Select a fresh transfer variant from `INTERVIEW_BANK.md`; a reviewer should add an unseen
failure case rather than repeat a memorized answer. Keep generated worked solutions
separate from unaided assessment. The learner's ability is unassessed until demonstrated.

## Every mastery record must contain

A precise concept, implementation evidence, tests you ran, edge case debugged, complexity/failure analysis, architecture tradeoff, answer to three tough questions, and a reinforcement task scheduled for a later sprint. Template: `templates/MASTERY_RECORD.md`.

## Suggested external courses

MIT 6.006 algorithms, CMU 15-445 databases, Stanford CS144 networking, Google SRE workbook and OpenTelemetry/OWASP/NIST engineering resources. Links in `docs/REFERENCES.md`.
