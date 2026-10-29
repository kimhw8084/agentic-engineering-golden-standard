# Revision-aware parameter investigation: synthetic pilot

This is a working, local study fixture for Manufacturing System Intelligence. It accepts
only two bundled synthetic Python snapshots. It cannot ingest company code, connect a
model, query equipment or modify a recipe. Keep company implementations in separately
authorized internal repositories. Status: **VERIFIED IN FIXTURES; independent review pending**.

## Use it

On Windows, after an operator provisions approved Python 3.11+ and reviews this snapshot,
double-click `START_SYNTHETIC_PILOT.cmd` at the repository root. A local browser opens.
Choose r1/r2 and a parameter, click Investigate, open source excerpts, inspect unresolved
dependencies and save the result or feedback. No prompts, Git or terminal commands are
required in the employee journey. Python provisioning and launcher execution on the actual
work PC remain unverified. Closing the server stops the pilot; restart never silently
resumes interrupted work. This is one local synthetic session, not a shared employee service.

Operator/author alternative: `python -m scripts.investigation_app`. Keep the server window
open. It binds only 127.0.0.1 on an assigned port. Remote binding is not configurable.
Do not expose it through a proxy. Do not add credentials or company data to the workspace.

## What it answers

The curated manifest maps an exact parameter to a root function at a hash-pinned snapshot.
The resolver parses Python AST without importing/executing source and traverses reachable
syntactic local calls. Every node/edge cites path, snapshot, full byte SHA256 and exact lines.
It enumerates potential calls, including branches that may not execute; it does **not**
prove runtime data flow, effective values, equipment effects or completeness beyond the
curated module. `supported` means supported static closure within this restricted grammar.
Even an all-static cycle does not prove termination. No automatic corpus discovery or cache.

| Input | Observable result |
|---|---|
| sample_count / r1 | Default/parser/override/validator/dispatch excerpts; unknown runtime handler |
| sample_count / r2 | Changed default/bound and added normalization; missing external source remains explicit |
| exposure_ms | Complete local static call closure in this specimen |
| cycle_count | Traversal terminates on two-node cycle; runtime termination not asserted |
| missing_count | Partial result naming the missing function |
| restricted_gain | Denied before reading a source snapshot |
| Unknown parameter / revision | Abstained / unavailable; no invented dependency or implicit latest revision |

The manifest mapping/labels are author-generated. Source-owner verification is pending.
Hashes bind bytes to a trusted manifest; they do not authenticate a maliciously replaced
manifest. Source excerpts are untrusted text rendered through `textContent`, not HTML or
instructions. No source text goes to a model or external service.

## Externally controlled stop drill

The operator capability is provisioned locally in `workspace/pilot-operator.key`; only its
hash is in SQLite. It is not in browser responses, requests, model context or telemetry.
The browser capability cannot administer the supervisor. OS ownership is the trust root:
someone who can read the operator key or edit the DB can bypass controls. POSIX creation
uses mode 0600; Windows ACL hardening is **not implemented/verified**. Never share this
prototype as an employee-authenticated service.

In a separate operator process at the repository root:

```text
python -m scripts.pilot_control stop --reason "synthetic drill"
python -m scripts.pilot_control inventory
```

The transaction disables the sole read capability, increments the epoch, cancels queued/
running jobs and marks admitted in-flight reads uncertain. Inventory lists operation IDs,
tool, intended system/path/source hash, terminal/uncertain state, artifact hashes and event
sequence. A `read_returned` event distinguishes a returned read from an admitted intent.
Failed reads may have opened a source: treat their scope conservatively. No external
systems/tools are involved. State and events commit together; SQLite is mutable local
evidence, not a protected/signed audit sink. Archive under approved retention before local
cleanup; no automatic deletion or upload is performed.

Read admission is the linearization point. An already admitted OS read may finish after
stop; there is no claim to preempt filesystem I/O or undo disclosed bytes. Workers check
before/after reads and fence result publication against cancellation, deadline and epoch.
Late results cannot restore canceled work even after authorized recovery. The ten-second
deadline is checked at gates, not a hard process timeout. Two workers, 16 pending jobs,
one source read/job, 100KB source and 64 graph nodes bound this fixture.

If inventory shows `unknown`, an operator must inspect each operation and establish the
read-only scope. For this fixture only, acknowledge it by ID, then recover against the exact
epoch reported in inventory:

```text
python -m scripts.pilot_control reconcile --operation OPERATION_ID --reason "verified bundled local read only"
python -m scripts.pilot_control resume --epoch EPOCH_NUMBER --reason "operator reviewed scope and source integrity"
```

Recovery re-enables only the one synthetic read capability. Old jobs remain terminal;
create a new request to investigate again. Same owner/key/input replays the stored job;
different input conflicts. No retry of remote effects exists. If DB/policy access fails,
the app fails closed. Reconciliation for a real remote operation would require its trusted
adapter/operation status and a separate authorized process; this fixture cannot provide it.
Browser capability/owner rotate on server restart; old jobs remain in operator inventory,
but the new browser session cannot resume or retrieve them. Dedupe is scoped to the
trusted synthetic session/key, not durable employee identity.

## Reproduce

```text
python scripts/offline_preflight.py
python -m scripts.evaluate_investigation --repeats 5
```

The 32 visible cases are development self-checks; eight contain positive dependency labels.
They are neither independently labeled nor a protected holdout. Fault cases simulate
missing/tampered sources; integration tests also inject actual read failures, a process
crash, separate-process stop, races, rejected recovery and late completion.
The literal-search comparison measures locator coverage, not answer quality or human time.
Repeated deterministic trials measure timing only. Raw local results go to ignored `out/`.
Do not place internal cases, user observations or evaluation records in public commits.

Adoption/measurement gates and observed limits: [readiness report](../../docs/FIRST_WIN_READINESS.md).
Mastery: [unaided resolver exercise](../../academy/REVISION_RESOLVER_EXERCISE.md).
