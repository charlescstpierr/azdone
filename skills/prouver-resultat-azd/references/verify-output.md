# Sortie · verification

Bloc de sortie complet du skill `prouver-resultat-azd`.

```yaml
verification:
  commit: ""
  ci: green | red | unknown
  worktree: ""
  provenance:
    agent_id: ""
    agent_role: ""
    verified_commit: ""
    evaluator_commit: ""
    commands: []
    artifacts: []
  detected_surfaces: []
  surface_gates:
    web: []
    mobile: []
    backend: []
    api: []
    infra: []
    data: []
    library: []
    cli_tui: []
    docs_workflow: []
  evaluator:
    frozen: true
    outside_candidate_write_scope: true
  carryover_gate:
    checked_transitions: []
    dropped_fields: []
    freshness_boundaries: []
    status: pass | fail | blocked
  evidence_graph:
    nodes: [{type: claim | source | artifact | oracle, id: ""}]
    edges: [{type: supports | contradicts | derived_from | supersedes, from: "", to: ""}]
    drift: [{type: stale | superseded | contradicted | temporal_regression | negation_artifact, revalidation_condition: ""}]
  matrix:
    - claim: ""
      status: passed | partial | blocked | failed
      evidence: ""
      freshness: ""
      oracle: ""
      risk: ""
  readiness_usage:
    forecast: ""
    planned_tools: []
    tools_actually_used: []
    missing_means: []
  app_verification:
    mode: generer | executer | maintenir
    skill_path: ""
    matrix: []
    feature_map_updated: true | false
    verdict: verified | partial | blocked | failed
  functional_proof: verified | partial | blocked | failed
  approval_readiness:
    target_ecosystems: []
    status: ready | partial | blocked | not-applicable
    evidence: []
  external_approval:
    status: not-requested | submitted | approved | rejected | blocked
    evidence: []
  causal_return: none | readiness | understanding | diagnosis | design | plan | build
  status: verified | partial | blocked | failed
```

`ci` reflète le dernier run CI observé sur `commit`, `unknown` en son absence. `reviser-qualite-azd` reprend `commit` et `ci` tels quels dans le témoin `.azdone/conditions-ok`.
