---
name: decide
description: Use when the human wants to record a decision — prepares a row for CONSTITUTION.md § Decisions or PENDING.md in the exact grammar the guardians check, and stops. Never commits, never appends by itself.
---

# Prepare a decision row

The Decisions section of `CONSTITUTION.md` holds what the human has laid down:
the rules they gave themselves and the conditions under which they decide. Rows
are never rewritten — one is added below, dated, pointing at something that
already exists.

This skill prepares the text and stops. It does not open the charter, does not
append, does not commit. Everything below is printed for the human to paste.

## 1. Ask the four fields

Ask them one at a time, in this order, and do not fill any of them in yourself:

1. **The decision**, in one sentence. Not a topic: a sentence that could be
   wrong.
2. **Reviewed by** — the date, `YYYY-MM-DD`, on which the human will look at
   this row again. A decision with no review date is a decision nobody will ever
   reopen.
3. **Conditions (may say no)** — what would make this decision wrong. If the
   answer is "nothing could", the row is not a decision, it is a preference:
   say so and ask again. The guardian fails an empty conditions field, and it is
   right to.
4. **Requirements (completed by working)** — what has to be built for the
   decision to hold. This is the half that gets done by working, not by
   deciding.

## 2. Ask for the pointer

Every row cites something that **already existed when the row was written**:

- a repo-relative path to a file that exists, or
- the 7-to-40-character lowercase hex hash of a commit that is already in the
  history, as `git` prints it. A hash copied from an interface that uppercases
  it is rejected by the guardian.

Never the hash of the commit that introduces this row. That commit does not
exist while the row is being written, and a pointer to it is a promise dressed
as a citation. Check the pointer before printing it: the file must be there, or
`git cat-file -e <hash>^{commit}` must succeed.

## 3. Ask for the reason, and count it

The reason must be at least **40 characters after whitespace normalization** —
whitespace runs collapsed to single spaces, ends trimmed, then measured. Count
it and show the number back to the human before printing the row:

```bash
# use `python` instead of `python3` where that is the interpreter on the PATH
python3 -c 'import sys; s=" ".join(sys.argv[1].split()); print(len(s), repr(s))' "<the reason>"
```

If it comes back under 40, say the count and ask for a fuller reason. Do not pad
it and do not write one on the human's behalf. A reason that will not survive
being written down belongs to a row that was not decided, only typed.

## 4. Print the row

Three lines, exactly this grammar — the guardian reads them as one row and fails
if any of the three is missing:

```
**<the decision, in one sentence>** — reviewed by <YYYY-MM-DD>.
Conditions (may say no): <what would make this decision wrong>. Requirements (completed by working): <what has to be built for it to hold>.
— <YYYY-MM-DD>, decided by <name>, `<file path or commit hash>` — reason: <the reason, ≥ 40 normalized characters>
```

It goes **below** the rows already there, inside `CONSTITUTION.md` between
`<!-- toem:decisions:begin -->` and `<!-- toem:decisions:end -->`. Nothing above
it is edited.

Say also that the same reason belongs in `CORRESPONDENCE.md`, under **Admitted
rows**: the charter holds what was decided, that file holds why, and the two are
kept apart so neither gets edited to tidy up the other.

## 5. A decision that waits is a different row

If the human is not deciding today, nothing goes into the charter. The row goes
into `PENDING.md` instead, in this grammar:

```
| A-01 | <the question, in one line, phrased so that an answer closes it> | <name> | <YYYY-MM-DD> | <what has to exist or be said for this row to leave> | waiting |
```

Two states only. `waiting` means nobody has decided and nobody has named a day —
the guardian fails it after 30 days counted from `Since`. `postponed to
YYYY-MM-DD` means the human looked at it, chose not to decide, and set the day —
the guardian fails it once that date is past. There is no third state: "in
progress" is a state of the work that follows a decision, not of the decision,
and writing it here is how a register stops being able to fail.

**Simultaneity.** When a waiting row is finally decided, the same commit that
adds the row to the charter removes it from the register. Not the next commit,
not later that day. A register that still lists a decision already taken is a
lie the guardian cannot catch, because both files are individually well-formed.

## 6. Print the guardian command, then stop

Give the human this, to run after they have pasted:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/guardians/run.sh" .
```

Expect `constitution: ok` and `pending: ok`. If a line fails, it names what it
found: a pointer that does not resolve, a reason under 40 normalized
characters, an empty conditions field, a missing line of the row.

**The hand that appends is yours: paste, run the guardian, commit.**
