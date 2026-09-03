# Pending — decisions that wait

A decision that waits has a row here. When it is taken it leaves this file and
is written where it belongs: the Decisions section of `CONSTITUTION.md` if it is
a rule the human gives themselves, a specification if it shapes what gets built,
or a commit that declares it if it is neither. This register holds what has not
been decided yet. It is not an archive of what was, and a row that stays after
the decision was taken is a lie the guardian cannot catch.

A row is in one of two states. `waiting` means nobody has decided and nobody has
named a day. `postponed to YYYY-MM-DD` means the human looked at it, chose not
to decide, and set the date on which they will. There is no third state: "in
progress" is not a state of a decision, it is a state of the work that follows
one, and writing it here is how a register stops being able to fail.

The guardian fails a row in the two ways a decision rots. A row `waiting` for
more than 30 days fails, counted from `Since`. A `postponed to` date already in
the past fails. The columns `Since` and `Status` are mandatory and must keep their
names: without the entry date the count of days does not exist, and without the
state there is nothing to check. Whoever prunes them in good faith is left with
a register whose guardian can never fail anything.

| # | What waits | Proposed by | Since | What closes it | Status |
|---|---|---|---|---|---|
| A-01 | Should the guardian CI job run on every push or only on pull requests? | Giovanni | 2026-08-20 | A written decision row in CONSTITUTION.md | waiting |
