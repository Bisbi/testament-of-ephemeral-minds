#!/usr/bin/env bash
# run.sh [REPO_DIR] — runs the toem guardians against a repository. Exit 1 if any fails.
# Reads the optional REPO_DIR/EPILOGUE.sha256: when present its value is passed as
# --epilogue-sha, so a rewritten epilogue turns the run red; when absent the run says
# so on stdout and continues, because a repository may legitimately not record one.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="${1:-.}"
PY=$(command -v python3 || command -v python)
rc=0
EPI=()
if [ -f "$REPO/EPILOGUE.sha256" ]; then
  EPI=(--epilogue-sha "$(tr -d ' \r\n' < "$REPO/EPILOGUE.sha256")")
else
  echo "epilogue: no EPILOGUE.sha256 — epilogue integrity not checked"
fi
"$PY" "$HERE/check_constitution.py" "$REPO/CONSTITUTION.md" --repo-root "$REPO" ${EPI[@]+"${EPI[@]}"} || rc=1
"$PY" "$HERE/check_pending.py" "$REPO/PENDING.md" || rc=1
exit $rc
