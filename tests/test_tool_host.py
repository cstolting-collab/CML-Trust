from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from cml_trust.tool_host import CMLTrustToolHost, tool_definitions


INVARIANTS = {
    "inv_node": {
        "statement": "The cup remains the same cup.",
        "strength": "hard",
        "scope": "node",
        "required_for_completeness": True,
        "governs": "always",
    }
}


class FakeCompiler:
    def compile_file(self, path: Path) -> SimpleNamespace:
        return SimpleNamespace(
            valid=True,
            ir={"format": "CML-IR", "projects": []},
            diagnostics=(),
        )

    def version(self) -> str:
        return "test compiler; CML 1.0.0"


class FailingCompiler(FakeCompiler):
    def compile_file(self, path: Path) -> SimpleNamespace:
        diagnostic = SimpleNamespace(code="CML-TEST", message="bad source")
        return SimpleNamespace(valid=False, ir=None, diagnostics=(diagnostic,))


class ExplodingCompiler(FakeCompiler):
    def compile_file(self, path: Path) -> SimpleNamespace:
        raise RuntimeError("sensitive internal detail")


class ToolHostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "scene.cml"
        self.source.write_text("PROJECT demo {}", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def host(self, compiler: type[FakeCompiler] = FakeCompiler) -> CMLTrustToolHost:
        return CMLTrustToolHost(self.root, compiler_factory=compiler)

    def seal_arguments(self) -> dict[str, object]:
        return {
            "source_path": "scene.cml",
            "plan_id": "plan_001",
            "invariants": INVARIANTS,
            "accepted_coverage": ["every_frame"],
        }

    def test_tool_definitions_expose_only_two_operations(self) -> None:
        names = [item["function"]["name"] for item in tool_definitions()]
        self.assertEqual(names, ["cml_plan_seal", "cml_status_derive"])

    def test_relative_source_and_store_resolve_inside_allowed_root(self) -> None:
        host = self.host()
        result = host.execute("cml_plan_seal", self.seal_arguments())
        self.assertTrue(result["ok"])
        self.assertTrue(host.store_path.is_relative_to(self.root))
        self.assertTrue(host.store_path.is_file())

    def test_sibling_prefix_does_not_bypass_path_boundary(self) -> None:
        sibling = self.root.parent / f"{self.root.name}-evil.cml"
        sibling.write_text("PROJECT evil {}", encoding="utf-8")
        self.addCleanup(sibling.unlink, missing_ok=True)
        arguments = self.seal_arguments()
        arguments["source_path"] = str(sibling)
        result = self.host().execute("cml_plan_seal", arguments)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "ARGUMENT_INVALID")
        self.assertEqual(result["error"]["message"], "path outside allowed root")

    def test_model_cannot_select_a_store_path(self) -> None:
        result = self.host().execute(
            "cml_status_derive", {"store_path": "/tmp/another-ledger.jsonl"}
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "ARGUMENT_INVALID")

    def test_unknown_operation_fails_closed(self) -> None:
        result = self.host().execute("run_shell", {"command": "whoami"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "TOOL_UNKNOWN")

    def test_compile_failure_keeps_machine_readable_code(self) -> None:
        result = self.host(FailingCompiler).execute(
            "cml_plan_seal", self.seal_arguments()
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "COMPILE_FAILED")
        self.assertIn("CML-TEST", result["error"]["message"])

    def test_schema_error_code_is_preserved(self) -> None:
        host = self.host()
        first = host.execute("cml_plan_seal", self.seal_arguments())
        second = host.execute("cml_plan_seal", self.seal_arguments())
        self.assertTrue(first["ok"])
        self.assertFalse(second["ok"])
        self.assertEqual(second["error"]["code"], "DUP_ID")

    def test_unexpected_error_does_not_expose_internal_detail(self) -> None:
        result = self.host(ExplodingCompiler).execute(
            "cml_plan_seal", self.seal_arguments()
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INTERNAL_ERROR")
        self.assertNotIn("sensitive", result["error"]["message"])

    def test_status_is_derived_without_mutating_the_ledger(self) -> None:
        host = self.host()
        host.execute("cml_plan_seal", self.seal_arguments())
        before = host.store_path.read_bytes()
        result = host.execute("cml_status_derive", {})
        after = host.store_path.read_bytes()
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"]["status"], "no_checkpoints")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
