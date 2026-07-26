---
name: construire-solution-azd
description: "Construire le plus petit changement de code ou de contenu valide avec TDD strict, contrats publics exacts et preuves bornées. Utiliser lorsqu'un contrat accepté, un test rouge ou un plan approuvé est prêt à devenir un patch minimal sans compromettre sécurité, accessibilité, tests ou indépendance des évaluateurs."
---

# Étape 08 · Construire la solution

Construis le plus petit changement valide. Implement the smallest valid change. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$construire-solution-azd "Ajoute le champ JSON public-contract.json#/status sans renommer les tokens existants."`

Verdict attendu: test `red` capture l'absence du champ, patch minimal, test `green`, fichiers changes, risque residuel.

## Utiliser quand / Use when

Utilise ce skill quand le resultat est assez clair pour coder, qu'un failing test existe ou qu'un plan accepte doit devenir un patch minimal.

## Boucle / Loop

1. Confirmer que la carte est `Ready`, que son Proof Contract et son Readiness Forecast sont frais et que le Route Pack, Language Pack, ADR et contexte minimal sont résolus. Sinon retourner à la première gate manquante.
2. Pars du public seam, pas des internals.
3. RED: écris ou modifie d'abord un test qui échoue; enregistre commande, sortie, commit/worktree et raison de l'échec.
4. Si du code candidat précède le test, supprime-le ou isole-le hors candidate scope, puis repars du test rouge.
5. GREEN: implémente uniquement ce qui rend ce test vert.
6. REFACTOR: simplifie seulement après le vert, sans changer le comportement.
7. Rejoue le test et les checks natifs proportionnés; enregistre l'evidence `green`.
8. Pour une surface humaine, implémente chaque ligne de la `UI acceptance matrix`: états non nominaux, selectors/attributes publics exacts, clavier, live region, viewports et artefacts.
9. Ajoute un test qui échoue si un état requis existe seulement dans la prose ou le JavaScript sans représentation vérifiable.
10. Si l'exécution révèle un prérequis, une décision ou une idée hors carte, ne pas l'absorber: créer une carte `Draft` liée et poursuivre seulement si la carte active reste valide.
11. Si une preuve échoue, classer la première hypothèse invalidée (`readiness | understanding | diagnosis | design | plan | build`) et retourner à cette gate. Ne pas affaiblir le claim ni modifier l'oracle pour passer.
12. Arrête la tranche quand elle est verte et prouvée.

## Règles / Rules

- Use TDD and project-native patterns.
- Garde le `smallest valid change`.
- Applique Ponytail: supprimer avant d'ajouter, reutiliser avant d'inventer, refuser les abstractions sans complexite reelle.
- Preserve safety, accessibility, user changes and existing tests.
- Garde evaluator, reviewer, hidden oracle et protected regressions hors du write scope candidat.
- Si le besoin reste ambigu, retourne à `$clarifier-objectif-azd` ou `$concevoir-experience-azd`.
- Ne remplace jamais un token normatif par un synonyme: paths, schema fields, IDs, roles, attributes et viewport dimensions restent exacts.

## Sortie / Output

```yaml
build:
  card_id: ""
  readiness_forecast: fresh | stale | blocked
  proof_contract: locked | missing | stale
  author_id: ""
  worktree: ""
  write_scope: []
  red:
    command: ""
    evidence: ""
  green:
    command: ""
    evidence: ""
  refactor:
    command: ""
    evidence: ""
  changed_files: []
  protected_out_of_scope: []
  discovered_draft_cards: []
  causal_return: none | readiness | understanding | diagnosis | design | plan | build
  verdict: green | partial | blocked | failed
```

Stop when the assigned slice is green and no scoped failure remains. Sinon rends `partial`, `blocked` ou `failed` avec le blocker exact. Garde code, paths, commands and verdicts identical in Français and English.
