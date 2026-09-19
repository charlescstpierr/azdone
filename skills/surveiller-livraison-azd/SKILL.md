---
name: surveiller-livraison-azd
description: "Surveiller une livraison, exécuter un canary autorisé, comparer la production à une baseline et traiter incident ou rollback avec preuves. Utiliser pour observer logs, métriques, traces, santé de production, impact d'incident ou conditions d'un rollback autorisé."
---

# Étape 12 · Surveiller la livraison

Observe une livraison et récupère uniquement sous autorité explicite.

## Quick start

Invocation : `$surveiller-livraison-azd "Observe le canary 10% de release abc123 pendant 30 minutes; rollback seulement si autorise."`

Artefact attendu : baseline, logs/metrics/traces horodatés, décision `continue`, `hold`, `escalate`, `rollback` ou `authority-request`.

## Utiliser quand

- Une release doit être monitorée et comparée à une baseline.
- Un incident survient et exige preuve, mitigation et root cause séparées.
- Un canary ou un rollback autorisé doit être conduit ou préparé.
- Observation d'une PR ou d'une CI via `agents/azd-watcher.md` (lecture seule, réveil par `/loop` sous Claude Code et Cursor).

## Procédure

1. Identifier release, environment, parcours critiques, owners, risques du graphe et observation window.
2. Capturer une `baseline` comparable avant changement avec les mêmes requêtes et fenêtres.
3. Choisir les signaux : `logs`, `metrics`, `traces`, erreurs, latence, saturation, disponibilité et indicateurs produit.
4. Geler les seuils de success, hold, canary-stop, incident-escalation et rollback avant toute mutation de `production`.
5. Commencer en lecture seule ; ne pas déduire l'autorité de mutation depuis l'accès observability, et vérifier l'`explicit authority` avant canary, traffic shift, config change, deploy ou rollback, sinon retourner `authority-request`. L'autorité explicite se lit dans `.azdone/trust.yaml` (`actions.<action>`) quand ce fichier existe ; sinon `authority-request`.
6. Déclarer les `host_capabilities` réellement disponibles (`observability`, `traffic_control`, `deploy_control`, `rollback_control`, `incident_channel`, `artifact_write`) : missing capability doit fail closed, retourner `blocked` avec `capability_gap` au lieu de simuler une observation, un canary ou un rollback.
7. Augmenter l'exposition par paliers prédéterminés après une fenêtre complète et conforme ; stopper sur toute protected regression sans compenser un défaut critique par une bonne moyenne globale.
8. Publier un `progress_snapshot` : `phase`, `status`, `done`, `total`, `blocked_by`, `last_checked_at`, `next_check`.
9. En incident, horodater le signal, préserver l'evidence, annoncer l'impact connu, comparer baseline/deployments/dependencies, puis séparer mitigation, root cause et correction durable ; créer les cartes liées et invalider les nœuds descendants concernés.
10. Après rollback autorisé, prouver la version active et la santé avec les signaux originaux.

Voir [operate-output.md](references/operate-output.md) pour l'evidence contract complet (`incident_evidence`, `canary_evidence`, `rollback_evidence`).

## Sortie

Le skill rend un bloc `operate` documenté dans [operate-output.md](references/operate-output.md) : `release`, `environment`, `host_capabilities`, `progress_snapshot`, `baseline`, `thresholds`, `canary_evidence`, `incident_evidence`, `observations`, `graph_invalidations`, `linked_cards`, `decision`, `rollback_evidence`, `verdict`.

## Arrêt et interdits

- Ne jamais inventer un état sain quand les données sont absentes ou non comparables.
- Reporter `partial`, `blocked` ou `failed` avec la prochaine action sûre.
- Fail closed si une host capability requise est absente au lieu de simuler l'observation, le canary ou le rollback.
- N'agir sur canary, traffic shift, config change, deploy ou rollback qu'avec `explicit authority` prouvée.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
