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
