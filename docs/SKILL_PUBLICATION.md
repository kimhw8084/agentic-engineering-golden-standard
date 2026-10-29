# Versioned skill publication and safe rollout

Publish reviewed immutable Git commit/tag plus `.opencode/skills-manifest.json` with standard
version and every skill's SHA-256. Referenced docs/commands/agents come from the **same pinned
commit**; manifest alone does not attest supporting files or safety. Run
`python -m scripts.skill_manifest` to check drift; `--write` regenerates only the manifest.
It never installs skills or changes model/provider settings. Review diffs as code.

Publication: bounded change → deterministic/negative checks → separately accountable
reviewer checks exact commit/permissions/injection risks → maintainer publishes approved
version/changelog. Tags/hashes grant no trust. Verify provenance through approved company
process; signing/enforcement is outside this repo.

Canary one synthetic sandbox, then one opt-in team; expand after agreed quality, calls,
cost/latency and usability gates. Record old/new commit, manifest hash, owner, classification,
checks and rollback. Revoke on poisoning/drift; disable helper/tool, restore prior reviewed
commit and rerun regressions. No automatic runtime-schema downgrade.

Brownfield: dry-run, inspect collisions/symlink skips, apply to approved scope. Existing
skills/docs remain unchanged; reconcile differences/references manually. Installer copies
no Python runtime/tests or publication manifest. Keep manifest as review evidence, not a
claim target files match. Repeated single-process apply copies no existing files; concurrent
hostile filesystem replacement is outside its guarantee.
