---
name: planifier-travail-azd
description: "Planifier le travail en convertissant un résultat approuvé en cartes progressives, Project Decision Graph, DAG de phases, contrats de preuve, responsabilités et ordre causal. Utiliser avant l'exécution quand dépendances, readiness, propriétaires, chevauchements, reprise, rollback ou contrats DevEx doivent être verrouillés."
---

# Étape 06 · Planifier le travail

Transformer le résultat accepté en ordre exécutable et vérifiable.

Wayfinder (navigation d'un grand projet : destination, brouillard, frontière) est domain-agnostic: ne jamais faire de CLI/API/SDK la surface par défaut. Appliquer le plan à produit, backend, infra, data, mobile, desktop, web, CLI, librairie, docs, migration et incident.

## Quick start

```text
$planifier-travail-azd "Planifie les tâches pour corriger l'onboarding accessible et vérifier web + CLI"
```

Artefact attendu: `plan.verdict`, carte active, états et liens du graphe, DAG de phases, `requirement_to_proof`, Proof Contract verrouillé, Readiness Forecast frais, ownership et contrat DevEx seulement si pertinent.

## Utiliser quand

- plusieurs étapes, owners ou preuves dépendent les uns des autres;
- le projet est assez large pour nécessiter destination, fog/frontier, décisions persistées, tickets ou reprise;
- une CLI, API ou SDK existe dans le scope et exige alors un contrat DevEx précis avant exécution;
- l'overlap doit être détecté avant le parallèle, ou l'intégration/le rollback doit être prévu avant les edits.

## Procédure

1. Partir de la Boussole (cadrage : utilisateur, problème, succès, limites), du Language Pack (termes utiles à la carte active), de la System Success Map, du contrat de résultat, des ADR et des preuves fraîches, et maintenir le Project Decision Graph (nœuds typés, liens causaux, evidence, confiance, invalidation, impact descendant) sans créer de second graphe concurrent.
2. Utiliser les cartes progressives `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done` (avec `Blocked`, `Needs Revalidation`, `Rejected`, `Superseded`), en grillant chaque carte juste avant sa frontière d'exécution, pas tout le backlog en profondeur.
3. Faire de toute découverte hors scope une carte `Draft` liée, et exposer pour toute décision matérielle recommandation, meilleure alternative, statu quo et trade-offs.
4. Pour grand projet, activer Wayfinder: destination, fog, frontier, decision ticket, cartes HITL/AFK, claims, blocking, reprise et tracker configuré par le setup; si le tracker configuré est indisponible, demander l'autorité avant de créer un tracker de secours repo-local. Voir [planning-contract.md](references/planning-contract.md).
5. Construire un DAG de phases avec gates cumulatifs et commits fonctionnels; paralléliser uniquement des nœuds réellement indépendants.
6. Pour CLI/API/SDK seulement si cette surface existe et change, écrire le contrat DevEx exact avant les tâches: commands, flags, stdout, stderr, exit codes, config precedence, idempotency et examples.
7. Construire la `requirement-to-proof map`, le verification overlay par surface, et verrouiller le Proof Contract avant `Ready`: claim, oracle indépendant, outil, environnement, données/accès, artefact, seuil, freshness et condition d'échec; puis appeler `$verifier-readiness-azd` pour chaque carte candidate à `Ready` (un gap matériel crée une carte prérequise).
8. Donner à chaque tâche action, `author_id`, `reviewer_id`, dépendances, repo-local paths, commandes exactes, write scope, test rouge, test vert, preuve/evidence, sortie et reprise: no vague steps.
9. Dimensionner le staffing par scope utile, risque, inconnues et indépendance, jamais par nombre brut de fichiers (Rapid: 0 par défaut, 1 max; Standard: 1 à 3 lanes; Critical: 2 à 5 lanes incluant un verifier indépendant), et porter un contexte frais minimal sans tout l'historique par défaut; déclencher `$structurer-code-azd` avant de figer les tâches quand ses conditions sont réunies.
10. Lire `discovery.active_work.overlap` avant d'ouvrir une lane, détecter l'overlap, sérialiser les écritures couplées, garder evaluator hors candidate write scope, et fixer ordering, intégration, recovery, resume checkpoints, rollback et plan `frozen`; toute nouvelle preuve matérielle invalide explicitement les nœuds concernés.

## Sortie

Le skill rend `plan` ([planning-output.md](references/planning-output.md)) avec les champs frozen, risk_level, active_card, project_decision_graph, phase_dag, wayfinder, devex_contract, dependency_graph, requirement_to_proof, proof_contracts, readiness_forecast, context_packet, staffing, resume_context, tasks, evaluator_scope, recovery, rollback, verdict.

## Arrêt et interdits

- Arrêter lorsque chaque exigence possède owner, dépendances, preuve et sortie.
- Interdire `Ready` si le Proof Contract ou le Readiness Forecast manque, est périmé ou laisse un moyen de preuve obligatoire impossible.
- Interdits: no vague steps, missing paths, missing commands, hidden dependency, ownership gap, same-worktree parallel writes, evaluator overlap ou parallèle sans overlap analysis.
- Fail closed si `author_id == reviewer_id` pour une tâche qui écrit.
- Fail closed si un contrat CLI/API/SDK manque stdout/stderr/exit codes/config precedence/idempotency alors que ces surfaces existent et changent.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
