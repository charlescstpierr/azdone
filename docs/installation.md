# Installer, mettre à jour et retirer AZDone

AZDone est distribué comme dossiers Agent Skills. L’installation consiste à
copier `skills/*` dans l’emplacement de skills reconnu par l’hôte.

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

## Vérifier l’installation

Le dépôt cible doit contenir 16 dossiers AZDone :

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type d -name '*-azd' | wc -l
```

Puis :

1. ouvrez `/skills`;
2. invoquez `$initialiser-projet-azd`;
3. vérifiez la présence d’un statut explicite;
4. invoquez à nouveau l’init et exigez `already-initialized`.

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

Avant toute suppression, vérifiez que le dossier ne contient que les 16 skills
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

## Limites de la distribution actuelle

- Pas d’installateur automatisé.
- Pas de gestionnaire de version AZDone.
- Pas de Doctor public.
- Pas de migration automatique.
- Pas de preuve Pilot 0 sur environnement propre.
- Pas de licence de réutilisation sélectionnée à ce stade.

