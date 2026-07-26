---
name: isoler-travail-azd
description: "Isoler le travail dans des branches ou worktrees du même dépôt avec responsabilités, checkpoints, évaluateur gelé et intégration sûre. Utiliser lorsque des hypothèses concurrentes, des sous-agents réellement observables, une vérification adversariale, une reprise ou plusieurs tranches indépendantes justifient des lanes séparées."
---

# Étape 07 · Isoler le travail

Isoler le travail concurrent dans le same repository sans contamination. Isolate concurrent work in the same repository without cross-contamination.

## Quick start

```text
$isoler-travail-azd "Compare deux correctifs indépendants de cache dans des worktrees séparés"
```

Artefact attendu: `branch_lab.decision`, lanes avec `agent_id`, `execution_status`, `artifacts`, leases/checkpoints, et preuve du frozen evaluator.

## Utiliser quand / Use when

- des hypothèses concurrentes, tranches indépendantes ou reviews adversariales justifient plusieurs branches/worktrees;
- des subagent briefs et ownership séparés accélèrent réellement le résultat;
- une pause/reprise exige leases and checkpoints.

## Procédure / Procedure

1. Lire `risk_level`, DAG, overlap map et Readiness Forecast. Ne créer aucune lane si le travail séquentiel est plus rapide ou plus sûr.
2. Appliquer les bornes adaptatives: Rapid `0` par défaut et `1` maximum; Standard `1-3`; Critical `2-5` incluant une vérification indépendante. Le nombre de fichiers n'est jamais un critère suffisant.
3. Donner à chaque lane indépendante une hypothèse, un `author_id`, un `reviewer_id`, un base commit, une branch, un worktree repo-local du même dépôt, un write scope et une condition de sortie.
4. Exécuter `isolation_preflight`: `existing_isolation`, `submodule_guard`, `native_tool_used`, `directory_ignored`, `baseline_ready`.
5. Vérifier l'overlap avant les edits; sérialiser les scopes couplés.
6. Écrire un brief frais et minimal par lane: carte, Boussole pertinente, Language Pack, ADR touchés, Proof Contract, Readiness Forecast, paths, condition de sortie. Ne pas copier toute la conversation.
7. Quand le host expose des subagents natifs et que les tâches sont réellement indépendantes, lancer un agent frais par tâche pertinente. Enregistrer `agent_id`, rôle, scope, `cwd`, worktree, commit/base commit, tool evidence, statut final et artefacts. Ne jamais présenter un plan de délégation comme une exécution observée.
8. Si les subagents natifs sont indisponibles, rester sériel ou retourner `subagents-unavailable`; ne jamais simuler des événements ou identités.
9. Utiliser native Git et les outils du host; no shared worktree.
10. Enregistrer leases et checkpoints avant pause, resume ou handoff avec `resume_context`.
11. Appliquer la `dirty-worktree safety`: préserver les changements utilisateur et refuser tout cleanup ambigu.
12. Comparer chaque lane avec le même `frozen evaluator`.
13. Faire une `safe integration` du candidat retenu puis revérifier le résultat combiné.

## Sortie / Output

- lane ledger, subagent briefs et journal d'exécution observable (`agent_id`, `cwd`, worktree, commit provenance, tool evidence, statut, artefacts), ou preuve explicite d'indisponibilité;
- branches/worktrees, leases et checkpoints;
- comparaison, décision et rapport de safe integration;
- verdict `integrate`, `prepare`, `discard`, `preserve`, `blocked`, `subagents-unavailable` ou `authority-request`.

```yaml
branch_lab:
  risk_level: rapid | standard | critical
  staffing_reason: ""
  isolation_preflight:
    existing_isolation: ""
    submodule_guard: ""
    native_tool_used: ""
    directory_ignored: ""
    baseline_ready: false
  resume_context: {base_commit: "", branch: "", worktree: "", current_step: "", remaining_work: [], failed_approaches: [], resume_commands: [], next_safe_action: "", blockers: []}
  lanes:
    - id: ""
      author_id: ""
      reviewer_id: ""
      base_commit: ""
      branch: ""
      worktree: ""
      cwd: ""
      commit_provenance: ""
      write_scope: []
      brief_path: ""
      review_package_path: ""
      dispatch_scope: []
      expected_output: ""
      context_packet: {compass: "", card: "", language_pack: "", adrs: [], proof_contract: "", readiness_forecast: "", checkpoint: ""}
      exit: ""
      agent_id: ""
      tool_evidence: []
      execution_status: planned | running | completed | failed | unavailable
      artifacts: []
      checkpoint: ""
  evaluator:
    path: ""
    frozen: true
    outside_candidate_write_scope: true
  decision: integrate | prepare | discard | preserve | blocked | subagents-unavailable | authority-request
```

## Arrêt et interdits / Stop and forbidden

- Arrêter lorsque chaque lane a une sortie et que le résultat intégré a une evidence fraîche.
- No shared worktree, hidden owner, reviewer same as author, evaluator drift, unsafe cleanup, faux événement de subagent ou écriture hors scope.
- No fan-out fondé sur le nombre de fichiers, lane dépendante déguisée en parallèle ou historique complet injecté sans nécessité.
- Fail closed si deux lanes écrivent le même chemin ou si un worktree n'appartient pas au même repository.
- Garder les règles identiques en Français and English.
