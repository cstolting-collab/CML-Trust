from __future__ import annotations

from pathlib import Path
from typing import Any

from .hashutil import sha256_file


UNRESOLVED_RESULTS = {"unobserved", "uncertain", "not_checked"}


def _indexes(records: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    plans = {item["id"]: item for item in records if item["kind"] == "sealed_plan"}
    checkpoints = {item["id"]: item for item in records if item["kind"] == "checkpoint"}
    return plans, checkpoints


def invalid_checkpoint_ids(records: list[dict[str, Any]]) -> set[str]:
    _, checkpoints = _indexes(records)
    invalid: set[str] = set()
    descendant_roots: set[str] = set()

    for record in records:
        if record["kind"] != "revocation":
            continue
        invalid.update(record["target_ids"])
        if record["scope"] == "targets_and_descendants":
            descendant_roots.update(record["target_ids"])

    changed = True
    while changed:
        changed = False
        for checkpoint_id, checkpoint in checkpoints.items():
            parent_id = checkpoint.get("parent_id")
            should_invalidate = (
                parent_id is not None
                and (parent_id not in checkpoints or parent_id in descendant_roots or parent_id in invalid)
            )
            if should_invalidate and checkpoint_id not in invalid:
                invalid.add(checkpoint_id)
                descendant_roots.add(checkpoint_id)
                changed = True
    return invalid


def _required_invariants(plan: dict[str, Any], scope: str) -> list[str]:
    valid_scopes = {scope, "both"}
    return [
        invariant_id
        for invariant_id, metadata in plan["invariant_table"].items()
        if metadata["scope"] in valid_scopes
        and metadata["strength"] == "hard"
        and metadata["required_for_completeness"]
        and metadata["governs"] == "always"
    ]


def derive_checkpoint_status(
    checkpoint: dict[str, Any],
    plan: dict[str, Any],
    invalid_ids: set[str],
) -> dict[str, Any]:
    checkpoint_id = checkpoint["id"]
    if checkpoint_id in invalid_ids:
        return {"status": "invalid_lineage", "blocking_invariants": []}

    frame_path = Path(checkpoint["frame_ref"])
    if not frame_path.is_file() or sha256_file(frame_path) != checkpoint["frame_sha256"]:
        return {"status": "evidence_mismatch", "blocking_invariants": []}

    required = _required_invariants(plan, "node")
    results = checkpoint["results"]
    failures: list[str] = []
    unresolved: list[str] = []
    unauthorized_na: list[str] = []
    for invariant_id in required:
        result = results.get(invariant_id, "not_checked")
        if result == "observed_fail":
            failures.append(invariant_id)
        elif result == "not_applicable":
            unauthorized_na.append(invariant_id)
        elif result != "observed_pass":
            unresolved.append(invariant_id)

    if unauthorized_na:
        return {
            "status": "invalid_observation",
            "reason": "N_A_UNAUTHORIZED",
            "blocking_invariants": unauthorized_na,
        }
    if failures:
        return {"status": "content_rejected", "blocking_invariants": failures}
    if unresolved:
        return {"status": "incomplete", "blocking_invariants": unresolved}
    return {"status": "complete", "blocking_invariants": []}


def derive_span_status(span: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    required = _required_invariants(plan, "span")
    results = span["results"]
    failures: list[str] = []
    unresolved: list[str] = []
    for invariant_id in required:
        result = results.get(invariant_id, "not_checked")
        if result == "observed_fail":
            failures.append(invariant_id)
        elif result != "observed_pass":
            unresolved.append(invariant_id)

    # A directly observed hard failure remains a failure even when the review
    # did not satisfy the plan's full coverage method. Coverage limits the
    # claims we can make about unseen material; it does not erase seen defects.
    if failures:
        return {"status": "observed_fail", "blocking_invariants": failures}
    if span["coverage"] not in plan["span_policy"]["accepted_coverage"]:
        return {
            "status": "coverage_limited",
            "blocking_invariants": unresolved,
            "reason": "coverage_method_not_accepted",
        }
    if unresolved:
        return {"status": "coverage_limited", "blocking_invariants": unresolved}
    return {"status": "observed_pass", "blocking_invariants": []}


def lineage_for_tip(
    tip_id: str, checkpoints: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    lineage: list[dict[str, Any]] = []
    seen: set[str] = set()
    current_id: str | None = tip_id
    while current_id is not None:
        if current_id in seen:
            raise ValueError(f"CYCLE: checkpoint cycle at {current_id}")
        seen.add(current_id)
        current = checkpoints.get(current_id)
        if current is None:
            raise ValueError(f"PARENT_INVALID: missing checkpoint {current_id}")
        lineage.append(current)
        current_id = current.get("parent_id")
    lineage.reverse()
    return lineage


def derive_project_status(records: list[dict[str, Any]]) -> dict[str, Any]:
    plans, checkpoints = _indexes(records)
    invalid_ids = invalid_checkpoint_ids(records)
    valid_checkpoints = {
        key: value for key, value in checkpoints.items() if key not in invalid_ids
    }
    if not valid_checkpoints:
        return {
            "status": "no_checkpoints",
            "tips": [],
            "invalid_checkpoint_ids": sorted(invalid_ids),
        }

    valid_parent_ids = {
        item.get("parent_id")
        for item in valid_checkpoints.values()
        if item.get("parent_id") in valid_checkpoints
    }
    tip_ids = sorted(set(valid_checkpoints) - valid_parent_ids)
    interval_spans = [
        item
        for item in records
        if item["kind"] == "span_review" and item.get("review_type", "interval") == "interval"
    ]
    span_by_edge: dict[tuple[str, str], dict[str, Any]] = {
        (item["from_id"], item["to_id"]): item for item in interval_spans
    }

    tip_reports: list[dict[str, Any]] = []
    for tip_id in tip_ids:
        lineage = lineage_for_tip(tip_id, valid_checkpoints)
        node_reports: list[dict[str, Any]] = []
        all_nodes_complete = True
        for checkpoint in lineage:
            plan = plans.get(checkpoint["plan_id"])
            if plan is None:
                node_status = {"status": "invalid_plan", "blocking_invariants": []}
            else:
                node_status = derive_checkpoint_status(checkpoint, plan, invalid_ids)
            all_nodes_complete = all_nodes_complete and node_status["status"] == "complete"
            node_reports.append({"checkpoint_id": checkpoint["id"], **node_status})

        if len(lineage) == 1:
            chain_status = "checkpoint_samples_only"
            span_reports: list[dict[str, Any]] = []
        else:
            span_reports = []
            all_spans_complete = True
            for left, right in zip(lineage, lineage[1:]):
                span = span_by_edge.get((left["id"], right["id"]))
                if span is None:
                    span_status = {"status": "missing", "blocking_invariants": []}
                else:
                    plan = plans.get(span["plan_id"])
                    span_status = (
                        derive_span_status(span, plan)
                        if plan is not None
                        else {"status": "invalid_plan", "blocking_invariants": []}
                    )
                all_spans_complete = all_spans_complete and span_status["status"] == "observed_pass"
                span_reports.append(
                    {"from_id": left["id"], "to_id": right["id"], **span_status}
                )
            has_observed_failure = any(
                item["status"] == "content_rejected" for item in node_reports
            ) or any(item["status"] == "observed_fail" for item in span_reports)
            if has_observed_failure:
                chain_status = "observational_chain_failed"
            elif all_nodes_complete and all_spans_complete:
                chain_status = "observational_chain_complete"
            else:
                chain_status = "coverage_incomplete"

        tip_reports.append(
            {
                "tip_id": tip_id,
                "status": chain_status,
                "nodes": node_reports,
                "spans": span_reports,
            }
        )

    overall = (
        tip_reports[0]["status"]
        if len(tip_reports) == 1
        else "multiple_active_tips"
    )
    return {
        "status": overall,
        "tips": tip_reports,
        "invalid_checkpoint_ids": sorted(invalid_ids),
    }
