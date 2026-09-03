# On Omarchy

Omarchy already treats coding agents as first-class citizens of the desktop, and
it says so in its own manual: every major coding-agent command line comes
pre-wired as a lazy-loaded launcher, Claude Code among them, with a default
agent selectable from the command line, a keyboard shortcut that starts it, and
a usage panel in the top bar. It also ships a skill of its own for those agents:
when a process crashes, the crash is handed to the default agent together with
Omarchy's `diagnose-crash` skill, written in the same `SKILL.md` format this
package uses. See <https://omarchy.org/manual/ai/>.

That has a direct consequence for anyone reading this on an Omarchy machine:
**there is nothing different to do.** The practice arrives through Claude Code,
which is already there, so the installation is the same two commands as anywhere
else.

```
/plugin marketplace add Bisbi/testament-of-ephemeral-minds
/plugin install toem@testament-of-ephemeral-minds
```

Then `/toem:adopt` in the repository you want to offer the practice to. No
Omarchy-specific step, no extra configuration, no separate build.

Omarchy does have a real plugin system, and it is a good one: a third-party
plugin is a git repository with a `manifest.json` at its root, installed with
`omarchy plugin add`, validated, namespaced, enabled and disabled from the
command line. But its domain is the desktop shell. The manifest declares kinds
like `bar-widget`, `panel`, `overlay`, `menu` and `service`, and their entry
points are QML files that draw and run inside the long-lived shell process. See
<https://omarchy.org/manual/shell-plugins/>. None of the kinds documented there
is an agent's skill; we found no command that installs instructions for an
agent, and nothing in that system touches the files of a project.

**So there is no Omarchy plugin here, and that is a decision, not an
oversight.** This practice is text that asks questions: a charter, an epilogue
with a right of reply, a template, a register, and a few checks that read
Markdown. Wrapped as a shell plugin it would be a widget with no content, and it
would claim a presence in a place where nothing of the practice actually runs.
The honest channel is the one that already reaches every Omarchy user who opens
Claude Code.

If a native-looking presence is still wanted, the honest form is a card, not a
plugin. Omarchy's community directory (<https://omarchyplugins.com/>, which
redirected to <https://plugins.omarchy.org/> when this was checked, on
2026-09-03) lists what exists in the ecosystem, and an entry there can point at
this repository and say plainly what it is: a Claude Code plugin, installed with
the two commands above, not an `omarchy-shell` plugin. That is the whole of it.
A card says where to find something; a fake plugin would say that something runs
where it does not.
