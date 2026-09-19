#!/usr/bin/env bash
# azd-trust-guard.sh : hook de confiance AZDone (PreToolUse Bash sous Claude Code,
# beforeShellExecution sous Cursor). Délègue la classification à azd-trust-guard.py.
#
# Sans python3, ce script n'utilise que des builtins bash :
#   - aucune politique `enforced` trouvée : autoriser, silencieusement ;
#   - politique `enforced` trouvée : refuser (fail-closed), en expliquant pourquoi.
# Le format de sortie suit l'hôte (voir azd-trust-guard.py et hooks/README.md).
# AZD_TRUST_FILE force le chemin de trust.yaml (tests).

set -uo pipefail

HERE="${BASH_SOURCE[0]%/*}"
[ "$HERE" = "${BASH_SOURCE[0]}" ] && HERE="."

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HERE/azd-trust-guard.py"
fi

RAW="$(</dev/stdin)"

find_trust_file() {
  if [ -n "${AZD_TRUST_FILE:-}" ]; then
    [ -f "$AZD_TRUST_FILE" ] && printf '%s' "$AZD_TRUST_FILE"
    return
  fi
  local start dir
  for start in "${CLAUDE_PROJECT_DIR:-}" "${CURSOR_PROJECT_DIR:-}" "$PWD"; do
    [ -n "$start" ] || continue
    dir="$start"
    while :; do
      if [ -f "$dir/.azdone/trust.yaml" ]; then
        printf '%s' "$dir/.azdone/trust.yaml"
        return
      fi
      [ "$dir" = "/" ] || [ -z "$dir" ] && break
      dir="${dir%/*}"
      [ -z "$dir" ] && dir="/"
    done
  done
}

TRUST_FILE="$(find_trust_file)"
[ -n "$TRUST_FILE" ] || exit 0
CONTENT="$(<"$TRUST_FILE")"
[[ "$CONTENT" =~ (^|$'\n')enforcement:[[:space:]]*enforced ]] || exit 0

REASON="python3 est requis par hooks/azd-trust-guard.sh pour appliquer enforcement: enforced. Refus fail-closed. Installez python3 ou passez enforcement: declared dans .azdone/trust.yaml."
if [[ "$RAW" == *'"tool_input"'* ]] || [[ "$RAW" =~ \"hook_event_name\"[[:space:]]*:[[:space:]]*\"PreToolUse\" ]]; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}' "$REASON"
else
  printf '{"permission":"deny","user_message":"%s","agent_message":"%s"}' "$REASON" "$REASON"
fi
exit 0
