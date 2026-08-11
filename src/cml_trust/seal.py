from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .hashutil import sha256_canonical_json, sha256_file
from .schema import SCHEMA_VERSION, validate_record


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def seal_plan(
    source_path: str | Path,
    plan_id: str,
    invariant_table: dict[str, Any],
    accepted_coverage: list[str],
    compiler_factory: Callable[[], Any] | None = None,
) -> dict[str, Any]:
    source = Path(source_path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    if compiler_factory is None:
        from cml_adapter import CMLCompiler

        compiler_factory = CMLCompiler

    compiler = compiler_factory()
    result = compiler.compile_file(source)
    if not result.valid or result.ir is None:
        summary = "; ".join(
            f"{item.code}: {item.message}" for item in result.diagnostics
        ) or "CML compilation failed"
        raise ValueError(f"COMPILE_FAILED: {summary}")

    version = compiler.version()
    compiler_entry_hash = None
    cli_path = getattr(compiler, "cli_path", None)
    if cli_path is not None and Path(cli_path).is_file():
        compiler_entry_hash = sha256_file(cli_path)

    record = {
        "kind": "sealed_plan",
        "schema_version": SCHEMA_VERSION,
        "id": plan_id,
        "cml_path": str(source),
        "cml_sha256": sha256_file(source),
        "ir_sha256": sha256_canonical_json(result.ir),
        "ir_encoding": "canonical_json_sorted_keys_compact_utf8",
        "compiler_id": "cml-reference-compiler",
        "compiler_version": version,
        "compiler_entry_sha256": compiler_entry_hash,
        "compile_ok": True,
        "invariant_table": invariant_table,
        "span_policy": {"accepted_coverage": accepted_coverage},
        "sealed_at": utc_now(),
        "time_authority": "local_clock_untrusted",
    }
    return validate_record(record)

