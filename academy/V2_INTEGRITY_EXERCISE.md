# Independent exercise — hash gates, state and retries

Time box 45–60 minutes; no AI-generated solution. Tied to v2 hash/state fixes. Human ability
is not assessed until observed; generated PR work is assisted.

Implement a SQLite transition store with standard library: request ID, actor, state version,
draft hash, validator revision, idempotency key. Two workers attempt validated → reviewed:
one transition, same-key/hash replay, conflicting payload rejection, crash/restart recovery.
Add cancel competing with handoff; late work cannot overwrite canceled state. Label identity
simulated. Demonstrate order/mutation/retry/race/cancel/restart tests to an independent examiner.
Explain transaction boundary, unique index, encoding, rollback and auth/audit gaps. Record
code/test output and complexity/failure reasoning with canonical rubric in `README.md` and
`templates/MASTERY_RECORD.md`; distinguish assisted vs unaided work.

Interview defense: approval commits but client times out; a second worker retries while
user cancels. Which result is authoritative? Prevent duplicate handoff; explain limits after
remote execution. Defend transaction/outbox against an in-memory lock and local hash chain.
Why do a hash and independent=True fail to authenticate reviewer independence?

Recall: day 2 reconstruct transitions unaided; day 7 debug a new retry/race; day 30 defend
design and reproduce key test. Record actual dates/results/gaps. External career evidence
requires source-owner/confidentiality approval; use synthetic code for this exercise.
