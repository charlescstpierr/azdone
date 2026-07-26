---
name: surveiller-livraison-azd
description: "Surveiller une livraison, exécuter un canary autorisé, comparer la production à une baseline et traiter incident ou rollback avec preuves. Utiliser pour observer logs, métriques, traces, santé de production, impact d'incident ou conditions d'un rollback autorisé."
---

# Étape 12 · Surveiller la livraison

Observe une livraison et recupere sous autorite. Monitor and recover under authority. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$surveiller-livraison-azd "Observe le canary 10% de release abc123 pendant 30 minutes; rollback seulement si autorise."`

Verdict attendu: baseline, logs/metrics/traces horodates, decision `continue`, `hold`, `escalate`, `rollback` ou `authority-request`.

## Utiliser quand / Use when

Utilise ce skill pour monitor une release, comparer avec une baseline, traiter un incident, conduire un canary autorise ou preparer/executer un rollback autorise.

## Procedure

1. Identifie release, environment, parcours critiques, owners, risques du graphe et observation window.
2. Capture une `baseline` comparable avant changement avec les memes requetes et fenetres.
3. Choisis signaux: `logs`, `metrics`, `traces`, erreurs, latence, saturation, disponibilite et indicateurs produit.
4. Gele les seuils de success, hold, canary-stop, incident-escalation et rollback avant mutation de `production`.
5. Commence en lecture seule; ne deduis pas l'autorite de mutation depuis l'acces observability.
6. Verifie l'`explicit authority` avant canary, traffic shift, config change, deploy ou rollback; sinon retourne `authority-request`.
7. Declare les `host_capabilities` reellement disponibles: `observability`, `traffic_control`, `deploy_control`, `rollback_control`, `incident_channel`, `artifact_write`. Missing capability must fail closed: retourne `blocked` avec `capability_gap` au lieu de simuler une observation, un canary ou un rollback.
8. Augmente l'exposition par paliers predetermines apres une fenetre complete et conforme.
9. Stoppe sur toute protected regression; ne compense pas un defaut critique par une bonne moyenne globale.
10. Publie un `progress_snapshot`: `phase`, `status`, `done`, `total`, `blocked_by`, `last_checked_at`, `next_check`.
11. En incident, horodate le signal, préserve l'evidence, annonce l'impact connu, compare baseline/deployments/dependencies, puis sépare mitigation, root cause et correction durable. Créer les cartes liées et invalider les nœuds descendants concernés.
12. Apres rollback autorise, prouve la version active et la sante avec les signaux originaux.

## Evidence contract

- `incident_evidence` contient `incident_id`, `timeline`, `first_seen_at`, `detected_by`, `impact`, `affected_paths`, `baseline_refs`, `current_refs`, `mitigation`, `root_cause_status`, `owner`, `next_update_at` et des liens d'artefacts redacted.
- `canary_evidence` contient chaque `step`, pourcentage, fenetre, `baseline_refs`, requetes/synthetics executes, resultats logs/metrics/traces, decision gate et raison de stop/advance.
- `rollback_evidence` contient `authority_artifact`, action executee, `previous_version`, `target_version`, `active_version_proof`, post-rollback health checks, residual risk et owner.
- Toute evidence doit porter provenance: source, timestamp, query/window, environment, artifact path ou dashboard link. Secrets, tokens et personal data sont remplaces par `redacted` avec une note de redaction.
- Une absence de baseline comparable, d'autorite explicite, de host capability ou d'artefact writable produit `partial`, `blocked`, `failed` ou `authority-request`; never infer healthy production from missing evidence.

## Sortie / Output

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

Ne jamais inventer un etat sain quand les donnees sont absentes ou non comparables. Reporte `partial`, `blocked` ou `failed` avec la prochaine action sure.
