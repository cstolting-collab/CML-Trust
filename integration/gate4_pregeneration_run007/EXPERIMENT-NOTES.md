# Operation Coffee Cup Run 007 — pre-generation gate

**Current state:** Post-generation evidence registered and reviewed; the derived
project status is `observational_chain_failed`.

This experiment tests only whether a compile-valid CML audit plan and exact
generation inputs were locally sealed before a new external generation job,
then preserved unchanged through post-generation review.

It does not claim that the generator consumes or executes CML. Local hashes
bind bytes but do not prove creation time against an operator able to rewrite
the complete local environment.

The source still was deliberately corrected before sealing because the prior
image already showed both hands touching the cup and therefore could not
support an unambiguous one-hand opening-state claim.

After sealing, do not modify the CML plan, invariant table, prompt, or source
image. Any change requires a new plan id and a new record store.

## Pre-seal compilation history

The first local compile attempt included a second `PAUSE` after `TRANSITION`
and was rejected with `CML-E104` because it violated CML's normative execution
order. No `sealed_plan` record was appended and no generation had begun. The
invalid trailing pause was removed before the plan was sealed; the required
two-second final hold remains explicit in the invariant table and generation
prompt.

## Sealed snapshot

- Plan id: `run007_pregen_plan_001`
- CML SHA-256: `3b80cf4fefa0cc90b2974db25e45fa8513b230981f97182ed86d4315980ade53`
- IR SHA-256: `dbe0753539fc1c721729b257bcdb46d41209f92b93f786784cd9d5768358ded2`
- Prompt SHA-256: `df340b391285aba67a2b8953850b11007f216693155685cea14c3709ee772cd8`
- Source-image SHA-256: `9e31b0625021411dc21f8693a31736814941e54db29a36775e25fc15bf0c17ca`
- Initial JSONL SHA-256: `c7dad5b511ff8fd1a3d5f33b37be72264ee83dbce85ccbb1011f71ae382e49fa`
- Compiler: `cml-reference-compiler 1.1.0-rc.2 (CML 1.0.0)`

The immutable sidecar snapshot is
`PREGENERATION-SEAL-MANIFEST.json`. It is not a canonical CML-Trust record and
does not upgrade the local clock into trusted time.

## Post-generation review

- Source-video SHA-256: `6599139afd6471bc77c4840c6a04a8116f0dcffce64319ced0c3d46fed71d4de`
- Video stream: H.264, 1264×720, 24 fps, time base `1/12288`
- Extracted frames: 241, all registered with SHA-256 and integer PTS
- Coverage: every extracted video frame reviewed
- Evidence-log SHA-256 after review: `c5355fa2b36a1381fe39a572db18a7cfe5ca705e021198fcd061a8b4fb015702`

The opening state is observed as requested. During the transition, a second
handle begins forming on the screen-left side of the cup and is clearly
established by extracted frame 87 (frame index 86, approximately 3.58 s),
while the original screen-right handle remains. The receiving screen-left hand
takes this emergent handle instead of gripping the lower cup body. The original
screen-right hand releases at approximately 4.8–5.0 s. A receiving-hand-only
endpoint is then held for more than two seconds, but the cup is two-handled,
the receiver is not using the required body side grip, and the released hand
remains curled rather than open.

Observed hard failures:

- `inv_002`: the sealed single-handle cup appearance is not continuous;
- `inv_006`: the required lower-body side-grip transfer path is not completed;
- `inv_007`: the final grip and released-hand configuration do not match the
  sealed endpoint requirement.

Identity, hand anatomy, room/camera continuity, and shot visibility were marked
observed pass. These are narrow observational findings about this artifact,
not validation of a generator or of CML as causal control.

## Alpha applicability limitation found by the experiment

The sealed invariant table describes `inv_005` as opening-checkpoint-specific
and `inv_007` as final-checkpoint-specific, but the `trust.v1` alpha accepts
only `governs: always`. Therefore the current tool cannot formally mark the
opposite endpoint as non-governing. The review records use `not_checked` for
the irrelevant endpoint-specific claim, which correctly prevents a false
complete-node claim but leaves the opening node derived as incomplete.

This schema limitation did not cause the overall failure: the final node and
the reviewed span contain direct observed failures. It does identify a future
need for tool-derived checkpoint-role applicability rather than reviewer-chosen
`not_applicable`.
