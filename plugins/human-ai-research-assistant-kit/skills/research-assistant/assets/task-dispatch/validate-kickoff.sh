#!/usr/bin/env bash
# Validate and print a safe DISPATCH / NUDGE kickoff line.
# Usage:
#   validate-kickoff.sh DISPATCH <task_id> <revision>
#   validate-kickoff.sh NUDGE    <task_id> <revision> <token>
# Prints the single-line payload on stdout iff every field passes the
# whitelist; exits non-zero otherwise. Pipe the output to a structured
# send API (e.g. tmux send-keys -l) — never build the line by hand.
set -euo pipefail
ID_RE='^[A-Za-z0-9._-]{1,128}$'
UINT_RE='^[1-9][0-9]*$'
kind="${1:?kind (DISPATCH|NUDGE) required}"; task_id="${2:?task_id required}"; revision="${3:?revision required}"
[[ "$task_id" =~ $ID_RE ]]   || { echo "invalid task_id" >&2; exit 1; }
[[ "$revision" =~ $UINT_RE ]] || { echo "invalid revision" >&2; exit 1; }
case "$kind" in
  DISPATCH) printf 'DISPATCH task_id=%s revision=%s\n' "$task_id" "$revision" ;;
  NUDGE)    token="${4:?token required for NUDGE}"
            [[ "$token" =~ $ID_RE ]] || { echo "invalid token" >&2; exit 1; }
            printf 'NUDGE task_id=%s revision=%s token=%s\n' "$task_id" "$revision" "$token" ;;
  *) echo "kind must be DISPATCH or NUDGE" >&2; exit 1 ;;
esac
