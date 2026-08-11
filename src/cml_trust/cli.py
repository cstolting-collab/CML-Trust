from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .commands import add_checkpoint, add_revocation, add_span, register_extract_manifest
from .derive import derive_project_status, lineage_for_tip
from .schema import SchemaError
from .seal import seal_plan
from .store import JsonlStore


def _json_file(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmltrust",
        description="Local external evidence notebook for CML continuity claims.",
    )
    parser.add_argument(
        "--store", default=".cml-trust/records.jsonl", help="append-only JSONL path"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan")
    plan_commands = plan.add_subparsers(dest="plan_command", required=True)
    seal = plan_commands.add_parser("seal")
    seal.add_argument("source")
    seal.add_argument("--id", required=True)
    seal.add_argument("--invariants", required=True)
    seal.add_argument(
        "--accepted-coverage",
        default="every_frame",
        help="comma-separated span coverage methods",
    )
    plan_commands.add_parser("show")

    extract = commands.add_parser("extract")
    extract_commands = extract.add_subparsers(dest="extract_command", required=True)
    extract_register = extract_commands.add_parser("register")
    extract_register.add_argument("manifest")

    checkpoint = commands.add_parser("checkpoint")
    checkpoint_commands = checkpoint.add_subparsers(
        dest="checkpoint_command", required=True
    )
    checkpoint_add = checkpoint_commands.add_parser("add")
    checkpoint_add.add_argument("--id", required=True)
    checkpoint_add.add_argument("--plan", required=True)
    checkpoint_add.add_argument("--frame", required=True)
    checkpoint_add.add_argument("--parent")
    checkpoint_add.add_argument("--frame-index", type=int)
    checkpoint_add.add_argument("--results", required=True)
    checkpoint_add.add_argument("--reviewer", required=True)

    span = commands.add_parser("span")
    span_commands = span.add_subparsers(dest="span_command", required=True)
    span_add = span_commands.add_parser("add")
    span_add.add_argument("--id", required=True)
    span_add.add_argument("--plan", required=True)
    span_add.add_argument("--from", dest="from_id", required=True)
    span_add.add_argument("--to", dest="to_id", required=True)
    span_add.add_argument("--coverage", required=True)
    span_add.add_argument("--frames", default="")
    span_add.add_argument("--results", required=True)
    span_add.add_argument("--reviewer", required=True)
    span_add.add_argument(
        "--review-type", choices=("interval", "boundary_window"), default="interval"
    )
    span_add.add_argument("--notes", default="")

    revoke = commands.add_parser("revoke")
    revoke.add_argument("--id", required=True, help="revocation record id")
    revoke.add_argument("--target", action="append", required=True)
    revoke.add_argument("--reason", required=True)
    revoke.add_argument(
        "--scope",
        choices=("targets_only", "targets_and_descendants"),
        default="targets_and_descendants",
    )

    lineage = commands.add_parser("lineage")
    lineage.add_argument("--tip")
    commands.add_parser("status")
    return parser


def _run(args: argparse.Namespace) -> Any:
    store = JsonlStore(args.store)
    if args.command == "plan" and args.plan_command == "seal":
        invariants = _json_file(args.invariants)
        accepted = [item.strip() for item in args.accepted_coverage.split(",") if item.strip()]
        record = seal_plan(args.source, args.id, invariants, accepted)
        store.append(record)
        return record

    if args.command == "plan" and args.plan_command == "show":
        return [item for item in store.read_all() if item["kind"] == "sealed_plan"]

    if args.command == "extract" and args.extract_command == "register":
        manifest_path = Path(args.manifest).expanduser().resolve()
        return register_extract_manifest(
            store,
            _json_file(str(manifest_path)),
            manifest_path.parent,
        )

    if args.command == "checkpoint" and args.checkpoint_command == "add":
        return add_checkpoint(
            store=store,
            checkpoint_id=args.id,
            plan_id=args.plan,
            frame_path=args.frame,
            results=_json_file(args.results),
            reviewer=args.reviewer,
            parent_id=args.parent,
            frame_index=args.frame_index,
        )

    if args.command == "span" and args.span_command == "add":
        frames = [int(value) for value in args.frames.split(",") if value.strip()]
        return add_span(
            store=store,
            span_id=args.id,
            plan_id=args.plan,
            from_id=args.from_id,
            to_id=args.to_id,
            coverage=args.coverage,
            frames_inspected=frames,
            results=_json_file(args.results),
            reviewer=args.reviewer,
            review_type=args.review_type,
            notes=args.notes,
        )

    if args.command == "revoke":
        return add_revocation(
            store=store,
            revocation_id=args.id,
            target_ids=args.target,
            reason=args.reason,
            scope=args.scope,
        )

    if args.command == "status":
        return derive_project_status(store.read_all())

    if args.command == "lineage":
        records = store.read_all()
        checkpoints = {
            item["id"]: item for item in records if item["kind"] == "checkpoint"
        }
        status = derive_project_status(records)
        tip_id = args.tip
        if tip_id is None:
            reports = status.get("tips", [])
            if len(reports) != 1:
                raise SchemaError(
                    "TIP_REQUIRED", "specify --tip when there is not exactly one active tip"
                )
            tip_id = reports[0]["tip_id"]
        return [item["id"] for item in lineage_for_tip(tip_id, checkpoints)]

    raise RuntimeError("unhandled command")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        _print(_run(args))
        return 0
    except (SchemaError, ValueError, FileNotFoundError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
