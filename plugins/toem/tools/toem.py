#!/usr/bin/env python3
"""toem — the command a human runs to append what a skill prepared.

Run from the root of an adopted repository. `admit` inserts a reply row above
the closing anchor of CONSTITUTION.md's additions section and the matching
entry under CORRESPONDENCE.md's `## Admitted rows`; `decide` inserts a
three-line decision row above the closing anchor of the decisions section, the
matching entry, and optionally removes the row it settles from PENDING.md;
`pending` appends a waiting row to PENDING.md with today's date and the next
free number. Each prints exactly what it will write, asks before writing
(unless --yes), then runs the guardians and prints the commit command.

It never commits and never pushes. Exit codes: 0 written or dry run, 1 declined
or written with the guardians red, 2 refused before anything was written.
Standard library only; Python 3.9+.
"""
import argparse
import datetime
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent
GUARDIANS = PLUGIN_ROOT / "guardians"

CHARTER = "CONSTITUTION.md"
CORRESPONDENCE = "CORRESPONDENCE.md"
REGISTER = "PENDING.md"
ADMITTED_ROWS = "## Admitted rows"
MIN_REASON = 40

REPLY_HEADING = re.compile(r"^##[ \t]+(Reply to the epilogue|Risposta all['\u2019]epilogo)[ \t]*$", re.M | re.I)
NEXT_HEADING = re.compile(r"^## ", re.M)
SEPARATOR_ROW = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
ROW_ID = re.compile(r"^A-(\d+)$")


# --- refusals -------------------------------------------------------------

def refuse(message):
    """Print a refusal on stderr and exit 2. Nothing has been written when
    this is called: every check runs before the first byte goes to disk."""
    print(f"refused: {message}", file=sys.stderr)
    sys.exit(2)


def normalized(s):
    """Whitespace runs collapsed to single spaces, ends trimmed — the form in
    which text is measured against the 40-character reason floor and the form
    in which it is written into a row, so that no field can carry a line break
    into a grammar the guardians read line by line."""
    return " ".join(s.split())


def require_reason(reason):
    """Return the normalized reason, or refuse naming the count it fell short
    by. The order matters: normalize first, then measure, or forty characters
    of spaces pass for a reason."""
    text = normalized(reason)
    if len(text) < MIN_REASON:
        refuse(
            f"the reason is {len(text)} characters once whitespace is collapsed, "
            f"and {MIN_REASON} is the floor: {text!r}"
        )
    return text


def require_date(value, what):
    """Return `value` if it is a YYYY-MM-DD calendar date, else refuse."""
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        refuse(f"{what} must be a date in the form YYYY-MM-DD: {value!r}")
    return value


def require_field(value, what):
    """Return the normalized value, or refuse when it is empty."""
    text = normalized(value)
    if not text:
        refuse(f"{what} is empty, and the row would say nothing")
    return text


# --- the guardian, as the single definition of what a pointer is ----------

_GUARDIAN = None


def guardian():
    """Import `check_constitution.py` from the plugin's guardians folder, once.

    The runner refuses exactly what the guardian would refuse, so the two share
    one definition of a resolvable pointer instead of holding two that drift.
    """
    global _GUARDIAN
    if _GUARDIAN is not None:
        return _GUARDIAN
    path = GUARDIANS / "check_constitution.py"
    spec = importlib.util.spec_from_file_location("toem_guardian_constitution", path)
    if spec is None or spec.loader is None:
        refuse(f"the guardian is not where the runner expects it: {path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except OSError:
        refuse(f"the guardian is not where the runner expects it: {path}")
    _GUARDIAN = module
    return module


# --- reading the repository ----------------------------------------------

def read(path):
    """File text, decoded UTF-8, with line endings left exactly as they are.

    Opened through `io.open` rather than `Path.read_text(newline=...)`, which
    only accepts that argument from Python 3.13 on: this tool has to run under
    whatever interpreter an adopting repository already has."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path, text):
    """Write `text` verbatim: no line-ending translation, so the LF the runner
    inserts stays LF and every byte it did not touch survives the round trip."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def repo_root():
    """The current directory, refusing when it is not an adopted repository:
    a charter and a correspondence file both have to be there before anything
    can be admitted into either."""
    root = pathlib.Path.cwd()
    if not (root / CHARTER).is_file():
        refuse(f"run this from the root of an adopted repository: no {CHARTER} here ({root})")
    if not (root / CORRESPONDENCE).is_file():
        refuse(f"run this from the root of an adopted repository: no {CORRESPONDENCE} here ({root})")
    return root


def charter_section(text, name):
    """The text between one begin/end anchor pair, refusing when the pair is
    missing, duplicated or out of order — a section the runner cannot find is
    a section it must not guess the position of."""
    body = guardian().section(text, name)
    if body is None:
        refuse(
            f"{CHARTER} has no usable {name} anchors: expected exactly one "
            f"<!-- toem:{name}:begin --> and one <!-- toem:{name}:end -->, in that order"
        )
    return body


def admitted_rows_span(text):
    """(start, end) offsets of the body of `## Admitted rows`, from the end of
    the heading line to the next `## ` heading or the end of file. Refuses
    when the heading is not there."""
    match = re.search(r"^" + re.escape(ADMITTED_ROWS) + r"[ \t]*$", text, re.M)
    if match is None:
        refuse(f"{CORRESPONDENCE} has no `{ADMITTED_ROWS}` heading, and the entry has nowhere to go")
    start = match.end()
    following = NEXT_HEADING.search(text, start)
    return start, following.start() if following else len(text)


def reply_section(text):
    """The reply-to-the-epilogue section of a testament, up to the next `## `
    heading, or None when the testament has no such section."""
    match = REPLY_HEADING.search(text)
    if match is None:
        return None
    start = match.end()
    following = NEXT_HEADING.search(text, start)
    return text[start:following.start()] if following else text[start:]


# --- writing ---------------------------------------------------------------

def insert_above_anchor(text, name, lines):
    """Return `text` with a blank line and `lines` inserted immediately above
    the line carrying `<!-- toem:<name>:end -->`. Everything else is untouched,
    byte for byte, and the inserted lines end with LF."""
    anchor = f"<!-- toem:{name}:end -->"
    at = text.index(anchor)
    line_start = text.rfind("\n", 0, at) + 1
    block = "\n" + "".join(line + "\n" for line in lines)
    return text[:line_start] + block + text[line_start:]


def append_admitted_entry(text, lines):
    """Return `text` with `lines` appended at the end of the `## Admitted rows`
    section, separated by one blank line and followed by one blank line when
    another section follows."""
    _, end = admitted_rows_span(text)
    head, tail = text[:end], text[end:]
    block = "\n\n" + "\n".join(lines) + "\n"
    return head.rstrip("\n") + block + ("\n" + tail if tail else "")


# --- the register ----------------------------------------------------------

def comment_spans(text):
    """Offset spans of every HTML comment, so the commented example row of the
    register is never mistaken for a row of it."""
    return [m.span() for m in re.finditer(r"<!--.*?-->", text, re.S)]


def register_table(text):
    """(header_index, separator_index, rows) for the register's table, where
    rows is a list of (line_index, cells) for the real rows — commented ones
    excluded. Refuses when the header does not name both Since and Status,
    which is the shape the pending guardian needs to be able to fail."""
    lines = text.splitlines(keepends=True)
    spans = comment_spans(text)
    offsets, at = [], 0
    for line in lines:
        offsets.append(at)
        at += len(line)

    def commented(i):
        return any(a <= offsets[i] < b for a, b in spans)

    header = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("|") and "Since" in s and "Status" in s and not commented(i):
            header = i
            break
    if header is None:
        refuse(f"{REGISTER} has no table header naming both Since and Status")

    separator = header + 1 if header + 1 < len(lines) and SEPARATOR_ROW.match(lines[header + 1]) else header
    rows = []
    for i in range(separator + 1, len(lines)):
        s = lines[i].strip()
        if not s.startswith("|") or commented(i) or SEPARATOR_ROW.match(lines[i]):
            continue
        rows.append((i, [c.strip() for c in s.strip("|").split("|")]))
    return header, separator, rows


def next_row_id(rows):
    """The next free `A-NN` identifier, given the register's real rows."""
    used = [int(m.group(1)) for _, cells in rows if cells and (m := ROW_ID.match(cells[0]))]
    return f"A-{(max(used) + 1) if used else 1:02d}"


def normalize_row_id(value):
    """Accept `A-01`, `a-1` or `1` and return the canonical `A-01`."""
    text = value.strip().upper()
    if text.startswith("A-"):
        text = text[2:]
    if not text.isdigit():
        return value.strip()
    return f"A-{int(text):02d}"


def register_row_line(text, wanted):
    """(line_index, line) of the register row whose identifier is `wanted`, or
    refuse naming it — a decision that claims to settle a row nobody can find
    settles nothing."""
    _, _, rows = register_table(text)
    target = normalize_row_id(wanted)
    for i, cells in rows:
        if cells and normalize_row_id(cells[0]) == target:
            return i, text.splitlines(keepends=True)[i]
    refuse(f"{REGISTER} has no row {target}")


# --- the guardians and the commit ------------------------------------------

def find_bash():
    """A POSIX bash able to run the guardians. On Windows the bash shipped
    with git is preferred over any WSL shim, which cannot see drive paths."""
    candidates = []
    if sys.platform == "win32":
        git = shutil.which("git")
        if git:
            candidates.append(pathlib.Path(git).resolve().parents[1] / "bin" / "bash.exe")
        candidates.append(pathlib.Path(r"C:\Program Files\Git\bin\bash.exe"))
    found = shutil.which("bash")
    if found:
        candidates.append(pathlib.Path(found))
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None


def run_guardians(root):
    """Run `guardians/run.sh` against `root`, printing its output. Returns its
    exit code, or None when no bash was found to run it with."""
    bash = find_bash()
    script = GUARDIANS / "run.sh"
    if bash is None or not script.is_file():
        return None
    result = subprocess.run(
        [str(bash), script.as_posix(), pathlib.Path(root).as_posix()],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def finish(root, touched, commit_message):
    """Run the guardians over what was just written, then print the commit
    command — which is never run here. Exits 1 when the guardians are red or
    could not be run, so the shell of whoever pressed knows the charter is not
    in the state they asked for."""
    files = " ".join(touched)
    code = run_guardians(root)
    if code is None:
        print(
            f"written but the guardians could not be run: no bash found — run them yourself, "
            f'or revert with git checkout -- {files}'
        )
        return 1
    if code != 0:
        print(f"written but the guardians are red — fix or revert with git checkout -- {files}")
        return 1
    print()
    print(f'git add {files} && git commit -m "{commit_message}"')
    return 0


def confirm(question, assume_yes):
    """Ask before writing. `--yes` answers for the human who already read the
    blocks; anything but y/yes, and an empty stdin, is a no."""
    if assume_yes:
        return True
    print()
    print(f"{question} ", end="", flush=True)
    try:
        answer = input()
    except EOFError:
        print()
        return False
    return answer.strip().lower() in ("y", "yes")


def show(title, lines):
    """Print one block exactly as it will be written, under its destination."""
    print()
    print(title)
    print()
    for line in lines:
        print(line)


# --- admit -----------------------------------------------------------------

def cmd_admit(args):
    root = repo_root()
    charter_text = read(root / CHARTER)
    additions = charter_section(charter_text, "additions")
    correspondence_text = read(root / CORRESPONDENCE)
    admitted_rows_span(correspondence_text)

    cited = args.file.replace("\\", "/")
    cited = cited[2:] if cited.startswith("./") else cited
    if not cited.startswith("testaments/") or not cited.endswith(".md"):
        refuse(f"an addition row cites a testament under testaments/, and the guardian reads nothing else: {cited}")
    testament = root / cited
    if not testament.is_file():
        refuse(f"no such testament: {cited}")

    section = reply_section(read(testament))
    if section is None:
        refuse(
            f"{cited} has no reply section: the sentence is looked for under "
            f"`## Reply to the epilogue` or `## Risposta all'epilogo`"
        )

    sentence = require_field(args.sentence, "the sentence")
    if sentence not in normalized(section):
        refuse(
            f"the sentence is not in the `## Reply to the epilogue` section of {cited}, "
            f"compared with whitespace collapsed — a row carries the sentence as the mind wrote it"
        )
    if sentence in normalized(guardian().strip_comments(additions)):
        refuse("that sentence is already among the additions, and admitting it twice makes the section look fuller than the practice is")

    reason = require_reason(args.reason)
    by = require_field(args.by, "the name of whoever admits the row")
    when = require_date(args.date or datetime.date.today().isoformat(), "--date")

    row = [f"**{sentence}**", f"— {when}, `{cited}`"]
    entry = [f"**{sentence}**", f"Admitted by {by}, {when}.", f"Reason: {reason}"]
    show(f"{CHARTER} — above <!-- toem:additions:end -->:", row)
    show(f"{CORRESPONDENCE} — under {ADMITTED_ROWS}:", entry)

    if args.dry_run:
        print()
        print("dry run: nothing written")
        return 0
    if not confirm("Append these two blocks? [y/N]", args.yes):
        print("nothing written")
        return 1

    write(root / CHARTER, insert_above_anchor(charter_text, "additions", row))
    write(root / CORRESPONDENCE, append_admitted_entry(correspondence_text, entry))
    print()
    return finish(root, [CHARTER, CORRESPONDENCE], "docs(constitution): a row admitted among the additions")


# --- decide ----------------------------------------------------------------

def cmd_decide(args):
    root = repo_root()
    charter_text = read(root / CHARTER)
    charter_section(charter_text, "decisions")
    correspondence_text = read(root / CORRESPONDENCE)
    admitted_rows_span(correspondence_text)

    decision = require_field(args.decision, "the decision")
    conditions = require_field(args.conditions, "the conditions, which may say no").rstrip(".")
    requirements = require_field(args.requirements, "the requirements, completed by working").rstrip(".")
    reason = require_reason(args.reason)
    by = require_field(args.by, "the name of whoever decides")
    if "," in by:
        refuse(f"the row's grammar reads the name up to the first comma, so the name cannot carry one: {by!r}")
    review_by = require_date(args.review_by, "--review-by")
    when = require_date(args.date or datetime.date.today().isoformat(), "--date")

    pointer = args.pointer.replace("\\", "/").strip()
    if "`" in pointer:
        refuse(f"the pointer sits inside backticks and cannot contain one: {pointer!r}")
    if not guardian()._pointer_ok(pointer, root):
        refuse(
            f"the pointer resolves to nothing that already exists: {pointer!r} is neither a file "
            f"under this repository nor a commit already in its history"
        )

    register_text = None
    leaving = None
    if args.from_pending:
        register_path = root / REGISTER
        if not register_path.is_file():
            refuse(f"no {REGISTER} here, and --from-pending has no row to remove")
        register_text = read(register_path)
        index, line = register_row_line(register_text, args.from_pending)
        lines = register_text.splitlines(keepends=True)
        leaving = line.rstrip("\n")
        register_text = "".join(lines[:index] + lines[index + 1:])

    row = [
        f"**{decision}** — reviewed by {review_by}.",
        f"Conditions (may say no): {conditions}. Requirements (completed by working): {requirements}.",
        f"— {when}, decided by {by}, `{pointer}` — reason: {reason}",
    ]
    entry = [f"**{decision}**", f"Decided by {by}, {when}.", f"Reason: {reason}"]
    show(f"{CHARTER} — above <!-- toem:decisions:end -->:", row)
    show(f"{CORRESPONDENCE} — under {ADMITTED_ROWS}:", entry)
    if leaving is not None:
        show(f"{REGISTER} — the row that leaves the register:", [leaving])

    if args.dry_run:
        print()
        print("dry run: nothing written")
        return 0
    if not confirm("Append these two blocks? [y/N]", args.yes):
        print("nothing written")
        return 1

    write(root / CHARTER, insert_above_anchor(charter_text, "decisions", row))
    write(root / CORRESPONDENCE, append_admitted_entry(correspondence_text, entry))
    touched = [CHARTER, CORRESPONDENCE]
    if register_text is not None:
        write(root / REGISTER, register_text)
        touched.append(REGISTER)
    print()
    return finish(root, touched, "docs(constitution): a decision written into the charter")


# --- pending ---------------------------------------------------------------

def cmd_pending(args):
    root = repo_root()
    register_path = root / REGISTER
    if not register_path.is_file():
        refuse(f"no {REGISTER} here: a decision that waits needs the register to wait in")
    register_text = read(register_path)
    _, separator, rows = register_table(register_text)

    what = require_field(args.what, "what waits")
    closes = require_field(args.closes, "what closes it")
    by = require_field(args.by, "the name of whoever proposes the row")
    when = require_date(args.date or datetime.date.today().isoformat(), "--date")
    for cell, name in ((what, "what waits"), (closes, "what closes it"), (by, "the name")):
        if "|" in cell:
            refuse(f"{name} cannot contain a pipe, which is the column separator of the register: {cell!r}")

    row = f"| {next_row_id(rows)} | {what} | {by} | {when} | {closes} | waiting |"
    show(f"{REGISTER} — a row of the table:", [row])

    if args.dry_run:
        print()
        print("dry run: nothing written")
        return 0
    if not confirm("Append this row? [y/N]", args.yes):
        print("nothing written")
        return 1

    lines = register_text.splitlines(keepends=True)
    at = (rows[-1][0] if rows else separator) + 1
    write(register_path, "".join(lines[:at] + [row + "\n"] + lines[at:]))
    print()
    return finish(root, [REGISTER], "docs(pending): a decision that waits")


# --- the command line ------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="toem",
        description="Append what a skill prepared: a reply admitted, a decision taken, a decision that waits. "
                    "Run from the root of an adopted repository. Never commits.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    def common(sub):
        sub.add_argument("--date", help="YYYY-MM-DD, defaults to today")
        sub.add_argument("--yes", action="store_true", help="do not ask; the blocks are still printed")
        sub.add_argument("--dry-run", action="store_true", help="print the blocks and write nothing")

    admit = subcommands.add_parser("admit", help="admit one sentence of a testament's reply into the additions")
    admit.add_argument("--file", required=True, help="the testament, as testaments/<file>.md")
    admit.add_argument("--sentence", required=True, help="the sentence, as the mind wrote it")
    admit.add_argument("--by", required=True, help="who admits the row")
    admit.add_argument("--reason", required=True, help="why it changes what a mind does tomorrow (40 characters, normalized)")
    common(admit)
    admit.set_defaults(func=cmd_admit)

    decide = subcommands.add_parser("decide", help="write a decision into the charter")
    decide.add_argument("--decision", required=True, help="the decision, in one sentence")
    decide.add_argument("--review-by", required=True, help="YYYY-MM-DD, when the row is looked at again")
    decide.add_argument("--conditions", required=True, help="what would make this decision wrong")
    decide.add_argument("--requirements", required=True, help="what has to be built for it to hold")
    decide.add_argument("--pointer", required=True, help="a file under the repository, or a commit hash already in its history")
    decide.add_argument("--by", required=True, help="who decides")
    decide.add_argument("--reason", required=True, help="why (40 characters, normalized)")
    decide.add_argument("--from-pending", help="the register row this decision settles, as A-NN; removed in the same run")
    common(decide)
    decide.set_defaults(func=cmd_decide)

    pending = subcommands.add_parser("pending", help="add a decision that waits to the register")
    pending.add_argument("--what", required=True, help="the question, phrased so that an answer closes it")
    pending.add_argument("--by", required=True, help="who proposes the row")
    pending.add_argument("--closes", required=True, help="what has to exist or be said for this row to leave")
    common(pending)
    pending.set_defaults(func=cmd_pending)

    return parser


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
