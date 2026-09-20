# Le parcours AZDone

Un objectif humain devient un résultat vérifié en cinq temps. `/azd` et
`$piloter-workflow-azd` routent une demande à travers ces temps sans les
réordonner ni en sauter un sans le dire.

## Temps zéro. Cadrer

- `$clarifier-objectif-azd` fixe le contrat de résultat et les inconnues
  matérielles.
- `$inspecter-projet-azd` ancre la décision dans les preuves du dépôt et
  inventorie le travail actif des autres agents.
- `$diagnostiquer-probleme-azd` isole la cause racine quand un défaut est
  signalé, sans le corriger.
- `$planifier-travail-azd` verrouille le DAG, le Proof Contract et le
  Readiness Forecast.
- Gate de sortie : chaque carte candidate à `Ready` a un owner, une preuve
  prévue et un `next_safe_action` si un gap subsiste.

## Temps 1. Isoler

- `$isoler-travail-azd` ouvre une branche ou un worktree par tranche
  indépendante, avec évaluateur gelé.
- Gate de sortie : `author_id != reviewer_id`, overlap vérifié, checkpoint
  posé.

## Temps 2. Construire

- `$concevoir-experience-azd` fixe l'expérience d'une surface humaine avant
  le code, quand une décision humaine observable est en jeu.
- `$structurer-code-azd` décide la structure du code (formes de données,
  frontières, invariants, ADR), après le plan, avant construire, seulement
  lorsqu'un changement traverse une frontière de module, ajoute de l'état ou
  une forme de donnée, ou laisse le choix entre plusieurs structures.
- `$construire-solution-azd` écrit le plus petit changement valide en TDD
  strict.
- Gate de sortie : test rouge puis vert sur le changement, contrat public
  respecté au token près.

## Temps 3. Prouver

- `$prouver-resultat-azd` prouve chaque affirmation avec une preuve fraîche
  adaptée à la surface.
- `$verifier-application-azd` lance l'application réelle et l'exerce en
  isolation.
- `$reviser-qualite-azd` fait relire le changement par un reviewer
  indépendant de l'auteur.
- Gate de sortie : verdict `verified` ou `partial` documenté ; jamais un
  `failed` déclaré terminé.

## Temps 4. Livrer

- `$livrer-changement-azd` intègre le résultat accepté et prépare push, PR,
  merge ou déploiement sous autorité explicite.
- `$surveiller-livraison-azd` observe la production après une livraison
  autorisée.
- `$conserver-apprentissages-azd` capture ce qui est prouvé, jamais une
  anecdote promue en règle.
- Gate de sortie : livraison vérifiée sur le résultat intégré, apprentissage
  conservé ou explicitement écarté.

`$verifier-readiness-azd` et `$verifier-application-azd` sont transversaux :
chaque temps peut les appeler quand la readiness ou une preuve sur
l'application réelle le demande. `$ameliorer-workflow-azd` reste hors du
parcours normal ; il ne s'active que si des preuves répétées justifient une
mutation de skill.

## Sections à remplir pour ce dépôt

`initialiser-projet-azd` propose de copier cette section en `PARCOURS.md`
repo-local, puis de la compléter avec les faits observés de ce dépôt.

- **Commandes de test et de démarrage.** `<commande de test>`, `<commande de
  démarrage>`, `<commande d'arrêt>`.
- **Invariants.** `<ce qui ne doit jamais casser dans ce dépôt>`.
- **Environnement.** `<runtime, versions, variables non secrètes
  requises>`.
- **Surfaces.** `<web, api, cli, mobile, data ou autre, une ligne chacune>`.
- **Ce qui exige un humain.** `<actions jamais automatiques dans ce
  dépôt>`.
