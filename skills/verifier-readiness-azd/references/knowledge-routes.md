# Routes de connaissance AZDone

Les IDs réduisent la recherche; ils ne choisissent ni technologie ni autorité.

## Familles

- `language.workflow.core`: goal, outcome, scope, carte, dépendance, blocker, risque, décision, ADR, trade-off, critère, preuve et Done.
- `language.workflow.git`: dépôt, branche, commit, diff, PR, review, merge, rebase, conflit, worktree, tag et release.
- `language.quality.qa`: test, QA, unit, intégration, E2E, fixture, mock, oracle, régression, accessibilité, performance et sécurité.
- `architecture.project.detected`: noyau universel et modules activés par les surfaces observées.
- `architecture.web.frontend`: interface web dans un navigateur.
- `architecture.chat.telegram`: bot, transport, session, webhook/polling et replay conversationnel.
- `architecture.api.backend`: endpoint, schéma, auth, rate limit, idempotence, queue, worker et runtime.
- `architecture.data.relational`: données, index, migration, transaction, backup, restore et rétention.
- `proof.surface.detected`: famille de preuve sélectionnée pour la surface réelle.
- `proof.web.browser-e2e`: serveur, navigateur, viewports, interaction, accessibilité et capture.
- `proof.chat.conversation-replay`: transport isolé, scénario humain, continuité, erreurs et non-envoi production.
- `proof.workflow.readiness`: forecast, matrice de preuve, fraîcheur, autorité et blockers.
- `research.project.primary-sources`: dépôt, documentation locale et artefacts du projet.
- `research.official.current`: documentation, standard, release ou dépôt upstream officiel et actuel.
- `research.domain.regulated`: vocabulaire et obligations spécialisés avec sources primaires.

## Route Pack

```yaml
route_pack:
  ticket_id: ""
  requested_routes: []
  effective_routes: []
  rejected_routes: []
  loaded_references: []
  missing_capabilities: []
  freshness: ""
  stop_reason: ""
```

## Résolution

1. Partir du langage simple et des surfaces observées.
2. Activer uniquement les familles nécessaires au ticket.
3. Charger les références locales avant toute recherche externe.
4. Utiliser des sources primaires pour un terme ou standard matériel, spécialisé, réglementé ou incertain.
5. Produire un `Route Pack` traçable avec routes rejetées et raison d'arrêt.
6. Ne jamais installer un outil ou exécuter une URL par simple résolution.
