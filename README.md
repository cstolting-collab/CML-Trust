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
**Model-tool integration:** optional host-side function wrapper; no hosted service

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

### Distribution status

`cml-python-adapter` 0.1.2 is publicly available from PyPI. A clean local
Python 3.12 environment successfully installed that adapter and the
`cml-trust` 0.1.0a1 wheel, then completed a real plan seal through CML
Reference Compiler `1.1.0-rc.2`.

`cml-trust` 0.1.0a1 is distributed as a GitHub alpha pre-release source
package. It is not published on PyPI. The clean verification used a locally
built alpha wheel and a local trusted compiler checkout, so it is not an
independent outsider-installation result. See
[`docs/INSTALL-VALIDATION.md`](docs/INSTALL-VALIDATION.md).

## Development setup

Create an isolated environment and install the public adapter plus this
checkout:

```text
python -m venv .venv
python -m pip install cml-python-adapter==0.1.2
python -m pip install -e .
```

From the `cml-trust` directory, run the test suite:

```text
python -m unittest discover -s tests -v
```

For a real plan seal, point the adapter at the local reference compiler:

```text
CML_COMPILER_DIR=../reference-compiler \
cmltrust plan seal scene.cml \
  --id plan_001 \
  --invariants invariants.json
```

The compiler path identifies JavaScript executed with the current user's
permissions. Use only a trusted compiler checkout. The recorded seal time is a
local, untrusted clock value; it is not cryptographic proof of when the plan
existed.

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

## Optional model-tool wrapper

`cml_trust.tool_host.CMLTrustToolHost` exposes two allow-listed operations for
developer-controlled function-calling applications:

- `cml_plan_seal`
- `cml_status_derive`

The host fixes the workspace and ledger paths; the model cannot execute shell
commands or select an arbitrary store. See
[`docs/MODEL-TOOL-INTEGRATION.md`](docs/MODEL-TOOL-INTEGRATION.md) for the exact
boundary and its remaining single-writer-process requirement.

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
- **Gate 4:** Run 007 plan and generation inputs were locally sealed before
  submission, followed by a new external render, every-frame audit, canonical
  ledger, hash manifest, and one blind human review

Gate 4 derived `observational_chain_failed`: the opening and final states were
readable, but a second cup handle formed during transfer, the receiving hand
used that emergent handle instead of the sealed side grip, and the released
hand remained closed.

These are bounded artifact-level findings. The local seal is not trusted time,
the generator is not shown to have consumed CML, and one blind reviewer is not
a statistical validation study. See
[`integration/gate4_pregeneration_run007/`](integration/gate4_pregeneration_run007/).

## Engineering performance evidence rule

Optimization work follows a standing real-workload evidence rule. Passing CI can
verify implementation and benchmark-harness integrity, but a performance claim
is not considered verified until a supported workload has run with correctness
parity, exact environment identity, repeated baseline/treatment measurements,
startup treatment, and distribution reporting.

See
[`docs/REAL-WORKLOAD-PERFORMANCE-EVIDENCE.md`](docs/REAL-WORKLOAD-PERFORMANCE-EVIDENCE.md).

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
