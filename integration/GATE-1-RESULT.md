# Gate 1 — Real Compiler Integration Result

**Date:** 2026-08-11  
**Purpose:** Determine whether the independent `cml-trust` plan seal works through the real CML Python Adapter and authoritative CML Reference Compiler rather than a mock.

## Components tested

| Component | Identity |
| --- | --- |
| Reference Compiler repository | `cstolting-collab/CML-Reference-Compiler` |
| Reference Compiler commit | `93d9db1381fec735be80eb32f7aadb3766c0a160` |
| Reference Compiler package | `1.1.0-rc.2` |
| CML source-language version | `1.0.0` |
| Python Adapter | `0.1.2` |
| Node runtime used | `v24.14.0` |
| CML source | `reference-compiler/examples/natural-smile.cml` |
| Trust schema | `trust.v1` |

The compiler requires Node `>=18.19`; the runtime used satisfies that declared minimum. This test does not establish compatibility with every supported Node version or operating system.

## Reference Compiler verification

Command:

```text
npm run verify
```

Observed result:

- format verification passed;
- static quality verification passed for 126 JavaScript files;
- all 61 test files passed;
- Phase 20 security/resource tests passed 14/14;
- conformance passed 51/51 across the claimed full profile;
- example validation and compilation passed;
- zero production runtime dependencies check passed;
- package installation smoke test passed.

## Real Adapter result

The Python Adapter was configured with the recovered Reference Compiler directory and used to compile the real `natural-smile.cml` example.

Observed result:

```text
adapter=0.1.2
compiler=1.1.0-rc.2 (CML 1.0.0)
valid=True
format=CML-IR
source_cml_version=1.0.0
scenes=1
```

This establishes that the tested Adapter and Compiler versions interoperated successfully for this input and environment. It does not establish universal platform compatibility.

## Real cml-trust seal result

`cml-trust` called the real Adapter, received real compiled IR, and appended one `sealed_plan` record.

| Bound artifact | SHA-256 |
| --- | --- |
| CML source | `3209371fae35ec183dd798bea749ca9b1488853078b8ef7b14c06b3f744b413e` |
| Canonical compiled IR | `c3d879b67df5792681c7430a1c9b45cc207ce230aeb1866fe146e21ab1f462cd` |
| Compiler CLI entry file | `a236635e7f4455ea067882205fe8e44cff2fb1992431ac6b6ca21df822992ab8` |
| Resulting JSONL log | `49f7e01010d7b3ce1b8cd3996e52258bc5024d06aa1aa66a4691ac95bd34eff4` |

The sealed record reports `time_authority: local_clock_untrusted`. The timestamp is not claimed as trusted evidence that the plan existed before any external generation job.

Current derived project status is correctly:

```text
no_checkpoints
```

A sealed plan alone does not create observational evidence or continuity status.

## Finding: tracked conformance report is stale

`npm run verify` regenerated `reports/conformance.json`. The regenerated report described the current 51-test full conformance suite, while the committed report contained an older five-test structure. The command still returned success and left the checkout dirty.

The generated change was restored locally after inspection so the recovered Reference Compiler checkout again exactly matches commit `93d9db1`. No source code or remote repository content was changed.

This is a release-hygiene finding:

- the executed conformance suite passed;
- the tracked report artifact did not reproduce from the current suite;
- `npm run verify` does not currently enforce a zero-diff generated-artifact check.

It should be corrected in the authorized Reference Compiler control session before treating the committed report as current release evidence.

## Verdict

**Gate 1 execution result: PASS.**

The real chain executed successfully:

```text
real CML source
  -> CML Reference Compiler 1.1.0-rc.2
  -> CML Python Adapter 0.1.2
  -> canonical CML-IR hash
  -> appended cml-trust sealed_plan record
```

**Release-hygiene result: OPEN FINDING.** The tracked conformance report is stale relative to the suite that generated 51/51 passing results.

## Proof boundary

This gate proves only that the named software versions interoperated for the tested source in this environment and that `cml-trust` bound the resulting artifacts into a valid sealed-plan record.

It does not prove:

- that any generator executed the plan;
- that rendered media complied with it;
- that a person or object remained physically identical;
- that unobserved spans passed;
- market demand, originality, or patentability.

## Next gate

Gate 2 requires one actual rendered clip and extracted evidence frames. The audit must include:

1. a hashed opening checkpoint;
2. a reviewed transfer span;
3. a hashed final checkpoint;
4. a derived result that remains unresolved or coverage-limited if the transfer path is not visible.
