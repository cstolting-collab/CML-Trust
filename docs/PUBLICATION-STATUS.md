# Publication status — 0.1.0a1

## Recommended channel

Publish first as a **GitHub pre-release source package** labeled research
prototype / alpha.

Do not publish to PyPI yet.

## Why GitHub alpha is acceptable

- Core source is present and locally testable.
- Apache-2.0 license, NOTICE, and third-party notice are present.
- The implemented record kinds and non-goals are disclosed.
- A wheel builds locally.
- The evidence-gate reports distinguish engineering results from media claims.
- The browser review form removes the manual-JSON usability failure.

## Dependency verification completed

`cml-trust` depends on `cml-python-adapter>=0.1.2,<0.2`. Adapter version 0.1.2
is publicly available from PyPI. On 2026-08-11, a fresh local Python 3.12
environment installed the public adapter and the locally built CML-Trust alpha
wheel, then completed a real seal through CML Reference Compiler
`1.1.0-rc.2`.

This closes the former “adapter unavailable” blocker. It does not establish an
independent outsider installation, a public CML-Trust distribution install, or
cross-platform support. See [`INSTALL-VALIDATION.md`](INSTALL-VALIDATION.md).

## Why CML-Trust PyPI publication remains deferred

Required before PyPI publication:

1. Install CML-Trust from its actual public release artifact, not a local wheel.
2. Have a person outside the development sessions follow only the published
   instructions.
3. Run a real compiler seal in that outsider environment.
4. Test Python 3.10, 3.11, 3.12, and 3.13 across the supported operating-system
   matrix.

Repository source and issue URLs are now declared in package metadata.

## Implemented alpha surface

- sealed plans
- extraction manifests
- checkpoints
- interval and boundary-window span reviews
- revocation and derived invalid lineage
- derived checkpoint and chain status
- offline Run 006 browser review

## Reserved, not implemented

- event evidence and phase derivation
- bridge-repair records
- residual audio-clock ledger
- multi-reviewer fusion or reliability scoring
- automatic video editing or generator integration

## Evidence claim allowed at publication

One blind human independently identified the central transient two-handle
continuity defect in Run 006 near the same transfer region as the first
AI-assisted review.

Do not convert that into a claim of statistical validation, generator control,
or improved generation quality.

## Next evidence gate

Run one new artifact from a plan sealed before generation, then publish the
plan record, media/extraction hashes, checkpoint results, span reviews, and any
failures. The exact procedure and claim boundary are documented in
[`PREGENERATION-SEAL-PROTOCOL.md`](PREGENERATION-SEAL-PROTOCOL.md).
