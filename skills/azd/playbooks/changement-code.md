### Changement de code

**Le pilote possède la livraison. Composer, construire, prouver, livrer.**

1. `$clarifier-objectif-azd` fixe le résultat, le risque et la question matérielle éventuelle.
2. `$inspecter-projet-azd` rassemble les faits du dépôt avant tout plan.
3. `$planifier-travail-azd` ordonne cartes, dépendances et Proof Contract.
4. `$construire-solution-azd` implémente la plus petite solution valide dans le write scope accepté.
5. `$prouver-resultat-azd` sépare preuve fonctionnelle et readiness d'approbation.
6. `$reviser-qualite-azd` lance une review indépendante (`author_id != reviewer_id`).
7. `$livrer-changement-azd` intègre selon `.azdone/trust.yaml` : `actions.commit` et `actions.push` gouvernent chaque écriture.

Prédicat de sortie : verdict `verified` avec preuve fraîche pour chaque claim, ou `partial`/`blocked` avec `next_safe_action`.

Réponse : ce qui a changé, la preuve, la review, le verdict et la prochaine action sûre.
