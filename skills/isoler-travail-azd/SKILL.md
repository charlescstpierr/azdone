---
name: isoler-travail-azd
description: "Isoler le travail dans des branches ou worktrees du même dépôt avec responsabilités, checkpoints, évaluateur gelé et intégration sûre. Utiliser lorsque des hypothèses concurrentes, des sous-agents réellement observables, une vérification adversariale, une reprise ou plusieurs tranches indépendantes justifient des lanes séparées."
---

# Étape 07 · Isoler le travail

Isoler le travail concurrent dans le same repository sans contamination.

## Quick start

```text
$isoler-travail-azd "Compare deux correctifs indépendants de cache dans des worktrees séparés"
```

Artefact attendu: `branch_lab.decision`, lanes avec `agent_id`, `execution_status`, `artifacts`, leases/checkpoints, et preuve du frozen evaluator.

## Utiliser quand

- des hypothèses concurrentes, tranches indépendantes ou reviews adversariales justifient plusieurs branches/worktrees;
- des subagent briefs et ownership séparés accélèrent réellement le résultat;
- une pause/reprise exige leases and checkpoints.

## Procédure

1. Lire `risk_level`, DAG, overlap map et Readiness Forecast; ne créer aucune lane si le travail séquentiel est plus rapide ou plus sûr.
2. Appliquer les bornes adaptatives: Rapid `0` par défaut et `1` maximum; Standard `1-3`; Critical `2-5` incluant une vérification indépendante. Le nombre de fichiers n'est jamais un critère suffisant.
3. Donner à chaque lane indépendante une hypothèse, un `author_id`, un `reviewer_id`, un base commit, une branch, un worktree repo-local du même dépôt, un write scope et une condition de sortie.
4. Exécuter `isolation_preflight` (`existing_isolation`, `submodule_guard`, `native_tool_used`, `directory_ignored`, `baseline_ready`), puis vérifier l'overlap avant les edits et sérialiser les scopes couplés.
5. Écrire un brief frais et minimal par lane: carte, Boussole (cadrage : utilisateur, problème, succès, limites) pertinente, Language Pack (termes utiles à la carte active), ADR touchés, Proof Contract, Readiness Forecast, paths, condition de sortie. Ne pas copier toute la conversation.
6. Quand le host expose des subagents natifs et que les tâches sont réellement indépendantes, lancer un agent frais par tâche pertinente et enregistrer `agent_id`, rôle, scope, `cwd`, worktree, commit/base commit, tool evidence, statut final et artefacts. Ne jamais présenter un plan de délégation comme une exécution observée.
7. Si les subagents natifs sont indisponibles, rester sériel ou retourner `subagents-unavailable`; ne jamais simuler des événements ou identités.
8. Utiliser native Git et les outils du host; no shared worktree. Enregistrer leases et checkpoints avant pause, resume ou handoff avec `resume_context`.
9. Appliquer la `dirty-worktree safety`: préserver les changements utilisateur et refuser tout cleanup ambigu.
10. Comparer chaque lane avec le même `frozen evaluator`, puis faire une `safe integration` du candidat retenu et revérifier le résultat combiné.

## Sortie

Le skill rend `branch_lab` ([isolation-output.md](references/isolation-output.md)) avec les champs risk_level, staffing_reason, isolation_preflight, resume_context, lanes, evaluator, decision.

## Arrêt et interdits

- Arrêter lorsque chaque lane a une sortie et que le résultat intégré a une evidence fraîche.
- Interdits: shared worktree, hidden owner, reviewer same as author, evaluator drift, unsafe cleanup, faux événement de subagent ou écriture hors scope.
- Interdits: fan-out fondé sur le nombre de fichiers, lane dépendante déguisée en parallèle, historique complet injecté sans nécessité.
- Fail closed si deux lanes écrivent le même chemin ou si un worktree n'appartient pas au même repository.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
