# Installer, mettre à jour et retirer AZDone

AZDone est distribué comme dossiers Agent Skills, plus une couche d’entrée
`/azd` et `/azd-setup`. L’installation consiste à copier `skills/*` et
`agents/*` dans l’emplacement reconnu par l’hôte, ou à passer par
`scripts/install.sh` ou par le plugin. Trois hôtes sont couverts : Codex,
Claude Code et Cursor.

## Avec `scripts/install.sh`

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
../azdone/scripts/install.sh claude .
```

Remplacez `claude` par `cursor` ou `codex`. Le script copie uniquement les
dossiers `*-azd`, `azd` et `azd-setup`, jamais un autre fichier du dépôt
cible, et copie les sous-agents `agents/*.md` vers `.claude/agents` ou
`.cursor/agents` (Codex n’a pas de sous-agents dédiés). Il est idempotent et
ne supprime jamais rien.

## Portée globale, en option

La portée projet reste le défaut et le mode recommandé. Si vous voulez les
skills dans tous vos projets sans les copier un par un :

```bash
../azdone/scripts/install.sh claude --global
```

Cibles : `~/.claude/skills` et `~/.claude/agents`, `~/.cursor/skills` et
`~/.cursor/agents`, `~/.agents/skills` pour Codex. Par défaut le script pose
des liens symboliques vers votre clone AZDone ; `--global --copy` copie à la
place.

Le compromis à connaître : avec des liens, un `git pull` dans le clone met à
jour tous vos projets d’un coup, et un `git checkout` dans ce même clone les
change aussi, sans avertissement. `--copy` fige une version.

Le script ne supprime jamais un dossier réel. S’il trouve à destination un
dossier existant, ou un lien qui pointe ailleurs que vers votre clone, il
laisse tout en place, liste les chemins concernés et sort en erreur. Seul un
lien qu’il a lui-même posé est remplacé.

Le hook de confiance n’est pas installé en portée globale : il lit le
`.azdone/trust.yaml` du projet et se branche dans les réglages du projet.

Pour Codex, la portée globale n’est pas sourcée par la documentation OpenAI,
qui ne décrit que `.agents/skills` en repo-local. Le script vous le dit et
vous demande de confirmer vous-même que Codex lit bien `~/.agents/skills`,
en le lançant hors de tout dépôt AZDone et en vérifiant `/skills`.

## Avec le plugin Claude Code ou Cursor

```bash
claude plugin marketplace add charlescstpierr/azdone
claude plugin install azdone@azdone
```

Le dépôt contient `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
et `.cursor-plugin/plugin.json`. L’installation par plugin namespace les
commandes : `/azdone:azd`, `/azdone:azd-setup`. La copie manuelle ou par
script donne les formes courtes `/azd`, `/azd-setup` (`$azd`, `$azd-setup`
sous Codex).

## Codex : installation repo-locale recommandée

La documentation OpenAI indique que Codex scanne `.agents/skills` depuis le
répertoire courant jusqu’à la racine du dépôt.

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
mkdir -p .agents/skills
cp -R ../azdone/skills/. .agents/skills/
```

Redémarrez Codex si nécessaire, puis utilisez `/skills`.

Pourquoi repo-local :

- l’équipe voit la même version;
- le comportement est versionné avec le projet;
- une mise à jour peut être révisée comme un diff;
- l’état décisionnel reste dans le projet et non dans l’installation globale.

Ces quatre raisons tiennent toujours : la portée globale décrite plus haut est
une commodité pour vos propres projets, pas le mode recommandé en équipe.

Source officielle :
[OpenAI — Build skills](https://developers.openai.com/codex/skills).

## Claude Code : emplacement compatible

Claude Code documente les skills de projet dans `.claude/skills`.

```bash
cd votre-projet
mkdir -p .claude/skills
cp -R ../azdone/skills/. .claude/skills/
```

Source officielle :
[Anthropic — Extend Claude with skills](https://code.claude.com/docs/en/skills).

Le format de base est compatible, mais le parcours AZDone complet n’a pas
encore reçu de Pilot 0 sur Claude Code. Ne transformez pas la reconnaissance des
skills en preuve d’équivalence comportementale.

## Cursor : emplacement compatible

Cursor lit les skills de projet dans `.cursor/skills` (auto-découverte sans
manifeste) ou via `.cursor-plugin/plugin.json` pour une installation en
plugin.

```bash
cd votre-projet
mkdir -p .cursor/skills
cp -R ../azdone/skills/. .cursor/skills/
```

Même limite qu’avec Claude Code : le format est compatible, le Pilot 0 sur
Cursor n’a pas été exécuté.

## Vérifier l’installation

Le dépôt cible doit contenir 18 dossiers de skills existants, plus `azd` et
`azd-setup`, soit 20 dossiers au total :

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type d \
  \( -name '*-azd' -o -name 'azd' -o -name 'azd-setup' \) | wc -l
```

Puis :

1. ouvrez `/skills`;
2. invoquez `$initialiser-projet-azd`;
3. vérifiez la présence d’un statut explicite;
4. invoquez à nouveau l’init et exigez `already-initialized`.

## Si `/azd` n’apparaît pas

1. Redémarrez l’hôte (Claude Code, Cursor ou Codex) : la découverte des
   skills de projet se fait souvent au démarrage, une copie faite en cours
   de session peut ne pas être vue avant un redémarrage.
2. Vérifiez un conflit de nom : un skill ou une commande `azd` déjà présent
   ailleurs dans le projet (un autre plugin, un skill local) peut masquer
   celui d’AZDone. Listez `/skills` (ou l’équivalent de votre hôte) et
   cherchez un doublon avant de soupçonner l’installation.
3. Revérifiez le compte de dossiers ci-dessus : un total différent de 20
   signale une copie partielle plutôt qu’un problème de découverte.

## Mettre à jour

Mettez d’abord à jour le clone AZDone, puis comparez avant de copier :

```bash
cd ../azdone
git pull --ff-only
cd ../votre-projet
diff -ru .agents/skills ../azdone/skills
cp -R ../azdone/skills/. .agents/skills/
```

Révisez et commitez la mise à jour dans le dépôt cible. Une mise à jour des
skills ne doit pas réinitialiser silencieusement les conventions du projet.

## Retirer AZDone

Avant toute suppression, vérifiez que le dossier ne contient que les 18 skills
copiés. Retirez ensuite chaque dossier `*-azd` explicitement avec votre méthode
de suppression habituelle.

Ne supprimez pas automatiquement :

- les cartes;
- la Boussole;
- le langage partagé;
- les ADR;
- le Project Decision Graph;
- les preuves et checkpoints.

Ces artefacts appartiennent au projet. Décidez séparément de les archiver, les
migrer ou les supprimer.

Si vous aviez installé en portée globale, retirez aussi les dossiers ou liens
`azd`, `azd-setup` et `*-azd` de `~/.claude/skills`, `~/.cursor/skills` ou
`~/.agents/skills`, et les cartes `azd-*.md` de `~/.claude/agents` ou
`~/.cursor/agents`.

`azd-setup` garde par ailleurs un cache de capacités hors dépôt, décrit dans
[host-capabilities.md](../skills/azd-setup/references/host-capabilities.md) :

```bash
rm -f ~/.azdone/host-capabilities.json
rmdir ~/.azdone 2>/dev/null || true
```

Ce cache ne contient que des faits sondés sur votre machine (CLI présents,
slugs de modèles réellement confirmés). Aucune politique de confiance n’y
figure : elle vit dans le `.azdone/trust.yaml` de chaque projet. Le supprimer
ne coûte qu’un nouveau sondage au prochain `azd-setup`.

## Limites de la distribution actuelle

- Pas d’installateur automatisé.
- Pas de gestionnaire de version AZDone.
- Pas de Doctor public.
- Pas de migration automatique.
- Pas de preuve Pilot 0 sur environnement propre.
- Pas de licence de réutilisation sélectionnée à ce stade.
- `enforcement: enforced` du hook de confiance n’existe que sous Claude Code
  et Cursor ; Codex reste en politique déclarée seulement.
- La portée globale de `scripts/install.sh` n’est pas confirmée sous Codex :
  la documentation OpenAI ne source que `.agents/skills` en repo-local.
- `scripts/install.sh` copie `hooks/azd-trust-guard.sh` dans le projet cible
  et affiche le bloc `.claude/settings.json` ou `.cursor/hooks.json` à ajouter
  à la main ; il ne l’enregistre jamais lui-même.
- L’installation en plugin embarque tout le dépôt, y compris `tests/` et
  `docs/` (environ 1,3 Mo au total) : aucun mécanisme d’exclusion de fichiers
  n’est documenté pour les manifestes de plugin Claude Code ou Cursor. C’est
  jugé acceptable pour un aperçu public, pas optimisé pour la taille.

