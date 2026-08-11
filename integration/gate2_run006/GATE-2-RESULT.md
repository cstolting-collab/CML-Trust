# Gate 2 result — Operation Coffee Cup Run 006

## Verdict

**Gate 2 correctly rejects the observational chain.**

The opening and final checkpoints are individually complete, but the reviewed
transfer span contains a visible hard continuity failure. The derived project
status is:

```text
observational_chain_failed
```

Blocking invariants:

```text
inv_002 — single appearance-continuous cup
inv_007 — receiving-hand side-grip path
```

This is not a claim that every possible defect was found. It is a claim that
the recorded evidence contains enough visible information to reject these two
hard invariants.

## Artifact and media clock

- Artifact: `grok-video-7ef6d779-2fdc-4039-afc5-0aa520238725 (4).mp4`
- Source video SHA-256: `27af50dc6d7c2f5b0967deed1d55cd9290474f02faa6658317cbe988228615fe`
- Reviewed video stream: index 0, H.264, 1264×720
- Frame rate: 24/1
- Video timebase: 1/12288
- Duration: 123392 video ticks
- Decoded frames: 241
- Reviewed PTS range: 0 through 122880, step 512
- Audio: AAC, 48000 Hz, timebase 1/48000

The container also has an MJPEG attachment stream. It was not treated as the
reviewed moving-picture stream.

## Retrospective audit-plan seal

- CML source SHA-256: `d7384abba8c5d733dd31f8c6a191f40c4237572b79914e5722e029d8b01a7ba3`
- Compiled IR SHA-256: `ef1651493bb1bb71b70d1fb6733e8fe84bbd212dd4084cb1a072732e63b89028`
- Compiler: `cml-reference-compiler 1.1.0-rc.2 (CML 1.0.0)`
- Compiler entry SHA-256: `a236635e7f4455ea067882205fe8e44cff2fb1992431ac6b6ca21df822992ab8`
- Compile result: valid, zero issues

This CML audit plan was compiled and sealed **after the video already existed**.
It operationalizes the original Run 006 instructions for retrospective review;
it is not evidence that a sealed CML plan governed generation.

The compiler proves that the audit plan is valid CML and binds the resulting
IR. It does not prove that Grok executed the plan, that this plan existed before
generation, or that the rendered pixels comply.

## Review method

All 241 extracted frames were inspected in chronological order using complete
30-frame sheets, transfer-focused sheets, and selected full-resolution frames.
The observations were entered as an **AI-assisted visual review with human
confirmation pending**. This is not represented as an independent human audit.

The source video, every decoded frame, the two checkpoint frames, the plan, and
the observation results are content-hashed in the local evidence record.

The original extraction command was not captured at extraction time. The
manifest states that limitation and therefore does not claim command-level
extraction reproducibility.

## Findings

| Claim | Result | Evidence summary |
|---|---|---|
| Opening holder state | observed pass | Cup begins in anatomical left hand; anatomical right hand is separated. |
| Final holder state | observed pass | Cup ends in anatomical right hand; released hand is open and separated for the final hold. |
| Person/clothing continuity | observed pass | No decisive identity, clothing, jewelry, or hair discontinuity found in the reviewed frames. |
| Cup appearance continuity | **observed fail** | During the transfer the cup visibly develops a second handle while the original handle remains present. The final endpoint later returns to a one-handle appearance. |
| Complete visible transfer path | observed pass | The hand approach, shared contact, release, and final hold remain visible; the transition is not hidden by a cut. |
| Required lower-side receiving grip | **observed fail** | The receiving hand takes an apparent newly generated left-side handle rather than the required lower-side body grip. |
| Hand anatomy throughout | uncertain | Some transfer frames do not support a confident all-frame finger-count pass. This uncertainty is recorded and not converted to a pass. |
| Room/light/camera continuity | observed pass | No decisive hard discontinuity found in the reviewed span. |

The two-handle condition is clear in the transfer region, including selected
source frame indices around 48, 64, 80, 96, and 112. The final frame alone
would not reveal it.

## Derived structure

```text
C_pre:  complete
C_post: complete
C_pre → C_post span: observed_fail
  blockers: inv_002, inv_007

project: observational_chain_failed
```

This is the concrete value of node-versus-span separation: valid endpoint
samples do not launder a failed interval.

## Correctness change discovered by the real artifact

The original three-way project vocabulary had no distinct status for a span
where a hard defect was actually observed. It would have collapsed that result
into `coverage_incomplete`, which is materially weaker and misleading.

Gate 2 therefore added and tested:

```text
observational_chain_failed
```

It also changed span derivation so an observed hard failure outranks a limited
coverage label. Limited coverage restricts claims about unseen frames; it does
not erase a defect already seen.

## What this gate demonstrates

This run demonstrates that the current vertical slice can:

1. compile and seal a real retrospective CML audit plan through the published
   Python adapter;
2. bind a specific source video and 241 decoded frames with SHA-256;
3. store complete endpoint samples without inferring interval success;
4. record a full-frame span review;
5. derive a failed chain from hard invariant results without a manual pass bit;
6. expose a transient defect that is absent from the final endpoint.

## What this gate does not prove

It does not prove:

- that the generator executed CML;
- plan-conformance-at-generation or pre-generation CML commitment;
- physical identity of the woman or cup;
- that the visual reviewer cannot miss a semantic defect;
- independent human confirmation;
- extraction fidelity beyond the registered media, PTS metadata, frame hashes,
  and stated command-capture limitation;
- tamper-proof local history or trusted time;
- that CML improves generation quality by itself.

## Evidence files

- Canonical append-only log: `records.jsonl`
- Log SHA-256 at completion: `915f775ee05c5732de70d4cf258fe162bfa88d3d43266383d6f8394ae98aab55`
- Extract descriptor: `extract-descriptor.json`
- Full contact sheet: `contact_sheet.png`
- Transfer contact sheet: `transfer_contact_sheet.png`
- Extracted source frames: `frames/`
- Ordered every-frame sheets: `sheets/`

## Gate status

**Engineering gate: pass. Media continuity claim: fail.**

That distinction is intentional. The tool passed because it refused to certify
a visually failed span whose endpoints looked acceptable.
