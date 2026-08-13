# Evidence gates

## Gate 1 — real toolchain integration

The CML Reference Compiler verification suite passed, the Python Adapter
compiled a real CML example, and `cml-trust` sealed the resulting audit plan.

This established integration among the existing components. It did not test
rendered media.

## Gate 2 — endpoint blindness on real media

Operation Coffee Cup Run 006 was decoded to 241 frames and reviewed across the
complete interval.

The opening and final checkpoints were individually complete. The transfer
span failed because the cup visibly developed a second handle and the receiving
hand interacted with the opposite-side handle rather than completing the
specified side grip.

Derived status:

```text
observational_chain_failed
```

Gate 2 also exposed a status-model defect: an observed hard failure could not be
honestly represented as merely `coverage_incomplete`. The alpha added and
tested `observational_chain_failed`, with observed failure taking precedence
over limited coverage.

The audit plan was sealed after generation. Gate 2 is retrospective
observational evidence, not plan-conformance-at-generation.

## Gate 3 — blind human replication

One human reviewer who reported no prior knowledge of the Gate 2 result
independently blocked the clip and described, at approximately 0:03:

- hand/finger continuity change;
- hand drift;
- a cup handle appearing on each side;
- a hand reaching toward a second cup handle.

This independently replicated the central transient defect class and temporal
region.

Gate 3 did not establish statistical inter-rater reliability. Classifications
and certainty differed on several invariants, and one original holder-state
question was ambiguous.

## Gate 4 — pre-generation-sealed Run 007

Before Run 007 was submitted for generation, the compile-valid CML plan, exact
generation prompt, invariant table, source image hash, normalized IR hash, and
compiler-entry hash were recorded in the local seal procedure.

The resulting eight-second artifact was decoded to 241 frames. The opening and
final holder states were readable, but every-frame review found that:

- a second cup handle formed during transfer;
- the receiving hand used the emergent handle rather than the sealed lower-body
  side grip;
- the released hand remained closed.

Derived status:

```text
observational_chain_failed
```

One blind human reviewer watching on a phone independently reported two handles
near approximately four seconds, a failed transfer, a closed released hand, and
a continuous shot.

The compact public bundle includes the plan, prompt, invariant table, canonical
five-record ledger, submitted results, audit report, blind review, and SHA-256
manifest. The source image, result MP4, and frame cache are omitted from Git,
but their hashes remain published.

Gate 4 establishes a bounded artifact-level finding relative to a locally
recorded pre-generation seal. It does not establish trusted chronology,
generator consumption or execution of CML, causal improvement, statistical
reliability, or provider adoption.

## Usability correction

The first Run 006 reviewer could not conveniently edit and save the manual JSON
form. The alpha includes a self-contained browser form that verifies the video
hash, splits opening and final boundary questions, requires notes and media
times for non-pass results, and exports JSON with one button.

## Narrow publication claims

The current evidence supports these statements:

> In one Run 006 artifact, full-interval review detected a transient continuity
> defect that clean endpoint samples missed, and one blind human independently
> identified the same central two-handle defect near the same transfer region.

> In Run 007, the plan and exact generation inputs were locally sealed before
> submission according to the published procedure; every-frame review then
> found a failed transfer interval despite readable opening and final states,
> and one blind human review reported the same two-handle failure class.

The evidence does not support claims of generator control, improved generation
quality, perfect identity verification, trusted time, provider adoption, or
broad statistical validation.
