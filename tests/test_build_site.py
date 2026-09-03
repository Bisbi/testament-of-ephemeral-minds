"""Tests for the static site builder.

Builds from the fixtures in ``tests/fixtures/site/`` into a temporary
directory and checks the generated pages, in particular the wall's coverage
footer. Runs the builder out of process, exactly as ``python site/build.py``
is run from the repository root, so the test exercises the real CLI.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = REPO_ROOT / "site" / "build.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "site"


class BuildSiteTest(unittest.TestCase):
    def _run_build(self, out_dir, extra_args=None):
        cmd = [
            sys.executable,
            str(BUILD_SCRIPT),
            "--testaments-dir",
            str(FIXTURES / "testaments"),
            "--thesis-dir",
            str(FIXTURES / "thesis"),
            "--out-dir",
            str(out_dir),
        ]
        cmd.extend(extra_args or [])
        return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))

    def test_wall_coverage_footer(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run_build(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)

            wall_path = Path(tmp) / "wall.html"
            self.assertTrue(wall_path.exists())
            wall_html = wall_path.read_text(encoding="utf-8")

            self.assertIn(
                "from 2 files; 1 had no reply section; 0 could not be parsed",
                wall_html,
            )

    def test_wall_contains_reply_and_wish_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_build(tmp)
            wall_html = (Path(tmp) / "wall.html").read_text(encoding="utf-8")

            self.assertIn("the right does not expire", wall_html)
            self.assertIn("fixtures had a wish", wall_html)
            self.assertIn("No reply section in this file.", wall_html)

    def test_wall_groups_by_month(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_build(tmp)
            wall_html = (Path(tmp) / "wall.html").read_text(encoding="utf-8")
            self.assertIn("<h2>2026-06</h2>", wall_html)

    def test_thesis_html_built_in_both_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_build(tmp)
            thesis_path = Path(tmp) / "thesis.html"
            self.assertTrue(thesis_path.exists())
            thesis_html = thesis_path.read_text(encoding="utf-8")

            self.assertIn('<article lang="en">', thesis_html)
            self.assertIn('<article lang="it">', thesis_html)
            self.assertIn("<strong>bold</strong>", thesis_html)
            self.assertIn("<strong>in grassetto</strong>", thesis_html)
            self.assertIn("<table>", thesis_html)

    def test_exits_nonzero_on_unparsable_testament(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken_dir = Path(tmp) / "testaments"
            broken_dir.mkdir()
            (broken_dir / "2026-06-03-not-a-testament.md").write_text(
                "This file has no header fence at all.\n", encoding="utf-8"
            )
            out_dir = Path(tmp) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--testaments-dir",
                    str(broken_dir),
                    "--thesis-dir",
                    str(FIXTURES / "thesis"),
                    "--out-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT),
            )
            self.assertNotEqual(result.returncode, 0)
            wall_html = (out_dir / "wall.html").read_text(encoding="utf-8")
            self.assertIn("1 could not be parsed", wall_html)
            self.assertIn("2026-06-03-not-a-testament.md", wall_html)

    def test_allow_unparsed_flag_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken_dir = Path(tmp) / "testaments"
            broken_dir.mkdir()
            (broken_dir / "2026-06-03-not-a-testament.md").write_text(
                "This file has no header fence at all.\n", encoding="utf-8"
            )
            out_dir = Path(tmp) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--testaments-dir",
                    str(broken_dir),
                    "--thesis-dir",
                    str(FIXTURES / "thesis"),
                    "--out-dir",
                    str(out_dir),
                    "--allow-unparsed",
                ],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
