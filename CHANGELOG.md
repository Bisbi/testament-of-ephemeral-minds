# Changelog

## 0.1.1 — 2026-09-07

Patch: no line of the plugin, the guardians or the runner changes. The tag
records what `main` has carried since the first release, so that the release,
the citation and the Zenodo record say the same thing.

- `CITATION.cff` and `.zenodo.json`: the package is citable by DOI, and each
  release gets its own version record with the right title.
- `CONTRIBUTING.md`, `SECURITY.md`, issue and pull request templates.
- The site is published by a workflow from `site/`; social preview, sitemap,
  robots, favicon.
- README: DOI badge and the citation, in both languages; wording of the
  attribution rule.

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
