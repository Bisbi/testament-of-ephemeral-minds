# Changelog

## 0.1.0 — 2026-09-03

- First package: the `toem` plugin — a constitution with a right of reply, the
  testament rite, the register of decisions that wait, the guardians, the
  SessionStart hook, the thesis and the site.
- `/toem:admit`: the skill that prepares the row admitting a mind's reply into
  the charter's additions, and the entry that keeps the reason. It reads, it
  prints two blocks, and it stops.
- `toem`: the command the human runs to append what a skill prepared — a reply
  admitted, a decision taken, a decision that waits. It shows what it will
  write, asks before writing, touches only the intended lines, runs the
  guardians, and prints the commit command without running it.
