### Release

**Livrer, surveiller, ne jamais dépasser l'autorité déclarée.**

1. `$prouver-resultat-azd` confirme la preuve fonctionnelle et la readiness d'approbation.
2. `$reviser-qualite-azd` confirme la review indépendante requise par le risque.
3. `$livrer-changement-azd` intègre. `actions.push` et `actions.open_pr` gouvernent chaque écriture externe. `actions.merge` : `auto` livre, `conditional` livre seulement si le témoin `.azdone/conditions-ok` est frais (CI verte, review acceptée, moins de 30 minutes), `ask` pose la question, `never` refuse.
4. `actions.deploy` de `.azdone/trust.yaml` gouverne tout déploiement selon la même logique.
5. `$surveiller-livraison-azd` observe la release (canary, production) et prépare le rollback ; `agents/azd-watcher.md` surveille directement CI et PR en amont, réveil par hôte (Claude Code et Cursor `/loop`, Codex par relance manuelle).

Prédicat de sortie : la release est livrée avec un verdict honnête, un témoin frais pour tout merge conditionnel, et une surveillance active, ou bloquée avec `next_safe_action` nommant l'autorité manquante.

Réponse : ce qui a été livré, le gate de `trust.yaml` appliqué, l'état de surveillance.
