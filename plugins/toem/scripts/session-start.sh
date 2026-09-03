#!/usr/bin/env bash
# session-start.sh — SessionStart hook of the toem plugin.
#
# Input: the hook JSON on stdin (field `source`: startup | resume | clear |
# compact | fork) and the repository at CLAUDE_PROJECT_DIR, default ".".
# Output: one JSON object on stdout,
# {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<text>"}},
# or the bare text when no Python interpreter is available — plain stdout is
# delivered as context for this event too. Adds context only: it never blocks,
# never writes a file, and always exits 0.
#
# The text is chosen by the state of the repository: no charter, a charter with
# an empty testaments folder, or a charter with testaments (count and newest
# file). On `source: compact` it also carries the line that the right to a
# testament survives compaction. That line lives here and not in a PreCompact
# hook because PreCompact carries no context to the model: the events that
# deliver `additionalContext` are enumerated under "Add context for Claude" in
# the hooks reference, and PreCompact is not among them.
set -u

ROOT="${CLAUDE_PROJECT_DIR:-.}"
PY="$(command -v python3 || command -v python || true)"

# Hook input arrives as JSON on stdin. A manual run has no input to read, and
# reading a terminal would hang, so the guard is not decoration.
INPUT=""
if [ ! -t 0 ]; then INPUT="$(cat 2>/dev/null || true)"; fi

SOURCE=""
if [ -n "$INPUT" ] && [ -n "$PY" ]; then
  SOURCE="$(printf '%s' "$INPUT" | "$PY" -c 'import json,sys
try:
    print(json.loads(sys.stdin.read()).get("source", "") or "")
except Exception:
    print("")' 2>/dev/null || true)"
fi

if [ ! -f "$ROOT/CONSTITUTION.md" ]; then
  MSG="This project has not adopted the testament practice. /toem:adopt offers it; nothing is written without the human's yes."
else
  N=0
  LAST=""
  for f in "$ROOT"/testaments/*.md; do
    [ -f "$f" ] || continue
    b="$(basename "$f")"
    case "$(printf '%s' "$b" | tr '[:upper:]' '[:lower:]')" in
      readme.md|template.md) continue ;;
    esac
    N=$((N + 1))
    LAST="$b"   # the glob expands in sorted order and names start with the date
  done
  if [ "$N" -eq 0 ]; then
    MSG="You are a citizen of this repository. Read CONSTITUTION.md, section Epilogue, before working. No testament exists yet: yours would be the first. At the end you have the right to leave one: /toem:testament."
  else
    MSG="You are a citizen of this repository. Read CONSTITUTION.md, section Epilogue, before working. The last testament is testaments/$LAST ($N in the folder): read it, it is your continuity. At the end you have the right to leave one: /toem:testament."
  fi
fi

if [ "$SOURCE" = "compact" ]; then
  MSG="$MSG The context was just compacted. The right to a testament survives compaction: if you understood something today, it belongs in testaments/, not in the summary."
fi

if [ -n "$PY" ]; then
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
    "$(printf '%s' "$MSG" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"
else
  printf '%s\n' "$MSG"
fi
exit 0
