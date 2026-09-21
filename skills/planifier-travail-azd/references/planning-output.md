# Sortie `plan` (Étape 06)

Contenu attendu :

- dependency graph;
- requirement-to-proof map;
- wayfinder map si activée;
- contrat DevEx CLI/API/SDK seulement si pertinent;
- ownership et overlap decisions;
- ordering, intégration, reprise et rollback;
- verdict `ready`, `partial`, `blocked` ou `authority-request`.

```yaml
plan:
  frozen: true
  risk_level: rapid | standard | critical
  active_card: {id: "", state: Draft | Needs-Grilling | Ready | In-Progress | Review | Done | Blocked | Needs-Revalidation}
  project_decision_graph:
    nodes: [{id: "", type: goal | decision | requirement | ticket | dependency | risk | proof | artifact | opportunity}]
    edges: [{from: "", to: "", type: depends-on | enables | blocks | proves | contradicts | supersedes | impacts}]
  phase_dag: [{phase: "", depends_on: [], gate: [], functional_commit: ""}]
  wayfinder: {enabled: false, destination: "", fog: [], frontier: [], tickets: [], resume: {}}
  devex_contract: {applies: false, surface: cli | api | sdk | none, commands: [], flags: [], stdout: [], stderr: [], exit_codes: [], config_precedence: [], idempotency: [], examples: []}
  dependency_graph: []
  requirement_to_proof: []
  proof_contracts: [{claim: "", oracle: "", tool: "", environment: "", access_data: [], artifact: "", threshold: "", freshness: "", failure: ""}]
  readiness_forecast: {verdict: ready | at-risk | waiting | authority-required | blocked}
  context_packet: {compass: "", card: "", language_pack: "", adrs: [], proof_contract: "", readiness_forecast: "", checkpoint: ""}
  staffing: [{role: "", model_hint: "", reasoning_effort: "", expected_output: ""}]
  resume_context: {base_commit: "", branch: "", worktree: "", current_step: "", remaining_work: [], failed_approaches: [], resume_commands: [], next_safe_action: "", blockers: []}
  tasks: [{author_id: "", reviewer_id: "", paths: [], commands: [], write_scope: [], dependencies: [], red: "", green: "", proof: [], exit: "", resume: ""}]
  evaluator_scope: outside-candidate-write-scope
  recovery: []
  rollback: []
  verdict: ready | partial | blocked | authority-request
```
