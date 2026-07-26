# Run contract / Contrat d’exécution

## Required fields

```yaml
goal: user wording
repository: absolute path
language: fr | en
base_commit: git sha or unknown
worktree: absolute repo-local path
author_id: agent or human implementing the change
reviewer_id: independent agent or human validating it
outcome:
  end_state: observable result
  invariants: []
  non_goals: []
  evidence_required: []
  unknowns: []
risk_level: rapid | standard | critical
project_compass:
  path: repo-local path
  freshness: fresh | stale | missing
active_card:
  id: ""
  state: Draft | Needs-Grilling | Ready | In-Progress | Review | Done | Blocked | Needs-Revalidation
decision_stack: []
opportunity_inbox: []
readiness_forecast:
  verdict: ready | at-risk | waiting | authority-required | blocked
policy:
  local_read: automatic
  reversible_isolated_write: automatic_with_trace
  global_install: explicit
  credentials: explicit
  external_publish: explicit
  merge_release_deploy: explicit
  destructive_or_ambiguous: explicit
route: []
status: running | verified | partial | blocked | failed
```

For interruption-safe runs, also carry:

```yaml
resume_context:
  base_commit: git sha or unknown
  branch: current or target branch
  worktree: active worktree
  current_step: current skill or gate
  remaining_work: []
  failed_approaches: []
  resume_commands: []
  next_safe_action: ""
  blockers: []
progress_snapshot:
  phase: init | clarification | discovery | diagnose | design | plan | isolate | build | verify | review | ship | operate | learn | evolve
  status: running | verified | partial | blocked | failed
  done: 0
  total: 0
  blocked_by: []
  last_checked_at: ""
  next_check: ""
```

Fail closed when `repository`, `author_id`, `reviewer_id`, required authority, or evidence freshness cannot be established. `author_id` and `reviewer_id` must be different for implementation review and evaluator review.

Use repo-local paths for every artifact:

```yaml
artifacts:
  bootstrap: []
  language: []
  architecture: []
  decision_graph: []
  readiness: []
  contracts: []
  plans: []
  tests: []
  screenshots: []
  accessibility: []
  verification: []
  release: []
  rollback: []
  learnings: []
```

## Gates distincts

```yaml
functional_proof:
  status: verified | partial | blocked | failed
approval_readiness:
  target_ecosystems: []
  status: ready | partial | blocked | not-applicable
external_approval:
  authority_required: true
  status: not-requested | submitted | approved | rejected | blocked
```

Une preuve fonctionnelle ne signifie pas une approbation externe. Une readiness
d'approbation ne signifie pas qu'Apple, Google, Microsoft, OpenAI, Anthropic ou
une autre plateforme a réellement approuvé le produit.

## Decision trace

Pour chaque transition, enregistrer brièvement le raisonnement et un
`handoff_carryover` lossless. Toute perte doit être explicite; une perte qui
touche une contradiction, un risque, une autorité, un oracle, un finding, un
rollback ou une claim incomplète bloque la transition.

```yaml
observed: fact with source
inferred: conclusion and confidence
decided: selected route
why: evidence or risk that justifies it
handoff_carryover:
  from_skill: ""
  to_skill: ""
  required_fields: []
  carried_fields: []
  transformed_fields: []
  dropped_fields: []
  freshness_boundary: ""
next_safe_action: skill, command, artifact check, authority request, or none
```

## Stop conditions

- Stopper en `verified` seulement avec preuve fraîche pour chaque claim; `next_safe_action: none`.
- Stopper en `partial` lorsque le résultat utile est incomplet mais récupérable; `next_safe_action` doit nommer la prochaine action fraîche et vérifiable.
- Stopper en `blocked` lorsqu’une autorité ou un état externe est indispensable; `next_safe_action` doit nommer la demande ou vérification qui débloque.
- Stopper en `failed` lorsqu’une vérification contredit le résultat et qu’aucune récupération sûre ne reste dans le run; `next_safe_action: none`.

## Resume

Recharger le goal, le commit de base, la route, les décisions, les preuves, `next_safe_action` et les changements non intégrés depuis `resume_context`. Revalider la fraîcheur de `next_safe_action` avant de reprendre; si elle n’est plus sûre ou vérifiable, recalculer une action fraîche avant toute écriture. Ne jamais reconstruire silencieusement l’intention à partir du dernier message seulement.

## Reviewer and evaluator separation

The author writes candidate changes only inside the declared write scope. The reviewer reads and reports independently. Any evaluator, benchmark, oracle, protected regression, or acceptance threshold stays outside the candidate write scope and is versioned before the candidate runs.
