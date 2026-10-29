# First use on a Windows work PC

Open `docs/field-guide/field-guide.pdf` first. It explains the system, repository map,
work loop, safety boundaries, ROI and interview practice. It needs only a PDF reader.

## Before the one-way transfer

Use the company's approved inbound-transfer process. Transfer the ZIP and its `.sha256`
sidecar; retain the expected checksum through a trusted approved channel. Compare it on
the destination with `Get-FileHash -Algorithm SHA256 .\golden-standard-<version>-<commit>.zip`.
Substitute the actual filename. A checksum detects change, not publisher identity or
company authorization. This snapshot can include proposed/unreleased work; review the
PR/commit before adopting it. No data needs to return from the work PC.

Confirm **Python 3.11+ for Windows** is already available through approved internal
provisioning. It is not bundled. A PDF reader is enough to read/learn; Python is needed
for runnable labs/checks. Git, internet and Python packages are not needed on the target.
OpenCode and an approved internal model/provider are separate optional prerequisites for
AI-assisted commands; their binaries, model weights and credentials are not in this ZIP.
External reference URLs are optional reading and may be unavailable at work.

## Verify the extracted snapshot

Extract to a new folder using the approved Windows ZIP tool. Open PowerShell in that folder:

```powershell
py -3 --version
py -3 scripts/offline_preflight.py --transfer
```

If the Python launcher `py` is absent but approved Python is on PATH, use
`python scripts/offline_preflight.py --transfer`. Ensure that interpreter reports >=3.11.
The script does not install anything or call a model. Stop on failure and preserve the
error locally. A blocked prerequisite goes to internal IT; do not bypass device controls.
The publisher records macOS/Linux/Windows CI results in the PR; your locked-down PC is
verified only after you run it. The publisher-only test skips without Git; symlink tests
skip if Windows cannot create symlinks. Skips are reported, not passes. Synthetic fixtures
do not certify company systems.

Keep the source snapshot unchanged. Put exercises in `workspace/`, results in `out/` or
`results/`; these folders and generated `__pycache__` are excluded from transfer rechecks.
The manifest itself is an untrusted local file unless its ZIP checksum/commit provenance
is independently verified. Intentional standard changes require a new reviewed snapshot.

## Adopt in an existing project

First read `docs/BROWNFIELD_ADOPTION.md`. From the separate standard snapshot:

```powershell
py -3 scripts/repo_audit.py C:\Approved\ExistingProject
py -3 scripts/retrofit.py C:\Approved\ExistingProject
```

The first is filenames/metadata only; the second is a dry run. Review paths and collisions
before separately choosing `--apply`. It copies missing helpers/guidance, not runtime,
tests or model configuration. Reconcile existing `AGENTS.md`, skills and docs manually;
skipped files are not upgraded. No command here starts an application or grants data access.

## First learning session

Read guide pages 1-3, run the synthetic preflight, then complete
`academy/assessment/README.md` unaided. Write a dated readiness record from
`templates/READINESS_SNAPSHOT.md` into `workspace/`. Leave unobserved competence unassessed.
Company-derived records stay inside approved company storage; public interview stories
need confidentiality/source-owner approval. This package requires no outbound reporting.
