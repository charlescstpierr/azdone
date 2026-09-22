#!/usr/bin/env bash
# Installe les skills et sous-agents AZDone dans un projet cible, ou dans la
# configuration personnelle de l'hote.
#
# Usage :
#   scripts/install.sh <claude|cursor|codex> [chemin-projet=.]
#   scripts/install.sh <claude|cursor|codex> --global [--copy]
#
# Le script ne copie que les dossiers de skills AZDone (*-azd, azd,
# azd-setup) et n'ecrase jamais un fichier hors de ces dossiers. Il est
# idempotent : le relancer met a jour les fichiers AZDone sans toucher au
# reste du projet cible. Il ne supprime jamais rien : aucune suppression
# recursive et forcee de fichiers. En portee globale il ne retire qu'un lien
# symbolique qu'il a lui-meme pose, jamais un dossier reel.
set -euo pipefail

usage() {
  echo "Usage : scripts/install.sh <claude|cursor|codex> [chemin-projet]" >&2
  echo "        scripts/install.sh <claude|cursor|codex> --global [--copy]" >&2
  echo "  claude : copie vers .claude/skills et .claude/agents" >&2
  echo "  cursor : copie vers .cursor/skills et .cursor/agents" >&2
  echo "  codex  : copie vers .agents/skills (pas de sous-agents Codex)" >&2
  echo "  --global : installe dans la configuration personnelle de l'hote" >&2
  echo "             (~/.claude, ~/.cursor, ~/.agents) par lien symbolique." >&2
  echo "  --copy   : avec --global, copie au lieu de lier." >&2
  echo "La portee projet reste le defaut et le mode recommande." >&2
}

global_scope=0
link_mode=1
positional=()

for arg in "$@"; do
  case "$arg" in
    --global) global_scope=1 ;;
    --copy) link_mode=0 ;;
    -h|--help) usage; exit 0 ;;
    -*)
      echo "Option inconnue : ${arg}" >&2
      usage
      exit 1
      ;;
    *) positional+=("$arg") ;;
  esac
done

if [ "${#positional[@]}" -lt 1 ] || [ "${#positional[@]}" -gt 2 ]; then
  usage
  exit 1
fi

host="${positional[0]}"

if [ "$global_scope" -eq 0 ] && [ "$link_mode" -eq 0 ]; then
  echo "--copy n'a de sens qu'avec --global : la portee projet copie deja." >&2
  usage
  exit 1
fi

if [ "$global_scope" -eq 1 ] && [ "${#positional[@]}" -eq 2 ]; then
  echo "--global n'accepte pas de chemin de projet : la cible est votre dossier personnel." >&2
  usage
  exit 1
fi

target="."
if [ "${#positional[@]}" -eq 2 ]; then
  target="${positional[1]}"
fi

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
    echo "Hôte inconnu : ${host}" >&2
    usage
    exit 1
    ;;
esac

if [ "$global_scope" -eq 1 ]; then
  case "$host" in
    claude)
      global_skills="${HOME}/.claude/skills"
      global_agents="${HOME}/.claude/agents"
      ;;
    cursor)
      global_skills="${HOME}/.cursor/skills"
      global_agents="${HOME}/.cursor/agents"
      ;;
    codex)
      global_skills="${HOME}/.agents/skills"
      global_agents=""
      ;;
  esac

  conflicts=()

  # Pose un dossier AZDone a destination, sans jamais supprimer de contenu
  # reel : seul un lien symbolique deja pose par ce script est remplace.
  place_entry() {
    src="$1"
    dest="$2"

    if [ -L "$dest" ]; then
      current="$(readlink "$dest")"
      case "$current" in
        "${repo_root}"/*)
          rm "$dest"
          ;;
        *)
          conflicts+=("${dest} : lien existant vers ${current}")
          return 0
          ;;
      esac
    elif [ -e "$dest" ] && [ "$link_mode" -eq 1 ]; then
      conflicts+=("${dest} : dossier reel existant, non pose par ce script")
      return 0
    fi

    if [ "$link_mode" -eq 1 ]; then
      ln -s "$src" "$dest"
    elif [ -d "$src" ]; then
      mkdir -p "$dest"
      cp -R "${src}/." "${dest}/"
    else
      # Les cartes de sous-agents sont des fichiers, pas des dossiers.
      cp "$src" "$dest"
    fi
  }

  mkdir -p "$global_skills"

  global_skill_count=0
  for skill_path in "${repo_root}/skills"/*; do
    [ -d "$skill_path" ] || continue
    name="$(basename "$skill_path")"
    case "$name" in
      *-azd|azd|azd-setup)
        place_entry "$skill_path" "${global_skills}/${name}"
        global_skill_count=$((global_skill_count + 1))
        ;;
    esac
  done

  if [ "$link_mode" -eq 1 ]; then
    echo "Skills AZDone lies : ${global_skill_count} -> ${global_skills}"
  else
    echo "Skills AZDone copies : ${global_skill_count} -> ${global_skills}"
  fi

  if [ -n "$global_agents" ] && [ -d "${repo_root}/agents" ]; then
    mkdir -p "$global_agents"
    global_agent_count=0
    for agent_file in "${repo_root}/agents"/*.md; do
      [ -f "$agent_file" ] || continue
      place_entry "$agent_file" "${global_agents}/$(basename "$agent_file")"
      global_agent_count=$((global_agent_count + 1))
    done
    echo "Sous-agents AZDone poses : ${global_agent_count} -> ${global_agents}"
  fi

  if [ "${#conflicts[@]}" -gt 0 ]; then
    echo "" >&2
    echo "Rien n'a ete supprime. Chemins laisses intacts :" >&2
    for entry in "${conflicts[@]}"; do
      echo "  - ${entry}" >&2
    done
    echo "Retirez-les vous-meme, puis relancez." >&2
    exit 1
  fi

  echo ""
  if [ "$link_mode" -eq 1 ]; then
    echo "Liens symboliques : un git pull dans ${repo_root} met a jour tous vos projets."
    echo "Contrepartie : un git checkout dans ce clone les change aussi, sans avertissement."
    echo "Utilisez --global --copy pour figer une version."
  fi
  echo "Le hook de confiance n'est pas installe en portee globale : il lit le"
  echo ".azdone/trust.yaml du projet et se branche dans les reglages du projet."
  echo ""
  if [ "$host" = "codex" ]; then
    echo "Confirmez que Codex lit bien ${global_skills} : lancez Codex hors de tout"
    echo "depot AZDone et verifiez que azd apparait dans /skills. La documentation"
    echo "OpenAI ne source que la portee repo-locale (.agents/skills)."
    echo "Lancez ensuite \$azd-setup dans un projet."
  else
    echo "Lancez /azd-setup dans un projet."
  fi
  exit 0
fi

if [ ! -d "$target" ]; then
  echo "Chemin de projet introuvable : ${target}" >&2
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
      # Dossier hors convention AZDone : jamais copié.
      ;;
  esac
done

echo "Skills AZDone copiés : ${copied_skills} -> ${target}/${skills_dir}"

if [ -n "$agents_dir" ] && [ -d "${repo_root}/agents" ]; then
  mkdir -p "${target}/${agents_dir}"
  agent_count=0
  for agent_file in "${repo_root}/agents"/*.md; do
    [ -f "$agent_file" ] || continue
    cp "$agent_file" "${target}/${agents_dir}/"
    agent_count=$((agent_count + 1))
  done
  echo "Sous-agents AZDone copiés : ${agent_count} -> ${target}/${agents_dir}"
elif [ "$host" != "codex" ]; then
  echo "Aucun dossier agents/ trouvé dans le dépôt AZDone (rien copié)."
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

# Copie du hook de confiance (jamais requis, jamais enregistré automatiquement :
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
    echo "Hook de confiance copié (non enregistré) -> ${hook_dir}/azd-trust-guard.sh"
  fi

  if [ "$host" = "claude" ]; then
    echo ""
    echo "Pour l'enregistrer, ajoutez ce bloc à ${target}/.claude/settings.json (fusionner, ne pas écraser) :"
    echo '  {"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/azdone/azd-trust-guard.sh\""}]}]}}'
    echo "Ce script ne modifie jamais settings.json lui-même."
  else
    echo ""
    echo "Pour l'enregistrer, ajoutez ce bloc à ${target}/.cursor/hooks.json (fusionner, ne pas écraser) :"
    echo '  {"version":1,"hooks":{"beforeShellExecution":[{"command":"bash \"./.cursor/hooks/azdone/azd-trust-guard.sh\""}]}}'
    echo "Chemin relatif utilisé volontairement : VERIFIED_FORMATS.md ne confirme pas la variable CURSOR_PROJECT_DIR pour un hooks.json de projet (hors plugin)."
    echo "Ce script ne modifie jamais hooks.json lui-même."
  fi
fi

if [ "$host" = "codex" ]; then
  echo ""
  echo "Codex : aucun mode enforced. La confiance y reste 'declared' seulement, aucun hook ne s'y exécute."

  if [ -f "${repo_root}/hooks/azd-trust-guard.py" ]; then
    codex_hook_dir="${target}/.agents/azdone"
    mkdir -p "${codex_hook_dir}"
    cp "${repo_root}/hooks/azd-trust-guard.py" "${codex_hook_dir}/azd-trust-guard.py"
    chmod +x "${codex_hook_dir}/azd-trust-guard.py"
    echo ""
    echo "azd-trust-guard.py copié (sans hook, Codex n'en exécute aucun) -> ${codex_hook_dir}/azd-trust-guard.py"
    echo "Il reste utilisable directement en ligne de commande pour 'record' (promotion/rétrogradation d'autonomy:) et 'witness' (écriture du témoin .azdone/conditions-ok), sans dépendre d'un hook."
  fi
fi
