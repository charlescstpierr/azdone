# Sortie · operate

## Evidence contract

- `incident_evidence` contient `incident_id`, `timeline`, `first_seen_at`, `detected_by`, `impact`, `affected_paths`, `baseline_refs`, `current_refs`, `mitigation`, `root_cause_status`, `owner`, `next_update_at` et des liens d'artefacts redacted.
- `canary_evidence` contient chaque `step`, pourcentage, fenetre, `baseline_refs`, requetes/synthetics executes, resultats logs/metrics/traces, decision gate et raison de stop/advance.
- `rollback_evidence` contient `authority_artifact`, action executee, `previous_version`, `target_version`, `active_version_proof`, post-rollback health checks, residual risk et owner.
- Toute evidence doit porter provenance: source, timestamp, query/window, environment, artifact path ou dashboard link. Secrets, tokens et personal data sont remplaces par `redacted` avec une note de redaction.
- Une absence de baseline comparable, d'autorite explicite, de host capability ou d'artefact writable produit `partial`, `blocked`, `failed` ou `authority-request`; never infer healthy production from missing evidence.

Bloc de sortie complet du skill `surveiller-livraison-azd`.

```yaml
operate:
  release: ""
  environment: ""
  host_capabilities:
    observability: present | missing
    traffic_control: present | missing
    deploy_control: present | missing
    rollback_control: present | missing
    incident_channel: present | missing
    artifact_write: present | missing
    capability_gap: []
  progress_snapshot: {phase: operate, status: running | verified | partial | blocked | failed, done: 0, total: 0, blocked_by: [], last_checked_at: "", next_check: ""}
  baseline:
    baseline_refs: []
    comparable_window: ""
    captured_at: ""
  thresholds:
    success: []
    hold: []
    rollback: []
  canary_evidence:
    - step: ""
      exposure: ""
      window: ""
      baseline_refs: []
      observations: []
      decision: continue | hold | stop | rollback | authority-request
      reason: ""
  incident_evidence:
    - incident_id: ""
      timeline: []
      impact: ""
      affected_paths: []
      baseline_refs: []
      current_refs: []
      mitigation: ""
      root_cause_status: unknown | suspected | confirmed
  observations: []
  graph_invalidations: []
  linked_cards: []
  decision: continue | hold | escalate | rollback | authority-request
  rollback_evidence:
    - authority_artifact: ""
      previous_version: ""
      target_version: ""
      active_version_proof: []
      post_rollback_health: []
      residual_risk: []
      redactions: []
  verdict: verified | partial | blocked | failed
```
