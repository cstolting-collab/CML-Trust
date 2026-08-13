# Publication status — 0.1.0a1

## Release channel

CML-Trust 0.1.0a1 is distributed as a **GitHub pre-release source package**
labeled research prototype / alpha.

It is not published on PyPI.

## Why the GitHub alpha is acceptable

- Core source is present and locally testable.
- Apache-2.0 license, NOTICE, and third-party notice are present.
- The implemented record kinds, reserved kinds, and non-goals are disclosed.
- A universal wheel builds locally.
- The evidence-gate reports distinguish engineering results from media claims.
- Run 007 completed the documented pre-generation seal procedure and preserves
  its failed observational result without converting it into a success claim.
- The browser review form removes the manual-JSON usability failure.
- The optional model-tool wrapper uses allow-listed operations and host-owned
  workspace and ledger paths.

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

1. Install CML-Trust from its actual public GitHub release artifact, not a local
   wheel.
2. Have a person outside the development sessions follow only the published
   instructions.
3. Run a real compiler seal in that outsider environment.
4. Test Python 3.10, 3.11, 3.12, and 3.13 across the supported operating-system
   matrix.

Repository source and issue URLs are declared in package metadata.

## Implemented alpha surface

- sealed plans
- extraction manifests
- checkpoints
- interval and boundary-window span reviews
- revocation and derived invalid lineage
- derived checkpoint and chain status
- offline Run 006 browser review
- host-side `cml_plan_seal` and `cml_status_derive` tool wrapper
- compact Run 007 pre-generation evidence bundle

## Reserved, not implemented

- event evidence and phase derivation
- bridge-repair records
- residual audio-clock ledger
- multi-reviewer fusion or reliability scoring
- automatic video editing or generator integration

## Evidence claims allowed at publication

Run 006 supports the narrow statement that full-interval review detected a
transient two-handle continuity defect that clean endpoint samples missed, and
one blind human independently identified the same central defect near the same
transfer region.

Run 007 supports the narrow statement that the plan and exact generation inputs
were locally sealed before submission according to the published procedure,
then every-frame review found a failed transfer interval despite readable
opening and final states. One blind human review reported the same two-handle
failure class.

Neither result establishes generator conformance, causal improvement from CML,
trusted chronology, statistical reliability, or provider adoption.

## Known alpha limitations

- `trust.v1` supports only `governs: always`; checkpoint-specific applicability
  cannot yet be represented.
- The JSONL store has no cross-process lock and requires one writer process or
  external locking.
- Local `sealed_at` values are untrusted clock readings.
- The Run 007 source image, result MP4, and 241-frame extraction cache are
  omitted from Git; their SHA-256 bindings remain published.
- No automated generator integration exists.

## Next validation gates

1. Independent installation from the public GitHub release artifact.
2. Real compiler sealing in that outsider environment.
3. Python 3.10–3.13 and cross-platform verification.
4. Additional artifacts and independent reviewers before any reliability or
   quality-improvement claim.
