# CML-Trust 0.1.0a1

First public alpha release of a local, external continuity-evidence notebook.

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
- allow-listed host-side `cml_plan_seal` and `cml_status_derive` tool wrapper;
- compact Run 007 pre-generation evidence bundle;
- Apache-2.0 license, NOTICE, and third-party notices;
- 36 passing tests in the latest code-validation change;
- Gate 1–4 evidence summaries.

## Evidence results

### Run 006

Run 006 produced clean opening and final checkpoint states but a failed transfer
span. One blind human later identified the same central transient two-handle
defect near approximately 0:03.

The audit plan was sealed after generation. This is one replicated
artifact-level finding, not a pre-generation conformance test or statistical
validation study.

### Run 007

The compile-valid plan and exact generation inputs were locally sealed before
submission according to the published procedure. Every-frame review of the
result found a failed transfer interval: a second cup handle formed, the
receiving hand used that emergent handle instead of the sealed side grip, and
the released hand remained closed.

The canonical derived status is:

```text
observational_chain_failed
```

One blind human reviewer independently reported the two-handle failure class,
failed transfer, closed released hand, and continuous shot.

## Explicit limits

- No evidence that a generator consumed or executed CML.
- No claim that CML caused an improvement in generation quality.
- No trusted time or tamper-proof ledger.
- No automatic semantic identity proof.
- `trust.v1` supports only `governs: always`; checkpoint-specific applicability
  is not represented.
- The JSONL store requires one writer process or external cross-process locking.
- No event evidence, bridge repair, residual ledger, or validator-fusion engine
  in this alpha.
- The Run 007 media and frame cache are omitted from Git; their hashes remain in
  the public bundle.
- The Python Adapter dependency is publicly available from PyPI and passed one
  clean local installation-and-seal check. CML-Trust itself remains unpublished
  on PyPI, and independent outsider installation is not yet demonstrated.
- Python 3.10–3.13 and the cross-platform support matrix are not yet verified.

## Release label

```text
v0.1.0a1 — pre-release
```

Do not label this build stable, production-ready, statistically validated, or a
completed trust engine.
