# Construire, prouver, livrer

Une fois le probleme clarifie, `/azd` construit le plus petit changement
valide, le prouve, le fait relire, puis le livre sous la politique de
confiance active.

## Un exemple de bout en bout

```text
/azd l'export ecrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Le playbook `correction-bug` route : `diagnostiquer-probleme-azd` reproduit
le defaut avant tout patch. Puis `construire-solution-azd` ecrit un test qui
echoue, corrige au minimum, fait passer le test. `prouver-resultat-azd`
verifie chaque claim avec une preuve fraiche. `reviser-qualite-azd` fait
relire par un agent distinct de l'auteur. `livrer-changement-azd` integre ou
publie selon `trust.yaml`.

## Construire

`construire-solution-azd` boucle RED, GREEN, REFACTOR, et n'ecrit que dans le
`write_scope` accorde. Il rend `changed_files`, l'etat rouge, l'etat vert, un
verdict.

## Prouver

`prouver-resultat-azd` rend une matrice `claim | status | evidence |
freshness`. Un verdict `verified` exige une preuve fraiche pour chaque claim
requis ; un `partial` ou un `blocked` porte toujours un `next_safe_action`.

## Reviser

`reviser-qualite-azd` est independant : `author_id != reviewer_id`. Il rend
des `findings[]` a identifiants stables et un verdict `accept` ou
`return-to-build`.

## Livrer

`livrer-changement-azd` verifie `trust.yaml` avant chaque action externe :
`push` et `open_pr` sont `auto` en `autonomous`, `merge` est `conditional`
(CI verte et review acceptee requises), `deploy` reste `ask` sauf en `full`.

```text
/azd la PR 88 est verte et relue. livre-la selon la politique actuelle.
```

Le playbook `release` applique les gates dans cet ordre : prouver, reviser,
livrer, puis surveiller si une release existe.

Suivant : [Lancer un run autonome](07-run-autonome.md).
