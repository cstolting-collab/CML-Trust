# Gate 3 result — blind human replication

## Verdict

**Central defect replication: pass.**

An independent human reviewer who reported no knowledge of the prior result
identified the same central transient defect at approximately 0:03:

- hand/finger continuity changes;
- hand drift;
- a cup handle appears on each side;
- a hand reaches toward a second cup handle;
- receiving-grip/cup movement remains uncertain at that moment.

Gate 2 independently recorded a two-handle cup condition during the transfer,
with the receiving hand using the newly visible opposite-side handle instead of
the required side grip. The independently described defect class and temporal
region therefore converge.

## Comparison

| Claim | Gate 2 AI-assisted review | Blind human review | Result |
|---|---|---|---|
| Identity/person continuity | pass | pass | exact agreement |
| Cup appearance continuity | fail: transient second handle | uncertain, then described handle on each side | defect description converges; certainty differs |
| Hands/fingers | uncertain | fail: change/continuity slip near 0:03 | human supplied stronger failure classification |
| Room/light/camera | pass | pass | exact agreement |
| Boundary holder state | pass | fail, then described mid-transfer second-handle reach | original classification preserved; question interpretation remains ambiguous |
| Visible transfer path | pass | pass | exact agreement |
| Required side grip | fail | uncertain near 0:03 cup movement | same event region; certainty differs |

## What is established

This gate supplies evidence that:

1. a reviewer without the prior verdict can use the checklist to block the same
   clip from a strict observational-chain pass;
2. the reviewer can independently locate the central transient defect near the
   same part of the video;
3. the two-handle cup failure is not merely an unsupported interpretation from
   the first AI-assisted review;
4. endpoint-only review would remain inadequate because the defect is described
   during the transfer rather than at the clean final hold.

## What is not established

This gate does not establish:

- statistical inter-rater reliability from one human reviewer;
- exact agreement on every invariant or severity label;
- perfect human or AI visual detection;
- plan-conformance-at-generation;
- generator execution of CML;
- that CML improved the generated video;
- trusted timestamps or tamper-proof local provenance.

## Form defects discovered

The review procedure exposed two product defects:

1. Manual JSON editing is unsuitable for ordinary reviewers. The first human
   could not reliably save the supplied JSON form.
2. Combining opening and final holder state in one left/right question invited
   the reviewer to classify a mid-transfer defect as an endpoint failure.

Required correction:

- use a simple browser form with buttons and one export action;
- split opening holder and final holder into separate questions;
- show anatomical and screen-relative hand labels separately;
- require a description and approximate media time whenever `fail` or
  `uncertain` is selected;
- preserve the raw submission before deriving comparison results.

## Gate status

**Gate 3 passes for independent replication of the central observed defect.**

It does not pass as a broad validation study. The justified claim is narrow:
one blind human independently found the same transient two-handle continuity
failure in the same transfer region.
