# Sortie `branch_lab` (Étape 07)

Contenu attendu :

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
