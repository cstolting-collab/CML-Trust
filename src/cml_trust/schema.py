from __future__ import annotations

from typing import Any


SCHEMA_VERSION = "trust.v1"
RECORD_KINDS = frozenset(
    {
        "sealed_plan",
        "extract_manifest",
        "checkpoint",
        "span_review",
        "event_evidence",
        "revocation",
        "repair_plan",
        "residual_ledger_entry",
    }
)
IMPLEMENTED_RECORD_KINDS = frozenset(
    {"sealed_plan", "extract_manifest", "checkpoint", "span_review", "revocation"}
)
RESULT_VALUES = frozenset(
    {
        "observed_pass",
        "observed_fail",
        "unobserved",
        "uncertain",
        "not_applicable",
        "not_checked",
    }
)
STRENGTH_VALUES = frozenset({"hard", "advisory"})
SCOPE_VALUES = frozenset({"node", "span", "both"})
COVERAGE_VALUES = frozenset(
    {"every_frame", "dense", "spotcheck", "endpoints", "custom", "unobserved"}
)
REVOCATION_SCOPES = frozenset({"targets_only", "targets_and_descendants"})


class SchemaError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _require_string(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SchemaError("FIELD_INVALID", f"{key} must be a non-empty string")
    return value


def _require_sha256(record: dict[str, Any], key: str) -> str:
    value = _require_string(record, key)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise SchemaError("FIELD_INVALID", f"{key} must be a lowercase SHA-256 hex digest")
    return value


def _validate_results(value: Any) -> None:
    if not isinstance(value, dict) or not value:
        raise SchemaError("FIELD_INVALID", "results must be a non-empty object")
    for invariant_id, result in value.items():
        if not isinstance(invariant_id, str) or not invariant_id:
            raise SchemaError("FIELD_INVALID", "result keys must be invariant ids")
        if result not in RESULT_VALUES:
            raise SchemaError("ENUM_INVALID", f"invalid result for {invariant_id}: {result}")


def _validate_invariant_table(value: Any) -> None:
    if not isinstance(value, dict) or not value:
        raise SchemaError("FIELD_INVALID", "invariant_table must be a non-empty object")
    for invariant_id, metadata in value.items():
        if not isinstance(invariant_id, str) or not invariant_id:
            raise SchemaError("FIELD_INVALID", "invariant id must be a non-empty string")
        if not isinstance(metadata, dict):
            raise SchemaError("FIELD_INVALID", f"metadata for {invariant_id} must be an object")
        if not isinstance(metadata.get("statement"), str) or not metadata["statement"].strip():
            raise SchemaError("FIELD_INVALID", f"{invariant_id}.statement is required")
        if metadata.get("strength") not in STRENGTH_VALUES:
            raise SchemaError("ENUM_INVALID", f"invalid strength for {invariant_id}")
        if metadata.get("scope") not in SCOPE_VALUES:
            raise SchemaError("ENUM_INVALID", f"invalid scope for {invariant_id}")
        if not isinstance(metadata.get("required_for_completeness"), bool):
            raise SchemaError(
                "FIELD_INVALID",
                f"{invariant_id}.required_for_completeness must be boolean",
            )
        if metadata.get("governs") != "always":
            raise SchemaError(
                "POLICY_BLOCK",
                "alpha accepts only governs='always'; event phases are not implemented",
            )


def _validate_rational(value: Any, field: str) -> None:
    if not isinstance(value, dict):
        raise SchemaError("FIELD_INVALID", f"{field} must be a rational object")
    numerator = value.get("num")
    denominator = value.get("den")
    if (
        not isinstance(numerator, int)
        or isinstance(numerator, bool)
        or not isinstance(denominator, int)
        or isinstance(denominator, bool)
        or denominator <= 0
    ):
        raise SchemaError(
            "FIELD_INVALID", f"{field} must contain integer num and positive den"
        )


def validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise SchemaError("FIELD_INVALID", "record must be an object")
    kind = _require_string(record, "kind")
    if kind not in RECORD_KINDS:
        raise SchemaError("ENUM_INVALID", f"unknown record kind: {kind}")
    if kind not in IMPLEMENTED_RECORD_KINDS:
        raise SchemaError(
            "POLICY_BLOCK",
            f"record kind is reserved but not implemented in this vertical slice: {kind}",
        )
    _require_string(record, "id")
    if record.get("schema_version") != SCHEMA_VERSION:
        raise SchemaError("SCHEMA_VERSION", f"schema_version must be {SCHEMA_VERSION}")

    if kind == "sealed_plan":
        if record.get("compile_ok") is not True:
            raise SchemaError("COMPILE_FAILED", "only compile-ok plans may be sealed")
        for key in ("cml_sha256", "ir_sha256"):
            _require_sha256(record, key)
        for key in ("compiler_id", "compiler_version", "sealed_at"):
            _require_string(record, key)
        _validate_invariant_table(record.get("invariant_table"))
        policy = record.get("span_policy")
        if not isinstance(policy, dict):
            raise SchemaError("FIELD_INVALID", "span_policy must be an object")
        accepted = policy.get("accepted_coverage")
        if not isinstance(accepted, list) or not accepted:
            raise SchemaError("FIELD_INVALID", "accepted_coverage must be a non-empty list")
        if any(item not in COVERAGE_VALUES for item in accepted):
            raise SchemaError("ENUM_INVALID", "span_policy contains invalid coverage")

    elif kind == "extract_manifest":
        for key in ("plan_id", "source_video_ref", "registered_at"):
            _require_string(record, key)
        _require_sha256(record, "source_video_sha256")
        video_stream = record.get("video_stream")
        if not isinstance(video_stream, dict):
            raise SchemaError("FIELD_INVALID", "video_stream must be an object")
        stream_index = video_stream.get("index")
        if not isinstance(stream_index, int) or isinstance(stream_index, bool) or stream_index < 0:
            raise SchemaError("FIELD_INVALID", "video_stream.index must be non-negative")
        _validate_rational(video_stream.get("time_base"), "video_stream.time_base")
        _validate_rational(
            video_stream.get("avg_frame_rate"), "video_stream.avg_frame_rate"
        )
        extraction = record.get("extraction")
        if not isinstance(extraction, dict):
            raise SchemaError("FIELD_INVALID", "extraction must be an object")
        for key in ("tool", "tool_version", "argv_status"):
            _require_string(extraction, key)
        argv = extraction.get("argv")
        if argv is not None and (
            not isinstance(argv, list)
            or not all(isinstance(item, str) and item for item in argv)
        ):
            raise SchemaError("FIELD_INVALID", "extraction.argv must be null or strings")
        frames = record.get("frames")
        if not isinstance(frames, list) or not frames:
            raise SchemaError("FIELD_INVALID", "frames must be a non-empty list")
        seen_indices: set[int] = set()
        for frame in frames:
            if not isinstance(frame, dict):
                raise SchemaError("FIELD_INVALID", "each frame must be an object")
            frame_index = frame.get("frame_index")
            if (
                not isinstance(frame_index, int)
                or isinstance(frame_index, bool)
                or frame_index < 0
                or frame_index in seen_indices
            ):
                raise SchemaError(
                    "FIELD_INVALID", "frame_index values must be unique and non-negative"
                )
            seen_indices.add(frame_index)
            _require_string(frame, "frame_ref")
            _require_sha256(frame, "frame_sha256")
            pts = frame.get("pts")
            if pts is not None and (not isinstance(pts, int) or isinstance(pts, bool)):
                raise SchemaError("FIELD_INVALID", "frame pts must be an integer or null")

    elif kind == "checkpoint":
        for key in ("plan_id", "frame_ref", "reviewer", "reviewed_at"):
            _require_string(record, key)
        _require_sha256(record, "frame_sha256")
        parent_id = record.get("parent_id")
        if parent_id is not None and (not isinstance(parent_id, str) or not parent_id):
            raise SchemaError("FIELD_INVALID", "parent_id must be null or a non-empty string")
        frame_index = record.get("frame_index")
        if frame_index is not None and (
            not isinstance(frame_index, int) or isinstance(frame_index, bool) or frame_index < 0
        ):
            raise SchemaError("FIELD_INVALID", "frame_index must be a non-negative integer")
        _validate_results(record.get("results"))

    elif kind == "span_review":
        for key in ("plan_id", "from_id", "to_id", "coverage", "reviewer", "reviewed_at"):
            _require_string(record, key)
        if record["coverage"] not in COVERAGE_VALUES:
            raise SchemaError("ENUM_INVALID", f"invalid coverage: {record['coverage']}")
        review_type = record.get("review_type", "interval")
        if review_type not in {"interval", "boundary_window"}:
            raise SchemaError("ENUM_INVALID", f"invalid review_type: {review_type}")
        frames = record.get("frames_inspected")
        if not isinstance(frames, list) or not all(
            isinstance(item, int) and not isinstance(item, bool) and item >= 0
            for item in frames
        ):
            raise SchemaError("FIELD_INVALID", "frames_inspected must be non-negative integers")
        _validate_results(record.get("results"))

    elif kind == "revocation":
        targets = record.get("target_ids")
        if not isinstance(targets, list) or not targets or not all(
            isinstance(item, str) and item for item in targets
        ):
            raise SchemaError("FIELD_INVALID", "target_ids must contain ids")
        if record.get("scope") not in REVOCATION_SCOPES:
            raise SchemaError("ENUM_INVALID", "invalid revocation scope")
        _require_string(record, "reason")
        _require_string(record, "at")

    return record
