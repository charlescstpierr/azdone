---
name: diagnostiquer-probleme-azd
description: "Diagnostiquer un problème en reproduisant l'échec, en isolant sa cause et en produisant un verdict sans corriger. Utiliser lorsqu'un bug, incident, test intermittent, échec incertain ou régression exige une preuve de cause racine avant toute remédiation."
---

# Étape 04 · Diagnostiquer le problème

Reproduire, isoler, prouver, puis s'arrêter au diagnostic. Reproduce, isolate, prove, then stop at diagnosis.

## Quick start

```text
$diagnostiquer-probleme-azd "Le test checkout_cache_flaky échoue parfois en CI"
```

Artefact attendu: `diagnosis.verdict: diagnose-only | blocked | failed`, reproduction minimale, hypothesis ledger et root cause soutenue.

## Utiliser quand / Use when

- un bug, incident, flaky test ou échec incertain existe;
- la cause n'est pas encore prouvée;
- une reproduction doit précéder toute correction.

## Procédure / Procedure

1. Reproduce the failure avec le plus petit cas utile: commande, seed/env, input, expected, actual, timestamp et artifact.
2. Create a reproducible `diagnosis_ledger`: chaque tentative garde command, exit/status, output digest et lien artifact.
3. Tenir un `hypothesis ledger` avec au moins deux hypothèses concurrentes quand possible: prediction, falsification test, evidence et status `open | falsified | supported | blocked`.
4. Isolate la root cause suspectée en changeant une variable à la fois; marquer explicitement les hypothèses falsifiées.
5. Obtenir de la fresh evidence pour chaque affirmation et séparer `author_evidence` de toute `reviewer_evidence`.
6. Séparer l'auteur du diagnostic et le reviewer éventuel; ne pas modifier le candidate code.
7. Lier la cause aux nœuds affectés du Project Decision Graph et identifier la première hypothèse invalidée sans modifier le code.
8. Rendre un verdict `diagnose-only`: reproduction, root cause prouvée ou cause la mieux soutenue, confiance, impact causal et blockers.

## Sortie / Output

- étapes de reproduction;
- `hypothesis ledger`;
- root cause ou meilleure explication soutenue;
- fresh evidence et verdict `diagnose-only`.

```yaml
diagnosis:
  author_id: ""
  reviewer_id: ""
  reproduction: []
  diagnosis_ledger:
    - command: ""
      environment: ""
      expected: ""
      actual: ""
      artifact: ""
  hypothesis_ledger: []
  author_evidence: []
  reviewer_evidence: []
  root_cause: ""
  invalidated_assumption: ""
  graph_impact: []
  confidence: low | medium | high
  evidence: []
  verdict: diagnose-only | blocked | failed
```

## Arrêt et interdits / Stop and forbidden

- Arrêter quand une cause est suffisamment prouvée pour être transférée à `$planifier-travail-azd` ou `$construire-solution-azd`, ou `blocked` si elle ne peut pas l'être.
- Ne pas corriger, refactorer ou planifier la remédiation dans ce skill.
- Ne pas produire de patch, fix-forward ou remediation steps; le transfert sortant est un paquet de diagnostic seulement.
- Fail closed si la reproduction est absente et que la cause n'est pas autrement prouvée.
- Fail closed si aucune hypothèse concurrente n'est falsifiée ou si l'auteur et le reviewer partagent la même evidence sans observation indépendante.
- Préserver les mêmes règles en Français and English.
