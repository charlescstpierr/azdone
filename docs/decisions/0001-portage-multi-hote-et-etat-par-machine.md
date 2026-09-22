# 0001. Portage multi-hôte : état par machine, sous-agents Codex, install global

- Statut : décidé, implémentation non commencée.
- Date : 2026-09-22.
- Surfaces visées : `scripts/install.sh`, `skills/azd-setup/SKILL.md`,
  `docs/guide/04-modeles-et-sous-agents.md`, `docs/installation.md`.
- Déclencheur : lecture du portage pstack vers Codex et Claude Code.

## Contexte

Le portage pstack résout quatre problèmes d'hôte qu'AZDone traite aujourd'hui
partiellement ou pas du tout :

1. installation globale des skills sous Codex (`~/.agents/skills/`), une fois
   pour toutes les machines plutôt qu'une fois par dépôt ;
2. sous-agents multi-modèles et parallèles sous Codex, derrière
   `multi_agent = true` dans `~/.codex/config.toml` ;
3. absence de déclenchement automatique sous Codex, compensée par un pointeur
   permanent dans `~/.codex/AGENTS.md` ;
4. mémorisation des modèles de l'hôte, écrite par `/setup-pstack` dans
   `~/.codex/pstack-models.md`.

Les quatre sont des trous réels pour AZDone. Le quatrième est le seul pour
lequel AZDone a déjà une réponse, et cette réponse est meilleure : il ne faut
donc pas copier le pattern pstack tel quel.

## État actuel d'AZDone, trou par trou

| Trou | État AZDone | Coût aujourd'hui |
| --- | --- | --- |
| Install global | `scripts/install.sh` copie uniquement en portée projet (`.claude/skills`, `.cursor/skills`, `.agents/skills`) | une copie par dépôt, mises à jour manuelles et divergentes |
| Sous-agents Codex | `docs/guide/04` : `host:<tier>` retombe sur `subagents-unavailable` sous Codex | le staffing par risque (2 à 5 sous-agents en `critical`) n'est atteignable sous Codex que par adaptateurs `cli:` |
| Déclenchement auto | `azd-setup` §12 pose un pointeur, Claude Code seulement | sous Codex l'humain doit se souvenir d'appeler `$azd` |
| Modèles détectés | `azd-setup` §6 et §7 sondent la machine à chaque projet | dix dépôts, dix probes identiques et dix fois la même question |

## Décision 1 : séparer les faits de machine des décisions de projet

`~/.codex/pstack-models.md` est un mémo en prose, global, lu par le modèle.
AZDone a déjà l'équivalent en plus strict : `.azdone/trust.yaml`, section
`models.roles`, YAML parsé, versionné, lu par `hooks/azd-trust-guard.py`.

Copier le mémo pstack casserait trois invariants posés par le projet :

- `README.md` promet que l'état du projet et de la confiance reste dans le
  dépôt utilisateur (`.azdone/`) ;
- le hook de confiance ne lit que `trust.yaml` : un markdown global serait
  suggéré à l'agent, jamais appliqué ;
- `azd-setup` §6 interdit d'écrire un slug de modèle non détecté, et un mémo
  en prose vieillit sans que rien ne le revalide.

Décision retenue : AZDone écrit un cache par machine qui ne contient **que
des faits sondés**, jamais une décision.

```json
{
  "schema": 1,
  "probed_at": "2026-09-22T14:03:11Z",
  "host": "codex",
  "host_version": "<sortie exacte de --version>",
  "adapters": {
    "codex": {"path": "/usr/local/bin/codex", "command_confirmed": true},
    "claude": {"path": "/opt/node22/bin/claude", "command_confirmed": true}
  },
  "models_probed_ok": ["gpt-5-codex"],
  "native_subagents": "unknown"
}
```

Emplacement : `~/.azdone/host-capabilities.json`, hôte-agnostique, un seul
fichier pour les trois hôtes.

Ce qui n'y entre **jamais** : `autonomy`, `ceiling`, `enforcement`,
`actions.*`, `models.roles`, `models.panels`, ni aucune préférence humaine.
Toute décision reste dans `.azdone/trust.yaml`, seul fichier versionné et
seul fichier que le hook lit.

Ce que `azd-setup` en fait :

1. lire le cache s'il existe, afficher son âge dans la question groupée
   « Modèle par rôle » ;
2. revalider le bon marché avant de proposer : présence sur le `PATH`. Un
   `--help` ou un `codex exec -m <slug>` en cache au-delà de 30 jours est
   resondé, jamais réutilisé tel quel ;
3. pré-remplir les propositions, sans jamais court-circuiter l'accord humain
   ni la règle §6 (aucun slug non détecté ou non confirmé n'entre dans
   `trust.yaml`) ;
4. écrire le cache après ses propres probes, et le dire dans la réponse.

Contraintes d'écriture : le cache est un fichier hors dépôt, donc son
écriture est annoncée explicitement, `docs/installation.md` documente son
chemin, et la désinstallation le retire. Un cache absent, illisible ou d'un
`schema` inconnu est ignoré en silence et resondé : il ne peut jamais faire
échouer `azd-setup`.

## Décision 2 : rien n'entre dans la doc sans probe réel

Les quatre faits pstack viennent d'une lecture, pas d'une mesure faite par ce
dépôt. `azd-setup` §6 et §7 et la note `VERIFIED_FORMATS` de
`scripts/install.sh` imposent la même discipline à AZDone qu'aux modèles
qu'il pilote. Aucun des quatre n'entre dans le guide ni dans le code avant
d'être prouvé sur une vraie session Codex.

| Fait à prouver | Protocole | Atterrit dans |
| --- | --- | --- |
| `~/.agents/skills/` est bien lu par Codex | y installer un skill témoin, lancer Codex, vérifier qu'il est listé | `install.sh --global codex`, `docs/installation.md` |
| Nom rendu d'un skill global | observer le token exact (`azdone:azd` ou `$azd`) | `docs/installation.md`, tokens publics de `CONTRIBUTING.md` |
| `multi_agent = true` donne des sous-agents natifs | poser le flag, lancer une tâche à deux sous-tâches, observer deux agents réels | `docs/guide/04`, mapping `host:<tier>` sous Codex |
| Précédence global contre projet | installer les deux, modifier un mot dans l'un, voir lequel est lu | `docs/installation.md`, `azd-setup` |

Le deuxième point est le plus coûteux s'il est ignoré : `CONTRIBUTING.md`
impose de conserver les tokens publics `<verbe>-<objet>-azd`. Si une install
globale sous Codex namespace les skills, la commande documentée `$azd` change
de forme et la doc ment.

Ces probes demandent le CLI `codex`, absent de l'environnement où cette note
est écrite. Ils appartiennent à la machine de l'humain.

## Décision 3 : l'install globale est une option, jamais le défaut

`scripts/install.sh` gagne un drapeau `--global`. La portée projet reste le
défaut.

Raison : modifier `~/` relève de l'action `install_global` de la table de
confiance, `ask` à tous les niveaux sauf `full`. Le script est lancé par un
humain dans un shell, donc l'appel explicite vaut accord ; mais **aucun skill
AZDone ne déclenche une install globale de lui-même**, à aucun niveau
d'autonomie.

Lien symbolique ou copie : le lien met à jour tous les projets d'un seul
`git pull` dans le clone AZDone, et fait aussi qu'un `git checkout` dans ce
clone change silencieusement les skills de tous les projets. Le drapeau
`--global` pose un lien, `--global --copy` force la copie, et
`docs/installation.md` énonce ce compromis. Les garanties actuelles du script
tiennent dans les deux cas : idempotent, jamais destructif, ne touche que les
dossiers `*-azd`, `azd` et `azd-setup`.

## Décision 4 : pointeur de projet d'abord, pointeur global sur demande

`azd-setup` §12 est étendu à Codex. L'ordre est strict :

1. fichier de contrôle du projet (`AGENTS.md` du dépôt) en premier ;
2. `~/.codex/AGENTS.md` seulement si l'humain le demande explicitement dans le
   tour courant, parce qu'un fichier de contrôle global influence tous ses
   projets, y compris ceux qui n'ont pas de `.azdone/`.

La règle existante tient : jamais de second fichier de contrôle, une ligne
pointeur ajoutée à celui qui existe.

## Alternatives rejetées

**Tout garder dans `.azdone/`.** Auditabilité parfaite, désinstallation
triviale. Rejetée : ne résout aucun des quatre trous, et committer « `codex`
est sur mon `PATH` » dans un dépôt partagé écrit un fait faux pour celui qui
clone. Ces faits sont de la machine, pas du projet.

**Copier `pstack-models.md` tel quel.** Le moins cher, zéro code. Rejetée :
casse les trois invariants de la décision 1, et ne couvre qu'un hôte sur
trois.

## Ce qui reste non prouvé

- Les quatre faits du tableau de la décision 2, tous.
- L'existence d'un mécanisme de réveil sous Codex : `docs/guide/04` le marque
  déjà « à vérifier », `multi_agent` ne le change pas tant qu'il n'est pas
  mesuré.
- Le comportement de `azd-setup` quand le cache décrit une machine dont les
  CLI ont été désinstallés depuis : couvert par la revalidation `PATH`, non
  encore testé.

## Prochaines actions

1. Exécuter les quatre probes de la décision 2 sur une machine avec Codex.
2. Selon leur résultat, ouvrir un changement par décision, avec son test de
   régression, plutôt qu'un seul gros changement.
3. Ne toucher à `docs/guide/04-modeles-et-sous-agents.md` qu'après le probe
   `multi_agent`.
