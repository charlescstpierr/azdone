### Release

**Livrer, surveiller, ne jamais dépasser l'autorité déclarée.**

1. `$prouver-resultat-azd` confirme la preuve fonctionnelle et la readiness d'approbation.
2. `$reviser-qualite-azd` confirme la review indépendante requise par le risque.
3. `$livrer-changement-azd` intègre. `actions.push` et `actions.open_pr` gouvernent chaque écriture externe. `actions.merge` : `auto` livre, `conditional` vérifie CI verte et review acceptée avant de livrer, `ask` pose la question, `never` refuse.
4. `actions.deploy` de `.azdone/trust.yaml` gouverne tout déploiement selon la même logique.
5. `$surveiller-livraison-azd` observe la release et prépare le rollback.

Prédicat de sortie : la release est livrée avec un verdict honnête et une surveillance active, ou bloquée avec `next_safe_action` nommant l'autorité manquante.

Réponse : ce qui a été livré, le gate de `trust.yaml` appliqué, l'état de surveillance.
