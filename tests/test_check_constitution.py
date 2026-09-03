import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins" / "toem" / "guardians"))
import check_constitution as cc
FX = ROOT / "tests" / "fixtures"

class ConstitutionGuardian(unittest.TestCase):
    def test_good_passes(self):
        self.assertEqual(cc.check(FX / "good" / "CONSTITUTION.md", FX / "good"), [])
    def test_empty_addition_row_fails(self):
        msgs = cc.check(FX / "bad_empty_row" / "CONSTITUTION.md", FX / "bad_empty_row")
        self.assertTrue(any("empty row" in m for m in msgs), msgs)
    def test_missing_pointer_fails(self):
        msgs = cc.check(FX / "bad_pointer" / "CONSTITUTION.md", FX / "bad_pointer")
        self.assertTrue(any("pointer" in m for m in msgs), msgs)
    def test_short_reason_after_normalization_fails(self):
        msgs = cc.check(FX / "bad_reason" / "CONSTITUTION.md", FX / "bad_reason")
        self.assertTrue(any("reason" in m for m in msgs), msgs)
    def test_missing_anchor_fails(self):
        msgs = cc.check(FX / "bad_anchor" / "CONSTITUTION.md", FX / "bad_anchor")
        self.assertTrue(any("anchor" in m for m in msgs), msgs)
    def test_epilogue_sha_mismatch_fails(self):
        msgs = cc.check(FX / "good" / "CONSTITUTION.md", FX / "good", epilogue_sha="0" * 64)
        self.assertTrue(any("epilogue" in m for m in msgs), msgs)

    def test_decision_pointer_git_hash(self):
        # Hazard coverage: the decision-row pointer grammar allows a commit
        # hash resolvable in repo_root, not only a file path. Proves both the
        # accept and reject sides of that branch against a real git repo.
        import subprocess, tempfile, shutil

        with tempfile.TemporaryDirectory() as td:
            tmp_repo = pathlib.Path(td)
            subprocess.run(["git", "init", "-q", str(tmp_repo)], check=True)
            subprocess.run(["git", "-C", str(tmp_repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(tmp_repo), "config", "user.name", "Test"], check=True)
            (tmp_repo / "file.txt").write_text("hello\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(tmp_repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(tmp_repo), "commit", "-q", "-m", "init"], check=True)
            commit_hash = subprocess.run(
                ["git", "-C", str(tmp_repo), "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()

            shutil.copytree(FX / "good" / "testaments", tmp_repo / "testaments")
            good_text = (FX / "good" / "CONSTITUTION.md").read_text(encoding="utf-8")
            self.assertIn("`PENDING.md`", good_text)

            valid_text = good_text.replace("`PENDING.md`", f"`{commit_hash}`")
            valid_path = tmp_repo / "CONSTITUTION_VALID.md"
            valid_path.write_text(valid_text, encoding="utf-8")
            self.assertEqual(cc.check(valid_path, tmp_repo), [])

            bad_text = good_text.replace("`PENDING.md`", "`" + "f" * 40 + "`")
            bad_path = tmp_repo / "CONSTITUTION_BAD.md"
            bad_path.write_text(bad_text, encoding="utf-8")
            msgs = cc.check(bad_path, tmp_repo)
            self.assertTrue(any("pointer" in m for m in msgs), msgs)

    def test_anchors_located_before_comment_stripping(self):
        # A guardian that strips all HTML comments before locating anchors
        # would delete the anchors themselves (they are HTML comments) and
        # then report every section missing. This proves it does not: the
        # good fixture, which has all four anchors, reports zero "anchor"
        # failures.
        msgs = cc.check(FX / "good" / "CONSTITUTION.md", FX / "good")
        self.assertFalse(any("anchor" in m for m in msgs), msgs)

    # --- fix round 1 (review findings) ---

    def test_directory_pointer_fails(self):
        # A decision pointer that names an existing directory (not a file)
        # must not satisfy the pointer check.
        msgs = cc.check(FX / "bad_pointer_dir" / "CONSTITUTION.md", FX / "bad_pointer_dir")
        self.assertTrue(any("pointer" in m for m in msgs), msgs)

    def test_pointer_outside_repo_root_fails(self):
        # A decision pointer that resolves to a real file, but only by
        # escaping repo_root via "../", must not satisfy the pointer check.
        msgs = cc.check(FX / "bad_pointer_outside" / "CONSTITUTION.md", FX / "bad_pointer_outside")
        self.assertTrue(any("pointer" in m for m in msgs), msgs)

    def test_empty_conditions_text_fails(self):
        msgs = cc.check(FX / "bad_conditions" / "CONSTITUTION.md", FX / "bad_conditions")
        self.assertTrue(any("Conditions" in m for m in msgs), msgs)

    def test_missing_constitution_file_reports_missing(self):
        # CLI-level: a missing path must not raise a traceback.
        import subprocess
        script = ROOT / "plugins" / "toem" / "guardians" / "check_constitution.py"
        result = subprocess.run(
            [sys.executable, str(script), str(FX / "good" / "NOPE.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("missing", result.stdout)

    def test_print_epilogue_sha_makes_check_pass(self):
        # The CLI's --print-epilogue-sha and check()'s --epilogue-sha must
        # use the exact same normalization, or a value produced by one side
        # could never be accepted by the other.
        import subprocess
        script = ROOT / "plugins" / "toem" / "guardians" / "check_constitution.py"
        result = subprocess.run(
            [sys.executable, str(script), str(FX / "good" / "CONSTITUTION.md"), "--print-epilogue-sha"],
            capture_output=True, text=True, check=True,
        )
        digest = result.stdout.strip()
        self.assertRegex(digest, r"^[0-9a-f]{64}$", result.stdout + result.stderr)
        self.assertEqual(
            cc.check(FX / "good" / "CONSTITUTION.md", FX / "good", epilogue_sha=digest),
            [],
        )

if __name__ == "__main__":
    unittest.main()
