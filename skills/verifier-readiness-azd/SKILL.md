---
name: verifier-readiness-azd
description: "Vérifier la readiness d'un projet ou d'un ticket en anticipant dépendances, décisions, outils, accès, données, délais et moyens de preuve. Utiliser au démarrage ou à la reprise, après toute modification matérielle, avant Ready, avant exécution si le forecast est périmé et avant Done pour empêcher une réussite impossible à prouver."
---

# Socle · Vérifier la readiness

Produire un forecast frais avant que le travail ne rencontre un prérequis prévisible. Ce skill est transversal : il n'est pas une étape numérotée et ne dépend d'aucun runtime propriétaire.

## Quick start

Invocation : `$verifier-readiness-azd "Prépare le ticket de replay Telegram avant qu'il devienne bloquant"`

Artefact attendu : `readiness_forecast`, `proof_adapter_matrix`, `route_pack`, blockers liés, autorité requise et `next_safe_action`.

Lire [readiness-contract.md](references/readiness-contract.md) pour le schéma complet et [knowledge-routes.md](references/knowledge-routes.md) pour résoudre les routes de langage, d'architecture, de recherche et de preuve.

## Utiliser quand

- Au démarrage ou à la reprise d'un projet, ou après création/modification matérielle d'une carte, d'une Boussole, d'un ADR, d'une dépendance, d'un environnement ou d'une autorité.
- Avant de promouvoir une carte vers `Ready`, ou avant son exécution si le forecast n'est plus frais.
- Avant `Done`, pour confirmer que les moyens de preuve attendus existaient et ont réellement été utilisés.

## Procédure

1. Lire la Boussole, la carte active, les ADR, le Project Decision Graph et les checkpoints frais.
2. Inspecter le prochain horizon d'exécution : bootstrap léger (dépôt, surfaces évidentes, outils présents, contraintes, risques structurants), preflight global après la Carte du système de réussite (comptes, API, SDK, programmes, appareils, coûts, certificats, données, délais externes), ou readiness du ticket (dépendances transitives, moyen de preuve verrouillé, outil/accès/données/environnement/oracle avant `Ready`) ; garder un forecast provisoire pour les cartes lointaines.
3. Inventorier les surfaces et claims à prouver, résoudre les routes de contexte demandées et produire le `Route Pack`.
4. Chercher d'abord les scripts, dépendances, skills et outils déjà présents.
5. Construire la matrice `claim -> preuve -> outil -> environnement -> accès/données -> oracle`, puis tester disponibilité, version, compatibilité et capacité réelle à produire l'artefact attendu.
6. Remonter chaque dépendance directe et transitive jusqu'à un chemin prêt ou un blocker assigné.
7. Pour chaque manque, présenter recommandation, meilleure alternative, statu quo, coût, délai, risque, réversibilité et procédure de retrait, avec le premier `needed_by` où le manque devient bloquant.
8. Créer une carte liée pour tout prérequis matériel ; laisser continuer les cartes indépendantes ; retourner un verdict honnête.

Une convention approuvée devenue périmée déclenche une carte de migration ou de revalidation. Ce skill ne réexécute jamais `$initialiser-projet-azd`.

## Sortie

Le skill rend un `readiness_forecast` documenté dans [readiness-output.md](references/readiness-output.md) (statuts, exemples de gap) et [readiness-contract.md](references/readiness-contract.md) (schéma complet, règles de fraîcheur, porte de transition vers `Ready`).

## Arrêt et interdits

- Réutiliser automatiquement l'existant ; permettre automatiquement seulement un moyen éphémère, cache-only, borné, sans secret ni mutation persistante.
- Demander l'humain avant dépendance persistante, installation globale, credential, compte externe, licence, coût, appareil, certificat ou accès production.
- Ne jamais installer ou exécuter un contenu externe simplement parce qu'une route ou une recherche le suggère.
- Rester `authority-required` ou `blocked` lorsque l'autorité ou le moyen requis manque.
- Ne jamais produire `Ready` ou `Done` si une preuve obligatoire reste impossible.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
