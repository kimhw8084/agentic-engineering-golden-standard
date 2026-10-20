# Start here — action plan

## A. Prove this template is intact (local; no network)

```bash
python scripts/verify_standard.py
python -m unittest discover -s tests -v
python -m scripts.evaluate_fixture
python -m scripts.change_demo
```

## B. Modernize projects already in progress (recommended)

1. Ensure you have company authorization, clean Git state, and a backup/snapshot.
2. Start with your **Manufacturing System Intelligence** repo, not a new autonomous application.
3. Run `python scripts/repo_audit.py /approved/path` (metadata-only, read-only).
4. Run `python scripts/retrofit.py /approved/path` (**dry-run**). Review all file paths and collisions.
5. Run `python scripts/retrofit.py /approved/path --apply` (**only after review**); it copies missing OpenCode helpers and supporting docs. It never overwrites existing files, source code or provider config.
6. Manually merge `templates/AGENTS_BROWNFIELD.md` into the existing project's `AGENTS.md`, respecting higher company policy.
7. In the **target repo** start OpenCode and use `/golden-audit` to analyze one explicitly approved source-code scope (no production writes or secrets).
8. Select first golden test: "How does synthetic/approved recipe parameter X flow through config, parser, validator and final system behavior?" Demand file/revision citations, verified call path and explicit unknowns.
9. Use `/golden-next` to choose one improvement, `/golden-build` to implement it, `/golden-eval` to verify, `/golden-master` to learn/defend.
10. Repeat in Work Intelligence repo, beginning with opt-in/approved subset of messages and per-user permission tests.

## C. Build new applications

Start from a copy of this repo, keep standard as shared base, add your application code in a separate package. Avoid making the toy `golden` implementation your production data/approval infrastructure. See `docs/ARCHITECTURE.md` and `docs/ROADMAP.md`.

## D. What to deliver to management at four weeks

A reproducible baseline, a verified small user benefit, exact quality/security tests performed, unknown or failed cases, architecture/ownership/rollback design, signed-off next stage proposal, and quantified human time saved *if measured*. No promises of immediate fab-wide deployment.

## E. What to deliver to yourself each week

One working feature, one independently solved engineering exercise, one design decision defended, one safely sanitized case-study entry. This is how hands-on work turns into Staff-level evidence over time.
