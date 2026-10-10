# CML-Trust

**An alpha-stage evidence notebook for external continuity observations.**

CML-Trust records observations against compile-valid CML audit plans. It hashes plans and evidence, appends observation records, derives coverage status, and preserves revocation history. Observations do not mutate canonical CML state.

**Status:** research prototype / alpha · **Version:** `0.1.0a1` · **Language:** Python · **License:** Apache-2.0

## Scope

The implementation supports plan sealing, extract manifests, checkpoints, span reviews, and revocations. Records append to a local JSONL ledger.

It can record whether supplied evidence matches recorded hashes and whether reviewed checkpoints and intervals meet the recorded criteria. It cannot establish unobserved events, infallible reviewer judgment, trusted timestamps, or that an external generator executed CML.

## Get started

Requirements: Python 3.10–3.13, Node.js 18.19+, a trusted local CML Reference Compiler checkout, and a compatible `cml-python-adapter` 0.1.x installation.

```bash
git clone https://github.com/cstolting-collab/CML-Trust.git
cd CML-Trust
python -m venv .venv
```

Activate the environment using the command for your shell:

| Shell | Command |
| --- | --- |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

Then install and inspect the CLI:

```bash
python -m pip install cml-python-adapter==0.1.2
python -m pip install -e .
cmltrust --help
```

Plan sealing requires the compiler setup described in [installation validation](docs/INSTALL-VALIDATION.md). This project is distributed as a GitHub alpha source package; installation of the Python package alone is not a complete compiler integration.

## Validation

```bash
python -m unittest discover -s tests -v
```

This is the repository test command, not a claim that the suite was run during this documentation update.

## Documentation

| Read | Purpose |
| --- | --- |
| [Installation validation](docs/INSTALL-VALIDATION.md) | Setup evidence and installation boundaries |
| [Evidence gates](docs/EVIDENCE-GATES.md) | Validation method |
| [Model-tool integration](docs/MODEL-TOOL-INTEGRATION.md) | Optional host-side wrapper |
| [Pre-generation seal protocol](docs/PREGENERATION-SEAL-PROTOCOL.md) | Plan and evidence preparation |
| [Performance evidence rule](docs/REAL-WORKLOAD-PERFORMANCE-EVIDENCE.md) | Requirements for performance claims |
| [Publication status](docs/PUBLICATION-STATUS.md) | Distribution context |
| [Changelog](CHANGELOG.md) | Recorded changes |

## Evidence interpretation

Checkpoint results include `observed_pass`, `observed_fail`, `unobserved`, `uncertain`, `not_applicable`, and `not_checked`. Project status separately describes interval coverage and observational-chain failure or completion.

A readable opening and closing frame does not establish that the interval between them preserved continuity. Local hashes identify bytes; they do not make reviewer observations or local timestamps independently trustworthy.

## License and attribution

[Apache License 2.0](LICENSE). See [NOTICE](NOTICE) and [third-party notices](THIRD_PARTY_NOTICES).

[Estra Logics profile](https://github.com/cstolting-collab) · [Engineering Work Record](https://github.com/cstolting-collab/CML-GitHub-Work-Record)
