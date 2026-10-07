# Dated CML Provenance Record

This record identifies prior implementation points in the private CML reference repository. The hashes are preserved here as dated provenance. The source repository remains private; access can be granted for technical review.

| Date | Commit | Evidence |
|---|---|---|
| 2026-08-20 | `a4eb6bb49555a8884e6f899c2dadb90b0ff2426a` | Domain-neutral state governance: explicit lifecycle, declarative invariants, provenance, hardened state-data boundaries, rejection before canonical commit. |
| 2026-08-20 | `67ac4fa72eef470966d69c6a8d58eba2e6a19aa5` | Deterministic bounded read-only continuity projection with freshness validation and resource limits. |
| 2026-08-20 | `767bd33cda8c93ab4e00c56a9324e5bdd3ab4047` | Guarded continuity checkpoint recovery. |
| 2026-08-27 | `3408dc28776dcef5da8275386d645a1f481a0c88` | Canonical lock transition test: identical candidate REJECT while locked, ACCEPT after authorized unlock; evaluation does not mutate canonical accepted state. |
| 2026-08-29 | `77bbb2de9ca1e40532d8a111f0edb6ebc9b3419d` | External observation conformance: PASS / FAIL / UNEVALUABLE, noncanonical evidence, evidence digesting, tamper-detection, fail-closed validation. |
| 2026-09-24 | `48913accb22a44efcef727a8b00ae893549671a8` | Fail closed before unapproved external workflow writes. |
| 2026-10-02 | `b49442158ea490eed1aa422e2c65d84a5b234e83` | EXP010 and continuity-preservation find/fix receipt. |

## Publicly reproducible statement

The public demo in this bundle is a minimal independent reproduction of the verification pattern above. It is not represented as a byte-for-byte publication of the private implementation.

## Non-claims

This record does not establish that CML:

- invented formal verification;
- is equivalent to a theorem prover;
- replaces perception, planning, policy, or learned memory;
- is safe for safety-critical autonomy without domain validation;
- has been adopted by OpenAI or any other external organization;
- proves all continuity properties in arbitrary systems.
