# CML-Trust — Alpha

**Problem:** External observations (logs, agent outputs, CI results) get mixed into canonical state and you can't tell what is trusted.

**What breaks without it:** An agent writes a bad checkpoint, you recover from it, and you never know it was untrusted. You ship a state you never accepted.

**30 sec try:**
```bash
git clone https://github.com/cstolting-collab/CML-Trust
cd CML-Trust
python -m pip install -e .
cmltrust --help
# See docs/INSTALL-VALIDATION.md for compiler setup and plan sealing.
```

**Evidence:**
- Method: canonical state != noncanonical evidence. Observation does not mutate state.
- Alpha implementation: plan sealing, append-only observations, derived status, and revocation history.
- Status: alpha-stage, breaking changes expected. Not a theorem prover.

License: [Apache-2.0](LICENSE) · Topics: cml, continuity, validation, trust, evidence
