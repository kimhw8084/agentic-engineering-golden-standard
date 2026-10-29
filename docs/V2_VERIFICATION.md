# v2 verification record

Scope: synthetic, offline teaching/reference standard. Base `a655268`. Three bounded commits
cover P0 integrity, P1 contracts/evaluation and P2 delivery/publication. Independent human
review, ADR acceptance, release tag and merge are pending. This is not production readiness.

Run: 2026-10-29 00:46:36 UTC (2026-10-28 local), Python 3.11.7,
macOS 26.6.2 arm64. P0 commit `56522bb`; P1 commit `aa6dc42`; P2 was uncommitted
during the recorded local gate. PR commit/diff and CI bind the final revision; evaluator
results independently hash executable sources and fixtures. Synthetic logs are in local
ignored `out/v2/`, not published company artifacts. A clean committed-tree check follows
before PR publication. No model, remote source or production operation was invoked.

| Executed command | Result |
|---|---|
| `python scripts/verify_standard.py` | PASS, 0 issues (structure/frontmatter/version/skill manifest) |
| `python -m unittest discover -s tests -v` | 44 tests PASS, 0.062s; all 24 original tests unchanged |
| `python -m scripts.evaluate_fixture --min-hit 0.85` | 7/7; recall/MRR 1; precision 0.8; abstention 1; 0 simulated role leaks |
| `python -m scripts.evaluate_fixture --cases examples/fixtures/domain_cases.json --repeats 20 --min-hit 1.0` | 30/30; recall/MRR 1; precision 0.9167; abstention 1; 0 simulated role leaks; 600 timing samples |
| `python -m scripts.change_demo` | Local draft exported; review explicitly caller-attested |
| `python -m scripts.trace_demo` | 1 permitted policy decision, 4 denials; zero real invocations |
| `python -m scripts.skill_manifest` | PASS, 11 skill hashes/version match |
| `git diff --check` | PASS |

Additional inspection: all local Markdown links resolved; `AGENTS.md`, `opencode.json`,
and original test files have no diff. No dependency/framework/agent added. CI now runs the
domain seed and policy traces in addition to every original gate; remote CI status must be
read from the PR, not inferred from local success. Tests remain offline/no-network.

## Falsification and measurements

Ran the eight new P0 integrity checks against baseline modules in a temporary synthetic
tree: six failed (mutation at validation/review, serialization atomicity, strict review
assertion, ID substring, symlink escape), two existing behaviors passed (one-shot export,
repeat/config preservation). After fixes all eight pass. This is reproduced defect evidence,
not a claim of independent security review. Unit suite grows 24 → 44; test duration grows
0.017 → 0.062 seconds on local samples, with no runtime performance inference.

Paired retrieval timing: load `golden/retrieval.py` from `git show a655268:golden/retrieval.py`
and current module in one process; build one index each from the same six records; for each
of seven original cases run 100 sequential searches with k=3 and fixed roles. Measure only
search using perf_counter; median p50 and nearest-rank p95 over 700 samples per version.
Both versions: 7/7 hits/abstentions, p50 **0.0178 ms**, p95 **0.0198 ms**. No speed claim.
Single process, fixed order, tiny warm workload, no confidence interval or realistic load.

The final separate domain run measured p50 0.0180 ms / p95 0.0201 ms (600 queries); the
seven-case run p50 0.0191 ms / p95 0.0562 ms. These workloads differ and must not be used
as a before/after comparison. Model calls/tokens/billed cost and external tool calls: zero.
Local compute/labor cost, answer correctness, grounding, employee task success and business
minutes saved: unmeasured. Repeated deterministic queries are not independent model trials.

## Provenance

- Evidence SHA-256: `f2f0e9539c4bdd73e7f159484fa3800860908bd86aff80cdecfec47315ab5713`
- Original cases SHA-256: `17702dd363b8b2d55c0603735fc053ab72ddb68d783ed56f7ea24a81dee15041`
- Domain cases SHA-256: `566190dc9425bffc91e8a3fbc92b1a85b9525906160b9ec36c594cc2bf01f8f6`
- Unit log SHA-256: `cbb295aa647d45c9d851099cf8207ef9214aba68babf3a6a8a3af41a9a001c3e`
- Domain result log SHA-256: `333099a01475c25aee842c8471f84ca7448f71b3a0b38443b9f935430f7c4852`

Executable hashes are emitted in each evaluation JSON. `out/v2/summary.json` records exact
commands, exits, environment and artifact hashes. Hashes identify these artifacts; local
files are mutable and are not an integrity-protected audit system.

## Unresolved gates and next adoption

No production identity/ACL, durable retry/cancel store, signed approvals/audit, employee UI,
live MCP/model or source integrations. Runtime contracts are specifications; tool examples
only test deterministic policy boundaries. No protected fresh holdout, independently labeled
domain benchmark, repeated model trials or calibrated human/AI grading has been executed.
Those require a separate curator/approved endpoint; public fixture names cannot establish
independence. Human review, ownership assignment, branch protection and ADR acceptance are
pending. This author session cannot independently approve its own consequential claims.

Highest-value next task: the synthetic revision-pinned parameter-flow UI slice and measured
pilot specified in `PRODUCT_DELIVERY.md`. Unaided SQLite concurrency/retry exercise and
timeout/cancel interview defense: `academy/V2_INTEGRITY_EXERCISE.md`. Human competence remains
unassessed; career evidence publication requires appropriate confidentiality approval.

## Exact modified files

- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/workflows/quality.yml`
- `.opencode/agents/golden-auditor.md`
- `.opencode/agents/golden-reviewer.md`
- `.opencode/skills-manifest.json`
- `.opencode/skills/agent-workflow/SKILL.md`
- `.opencode/skills/engineering-mastery/SKILL.md`
- `.opencode/skills/security-review/SKILL.md`
- `CHANGELOG.md`
- `README.md`
- `academy/V2_INTEGRITY_EXERCISE.md`
- `docs/AGENT_PATTERNS.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTEXT_ENGINEERING.md`
- `docs/DEFINITION_OF_DONE.md`
- `docs/GLOSSARY.md`
- `docs/GOVERNANCE.md`
- `docs/MIGRATION_V2.md`
- `docs/PRODUCT_DELIVERY.md`
- `docs/QUALITY_AND_EVALUATIONS.md`
- `docs/REFERENCES.md`
- `docs/RUNTIME_CONTRACTS.md`
- `docs/SKILL_PUBLICATION.md`
- `docs/TOOL_TRUST.md`
- `docs/V1_GAP_MATRIX.md`
- `docs/V2_VERIFICATION.md`
- `docs/adr/0001-integrity-and-canonical-contracts.md`
- `docs/adr/0002-offline-evaluation-and-tool-boundaries.md`
- `examples/fixtures/domain_cases.json`
- `golden/__init__.py`
- `golden/change.py`
- `golden/eval.py`
- `golden/retrieval.py`
- `golden/tools.py`
- `pyproject.toml`
- `scripts/change_demo.py`
- `scripts/evaluate_fixture.py`
- `scripts/retrofit.py`
- `scripts/skill_manifest.py`
- `scripts/trace_demo.py`
- `scripts/verify_standard.py`
- `tests/test_eval.py`
- `tests/test_integrity.py`
- `tests/test_standard.py`
- `tests/test_tools.py`
