from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from helpers import plan_record

from cml_trust.seal import seal_plan


class FakeCompiler:
    def __init__(self, valid: bool = True) -> None:
        self.valid = valid

    def compile_file(self, path: Path) -> SimpleNamespace:
        if self.valid:
            return SimpleNamespace(
                valid=True,
                ir={"format": "CML-IR", "projects": []},
                diagnostics=(),
            )
        diagnostic = SimpleNamespace(code="CML-TEST", message="bad source")
        return SimpleNamespace(valid=False, ir=None, diagnostics=(diagnostic,))

    def version(self) -> str:
        return "test compiler; CML 1.0.0"


class SealTests(unittest.TestCase):
    def test_seal_hashes_source_and_ir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scene.cml"
            source.write_text("PROJECT demo {}", encoding="utf-8")
            record = seal_plan(
                source,
                "plan_001",
                plan_record()["invariant_table"],
                ["every_frame"],
                compiler_factory=FakeCompiler,
            )
            self.assertTrue(record["compile_ok"])
            self.assertEqual(len(record["cml_sha256"]), 64)
            self.assertEqual(len(record["ir_sha256"]), 64)

    def test_failed_compile_cannot_be_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scene.cml"
            source.write_text("bad", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "COMPILE_FAILED"):
                seal_plan(
                    source,
                    "plan_001",
                    plan_record()["invariant_table"],
                    ["every_frame"],
                    compiler_factory=lambda: FakeCompiler(valid=False),
                )


if __name__ == "__main__":
    unittest.main()

