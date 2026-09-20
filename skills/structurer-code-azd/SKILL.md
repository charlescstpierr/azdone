---
name: structurer-code-azd
description: "Décider la structure du code avant d'écrire une ligne: formes de données, frontières, invariants et options comparées. Utiliser lorsqu'un changement traverse une frontière de module, ajoute de l'état ou une forme de donnée, ou laisse le choix entre plusieurs structures."
---

# Étape 06b · Structurer le code

Décider la structure du code avant d'écrire une ligne, formes de données d'abord.

## Quick start

```text
$structurer-code-azd "Le webhook Stripe et le webhook GitHub dupliquent la validation de signature. Choisis la structure avant le patch."
```

Artefact attendu: `structure.verdict: decided | question | blocked`, formes de données nommées, frontières tracées, options comparées, ADR et unités vérifiables.

## Utiliser quand

- lorsqu'un changement traverse une frontière de module, ajoute de l'état ou une forme de donnée, ou laisse le choix entre plusieurs structures;
- ne pas l'utiliser pour une correction locale d'une ligne ou un changement de docs seul. Aller directement à `$construire-solution-azd`.

## Procédure

1. Lire le contrat de résultat, le Language Pack (termes utiles à la carte active), les ADR existants, l'architecture détectée par `$inspecter-projet-azd` et `discovery.active_work.overlap`.
2. Nommer les formes de données (entités, identités, invariants, cycle de vie) et choisir leur organisation: machine à états plutôt que booléens dispersés, table ou registre plutôt que branches répétées, modèle typé plutôt qu'hypothèses de forme répétées.
3. Tracer les frontières: où on valide, où on fait confiance aux types, où vit la logique pure, et ce que partagent les acteurs concurrents avant de le sérialiser.
4. Rendre les états illégaux irreprésentables par les types, et marquer explicitement les opérations idempotentes.
5. Supprimer avant d'ajouter. Lister ce que la structure retenue permet de retirer.
6. Comparer deux ou trois structures candidates (recommandation, meilleure alternative, statu quo) avec coût, réversibilité, charge de lecture (couches, état caché), impact migration et preuve requise; poser au plus une question matérielle si une décision produit est en jeu, sinon décider.
7. Écrire la décision comme ADR à l'emplacement fixé par l'init, avec les invariants à tester et le plan de migration. Migrer les appelants puis supprimer l'ancien, en une vague.
8. Ordonner les unités vérifiables, chacune avec sa preuve; elles complètent le plan sans le rouvrir.
9. Transmettre sans perte à `$construire-solution-azd`: formes de données, frontières, invariants et ADR.

## Sortie

Le skill rend `structure` ([structure-output.md](references/structure-output.md)) avec les champs data_shapes, organizing_structures, boundaries, shared_state, invariants, idempotent_operations, removals, options, decision, adr_path, migration, verifiable_units, verdict.

## Arrêt et interdits

- Ne jamais écrire de code candidat ici; la sortie est une décision, pas un patch.
- Aucune abstraction n'est permise sans complexité réelle démontrée. Par défaut, supprimer avant d'ajouter reste la règle.
- Ne jamais garder un état de compatibilité jetable après la migration.
- Fail closed (`blocked`) si une forme de donnée reste `unknown` sur le chemin critique.
- Rapid: 0 sous-agent. Si délégué, suivre `skills/azd/references/context-packet.md` et `model-routing.md`.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
