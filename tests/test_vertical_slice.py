from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import plan_record

from cml_trust.commands import (
    add_checkpoint,
    add_revocation,
    add_span,
    register_extract_manifest,
)
from cml_trust.derive import derive_project_status, derive_span_status
from cml_trust.schema import SchemaError
from cml_trust.store import JsonlStore


class VerticalSliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = JsonlStore(self.root / "records.jsonl")
        self.store.append(plan_record())
        self.frame1 = self.root / "frame1.png"
        self.frame2 = self.root / "frame2.png"
        self.frame3 = self.root / "frame3.png"
        self.frame1.write_bytes(b"frame-one")
        self.frame2.write_bytes(b"frame-two")
        self.frame3.write_bytes(b"frame-three")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_c1(self) -> None:
        add_checkpoint(
            self.store,
            "C1",
            "plan_001",
            self.frame1,
            {"inv_node": "observed_pass"},
            "alex",
        )

    def test_standalone_checkpoint_is_samples_only(self) -> None:
        self.add_c1()
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["status"], "checkpoint_samples_only")

    def test_missing_span_blocks_complete_chain(self) -> None:
        self.add_c1()
        add_checkpoint(
            self.store,
            "C2",
            "plan_001",
            self.frame2,
            {"inv_node": "observed_pass"},
            "alex",
            parent_id="C1",
        )
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["status"], "coverage_incomplete")
        self.assertEqual(status["tips"][0]["spans"][0]["status"], "missing")

    def test_complete_nodes_and_span_form_complete_chain(self) -> None:
        self.add_c1()
        add_checkpoint(
            self.store,
            "C2",
            "plan_001",
            self.frame2,
            {"inv_node": "observed_pass"},
            "alex",
            parent_id="C1",
        )
        add_span(
            self.store,
            "S1",
            "plan_001",
            "C1",
            "C2",
            "every_frame",
            [1, 2],
            {"inv_span": "observed_pass"},
            "alex",
        )
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["status"], "observational_chain_complete")

    def test_observed_span_failure_has_distinct_chain_status(self) -> None:
        self.add_c1()
        add_checkpoint(
            self.store,
            "C2",
            "plan_001",
            self.frame2,
            {"inv_node": "observed_pass"},
            "alex",
            parent_id="C1",
        )
        add_span(
            self.store,
            "S1",
            "plan_001",
            "C1",
            "C2",
            "every_frame",
            [1, 2],
            {"inv_span": "observed_fail"},
            "alex",
        )
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["status"], "observational_chain_failed")
        self.assertEqual(status["tips"][0]["spans"][0]["status"], "observed_fail")

    def test_observed_failure_is_not_hidden_by_limited_coverage(self) -> None:
        plan = plan_record()
        span = {
            "coverage": "spotcheck",
            "results": {"inv_span": "observed_fail"},
        }
        status = derive_span_status(span, plan)
        self.assertEqual(status["status"], "observed_fail")
        self.assertEqual(status["blocking_invariants"], ["inv_span"])

    def test_unobserved_hard_node_is_incomplete_not_failed(self) -> None:
        add_checkpoint(
            self.store,
            "C1",
            "plan_001",
            self.frame1,
            {"inv_node": "unobserved"},
            "alex",
        )
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["tips"][0]["nodes"][0]["status"], "incomplete")

    def test_not_applicable_is_rejected_for_always_governing_invariant(self) -> None:
        with self.assertRaisesRegex(SchemaError, "N_A_UNAUTHORIZED"):
            add_checkpoint(
                self.store,
                "C1",
                "plan_001",
                self.frame1,
                {"inv_node": "not_applicable"},
                "alex",
            )

    def test_frame_replacement_causes_evidence_mismatch(self) -> None:
        self.add_c1()
        self.frame1.write_bytes(b"replaced")
        status = derive_project_status(self.store.read_all())
        self.assertEqual(
            status["tips"][0]["nodes"][0]["status"], "evidence_mismatch"
        )

    def test_revocation_invalidates_existing_descendants(self) -> None:
        self.add_c1()
        add_checkpoint(
            self.store,
            "C2",
            "plan_001",
            self.frame2,
            {"inv_node": "observed_pass"},
            "alex",
            parent_id="C1",
        )
        add_checkpoint(
            self.store,
            "C3",
            "plan_001",
            self.frame3,
            {"inv_node": "observed_pass"},
            "alex",
            parent_id="C2",
        )
        add_revocation(self.store, "R1", ["C2"], "bad cup state")
        status = derive_project_status(self.store.read_all())
        self.assertEqual(status["invalid_checkpoint_ids"], ["C2", "C3"])
        with self.assertRaisesRegex(SchemaError, "PARENT_INVALID"):
            add_checkpoint(
                self.store,
                "C4",
                "plan_001",
                self.frame3,
                {"inv_node": "observed_pass"},
                "alex",
                parent_id="C3",
            )

    def test_append_only_revocation_does_not_rewrite_checkpoint_line(self) -> None:
        self.add_c1()
        before = self.store.path.read_bytes()
        add_revocation(self.store, "R1", ["C1"], "bad evidence")
        after = self.store.path.read_bytes()
        self.assertTrue(after.startswith(before))

    def test_extract_manifest_binds_source_and_frame_bytes(self) -> None:
        video = self.root / "video.mp4"
        video.write_bytes(b"video-bytes")
        frames = self.root / "frames"
        frames.mkdir()
        (frames / "frame_000001.png").write_bytes(b"frame-one")
        (frames / "frame_000002.png").write_bytes(b"frame-two")
        descriptor = {
            "id": "extract_001",
            "plan_id": "plan_001",
            "source_video_path": "video.mp4",
            "video_stream": {
                "index": 0,
                "time_base": {"num": 1, "den": 24},
                "avg_frame_rate": {"num": 24, "den": 1},
            },
            "extraction": {
                "tool": "ffmpeg",
                "tool_version": "test",
                "argv_status": "captured",
                "argv": ["ffmpeg", "-i", "video.mp4"],
            },
            "frame_sequence": {
                "directory": "frames",
                "pattern": "frame_%06d.png",
                "first_file_number": 1,
                "first_frame_index": 0,
                "count": 2,
                "first_pts": 0,
                "pts_step": 1,
            },
        }
        record = register_extract_manifest(self.store, descriptor, self.root)
        self.assertEqual(len(record["frames"]), 2)
        self.assertNotEqual(record["source_video_sha256"], "0" * 64)
        self.assertEqual(record["frames"][1]["pts"], 1)


if __name__ == "__main__":
    unittest.main()
