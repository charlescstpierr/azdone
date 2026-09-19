# Installer AZDone

AZDone reste des dossiers de skills et des sous-agents ordinaires. Il n'y a
rien a demarrer, rien a heberger. Trois voies existent : le script
d'installation, la copie manuelle, ou le plugin pour Claude Code et Cursor.

## Avec le script

Depuis un clone d'AZDone, a cote de votre projet :

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
../azdone/scripts/install.sh claude .
```

Remplacez `claude` par `cursor` ou `codex` selon votre hote. Le script copie
uniquement les dossiers `*-azd`, `azd` et `azd-setup` vers `.claude/skills`,
`.cursor/skills` ou `.agents/skills`, et les sous-agents `agents/*.md` vers
`.claude/agents` ou `.cursor/agents` (Codex n'a pas de sous-agents dedies). Il
est idempotent : relancez-le apres une mise a jour sans crainte pour le reste
du projet.

## Avec le plugin (Claude Code, Cursor)

```bash
claude plugin marketplace add charlescstpierr/azdone
claude plugin install azdone@azdone
```

Cette voie namespace les commandes : `/azdone:azd`, `/azdone:azd-setup`. La
copie via `scripts/install.sh` donne les formes courtes `/azd` et
`/azd-setup`. Les deux formes appellent le meme skill.

Pour Cursor, le plugin `.cursor-plugin/plugin.json` declare les memes skills
et sous-agents ; suivez le flux d'installation de plugin de votre version de
Cursor.

## Verifier l'installation

```bash
find .agents/skills .claude/skills .cursor/skills -mindepth 1 -maxdepth 1 -type d \
  \( -name '*-azd' -o -name 'azd' -o -name 'azd-setup' \) 2>/dev/null | wc -l
```

Vous devez compter 18 dossiers au total dans l'emplacement que vous avez
choisi : les 16 skills existants, plus `azd` et `azd-setup`.

## Premier lancement

```text
/azd-setup
```

`/azd-setup` detecte l'hote, propose un niveau de confiance, un budget de
modeles, et ecrit `.azdone/trust.yaml`. Il ne l'ecrase jamais silencieusement :
un fichier existant est relu et confirme avant toute modification.

Suivant : [Router avec `/azd`](02-azd.md).
