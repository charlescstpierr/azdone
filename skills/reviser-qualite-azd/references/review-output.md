# Sortie · review

Bloc de sortie complet du skill `reviser-qualite-azd`.

```yaml
review:
  risk_level: rapid | standard | critical
  reviewer_id: ""
  author_id: ""
  base_commit: ""
  changed_files: []
  planted_defect_protocol:
    defect_class: logic | contract | security | test-gap | evidence-drift
    attempted: true | false
    result: found | not-found | blocked
  author_evidence: []
  reviewer_evidence: []
  stage_1_contract_spec: pass | fail | blocked
  stage_2_quality_correctness_security_simplicity: pass | fail | blocked
  findings:
    - id: ""
      source: host | cli:<adaptateur>
      severity: critical | high | medium | low
      file: ""
      line_or_selector: ""
      evidence: ""
      impact: ""
      action: ""
      correction_status: open | fixed | rejected
      reviewer_verdict: pending | accepted | rejected
  causal_return: readiness | understanding | diagnosis | design | plan | build | none
  verdict: accept | return-to-build | blocked | failed
```

`source` vaut `host` pour le reviewer principal, `cli:<adaptateur>` pour un relecteur externe (`second_reviewer` ou panel). Un finding externe porte l'id `EXT-<n>-<code>` (ex. `EXT-1-SEC-01`).

## Témoin D1 (`.azdone/conditions-ok`)

Écrit par ce skill seul, sur `accept`, un `clé: valeur` par ligne :

```
commit: <sha vérifié>
ci: green | red | unknown
review: accept | return-to-build
reviewer_id: <id>
author_id: <id>
risk: rapid | standard | critical
files_changed: <n>
lanes: <n>
written_at: <ISO-8601 UTC>
```

`commit` et `ci` sont repris tels quels du bloc de sortie `verification` de `prouver-resultat-azd` (champs `commit` et `ci`). Le témoin est supprimé sur `return-to-build`.
