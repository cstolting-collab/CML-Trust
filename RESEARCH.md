# Research Overview

CML Trust is an alpha-stage research implementation concerned with a narrow systems question:

> How can continuity observations be recorded, reviewed, and carried forward without allowing the act of evaluation to silently rewrite the authoritative state being evaluated?

The project treats declared state, external observation, derived evaluation, and commit authority as separate concerns.

## Working model

```text
DECLARED PLAN
      ↓
SEALED INPUTS
      ↓
EXTERNAL OBSERVATION
      ↓
NONCANONICAL EVIDENCE
      ↓
DERIVED EVALUATION
      ↓
AUTHORIZED STATE ACTION
```

## Research objectives

The alpha is being used to study four bounded questions:

1. **State separation** — whether authoritative state can remain distinct from observations about that state.
2. **Evidence lineage** — whether observations, revocations, and derived status can remain inspectable without rewriting earlier records.
3. **Failure handling** — whether directly observed failures remain visible even when other coverage is incomplete.
4. **Reproducibility** — whether another reviewer can inspect the same public artifacts and reproduce the recorded evaluation path.

## Current implementation boundary

The public repository contains a working research prototype, tests, examples, human-review tooling, and bounded evidence-gate artifacts.

It does not establish hidden generator behavior, physical identity, trusted time, truth of unobserved frames, or equivalence to formal verification.

## Evaluation posture

Results are reported as evidence-bound observations, not universal claims.

The project distinguishes implementation behavior, artifact-level findings, hypotheses, unresolved questions, and future work.

## Public research record

Start with:

- [README](README.md)
- [Evidence guide](evidence/README.md)
- [Examples and reproduction guide](examples/README.md)
- [Evidence gates](docs/EVIDENCE-GATES.md)
- [Publication status](docs/PUBLICATION-STATUS.md)
- [Adjacent research and technical distinctions](docs/ADJACENT-RESEARCH-AND-TECHNICAL-DISTINCTIONS.md)

## Authorship

CML Trust is authored by Sherrie Joseph as part of ongoing CML research.

The project does not claim invention of the established foundations it uses, including formal verification, invariants, state machines, provenance, append-only logs, hashing, or audit trails.
