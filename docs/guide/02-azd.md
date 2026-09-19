# Router avec `/azd`

`/azd` est la porte d'entree. Vous lui donnez un objectif, il lit
`.azdone/trust.yaml`, classe la demande, choisit un playbook parmi huit, et
appelle les skills AZDone dans l'ordre du playbook.

## Ce qui se passe

```text
/azd "<objectif>"
   │
   ▼
lit .azdone/trust.yaml (absent -> propose /azd-setup, continue en assisted declare)
   │
   ▼
classe la demande : code-change | investigation | human-surface | release-ops | skill-mutation
   │
   ▼
choisit un playbook, copie ses etapes dans une liste de taches
   │
   ▼
appelle les skills, applique la politique de confiance a chaque action sensible
   │
   ▼
verdict + preuves + next_safe_action
```

## Donnez l'objectif, pas la ceremonie

Vous ne redigez pas une specification. Vous dites ce qui ne va pas, avec ce
que vous savez deja :

```text
/azd l'export ecrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

« Reproduis d'abord » est une contrainte reelle, pas une politesse : le
playbook correction de bug la respecte. Une etape sautee reste visible dans
la liste avec `skip: <raison>`.

## Les huit playbooks

| Playbook | Pour |
| --- | --- |
| `changement-code` | un changement de code ordinaire, du plan a la livraison |
| `correction-bug` | reproduire un defaut avant de le corriger |
| `investigation` | une question en lecture seule, aucune ecriture |
| `surface-humaine` | un changement qu'un utilisateur va voir ou toucher |
| `release` | pousser, ouvrir une PR, fusionner, deployer sous garde-fous |
| `run-autonome` | un travail long avec un predicat de sortie declare |
| `reprise-de-session` | reprendre un travail interrompu depuis la derniere preuve |
| `babysit-pr` | mener une PR jusqu'a mergeable : conflits, threads, CI |

## Sticky et opt-out

`/azd` reste actif d'un tour a l'autre une fois invoque. Dites simplement que
vous voulez sortir pour reprendre une conversation ordinaire.

## Toujours invocables seuls

Les seize skills existants restent utilisables directement, par exemple
`$prouver-resultat-azd`, sans passer par `/azd`. `/azd` les compose, il ne les
remplace pas. Voir la [reference des skills](../reference-skills.md).

Suivant : [Comprendre la confiance](03-confiance.md).
