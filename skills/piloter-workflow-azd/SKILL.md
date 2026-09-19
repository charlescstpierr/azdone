---
name: piloter-workflow-azd
description: "Piloter le parcours AZDone depuis un projet initialisé jusqu'à un résultat vérifié, livré et appris. Utiliser comme point d'entrée pour router clarification, inspection, diagnostic, design, planification, construction, preuve, review, livraison, surveillance et apprentissage selon le risque, les cartes actives, la readiness et l'autorité."
---

# Étape 01 · Piloter le workflow

Transformer un objectif naturel en résultat vérifié.

## Contract

Accepter `goal`, `repository` et une `authority policy` optionnelle; produire un compte rendu qui distingue `verified`, `partial`, `blocked` et `failed`, avec une evidence fraîche pour chaque affirmation. Lire [run-contract.md](references/run-contract.md) avant de commencer et le conserver pendant toute reprise (`resume`); renseigner `author_id`, `reviewer_id`, `base_commit`, `worktree` et les artefacts repo-locaux, fail closed si une identité, autorité ou preuve critique manque.

## Quick start

```text
$piloter-workflow-azd "Ajoute un onboarding accessible dans ce repo et prépare une PR vérifiée" repository=. authority="local edits only"
```

Artefact attendu: `run.status: verified | partial | blocked | failed`, route AZDone minimale, carte active, `readiness_forecast`, `decision_stack`, `progress_snapshot`, `handoff_carryover`, preuves fraîches et aucune affirmation sans preuve.

## Route

Choisir le plus petit parcours qui couvre réellement le besoin:

0. `$initialiser-projet-azd`: vérifier le setup ou initialiser une seule fois les conventions, pointeurs et amorces du projet.
1. `$clarifier-objectif-azd`: fixer le résultat, le risque et la prochaine décision matérielle.
2. `$inspecter-projet-azd`: inspecter dépôt, sources, mémoire optionnelle, opportunités et capacités manquantes.
3. `$diagnostiquer-probleme-azd`: reproduire et isoler la cause d'un bug, incident ou échec incertain.
4. `$concevoir-experience-azd`: produire un prototype ou design contract lorsqu'une décision humaine observable change.
5. `$planifier-travail-azd`: construire cartes, graphe causal, dépendances, preuve et ordre d'exécution.
6. `$isoler-travail-azd`: ouvrir seulement les lanes indépendantes que le risque et le scope justifient.
7. `$construire-solution-azd`: implémenter la plus petite solution valide.
8. `$prouver-resultat-azd`: séparer preuve fonctionnelle, readiness d'approbation et verdict externe.
9. `$reviser-qualite-azd`: lancer les reviews indépendantes nécessaires au niveau de risque.
10. `$livrer-changement-azd`: intégrer, documenter et préparer ou exécuter la livraison selon l'autorité.
11. `$surveiller-livraison-azd`: observer, détecter une régression et rollback si nécessaire.
12. `$conserver-apprentissages-azd`: proposer puis promouvoir uniquement les apprentissages reliés à des preuves.
13. `$ameliorer-workflow-azd`: tester une amélioration de skill dans une branche isolée sans reward hacking.

`$verifier-readiness-azd` est un socle transversal, pas une étape numérotée: l'appeler au bootstrap, après un changement matériel, avant `Ready`, avant exécution si le forecast est périmé et avant `Done`.

## Routing rules

- Vérifier d'abord l'initialisation: si aucune preuve de setup AZDone n'existe, appeler `$initialiser-projet-azd` une seule fois; si le setup existe mais qu'une Boussole, un langage partagé, une System Success Map, un graphe ou un preflight manque ou est périmé, ne jamais relancer l'init, mais créer une carte explicite de migration, de complétion ou de revalidation puis router vers le skill normal concerné et `$verifier-readiness-azd`.
- Commencer ensuite par `$clarifier-objectif-azd`; ne pas coder à partir d'une interprétation implicite.
- Classer le run `Rapid | Standard | Critical`. Rapid: aucun arbitrage par défaut et au plus une lane d'aide; Standard: une à trois lanes réellement indépendantes; Critical: deux à cinq lanes pertinentes, verifier indépendant et auteur incapable de s'auto-approuver.
- Utiliser les états `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done`; ajouter `Blocked`, `Needs Revalidation`, `Rejected` ou `Superseded` sans écraser l'historique.
- Garder une seule carte active et une seule question matérielle par round, en inspectant les faits et en présentant recommandation, meilleure alternative, statu quo et trade-offs avant de demander; toute découverte hors périmètre devient une carte `Draft` liée sans jamais élargir silencieusement la carte active.
- Maintenir une `Decision Stack` séparée de l'`Opportunity Inbox`: une idée externe n'interrompt que si elle change matériellement le risque, le coût, la réversibilité ou la valeur, puis reprendre exactement au checkpoint causal.
- Classer le besoin par capacités, pas par technologie: `code-change`, `investigation`, `human-surface`, `release-ops`, `skill-mutation`, ou une combinaison; utiliser cette classification pour omettre les couches sans effet sur le résultat.
- Router les domaines complexes vers le domain model léger de `$clarifier-objectif-azd`: vocabulaire, identités, entités, invariants, lifecycle, exemples et contre-exemples.
- Pour tout travail sur un dépôt, appeler ensuite `$inspecter-projet-azd` avant le diagnostic, le design, le plan ou le code, sauf si les preuves du dépôt ont déjà été fournies et sont encore fraîches; appeler `$diagnostiquer-probleme-azd` avant le plan lorsque la cause reste inconnue.
- Pendant une passe `$clarifier-objectif-azd`, poser au plus une question matérielle par round, arrêter tôt quand le contrat est assez sûr, et retourner `blocked` quand le zero-assumption gate ne permet pas d'avancer.
- Appeler `$concevoir-experience-azd` seulement lorsqu'une UI, CLI/TUI, app, IDE, chat, onboarding, rapport ou notification change une décision humaine observable. Pour une sortie textuelle stable sans décision de design, omettre cette étape et laisser `$prouver-resultat-azd` prouver le contrat.
- Pour CLI/API/SDK, demander à `$planifier-travail-azd` un contrat DevEx exact (commands, flags, stdout, stderr, exit codes, config precedence, idempotency) seulement quand cette surface existe.
- Pour un grand projet, demander à `$planifier-travail-azd` une destination, une decision map persistée, le fog/frontier, des decision tickets, claims, blocking et reprise avant l'execution plan; utiliser le mode Wayfinder seulement quand une carte de navigation apporte une valeur réelle.
- Après `$concevoir-experience-azd`, transmettre la `UI acceptance matrix` sans perte à la planification, construction, preuve et review, en conservant chaque token, selector ou attribut normatif.
- Après `$inspecter-projet-azd`, transmettre sans perte `discovery.contradictions`, `discovery.blind_spots` et les failure modes sourcés à la planification, construction, preuve et review.
- Utiliser `$isoler-travail-azd` seulement pour des hypothèses concurrentes, des tranches indépendantes ou une vérification adversariale; sinon rester séquentiel.
- Ne jamais faire travailler deux subagents dans le même worktree; toute lane parallèle appartient au same repository et à un worktree distinct.
- Garder le reviewer et tout evaluator hors du write scope de l'auteur: `author_id != reviewer_id`.
- Revenir à `$construire-solution-azd` après un échec de vérification ou de review puis refaire les gates concernées; après un échec de preuve, revenir à la première hypothèse invalidée (readiness, compréhension, diagnostic, design, plan ou build) sans renvoyer aveuglément au code.
- Ne pas appeler `$ameliorer-workflow-azd` après chaque run; exiger un signal répété ou pertinent pour le benchmark.
- Attribuer honnêtement les capacités: les skills prescrivent le parcours, le host compatible exécute outils, Git, subagents et lifecycle, le harness externe mesure seulement les cas qu'il observe.
- Doctor est hors workflow utilisateur: il sert au builder pour auditer un pilote après coup; ne jamais le router, l'installer ou l'invoquer ici.

Voir [run-contract.md](references/run-contract.md) pour les champs obligatoires, authority, safety, completion et statuts d'arrêt.

## Sortie

Le skill rend `run` ([run-contract.md](references/run-contract.md)) avec les champs `run.goal`, repository, base_commit, worktree, author_id, reviewer_id, risk_level, project_compass, active_card, decision_stack, opportunity_inbox, route, readiness_forecast, functional_proof, approval_readiness, `progress_snapshot: {phase, status, done, total, blocked_by, last_checked_at, next_check}`, handoff_carryover, artifacts, status, evidence, next_safe_action. Pour `partial` ou `blocked`, `next_safe_action` doit être fraîche, vérifiable et autorisée; pour `verified` ou `failed`, rendre `next_safe_action: none`.

## Arrêt et interdits

- Ne dire « terminé » que si chaque exigence possède une evidence actuelle et si aucun blocker connu ne reste; sinon rendre un verdict honnête, la dernière étape sûre, les preuves disponibles et `next_safe_action`.
- Ne pas coder avant d'avoir compris le résultat ni déclarer une hypothèse comme un fait.
- Ne pas paralléliser des écritures qui se chevauchent, partager un worktree ou écraser un changement utilisateur.
- Ne pas contourner les gates de design, sécurité, accessibility, review ou authority pour terminer plus vite.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
