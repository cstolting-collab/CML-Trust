from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from .schema import SchemaError, validate_record


class JsonlStore:
    def __init__(self, path: str | Path = ".cml-trust/records.jsonl") -> None:
        self.path = Path(path)

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as error:
                    raise SchemaError(
                        "LOG_CORRUPT", f"invalid JSON on line {line_number}"
                    ) from error
                records.append(validate_record(value))
        self._check_duplicate_ids(records)
        return records

    def append(self, record: dict[str, Any]) -> None:
        validated = validate_record(record)
        existing = self.read_all()
        ids = {item["id"] for item in existing}
        if validated["id"] in ids:
            raise SchemaError("DUP_ID", f"record id already exists: {validated['id']}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(
            validated,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(encoded)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _check_duplicate_ids(records: Iterable[dict[str, Any]]) -> None:
        seen: set[str] = set()
        for record in records:
            record_id = record["id"]
            if record_id in seen:
                raise SchemaError("DUP_ID", f"duplicate record id in log: {record_id}")
            seen.add(record_id)

