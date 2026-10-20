---
name: evaluation-design
description: Design golden datasets, deterministic graders and domain-expert evaluations for agent accuracy and safety.
license: UNLICENSED
compatibility: opencode
metadata:
  opencode/slash: "true"
---
# Evaluation Design

## Procedure
Read `docs/QUALITY_AND_EVALUATIONS.md`. Define task distribution, dataset version, human ground truth, evidence references, source/time/ACL scopes, expected answers and forbidden claims. Separate source retrieval Recall@k/MRR from citation correctness, semantic answer judgments and action safety. Include stale revisions, ambiguity, abstentions, injection, unauthorized access, missing systems, timeout and concurrent actions. Freeze held-out cases. Implement reproducible runners and report uncertainty. Avoid self-grading as sole evidence.
