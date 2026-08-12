# Installation validation — local clean environment

**Date:** 2026-08-11  
**Scope:** Dependency resolution and real plan sealing  
**Result:** Passed at the scope stated below

## Environment

- Linux execution environment
- Python `3.12.13`
- Node.js `24.14.0`
- `cml-python-adapter==0.1.2` downloaded from PyPI
- `cml-trust==0.1.0a1` installed from the locally built universal wheel
- trusted local CML Reference Compiler `1.1.0-rc.2` checkout

## Procedure

1. Created a new temporary Python virtual environment.
2. Installed `cml-python-adapter==0.1.2` from PyPI.
3. Installed `cml_trust-0.1.0a1-py3-none-any.whl` from the local build.
4. Set `CML_COMPILER_DIR` to the trusted local Reference Compiler checkout.
5. Ran `cmltrust plan seal` on the Operation Coffee Cup Run 006 audit plan.
6. Ran `cmltrust status` against the new store.

## Observed result

- Adapter installation succeeded at version `0.1.2`.
- CML-Trust installation succeeded at version `0.1.0a1`.
- The compiler reported `1.1.0-rc.2 (CML 1.0.0)`.
- Plan compilation succeeded.
- A `sealed_plan` record was appended with source, normalized-IR, and compiler
  entry hashes.
- Status correctly reported `no_checkpoints` because the clean store contained
  only the seal.

## What this establishes

This run establishes that the published Python Adapter dependency can be
resolved in a fresh local Python 3.12 environment and can support a real
CML-Trust plan seal using a trusted local Reference Compiler checkout.

## What this does not establish

- It was not performed by an independent outsider.
- CML-Trust was installed from a local wheel, not a public package index or
  public release download.
- Only one Python version, operating system, and Node.js version were tested.
- The Reference Compiler was already available locally.
- The plan used for this installation check describes an earlier artifact; the
  run does not establish pre-generation plan timing or generator execution.
- The local `sealed_at` field is explicitly untrusted time.

The next installation gate requires an outside person to install CML-Trust
from an actual public release artifact using only published instructions.
