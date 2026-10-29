# Visual field guide

Read `field-guide.pdf` with any PDF reader. It is a static black/white/gray explanatory
guide with source paths on every page. Canonical rules remain in the cited repository files.
No remote fonts, scripts, images or network are used for reading. External sources in the
academy are optional further reading, not offline prerequisites.

`content.json` is the narrative source. The publisher can render it with
`python scripts/build_field_guide.py` using an already approved ReportLab installation,
then visually inspect every page and copy the resulting PDF here before committing. That
authoring dependency is not required to read, run the standard or verify the offline bundle.
The generated PDF footer binds the content hash and standard version. Regenerate after
content changes; review the guide alongside changes to the canonical sources it summarizes.

The Windows handoff is described in `OFFLINE_START.md` at repository root. From a clean
reviewed commit the publisher runs `python scripts/build_offline_bundle.py`. The resulting
ZIP contains this PDF, source/guidance/tests and a per-file hash manifest. Its sidecar
checksum must be retained through an approved trusted channel. No model or Python installer
is included. The packaging script does not release, deploy or grant company authorization.
