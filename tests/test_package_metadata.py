from __future__ import annotations

import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import cml_trust


class PackageMetadataTests(unittest.TestCase):
    def test_version_matches_pyproject(self) -> None:
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(metadata["project"]["version"], cml_trust.__version__)

    def test_publication_files_exist(self) -> None:
        for filename in (
            "LICENSE",
            "NOTICE",
            "THIRD_PARTY_NOTICES",
            "README.md",
            "CHANGELOG.md",
        ):
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / filename).is_file())

    def test_package_is_marked_alpha(self) -> None:
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertIn("Development Status :: 3 - Alpha", metadata["project"]["classifiers"])
        self.assertIn("a", metadata["project"]["version"])

    def test_public_repository_urls_are_declared(self) -> None:
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        urls = metadata["project"]["urls"]
        self.assertEqual(
            urls["Source"],
            "https://github.com/cstolting-collab/CML-Trust",
        )
        self.assertEqual(
            urls["Issues"],
            "https://github.com/cstolting-collab/CML-Trust/issues",
        )


if __name__ == "__main__":
    unittest.main()
