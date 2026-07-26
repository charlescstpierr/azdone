---
name: reviser-qualite-azd
description: "Réviser indépendamment la conformité au contrat, la correction, la sécurité, le design, la qualité des preuves et la simplicité en deux étapes. Utiliser lorsqu'un changement borné exige un réviseur distinct de l'auteur avant acceptation, retour à la construction ou livraison."
---

# Étape 10 · Réviser la qualité

Relis independamment, puis accepte ou retourne a build. Review independently, then accept or return to build. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$reviser-qualite-azd "Révise le diff de construction contre le contrat public et les preuves fraîches."`

Verdict attendu: findings ranked/actionable, `author_id != reviewer_id`, decision `accept`, `return-to-build`, `blocked` ou `failed`.

## Utiliser quand / Use when

Utilise ce skill quand un changement doit recevoir un second regard independant avant acceptation ou livraison.

## Pipeline / Review pipeline

1. Lire `risk_level`. Rapid peut utiliser un seul reviewer ciblé; Standard couvre contrat puis qualité; Critical exige indépendance forte, surfaces sécurité/architecture/preuve et interdit toute auto-approbation.
2. Stage 0 `planted-defect protocol`: avant de lire la conclusion auteur, choisir au moins un defect class plausible: logic, contract, security, test gap ou evidence drift.
3. Stage 1 `contract/spec compliance`: un reviewer indépendant refait le `contract-completeness pass`.
4. Stage 2 `quality/correctness/security/simplicity`: le reviewer vérifie correctness, security, design fit, accessibility, evidence freshness, Ponytail discipline et project-native reuse.
5. Vérifie `author_id != reviewer_id`, diff limité au scope accepté, evaluator hors write scope et absence de cleanup ambigu.
6. Rends des findings `ranked` et actionable avec stable finding IDs comme `SEC-01`, `TEST-02` et `ARCH-03`.
7. Réception: l'auteur accuse réception de chaque finding, corrige le plus petit scope nécessaire ou rejette avec preuve explicite.
8. Re-review: le reviewer valide chaque correction/rejet avec preuve indépendante.
9. Pour un échec, indiquer la première gate invalidée; `return-to-build` seulement si la cause est réellement dans l'implémentation.

## Sortie / Output

```yaml
review:
  risk_level: rapid | standard | critical
  reviewer_id: ""
  author_id: ""
  base_commit: ""
  changed_files: []
  planted_defect_protocol:
    defect_class: logic | contract | security | test-gap | evidence-drift
    attempted: true | false
    result: found | not-found | blocked
  author_evidence: []
  reviewer_evidence: []
  stage_1_contract_spec: pass | fail | blocked
  stage_2_quality_correctness_security_simplicity: pass | fail | blocked
  findings:
    - id: ""
      severity: critical | high | medium | low
      file: ""
      line_or_selector: ""
      evidence: ""
      impact: ""
      action: ""
      correction_status: open | fixed | rejected
      reviewer_verdict: pending | accepted | rejected
  causal_return: readiness | understanding | diagnosis | design | plan | build | none
  verdict: accept | return-to-build | blocked | failed
```

## Arrêt et interdits / Stop and forbidden

- Arrete quand chaque finding possede preuve, impact et action minimale.
- Reste independent de l'implementation lane; ne corrige pas silencieusement pendant la review.
- Utilise un ou plusieurs reviewers distincts de l'auteur; un auteur ne peut pas accepter ses propres corrections.
- Stable finding IDs must survive fix/re-review loops; never renumber open findings after corrections.
- `reviewer_evidence` must be freshly observed and distinct from `author_evidence`, not a copy of the author's claim.
- Prefere le plus petit correctif bloquant qui protege le resultat.
- Fail closed si reviewer et author sont identiques, si l'evidence est stale, ou si le reviewer doit ecrire dans le candidate scope.
- Garde decisions et rules identical in Français and English.
