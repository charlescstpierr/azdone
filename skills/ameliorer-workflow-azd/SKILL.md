---
name: ameliorer-workflow-azd
description: "Améliorer le workflow par une expérience longitudinale protégée avec worktrees isolés, baselines et évaluateurs gelés, séparation train/held-out/protected, détection de dérive, rollback et double review indépendante. Utiliser seulement lorsque des preuves répétées justifient une mutation contrôlée et une décision mesurable."
---

# Étape 14 · Améliorer le workflow

Teste une mutation de skill seulement quand des preuves repetees la justifient. Run controlled longitudinal evolution, not self-serving drift. This is a skill-only protocol: no runtime, daemon, database, scheduler, dependency, or hidden service is required or implied. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$ameliorer-workflow-azd "Teste si prouver-resultat-azd gagne en précision sur les évaluations protégées sans changer l'evaluator."`

Verdict attendu: falsifiable hypothesis, candidate branch, isolated worktree, frozen baseline/evaluator hashes, raw train/held-out/hidden oracle/protected regressions, deux reviews independantes, promotion observation window, drift check, rollback proof, decision `keep | discard | rollback | human-gate | insufficient-evidence | fail-closed`.

## Utiliser quand / Use when

Utilise ce skill seulement lorsqu'un signal répété, un benchmark confirmé ou une régression prouvent qu'une mutation contrôlée vaut le coût. Ne jamais l'activer automatiquement pendant un projet utilisateur; le futur builder de self-evolution reste différé.

## Procedure courte

1. Charge baseline acceptee, source runs et apprentissages gouvernes; freeze baseline snapshot, accepted behavior contract, evaluator, thresholds, prompts, fixtures and rollback bundle before any candidate edit.
2. Formule une `falsifiable hypothesis` unique: population cible, effet attendu, metriques, seuil minimal et rejet.
3. Arrete avec `insufficient-evidence` si l'idee vient d'une preference ponctuelle.
4. Cree une `candidate branch` dans un `isolated worktree` du same repository.
5. Lie `author_id`, `reviewer_id` et `second_reviewer_id` distincts; reviewers must be independent from author and from each other. Fail closed si l'auteur evalue, selectionne les cas, modifie l'evaluator, ou accepte sa candidate.
6. Limite les ecritures aux skills candidats; enregistre baseline commit.
7. Garde `frozen evaluator`, oracles, held-out set, protected regressions, reviewer briefs et promotion criteria outside_candidate_write_scope avec versions, paths et hashes.
8. Avant l'essai, separe strictement `train`, `held_out_eval`, `hidden_oracle` et `protected_regressions`; the candidate author may see train only. Held-out, hidden oracle and protected regressions remain read-restricted until scoring.
9. Ajoute des `forward-tests clean-room` pour tout nouveau skill ou comportement public: nominal, edge et rejet, hors write scope candidat.
10. Compare baseline et candidate sous conditions identiques: runtime, model, authority, budgets, seeds, snapshots and host evidence capture.
11. Mesure correctness et gates protegees before scoring/before comparing cost, latency, tokens, tool calls et interruptions.
12. Invalide toute evaluation `incomplete or interrupted`; persist a resume checkpoint and rerun the full frozen comparison from the last trusted checkpoint before considering promotion.
13. Traite evaluator edits, oracle access, skipped cases, selective reruns, threshold changes, prompt leakage, reviewer collusion ou proxy optimisation comme `reward hacking` et `discard`.
14. Exige deux reviews independantes avant promotion; un desaccord donne `human-gate` ou `discard`.
15. Promotion is provisional: after `keep`, run an explicit promotion observation window on fresh post-promotion runs, compare drift against baseline, and keep the rollback bundle ready until the window closes.
16. Si l'observation, drift detection, protected regressions, or promoted commit verification fail, `rollback` vers la derniere baseline and prove recovery with fresh evidence.
17. Toute preuve manquante, host evidence absente, author/reviewer identity conflict, modified frozen artifact, interrupted run without resume proof, or hidden-oracle exposure gives `fail-closed`.
18. Voir [evolve-details.md](references/evolve-details.md) pour les verdicts et anti-reward-hacking complets.

## Sortie / Output

```yaml
evolve:
  hypothesis: ""
  baseline_commit: ""
  baseline_snapshot:
    behavior_contract_hash: ""
    rollback_bundle: ""
    frozen_at: ""
  author_id: ""
  reviewer_id: ""
  second_reviewer_id: ""
  independence:
    author_reviewer_distinct: true
    reviewers_distinct: true
    reviewer_briefs_hash: ""
  candidate:
    branch: ""
    worktree: ""
    write_scope: []
  evaluator:
    path: ""
    hash: ""
    outside_candidate_write_scope: true
    thresholds_hash: ""
    prompts_hash: ""
  cohorts:
    train: {visible_to_author: true, cases: []}
    held_out_eval: {visible_to_author: false, cases: []}
    hidden_oracle: {visible_to_author: false, cases: []}
    protected_regressions: {visible_to_author: false, cases: []}
  forward_tests:
    clean_room: true
    outside_candidate_write_scope: true
    cases: []
  host_evidence:
    required: true
    agent_ids: []
    tool_calls: []
    worktrees: []
    artifacts: []
    transcripts: []
    execution_status: observed | partial | blocked | failed
  resume:
    interruption_safe: true
    checkpoint: ""
    resumed_from_checkpoint: false
    full_rerun_after_resume: false
  raw_results:
    train: []
    held_out_eval: []
    hidden_oracle: []
    protected_regressions: []
    forward_tests: []
  independent_reviews: []
  anti_reward_hacking:
    frozen_artifacts_unchanged: true
    no_oracle_access: true
    no_selective_reruns: true
    no_proxy_optimization: true
    no_reviewer_collusion: true
  deltas:
    correctness: ""
    quality: ""
    cost: ""
    latency: ""
    interruptions: ""
  promotion_observation_window:
    required_after_keep: true
    duration_or_runs: ""
    fresh_runs: []
    drift_detected: false
    protected_gates_passed: false
  rollback: {bundle: "", trigger: "", recovery_evidence: []}
  fail_closed_reason: ""
  verdict: keep | discard | rollback | human-gate | insufficient-evidence | fail-closed
```

A candidate cannot broaden its own authority policy and must not touch evaluators, reviewers, forward-tests, fixtures or promotion criteria.
