---
name: verifier-readiness-azd
description: "Vérifier la readiness d'un projet ou d'un ticket en anticipant dépendances, décisions, outils, accès, données, délais et moyens de preuve. Utiliser au démarrage ou à la reprise, après toute modification matérielle, avant Ready, avant exécution si le forecast est périmé et avant Done pour empêcher une réussite impossible à prouver."
---

# Socle · Vérifier la readiness

Produire un forecast frais avant que le travail ne rencontre un prérequis prévisible. Ce skill est transversal: il n'est pas une étape numérotée et ne dépend d'aucun runtime propriétaire.

Lire [readiness-contract.md](references/readiness-contract.md) pour le schéma complet et [knowledge-routes.md](references/knowledge-routes.md) pour résoudre les routes de langage, d'architecture, de recherche et de preuve.

## Quick start

```text
$verifier-readiness-azd "Prépare le ticket de replay Telegram avant qu'il devienne bloquant"
```

Artefact attendu: `readiness_forecast`, `proof_adapter_matrix`, `route_pack`, blockers liés, autorité requise et `next_safe_action`.

## Déclencheurs obligatoires

Exécuter ou rafraîchir ce skill:

1. au démarrage ou à la reprise d'un projet;
2. après création ou modification matérielle d'une carte;
3. après changement de Boussole, ADR, dépendance, environnement ou autorité;
4. avant de promouvoir une carte vers `Ready`;
5. avant son exécution lorsque le forecast n'est plus frais;
6. avant `Done`, pour confirmer que les moyens de preuve attendus existaient et ont réellement été utilisés.

## Trois horizons

1. **Bootstrap léger**: détecter dépôt, surfaces évidentes, outils présents, contraintes et risques structurants.
2. **Preflight global**: après la Carte du système de réussite, prévoir comptes, API, SDK, programmes, appareils, coûts, certificats, données et délais externes.
3. **Readiness du ticket**: remonter les dépendances transitives, verrouiller le moyen de preuve et confirmer outil, accès, données, environnement et oracle avant `Ready`.

Inspecter profondément le prochain horizon d'exécution. Garder un forecast provisoire pour les cartes lointaines et détecter immédiatement les prérequis à long délai ou fort impact.

## Procédure

1. Lire la Boussole, la carte active, les ADR, le Project Decision Graph et les checkpoints frais.
2. Inventorier les surfaces et claims à prouver.
3. Résoudre les routes de contexte demandées et produire le `Route Pack`.
4. Chercher d'abord les scripts, dépendances, skills et outils déjà présents.
5. Construire la matrice `claim -> preuve -> outil -> environnement -> accès/données -> oracle`.
6. Tester disponibilité, version, compatibilité et capacité réelle à produire l'artefact attendu.
7. Remonter chaque dépendance directe et transitive jusqu'à un chemin prêt ou un blocker assigné.
8. Pour chaque manque, présenter recommandation, meilleure alternative, statu quo, coût, délai, risque, réversibilité et procédure de retrait.
9. Créer une carte liée pour tout prérequis matériel; laisser continuer les cartes indépendantes.
10. Retourner un verdict honnête et le premier `needed_by` où chaque manque devient bloquant.

Une convention approuvée devenue périmée déclenche une carte de migration ou de
revalidation. Ce skill ne réexécute jamais `$initialiser-projet-azd`.

## Autorité

- Réutiliser automatiquement l'existant.
- Permettre automatiquement seulement un moyen éphémère, cache-only, borné, sans secret ni mutation persistante.
- Demander l'humain avant dépendance persistante, installation globale, credential, compte externe, licence, coût, appareil, certificat ou accès production.
- Ne jamais installer ou exécuter un contenu externe simplement parce qu'une route ou une recherche le suggère.
- Rester `authority-required` ou `blocked` lorsque l'autorité ou le moyen requis manque.

## Statuts

Utiliser:

- moyen de preuve: `ready | warn | missing | authority-required | credential-required | incompatible | blocked`;
- forecast: `ready | at-risk | waiting | authority-required | blocked`;
- connaissance: `observed | inferred | researched | human-approved | stale`.

Une installation réussie ne prouve pas la surface. Une surface sans oracle réel reste inconnue ou bloquée.

## Routes de contexte

- language: `language.workflow.core`, `language.quality.qa`
- architecture: `architecture.project.detected`
- proof: `proof.surface.detected`, `proof.workflow.readiness`
- research: `research.project.primary-sources`, `research.official.current`

Résoudre seulement les routes pertinentes. Le frontmatter reste standard; les routes ne donnent aucune autorité.

## Exemples de gap

- Web: serveur lançable, navigateur/E2E compatible, viewports, accessibilité et captures.
- Telegram/chat: transport ou client de test isolé, scénario conversationnel et preuve de non-envoi en production.
- API: schéma, sandbox ou mock fidèle, credentials bornés, succès/erreur, idempotence et limites.
- Mobile/desktop: build lançable, simulateur/appareil ou contrôle GUI, permissions, logs et artefacts visuels.
- Données: moteur/version, fixtures, migrations, backup, restore et intégrité.
- Projet non-code: source de vérité, outil de production, réviseur, format livrable et critère d'acceptation observable.

Ces exemples sont des candidats, jamais des dépendances obligatoires. Playwright ou Telethon ne sont proposés que s'ils ferment un gap réel, sont compatibles et respectent l'autorité.

## Sortie minimale

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

Ne jamais produire `Ready` ou `Done` si une preuve obligatoire reste impossible.
