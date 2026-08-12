# Adjacent Research and Technical Distinctions

## CML, LUFF, Trusted Checkpoints, and CML-Trust

**Status:** Working research note, version 0.2  
**Date:** 2026-08-11  
**Purpose:** Identify relevant prior research and standards while stating where
the CML architecture is technically different.  
**Not claimed:** endorsement by Harvard University, Stanford University, any
cited author, or any standards body.

## 1. Executive conclusion

The reviewed sources do not describe Continuity Markup Language (CML), LUFF,
Trusted Checkpoints, and CML-Trust as one existing system. They do establish
several mature neighboring ideas:

1. continuous experience is cognitively divided at meaningful event
   boundaries;
2. gesture and reciprocal action can carry information before or alongside
   speech;
3. pauses and silence can function as temporal and communicative signals;
4. state, event order, and causality require explicit representations;
5. provenance records support judgments about the origin and reliability of
   evidence; and
6. language-model control and long-context stability remain active research
   problems.

These sources support the *problem framing* behind CML. They do not validate
the CML implementation, prove LUFF's proposed temporal law, establish a
universal `0.05` coefficient, or show that a media generator executes either
system.

The possible technical contribution is therefore a domain-specific
engineering synthesis: declarative continuity invariants, temporal pacing,
state transitions, checkpoint and span evidence, provenance, revocation, and
claim-specific derived status for generated timed media.

## 2. System terms and current implementation boundary

### 2.1 Continuity Markup Language (CML)

CML is intended to declare continuity-relevant entities, states, locks,
actions, events, and constraints across timed media. It is not a pixel model,
identity model, video codec, or generator.

### 2.2 LUFF

LUFF is the proposed global temporal-governor layer for observable pacing:
anticipation, body and hand movement, facial transition, environmental motion,
camera motion, speech cadence, silence, reaction spacing, and settling.

LUFF is conceptually separate from LUFS, the established acoustic-loudness
measurement. The sources below do not use the term LUFF in this sense.

### 2.3 Trusted Checkpoint

A Trusted Checkpoint is not a declaration that pixels reveal physical identity
or absolute truth. In the architecture, it is a named state boundary carrying
a specified certificate: for example, a content-hashed observation with
explicit invariant results, lineage, coverage, and provenance.

### 2.4 CML-Trust

CML-Trust is an external audit notebook. The public `0.1.0a1` alpha currently
implements:

- compile-valid CML audit-plan seals;
- source and compiled-IR hashes;
- extraction manifests and frame hashes;
- checkpoint observations;
- interval and boundary-window span reviews;
- append-only revocation;
- derived incomplete, failed, and complete observational-chain status.

It does **not** currently implement LUFF execution, generator integration,
event-phase certification, bridge repair, a residual audio-clock ledger,
multi-validator fusion, trusted timestamps, or tamper-proof storage.
The alpha neither implements nor tests a LUFF `0.05` coefficient.

## 3. Adjacent research

### 3.1 Event boundaries and the segmentation of continuous experience

Research in cognitive neuroscience reports that temporal structure plays a
major role in understanding everyday events.
Observers divide ongoing activity into meaningful parts, and brain activity is
time-locked to salient event boundaries during both intentional segmentation
and passive viewing.

A later human-neuron study describes experience as continuous while memory is
organized into discrete events. Boundary-related neural changes helped
structure episodic memory, although the study also found a tradeoff between
content memory and temporal-order memory.

**Relevance to CML:** This supports treating transitions and settled boundaries
as first-class objects rather than treating video as an undifferentiated frame
stream.

**Technical distinction:** Cognitive event segmentation describes how humans
perceive and remember experience. CML declares expected media states and
transitions; CML-Trust records evidence about whether particular artifacts
were observed to satisfy them. Cognitive research does not supply CML's schema
or certify its outputs.

Sources:

- Zacks et al., “Human brain activity time-locked to perceptual event
  boundaries,” *Nature Neuroscience* (2001), [journal article; authors were
  affiliated with Washington
  University](https://www.nature.com/articles/nn0601_651).
- Zheng et al., “Neurons detect cognitive boundaries to structure episodic
  memories in humans,” *Nature Neuroscience* (2022), [Harvard Medical School
  publication record](https://eye.hms.harvard.edu/publications/neurons-detect-cognitive-boundaries-structure-episodic-memories-humans).

### 3.2 Gesture and communication before or alongside words

Developmental research by University of Chicago authors found that children's
early gesture use predicted later vocabulary size even after accounting for
early spoken-word use. Related Harvard educational material describes
pointing as a way for children to communicate and elicit verbal information
before they can produce the corresponding words.

Harvard's Center on the Developing Child also describes “serve and return” as
contingent, reciprocal interaction that begins before babies can talk.

**Relevance to CML:** Meaningful continuity is multimodal. A hand movement,
gaze shift, object transfer, response delay, or reciprocal action cannot be
reduced to the words in a transcript.

**Technical distinction:** Developmental research observes relationships among
gesture, interaction, and language acquisition. CML attempts to encode
media-production obligations such as ordering gaze before head movement or
requiring shared contact during an object transfer.

Sources:

- Rowe, Özçalışkan, and Goldin-Meadow, “Learning words by hand: Gesture's role
  in predicting vocabulary development” (2008), [journal article; authors
  were affiliated with the University of
  Chicago](https://journals.sagepub.com/doi/10.1177/0142723707088310). A copy
  is also [hosted by Harvard
  DASH](https://dash.harvard.edu/entities/publication/73120378-db78-6bd4-e053-0100007fdf3b).
- Center on the Developing Child at Harvard University, [“5 Steps for
  Brain-Building Serve and
  Return”](https://developingchild.harvard.edu/resources/videos/how-to-5-steps-for-brain-building-serve-and-return/).

### 3.3 Silence, pauses, turn-taking, and prosody

Stanford work on voice-assistant turn-taking describes thinking pauses,
intonation changes, and backchannels as signals humans use to determine whether
someone is continuing or yielding a turn. Separate Stanford research found
that listeners differ in how they interpret overlap and silence: some treat
overlapping talk as engagement, while others prefer one speaker at a time.

Stanford Humanities work on performed poetry treats pitch, timing, line
breaks, and measurable pauses as part of prosodic form. A Harvard-hosted study
of conversational pause-fillers likewise shows that filled pauses vary
systematically across language-contact communities.

**Relevance to LUFF:** Silence is not necessarily empty duration. It may carry
turn state, anticipation, uncertainty, emphasis, breath, reaction, or settle.
Removing it can change the perceived action or compress multiple transitions
into an unreadable interval.

**Technical distinction:** The cited work studies human language and
interaction. LUFF proposes a renderer-neutral temporal envelope spanning not
only speech but bodies, hands, faces, objects, camera, and environment. No
cited source establishes LUFF's name, implementation, or coefficient.

Sources:

- Stanford HAI, [“Is It My Turn Yet? Teaching a Voice Assistant When to
  Speak”](https://hai.stanford.edu/news/it-my-turn-yet-teaching-voice-assistant-when-speak).
- Stanford Report, [“Exploring what an interruption is in
  conversation”](https://news.stanford.edu/stories/2018/05/exploring-interruption-conversation).
- Stanford Humanities Center, [“After Scansion: Visualizing, Deforming, and
  Listening to Poetic
  Prosody”](https://shc.stanford.edu/arcade/interventions/after-scansion-visualizing-deforming-and-listening-poetic-prosody).
- Instituto Cervantes at Harvard, [“What We Say When We Say Nothing at
  All”](https://cervantesobservatorio.fas.harvard.edu/en/reports/what-we-say-when-we-say-nothing-all-clues-contact-induced-language-change-spanish).

### 3.4 State models and reactive systems

David Harel's Statecharts extend conventional state-transition diagrams with
hierarchy, concurrency, and communication for complex reactive systems.

**Relevance to CML:** Timed media can contain concurrent state: a person,
object, camera, environment, and audio layer may change simultaneously while
remaining subject to different invariants.

**Technical distinction:** Statecharts are a general formalism for reactive
systems. CML is intended as a domain-specific language for continuity and
timed-media declarations. Any claim of formal verification for CML would
require its own semantics, conformance suite, and proofs; resemblance to state
machines is not such proof.

Source:

- Harel, “Statecharts: A Visual Formalism for Complex Systems,” *Science of
  Computer Programming* (1987), [Weizmann Institute publication
  record](https://weizmann.elsevierpure.com/en/publications/statecharts-a-visual-formalism-for-complex-systems/).

### 3.5 Event ordering is not the same as wall-clock time

Leslie Lamport's work on distributed systems distinguishes causal event order
from physical clock time and formalizes a “happened-before” relation.

**Relevance to CML-Trust:** A content hash identifies bytes but does not prove
when those bytes existed. Similarly, a storyboard schedule does not prove that
a rendered event occurred. Event order, local timestamps, content integrity,
and semantic occurrence must remain separate claims.

**Technical distinction:** Lamport addresses distributed-computing event
ordering. CML-Trust uses much simpler local records and explicitly does not
claim trusted time or distributed consensus.

Source:

- Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,”
  *Communications of the ACM* (1978), [Microsoft Research publication
  record](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/).

### 3.6 Provenance and responsibility

The W3C PROV Data Model defines provenance through entities, activities,
agents, derivations, responsibility, and time-related relations. It explicitly
connects provenance information with assessments of quality, reliability, and
trustworthiness. It can also represent a plan as an entity associated with an
activity.

**Relevance to CML-Trust:** Plans, compiled artifacts, media, extractions,
observations, reviewers, amendments, and revocations are provenance-bearing
objects. The history of an artifact cannot be repaired merely by applying a
new label.

**Technical distinction:** W3C PROV is domain-agnostic and substantially more
general. CML-Trust is a narrow local schema for media-continuity evidence. The
alpha is not currently a W3C PROV implementation and should not claim PROV
conformance.

Source:

- W3C, [PROV-DM: The PROV Data Model, W3C Recommendation (30 April
  2013)](https://www.w3.org/TR/prov-dm/).

### 3.7 Mechanistic control of language models

A 2025 Harvard dissertation on mechanistic control of language models examines
world representations, internal knowledge, attention decay, user
representation, system-prompt stability, planning, and hallucination.

**Relevance to the wider CML program:** It confirms that model control and
long-context stability are active technical problems, not solved merely by
writing longer prompts.

**Technical distinction:** The dissertation studies internal language-model
mechanisms. CML-Trust is intentionally external and renderer-neutral. It
records what was declared and what was observed without claiming access to a
generator's internal state.

Source:

- Li, “Mechanistic Control of Language Models” (2025), [Harvard DASH
  record](https://dash.harvard.edu/items/23c45a6c-b171-428b-9fa4-723e73077026).

### 3.8 Multimedia metadata and timeline annotation

Established media standards already describe audiovisual resources through
timeline positions, durations, parts, timed annotations, and structural
metadata. EBUCore 1.10, for example, defines video and audio time-point
references and describes ways to localize editorial parts, props, timed text,
actions, and emotions on an audiovisual timeline. Timed-text standards likewise
associate content and styling with explicit temporal intervals.

**Relevance to CML:** These systems demonstrate that timed-media intervals,
events, objects, and annotations are established technical concepts. They are
important prior art for any claim that CML alone introduced time-addressed
media description.

**Technical distinction:** Multimedia metadata standards primarily describe,
exchange, locate, or present media information. The proposed CML-family
synthesis adds plan-scoped continuity obligations, content-bound human
observations, checkpoint/span coverage, derived completeness or failure, and
non-erasing revocation. CML-Trust does not currently implement or claim
conformance with EBUCore, MPEG-7, or TTML.

Sources:

- European Broadcasting Union, [EBUCore Metadata Set, Tech 3293 v1.10
  (2020)](https://tech.ebu.ch/docs/tech/tech3293.pdf).
- W3C, [Timed Text Markup Language 2 (TTML2), W3C Recommendation](https://www.w3.org/TR/ttml2/).

### 3.9 Temporal logic and runtime verification

Temporal logics provide formal ways to state properties that must hold across
ordered executions, timed behaviors, or continuous signals. Signal Temporal
Logic was introduced for specifying and monitoring temporal properties of
continuous signals, including automated checks over bounded traces.

**Relevance to CML:** Statements such as “a condition holds throughout an
interval,” “one state must precede another,” or “an event must eventually
occur” have mature formal relatives. CML's temporal obligations therefore
need direct semantic comparison with temporal-logic and runtime-verification
systems.

**Technical distinction:** CML-Trust `0.1.0a1` evaluates a small,
domain-specific evidence model over externally rendered media and human review
records. It is not an LTL, MTL, MITL, or STL parser, theorem prover, model
checker, or signal monitor. Any future formal-verification claim would require
defined CML semantics and an implementation that can be compared against those
systems.

Source:

- Maler and Nickovic, “Monitoring Temporal Properties of Continuous Signals”
  (2004), [institutional publication
  record](https://research-explorer.ista.ac.at/record/4372).

## 4. Technical-distinction matrix

| Adjacent field | Established neighboring idea | CML-family distinction |
|---|---|---|
| Event segmentation | Continuous experience is parsed at meaningful boundaries | Declared state transitions plus artifact-specific node and span evidence |
| Gesture research | Movement can communicate before or alongside speech | Operational invariants for gaze, hands, object ownership, and action order |
| Turn-taking and prosody | Silence and timing can carry communicative structure | A proposed global envelope across speech, body, objects, camera, and environment |
| Statecharts | Complex systems can be represented through hierarchical and concurrent states | Timed-media continuity vocabulary and domain-specific acceptance rules |
| Distributed event ordering | Causal order is distinct from physical time | Separate plan schedule, observed occurrence, media PTS, local timestamps, and hashes |
| W3C provenance | Entities, activities, agents, plans, and derivations can be recorded | Specialized append-only continuity evidence and derived release-profile claims |
| Mechanistic model control | Internal representations can provide surfaces for intervention | External audit without claiming generator internals or execution |
| Multimedia metadata and annotation | Time points, parts, props, actions, and timed text can be located on audiovisual timelines | Plan-scoped continuity obligations plus content-bound checkpoint/span evidence and derived status |
| Temporal logic and runtime verification | Formal properties can be evaluated across ordered traces or continuous signals | Human-evidence audit over rendered media; the alpha is not a temporal-logic parser or model checker |

## 5. The proposed synthesis

The architecture can be summarized as:

```text
sealed declarations
  → generated artifact
  → content-bound extraction
  → checkpoint observations
  → interval and transition review
  → derived claim-specific status
  → append-only amendment or revocation
```

The important synthesis is not any single arrow. It is the refusal to collapse
them:

- a plan hash is not proof of plan timing;
- a scheduled event is not an observed event;
- a valid endpoint is not a valid interval;
- separate attribute sightings do not prove a joint relation;
- an unobserved invariant is not a pass;
- a later seal does not cleanse earlier lineage;
- local conformance does not erase adaptive ancestry;
- integrity does not guarantee semantic truth; and
- “trusted” is incomplete unless the certificate names the claim or release
  profile.

## 6. Current evidence and permissible claims

### 6.1 Directly supported

The current public alpha and its recorded tests support these engineering
claims:

- compile-valid CML audit plans can be content-bound to compiled IR;
- extracted frames and checkpoints can be content-hashed;
- checkpoint state and interval coverage can be represented separately;
- missing spans prevent a complete observational-chain status;
- an observed hard span failure produces a failed chain even when endpoints
  are individually complete;
- revocation can remain append-only while descendant invalidation is derived.

Operation Coffee Cup Run 006 additionally supports one narrow artifact-level
finding: full-interval review found a transient two-handle cup defect that clean
endpoint samples missed, and one blind human independently described the same
central defect near the same temporal region.

### 6.2 Reasonable design inferences

The adjacent research makes these design choices reasonable to investigate:

- represent event boundaries explicitly;
- preserve gesture, reaction, silence, and settle as observable temporal
  structure;
- assess nodes and intervals separately;
- retain provenance and amendment history; and
- use claim-specific certificates rather than one undifferentiated trust bit.

These are research-motivated engineering choices, not externally validated
performance claims.

### 6.3 Not established

Current evidence does not establish:

- that a generator executed CML or LUFF;
- that CML or LUFF improves generation quality;
- that `0.05` is a universal or optimal temporal coefficient;
- that a content hash proves when a plan existed;
- that pixels establish physical identity;
- that CML is the first system ever to address continuity;
- that Harvard, Stanford, or any cited researcher endorses the architecture;
- that one artifact and one blind human constitute statistical validation; or
- that local JSONL storage is tamper-proof.

## 7. Novelty and prior-art boundary

This note is not a patentability opinion, exhaustive literature review, or
legal prior-art search.

The component ideas—state machines, temporal constraints, provenance, event
segmentation, gesture, prosody, checkpoints, and audit logs—have substantial
prior histories. Any defensible originality claim must therefore concern a
specific combination, schema, execution law, or demonstrated behavior and must
be tested against both academic literature and existing production systems.

The safe present wording is:

> CML is an independently developed continuity-declaration architecture whose
> combination of timed-media invariants, temporal governance, checkpoint/span
> evidence, and claim-specific provenance is being evaluated against adjacent
> research and existing technical systems.

## 8. Required validation before stronger claims

1. **Independent installation:** A person outside the development sessions
   installs the public repositories using only published instructions.
2. **Pre-generation sealing:** Plans are sealed before generation, with an
   auditable job-to-plan binding.
3. **True control conditions:** Compare CML/LUFF configurations with a genuine
   no-CML/no-LUFF condition; do not infer causality from two treatments that
   both contain the tested mechanism.
4. **Blinded review:** Use multiple reviewers who do not know the expected
   result, with preserved raw submissions and predeclared questions.
5. **Multiple artifacts and generators:** Test transient, relational,
   identity, object, camera, and timing failures across different systems.
6. **Coverage disclosure:** Record full-frame, sampled, unobserved, occluded,
   and uncertain regions separately.
7. **Failure reporting:** Publish failures and ambiguous results alongside
   passes.
8. **Formal comparison:** Compare the CML semantics directly with statechart,
   temporal-logic, workflow, provenance, and multimedia-annotation systems.

## 9. Strongest honest conclusion

Research from Harvard, Stanford, and foundational computer science supplies
credible intellectual neighbors for the problems CML addresses: event
boundaries, multimodal communication, silence and timing, state transitions,
causal order, provenance, and model stability.

It does not supply an endorsement or validation of CML.

The present contribution is a testable engineering proposition: continuity in
timed generative media should be declared as state and transition obligations,
reviewed across both checkpoints and intervals, and certified only through
claim-specific evidence with non-erasing provenance.
