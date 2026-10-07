# CML Trust

**A research prototype for evidence-bound continuity evaluation and state-transition review**

[![Status: Research Alpha](https://img.shields.io/badge/status-research%20alpha-555555)](#project-status)
[![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-555555)](https://www.python.org/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-555555)](LICENSE)

CML Trust is an open research prototype for recording, preserving, and evaluating external continuity evidence against a compile-valid CML audit plan.

The project is intentionally narrow. It does **not** attempt to prove that a generator executed CML, establish physical identity, infer unseen states, or replace formal verification. Its purpose is to make continuity observations explicit, reproducible, inspectable, and resistant to silent state rewriting.

---

## Research question

**Can a small, explicit evidence layer improve the auditability of long-horizon state transitions without allowing evaluation itself to rewrite the state being evaluated?**

CML Trust approaches that question by separating:

```text
declared plan
    ↓
sealed inputs
    ↓
external observation
    ↓
noncanonical evidence
    ↓
derived evaluation
    ↓
explicit commit / revocation boundary
```

The central design rule is simple:

> **Observation is evidence. Evidence is not canonical state.**

---

## Current research scope

| Area | Current alpha behavior |
|---|---|
| Plan integrity | Records compile-valid CML plans and associated hashes |
| Evidence integrity | Records SHA-256 identities for plans, media, frames, and review artifacts |
| Checkpoint review | Stores explicit observation outcomes at selected states |
| Interval review | Records whether required continuity coverage exists between checkpoints |
| Failure handling | Preserves directly observed hard failures |
| Revocation | Appends revocations without rewriting earlier records |
| Derived status | Computes current status from the evidence ledger |
| Model integration | Provides a constrained host-side function wrapper |
| Storage | Local append-only JSONL |

### Canonical record types implemented

- `sealed_plan`
- `extract_manifest`
- `checkpoint`
- `span_review`, including `review_type: boundary_window`
- `revocation`

Reserved record types that are **not implemented** are rejected fail-closed with `POLICY_BLOCK` rather than silently treated as supported features.

---

## What the prototype can establish

Given supplied artifacts and reviewer observations, the current alpha can establish that:

1. a CML audit plan compiled successfully through the reference compiler;
2. recorded source, IR, media, and reviewed frame bytes match stored SHA-256 values;
3. checkpoint observations were recorded using explicit result enums;
4. adjacent checkpoint intervals have or lack required review coverage;
5. a directly observed hard failure blocks an observational chain;
6. revocation and descendant invalidation remain append-only and derived.

These are **artifact-level findings**. They are not claims about hidden generator internals or unobserved state.

---

## What the prototype does not establish

CML Trust does not prove:

- that a generator executed CML;
- that an audit plan existed before generation without an independently trusted timestamp;
- physical identity of a person or object;
- truth of unobserved frames;
- perfect human or machine semantic judgment;
- tamper-proof local storage;
- that CML improves generation quality;
- release eligibility under an unspecified “trusted” Boolean;
- equivalence to theorem proving or formal verification.

This boundary is deliberate.

---

## Evidence model

Observation results are explicit:

```text
observed_pass
observed_fail
unobserved
uncertain
not_applicable
not_checked
```

For this alpha:

- occlusion is represented as `unobserved`;
- `not_applicable` is rejected for invariants declared as always governing;
- directly observed hard failure is not downgraded because coverage elsewhere is incomplete.

Derived project status is one of:

```text
checkpoint_samples_only
coverage_incomplete
observational_chain_failed
observational_chain_complete
```

---

## Reproducibility

### Requirements

- Python 3.10–3.13
- Node.js 18.19 or newer
- CML Reference Compiler available locally
- `cml-python-adapter` 0.1.2 or compatible 0.1.x

### Install for development

```bash
python -m venv .venv
python -m pip install cml-python-adapter==0.1.2
python -m pip install -e .
```

### Run the test suite

```bash
python -m unittest discover -s tests -v
```

### Seal a plan

```bash
CML_COMPILER_DIR=../reference-compiler \
cmltrust plan seal scene.cml \
  --id plan_001 \
  --invariants invariants.json
```

The compiler path identifies JavaScript executed with the current user's permissions. Use only a trusted compiler checkout.

---

## Minimal workflow

```bash
cmltrust plan seal scene.cml --id plan_001 --invariants invariants.json

cmltrust extract register extract-descriptor.json

cmltrust checkpoint add \
  --id C1 \
  --plan plan_001 \
  --frame frames/000001.png \
  --results C1-results.json \
  --reviewer reviewer_1

cmltrust checkpoint add \
  --id C2 \
  --plan plan_001 \
  --parent C1 \
  --frame frames/000100.png \
  --results C2-results.json \
  --reviewer reviewer_1

cmltrust span add \
  --id S1 \
  --plan plan_001 \
  --from C1 \
  --to C2 \
  --coverage every_frame \
  --results S1-results.json \
  --reviewer reviewer_1

cmltrust status
```

Records append to `.cml-trust/records.jsonl` by default. Normal commands do not rewrite earlier lines.

---

## Reproducible public evidence

The repository contains bounded public evidence rather than broad claims.

### Completed evidence gates

**Gate 1 — compiler / adapter integration**  
Real CML Reference Compiler and Python adapter integration.

**Gate 2 — full-frame audit**  
Run 006 demonstrated clean endpoint observations with a failed interval.

**Gate 3 — independent human replication**  
One blind reviewer independently identified the central transient defect in the same transfer region.

**Gate 4 — pre-generation seal protocol**  
Run 007 preserved locally sealed plan and generation inputs before submission, followed by external rendering, every-frame audit, a canonical evidence ledger, hash manifest, and blind human review.

Gate 4 derived `observational_chain_failed`. This remains a bounded artifact-level result: the local seal is not trusted time, the generator is not shown to have consumed CML, and one blind reviewer is not a statistical validation study.

See:

- [Evidence gates](docs/EVIDENCE-GATES.md)
- [Pre-generation seal protocol](docs/PREGENERATION-SEAL-PROTOCOL.md)
- [Publication status](docs/PUBLICATION-STATUS.md)
- [Gate 4 public evidence](integration/gate4_pregeneration_run007/)
- [Adjacent research and technical distinctions](docs/ADJACENT-RESEARCH-AND-TECHNICAL-DISTINCTIONS.md)

---

## Human review instrument

`review/operation-coffee-cup-run006-review.html` is a self-contained browser review form for the Run 006 replication artifact.

It:

- makes no network requests;
- verifies the selected MP4 by SHA-256 in the browser;
- separates opening and final holder questions;
- distinguishes anatomical from screen-relative hand labels;
- requires descriptions and approximate times for failed or uncertain observations;
- exports a completed JSON submission.

The reviewed media artifact is distributed separately.

---

## Model-tool boundary

`cml_trust.tool_host.CMLTrustToolHost` exposes two allow-listed host operations:

- `cml_plan_seal`
- `cml_status_derive`

The host fixes workspace and ledger paths. A model cannot use this wrapper to execute arbitrary shell commands or select an arbitrary store.

See [Model-tool integration](docs/MODEL-TOOL-INTEGRATION.md).

---

## Engineering evidence standard

Performance work follows a standing real-workload evidence rule.

Passing CI can establish implementation and benchmark-harness integrity, but a performance claim is not treated as verified until a supported workload has been tested with:

- correctness parity;
- exact environment identity;
- repeated baseline and treatment measurements;
- startup treatment;
- distribution reporting.

See [Real-workload performance evidence](docs/REAL-WORKLOAD-PERFORMANCE-EVIDENCE.md).

---

## Project status

**Version:** `0.1.0a1`  
**Maturity:** research prototype / alpha  
**Storage:** local JSONL  
**Generator integration:** none  
**Hosted service:** none  
**License:** Apache-2.0

`cml-python-adapter` 0.1.2 is publicly available from PyPI. `cml-trust` 0.1.0a1 is currently distributed as a GitHub alpha pre-release source package and is not published on PyPI.

See [Installation validation](docs/INSTALL-VALIDATION.md).

---

## Repository guide

| Path | Purpose |
|---|---|
| `src/` | implementation |
| `tests/` | unit and regression tests |
| `examples/` | example CML and invariant inputs |
| `integration/` | evidence-gate runs and results |
| `review/` | self-contained human review instrument |
| `docs/` | protocols, scope boundaries, and research notes |
| `evidence/` | bounded public evidence bundles |

---

## Review and contribution

Technical review is welcome, especially around:

- state and evidence separation;
- failure precedence;
- revocation semantics;
- lineage and recovery;
- reproducibility;
- adversarial cases;
- terminology and scope boundaries.

Issues should distinguish observed implementation behavior from proposals, hypotheses, or broader research interpretation.

---

## Authorship and attribution

CML Trust is authored by **Sherrie Joseph** as part of ongoing CML research.

The project does not claim invention of formal verification, invariants, state machines, provenance, append-only logs, or other established foundations on which this work depends. Adjacent work and technical distinctions are documented explicitly in [Adjacent research and technical distinctions](docs/ADJACENT-RESEARCH-AND-TECHNICAL-DISTINCTIONS.md).

---

## License

Apache License 2.0. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES).
