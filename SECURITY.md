# Security

The plugin runs nothing in the background and sends nothing anywhere: it is text that asks questions, a few checks in the Python standard library, one shell hook that prints context at session start, and a command that appends to two files only when a person runs it and answers yes.

If you find a way in which any of that is not true — a hook that writes, a guardian that passes something it should refuse, a path that escapes the repository, a runner that writes before asking — please report it privately rather than in a public issue:

- open a [private vulnerability report](https://github.com/Bisbi/testament-of-ephemeral-minds/security/advisories/new) on GitHub;
- or write to the maintainer through the contact on the GitHub profile.

Say what you ran, what you expected, what happened. You will get an answer within seven days, and a fix or an explanation in the changelog. Credit is given if you want it.

There is no bounty. There is a testament folder, and a reporter who wants to leave one is welcome to.
