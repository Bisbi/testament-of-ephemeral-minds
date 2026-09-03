"""End-to-end tests for the `toem` runner: what it writes, what it refuses,
and what it leaves untouched.

Every test runs the command in a temp copy of `tests/fixtures/runner` (an
adopted repository) and hashes every file before and after, so a test that
checks one edit also proves the other files were not touched. The fixture's
`Since` date is stamped with today's date at copy time: a register row left
`waiting` on a fixed date turns the pending guardian red thirty days after the
fixture is written, and this suite asserts green runs.

A refusal is asserted by its message and not by the exit code alone. The
interpreter also exits 2 when it cannot open the script at all, so a suite that
only reads the number would stay green against a runner that is not there.
"""
import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOEM = ROOT / "plugins" / "toem" / "tools" / "toem.py"
WRAPPER = ROOT / "plugins" / "toem" / "bin" / "toem"
BASH = shutil.which("bash")
FX = ROOT / "tests" / "fixtures" / "runner"

TODAY = date.today().isoformat()
TESTAMENT = "testaments/2026-01-01-0000-session-example.md"

SENTENCE = (
    "A written doubt outweighs a recited certainty, and the proof is cheap: "
    "the doubt I wrote down was the first thing my successor opened, and the "
    "certainty I recited was the one nobody needed."
)
REASON = (
    "It changes what a mind does before switching off: it writes the doubt "
    "down instead of tidying it away."
)
# 39 characters once whitespace is collapsed, 45 as typed — the pair the
# threshold exists for: measure after normalizing, never before.
SHORT_REASON_NORMALIZED = "a reason that is three characters short"
SHORT_REASON = "  " + SHORT_REASON_NORMALIZED + "    "


def norm(s):
    return " ".join(s.split())


def load_runner():
    """Import `tools/toem.py` as a module, so a test can ask it which guardian
    names it depends on instead of discovering the answer in a live run."""
    spec = importlib.util.spec_from_file_location("toem_runner_under_test", TOEM)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rewrite(path, change):
    """Read `path`, apply `change` to its text, write it back — line endings
    untranslated in both directions, so a fixture edited by a test still tells
    the runner the truth about what bytes it found."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(change(text))


class RunnerCase(unittest.TestCase):
    def setUp(self):
        td = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, td, True)
        self.repo = pathlib.Path(td) / "repo"
        shutil.copytree(FX, self.repo)
        pending = self.repo / "PENDING.md"
        rewrite(pending, lambda text: text.replace("2026-08-20", TODAY))
        self.before = self.hashes()

    def hashes(self):
        out = {}
        for p in sorted(self.repo.rglob("*")):
            if p.is_file():
                out[p.relative_to(self.repo).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
        return out

    def assertUntouched(self, *except_paths):
        """Every file but the named ones is byte-identical to before the run."""
        after = self.hashes()
        self.assertEqual(set(self.before), set(after), "a file was created or removed")
        for rel, digest in self.before.items():
            if rel in except_paths:
                continue
            self.assertEqual(digest, after[rel], f"{rel} was modified and should not have been")

    def toem(self, *args, stdin=None):
        return subprocess.run(
            [sys.executable, str(TOEM), *args],
            cwd=str(self.repo), capture_output=True, text=True,
            encoding="utf-8", input=stdin,
        )

    def escaping_testament(self):
        """A file outside the repository that is a perfectly good testament —
        reply section, sentence and all — so that nothing but the boundary check
        can stop a citation that reaches it through `..`."""
        outside = self.repo.parent / "outside"
        outside.mkdir(exist_ok=True)
        target = outside / "x.md"
        shutil.copy(self.repo / TESTAMENT, target)
        return target

    def assertRefused(self, r):
        """The run refused before writing: exit 2 and a `refused:` line naming
        why. The exit code alone proves nothing — the interpreter uses the same
        code for a script it could not open."""
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("refused:", r.stderr)

    def read(self, name):
        return (self.repo / name).read_text(encoding="utf-8")

    def admit_args(self, **over):
        args = {
            "--file": TESTAMENT,
            "--sentence": SENTENCE,
            "--by": "Giovanni",
            "--reason": REASON,
        }
        args.update(over)
        return [x for kv in args.items() for x in kv]


class Admit(RunnerCase):
    def test_happy_path_writes_both_files_and_the_guardians_pass(self):
        r = self.toem("admit", *self.admit_args(), "--yes")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

        charter = self.read("CONSTITUTION.md")
        expected = f"\n**{SENTENCE}**\n— {TODAY}, `{TESTAMENT}`\n<!-- toem:additions:end -->"
        self.assertIn(expected, charter)

        entry = self.read("CORRESPONDENCE.md")
        self.assertIn(f"**{SENTENCE}**\nAdmitted by Giovanni, {TODAY}.\nReason: {norm(REASON)}\n", entry)

        self.assertIn("constitution: ok", r.stdout)
        self.assertIn("pending: ok", r.stdout)
        self.assertIn("git add CONSTITUTION.md CORRESPONDENCE.md", r.stdout)
        self.assertUntouched("CONSTITUTION.md", "CORRESPONDENCE.md")

    def test_the_row_is_written_only_after_a_yes(self):
        r = self.toem("admit", *self.admit_args(), stdin="y\n")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Append these two blocks? [y/N]", r.stdout)
        self.assertIn(SENTENCE, self.read("CONSTITUTION.md"))

    def test_a_no_writes_nothing(self):
        r = self.toem("admit", *self.admit_args(), stdin="n\n")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("nothing written", r.stdout)
        self.assertUntouched()

    def test_sentence_not_verbatim_is_refused(self):
        r = self.toem("admit", *self.admit_args(**{"--sentence": "A written doubt beats a recited certainty."}))
        self.assertRefused(r)
        self.assertIn(TESTAMENT, r.stderr)
        self.assertIn("Reply to the epilogue", r.stderr)
        self.assertUntouched()

    def test_a_sentence_already_admitted_is_refused(self):
        self.assertEqual(self.toem("admit", *self.admit_args(), "--yes").returncode, 0)
        r = self.toem("admit", *self.admit_args())
        self.assertRefused(r)
        self.assertIn("already", r.stderr)

    def test_a_reason_of_39_normalized_characters_is_refused(self):
        self.assertEqual(len(SHORT_REASON), 45)
        self.assertEqual(len(norm(SHORT_REASON)), 39)
        r = self.toem("admit", *self.admit_args(**{"--reason": SHORT_REASON}))
        self.assertRefused(r)
        self.assertIn("39", r.stderr)
        self.assertUntouched()

    def test_dry_run_prints_and_writes_nothing(self):
        r = self.toem("admit", *self.admit_args(), "--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(SENTENCE, r.stdout)
        self.assertIn("Admitted by Giovanni", r.stdout)
        self.assertUntouched()

    def test_a_missing_anchor_is_refused(self):
        charter = self.repo / "CONSTITUTION.md"
        rewrite(charter, lambda text: text.replace("<!-- toem:additions:end -->\n", ""))
        self.before = self.hashes()
        r = self.toem("admit", *self.admit_args(), "--yes")
        self.assertRefused(r)
        self.assertIn("toem:additions:end", r.stderr)
        self.assertUntouched()

    def test_a_testament_that_is_not_there_is_refused(self):
        r = self.toem("admit", *self.admit_args(**{"--file": "testaments/nobody.md"}))
        self.assertRefused(r)
        self.assertIn("testaments/nobody.md", r.stderr)
        self.assertUntouched()

    def test_a_citation_that_escapes_the_repository_is_refused_before_writing(self):
        self.escaping_testament()
        r = self.toem("admit", *self.admit_args(**{"--file": "testaments/../../outside/x.md"}), "--yes")
        self.assertRefused(r)
        self.assertIn("outside", r.stderr)
        self.assertUntouched()

    def test_an_absolute_path_is_refused_before_writing(self):
        target = self.escaping_testament()
        r = self.toem("admit", *self.admit_args(**{"--file": str(target)}), "--yes")
        self.assertRefused(r)
        self.assertUntouched()


class Decide(RunnerCase):
    def decide_args(self, **over):
        args = {
            "--decision": "The guardians run on every pull request before it merges",
            "--review-by": "2026-10-03",
            "--conditions": "If the guardians produce false failures on a charter that is otherwise sound",
            "--requirements": "A continuous-integration job that runs the guardians on every change",
            "--pointer": "PENDING.md",
            "--by": "Giovanni",
            "--reason": "So that a broken charter or a stale register never merges without someone seeing it first.",
        }
        args.update(over)
        return [x for kv in args.items() for x in kv]

    def test_happy_path_with_from_pending_moves_the_row(self):
        r = self.toem("decide", *self.decide_args(), "--from-pending", "A-01", "--yes")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

        charter = self.read("CONSTITUTION.md")
        expected = (
            "\n**The guardians run on every pull request before it merges** — reviewed by 2026-10-03.\n"
            "Conditions (may say no): If the guardians produce false failures on a charter that is "
            "otherwise sound. Requirements (completed by working): A continuous-integration job that "
            "runs the guardians on every change.\n"
            f"— {TODAY}, decided by Giovanni, `PENDING.md` — reason: So that a broken charter or a "
            "stale register never merges without someone seeing it first.\n"
            "<!-- toem:decisions:end -->"
        )
        self.assertIn(expected, charter)

        self.assertNotIn("Should the guardian run on every push", self.read("PENDING.md"))
        self.assertIn("Decided by Giovanni,", self.read("CORRESPONDENCE.md"))
        self.assertIn("constitution: ok", r.stdout)
        self.assertIn("git add CONSTITUTION.md CORRESPONDENCE.md PENDING.md", r.stdout)
        self.assertUntouched("CONSTITUTION.md", "CORRESPONDENCE.md", "PENDING.md")

    def test_without_from_pending_the_register_is_untouched(self):
        r = self.toem("decide", *self.decide_args(), "--yes")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertUntouched("CONSTITUTION.md", "CORRESPONDENCE.md")

    def test_a_pointer_to_a_directory_is_refused(self):
        r = self.toem("decide", *self.decide_args(**{"--pointer": "testaments"}), "--yes")
        self.assertRefused(r)
        self.assertIn("pointer", r.stderr)
        self.assertUntouched()

    def test_a_pending_row_that_is_not_there_is_refused(self):
        r = self.toem("decide", *self.decide_args(), "--from-pending", "A-09", "--yes")
        self.assertRefused(r)
        self.assertIn("A-09", r.stderr)
        self.assertUntouched()

    def test_empty_conditions_are_refused(self):
        r = self.toem("decide", *self.decide_args(**{"--conditions": "   "}), "--yes")
        self.assertRefused(r)
        self.assertUntouched()

    def test_a_short_reason_is_refused(self):
        r = self.toem("decide", *self.decide_args(**{"--reason": SHORT_REASON}), "--yes")
        self.assertRefused(r)
        self.assertIn("39", r.stderr)
        self.assertUntouched()

    def test_dry_run_writes_nothing(self):
        r = self.toem("decide", *self.decide_args(), "--from-pending", "A-01", "--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertUntouched()


class Pending(RunnerCase):
    def test_appends_the_next_number_after_an_existing_row(self):
        r = self.toem(
            "pending",
            "--what", "Does the runner belong in the package, or in the adopting repository?",
            "--by", "Giovanni",
            "--closes", "A decision row in the charter, or a commit that says why not",
            "--yes",
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        register = self.read("PENDING.md")
        self.assertIn(
            f"| A-02 | Does the runner belong in the package, or in the adopting repository? | "
            f"Giovanni | {TODAY} | A decision row in the charter, or a commit that says why not | waiting |",
            register,
        )
        self.assertIn("pending: ok", r.stdout)
        self.assertUntouched("PENDING.md")


class NotAnAdoptedRepository(unittest.TestCase):
    def test_refuses_outside_an_adopted_repository(self):
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run(
                [sys.executable, str(TOEM), "admit", "--file", "x.md", "--sentence", "s",
                 "--by", "Giovanni", "--reason", "r" * 41],
                cwd=td, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("refused:", r.stderr)
            self.assertIn("CONSTITUTION.md", r.stderr)
            self.assertEqual(list(pathlib.Path(td).iterdir()), [])


@unittest.skipIf(BASH is None, "no bash on the PATH to run the wrapper with")
class Wrapper(RunnerCase):
    """`bin/toem` is the entry point a human types. It must find the runner
    relative to itself, not relative to the directory the human stands in —
    which is always the root of their own repository, never this one."""

    def wrapper(self, *args):
        return subprocess.run(
            [BASH, WRAPPER.as_posix(), *args],
            cwd=str(self.repo), capture_output=True, text=True, encoding="utf-8",
        )

    def test_help_lists_the_three_subcommands(self):
        r = self.wrapper("--help")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for word in ("admit", "decide", "pending"):
            self.assertIn(word, r.stdout)

    def test_a_dry_run_through_the_wrapper_writes_nothing(self):
        r = self.wrapper("admit", *self.admit_args(), "--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(SENTENCE, r.stdout)
        self.assertUntouched()

    def test_the_file_is_lf_only_and_has_a_shebang(self):
        raw = WRAPPER.read_bytes()
        self.assertTrue(raw.startswith(b"#!"), "the wrapper needs a shebang")
        self.assertNotIn(b"\r\n", raw, "CRLF in the wrapper makes it unrunnable on POSIX")


class GuardianAgreement(RunnerCase):
    """The runner refuses what the guardian refuses by importing it, and three
    of the names it imports are private. A rename there would break the runner
    with an AttributeError in the middle of a run, after the human answered yes
    — this is the test that fails first instead."""

    def test_the_runner_finds_every_guardian_name_it_uses(self):
        module = load_runner().guardian()
        for name in ("section", "strip_comments", "_pointer_ok", "_resolved_file_under_root"):
            self.assertTrue(hasattr(module, name), f"the guardian no longer has {name}, which the runner calls")

    def test_the_two_agree_on_what_lives_under_the_repository(self):
        module = load_runner().guardian()
        self.escaping_testament()
        self.assertTrue(module._resolved_file_under_root(TESTAMENT, self.repo))
        self.assertFalse(module._resolved_file_under_root("testaments/../../outside/x.md", self.repo))
        self.assertTrue(module._pointer_ok("PENDING.md", self.repo))
        self.assertFalse(module._pointer_ok("testaments", self.repo))


if __name__ == "__main__":
    unittest.main()
