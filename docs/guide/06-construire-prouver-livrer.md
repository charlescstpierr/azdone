# Construire, prouver, livrer

Une fois le problème clarifié, `/azd` construit le plus petit changement
valide, le prouve, le fait relire, puis le livre sous la politique de
confiance active.

## Un exemple de bout en bout

```text
/azd l'export écrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Le playbook `correction-bug` route : `diagnostiquer-probleme-azd` reproduit
le défaut avant tout patch. Puis `construire-solution-azd` écrit un test qui
échoue, corrige au minimum, fait passer le test. `prouver-resultat-azd`
vérifie chaque claim avec une preuve fraîche. `reviser-qualite-azd` fait
relire par un agent distinct de l'auteur. `livrer-changement-azd` intègre ou
publie selon `trust.yaml`.

## Structurer le code

`structurer-code-azd` intervient après le plan, avant construire, seulement
lorsqu'un changement traverse une frontière de module, ajoute de l'état ou
une forme de donnée, ou laisse le choix entre plusieurs structures. Il
compare les options candidates et écrit la décision retenue comme ADR, avec
les unités vérifiables qui complètent le plan sans le rouvrir.

```text
$structurer-code-azd "Le webhook Stripe et le webhook GitHub dupliquent la validation de signature. Choisis la structure avant le patch."
```

## Construire

`construire-solution-azd` boucle RED, GREEN, REFACTOR, et n'écrit que dans le
`write_scope` accordé. Il rend `changed_files`, l'état rouge, l'état vert, un
verdict.

## Prouver

`prouver-resultat-azd` rend une matrice `claim | status | evidence |
freshness`. Un verdict `verified` exige une preuve fraîche pour chaque claim
requis ; un `partial` ou un `blocked` porte toujours un `next_safe_action`.

## Vérifier l'application réelle

`initialiser-projet-azd` génère une fois le skill repo-local
`verifier-<app>` ; `prouver-resultat-azd` l'exécute (`$verifier-application-azd
executer`) pour tout claim sur une surface exécutable, jamais contre la
production, un compte réel ou des credentials. Une observation impossible
rend `blocked`, jamais `verified` : « inconclusive » n'est pas un succès.

```text
$verifier-application-azd executer "export CSV, filtre par date, erreur sur date invalide"
```

## Réviser

`reviser-qualite-azd` est indépendant : `author_id != reviewer_id`. Il rend
des `findings[]` à identifiants stables et un verdict `accept` ou
`return-to-build`.

## Livrer

`livrer-changement-azd` vérifie `trust.yaml` avant chaque action externe :
`push` et `open_pr` sont `auto` en `autonomous`, `merge` est `conditional`
(CI verte et review acceptée requises), `deploy` reste `ask` sauf en `full`.

```text
/azd la PR 88 est verte et relue. livre-la selon la politique actuelle.
```

Le playbook `release` applique les gates dans cet ordre : prouver, réviser,
livrer, puis surveiller si une release existe.

Suivant : [Lancer un run autonome](07-run-autonome.md).
