### Prototype

**Trancher une question par la mesure. Le code est jetable, la mesure ne l'est pas.**

1. `$clarifier-objectif-azd` fixe la question exacte que le prototype doit trancher et le seuil de décision.
2. `$construire-solution-azd` écrit le plus petit code jetable dans un `write_scope` isolé (worktree dédié, jamais le scope livrable).
3. `$prouver-resultat-azd` exécute la mesure et rend le résultat brut, sans habillage.
4. Rapporter la mesure au playbook d'origine (`investigation.md` ou autre) qui a demandé le prototype. Le prototype ne se livre pas lui-même.

Prédicat de sortie : la question posée à l'étape 1 a une réponse mesurée, avec preuve fraîche.

Réponse : la question, la mesure, la décision qu'elle tranche, le retour au verdict d'investigation.

Interdits : aucun `$livrer-changement-azd`, aucune PR, aucune fusion du code jetable dans le scope livrable.
