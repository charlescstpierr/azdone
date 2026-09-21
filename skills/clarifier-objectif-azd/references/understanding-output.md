# Sortie `understanding` (Étape 02)

Contenu attendu :

- `outcome contract`;
- `blind spots`;
- Boussole et changements proposés;
- `risk_level`;
- `language_pack`;
- `domain_model` léger;
- `confidence` et `zero_assumption_gate`;
- `author_id`, `reviewer_id`, `repository`, `worktree` si connus;
- one material question maximum per round avec trois directions maximum, ou verdict `proceed` / `blocked`.

```yaml
understanding:
  outcome: ""
  constraints: []
  non_goals: []
  evidence_required: []
  unknowns: []
  blind_spots: []
  domain_model:
    vocabulary: []
    identities: []
    entities: []
    invariants: []
    lifecycle: []
    examples: []
    counterexamples: []
  confidence: low | medium | high
  zero_assumption_gate:
    passed: false
    blockers: []
  project_compass:
    user: ""
    problem: ""
    success: []
    target_ecosystems: []
    non_negotiables: []
    refusals: []
    non_goals: []
    opportunity_criteria: []
    freshness: fresh | stale
  language_pack:
    human_terms: []
    business_terms: []
    technical_terms: []
    architecture_terms: []
    proof_terms: []
  risk_level: rapid | standard | critical
  material_question:
    round: 1
    question: ""
    risk_removed: ""
    options:
      - type: recommendation | best-alternative | status-quo
        tradeoffs: {cost: "", delay: "", complexity: "", risk: "", reversibility: "", graph_impact: "", proof: ""}
  author_id: ""
  reviewer_id: ""
  repository: ""
  worktree: ""
  verdict: proceed | blocked
```
