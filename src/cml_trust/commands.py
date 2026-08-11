from __future__ import annotations

from pathlib import Path
from typing import Any

from .derive import invalid_checkpoint_ids
from .hashutil import sha256_file
from .schema import SCHEMA_VERSION, SchemaError, validate_record
from .seal import utc_now
from .store import JsonlStore


def _records_by_kind(records: list[dict[str, Any]], kind: str) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in records if item["kind"] == kind}


def _validate_result_ids(
    results: dict[str, str], plan: dict[str, Any], scope: str
) -> None:
    valid_scopes = {scope, "both"}
    expected = {
        invariant_id
        for invariant_id, metadata in plan["invariant_table"].items()
        if metadata["scope"] in valid_scopes
    }
    unknown = set(results) - set(plan["invariant_table"])
    if unknown:
        raise SchemaError("INVARIANT_UNKNOWN", f"unknown invariant ids: {sorted(unknown)}")
    missing = expected - set(results)
    if missing:
        raise SchemaError("EVIDENCE_INCOMPLETE", f"missing result ids: {sorted(missing)}")
    for invariant_id, result in results.items():
        if result == "not_applicable" and plan["invariant_table"][invariant_id]["governs"] == "always":
            raise SchemaError("N_A_UNAUTHORIZED", f"{invariant_id} governs at this record")


def register_extract_manifest(
    store: JsonlStore,
    descriptor: dict[str, Any],
    base_directory: str | Path,
) -> dict[str, Any]:
    records = store.read_all()
    plans = _records_by_kind(records, "sealed_plan")
    plan_id = descriptor.get("plan_id")
    if plan_id not in plans:
        raise SchemaError("PLAN_MISSING", f"unknown plan: {plan_id}")

    base = Path(base_directory).expanduser().resolve()
    source = Path(descriptor.get("source_video_path", ""))
    if not source.is_absolute():
        source = base / source
    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    sequence = descriptor.get("frame_sequence")
    if not isinstance(sequence, dict):
        raise SchemaError("FIELD_INVALID", "frame_sequence must be an object")
    directory = Path(sequence.get("directory", ""))
    if not directory.is_absolute():
        directory = base / directory
    directory = directory.resolve()
    pattern = sequence.get("pattern")
    if not isinstance(pattern, str) or not pattern:
        raise SchemaError("FIELD_INVALID", "frame_sequence.pattern is required")
    values = {
        key: sequence.get(key)
        for key in ("first_file_number", "first_frame_index", "count")
    }
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in values.values()
    ) or values["count"] == 0:
        raise SchemaError(
            "FIELD_INVALID",
            "frame sequence numbers must be non-negative integers and count must be positive",
        )
    first_pts = sequence.get("first_pts")
    pts_step = sequence.get("pts_step")
    if (first_pts is None) != (pts_step is None) or (
        first_pts is not None
        and (
            not isinstance(first_pts, int)
            or isinstance(first_pts, bool)
            or not isinstance(pts_step, int)
            or isinstance(pts_step, bool)
            or pts_step <= 0
        )
    ):
        raise SchemaError(
            "FIELD_INVALID", "first_pts and positive integer pts_step must appear together"
        )

    frames: list[dict[str, Any]] = []
    for offset in range(values["count"]):
        file_number = values["first_file_number"] + offset
        try:
            filename = pattern % file_number
        except (TypeError, ValueError) as error:
            raise SchemaError(
                "FIELD_INVALID", "frame_sequence.pattern must accept one integer"
            ) from error
        frame = (directory / filename).resolve()
        if not frame.is_file():
            raise FileNotFoundError(frame)
        entry: dict[str, Any] = {
            "frame_index": values["first_frame_index"] + offset,
            "frame_ref": str(frame),
            "frame_sha256": sha256_file(frame),
            "pts": None if first_pts is None else first_pts + offset * pts_step,
        }
        frames.append(entry)

    record = {
        "kind": "extract_manifest",
        "schema_version": SCHEMA_VERSION,
        "id": descriptor.get("id"),
        "plan_id": plan_id,
        "source_video_ref": str(source),
        "source_video_sha256": sha256_file(source),
        "video_stream": descriptor.get("video_stream"),
        "audio_stream": descriptor.get("audio_stream"),
        "extraction": descriptor.get("extraction"),
        "frames": frames,
        "registered_at": utc_now(),
        "time_authority": "container_pts_and_local_registration_clock",
    }
    store.append(validate_record(record))
    return record


def add_checkpoint(
    store: JsonlStore,
    checkpoint_id: str,
    plan_id: str,
    frame_path: str | Path,
    results: dict[str, str],
    reviewer: str,
    parent_id: str | None = None,
    frame_index: int | None = None,
) -> dict[str, Any]:
    records = store.read_all()
    plans = _records_by_kind(records, "sealed_plan")
    checkpoints = _records_by_kind(records, "checkpoint")
    plan = plans.get(plan_id)
    if plan is None:
        raise SchemaError("PLAN_MISSING", f"unknown plan: {plan_id}")
    if parent_id is not None:
        parent = checkpoints.get(parent_id)
        if parent is None or parent_id in invalid_checkpoint_ids(records):
            raise SchemaError("PARENT_INVALID", f"invalid parent: {parent_id}")
        if parent["plan_id"] != plan_id:
            raise SchemaError("PARENT_INVALID", "parent and child must use the same sealed plan")
    _validate_result_ids(results, plan, "node")
    frame = Path(frame_path).expanduser().resolve()
    if not frame.is_file():
        raise FileNotFoundError(frame)
    record = {
        "kind": "checkpoint",
        "schema_version": SCHEMA_VERSION,
        "id": checkpoint_id,
        "parent_id": parent_id,
        "plan_id": plan_id,
        "frame_ref": str(frame),
        "frame_sha256": sha256_file(frame),
        "frame_index": frame_index,
        "results": results,
        "reviewer": reviewer,
        "reviewed_at": utc_now(),
    }
    store.append(validate_record(record))
    return record


def add_span(
    store: JsonlStore,
    span_id: str,
    plan_id: str,
    from_id: str,
    to_id: str,
    coverage: str,
    frames_inspected: list[int],
    results: dict[str, str],
    reviewer: str,
    review_type: str = "interval",
    notes: str = "",
) -> dict[str, Any]:
    records = store.read_all()
    plans = _records_by_kind(records, "sealed_plan")
    checkpoints = _records_by_kind(records, "checkpoint")
    plan = plans.get(plan_id)
    if plan is None:
        raise SchemaError("PLAN_MISSING", f"unknown plan: {plan_id}")
    left = checkpoints.get(from_id)
    right = checkpoints.get(to_id)
    if left is None or right is None:
        raise SchemaError("PARENT_INVALID", "span endpoints must exist")
    if right.get("parent_id") != from_id and review_type == "interval":
        raise SchemaError("EDGE_INVALID", "interval span endpoints must be adjacent")
    if left["plan_id"] != plan_id or right["plan_id"] != plan_id:
        raise SchemaError("PLAN_MISMATCH", "span and endpoints must use one plan")
    if from_id in invalid_checkpoint_ids(records) or to_id in invalid_checkpoint_ids(records):
        raise SchemaError("PARENT_INVALID", "span endpoint has invalid lineage")
    if review_type == "interval":
        duplicate = any(
            item["kind"] == "span_review"
            and item.get("review_type", "interval") == "interval"
            and item["from_id"] == from_id
            and item["to_id"] == to_id
            for item in records
        )
        if duplicate:
            raise SchemaError("DUP_EDGE", "an interval review already exists for this edge")
    _validate_result_ids(results, plan, "span")
    record = {
        "kind": "span_review",
        "schema_version": SCHEMA_VERSION,
        "id": span_id,
        "plan_id": plan_id,
        "from_id": from_id,
        "to_id": to_id,
        "review_type": review_type,
        "coverage": coverage,
        "frames_inspected": frames_inspected,
        "results": results,
        "notes": notes,
        "reviewer": reviewer,
        "reviewed_at": utc_now(),
    }
    store.append(validate_record(record))
    return record


def add_revocation(
    store: JsonlStore,
    revocation_id: str,
    target_ids: list[str],
    reason: str,
    scope: str = "targets_and_descendants",
) -> dict[str, Any]:
    records = store.read_all()
    checkpoint_ids = {
        item["id"] for item in records if item["kind"] == "checkpoint"
    }
    missing = set(target_ids) - checkpoint_ids
    if missing:
        raise SchemaError("TARGET_MISSING", f"unknown checkpoint ids: {sorted(missing)}")
    record = {
        "kind": "revocation",
        "schema_version": SCHEMA_VERSION,
        "id": revocation_id,
        "target_ids": target_ids,
        "scope": scope,
        "reason": reason,
        "at": utc_now(),
    }
    store.append(validate_record(record))
    return record
