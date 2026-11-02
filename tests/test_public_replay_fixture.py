from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path


class PublicReplayFixtureTests(unittest.TestCase):
    def test_replay_fixture_matches_checked_in_verdicts(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is required by the documented repository requirements")
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [node, str(root / "examples" / "replay-fixture" / "replay.mjs")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("REPLAY FIXTURE: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
