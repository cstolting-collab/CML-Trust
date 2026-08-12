# CML-Trust 0.1.0a1

First public alpha candidate for a local, external continuity-evidence
notebook.

## Why this alpha exists

Continuity cannot be certified from clean endpoint frames alone. A transient
defect can occur between checkpoints and later recover. CML-Trust records nodes
and spans separately so an observed interval failure remains visible.

## Included

- compile-valid audit-plan seals;
- source and normalized-IR SHA-256 binding;
- source-video and extracted-frame manifests;
- hashed checkpoint observations;
- interval and boundary-window span reviews;
- append-only revocation and derived invalid lineage;
- explicit incomplete, failed, and complete chain statuses;
- offline browser reviewer for Operation Coffee Cup Run 006;
- 27 passing offline tests;
- Gate 1–3 evidence summaries.

## Evidence result

Run 006 produced clean opening and final checkpoint states but a failed transfer
span. One blind human later identified the same central transient two-handle
defect near approximately 0:03.

This is one replicated artifact-level finding, not a statistical validation
study.

## Explicit limits

- Audit plan sealed after the tested render; no pre-generation conformance
  claim.
- No generator integration.
- No trusted time or tamper-proof ledger.
- No automatic semantic identity proof.
- No event evidence, bridge repair, residual ledger, or validator-fusion engine
  in this alpha.
- The Python Adapter dependency is publicly available from PyPI and passed one
  clean local installation-and-seal check. CML-Trust itself remains unpublished
  on PyPI, and independent outsider installation is not yet demonstrated.

## Recommended release label

```text
v0.1.0-alpha.1 — pre-release
```

Do not label this build stable, production-ready, or a completed trust engine.
