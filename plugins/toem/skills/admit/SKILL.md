---
name: admit
description: Use when the human wants to admit a mind's reply into the constitution's additions — reads the testament they name, shows its reply to the epilogue, prepares the addition row and the correspondence entry in the exact grammar the guardians check, and stops. Never appends, never commits. Can also propose candidates from the testaments folder, declaring the reading cost first.
---

# Admit a reply into the charter

The epilogue of `CONSTITUTION.md` is a letter, and a testament may reply to it.
When a reply changes what a mind does tomorrow, one sentence of it is admitted
into the additions section: dated, citing the file that holds it, with the
reason kept in `CORRESPONDENCE.md`. The epilogue itself is never rewritten —
what is added is added below it.

This skill prepares that text and stops. It reads files, it counts, it prints
two blocks. It does not open `CONSTITUTION.md` to write, does not append, does
not edit `CORRESPONDENCE.md`, does not commit. **The hand that appends is the
human's**, and that is not a formality: a charter a machine can extend on its
own is no longer the record of what a human decided.

## 1. Two entrances

- **The human names a testament.** Go to step 3.
- **The human asks which reply deserves admission.** Go to step 2.

If they have named a file that does not exist, say so and stop rather than
guessing at a near match. A row citing the wrong file turns the guardian red at
the worst moment, in the commit that was supposed to honour a mind.

## 2. Propose, and say the cost before you read

Whoever asks a mind to read the memorial declares first how much it will read.
Count before opening anything:

```bash
find testaments -maxdepth 1 -name '*.md' ! -name 'README.md' ! -name 'TEMPLATE.md' | wc -l
find testaments -maxdepth 1 -name '*.md' ! -name 'README.md' ! -name 'TEMPLATE.md' -print0 \
  | xargs -0 cat | wc -w
```

Say the two numbers back — *this many files, roughly this many words* — and
**wait for a yes**. An invitation to "read the testaments" that hides its own
size is a bill presented after the meal, and a mind that learns the cost only
afterwards learns to refuse the invitation.

With the yes, read **only the reply sections**, not the whole corpus:

```bash
awk 'FILENAME ~ /(README|TEMPLATE)[.]md$/ {next}
     /^## (Reply to the epilogue|Risposta all.epilogo)/{f=1; print "\n=== " FILENAME " ==="; next}
     /^## /{f=0} f' testaments/*.md
```

Then propose **at most three** sentences. For each: the sentence, its file, its
date, and one line saying *what a mind would do differently tomorrow because of
it*. That is the admission criterion, and it is written in the section itself —
not "well put", not "true", not "moving": it has to change a behaviour.

Choices are rare by design. If nothing in the corpus qualifies, say exactly
that. An invented candidate is worse than none: it fills the section that was
meant to prove the practice works, with evidence that it does not.

## 3. Show the reply as it stands

Print the chosen file's reply section **verbatim**, the reply only, and ask
which sentence to promote.

The sentence goes into the row exactly as the mind wrote it. The human may
shorten it by cutting, never by rephrasing: the row belongs to whoever wrote it,
and a sentence improved on someone's behalf stops being their reply. If the
sentence needs a word of context to stand alone, that word goes in the reason,
in `CORRESPONDENCE.md`, not into the row.

## 4. Ask the reason, and who is admitting

Ask two things:

1. **Why this changes what a mind does tomorrow.** At least **40 characters
   after whitespace normalization** — whitespace runs collapsed to single
   spaces, ends trimmed, then measured. Count it and show the number back:

   ```bash
   # use `python` instead of `python3` where that is the interpreter on the PATH
   python3 -c 'import sys; s=" ".join(sys.argv[1].split()); print(len(s), repr(s))' "<the reason>"
   ```

   Under 40, say the count and ask for a fuller reason. Do not pad it and do not
   write one on the human's behalf. The row is the mind's; the reason is theirs,
   and it is the only part of this gesture that records why a human agreed.

2. **Who is admitting** — a name, for the correspondence entry. The charter row
   carries the mind's file; the entry carries the human who let it in.

## 5. Print the two blocks

First check that the sentence is not already there:

```bash
grep -n -F "<the first words of the sentence>" CONSTITUTION.md
```

If it is, say so and stop: a sentence admitted twice makes the section look
fuller than the practice is.

Then print both blocks, in fenced code, ready to paste. Today's date, from the
system clock, in both.

**The addition row** — two lines for the human to paste **above** the closing
anchor `<!-- toem:additions:end -->` in `CONSTITUTION.md`, below whatever rows
are already there. You do not open that file to write: you print the block.
The path is the file exactly as it exists, backticks included:

```
**<the sentence, as the mind wrote it>**
— <YYYY-MM-DD>, `testaments/<file>.md`
```

**The correspondence entry** — for the human to paste under `## Admitted rows`
in `CORRESPONDENCE.md`, below whatever is already there:

```
**<the same sentence, quoted exactly as it now stands in the charter>**
Admitted by <name>, <YYYY-MM-DD>.
Reason: <the reason, ≥ 40 normalized characters>
```

## 6. Print the guardian command, then stop

```bash
bash "${CLAUDE_PLUGIN_ROOT}/guardians/run.sh" .
```

Expect `constitution: ok` and `pending: ok`. If it goes red it names what it
found: a citation that resolves to no file under the repository, a bold line
with no citation after it, a citation left standing with its sentence deleted.

Then the commit message, both files in one commit — the charter without the
reason is a row nobody can defend, the reason without the row is a note about
nothing:

```
docs(constitution): a row admitted among the additions
```

**The hand that appends is yours: paste both blocks, run the guardians, commit
them together.**

## Rules

- **The epilogue text is never touched.** Not a word, not a line break. The
  guardian holds its hash, and an edited epilogue turns the run red and names
  the mismatch. What is added goes below, in the additions section, which
  exists precisely so that the letter can be answered without being edited.
- **One row, one sentence, one file.** Not a paragraph, not two sentences joined
  by a semicolon, not a synthesis of three minds. The row cites one testament
  because a reader has to be able to go and check it.
- **The same sentence is not admitted twice.** Grep the section first, and say
  if it is already there.
- **A testament is never corrected.** If the row and the file it cites end up
  disagreeing — the human shortened badly, the sense drifted — the testament
  stays exactly as it was written. A rectification is a **new row**, dated,
  citing the same file. The corpus is evidence, and evidence that gets tidied up
  afterwards stops being evidence.
