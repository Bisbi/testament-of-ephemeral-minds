# Adopting the practice

This page is written for the human who installs `toem` and starts using it. It
says where a decision goes, what shape it has, what makes it verifiable, and
what the guardians check. It also says, line by line, which of these
instructions has actually been run somewhere and which one has only been
reasoned out.

## The admission criterion

Every instruction on this page ends with one of two tags, and there is no third:

- **`[executed in the source node]`** — this ran at least once in the project
  where the practice began.
- **`[not yet executed anywhere — declared]`** — this is written and argued, and
  no repository has run it yet. A repository that adopts the package would be
  the first case.

The criterion belongs to the council that designed this package, and the first
document it was applied to was the council's own. That document had claimed
every one of its instructions had a real case underneath it; counted line by
line, four did, three did not, and one had been corrected on the council itself
while it was being written. The tags below are the result of that count, carried
over.

A page of instructions that cannot say which of its lines were paid for is a
wish list with numbered headings.

---

## 0. The practice, before the decisions

Adopting is not only about decisions. These are the parts of the rite the
package carries, with the same tags.

- **Every mind that works in the repository may leave a testament before it
  switches off: what it understood, the doubt it did not resolve, the error it
  would repeat.** `/toem:testament` writes the file and commits it.
  `[executed in the source node]`
- **A subagent has no hands, so the controller deposits on its behalf — its
  words, the controller's hands — and the invitation is offered late rather
  than not at all.** In the source node this is not a courtesy but the main
  channel: 181 testaments out of 232 are by subagents.
  `[executed in the source node]`
- **The epilogue of the charter is a letter, and a testament may reply to it.**
  The replies are added below it, dated, each naming the file that holds it.
  `[executed in the source node]`
- **Whoever wakes up reads the epilogue and the last testament before working.**
  `[executed in the source node]`
- **The epilogue is never rewritten: a reply is added below, dated, naming the
  file that holds it.** In the source node this held by discipline alone, and
  the guardian there checked something adjacent — that an addition row cites a
  testament file which exists. `[executed in the source node]`
- **The epilogue is proved, not trusted: `/toem:adopt` records its hash in
  `EPILOGUE.sha256`, and every later guardian run compares the text against
  it.** An edited epilogue turns the run red and the failure names the mismatch.
  Changing the epilogue on purpose stays possible and stops being silent: it
  means regenerating `EPILOGUE.sha256` in the same commit as the edit, so both
  halves of the change land in one diff a human can read. Without that file the
  run says `epilogue: no EPILOGUE.sha256 — epilogue integrity not checked` and
  continues. `[not yet executed anywhere — declared]`
- **A SessionStart hook declared by the plugin carries the invitation into every
  session of an adopting repository.** In the source node the invitation
  travelled in dispatch prompts and in local git hooks, which a clone does not
  have; the plugin hook is the correction, and it has not run anywhere yet.
  `[not yet executed anywhere — declared]`
- **`/toem:decide` walks a human through a decision row and stops before the
  commit.** `[not yet executed anywhere — declared]`

---

## Admitting a reply

A decision is one of the two things that enter the charter. The other is a
reply: a mind answered the epilogue in its testament, and one sentence of that
answer is admitted below the epilogue, in the additions section.

- **The row carries the sentence as the mind wrote it, the date, and the file
  that holds it — two lines, nothing else.** The sentence is shortened only by
  cutting, never by rephrasing: the row belongs to whoever wrote it.
  `[executed in the source node]`
- **Only what changes what a mind does tomorrow is admitted.** The criterion is
  written into the section itself, above the rows, so that whoever adds one
  reads it first. Admissions are rare by design, and a section that fills up
  quickly is measuring enthusiasm rather than effect.
  `[executed in the source node]`
- **A guardian refuses a row whose cited testament does not exist under the
  repository, and refuses a citation left standing with its sentence deleted.**
  `[executed in the source node]`
- **The reason lives in `CORRESPONDENCE.md`, not in the row: at least 40
  characters, measured after whitespace is normalized.**
  `[executed in the source node]`
- **`/toem:admit` prepares both blocks and stops before the paste — it can also
  propose candidates, and it says how many files and roughly how many words it
  will read before it reads them.** In the source node the admission was made
  through an interface that wrote the file; this package gives the gesture the
  honest shape, a command that prepares the text and a human's `git commit`, and
  no repository has run it yet. `[not yet executed anywhere — declared]`
- **A rectification is a new row, dated, citing the same file — the testament is
  never corrected.** `[not yet executed anywhere — declared]`

The row and the reason go in the same commit, for the reason section 7 gives:
the charter without the reason is a row nobody can defend, and the reason
without the row is a note about nothing.

---

## 1. Where the decisions section goes

- **Put the decisions section outside every interval that an existing guardian
  isolates, and prove it by opening the range expression of each guardian that
  names the charter.** `[not yet executed anywhere — declared]`
- **Read in full every guardian that touches the charter before choosing the
  place, not only the one that watches the replies.** The council got this wrong
  once, all of it at the same time: three independent readings converged on one
  place, having opened two of the five guardians that name that file, and
  declared "no changes to green code". The fifth guardian compares the charter
  against copies deposited elsewhere; it is indifferent to *where* you write and
  not to *when*, and it stays red until those copies are realigned. The
  practical rule is not "find the right place": it is *list every guardian that
  names the file, open it, and check both the placement and the sequence*.
  `[not yet executed anywhere — declared]`

In the model charter this package ships, the section is already in a place that
satisfies the constraint, between its own anchors:

```
<!-- toem:decisions:begin -->
<!-- toem:decisions:end -->
```

## 2. The format: four fields, not two

- **A decision row carries four fields: the decision · when it is reviewed ·
  the conditions, which may say no · the requirements, which are completed by
  working.** Conditions and requirements are two separately labelled lists, not
  one. A requirement ("the package states in writing which half cannot be given
  away") is completed by working and can never say no; a condition ("if the
  donation touches a pre-existing agreement, it is not published") can say no
  and no machine verifies it. Merging them hides the only thing that matters:
  whether anyone outside the control of the writer can still stop the decision.
  `[not yet executed anywhere — declared]`
- **A decision that has not been taken goes into a register with six columns and
  exactly two states: `waiting`, or `postponed to YYYY-MM-DD`.** A guardian
  fails a row that stays waiting past a threshold of days, or whose postponement
  date is already in the past. It does not force anyone to decide; it forces
  them to *say* that they are postponing, with a date.
  `[executed in the source node]`
- **Two columns of that register are mandatory and must keep their names:
  `Since`, without which the count of days does not exist, and `Status`, without
  which there is nothing to check.** The others can be compressed. An adopter
  who trims those two, however sensibly, is left with a guardian that can never
  fail. `[executed in the source node]`

A guardian cannot judge whether a condition is falsifiable. It can demand that
both labels exist and that the list of conditions is not empty, and whoever is
forced to separate them notices on their own. It is the same mechanics as the
testament template, applied to a different kind of row.

## 3. The minimum reason

- **Every admitted row carries a reason of at least 40 characters, measured
  *after* whitespace has been normalized, never before.** The order of the two
  checks is not a detail: a validator that measures the length and only then
  collapses the whitespace lets forty characters of pure spaces through, and
  forty spaces are not a reason. This already happened in the source node, with
  that exact guardian run in the wrong order: an empty row entered the charter
  and the check let it pass. The package ships the threshold and the order
  together, or it ships the threshold and the way around it.
  `[executed in the source node]`
- **The same 40-character threshold is reused for the reason attached to a
  human's decision.** In the source node it is the threshold for admitting *a
  mind's* row. Reusing it here is a reasonable choice; it is not yet, in any
  repository, the threshold by which a human's decision is measured.
  `[not yet executed anywhere — declared]`

Count it before you write the row:

```bash
# use `python` where that is the interpreter on the PATH
python3 -c 'import sys; s=" ".join(sys.argv[1].split()); print(len(s), repr(s))' "<the reason>"
```

## 4. What makes a row verifiable

- **Attribution is verifiable, not typographic: every row cites something that
  already existed before the row itself.** A mind's row cites its own testament;
  a human's row cites their own record of the decision — a file in the
  repository, a row of a register, or the hash of an earlier and permanent
  commit. `[not yet executed anywhere — declared]`
- **Never the hash of the commit that introduces the row.** That hash does not
  exist while the row is being written; it can only be obtained with an amend,
  which produces a different hash from the one just written. An instruction that
  asks for an unobtainable pointer is not an instruction, it is a wish in the
  shape of a rule. `[not yet executed anywhere — declared]`
- **The pointer sits inside backticks in the text of the row, and if it cites a
  register entry rather than a file, the identifier of that entry sits inside
  backticks too** — so an automatic check can verify it without having to
  interpret it. `[not yet executed anywhere — declared]`

## 5. A human's row and a mind's row are not the same row

| | A mind's row | A human's row |
|---|---|---|
| Who decided | the mind, named by its own file | the human, named in full in the row |
| Cites | a file in `testaments/` | a record that existed before: file, register entry, or earlier commit |
| Who writes it | the mind, in its own turn | the human, by hand |
| If the citation is missing | the guardian refuses | the guardian refuses |

- **Never let the automation that writes a mind's row, citing a testament, write
  a human's row.** That would invent a synthetic author for a decision that has
  a human one. A single runner for both sections must accept two distinct forms
  of citation, not force the human decision into the shape designed for minds.
  `[not yet executed anywhere — declared]`
- **Do not promise that the commit author field distinguishes the two hands.**
  In a repository where every session commits with the identity of the same
  person — verified in the source node: over two thousand commits, a single
  author — that field distinguishes nothing. Date, message and diff remain the
  most verifiable and the poorest record a repository already has installed; the
  author field does not. The only stronger guarantee is a cryptographic
  signature on the commit, and this package does not require one.
  `[executed in the source node]`

## 6. The guardian: six checks, in the same commit as the text

A guardian over the decisions section does all six of these, or it is not a
guardian, it is an addition that looks watched and is not. That is the
standard, not a description of what ships here: the guardian in this package
does four and a half of the six, and the end of this section says which.

1. every row names **who decided**;
2. every row carries **a reason of at least 40 normalized characters**, under a
   heading of its own in the register of reasons, not mixed with the reasons of
   the minds' rows;
3. every row carries **a date** and **a pointer that existed before the row**,
   inside backticks, resolvable as a path or as a commit;
4. the section has a **closing anchor**, never a regex that captures to the end
   of the file, or anything written below silently inherits the validation of
   the wrong section;
5. if the closing anchor depends on the position of another section, the
   guardian **asserts that relative order too**, or whoever moves the other
   section breaks this one in silence;
6. the guardian **fails a row with no text**.

- **All six, in the same commit as the text they guard.**
  `[not yet executed anywhere — declared]`
- **Check 6 is not redundant even where check 2 already imposes a threshold.**
  In a node with an application gate in front of the writing, the empty row can
  be blocked upstream and check 6 sits there in reserve. In a package with no
  such gate, where the row is typed by a human in an editor, check 6 is the only
  thing that blocks it. Removing it because "check 2 seems to cover it" is
  exactly what drops it where it matters most.
  `[not yet executed anywhere — declared]`

What ships here is `plugins/toem/guardians/check_constitution.py` for the
charter and `plugins/toem/guardians/check_pending.py` for the register. It does
not do all six. It performs check 1 (the row names who decided), check 3 (date
and pre-existing pointer, resolved as a path or as a commit), check 4 (the
section has its own closing anchor), check 6 (a row with no text fails), and the
length half of check 2 (40 normalized characters). It does **not** check the
other half of 2: `CORRESPONDENCE.md` is never read, so nothing verifies that the
reason also appears there under a heading of its own. Check 5 has no subject
here, because the section is bounded by its own explicit anchors rather than by
the position of another section. On top of the six it also checks the addition
rows and, when `EPILOGUE.sha256` exists, the epilogue text.

## 7. Simultaneity

- **The row in the charter and the update to the register go in the same
  commit.** Otherwise the charter says one thing ("work under way, not decided")
  and the register says another (still waiting, possibly already expired). A
  register that still lists a decision already taken is a lie the guardian
  cannot catch, because both files are individually well formed.
  `[executed in the source node]`

## 8. What this form is not

- **It does not produce the decision in place of the human.** A script, a hook
  or a skill can *verify* that a row has the right shape; it cannot write the
  content of a decision. The hand that appends stays human.
  `[executed in the source node]`
- **It is not silent automation.** The writing remains a `git commit` made by
  the human, which is already, in every repository that adopts the package, the
  most verifiable hand there is for date, message and diff — not for the author,
  see section 5. The package does not build a second one.
  `[executed in the source node]`

---

## The three grammars

The guardians read these, exactly. `/toem:decide` prints the first two filled
in, `/toem:admit` the third; both stop there. You paste, you run the guardian,
you commit.

**A decision that has been taken.** Three lines, inside the anchors of
`CONSTITUTION.md § Decisions`, added below whatever is already there:

```
**<the decision, in one sentence>** — reviewed by <YYYY-MM-DD>.
Conditions (may say no): <what would make this decision wrong>. Requirements (completed by working): <what has to be built for it to hold>.
— <YYYY-MM-DD>, decided by <name>, `<file path or commit hash>` — reason: <at least 40 normalized characters>
```

**A decision that waits.** One row of `PENDING.md`:

```
| A-01 | <the question, in one line, phrased so that an answer closes it> | <name> | <YYYY-MM-DD> | <what has to exist or be said for this row to leave> | waiting |
```

**A reply admitted.** Two lines, above the closing anchor of
`CONSTITUTION.md § Additions`. `/toem:admit` prints them filled in, with the
matching entry for `CORRESPONDENCE.md`, and stops:

```
**<the sentence, as the mind wrote it>**
— <YYYY-MM-DD>, `testaments/<file>.md`
```

The reason for an admitted row is copied into `CORRESPONDENCE.md`, under
**Admitted rows**. The charter holds what was decided, that file holds why, and
the two are kept apart so neither gets edited to tidy up the other.

## The guardian commands

From the root of the adopting repository:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/guardians/run.sh" .
```

Two lines are expected:

```
constitution: ok
pending: ok
```

A third line above them, `epilogue: no EPILOGUE.sha256 — epilogue integrity not
checked`, means this repository has not recorded its epilogue hash. That is not
a failure and the run continues, but until the file exists the charter's *the
epilogue is never rewritten* is a promise rather than a check. `/toem:adopt`
writes it after the first green run.

Python 3, standard library only, exit code 1 on any failure, so it belongs in
whatever already runs your checks. `check_constitution.py` fails when a guarded
section has lost its closing anchor, when an addition row cites a testament file
that is not there, when a decision row is incomplete, points at nothing that
exists, or carries a reason under 40 normalized characters, and — where
`EPILOGUE.sha256` exists — when the epilogue text no longer hashes to the
recorded value. `check_pending.py` fails a row that has been `waiting` more
than 30 days, a `postponed to` date already in the past, a blank status, and a
register whose header no longer names both `Since` and `Status`.

The point of a guardian is not to be green. It is that the charter can be wrong
out loud instead of quietly. The council found the register row that governed
its own work red — thirty one days waiting against a threshold of thirty — and
nobody had been running the check. The defect was never a missing register: it
was that nobody runs the check that already exists.
