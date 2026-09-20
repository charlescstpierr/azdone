# AZDone

AZDone est une couche d'entrée, `/azd`, posée sur **17 Agent Skills
ordinaires**. Elle route un objectif jusqu'à un résultat construit, prouvé,
révisé et livré, sous une politique de confiance déclarative que vous
contrôlez.

[English overview](README.en.md)

## Statut

**Aperçu public, skill-only.**

- Aucun runtime AZDone, daemon, dashboard ou service propriétaire.
- Aucun besoin d'OMX pour utiliser les skills.
- L'état du projet et de la confiance reste dans le dépôt utilisateur
  (`.azdone/`).
- Les 17 dossiers de skills passent les contrôles structurels et la suite de
  contrats locale.
- Le Pilot 0 sur un vrai projet humain n'a pas encore été exécuté.
- AZDone ne revendique ni supériorité générale ni approbation Apple, Google,
  Microsoft, OpenAI ou Anthropic.
- Le dépôt est public à des fins d'audit, mais **public ne signifie pas
  encore open source** : aucune licence de réutilisation n'est encore
  sélectionnée.

## Démarrage en 3 commandes

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
../azdone/scripts/install.sh claude .
```

```text
/azd-setup
```

```text
/azd l'export écrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Remplacez `claude` par `cursor` ou `codex` selon votre hôte. Sous Codex, les
commandes s'écrivent `$azd-setup` et `$azd`. Installé comme plugin Claude Code
ou Cursor depuis la marketplace du dépôt, les commandes sont namespacées :
`/azdone:azd-setup`, `/azdone:azd`. Le [guide
d'installation](docs/installation.md) couvre les trois hôtes et le plugin.

### Si vous ne retenez qu'une chose

Donnez à l'agent un objectif et une façon de vérifier, dans vos mots :

```text
/azd l'export écrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Vous n'avez pas besoin de nommer un playbook ni de lister des skills.
« Reproduis d'abord » et un résultat vérifiable suffisent comme signal de
routage.

## Ce qui se passe

```text
/azd "<objectif>"  →  lit trust.yaml, choisit un playbook  →  appelle les skills  →  verdict honnête
```

`/azd` classe la demande, copie les étapes du playbook choisi dans une liste
de tâches, applique la politique de confiance à chaque action sensible, puis
rend un verdict (`verified | partial | blocked | failed`) avec sa preuve et
sa `next_safe_action`. Détails dans le [guide](docs/guide/02-azd.md).

## Confiance

`.azdone/trust.yaml` fixe ce qu'un agent peut faire sans demander. Seul un
humain qui l'écrit ou l'approuve accorde cette autorité ; aucun texte de
skill ne le peut.

| Action | guided | assisted | autonomous | full |
| --- | --- | --- | --- | --- |
| lecture, checks natifs | auto | auto | auto | auto |
| écriture worktree isolé | ask | auto | auto | auto |
| écriture worktree principal (scope accepté) | ask | auto | auto | auto |
| commit | ask | auto | auto | auto |
| push, open_pr | ask | ask | auto | auto |
| merge | ask | ask | conditional | auto |
| deploy | ask | ask | ask | conditional |
| install_global, external_message | ask | ask | ask | auto |
| spawn_agent | ask | ask | ask | auto |
| credentials, delete_data, rewrite_shared_history | never | never | never | never |

`never` = refusé, un humain l'exécute lui-même : aucun niveau, aucune phrase
de session ne rend ces actions `auto`. Une liste toujours-pause du fichier
reste elle aussi non contournable : force-push partagé, suppression de
données non fusionnées, mutation de production sans rollback prouvé, message
à un tiers, usage de credentials, élargissement de `trust.yaml` par l'agent
lui-même ; une entrée retirée est réappliquée par le skill et par le hook.

`merge` en `conditional` vérifie le témoin `.azdone/conditions-ok`, écrit par
la review finale, contre les `conditions:` du fichier (CI verte, review
indépendante, risque, fichiers, lanes). La promotion automatique d'`autonomy:`
passe uniquement par `python3 hooks/azd-trust-guard.py record`, seule écriture
de `trust.yaml` permise à l'agent. Les phrases de session (« sois autonome »,
etc.) ne comptent que dans un message humain direct du tour courant et
n'élargissent que `commit`, `push`, `open_pr` et `merge`. Sous Cursor, le hook
n'intercepte pas les éditions de fichiers natives : seules les commandes
shell passent par lui.

La confiance gagnée est active par défaut : cinq runs `verified` consécutifs
sans rollback font monter d'un cran jusqu'au plafond `ceiling`, journalisé
dans `.azdone/trust-ledger.md`. `enforcement: declared` guide l'agent sans
vérification externe (seul mode sous Codex). `enforcement: enforced`, sous
Claude Code et Cursor, ajoute un hook (`hooks/azd-trust-guard.sh`) qui bloque
les commandes shell que la politique refuse. Détails dans le [guide de la
confiance](docs/guide/03-confiance.md).

## Modèles et sous-agents

Cinq rôles : `scout`, `builder`, `verifier`, `reviewer`, `watcher`. Chaque
rôle pointe vers `host:small|default|strong` (sous-agent natif de l'hôte) ou
`cli:codex|claude|cursor` (adaptateur externe confirmé sur le PATH). Le
relecteur reste indépendant de l'auteur. Détails dans le [guide des modèles
et sous-agents](docs/guide/04-modeles-et-sous-agents.md).

## Les 17 skills

Chaque skill reste invocable seul, sans passer par `/azd`. Voir la
[référence des 17 skills](docs/reference-skills.md).

## Documentation

- [Le guide AZDone](docs/guide/README.md)
- [Installation, mise à jour et désinstallation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Référence des skills](docs/reference-skills.md)
- [Validation et limites des preuves](docs/validation.md)
- [Contrats publics](CONTRACTS.md)
- [Fonctionnement détaillé](HOW_IT_WORKS.md)
- [Contribuer](CONTRIBUTING.md)
- [Sécurité](SECURITY.md)
- [Support](SUPPORT.md)
- [Historique des versions](CHANGELOG.md)

## Vérifier le package

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

La suite publique vérifie les noms, déclencheurs, contrats, garde-fous,
références, l'empaquetage des manifestes et l'absence de runtime dans les
skills. Elle ne prouve pas à elle seule le comportement d'un agent sur un
projet réel.

## Licence

Aucune licence de réutilisation n'est encore sélectionnée. Le dépôt public est
un aperçu auditable, mais **public ne signifie pas encore open source**. Le choix
MIT, Apache-2.0 ou autre doit être fait explicitement avant une version stable.
