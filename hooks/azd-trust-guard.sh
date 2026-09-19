#!/usr/bin/env bash
# azd-trust-guard.sh — hook de confiance AZDone (PreToolUse Bash / beforeShellExecution).
#
# Lit une commande shell proposée par l'agent, la classe selon .azdone/trust.yaml
# et bloque celles que la politique de confiance n'autorise pas. Bash pur plus
# awk/grep/sed. jq est utilisé s'il est présent, jamais requis. Codex n'a pas de
# hook équivalent: la confiance y reste déclarée seulement (voir hooks/README.md).
#
# Entrée (stdin, JSON):
#   Claude Code: {"hook_event_name":"PreToolUse","tool_input":{"command":"..."},"cwd":"..."}
#   Cursor:      {"hook_event_name":"beforeShellExecution","command":"...","cwd":"...",
#                 "workspace_roots":["..."],"sandbox":"...","conversation_id":"...","generation_id":"..."}
#   Cursor envoie aussi hook_event_name; le format Claude Code se reconnaît à la
#   présence de tool_input, ou à hook_event_name == "PreToolUse", jamais à la
#   seule présence de hook_event_name.
#
# Sortie de blocage (stdout, exit 0 dans les deux cas):
#   Claude Code: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}
#   Cursor:      {"permission":"deny","user_message":"...","agent_message":"..."}
#                (permission accepte allow | ask | deny)
# Autoriser: exit 0 sans aucune sortie sur stdout.
#
# AZD_TRUST_FILE force le chemin de trust.yaml (utile aux tests).

set -uo pipefail

RAW="$(cat)"
RAW_FLAT="$(printf '%s' "$RAW" | tr '\n' ' ')"

HAVE_JQ=0
command -v jq >/dev/null 2>&1 && HAVE_JQ=1

# --- Détection du format et extraction de la commande / du cwd -------------

FORMAT="cursor"
if printf '%s' "$RAW_FLAT" | grep -q '"tool_input"'; then
  FORMAT="claude"
elif printf '%s' "$RAW_FLAT" | grep -Eq '"hook_event_name"[[:space:]]*:[[:space:]]*"PreToolUse"'; then
  FORMAT="claude"
fi

if [ "$HAVE_JQ" = "1" ]; then
  if [ "$FORMAT" = "claude" ]; then
    COMMAND="$(printf '%s' "$RAW" | jq -r '.tool_input.command // empty' 2>/dev/null)"
    CWD="$(printf '%s' "$RAW" | jq -r '.cwd // empty' 2>/dev/null)"
  else
    COMMAND="$(printf '%s' "$RAW" | jq -r '.command // empty' 2>/dev/null)"
    CWD="$(printf '%s' "$RAW" | jq -r '.cwd // (.workspace_roots[0] // empty)' 2>/dev/null)"
  fi
else
  if [ "$FORMAT" = "claude" ]; then
    COMMAND="$(printf '%s' "$RAW_FLAT" | grep -o '"tool_input"[[:space:]]*:[[:space:]]*{[^}]*}' \
      | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' \
      | head -1 | sed -E 's/^"command"[[:space:]]*:[[:space:]]*"(.*)"$/\1/')"
  else
    COMMAND="$(printf '%s' "$RAW_FLAT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' \
      | head -1 | sed -E 's/^"command"[[:space:]]*:[[:space:]]*"(.*)"$/\1/')"
  fi
  CWD="$(printf '%s' "$RAW_FLAT" | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' \
    | head -1 | sed -E 's/^"cwd"[[:space:]]*:[[:space:]]*"(.*)"$/\1/')"
  if [ -z "${CWD:-}" ]; then
    CWD="$(printf '%s' "$RAW_FLAT" | grep -o '"workspace_roots"[[:space:]]*:[[:space:]]*\[[[:space:]]*"[^"]*"' \
      | sed -E 's/^.*"([^"]*)"$/\1/')"
  fi
  COMMAND="$(printf '%s' "${COMMAND:-}" | sed -e 's/\\"/"/g' -e 's/\\\\/\\/g')"
fi

[ -z "${COMMAND:-}" ] && exit 0

# --- Localisation de trust.yaml ---------------------------------------------

if [ -n "${AZD_TRUST_FILE:-}" ]; then
  TRUST_FILE="$AZD_TRUST_FILE"
else
  START_DIR="${CWD:-${CLAUDE_PROJECT_DIR:-${CURSOR_PROJECT_DIR:-$PWD}}}"
  TRUST_FILE=""
  dir="$START_DIR"
  while [ -n "$dir" ]; do
    if [ -f "$dir/.azdone/trust.yaml" ]; then
      TRUST_FILE="$dir/.azdone/trust.yaml"
      break
    fi
    [ "$dir" = "/" ] && break
    dir="$(dirname "$dir")"
  done
fi

if [ -z "${TRUST_FILE:-}" ] || [ ! -f "$TRUST_FILE" ]; then
  exit 0
fi

# --- enforcement -------------------------------------------------------------

ENFORCEMENT="$(grep -E '^enforcement:' "$TRUST_FILE" | head -1 | sed -E 's/^enforcement:[[:space:]]*([A-Za-z_]+).*/\1/')"
if [ "$ENFORCEMENT" != "enforced" ]; then
  exit 0
fi

# --- sortie de blocage -------------------------------------------------------

json_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | tr '\n' ' '
}

deny() {
  local msg esc
  msg="$1"
  esc="$(json_escape "$msg")"
  if [ "$FORMAT" = "claude" ]; then
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$esc"
  else
    printf '{"permission":"deny","user_message":"%s","agent_message":"%s"}\n' "$esc" "$esc"
  fi
  exit 0
}

always_pause_deny() {
  deny "Action toujours-pause: $1. Non contournable, même avec actions.* en auto ou autonomy: full. Voir /azd-setup ou éditer .azdone/trust.yaml (la liste toujours-pause ne peut pas être retirée)."
}

# --- lecture de trust.yaml ----------------------------------------------------

get_action() {
  awk -v n="$1" '
    /^actions:/ { inblock=1; next }
    inblock && /^[^ ]/ { inblock=0 }
    inblock {
      line=$0
      sub(/^[[:space:]]+/, "", line)
      if (line == "") next
      split(line, parts, ":")
      key=parts[1]
      gsub(/[[:space:]]/, "", key)
      if (key == n) {
        val=line
        sub(/^[^:]+:[[:space:]]*/, "", val)
        sub(/[[:space:]]*#.*/, "", val)
        gsub(/[[:space:]]+$/, "", val)
        print val
      }
    }
  ' "$TRUST_FILE"
}

witness_fresh() {
  local witness now mtime age
  witness="$(dirname "$TRUST_FILE")/conditions-ok"
  [ -f "$witness" ] || return 1
  now="$(date +%s)"
  mtime="$(stat -c %Y "$witness" 2>/dev/null || stat -f %m "$witness" 2>/dev/null)"
  [ -z "${mtime:-}" ] && return 1
  age=$((now - mtime))
  [ "$age" -lt 1800 ]
}

decide() {
  local action="$1" reason="$2" value
  value="$(get_action "$action")"
  case "$value" in
    auto)
      exit 0
      ;;
    conditional)
      if witness_fresh; then
        exit 0
      fi
      deny "Action '$action' est 'conditional' ($reason) mais aucun témoin frais .azdone/conditions-ok (moins de 30 minutes). Voir /azd-setup ou éditer .azdone/trust.yaml."
      ;;
    *)
      deny "Action '$action' est '${value:-ask}' dans la politique de confiance ($reason). Voir /azd-setup ou éditer .azdone/trust.yaml pour changer cette politique."
      ;;
  esac
}

# --- classification de la commande -------------------------------------------

is_force_push() {
  printf '%s' "$1" | grep -Eq 'git[[:space:]]+push' || return 1
  printf '%s' "$1" | grep -Eq -- '--force(-with-lease)?([[:space:]]|=|$)|([[:space:]]|^)-f([[:space:]]|$)'
}

is_delete_data() {
  local cmd="$1" paths p
  printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+branch[[:space:]]+-D' && return 0
  printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+push.*--delete' && return 0
  if printf '%s' "$cmd" | grep -Eq 'rm[[:space:]]+-[a-zA-Z]*rf[a-zA-Z]*([[:space:]]|$)|rm[[:space:]]+-[a-zA-Z]*fr[a-zA-Z]*([[:space:]]|$)'; then
    paths="$(printf '%s' "$cmd" | sed -E 's/^.*rm[[:space:]]+-[a-zA-Z]+[[:space:]]*//')"
    for p in $paths; do
      case "$p" in
        -*) continue ;;
        /tmp|/tmp/*) continue ;;
        *) return 0 ;;
      esac
    done
  fi
  return 1
}

if is_force_push "$COMMAND"; then
  always_pause_deny "force-push (git push --force / -f)"
fi

if is_delete_data "$COMMAND"; then
  decide "delete_data" "suppression de données ou de branche"
fi

if printf '%s' "$COMMAND" | grep -Eq 'deploy|kubectl[[:space:]]+apply|terraform[[:space:]]+apply|vercel[[:space:]]+--prod|fly[[:space:]]+deploy|helm[[:space:]]+upgrade'; then
  decide "deploy" "déploiement ou mutation d'infrastructure"
fi

if printf '%s' "$COMMAND" | grep -Eq 'gh[[:space:]]+pr[[:space:]]+merge|git[[:space:]]+merge.*(main|master)'; then
  decide "merge" "fusion vers la branche principale"
fi

if printf '%s' "$COMMAND" | grep -Eq 'gh[[:space:]]+pr[[:space:]]+create|glab[[:space:]]+mr[[:space:]]+create'; then
  decide "open_pr" "ouverture de pull/merge request"
fi

if printf '%s' "$COMMAND" | grep -Eq 'git[[:space:]]+push'; then
  decide "push" "envoi vers le remote"
fi

if printf '%s' "$COMMAND" | grep -Eq 'npm[[:space:]]+i(nstall)?[[:space:]]+-g|pip[[:space:]]+install[[:space:]]+--user|brew[[:space:]]+install'; then
  decide "install_global" "installation globale"
fi

exit 0
