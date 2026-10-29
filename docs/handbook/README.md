# Foundations design and practice handbook

This is the in-depth teaching companion to the standard. It explains mechanisms, reasons
for the controls, human and AI responsibilities, two worked use cases and fair comparison
with established methods. It is explanatory; canonical rules remain in the linked sources.

- `agentic-engineering-handbook.html`: static offline browser document with contents and
  embedded vector diagrams; no JavaScript, remote fonts or automatically fetched assets.
- `agentic-engineering-handbook.pdf`: printable version with page-level sources and bookmarks.
- `HANDBOOK.md`: readable repository version with Mermaid diagram source and linked references.
- `content.json`: common narrative/diagram source for all three formats.

The 12-page field guide is the short orientation. This handbook supplies the mechanisms
and worked reasoning behind it. Start with chapters 3-9 for model/retrieval fundamentals,
10-20 for runtime/evidence, 21-24 for value/comparison, 25-33 for people/use cases and 34-36
for practice and offline adoption. The comparisons describe scope and tradeoffs, not proven
superiority; this repository has no controlled head-to-head enterprise study.

Publisher workflow: `python scripts/build_handbook.py` (existing approved ReportLab needed
only for authoring), render PDF pages with Poppler, inspect every page, then copy the three
generated outputs from `output/pdf/handbook/` here. The narrative hash appears in the PDF
and HTML. Cross-check diagrams, examples and source links when canonical rules change.
Do not ship a regenerated format without checking it. Reference checks do not import the
authoring dependency. All prebuilt reading files are in the offline snapshot.

External sources are primary research, standards or official methodology documentation,
listed in the bibliography. Their summaries are dated; URLs are optional further reading
on an approved network. No external papers, company data or proprietary source are bundled.
The learner's unaided mastery and real corporate ROI remain unassessed until observed.
