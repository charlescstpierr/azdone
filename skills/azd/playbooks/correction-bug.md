### Correction de bug

**Reproduire avant de corriger. Aucune ligne ne ship sans preuve d'exécution.**

1. `$diagnostiquer-probleme-azd` reproduit le défaut et isole la cause. Ne pas patcher avant cette étape.
2. `$construire-solution-azd` écrit le plus petit correctif que la preuve justifie, avec un test rouge avant le correctif, toujours (TDD strict de `$construire-solution-azd`).
3. `$prouver-resultat-azd` (via `$verifier-application-azd executer` pour toute surface exécutable) rejoue la reproduction d'origine. Elle doit passer.
4. `$reviser-qualite-azd` fait relire le correctif par un agent indépendant.
5. `$livrer-changement-azd` intègre selon les gates `actions.commit`/`actions.push` de `.azdone/trust.yaml`.

Prédicat de sortie : la reproduction originale passe avec preuve fraîche, ou le run rend `blocked`/`failed` avec `next_safe_action`.

Réponse : ce qui était cassé, la cause racine, le correctif, la preuve d'exécution avant/après.
