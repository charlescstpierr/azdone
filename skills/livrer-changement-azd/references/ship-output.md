# Sortie · ship

Bloc de sortie complet du skill `livrer-changement-azd`.

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
