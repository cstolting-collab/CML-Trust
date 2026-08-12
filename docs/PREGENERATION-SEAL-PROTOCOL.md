# Pre-generation seal protocol

**Status:** Required next evidence gate; not yet completed  
**Purpose:** Test declaration-before-generation ordering without claiming that
the generator executes CML.

## Claim under test

The narrow claim is:

> A specific compile-valid CML audit plan was sealed and content-hashed before
> a new generation job was initiated, and the resulting artifact was later
> reviewed against that unchanged plan.

This is not a claim that the generator consumed or executed CML. With local
clocks and local files, it is also not cryptographic proof against an operator
who can rewrite the complete environment.

## Required inputs

- a new CML plan that has not been amended after viewing the target artifact;
- a plan-local invariant table;
- a trusted local CML Reference Compiler checkout;
- a fresh CML-Trust record store;
- an external generator or renderer;
- the final rendered video and extracted evidence frames.

## Procedure

1. Create a fresh project directory and record store.
2. Author the CML plan and invariant table before generating the target media.
3. Run `cmltrust plan seal` and preserve the appended `sealed_plan` record.
4. Record the plan id, source hash, IR hash, compiler identity, and current
   record-log hash in the experiment notes.
5. Start the external generation job without modifying the sealed plan.
6. Record the external job identifier and locally observed start/end times as
   untrusted operational metadata. Do not treat them as trusted timestamps.
7. Preserve the returned media bytes and compute the source-video hash.
8. Register the extraction manifest and frame hashes.
9. Add opening and final checkpoints using the sealed plan id.
10. Add a span review for every adjacent checkpoint pair, using the coverage
    required by the sealed plan.
11. Run `cmltrust status` and retain the complete JSONL record store.
12. Publish passes, failures, uncertain results, missing coverage, hashes, and
    the exact plan without amendment or selective deletion.

## Acceptance conditions

- The plan record exists before the locally recorded generation-job start.
- The checkpoint and span records reference the same unchanged `plan_id`.
- Source and IR hashes recompute correctly.
- Media and evidence hashes recompute correctly.
- Every adjacent checkpoint pair has the required span review.
- Any observed hard failure remains a failed observational chain.
- Any missing or insufficient span remains incomplete.

## Required disclosure

The report must state:

- whether ordering is supported only by local records or by an external
  witness;
- that a hash proves content identity, not creation time;
- that sealing before generation does not prove generator execution;
- the complete temporal coverage reviewed;
- all failures, uncertainties, occlusions, and skipped checks; and
- whether any plan amendment occurred after generation began.

## Failure conditions

The run does not satisfy this gate if:

- the plan is sealed after the generation job starts;
- the sealed plan is amended in place;
- a new plan is substituted after observing the artifact;
- checkpoints are presented as interval continuity without span review;
- unobserved material is converted into a pass; or
- failed or incomplete records are removed from the published history.
