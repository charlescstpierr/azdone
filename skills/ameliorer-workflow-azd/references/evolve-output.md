# Sortie · evolve

Bloc de sortie complet du skill `ameliorer-workflow-azd`.

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
