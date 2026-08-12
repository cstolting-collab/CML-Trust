# Changelog

## 0.1.0a1 — 2026-08-11

Initial alpha publication candidate.

- Compile-valid CML audit-plan seals with source and IR hashes.
- Content-hashed extraction manifests and checkpoint evidence.
- Per-invariant observation enums.
- Span coverage between adjacent checkpoints.
- Append-only revocation with derived descendant invalidation.
- Distinct checkpoint, incomplete-coverage, observed-failure, and complete-chain
  statuses.
- Hard observed failures take precedence over limited-coverage labels.
- Self-contained Run 006 browser-review form with local SHA-256 verification and
  one-click JSON export.
- Three evidence gates documented, including one blind human replication of the
  central Run 006 defect.

Known limitations:

- No generator integration.
- No trusted timestamps or tamper-proof storage.
- No event-evidence, repair-plan, or residual-ledger implementation.
- No statistical reviewer-reliability claim.
- CML-Trust is not published on PyPI and has not completed independent outsider
  installation or its full platform matrix. The Python adapter dependency is
  publicly available and has passed one clean local installation-and-seal
  verification.
