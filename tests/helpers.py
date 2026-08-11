from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def plan_record(plan_id: str = "plan_001") -> dict[str, Any]:
    return {
        "kind": "sealed_plan",
        "schema_version": "trust.v1",
        "id": plan_id,
        "cml_sha256": "a" * 64,
        "ir_sha256": "b" * 64,
        "compiler_id": "test-compiler",
        "compiler_version": "test CML 1.0.0",
        "compile_ok": True,
        "sealed_at": "2026-08-11T00:00:00+00:00",
        "invariant_table": {
            "inv_node": {
                "statement": "Cup remains the same at checkpoints",
                "strength": "hard",
                "scope": "node",
                "required_for_completeness": True,
                "governs": "always",
            },
            "inv_span": {
                "statement": "Cup remains continuous through the span",
                "strength": "hard",
                "scope": "span",
                "required_for_completeness": True,
                "governs": "always",
            },
        },
        "span_policy": {"accepted_coverage": ["every_frame"]},
    }
