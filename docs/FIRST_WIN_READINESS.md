# Engineering Readiness and First-Win Report — 2026-10-29

**Decision: local synthetic proof only. No real manufacturing win, independent signoff,
employee adoption or independently demonstrated human mastery has been established.**
Integration note: on 2026-10-29 the user explicitly authorized merging to main. This
dated report retains its pre-integration audit state; that authorization does not establish
independent signoff, operational approval or production readiness.

Working code and executed counterexamples now replace several specification-only gaps.
Do not merge, deploy or substitute company sources without required review/authorization.

## 1. Exact audited state and reproduction

Initial checkout: clean `codex/technical-handbook`,
`9591fb1266299fa6168615a3d8210bb0bb6c6874` (PR #3 open/unmerged).
Fetched remote main: `04c37fb517a0d288822ef9ea12e6e29ea6cb10c4`, version `2.0.0`
proposed/unreleased. Existing PRs #1/#2 merged. No main/handbook history rewritten.
Implementation branches start from main; the handbook remains a separate review.
First bounded correction: `eafc134` / PR #4, then the stacked synthetic-pilot increment.
Executable source verified at clean commit `5e757cb489ea3c45bc56c064f1d6f9ede35e18d9`.
Later evidence-only commits preserve those executable bytes; final PR head and per-file
SHA256s are recorded in the evidence. Code identity is not inferred from the version number. No release tag is created.

Environment: macOS 26.6.2 arm64, Python 3.11.7 (Clang 14.0.6). No packages installed.
Runtime/reference checks use Python standard library. Author-only browser QA uses the
already installed Chrome and Playwright; it is not an app dependency or independent review.
Tracked file inventory/byte hashes were captured in `out/first-win/audit-inventory.json`.
Reviewed implementation, tests, commands/skills, CI, canonical contracts/security/governance,
evaluation/training and application boundaries. Inventory is not a security certification.

Commands executed (shell runs prefixed with local `rtk proxy`):

```text
python scripts/offline_preflight.py                  # initial main: 51 tests, no failures/skips
python -m unittest discover -s tests -v              # implementation: 79 tests, no failures/skips
python -m scripts.evaluate_investigation --repeats 5 # 32/32 development self-checks
python scripts/verify_standard.py                   # PASS
git diff --check                                   # PASS
PYTHONPATH=. python out/first-win/browser-smoke.py    # author-only automation; 20 positive journeys
```

Frozen records: [verification](evidence/first-win/verification.json),
[development comparison](evidence/first-win/investigation-evaluation.json) and
[browser automation](evidence/first-win/browser-smoke.json). These are author observations.

The preflight also runs the original seven retrieval cases, 30 public domain cases, change
demo and tool-policy trace demo. Original tests preserved. Cold packet and snapshot results
are linked from the PR; raw logs and data hashes allow rerun rather than trusting test names.
The browser harness initially failed because its string-eval wait violated the app's CSP;
the harness switched to locator assertions without loosening CSP. This was a QA-harness
failure, not a suppressed application pass. No company integrations were attempted.

## 2. Capability classification

No capability is claimed **implemented and independently verified** by an accountable
external engineer/human in this session. CI is useful separate execution, not domain signoff.

| Consequential capability | Classification and evidence |
|---|---|
| No-overwrite retrofit, publication/transfer integrity, valid input regressions | Implemented but not independently verified; existing installer/manifest/offline tests rerun |
| Legacy lexical search / role filter | Synthetic demonstration only; caller roles are not identity and revisions are not selected |
| ChangeRun validation/review/export | Synthetic demonstration only; ordinary mutation guarded, public fields and caller review remain bypassable |
| Tool definition/scope/classification gate | Synthetic demonstration only; strict malformed-input fixes; no live MCP enrollment/client |
| Revision-aware source references and static dependency closure | Synthetic demonstration only; two hash-pinned Python modules; missing/dynamic edges explicit |
| Browser employee-style journey and local supervisor | Synthetic demonstration only; read-only loopback UI, SQLite admission/dedupe/cancel/stop/recovery; no employee auth |
| Production request/evidence/approval contracts; model context rules | Documented specification only; full envelopes, signed approval and enterprise adapters absent |
| Real SSO/source ACL, remote-effect reconciliation, protected audit, 200-user support | Missing enterprise implementation |
| Protected independent domain evaluation, calibrated expert/model grading | Missing; public author-generated labels cannot substitute |
| Real value/adoption and unaided mastery | Missing evidence; no participants or completed assessments |

## 3. Ten adversarial findings, ordered by consequence

See the canonical [risk register](SECURITY_THREAT_MODEL.md#synthetic-investigation-risk-register)
for each trust boundary, responsible role, preventive/detective controls, evidence, status,
residual risk, deployment decision and NIST GOVERN/MAP/MEASURE/MANAGE coverage.
Severity reflects misuse in company work, not actual production exposure.

| Finding | Falsification / disposition |
|---|---|
| Critical R1: role/identity forgery | Caller can assert a privileged role in legacy search. Reproduced, preserved as a boundary counterexample; no shared deployment |
| High R2: reviewer/hash authority | Caller can name another reviewer and recompute all mutable hashes before export. Reproduced known toy limit; no approved executor |
| High R3: stale revision | Legacy index returns r1/r2 together. Reproduced. New pilot requires explicit snapshot and rejects byte drift; deployment revision still unknown |
| High R4: malformed scopes and retry races | `not-evidence:read` string satisfied scope membership; role string became character grants. Both reproduced and fixed. New local dedupe/race tests do not prove remote idempotency |
| High R5: stop, cancel and uncertain outcomes | Separate process stops while a read is held; late result stays canceled across recovery. Crash leaves reconcilable intent. Cancel/publish race has one terminal outcome. Real remote reconciliation absent |
| High R6: tool drift | Mutated descriptions/version/nested schemas rejected by full-definition pin; real server trust and enrollment unverified |
| High R7: model/data exposure | Browser automation observes loopback-only requests; source injection stays quoted data. No model exists here, so no model injection-resistance claim |
| High R8: dependency/claim completeness | Missing external function and runtime dispatch stay unknown; cycles terminate in traversal; duplicate/nested definitions and budget edges challenged. Static graph still cannot prove runtime impact |
| High R9: evaluation false confidence | Legacy hit metric passes while recall is 0.5. New grader rejects wrong revision, missing citation and fabricated edge. Labels are still public/author-generated, not independent |
| Medium R10: value/support assumption | No actual frequency, active time, eligible-user count or operator assigned. Benefits cannot be extrapolated from headcount |

During implementation a duplicate worker initially could cancel the winning worker after
losing its claim. This was corrected and a blocking-reader regression now verifies one
read/result. It was a development defect, not an existing-v1 finding. No independent
human or cold separate-model signoff is fabricated; the separate cold packet requests it.

## 4. Emergency-stop readiness

The [operator drill](../examples/manufacturing/README.md#externally-controlled-stop-drill)
is executable in another process. Admissions and publication are enforced by the host,
not prompts. Stop atomically disables the capability, increments epoch, cancels pending
work and preserves uncertain read intents. An observed return is recorded separately.
Inventory identifies operation IDs, tools, intended source/system/hashes and result artifacts.
Recovery requires operator capability, exact epoch and reconciliation of unknown operations.

**Ready for a local synthetic read-only drill. Not ready for corporate incident response.**
Already admitted filesystem reads can complete; canceled output is fenced, not rolled back.
The control file/DB depend on OS access, Windows ACL hardening is unverified, evidence is
mutable local SQLite, and distributed adapters, revocation propagation and protected audit
are not implemented. A real external action would require authoritative operation status,
scope inventory and existing incident/change controls before resumption.

## 5. Selected first-win experiment and comparison

Problem: investigate how one parameter travels through defaults, parsing, validation,
overrides, dispatch and downstream interfaces at an exact revision. Synthetic `sample_count`
r1/r2 includes a changed default/bound, per-run override, ambiguous handler mapping and
missing external normalization source. These values have no manufacturing authority.

| Approach | Evidence / decision |
|---|---|
| A manual investigation | Real baseline not observed. Must measure expert active reading, verification and rework; keep this fallback |
| B literal search / static analysis | Literal search is the simplest locator baseline. Bounded AST closure improves indirect toy locator coverage; selected as the working candidate |
| C bounded AI-assisted investigation | Runtime model not run: no approved endpoint or proven incremental need. AI assisted the engineering, not source execution. Add a bounded model only if frozen paired trials beat B after review/rework/cost |

B wins only on the observed synthetic locator criterion below. It has **not** beaten manual
work or shown the highest organizational ROI. This workflow is the cheapest available
discriminating experiment, selected from the default mission and data-access constraints.
No vector DB/framework/swarm or external system was added. See [ADR-0003](adr/0003-bounded-synthetic-investigation.md).

Observed development run (32 cases, eight positive dependency cases, five timing repeats):

| Measure | Literal baseline | Static candidate |
|---|---|---|
| Mean required-function locator recall, 8 positive author-labeled cases | 0.1994 | 1.0000 |
| Exact expected status/nodes/edges/unknowns + source bindings | Not an answer-producing baseline | 32/32 public development self-checks |
| Positive lookup p50 / p95, 40 local timing samples | 0.2765 / 0.3128 ms | 0.2238 / 0.3235 ms |
| Runtime model/external calls | 0 / 0 | 0 / 0 |
| Human active minutes, total costs, independent accuracy | Unmeasured | Unmeasured |

Timing is median / nearest-rank p95 over a tiny warm-filesystem corpus, including trusted
authorization/read/parse, excluding UI and verification. Fixed candidate-then-baseline
order can bias cache timing; no speed superiority claim. Repeats are not new tasks.
Browser automation separately completed 20 alternating r1/r2 journeys, with click-to-render
p50 47.936ms/p95 59.567ms (includes automation/polling overhead). This is not a load test
or observed employee usability. Download/unavailable/stop paths succeeded, no page errors
or external requests. Source/hash binding is checked, not independent semantic correctness.

## 6. What must happen internally before claiming a win

Keep all internal sources/labels/trials/feedback in authorized company systems. Assign a
source owner to freeze one bounded approved snapshot and verify parameter-to-root mappings
and language limitations. Reuse existing company UI/identity/ACL/support infrastructure;
do not expose this local server to 200 people or silently swap proprietary code into it.

An independent evaluation owner targets **40 representative domain cases** (adjust 30–50
to approved evidence), with 20 development and 20 protected cases created after the adapter
freezes. The holdout/custodian/labels remain outside author/agent/public context. Include
wrong revisions, overrides, missing/ambiguous dependencies, denied access, source outages,
adversarial content and failure recovery. Two domain experts blindly calibrate/adjudicate
labels under the existing [evaluation protocol](QUALITY_AND_EVALUATIONS.md). These cases
and calibration do not exist yet; the 32 public toy cases are not a substitute.

Predeclare paired manual/B/C crossover tasks and quality/latency thresholds before trials.
Counterbalance order, track task complexity and all exclusions. Observe exact-revision and
claim correctness, missing/incorrect dependencies, unsupported claims/abstentions, failures,
active investigation + verification + rework minutes, help requests, tool/model usage and
cost basis. Critical leaks/unsafe actions block promotion regardless of averages. A proposed
local target is zero wrong-revision/unsupported critical conclusions and all known critical
dependency omissions detected; sponsor/domain owners must approve actual targets.

Frequency, eligible fraction, reuse, training, build/integration/support/retirement cost are
unknown. Use the canonical [impact calculation](IMPACT_AND_EXECUTIVE_RECOGNITION.md) and
report capacity released separately from cash savings. Deduct review/rework once and recurring
support. Approximately 200 personnel is a possible population, never 200 assumed adopters.

## 7. Adoption roles and next gate

| Required role | Assigned person / current state | Required next evidence |
|---|---|---|
| Business sponsor | UNASSIGNED | Authorized problem, demand and stop/promotion thresholds |
| Technical owner | UNASSIGNED; implementation here is AI-assisted | Internal adapter/interface ownership and alternatives defense |
| Source/data owner | UNASSIGNED | Approved bounded snapshot, revision and source-access mapping |
| Security reviewer | UNASSIGNED | Real identity/ACL/data-route and stop/recovery review |
| Evaluation owner | UNASSIGNED, independent of implementation | Protected cases, labels/calibration and frozen trial protocol |
| Operational support owner | UNASSIGNED | Support hours, incident/retention/manual recovery ownership |
| Pilot participants | NONE enrolled | 5–10 authorized opt-in engineers after gates pass |

Next gate: **independent expert verification of the synthetic implementation**, followed by
an authorized single-user internal proof. No internal promotion is currently authorized.
Then use Single-user proof → Independent expert verification → Narrow team pilot → Measured
benefit → Cross-team reuse, instantiating existing [delivery gates](PRODUCT_DELIVERY.md).
The early synthetic review does not replace independent verification of the internal adapter.

During the 5–10-person pilot, an observer records task completion without developer help,
confusion, failure, help, corrections, active time, repeat use and willingness to reuse.
No such observation has occurred. Promote only after frozen quality gates, conservative
net benefit and operator/sponsor acceptance; scale eligibility gradually, then validate one
second team independently before broader reuse. Do not promote because this demo runs.

## 8. Engineering mastery and cold review

The [resolver exercise](../academy/REVISION_RESOLVER_EXERCISE.md) requires unaided code,
new unseen cases, an examiner-injected bug, alternatives/complexity/failure defense and
human scoring using the existing 0–4 rubric. Retest +2/+7/+30 days after actual assessment.
All personal ability, completion dates and human scores remain unassessed. Its defense
record separates assisted implementation from what the learner can independently reproduce.

A cold source packet excludes this report, PR discussion and ADR-0003 rationale. Give it
to a separately approved session/model and accountable human; do not include author chat
history or private labels. Record reviewer identity/model/version, packet hash, exact source,
commands/findings, scope and unresolved risks. A separate AI check still cannot authenticate
human reviewer independence, approve release or grade unaided human performance.

## 9. Exact next three actions

1. **Independent cold reproduction and expert review.** Highest immediate risk reduction,
   low setup cost; reviewer scheduling unknown. Review the bounded fixes first, then the
   pilot. Exit: reproducible findings against exact hashes and human disposition; no merge yet.
2. **One authorized internal baseline/curation session.** Highest expected information/ROI
   value; authorization and participant availability are blockers. Assign sponsor/source/
   evaluation owners, time manual vs deterministic investigation on a bounded snapshot and
   freeze independent case protocol. Exit: actual labor/quality/demand evidence deciding
   whether this workflow and any model deserve further work.
3. **Unaided resolver assessment, then gated opt-in pilot preparation.** High learning value;
   no operational benefit assumed. Complete human-observed implementation/debug/defense and
   schedule recall. Only after internal proof/security/expert gates, enroll 5–10 users with
   named support and observed task sessions. Exit: assessed skill evidence and a reviewable
   go/no-go for team use, not automatic rollout.
