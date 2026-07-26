---
name: livrer-changement-azd
description: "Livrer un changement accepté en intégrant le travail, en prouvant le résultat combiné et en préparant checkpoint, handoff, notes de livraison et rollback. Utiliser pour intégrer des branches ou préparer ou exécuter un push, une pull request, un merge, un déploiement ou une conservation locale sous autorité explicite."
---

# Étape 11 · Livrer le changement

Integre et prepare une livraison sans perdre de travail. Ship only the verified integrated result. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$livrer-changement-azd "Integre les branches acceptees en dependency order et prepare une pull request sans merge."`

Verdict attendu: checkpoint, fresh verification sur l'`integrated result`, release notes, remaining risks, action `keep-local`, `open-pr`, `merge`, `deploy` ou `authority-request`.

## Utiliser quand / Use when

Utilise ce skill après `$prouver-resultat-azd` et `$reviser-qualite-azd` pour intégrer, documenter, préparer une livraison locale, ou exécuter une action externe déjà autorisée.

## Procedure courte

1. Charge exigences gelées, DAG et dependency order, Readiness Forecast, Functional Proof, Approval Readiness, verdicts de review et politique d'`explicit authority`.
2. Confirme que chaque candidat est accepte, rattache au bon base commit, et que `author_id != reviewer_id`.
3. Inventorie dirty state, worktrees, branches rejetees et artefacts recuperables; preserve tout travail utilisateur ambigu.
4. Cree ou valide un `checkpoint`: base commit, dirty-state inventory, diff attendu, artefacts, commandes passees/restantes et `resume_context` (`base_commit`, `branch`, `worktree`, `current_step`, `remaining_work`, `failed_approaches`, `resume_commands`, `next_safe_action`, `blockers`).
5. Integre avec operations Git reversibles; resous un conflit seulement si le comportement attendu est prouve.
6. Compare le diff final aux scopes acceptes; signale toute modification inattendue.
7. Lance une `fresh verification` sur le vrai `integrated result`, jamais seulement sur branches sources ou stale logs.
8. Rejoue les checks natifs pertinents: tests, protected suite, types, lint, build, migrations, smoke et visuel si applicable.
9. Produis un `context handoff` autonome avec etat, commandes, artefacts, risques, prochaine transition, rollback conditions et le dernier `handoff_carryover`; aucun champ requis ne peut être reconstruit silencieusement.
10. Prepare documentation utile, migration/rollback guidance, `release notes`, canary, monitoring et `remaining risks`.
11. Gate séparément `push`, `pull request`, `merge`, `submit-for-approval` et `deploy`; sans autorité, retourne `authority-request`.
12. Une soumission externe et son verdict sont des événements distincts. Ne jamais transformer `approval_readiness: ready` en `external_approval: approved`.
13. Voir [ship-details.md](references/ship-details.md) pour les règles complètes d'intégration, authority et rollback.

## Sortie / Output

```yaml
ship:
  author_id: ""
  reviewer_id: ""
  integrated_commit: ""
  progress_snapshot: {phase: ship, status: running | verified | partial | blocked | failed, done: 0, total: 0, blocked_by: [], last_checked_at: "", next_check: ""}
  checkpoint:
    base_commit: ""
    dirty_state_inventory: []
    expected_diff: []
    resume_commands: []
    recovery_plan: ""
  resume_context: {base_commit: "", branch: "", worktree: "", current_step: "", remaining_work: [], failed_approaches: [], resume_commands: [], next_safe_action: "", blockers: []}
  context_handoff:
    state: ""
    commands: []
    artifacts: []
    risks: []
    next_transition: ""
    rollback_conditions: []
    handoff_carryover: {from_skill: livrer-changement-azd, to_skill: "", required_fields: [], carried_fields: [], transformed_fields: [], dropped_fields: [], freshness_boundary: "", next_safe_action: ""}
  authority:
    push: false
    pull_request: false
    merge: false
    deploy: false
    submit_for_approval: false
  functional_proof: verified | partial | blocked | failed
  approval_readiness: ready | partial | blocked | not-applicable
  external_approval: not-requested | submitted | approved | rejected | blocked
  action: keep-local | open-pr | merge | discard-branch | deploy
  verification: []
  canary: []
  monitoring: []
  rollback: []
  verdict: verified | partial | blocked | failed | authority-request
```

Fail closed before integration when `author_id` and `reviewer_id` are missing or equal. Never convert `partial`, `blocked` or `failed` into delivered.
