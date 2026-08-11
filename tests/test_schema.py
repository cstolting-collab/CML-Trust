from __future__ import annotations

import unittest

from helpers import plan_record

from cml_trust.schema import SchemaError, validate_record


class SchemaTests(unittest.TestCase):
    def test_plan_must_compile(self) -> None:
        record = plan_record()
        record["compile_ok"] = False
        with self.assertRaisesRegex(SchemaError, "COMPILE_FAILED"):
            validate_record(record)

    def test_result_enum_rejects_unknown_value(self) -> None:
        record = {
            "kind": "checkpoint",
            "schema_version": "trust.v1",
            "id": "C1",
            "parent_id": None,
            "plan_id": "plan_001",
            "frame_ref": "/tmp/frame.png",
            "frame_sha256": "a" * 64,
            "frame_index": 1,
            "results": {"inv_node": "probably"},
            "reviewer": "alex",
            "reviewed_at": "now",
        }
        with self.assertRaisesRegex(SchemaError, "ENUM_INVALID"):
            validate_record(record)

    def test_boundary_window_is_span_review_type(self) -> None:
        record = {
            "kind": "span_review",
            "schema_version": "trust.v1",
            "id": "BW1",
            "plan_id": "plan_001",
            "from_id": "C1",
            "to_id": "C2",
            "review_type": "boundary_window",
            "coverage": "dense",
            "frames_inspected": [1, 2],
            "results": {"inv_span": "observed_pass"},
            "reviewer": "alex",
            "reviewed_at": "now",
        }
        self.assertEqual(validate_record(record)["kind"], "span_review")

    def test_reserved_unimplemented_kind_fails_closed(self) -> None:
        record = {
            "kind": "event_evidence",
            "schema_version": "trust.v1",
            "id": "EE1",
        }
        with self.assertRaisesRegex(SchemaError, "POLICY_BLOCK"):
            validate_record(record)

    def test_plan_rejects_missing_or_phase_governance(self) -> None:
        for governs in (None, "post_event:E10"):
            with self.subTest(governs=governs):
                record = plan_record()
                if governs is None:
                    del record["invariant_table"]["inv_node"]["governs"]
                else:
                    record["invariant_table"]["inv_node"]["governs"] = governs
                with self.assertRaisesRegex(SchemaError, "POLICY_BLOCK"):
                    validate_record(record)


if __name__ == "__main__":
    unittest.main()
