# Sortie `build` (Étape 08)

Bloc de sortie complet du skill `construire-solution-azd`.

```yaml
build:
  card_id: ""
  readiness_forecast: fresh | stale | blocked
  proof_contract: locked | missing | stale
  author_id: ""
  worktree: ""
  write_scope: []
  red:
    command: ""
    evidence: ""
  green:
    command: ""
    evidence: ""
  refactor:
    command: ""
    evidence: ""
  changed_files: []
  protected_out_of_scope: []
  discovered_draft_cards: []
  causal_return: none | readiness | understanding | diagnosis | design | plan | build
  verdict: green | partial | blocked | failed
```
