---
name: construire-solution-azd
description: "Construire le plus petit changement de code ou de contenu valide avec TDD strict, contrats publics exacts et preuves bornées. Utiliser lorsqu'un contrat accepté, un test rouge ou un plan approuvé est prêt à devenir un patch minimal sans compromettre sécurité, accessibilité, tests ou indépendance des évaluateurs."
---

# Étape 08 · Construire la solution

Construire le plus petit changement valide (`smallest valid change`) avec TDD strict.

## Quick start

Invocation: `$construire-solution-azd "Ajoute le champ JSON public-contract.json#/status sans renommer les tokens existants."`

Verdict attendu: test `red` capture l'absence du champ, patch minimal, test `green`, fichiers changés, risque résiduel.

## Utiliser quand

- Un contrat public est accepté et un test rouge ou un plan approuvé existe.
- Le résultat attendu est assez clair pour coder directement.
- Une carte est `Ready` avec Proof Contract et Readiness Forecast frais.

## Procédure

1. Vérifier que la carte est `Ready`, que Proof Contract et Readiness Forecast sont frais, et que Route Pack, Language Pack, ADR et contexte minimal sont résolus, et l'ADR de structure quand `$structurer-code-azd` a tourné, sinon retourner à la première gate manquante.
2. Partir du seam public, pas des internals.
3. RED : écrire ou modifier d'abord un test qui échoue ; si du code candidat le précède, supprime-le ou isole-le hors candidate scope puis repartir du test rouge, et enregistrer commande, sortie, commit/worktree et raison de l'échec.
4. GREEN : implémenter uniquement ce qui rend ce test vert.
5. REFACTOR : simplifier seulement après le vert sans changer le comportement, puis rejouer test et checks natifs proportionnés et enregistrer l'evidence `green`.
6. Pour une surface humaine, implémenter chaque ligne de la `UI acceptance matrix` (états non nominaux, selectors/attributes publics exacts, clavier, live region, viewports, artefacts) et ajouter un test qui échoue si un état requis n'existe que dans la prose ou le JavaScript.
7. Pour une surface `docs`, le gate rouge est un lien cassé, un exemple non exécutable ou une assertion de contenu manquante détectée par un check existant du dépôt ; sans check possible, sauter RED/GREEN et le dire dans le verdict.
8. Si délégué à un sous-agent, suivre `skills/azd/references/context-packet.md` et `model-routing.md` pour le rôle correspondant.
9. Si l'exécution révèle un prérequis, une décision ou une idée hors carte, créer une carte `Draft` liée sans l'absorber, et poursuivre seulement si la carte active reste valide.
10. Si une preuve échoue, classer la première hypothèse invalidée (`readiness | understanding | diagnosis | design | plan | build`) et retourner à cette gate, sans affaiblir le claim ni modifier l'oracle.
11. Arrêter la tranche quand elle est verte et prouvée.

## Sortie

Le skill rend `build` ([build-output.md](references/build-output.md)) avec les champs card_id, readiness_forecast, proof_contract, author_id, worktree, write_scope, red, green, refactor, changed_files, protected_out_of_scope, discovered_draft_cards, causal_return, verdict.

## Arrêt et interdits

- Ne jamais écrire de code candidat avant un test rouge (TDD strict).
- Garder le `smallest valid change` ; suivre les patterns project-native et appliquer Ponytail : supprimer avant d'ajouter, réutiliser avant d'inventer, refuser les abstractions sans complexité réelle.
- Préserver safety, accessibility, les changements utilisateur et les tests existants.
- Garder evaluator, reviewer, hidden oracle et protected regressions hors du write scope candidat.
- Si le besoin reste ambigu, retourner à `$clarifier-objectif-azd` ou `$concevoir-experience-azd`.
- Rapid : 0 sous-agent sauf justification écrite.
- Ne jamais remplacer un token normatif par un synonyme : paths, schema fields, IDs, roles, attributes et dimensions de viewport restent exacts.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
