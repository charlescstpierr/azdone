# Installer AZDone

AZDone reste des dossiers de skills et des sous-agents ordinaires. Il n'y a
rien à démarrer, rien à héberger. Trois voies existent : le script
d'installation, la copie manuelle, ou le plugin pour Claude Code et Cursor.

## Avec le script

Depuis un clone d'AZDone, à côté de votre projet :

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
../azdone/scripts/install.sh claude .
```

Remplacez `claude` par `cursor` ou `codex` selon votre hôte. Le script copie
uniquement les dossiers `*-azd`, `azd` et `azd-setup` vers `.claude/skills`,
`.cursor/skills` ou `.agents/skills`, et les sous-agents `agents/*.md` vers
`.claude/agents` ou `.cursor/agents` (Codex n'a pas de sous-agents dédiés). Il
est idempotent : relancez-le après une mise à jour sans crainte pour le reste
du projet.

## Avec le plugin (Claude Code, Cursor)

```bash
claude plugin marketplace add charlescstpierr/azdone
claude plugin install azdone@azdone
```

Cette voie namespace les commandes : `/azdone:azd`, `/azdone:azd-setup`. La
copie via `scripts/install.sh` donne les formes courtes `/azd` et
`/azd-setup`. Les deux formes appellent le même skill.

Pour Cursor, le plugin `.cursor-plugin/plugin.json` déclare les mêmes skills
et sous-agents ; suivez le flux d'installation de plugin de votre version de
Cursor.

## Vérifier l'installation

```bash
find .agents/skills .claude/skills .cursor/skills -mindepth 1 -maxdepth 1 -type d \
  \( -name '*-azd' -o -name 'azd' -o -name 'azd-setup' \) 2>/dev/null | wc -l
```

Vous devez compter 19 dossiers au total dans l'emplacement que vous avez
choisi : les 17 skills existants, plus `azd` et `azd-setup`.

## Enregistrer le hook de confiance (optionnel)

Sur `claude` et `cursor`, le script copie aussi `hooks/azd-trust-guard.sh`
dans `.claude/hooks/azdone/` ou `.cursor/hooks/azdone/`, puis affiche le bloc
JSON à ajouter vous-même dans `.claude/settings.json` ou `.cursor/hooks.json`.
Il ne modifie jamais ce fichier de réglages : voir
[Comprendre la confiance](03-confiance.md).

## Premier lancement

```text
/azd-setup
```

`/azd-setup` détecte l'hôte, propose un niveau de confiance, un budget de
modèles, et écrit `.azdone/trust.yaml`. Il ne l'écrase jamais silencieusement :
un fichier existant est relu et confirmé avant toute modification.

Suivant : [Router avec `/azd`](02-azd.md).
