# Cold verification request

This packet contains synthetic source, tests and existing canonical requirements. Its
manifest identifies the exact source commit and per-file SHA256s. It excludes the author's
chat, new readiness report, new decision rationale, new learning record and PR narrative.
No hidden company corpus or protected evaluation labels are included. Do not ask the author
for expected findings before completing the first pass.

Use a separately approved session/model without author-history inheritance. AI review is
assistance, not an independent human release decision. An accountable human reviewer must
identify themselves, reproduce consequential claims and resolve findings before approval.
Do not merge, deploy, contact others or connect external tools/endpoints during review.

Read source before accepting test names/assertions. Challenge authority boundaries,
malformed inputs, source/revision/citation binding, graph completeness, retries, cancellation,
crash recovery, tool drift, exposure, evaluator correctness and promotion claims. Create
at least one fresh negative case not copied from visible tests. Do not treat public labels
as independent ground truth. Distinguish reproducible defects from theoretical risks and
intentionally unsupported capabilities. Attempt to falsify the safety and usefulness claims.

Reproduction in a separate approved workspace, Python 3.11+:

```text
python scripts/verify_standard.py
python -m unittest discover -s tests -v
python -m scripts.evaluate_investigation --repeats 5
python scripts/offline_preflight.py
```

The app is optional: `python -m scripts.investigation_app`; restrict it to bundled synthetic
data and loopback. Operator CLI: `python -m scripts.pilot_control --help`. Read its code
before a separate-process stop/recovery drill. Do not attach proprietary sources or tools.

Return a record with reviewer identity/accountability, model/version if applicable, packet
SHA256 and source commit, environment, exact executed commands, failures/skips, findings
ranked by severity with minimal reproductions, evidence/limitations and suggested disposition.
State which controls remain missing and which business or human-competence claims cannot be
supported. Record reviewed commit and any changes requiring a fresh review.

Review status: NOT PERFORMED by an independent recipient at packet creation. Sending this
packet to another role prompt in the author's context is not independent human review.
