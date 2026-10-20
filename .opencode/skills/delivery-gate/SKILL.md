---
name: delivery-gate
description: Enforce test evidence, review, performance measurement, and rollback before a feature is called complete.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Delivery Gate

## Procedure
Follow `docs/DEFINITION_OF_DONE.md`. State precise acceptance criteria before changes. Execute local deterministic tests and negative cases; record command, exit status, failed scenarios, commit/revision and environment. Confirm permissions/secret handling and rollback. Compare baseline accuracy and latency where applicable. Never state `production ready` based on synthetic fixtures. Produce `Verified / Not Verified / Blocked` table and a one-sentence next task.
