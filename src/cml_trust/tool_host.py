from __future__ import annotations

from pathlib import Path
from threading import Lock, RLock
from typing import Any, Callable, Mapping

from .derive import derive_project_status
from .schema import COVERAGE_VALUES, SchemaError
from .seal import seal_plan
from .store import JsonlStore


_STORE_LOCKS: dict[Path, RLock] = {}
_STORE_LOCKS_GUARD = Lock()


def _lock_for_store(path: Path) -> RLock:
    """Return one in-process lock for every resolved JSONL store path."""

    with _STORE_LOCKS_GUARD:
        return _STORE_LOCKS.setdefault(path, RLock())


def tool_definitions() -> list[dict[str, Any]]:
    """Return function-tool definitions for the implemented host operations.

    The shape is compatible with APIs that accept ``type=function`` tools.
    Execution remains the responsibility of the application hosting this class.
    """

    invariant_metadata = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statement": {"type": "string", "minLength": 1},
            "strength": {"type": "string", "enum": ["hard", "advisory"]},
            "scope": {"type": "string", "enum": ["node", "span", "both"]},
            "required_for_completeness": {"type": "boolean"},
            "governs": {"type": "string", "enum": ["always"]},
        },
        "required": [
            "statement",
            "strength",
            "scope",
            "required_for_completeness",
            "governs",
        ],
    }
    return [
        {
            "type": "function",
            "function": {
                "name": "cml_plan_seal",
                "description": (
                    "Compile a CML plan, create a content-hashed sealed_plan record, "
                    "and append it to the host-controlled CML-Trust ledger."
                ),
                "parameters": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "minLength": 1,
                            "description": "CML source path inside the configured workspace.",
                        },
                        "plan_id": {"type": "string", "minLength": 1},
                        "invariants": {
                            "type": "object",
                            "minProperties": 1,
                            "additionalProperties": invariant_metadata,
                        },
                        "accepted_coverage": {
                            "type": "array",
                            "minItems": 1,
                            "uniqueItems": True,
                            "items": {
                                "type": "string",
                                "enum": sorted(COVERAGE_VALUES),
                            },
                        },
                    },
                    "required": ["source_path", "plan_id", "invariants"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "cml_status_derive",
                "description": (
                    "Derive checkpoint, span, lineage, and revocation status from "
                    "the host-controlled append-only ledger."
                ),
                "parameters": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {},
                },
            },
        },
    ]


class CMLTrustToolHost:
    """Narrow host boundary for model-requested CML-Trust operations.

    Paths are confined to ``allowed_root`` after symlink resolution. The model
    cannot choose the JSONL store, invoke a shell, or select arbitrary Python
    callables. Writes are serialized across host instances in this process.
    Deployments with multiple writer processes must add an external lock or
    route all writes through one service process.
    """

    _OPERATIONS = frozenset({"cml_plan_seal", "cml_status_derive"})

    def __init__(
        self,
        allowed_root: str | Path,
        *,
        store_path: str | Path = ".cml-trust/records.jsonl",
        compiler_factory: Callable[[], Any] | None = None,
    ) -> None:
        root = Path(allowed_root).expanduser().resolve()
        if not root.is_dir():
            raise ValueError("allowed_root must be an existing directory")
        self.allowed_root = root
        self.store_path = self._resolve_path(store_path)
        self.store = JsonlStore(self.store_path)
        self.compiler_factory = compiler_factory
        self._store_lock = _lock_for_store(self.store_path)

    def execute(self, operation: str, arguments: Mapping[str, Any] | None) -> dict[str, Any]:
        """Execute one allow-listed operation and always return JSON-ready data."""

        if operation not in self._OPERATIONS:
            return self._error(
                "TOOL_UNKNOWN",
                "Unsupported tool operation.",
                error_type="ToolDispatchError",
            )
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, Mapping):
            return self._error(
                "ARGUMENT_INVALID",
                "Tool arguments must be an object.",
                error_type="TypeError",
            )

        try:
            if operation == "cml_plan_seal":
                return self._seal(arguments)
            return self._status(arguments)
        except SchemaError as error:
            return self._error(error.code, error.message, error_type=type(error).__name__)
        except FileNotFoundError as error:
            return self._error("FILE_NOT_FOUND", str(error), error_type=type(error).__name__)
        except (TypeError, ValueError) as error:
            message = str(error)
            code = "COMPILE_FAILED" if message.startswith("COMPILE_FAILED:") else "ARGUMENT_INVALID"
            if code == "COMPILE_FAILED":
                message = message.partition(":")[2].strip() or "CML compilation failed."
            return self._error(code, message, error_type=type(error).__name__)
        except Exception as error:
            adapter_error = self._adapter_error(error)
            if adapter_error is not None:
                return adapter_error
            return self._error(
                "INTERNAL_ERROR",
                "The tool host encountered an unexpected internal error.",
                error_type="InternalError",
            )

    def _seal(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self._reject_unknown_arguments(
            arguments,
            {"source_path", "plan_id", "invariants", "accepted_coverage"},
        )
        source_value = self._required_string(arguments, "source_path")
        plan_id = self._required_string(arguments, "plan_id")
        invariants = arguments.get("invariants")
        if not isinstance(invariants, dict) or not invariants:
            raise ValueError("invariants must be a non-empty object")
        accepted = arguments.get("accepted_coverage", ["every_frame"])
        if (
            not isinstance(accepted, list)
            or not accepted
            or not all(isinstance(item, str) and item for item in accepted)
        ):
            raise ValueError("accepted_coverage must be a non-empty string array")

        source = self._resolve_path(source_value)
        if not source.is_file():
            raise FileNotFoundError(source)

        with self._store_lock:
            record = seal_plan(
                source,
                plan_id,
                invariants,
                accepted,
                compiler_factory=self.compiler_factory,
            )
            self.store.append(record)
        return {"ok": True, "operation": "cml_plan_seal", "record": record}

    def _status(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self._reject_unknown_arguments(arguments, set())
        with self._store_lock:
            records = self.store.read_all()
            status = derive_project_status(records)
        return {"ok": True, "operation": "cml_status_derive", "status": status}

    def _resolve_path(self, value: str | Path) -> Path:
        candidate = Path(value).expanduser()
        if not candidate.is_absolute():
            candidate = self.allowed_root / candidate
        resolved = candidate.resolve()
        if not resolved.is_relative_to(self.allowed_root):
            raise ValueError("path outside allowed root")
        return resolved

    @staticmethod
    def _required_string(arguments: Mapping[str, Any], key: str) -> str:
        value = arguments.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        return value

    @staticmethod
    def _reject_unknown_arguments(
        arguments: Mapping[str, Any], allowed: set[str]
    ) -> None:
        unknown = set(arguments) - allowed
        if unknown:
            raise ValueError(f"unsupported arguments: {sorted(unknown)}")

    @staticmethod
    def _error(
        code: str,
        message: str,
        *,
        error_type: str,
    ) -> dict[str, Any]:
        return {
            "ok": False,
            "error": {
                "code": code,
                "type": error_type,
                "message": message,
            },
        }

    @classmethod
    def _adapter_error(cls, error: Exception) -> dict[str, Any] | None:
        """Classify adapter failures without requiring it at module import time."""

        try:
            from cml_adapter import CMLAdapterError, CMLCompilerUnavailableError
        except ImportError:
            return None
        if isinstance(error, CMLCompilerUnavailableError):
            return cls._error(
                "COMPILER_UNAVAILABLE", str(error), error_type=type(error).__name__
            )
        if isinstance(error, CMLAdapterError):
            return cls._error(
                "COMPILER_ERROR", str(error), error_type=type(error).__name__
            )
        return None
