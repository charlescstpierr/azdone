# Sortie · readiness_forecast

Voir [readiness-contract.md](readiness-contract.md) pour le schéma complet du `proof_adapter_matrix` et du `readiness_forecast`. Forme minimale :

```yaml
readiness_forecast:
  scope: ""
  risk_level: rapid | standard | critical
  freshness: fresh | stale | provisional
  dependencies: []
  missing_prerequisites: []
  affected_tickets: []
  verdict: ready | at-risk | waiting | authority-required | blocked
  next_safe_action: ""
```

## Statuts

- moyen de preuve : `ready | warn | missing | authority-required | credential-required | incompatible | blocked`.
- forecast : `ready | at-risk | waiting | authority-required | blocked`.
- connaissance : `observed | inferred | researched | human-approved | stale`.

Une installation réussie ne prouve pas la surface. Une surface sans oracle réel reste inconnue ou bloquée.

## Exemples de gap

- Web : serveur lançable, navigateur/E2E compatible, viewports, accessibilité et captures.
- Telegram/chat : transport ou client de test isolé, scénario conversationnel et preuve de non-envoi en production.
- API : schéma, sandbox ou mock fidèle, credentials bornés, succès/erreur, idempotence et limites.
- Mobile/desktop : build lançable, simulateur/appareil ou contrôle GUI, permissions, logs et artefacts visuels.
- Données : moteur/version, fixtures, migrations, backup, restore et intégrité.
- Projet non-code : source de vérité, outil de production, réviseur, format livrable et critère d'acceptation observable.

Ces exemples sont des candidats, jamais des dépendances obligatoires. Playwright ou Telethon ne sont proposés que s'ils ferment un gap réel, sont compatibles et respectent l'autorité.
