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
