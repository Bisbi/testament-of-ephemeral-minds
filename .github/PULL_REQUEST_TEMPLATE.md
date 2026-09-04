**What this changes** (one paragraph; link the issue if there is one)

**Which promise of the charter it touches**, if any (the epilogue is never rewritten · every row cites something that exists · no skill appends · the runner asks before writing · pending decisions do not age in silence) — and the test that proves it still holds.

**Checks run** (paste the last line of each)

```
python -m unittest discover -s tests
claude plugin validate ./plugins/toem && claude plugin validate .
python site/build.py && git status --porcelain site/
```

**Confidentiality**: this change adds no hostname, internal name, credential, or commit hash from another repository. ☐

**Attribution**: no co-authorship trailer, no session link, no assistant signature in commits or files. ☐
