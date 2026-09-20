# Sortie `structure` (Étape 06b)

Bloc de sortie complet du skill `structurer-code-azd`.

```yaml
structure:
  data_shapes:
    - name: ""
      kind: entity | identity | value | event | state-machine
      invariants: []
      lifecycle: []
  organizing_structures:
    - shape: ""
      chosen: state-machine | table | registry | typed-model
      rejected: []
      reason: ""
  boundaries:
    validate_at: []
    trust_inside: []
    pure_core: []
  shared_state:
    - actor_pair: ""
      shared: ""
      separated_before_serializing: true
  invariants: []
  idempotent_operations: []
  removals: []
  options:
    - name: recommendation | alternative | status-quo
      description: ""
      cost: ""
      reversibility: low | medium | high
      reading_load: ""
      migration_impact: ""
      proof_required: ""
  decision: ""
  adr_path: ""
  migration:
    plan: migrate-callers-then-remove-old
    waves: 1
    steps: []
  verifiable_units:
    - id: ""
      description: ""
      proof: ""
      depends_on: []
  verdict: decided | question | blocked
```

## Règles de verdict

- `decided`: une structure est choisie, l'ADR est écrit à `adr_path`, chaque `data_shapes` a ses invariants, `unverifiable_units` (`verifiable_units`) sont ordonnées avec leur preuve, et aucune forme de donnée du chemin critique ne reste `unknown`.
- `question`: une décision matérielle reste ouverte (impact produit, coût irréversible ou ambiguïté sur une forme de donnée partagée); rendre alors `options` complet et poser au plus une question matérielle avant de continuer.
- `blocked`: une forme de donnée du chemin critique reste `unknown`, un ADR requis ne peut pas être écrit à l'emplacement fixé par l'init, ou `shared_state` révèle une écriture concurrente non séparée; fail closed dans ces trois cas.
- `decision` doit toujours nommer l'option retenue parmi `options`, jamais un choix implicite.
- `migration.plan` reste `migrate-callers-then-remove-old`: aucun état de compatibilité jetable ne survit à la vague de migration.
