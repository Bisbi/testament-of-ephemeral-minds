"""End-to-end tests for guardians/run.sh: the exit code an adopter sees, and
the epilogue-integrity wiring that only exists in the runner. The unit tests
in test_check_constitution.py cover --epilogue-sha as a library call; these
prove the shipped command actually passes it."""
import os
import pathlib
import shutil
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARDIANS = ROOT / "plugins" / "toem" / "guardians"
RUN_SH = GUARDIANS / "run.sh"
FX = ROOT / "tests" / "fixtures"

EPILOGUE_SENTENCE = "Reading, here, is not informing yourself"


def _find_bash():
    """Locate a POSIX bash able to run run.sh. On Windows prefer the bash
    shipped with git over any WSL shim, which cannot see the drive paths the
    test passes in."""
    candidates = []
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            candidates.append(pathlib.Path(git).resolve().parents[1] / "bin" / "bash.exe")
        candidates.append(pathlib.Path(r"C:\Program Files\Git\bin\bash.exe"))
    found = shutil.which("bash")
    if found:
        candidates.append(pathlib.Path(found))
    for c in candidates:
        if c and c.exists():
            return c
    return None


BASH = _find_bash()


@unittest.skipIf(BASH is None, "no bash interpreter available to run run.sh")
class RunSh(unittest.TestCase):
    def _repo(self):
        """A temp copy of the good fixture, cleaned up with the test."""
        import tempfile

        td = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, td, True)
        repo = pathlib.Path(td) / "repo"
        shutil.copytree(FX / "good", repo)
        return repo

    def _run(self, repo):
        return subprocess.run(
            [str(BASH), RUN_SH.as_posix(), repo.as_posix()],
            capture_output=True, text=True,
        )

    def _record_epilogue(self, repo):
        digest = subprocess.run(
            [sys.executable, str(GUARDIANS / "check_constitution.py"),
             str(repo / "CONSTITUTION.md"), "--print-epilogue-sha"],
            capture_output=True, text=True, check=True,
        ).stdout
        (repo / "EPILOGUE.sha256").write_text(digest, encoding="utf-8")

    def test_without_recorded_epilogue_passes_and_says_it_is_unchecked(self):
        repo = self._repo()
        r = self._run(repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("no EPILOGUE.sha256", r.stdout)

    def test_recorded_epilogue_passes(self):
        repo = self._repo()
        self._record_epilogue(repo)
        r = self._run(repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("no EPILOGUE.sha256", r.stdout)
        self.assertIn("constitution: ok", r.stdout)
        self.assertIn("pending: ok", r.stdout)

    def test_edited_epilogue_turns_the_run_red(self):
        repo = self._repo()
        self._record_epilogue(repo)
        charter = repo / "CONSTITUTION.md"
        text = charter.read_text(encoding="utf-8")
        self.assertIn(EPILOGUE_SENTENCE, text)
        charter.write_text(
            text.replace(EPILOGUE_SENTENCE, "Reading, here, is not learning about yourself"),
            encoding="utf-8",
        )
        r = self._run(repo)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("epilogue", r.stdout)

    def test_failing_guardian_exits_non_zero(self):
        repo = self._repo()
        (repo / "PENDING.md").unlink()
        r = self._run(repo)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
