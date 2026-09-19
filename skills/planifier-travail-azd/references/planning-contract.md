# Planning contract / Contrat de planification

## Wayfinder details

- Activer `wayfinder` pour grand projet: `destination`, `decision_map`, `fog`, `frontier`, `claims`, `blocking`, `resume` et tickets.
- Persister la decision map dans un tracker existant si disponible; sinon créer un tracker de secours repo-local tel que `WAYFINDER.md` ou `.omx/plans/wayfinder-*.md` quand autorisé.
- Créer des decision tickets `research`, `prototype`, `dialogue` ou `unblock` avec owner, paths, evidence, blocking condition et handoff.
- Basculer vers execution plan seulement quand fog/frontier/tickets bloquants permettent d'ordonner les tâches.

## DevEx details

Pour CLI/API/SDK seulement lorsque ces surfaces changent, figer avant exécution: commands, flags, positional args, stdin, stdout, stderr, exit codes, config precedence, environment, idempotency, compatibility et examples.

## Task details

- Chaque tâche contient action concrète, `author_id`, `reviewer_id`, dependencies, repo-local paths, commands exactes, write scope, exit condition, `red`, `green` et `proof`.
- Chaque tâche ou lane déclare `handoff_inputs`, `handoff_outputs` et les relie à `requirement_to_proof`; aucun risque, contradiction, oracle, finding ou rollback requis ne peut disparaître.
- `staffing` nomme `role`, `model_hint` optionnel, `reasoning_effort` optionnel et `expected_output` quand la tâche gagne à être déléguée; le host choisit le modèle réel. `role` doit correspondre à un rôle de `models.roles` de `.azdone/trust.yaml` (scout, builder, verifier, reviewer, second_reviewer, watcher); `model_hint`, s'il diffère du palier par défaut, doit être une valeur `host:` ou `cli:` valide selon `skills/azd/references/model-routing.md`.
- `resume_context` conserve `base_commit`, `branch`, `worktree`, `current_step`, `remaining_work`, `failed_approaches`, `resume_commands`, `next_safe_action` et `blockers`.
- Détecter l'overlap; sérialiser les écritures couplées.
- Fixer ordering, intégration, recovery, resume checkpoints, rollback et evaluator location hors candidate write scope.
- Conserver un plan `frozen`; toute nouvelle preuve provoque une révision explicite et traçable.
