from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / "review" / "operation-coffee-cup-run006-review.html"
EXPECTED_VIDEO_SHA256 = (
    "27af50dc6d7c2f5b0967deed1d55cd9290474f02faa6658317cbe988228615fe"
)


class BrowserReviewFormTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = FORM.read_text(encoding="utf-8")

    def test_form_is_self_contained_and_network_free(self) -> None:
        lowered = self.source.lower()
        self.assertNotIn('src="http', lowered)
        self.assertNotIn('href="http', lowered)
        self.assertNotIn("fetch(", lowered)
        self.assertNotIn("xmlhttprequest", lowered)
        self.assertNotIn("websocket", lowered)

    def test_form_binds_expected_video_and_splits_boundary_questions(self) -> None:
        self.assertIn(EXPECTED_VIDEO_SHA256, self.source)
        self.assertIn('id: "inv_005_pre"', self.source)
        self.assertIn('id: "inv_005_post"', self.source)
        self.assertIn("screen-right", self.source)
        self.assertIn("screen-left", self.source)

    def test_form_does_not_cue_known_second_handle_finding(self) -> None:
        self.assertNotIn("second handle", self.source.lower())
        self.assertNotIn("handle appears on each side", self.source.lower())

    def test_form_has_eight_observational_questions(self) -> None:
        question_ids = re.findall(r'^\s+id: "(inv_[^"]+)"', self.source, re.MULTILINE)
        self.assertEqual(
            question_ids,
            [
                "inv_001",
                "inv_002",
                "inv_003",
                "inv_004",
                "inv_005_pre",
                "inv_005_post",
                "inv_006",
                "inv_007",
            ],
        )

    def test_embedded_javascript_parses(self) -> None:
        scripts = re.findall(r"<script>(.*?)</script>", self.source, re.DOTALL)
        self.assertEqual(len(scripts), 1)
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "review-form.js"
            script.write_text(scripts[0], encoding="utf-8")
            completed = subprocess.run(
                ["node", "--check", str(script)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
