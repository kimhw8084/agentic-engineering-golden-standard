# Brownfield adoption: protect working applications

## 0. Inventory, no edits

1. Confirm approved repository/access and local branch. Save work and inspect `git status`.
2. Run `python scripts/repo_audit.py /path/to/repo` for **metadata only**; it never reads code contents.
3. Use OpenCode's `/golden-audit` in the target repo for **authorized**, human-reviewable deep architectural analysis; record exact files/tests read. Do not enable unrestricted agent read access to entire email/recipe corpora.
4. Create a current-state matrix: implemented / tested / broken / unverified / duplicate / missing, with source locations.

## 1. Dry-run skills installation

`python scripts/retrofit.py /path/to/repo` previews. `--apply` copies only missing `.opencode/skills/`, `commands/`, `agents/`, `docs/`, `templates/` and `academy/` files. Existing files remain unchanged. Installer never edits model selection, credentials, AGENTS.md, opencode.json, tests or application source code. For colliding `docs/` paths, compare and reconcile manually before using referenced guidance.

## 2. Policy integration

Compare `templates/AGENTS_BROWNFIELD.md` with current `AGENTS.md` and merge manually. If OpenCode's corporate policy is stricter, preserve it. Preserve existing model/provider settings. Run `opencode` in an approved isolated dev environment.

## 3. First vertical slice

Pick one specific question, approved corpus, baseline method, and one golden test case. Ensure tool authorization and deterministic evaluation precede additional agents. Capture before/after accuracy and response-time samples.

## 4. Release and learn

Use `templates/EXPERIMENT.md`, `templates/MASTERY_RECORD.md`, and PR gates. Adopt standards incrementally, never force a large rewrite to gain a template.

## Anti-patterns

No automatic copy of entire company source/recipes/emails into embeddings; no universal unrestricted search account; no hiding failed tests; no premature microservice split; no treating an LLM's self-score as ground truth.
