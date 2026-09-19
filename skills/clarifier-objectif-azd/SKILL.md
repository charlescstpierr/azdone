---
name: clarifier-objectif-azd
description: "Clarifier adaptativement tout résultat produit, backend, infrastructure, données, mobile, desktop, web, CLI, librairie, documentation, migration ou incident. Utiliser lorsque l'objectif est large, incomplet, sensible à l'autorité ou exige une question matérielle, un niveau de confiance, un zero-assumption gate ou un modèle de domaine léger avant d'agir."
---

# Étape 02 · Clarifier l'objectif

Rester domain-agnostic: produit, backend, infra, data, mobile, desktop, web, CLI, librairie, docs, migration et incident partagent le même cadrage. Transformer adaptativement la demande en petit `adaptive outcome contract` avant de planifier ou coder.

## Quick start

```text
$clarifier-objectif-azd "Répare le flux de paiement sans casser les abonnements existants"
```

Artefact attendu: Boussole suffisamment fraîche, `risk_level`, `understanding.verdict`, `confidence`, `zero_assumption_gate`, Language Pack minimal et au plus une question matérielle.

Lire [decision-card.md](references/decision-card.md) lorsqu'une décision matérielle exige trois choix comparables.

## Utiliser quand

- l'objectif est large ou incomplet;
- une information manquante peut changer la voie, le risque ou l'autorité;
- les exigences cachées, non-objectifs ou critères d'acceptation comptent;
- le vocabulaire, les identités, entités, invariants, lifecycle ou exemples du domaine peuvent changer l'implémentation.

## Procédure

1. Lire la Boussole créée par `$initialiser-projet-azd`; si elle manque ou est structurellement périmée, revenir à l'étape 00.
2. Reformuler le résultat dans la langue de l'utilisateur, séparer faits, hypothèses, contraintes et inconnues, et marquer toute hypothèse non vérifiée comme `assumption`, jamais comme fait.
3. Fixer l'état final observable, la preuve attendue et la condition d'arrêt, puis compléter la Boussole (utilisateur, problème, succès, écosystèmes cibles, non-négociables, refus, non-objectifs, critères d'opportunité); toute modification matérielle devient une décision versionnée.
4. Nommer les blind spots qui pourraient changer l'approche, y compris autorité, données sensibles, surface humaine, destruction, compatibilité, exploitation, distribution et contrats d'interface, et les garder séparés des `unknowns`: un `unknown` est une donnée manquante, un `blind_spot` est un angle oublié qui peut invalider l'approche même si une donnée locale semble suffisante.
5. Construire un domain model léger quand le domaine compte: `vocabulary`, `identities`, `entities`, `invariants`, `lifecycle`, `examples`, `counterexamples`.
6. Produire un `Language Pack` borné à la carte: termes humains, termes métier, termes techniques utiles, éléments d'architecture touchés et moyens de preuve; définir brièvement un terme au premier usage et ne questionner que si l'ambiguïté change matériellement le résultat.
7. Classer le risque `rapid | standard | critical` selon irréversibilité, blast radius, sécurité, données, production, coût externe, dépendances et difficulté de preuve, et attribuer `author_id` pressenti et `reviewer_id` indépendant si le run continuera vers build/review.
8. Qualifier `confidence` en `low | medium | high` à partir de la clarté du résultat, des preuves disponibles, de l'autorité, du write scope et des risques de domaine, sans inventer une précision numérique.
9. Avant toute question, rechercher les faits disponibles, puis présenter au plus trois choix (recommandation, meilleure alternative, statu quo) avec pour chacun coût, délai, complexité, risque, réversibilité, impact sur le graphe et preuve requise.
10. Poser une seule question matérielle par round, sous forme de carte de décision, qui retire le plus grand risque restant, sans jamais empiler des questions mineures.
11. Adapter le budget: Rapid peut passer sans arbitrage si les preuves suffisent, Standard autorise jusqu'à deux rounds utiles, Critical jusqu'à trois rounds et exige validation humaine des choix irréversibles ou sensibles.
12. Fail closed via `zero_assumption_gate` quand avancer demanderait d'inventer autorité, identité, dépôt, preuve, contrat public, sémantique métier ou comportement d'une interface existante.

## Sortie

Le skill rend `understanding` ([understanding-output.md](references/understanding-output.md)) avec les champs outcome, constraints, non_goals, evidence_required, unknowns, blind_spots, domain_model, confidence, zero_assumption_gate, project_compass, language_pack, risk_level, material_question, author_id, reviewer_id, repository, worktree, verdict.

## Arrêt et interdits

- Arrêter dès que le résultat et sa preuve sont assez précis pour router la suite.
- Rester evidence-first; ne pas planifier ni implémenter ici.
- Fail closed: ne pas inventer authority, identité, repository, preuve, invariant métier, contrat public ou comportement d'interface.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
