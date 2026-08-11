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

## Why PyPI remains blocked

`cml-trust` depends on `cml-python-adapter>=0.1.2,<0.2`. Public PyPI
availability and clean installation of that dependency have not been verified.
Publishing the dependent package first could produce an installable-looking
release that fails dependency resolution for ordinary users.

Required before PyPI:

1. Publish or otherwise provide a stable public Python Adapter distribution.
2. Test a clean environment install using only documented public sources.
3. Run a real compiler seal from that clean environment.
4. Test Python 3.10, 3.11, 3.12, and 3.13 on supported operating systems.
5. Add repository URLs to package metadata after the canonical repository
   exists.

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
