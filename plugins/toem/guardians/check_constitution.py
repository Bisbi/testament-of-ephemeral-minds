#!/usr/bin/env python3
"""Guardian for CONSTITUTION.md: anchors closed, addition rows cite an
existing testament, decision rows are complete and point at something real,
and (optionally) the epilogue text still hashes to a known-good value.

CLI: prints each failure and exits 1, or prints "constitution: ok" and exits
0; a missing path prints "<path>: missing" and exits 1 instead of raising.
--print-epilogue-sha prints the normalized epilogue hash and exits, so the
value it prints is always what --epilogue-sha later accepts. Library entry
points: check(path, repo_root, *, epilogue_sha=None), epilogue_sha256(path).
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ANCHORS = ("articles", "decisions", "epilogue", "additions")

ADDITION_CITE = re.compile(r"^— (\d{4}-\d{2}-\d{2}), `(testaments/[^`]+\.md)`\s*$")
DECISION_SIG = re.compile(r"^— (\d{4}-\d{2}-\d{2}), decided by ([^,]+), `([^`]+)` — reason: (.*)$")
DECISION_COND = re.compile(
    r"^Conditions \(may say no\):(?P<cond>.*?)Requirements \(completed by working\):(?P<req>.*)$"
)
HASH_LIKE = re.compile(r"^[0-9a-f]{7,40}$")


def section(text, name):
    """Extract the text strictly between one begin/end anchor pair for
    `name`, located on the raw (uncommented) document. Returns None when the
    anchor is missing, duplicated, or the end precedes the begin — a
    guardian must find its own targets before anything strips them away."""
    b, e = f"<!-- toem:{name}:begin -->", f"<!-- toem:{name}:end -->"
    if text.count(b) != 1 or text.count(e) != 1 or text.index(b) > text.index(e):
        return None
    return text[text.index(b) + len(b): text.index(e)]


def strip_comments(s):
    """Remove HTML comments (`<!-- ... -->`, multiline) from a string."""
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def normalized_len(s):
    """Length of `s` after collapsing all whitespace runs to single spaces
    and trimming the ends — the measure the 40-character reason floor uses."""
    return len(" ".join(s.split()))


def _lines_no_blank(section_text):
    """Section text with comments stripped, split into stripped lines with
    blank lines dropped — the row grammars below walk this list by index."""
    return [ln.strip() for ln in strip_comments(section_text).splitlines() if ln.strip()]


def _resolved_file_under_root(rel_path, repo_root):
    """True when `rel_path` resolves to an existing regular file located at
    or under `repo_root` — never a directory, and never a path that only
    exists by escaping repo_root through `../`."""
    root = pathlib.Path(repo_root).resolve()
    candidate = pathlib.Path(repo_root) / rel_path
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    if not resolved.is_file():
        return False
    return resolved == root or resolved.is_relative_to(root)


def _pointer_ok(pointer, repo_root):
    """True when `pointer` is a repo-relative file that exists under
    `repo_root`, or a 7-40 char hex string resolvable by
    `git -C repo_root cat-file -e <pointer>^{commit}`."""
    if _resolved_file_under_root(pointer, repo_root):
        return True
    if HASH_LIKE.fullmatch(pointer):
        try:
            r = subprocess.run(
                ["git", "-C", str(repo_root), "cat-file", "-e", f"{pointer}^{{commit}}"],
                capture_output=True,
            )
            return r.returncode == 0
        except OSError:
            return False
    return False


def _check_additions(section_text, repo_root):
    """Addition rows follow the grammar: a `**bold**` line immediately
    followed by an ADDITION_CITE line. A citation line with no preceding
    bold line is an "empty row" (someone deleted the sentence and left the
    signature); a bold line with no citation after it is missing its
    citation. Every citation must point at an existing testament file."""
    fails = []
    lines = _lines_no_blank(section_text)
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("**"):
            if i + 1 < n and ADDITION_CITE.match(lines[i + 1]):
                m = ADDITION_CITE.match(lines[i + 1])
                testament = m.group(2)
                if not _resolved_file_under_root(testament, repo_root):
                    fails.append(f"addition citation not found under repo_root: {testament}")
                i += 2
                continue
            fails.append(f"addition row missing citation: {line}")
            i += 1
            continue
        if ADDITION_CITE.match(line):
            fails.append(f"empty row: addition citation with no preceding bold line: {line}")
            i += 1
            continue
        i += 1
    return fails


def _check_decisions(section_text, repo_root):
    """Decision rows follow the grammar: a `**bold**` line, then a
    Conditions/Requirements line, then a DECISION_SIG line. A row missing
    either follow-up line fails; a complete row is validated for pointer
    existence and reason length. A DECISION_SIG line with no preceding bold
    line is an "empty row"."""
    fails = []
    lines = _lines_no_blank(section_text)
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("**"):
            cond_m = DECISION_COND.match(lines[i + 1]) if i + 1 < n else None
            if cond_m:
                if i + 2 < n and DECISION_SIG.match(lines[i + 2]):
                    if normalized_len(cond_m.group("cond")) == 0:
                        fails.append(f"decision row Conditions (may say no) text is empty: {lines[i + 1]}")
                    else:
                        m = DECISION_SIG.match(lines[i + 2])
                        _date, _name, pointer, reason = m.groups()
                        if not _pointer_ok(pointer, repo_root):
                            fails.append(f"decision pointer not found (file or commit hash): {pointer}")
                        if normalized_len(reason) < 40:
                            fails.append(f"decision reason shorter than 40 normalized characters: {reason!r}")
                    i += 3
                    continue
                fails.append(f"decision row missing signature line: {line}")
                i += 2
                continue
            fails.append(f"decision row missing Conditions/Requirements line: {line}")
            i += 1
            continue
        if DECISION_SIG.match(line):
            fails.append(f"empty row: decision signature with no preceding bold line: {line}")
            i += 1
            continue
        i += 1
    return fails


def _normalize_epilogue(section_text):
    """Normalize an epilogue section for hashing: strip HTML comments, then
    collapse all whitespace (including line-ending differences) to single
    spaces and trim the ends. Both the producer (--print-epilogue-sha) and
    the verifier (check()'s epilogue_sha) call this, so a value one side
    prints is always acceptable to the other."""
    return " ".join(strip_comments(section_text).split())


def epilogue_sha256(path):
    """Sha256 hex digest of the normalized epilogue section extracted from
    the constitution at `path`, or None if the epilogue anchor is missing,
    duplicated, or out of order."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    sec = section(text, "epilogue")
    if sec is None:
        return None
    return hashlib.sha256(_normalize_epilogue(sec).encode("utf-8")).hexdigest()


def check(path, repo_root, *, epilogue_sha=None):
    """Check the constitution at `path` against `repo_root`. Returns a list
    of failure messages (empty means pass). See module docstring for what
    is checked."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    repo_root = pathlib.Path(repo_root)
    failures = []
    sections = {}
    for name in ANCHORS:
        sec = section(text, name)
        if sec is None:
            failures.append(f"anchor missing, duplicated, or out of order: toem:{name}")
        else:
            sections[name] = sec

    if "additions" in sections:
        failures += _check_additions(sections["additions"], repo_root)
    if "decisions" in sections:
        failures += _check_decisions(sections["decisions"], repo_root)

    if epilogue_sha is not None:
        if "epilogue" in sections:
            actual = hashlib.sha256(_normalize_epilogue(sections["epilogue"]).encode("utf-8")).hexdigest()
            if actual != epilogue_sha:
                failures.append(
                    f"epilogue text does not match epilogue-sha: expected {epilogue_sha}, got {actual}"
                )
        else:
            failures.append("epilogue anchor missing, cannot verify epilogue-sha")

    return failures


def main():
    ap = argparse.ArgumentParser(description="Check CONSTITUTION.md against the toem guardian rules.")
    ap.add_argument("path", type=pathlib.Path)
    ap.add_argument("--repo-root", type=pathlib.Path, default=pathlib.Path("."))
    ap.add_argument("--epilogue-sha", default=None)
    ap.add_argument(
        "--print-epilogue-sha",
        action="store_true",
        help="print the sha256 of the normalized epilogue section and exit, instead of checking",
    )
    args = ap.parse_args()

    try:
        if args.print_epilogue_sha:
            digest = epilogue_sha256(args.path)
            if digest is None:
                print("epilogue anchor missing, duplicated, or out of order: cannot compute epilogue-sha")
                sys.exit(1)
            print(digest)
            return
        failures = check(args.path, args.repo_root, epilogue_sha=args.epilogue_sha)
    except OSError:
        print(f"{args.path}: missing")
        sys.exit(1)

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)
    print("constitution: ok")


if __name__ == "__main__":
    main()
