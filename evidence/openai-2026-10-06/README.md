# CML Public Verification Evidence Bundle

**Date:** 2026-10-06  
**Project:** Continuity Markup Language (CML)  
**Purpose:** Public, minimal, independently runnable evidence of the continuity/state-validation pattern already implemented in CML research before 2026-10-06.

## Claim boundary

This bundle does **not** claim that CML is a mathematical proof system, does **not** claim ownership of formal verification, and does **not** claim equivalence to OpenAI's mathematics work.

The narrower claim is:

> CML independently developed and documented a machine-verifiable continuity/state-validation architecture before 2026-10-06, using explicit invariants, canonical accepted state, authorization boundaries, fail-closed transition handling, noncanonical observation evidence, and reproducible tests.

## What this bundle demonstrates

The included demo shows a minimal continuity invariant:

1. define canonical state;
2. lock a selected field;
3. propose a conflicting state transition;
4. evaluate without mutating canonical state;
5. receive a machine-readable rejection;
6. perform an authorized unlock;
7. reevaluate the identical candidate;
8. receive acceptance;
9. verify canonical state still changes only through the explicit commit path.

Run:

```bash
node evidence/openai-2026-10-06/demo/locked-state-demo.mjs
node evidence/openai-2026-10-06/demo/test.mjs
```

No external packages are required.

## Prior dated implementation record

The private CML reference repository contains the earlier implementation history. Exact commit identifiers and dates are preserved in [PROVENANCE.md](./PROVENANCE.md).

Relevant milestones include:

- 2026-08-20: domain-neutral state governance with declarative invariants, provenance, lifecycle, and rejection before canonical commit.
- 2026-08-20: deterministic read-only continuity projections with freshness validation and resource limits.
- 2026-08-20: guarded checkpoint recovery.
- 2026-08-27: engine/Unreal conformance test proving the same candidate is rejected while locked and accepted only after authorized unlock.
- 2026-08-29: external observation conformance with PASS / FAIL / UNEVALUABLE outcomes, noncanonical evidence, tamper detection, and fail-closed behavior.
- 2026-09-24: fail-closed handling before unapproved external workflow writes.
- 2026-10-02: experiment/history preservation receipt.

## Why this is intentionally small

This is an evidence-only public disclosure. It does not expose the full private CML implementation. The goal is to make the verification principle inspectable without publishing unrelated private research.

## Technical review request

Researchers or engineers working on evaluations, oversight, agent reliability, stateful systems, reproducibility, or verification are invited to inspect the demo and provenance record. Full source history and additional experiment artifacts can be provided for technical review.
