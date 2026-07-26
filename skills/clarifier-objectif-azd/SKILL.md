---
name: clarifier-objectif-azd
description: "Clarifier adaptativement tout résultat produit, backend, infrastructure, données, mobile, desktop, web, CLI, librairie, documentation, migration ou incident. Utiliser lorsque l'objectif est large, incomplet, sensible à l'autorité ou exige une question matérielle, un niveau de confiance, un zero-assumption gate ou un modèle de domaine léger avant d'agir."
---

# Étape 02 · Clarifier l’objectif

Rester domain-agnostic: produit, backend, infra, data, mobile, desktop, web, CLI et docs peuvent tous être la surface du résultat.

Transformer adaptativement la demande en petit contrat de résultat avant de planifier ou coder. Turn the request into a small adaptive outcome contract before planning or coding.

Rester domain-agnostic: appliquer le même cadrage à produit, backend, infra, data, mobile, desktop, web, CLI, librairie, docs, migration et incident.

## Quick start

```text
$clarifier-objectif-azd "Répare le flux de paiement sans casser les abonnements existants"
```

Artefact attendu: Boussole suffisamment fraîche, `risk_level`, `understanding.verdict`, `confidence`, `zero_assumption_gate`, Language Pack minimal et au plus une question matérielle.

## Utiliser quand / Use when

- l'objectif est large ou incomplet / the goal is broad or underspecified;
- une information manquante peut changer la voie, le risque ou l'autorité;
- les exigences cachées, non-objectifs ou critères d'acceptation comptent;
- le vocabulaire, les identités, entités, invariants, lifecycle ou exemples du domaine peuvent changer l'implémentation.

## Procédure / Procedure

1. Lire la Boussole créée par `$initialiser-projet-azd`; si elle manque ou est structurellement périmée, revenir à l'étape 00.
2. Reformuler le résultat dans la langue de l'utilisateur et accepter ses mots simples sans exiger son vocabulaire technique.
3. Séparer faits, hypothèses, contraintes et inconnues; marquer toute hypothèse non vérifiée comme `assumption`, jamais comme fait.
4. Fixer l'état final observable, la preuve attendue et la condition d'arrêt.
5. Compléter la Boussole: utilisateur, problème, succès, écosystèmes cibles, non-négociables, refus, non-objectifs et critères d'opportunité. Toute modification matérielle devient une décision versionnée.
6. Nommer les blind spots qui pourraient changer l'approche, y compris autorité, données sensibles, surface humaine, destruction, compatibilité, exploitation, distribution et contrats d'interface.
7. Construire un domain model léger quand le domaine compte: `vocabulary`, `identities`, `entities`, `invariants`, `lifecycle`, `examples`, `counterexamples`.
8. Produire un `Language Pack` borné à la carte: termes humains utilisés, termes métier, termes techniques utiles, éléments d'architecture touchés et moyens de preuve. Définir brièvement un terme au premier usage; questionner seulement si l'ambiguïté change matériellement le résultat.
9. Classer le risque `rapid | standard | critical` selon irréversibilité, blast radius, sécurité, données, production, coût externe, dépendances et difficulté de preuve.
10. Attribuer `author_id` pressenti et `reviewer_id` indépendant si le run continuera vers build/review.
11. Garder les blind spots séparés des `unknowns`: un `unknown` est une donnée manquante; un `blind_spot` est un angle oublié qui peut invalider l'approche même si une donnée locale semble suffisante.
12. Qualifier `confidence` en `low | medium | high` à partir de la clarté du résultat, des preuves disponibles, de l'autorité, du write scope et des risques de domaine. Ne pas inventer une précision numérique.
13. Avant toute question, rechercher les faits disponibles. Puis présenter au plus trois choix: recommandation, meilleure alternative et statu quo. Pour chacun: coût, délai, complexité, risque, réversibilité, impact sur le graphe et preuve requise.
14. Poser une seule question matérielle par round, sous forme de carte de décision. Elle doit retirer le plus grand risque restant. Ne jamais empiler des questions mineures.
15. Adapter le budget: Rapid peut passer sans arbitrage si les preuves suffisent; Standard autorise jusqu'à deux rounds utiles; Critical jusqu'à trois rounds et exige validation humaine des choix irréversibles ou sensibles.
16. Fail closed via `zero_assumption_gate` quand avancer demanderait d'inventer autorité, identité, dépôt, preuve, contrat public, sémantique métier ou comportement d'une interface existante.

## Sortie / Output

- `outcome contract`;
- `blind spots`;
- Boussole et changements proposés;
- `risk_level`;
- `language_pack`;
- `domain_model` léger;
- `confidence` et `zero_assumption_gate`;
- `author_id`, `reviewer_id`, `repository`, `worktree` si connus;
- one material question maximum per round avec trois directions maximum, ou verdict `proceed` / `blocked`.

```yaml
understanding:
  outcome: ""
  constraints: []
  non_goals: []
  evidence_required: []
  unknowns: []
  blind_spots: []
  domain_model:
    vocabulary: []
    identities: []
    entities: []
    invariants: []
    lifecycle: []
    examples: []
    counterexamples: []
  confidence: low | medium | high
  zero_assumption_gate:
    passed: false
    blockers: []
  project_compass:
    user: ""
    problem: ""
    success: []
    target_ecosystems: []
    non_negotiables: []
    refusals: []
    non_goals: []
    opportunity_criteria: []
    freshness: fresh | stale
  language_pack:
    human_terms: []
    business_terms: []
    technical_terms: []
    architecture_terms: []
    proof_terms: []
  risk_level: rapid | standard | critical
  material_question:
    round: 1
    question: ""
    risk_removed: ""
    options:
      - type: recommendation | best-alternative | status-quo
        tradeoffs: {cost: "", delay: "", complexity: "", risk: "", reversibility: "", graph_impact: "", proof: ""}
  author_id: ""
  reviewer_id: ""
  repository: ""
  worktree: ""
  verdict: proceed | blocked
```

## Arrêt et interdits / Stop and forbidden

- Arrêter dès que le résultat et sa preuve sont assez précis pour router la suite.
- Rester evidence-first; ne pas planifier ni implémenter ici.
- Fail closed: ne pas inventer authority, identité, repository, preuve, invariant métier, contrat public ou comportement d'interface.
- Conserver commandes, chemins, identifiants et règles de sécurité identiques en Français and English.
