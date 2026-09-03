#!/usr/bin/env python3
"""Guardian for PENDING.md: the required table columns exist, no `waiting`
row is older than `max_days`, no `postponed to` date has already passed,
and every non-blank row has a recognized status (a filled row with a blank
Status cell fails; only a fully blank row is skipped).

CLI: prints each failure and exits 1, or prints "pending: ok" and exits 0;
a missing path prints "<path>: missing" and exits 1 instead of raising.
Library entry point: check(path, today, max_days=30).
"""
import argparse
import datetime
import pathlib
import re
import sys

POSTPONED = re.compile(r"^postponed to (\d{4}-\d{2}-\d{2})$")


def strip_comments(s):
    """Remove HTML comments (`<!-- ... -->`, multiline) from a string —
    keeps the commented example row out of the parsed table."""
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def _find_header(lines):
    """Return (header_index, {column_name: index}) for the first pipe-table
    header row that names both `Since` and `Status`, or (None, None)."""
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("|") and "Since" in s and "Status" in s:
            cols = [c.strip() for c in s.strip("|").split("|")]
            if "Since" in cols and "Status" in cols:
                return i, {name: idx for idx, name in enumerate(cols)}
    return None, None


def check(path, today, max_days=30):
    """Check the pending register at `path` as of `today`. Returns a list
    of failure messages (empty means pass). See module docstring."""
    text = strip_comments(pathlib.Path(path).read_text(encoding="utf-8"))
    lines = text.splitlines()
    failures = []

    header_idx, col_index = _find_header(lines)
    if header_idx is None:
        failures.append("missing required column(s): header must name both Since and Status")
        return failures

    since_i = col_index["Since"]
    status_i = col_index["Status"]

    row_start = header_idx + 1
    if row_start < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[row_start]):
        row_start += 1

    for line in lines[row_start:]:
        s = line.strip()
        if not s.startswith("|"):
            continue
        cols = [c.strip() for c in s.strip("|").split("|")]
        if len(cols) <= max(since_i, status_i):
            continue
        if not any(cols):
            continue  # fully blank row (e.g. a stray "|||||" separator-like line)
        since_str, status_str = cols[since_i], cols[status_i]

        try:
            since_date = datetime.datetime.strptime(since_str, "%Y-%m-%d").date()
        except ValueError:
            failures.append(f"invalid Since date: {since_str!r}")
            continue

        if not status_str:
            failures.append(f"unknown status (must be waiting or postponed to YYYY-MM-DD): blank status cell for row since {since_str}")
            continue

        if status_str == "waiting":
            age = (today - since_date).days
            if age > max_days:
                failures.append(f"stale: row waiting since {since_str} is {age} days old (max {max_days})")
            continue

        m = POSTPONED.match(status_str)
        if m:
            postponed_date = datetime.datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if postponed_date < today:
                failures.append(f"expired: postponed-to date {m.group(1)} is in the past")
            continue

        failures.append(f"unknown status (must be waiting or postponed to YYYY-MM-DD): {status_str!r}")

    return failures


def main():
    ap = argparse.ArgumentParser(description="Check PENDING.md against the toem guardian rules.")
    ap.add_argument("path", type=pathlib.Path)
    ap.add_argument("--today", default=None, help="YYYY-MM-DD, defaults to the current date")
    ap.add_argument("--max-days", type=int, default=30)
    args = ap.parse_args()

    today = (
        datetime.datetime.strptime(args.today, "%Y-%m-%d").date()
        if args.today
        else datetime.date.today()
    )
    try:
        failures = check(args.path, today, max_days=args.max_days)
    except OSError:
        print(f"{args.path}: missing")
        sys.exit(1)
    if failures:
        for f in failures:
            print(f)
        sys.exit(1)
    print("pending: ok")


if __name__ == "__main__":
    main()
