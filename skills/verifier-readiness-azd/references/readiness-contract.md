# Contrat Readiness AZDone

## Proof Adapter Matrix

```yaml
proof_adapter_matrix:
  - claim_id: ""
    surface: ""
    proof_method: ""
    tool_or_adapter: ""
    environment: ""
    access_and_data: []
    oracle: ""
    status: ready | warn | missing | authority-required | credential-required | incompatible | blocked
    evidence: []
    verified_at: ""
    revalidate_on: []
```

## Readiness Forecast

```yaml
readiness_forecast:
  forecast_id: ""
  project_id: ""
  ticket_id: ""
  risk_level: rapid | standard | critical
  scope: ""
  observed_at: ""
  freshness: fresh | stale | provisional
  prerequisites:
    - id: ""
      kind: decision | ticket | component | tool | sdk | program | environment | account | credential | permission | data | fixture | contract | asset | approval | proof
      status: ready | at-risk | waiting | authority-required | blocked
      needed_by: ""
      dependency_path: []
      affected_tickets: []
      owner_or_authority: ""
      estimated_delay: ""
      recommended_margin: ""
      recommendation: ""
      best_alternative: ""
      status_quo: ""
      tradeoffs: []
      evidence: []
  verdict: ready | at-risk | waiting | authority-required | blocked
  next_safe_action: ""
  revalidate_on: []
```

## Règles de fraîcheur

- Fait local: revalider si fichier, commit, composant ou interface change.
- Outil: revalider si version, configuration, installation ou environnement change.
- Service externe: revalider si fournisseur, version, documentation, accès ou credential change.
- Décision: revalider si Boussole, contrainte, ADR ou dépendance matérielle change.
- Preuve: revalider si surface, environnement, données, oracle ou claim change.

Une entrée stale reste auditable mais ne peut prouver `Ready` ou `Done`.

## Porte de transition

Une carte ne devient `Ready` que si:

1. les décisions bloquantes sont résolues;
2. les dépendances transitives ont un chemin prêt ou un blocker assigné;
3. le contrat de preuve est verrouillé;
4. outil, accès, environnement, données et oracle sont prêts;
5. les routes de contexte nécessaires sont résolues;
6. le forecast est frais;
7. l'autorité nécessaire est présente.

Avant `Done`, vérifier que le moyen annoncé a effectivement produit la preuve attendue. Ne jamais substituer un mock, une installation ou un test inférieur à la preuve contractuelle sans rouvrir la décision.
