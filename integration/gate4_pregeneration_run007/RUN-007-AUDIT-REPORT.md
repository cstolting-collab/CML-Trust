# Operation Coffee Cup — Run 007 audit report

## Verdict

**Derived CML-Trust status: `observational_chain_failed`.**

The run achieved a readable one-shot movement from the opening holder to the
receiving hand, but it did not satisfy the sealed cup-continuity, side-grip
transfer, or final-state requirements.

## Evidence binding

| Item | Bound value |
| --- | --- |
| Plan id | `run007_pregen_plan_001` |
| CML SHA-256 | `3b80cf4fefa0cc90b2974db25e45fa8513b230981f97182ed86d4315980ade53` |
| Generation-prompt SHA-256 | `df340b391285aba67a2b8953850b11007f216693155685cea14c3709ee772cd8` |
| Source-image SHA-256 | `9e31b0625021411dc21f8693a31736814941e54db29a36775e25fc15bf0c17ca` |
| Result-video SHA-256 | `6599139afd6471bc77c4840c6a04a8116f0dcffce64319ced0c3d46fed71d4de` |
| Reviewed frames | 241/241 extracted video frames |
| Evidence-log SHA-256 | `c5355fa2b36a1381fe39a572db18a7cfe5ca705e021198fcd061a8b4fb015702` |

The seal and review clocks are local and untrusted. The local record order and
conversation workflow support that the plan and exact generation inputs were
sealed before the result was submitted, but they are not third-party proof of
time and do not show that the generator executed CML.

## Observed results

| Claim | Result | Evidence |
| --- | --- | --- |
| Identity and appearance continuity (`inv_001`) | `observed_pass` | Same woman, face, hair, clothing, earrings, and necklace throughout the inspected frames. |
| One appearance-continuous single-handle cup (`inv_002`) | `observed_fail` | A screen-left handle forms during the transfer while the original screen-right handle remains. It is clear by extracted frame 87 (~3.58 s). |
| Plausible hand anatomy (`inv_003`) | `observed_pass` | No clear fused, missing, or extra-finger defect was found in the full-frame review. |
| Room/camera continuity (`inv_004`) | `observed_pass` | Background, lighting, framing, and camera orientation remain continuous. |
| Opening configuration (`inv_005`) | `observed_pass` at opening sample | Cup starts in the screen-right hand by its original handle; screen-left hand is open, empty, and separated. |
| Required transfer path (`inv_006`) | `observed_fail` | The receiving hand takes the emergent second handle rather than the lower cup body with a side grip. |
| Required final configuration (`inv_007`) | `observed_fail` | Receiver becomes sole holder and the endpoint is held, but it holds a handle, the cup has two handles, and the released hand is curled rather than open. |
| Unhidden continuous shot (`inv_008`) | `observed_pass` | The transfer interval is visible without a detected cut, dissolve, occlusion, viewpoint reversal, or frame exit. |

## Timeline of the decisive defect

- Opening hold: approximately frames 1–60.
- Receiving hand approaches: approximately frames 61–78.
- Screen-left handle begins to form: approximately frame 79 (~3.25 s).
- Two handles clearly visible: by frame 87 (~3.58 s).
- Original screen-right hand releases: approximately frames 115–121
  (~4.75–5.00 s).
- Final receiving-hand-only state: approximately frame 121 through frame 241,
  more than the required two-second hold.

Frame numbers above are one-based extracted filenames; times are display
approximations derived from the 24 fps stream. The canonical extract manifest
stores zero-based frame indices, SHA-256 values, and integer PTS.

## What this run establishes

It establishes a narrow artifact-level result: predeclared, hashed invariants
plus every-frame span review caught a transient prop mutation and separated it
from otherwise successful endpoints. The final holder changed as intended,
but endpoint success did not launder the failed transition.

It does **not** establish generator conformance, statistical performance,
causal improvement from CML, trusted chronology, or general reliability.

## Tooling issue exposed

The alpha schema cannot yet express that one hard node invariant governs only
at the opening checkpoint while another governs only at the final checkpoint.
Both were sealed with `governs: always` because that is the only implemented
mode. The irrelevant endpoint results were therefore stored as `not_checked`,
making the opening node incomplete. This is fail-closed and honest, but the
next schema delta should add plan-derived checkpoint roles or phases without
allowing reviewers to self-authorize `not_applicable`.

## Independent blind review

One human reviewer, watching on a phone without knowing the expected result or
the primary review, independently marked cup continuity and the visible
transfer as failed. In follow-up, she reported that at approximately four
seconds “two coffee cup handles appear” and that the screen-left handle was
partial. She also independently marked the final released screen-right hand as
closed and the shot itself as continuous.

She marked the receiving grip uncertain and did not independently resolve the
precise grip mechanism. The full response is preserved verbatim in
`BLIND-REVIEW-01.md`. This is corroboration from one reviewer under limited
phone-viewing conditions, not statistical validation and not an authoritative
multi-validator fusion result.
