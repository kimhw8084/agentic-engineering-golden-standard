# Migration from 1.0.0 to 2.0.0

v2 remains an L1 teaching/reference template. No persistent service data migration.
Save target work/commit, read `V1_GAP_MATRIX.md` and `GOVERNANCE.md`, run original checks.
Preserve config, customized skills, code and tests. Review commits in order: P0 integrity,
P1 contracts/evaluation, P2 publication/delivery. ADRs are Proposed until independent review.

Template users pull reviewed commit and run full gate. Brownfield users dry-run retrofit
and reconcile collisions manually; a skip is not an upgrade. Installer copies guidance,
not Python fixes/tests. Assign people to owners and configure required PR checks.
No merge, tag, deployment or production permission is implied.

| Change | Consumer action |
|---|---|
| review requires literal True + nonblank string | Remove truthy strings/integers; review remains an unverified caller assertion |
| Hash checks at every gate; serialize before state change | Use set_draft/revalidate after edits; no retry guarantee |
| Exact ID tokens; bool/float top_k rejected | Remove substring/invalid-type dependencies |
| Canonical JSON rejects NaN/infinity | Finite valid JSON only; encoding is not RFC8785 canonicalization |
| Retrofit skip-symlink | Inspect redirected paths; existing files preserved |
| MRR excludes empty-label cases; nullable recall/precision/abstention split | Recompute same-denominator baseline; hit_at_k retains legacy combined rate |
| Empty/duplicate/missing/invisible labels rejected | Correct fixtures; repeats are timing, not model trials |
| Target runtime contracts 2.0 | Consumers implement schema/auth/store; docs are not enterprise APIs |
| Skill manifest | Pin supporting files to same commit; manual target reconciliation required |

Rollback: revert bounded commits, restore reviewed skill publication, rerun checks. No
external effects here. Consumers with persisted state need their own migration and
cancel/reconciliation tests. Exercise/defense: `academy/V2_INTEGRITY_EXERCISE.md`; neither
has been demonstrated by the user in this session. Human review precedes release tagging.
