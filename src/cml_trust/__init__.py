"""External evidence records for CML continuity claims."""

from .derive import derive_project_status
from .schema import RESULT_VALUES, SchemaError, validate_record
from .store import JsonlStore

__all__ = [
    "JsonlStore",
    "RESULT_VALUES",
    "SchemaError",
    "derive_project_status",
    "validate_record",
]

__version__ = "0.1.0a1"
