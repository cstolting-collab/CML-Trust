# cml-trust

`cml-trust` is an alpha-stage, local evidence notebook for recording external
continuity observations against a compile-valid CML audit plan.

It is deliberately narrower than a “trust engine.” It hashes plans and media
evidence, stores append-only observations, separates checkpoint state from
interval coverage, derives status, and preserves revocations without rewriting
prior records.

## Status

**Version:** `0.1.0a1`  
**Maturity:** research prototype / alpha  
**Storage:** local JSONL  
**Generator integration:** none

Implemented canonical records:

- `sealed_plan`
- `extract_manifest`
- `checkpoint`
- `span_review`, including `review_type: boundary_window`
- `revocation`

Reserved but intentionally rejected in this alpha:

- `event_evidence`
- `repair_plan`
- `residual_ledger_entry`

Reserved kinds fail closed with `POLICY_BLOCK`; they are not silently accepted
or represented as finished features.

## What it can establish

Given the supplied evidence and fallible reviewer observations, the current
alpha can establish that:

- a CML audit plan compiled successfully through the reference compiler;
- source, IR, video, and reviewed frame bytes match recorded SHA-256 values;
- individual checkpoint states were observed with explicit result enums;
- adjacent checkpoint intervals have or lack required span coverage;
- a directly observed hard failure blocks an observational chain;
- revocations and descendant invalidation remain append-only and derived.

## What it does not establish

It does not prove:

- that a generator executed CML;
- that a post-generation audit plan existed before generation;
- physical identity of a person or object;
- truth of unobserved frames;
- perfect human or machine semantic judgment;
- trusted timestamps or tamper-proof local storage;
- that CML improves generation quality;
- release eligibility under an unnamed “trusted” Boolean.

## Requirements

- Python 3.10–3.13
- Node.js 18.19 or newer
- CML Reference Compiler available locally
- `cml-python-adapter` 0.1.2 or a compatible 0.1.x release

### Publication limitation

The alpha wheel builds successfully, but PyPI installation is intentionally
blocked until `cml-python-adapter` is independently published and verified as a
publicly installable dependency. Until then, use a local adapter checkout or an
approved source installation.

## Development setup

From the `cml-trust` directory, with the Python adapter source available in a
sibling directory:

```text
PYTHONPATH=src:../src python -m unittest discover -s tests -v
```

For a real plan seal, point the adapter at the local reference compiler:

```text
CML_COMPILER_DIR=../reference-compiler \
PYTHONPATH=src:../src \
python -m cml_trust.cli plan seal scene.cml \
  --id plan_001 \
  --invariants invariants.json
```

## Minimal CLI workflow

```text
cmltrust plan seal scene.cml --id plan_001 --invariants invariants.json
cmltrust extract register extract-descriptor.json
cmltrust checkpoint add --id C1 --plan plan_001 \
  --frame frames/000001.png --results C1-results.json --reviewer reviewer_1
cmltrust checkpoint add --id C2 --plan plan_001 --parent C1 \
  --frame frames/000100.png --results C2-results.json --reviewer reviewer_1
cmltrust span add --id S1 --plan plan_001 --from C1 --to C2 \
  --coverage every_frame --results S1-results.json --reviewer reviewer_1
cmltrust status
```

Records append to `.cml-trust/records.jsonl` by default. Normal commands never
rewrite earlier lines.

## Observation results

```text
observed_pass | observed_fail | unobserved |
uncertain | not_applicable | not_checked
```

Occlusion is `unobserved`, never `not_applicable`. For this alpha,
`not_applicable` is rejected on invariants declared as always governing.

Project status distinguishes:

```text
checkpoint_samples_only
coverage_incomplete
observational_chain_failed
observational_chain_complete
```

A directly observed hard failure is never downgraded to
`coverage_incomplete`, even when the same review has limited coverage.

## Human review form

`review/operation-coffee-cup-run006-review.html` is a self-contained browser
form for the Run 006 replication artifact. It:

- makes no network requests;
- verifies the selected MP4 using SHA-256 in the browser;
- separates opening and final holder questions;
- distinguishes anatomical from screen-relative hand labels;
- requires descriptions and approximate times for failed or uncertain claims;
- exports one completed JSON submission with a single button.

Open the HTML file in a modern browser, select the matching Run 006 MP4
(distributed separately), complete the review, and choose **Save completed
review**.

## Evidence gates completed

- **Gate 1:** real compiler and Python adapter integration
- **Gate 2:** full-frame Run 006 audit; clean endpoints with a failed interval
- **Gate 3:** one blind human independently replicated the central transient
  two-handle defect near the same transfer region

Gate 3 is one independent reviewer, not a statistical validation study.

## Tests

```text
python -m unittest discover -s tests -v
```

The current suite covers schema rules, sealing, hashes, append-only revocation,
lineage, missing spans, hard-failure precedence, extract manifests, and the
self-contained browser review form.

## License

Software in this repository is licensed under the Apache License 2.0. See
`LICENSE`, `NOTICE`, and `THIRD_PARTY_NOTICES`.
