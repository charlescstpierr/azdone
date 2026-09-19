# Sortie `diagnosis` (Étape 04)

Contenu attendu :

- étapes de reproduction;
- `hypothesis ledger`;
- root cause ou meilleure explication soutenue;
- fresh evidence et verdict `diagnose-only`.

```yaml
diagnosis:
  author_id: ""
  reviewer_id: ""
  reproduction: []
  diagnosis_ledger:
    - command: ""
      environment: ""
      expected: ""
      actual: ""
      artifact: ""
  hypothesis_ledger: []
  author_evidence: []
  reviewer_evidence: []
  root_cause: ""
  invalidated_assumption: ""
  graph_impact: []
  confidence: low | medium | high
  evidence: []
  verdict: diagnose-only | blocked | failed
```
