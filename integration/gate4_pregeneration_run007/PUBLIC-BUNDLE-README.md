# Operation Coffee Cup — Run 007 evidence bundle

This directory publishes the compact evidence record for the first CML-Trust
pre-generation-seal experiment.

## Result

`observational_chain_failed`

The opening and final holder states were readable, but every-frame review found
that a second cup handle formed during the transfer. The receiving hand used
that emergent handle instead of the sealed lower-body side grip, and the
released hand remained closed. One blind human reviewer watching on a phone
independently reported two handles at approximately four seconds, a failed
transfer, a closed released hand, and a continuous shot.

## Contents

- `RUN-007-AUDIT-REPORT.md` — complete bounded claim and findings
- `BLIND-REVIEW-01.md` — verbatim blind-review answers and limits
- `EXPERIMENT-NOTES.md` — seal history, review history, and alpha limitation
- `operation-coffee-cup-run007.cml` — compile-valid plan source
- `generation-prompt.txt` — exact generation prompt sealed before submission
- `invariants.json` — sealed operational invariant table
- `PREGENERATION-SEAL-MANIFEST.json` — noncanonical pre-generation sidecar
- `opening-results.json`, `final-results.json`, `span-results.json` — submitted
  observations
- `records.jsonl.gz` — gzip-compressed canonical five-record ledger
- `SHA256SUMS` — byte hashes for the published bundle and omitted media

## Media boundary

The 241 extracted PNG frames and source MP4 are omitted from Git because they
are large generated-media artifacts. Their SHA-256 bindings remain in the
canonical ledger and audit report. The omitted result video SHA-256 is:

`6599139afd6471bc77c4840c6a04a8116f0dcffce64319ced0c3d46fed71d4de`

The bundle does not establish that a generator consumed or executed CML. It
does not provide trusted timestamps, statistical validation, or a general
performance claim. It establishes only the recorded artifact-level findings
relative to the published, fallible local seal and review procedure.
