#!/usr/bin/env bash
# Installe les skills et sous-agents AZDone dans un projet cible.
#
# Usage :
#   scripts/install.sh <claude|cursor|codex> [chemin-projet=.]
#
# Le script ne copie que les dossiers de skills AZDone (*-azd, azd,
# azd-setup) et n'ecrase jamais un fichier hors de ces dossiers. Il est
# idempotent : le relancer met a jour les fichiers AZDone sans toucher au
# reste du projet cible. Il ne supprime jamais rien : aucune suppression
# recursive et forcee de fichiers.
set -euo pipefail

usage() {
  echo "Usage: scripts/install.sh <claude|cursor|codex> [chemin-projet]" >&2
  echo "  claude : copie vers .claude/skills et .claude/agents" >&2
  echo "  cursor : copie vers .cursor/skills et .cursor/agents" >&2
  echo "  codex  : copie vers .agents/skills (pas de sous-agents Codex)" >&2
}

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  usage
  exit 1
fi

host="$1"
target="${2:-.}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

case "$host" in
  claude)
    skills_dir=".claude/skills"
    agents_dir=".claude/agents"
    ;;
  cursor)
    skills_dir=".cursor/skills"
    agents_dir=".cursor/agents"
    ;;
  codex)
    skills_dir=".agents/skills"
    agents_dir=""
    ;;
  *)
    echo "Hote inconnu : ${host}" >&2
    usage
    exit 1
    ;;
esac

if [ ! -d "$target" ]; then
  echo "Chemin projet introuvable : ${target}" >&2
  exit 1
fi

target="$(cd "$target" && pwd)"

mkdir -p "${target}/${skills_dir}"

copied_skills=0
for skill_path in "${repo_root}/skills"/*; do
  [ -d "$skill_path" ] || continue
  name="$(basename "$skill_path")"
  case "$name" in
    *-azd|azd|azd-setup)
      mkdir -p "${target}/${skills_dir}/${name}"
      cp -R "${skill_path}/." "${target}/${skills_dir}/${name}/"
      copied_skills=$((copied_skills + 1))
      ;;
    *)
      # Dossier hors convention AZDone : jamais copie.
      ;;
  esac
done

echo "Skills AZDone copies : ${copied_skills} -> ${target}/${skills_dir}"

if [ -n "$agents_dir" ] && [ -d "${repo_root}/agents" ]; then
  mkdir -p "${target}/${agents_dir}"
  agent_count=0
  for agent_file in "${repo_root}/agents"/*.md; do
    [ -f "$agent_file" ] || continue
    cp "$agent_file" "${target}/${agents_dir}/"
    agent_count=$((agent_count + 1))
  done
  echo "Sous-agents AZDone copies : ${agent_count} -> ${target}/${agents_dir}"
elif [ "$host" != "codex" ]; then
  echo "Aucun dossier agents/ trouve dans le depot AZDone (rien copie)."
fi

echo ""
if [ "$host" = "codex" ]; then
  echo "Lancez \$azd-setup dans ${target}."
else
  echo "Lancez /azd-setup dans ${target}."
fi

if [ "$host" = "claude" ]; then
  echo ""
  echo "Alternative : installer AZDone comme plugin Claude Code depuis GitHub."
  echo "  claude plugin marketplace add charlescstpierr/azdone"
  echo "  claude plugin install azdone@azdone"
  echo "Cette voie namespace les commandes : /azdone:azd, /azdone:azd-setup."
fi

# Copie du hook de confiance (jamais requis, jamais enregistre automatiquement :
# modifier settings.json / hooks.json exige l'accord explicite de l'humain).
if [ "$host" = "claude" ] || [ "$host" = "cursor" ]; then
  if [ "$host" = "claude" ]; then
    hook_dir="${target}/.claude/hooks/azdone"
  else
    hook_dir="${target}/.cursor/hooks/azdone"
  fi

  if [ -f "${repo_root}/hooks/azd-trust-guard.sh" ]; then
    mkdir -p "${hook_dir}"
    cp "${repo_root}/hooks/azd-trust-guard.sh" "${hook_dir}/azd-trust-guard.sh"
    chmod +x "${hook_dir}/azd-trust-guard.sh"
    if [ -f "${repo_root}/hooks/azd-trust-guard.py" ]; then
      cp "${repo_root}/hooks/azd-trust-guard.py" "${hook_dir}/azd-trust-guard.py"
      chmod +x "${hook_dir}/azd-trust-guard.py"
    fi
    echo ""
    echo "Hook de confiance copie (non enregistre) -> ${hook_dir}/azd-trust-guard.sh"
  fi

  if [ "$host" = "claude" ]; then
    echo ""
    echo "Pour l'enregistrer, ajoutez ce bloc a ${target}/.claude/settings.json (fusionner, ne pas ecraser) :"
    echo '  {"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/azdone/azd-trust-guard.sh\""}]}]}}'
    echo "Ce script ne modifie jamais settings.json lui-meme."
  else
    echo ""
    echo "Pour l'enregistrer, ajoutez ce bloc a ${target}/.cursor/hooks.json (fusionner, ne pas ecraser) :"
    echo '  {"version":1,"hooks":{"beforeShellExecution":[{"command":"bash \"./.cursor/hooks/azdone/azd-trust-guard.sh\""}]}}'
    echo "Chemin relatif utilise volontairement : VERIFIED_FORMATS.md ne confirme pas la variable CURSOR_PROJECT_DIR pour un hooks.json de projet (hors plugin)."
    echo "Ce script ne modifie jamais hooks.json lui-meme."
  fi
fi

if [ "$host" = "codex" ]; then
  echo ""
  echo "Codex : aucun mode enforced. La confiance y reste 'declared' seulement, aucun hook ne s'y execute."
fi
