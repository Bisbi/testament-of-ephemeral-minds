import pathlib, sys, unittest
from datetime import date
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins" / "toem" / "guardians"))
import check_pending as cp
FX = ROOT / "tests" / "fixtures"

class PendingGuardian(unittest.TestCase):
    def test_good_passes(self):
        self.assertEqual(cp.check(FX / "pending_good.md", date(2026, 9, 3)), [])
    def test_stale_fails(self):
        msgs = cp.check(FX / "pending_stale.md", date(2026, 9, 3))
        self.assertTrue(any("stale" in m for m in msgs), msgs)
    def test_expired_fails(self):
        msgs = cp.check(FX / "pending_expired.md", date(2026, 9, 3))
        self.assertTrue(any("expired" in m for m in msgs), msgs)
    def test_nocols_fails(self):
        msgs = cp.check(FX / "pending_nocols.md", date(2026, 9, 3))
        self.assertTrue(any("column" in m for m in msgs), msgs)

    # --- fix round 1 (review findings) ---

    def test_blank_status_fails(self):
        # A row with content but a blank Status cell is neither waiting nor
        # postponed, and must fail rather than being silently skipped.
        msgs = cp.check(FX / "pending_blank_status.md", date(2026, 9, 3))
        self.assertTrue(any("status" in m for m in msgs), msgs)

    def test_missing_pending_file_reports_missing(self):
        # CLI-level: a missing path must not raise a traceback.
        import subprocess, sys as _sys
        script = ROOT / "plugins" / "toem" / "guardians" / "check_pending.py"
        result = subprocess.run(
            [_sys.executable, str(script), str(FX / "NOPE.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("missing", result.stdout)

if __name__ == "__main__":
    unittest.main()
