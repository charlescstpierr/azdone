---
name: verifier-application-azd
description: "Vérifier l'application réelle en la lançant et en l'exerçant sur sa surface (web, API, CLI ou TUI, mobile, desktop, chat, données) à partir d'une carte de vérification propre au projet. Utiliser pour générer ou maintenir le skill repo-local `verifier-<app>`, pour prouver un claim sur l'artefact réel plutôt que sur un proxy, et avant Done quand les tests seuls ne suffisent pas."
---

# Socle · Vérifier l'application réelle

Prouver qu'une fonctionnalité marche en la faisant marcher, pas en lisant le code ni en se fiant à « les tests passent ». Ce skill est transversal : `initialiser-projet-azd` le génère une fois par projet, `prouver-resultat-azd` l'exécute à chaque preuve fonctionnelle, `surveiller-livraison-azd` le rejoue après une release.

## Quick start

```text
$verifier-application-azd generer
$verifier-application-azd executer "export CSV, filtre par date, erreur sur date invalide"
```

Artefact attendu : un skill repo-local `verifier-<app>/SKILL.md` (mode `generer`), ou une matrice `app_verification` fonctionnalité par fonctionnalité avec artefacts et verdict `verified | partial | blocked | failed` (mode `executer`).

## Utiliser quand

- `initialiser-projet-azd` entre pour la première fois dans un dépôt qui a une surface exécutable.
- `prouver-resultat-azd` doit prouver un claim sur l'application réelle et non sur un test unitaire.
- La surface a changé (nouvelle commande, nouvelle page, nouveau port) et la carte de vérification est périmée.

## Trois modes

**`generer`** (une fois, puis à la demande) :

1. Lire la Boussole, le System Success Map, le contrat public et le Readiness Forecast ; inspecter le dépôt pour détecter les surfaces réelles et la façon de les lancer (`package.json`, `Makefile`, `pyproject`, `Dockerfile`, `compose`, scripts, README).
2. Établir, sans rien installer, comment démarrer l'application en isolation : commande, port ou chemin, variables d'environnement non secrètes, données de test, condition de santé observable, commande d'arrêt.
3. Établir comment observer chaque fonctionnalité : navigateur piloté pour le web, requêtes réelles pour une API, transcript stdout/stderr/exit code pour une CLI ou TUI, simulateur ou appareil pour mobile, conversation rejouée pour un chat, requête et invariant pour des données.
4. Écrire le skill repo-local `verifier-<app>/SKILL.md` à partir de [verify-app-template.md](references/verify-app-template.md), dans le dossier de skills de l'hôte, avec la feature map ([feature-map-template.md](references/feature-map-template.md)) amorcée en `statut: never`.
5. Pour tout moyen manquant (navigateur, simulateur, fixture, compte de test), créer un gap dans le Readiness Forecast avec recommandation et repli ; ne jamais l'installer ni l'utiliser sans autorité.

**`executer`** (à chaque preuve) :

6. Lire `verifier-<app>/SKILL.md` ; s'il manque ou si la surface a changé, repasser par `generer` ou `maintenir` avant toute preuve.
7. Démarrer l'application en isolation (port dédié, données de test, jamais la production, jamais un compte réel), attendre la condition de santé, sinon rendre `blocked` avec la cause.
8. Pour chaque fonctionnalité demandée, exécuter l'observation décrite, comparer au résultat attendu, capturer un artefact horodaté sous `.azdone/proofs/<date>/` (capture, transcript, réponse HTTP, log) et noter le commit vérifié. Suivre le protocole [preuve-visuelle.md](references/preuve-visuelle.md) pour le `manifest.json`, le `report.md` et l'enregistrement d'écran optionnel.
9. Exercer aussi les états non nominaux listés dans la carte : vide, erreur, saisie invalide, interruption, taille de terminal pour une CLI.
10. Arrêter l'application, mettre à jour la feature map avec commit, date, artefact et statut, puis rendre la matrice `app_verification`.

**`maintenir`** (quand la surface change) :

11. Comparer la carte au dépôt courant, marquer `stale` ce qui a bougé, ajouter les nouvelles fonctionnalités en `never`, retirer celles qui n'existent plus, et le dire dans la réponse.

## Sortie

Le skill rend un bloc `app_verification` documenté dans [app-verification-output.md](references/app-verification-output.md) : `mode`, `app`, `skill_path`, `started`, `health`, `matrix` (feature, observation, expected, observed, artifact, status), `feature_map_updated`, `gaps`, `verdict`.

## Arrêt et interdits

- Jamais contre la production, un compte réel, des credentials ou des données client ; en isolation seulement. L'autorité explicite se lit dans `.azdone/trust.yaml` (`actions.<action>`) quand ce fichier existe ; sinon `authority-request`.
- « Inconclusive » n'est pas un succès : une observation impossible rend `blocked` avec le moyen manquant, jamais `verified`.
- Une fonctionnalité prouvée sur un proxy (mock, test unitaire, capture ancienne) ne peut pas passer `verified` ici.
- Ne jamais modifier le code candidat pendant la vérification ; un défaut trouvé retourne à `construire-solution-azd` par `prouver-resultat-azd`.
- Rapid : 0 sous-agent sauf justification écrite. Si délégué, suivre `skills/azd/references/context-packet.md` et `model-routing.md` pour le rôle `verifier`.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
