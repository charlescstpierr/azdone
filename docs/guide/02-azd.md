# Router avec `/azd`

`/azd` est la porte d'entrée. Vous lui donnez un objectif, il lit
`.azdone/trust.yaml`, classe la demande, choisit un playbook parmi huit, et
appelle les skills AZDone dans l'ordre du playbook.

## Ce qui se passe

```text
/azd "<objectif>"
   │
   ▼
lit .azdone/trust.yaml (absent -> propose /azd-setup, continue en assisted déclaré)
   │
   ▼
classe la demande : code-change | investigation | human-surface | release-ops | skill-mutation
   │
   ▼
choisit un playbook, copie ses étapes dans une liste de tâches
   │
   ▼
appelle les skills, applique la politique de confiance à chaque action sensible
   │
   ▼
verdict + preuves + next_safe_action
```

## Donnez l'objectif, pas la cérémonie

Vous ne rédigez pas une spécification. Vous dites ce qui ne va pas, avec ce
que vous savez déjà :

```text
/azd l'export écrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

« Reproduis d'abord » est une contrainte réelle, pas une politesse : le
playbook correction de bug la respecte. Une étape sautée reste visible dans
la liste avec `skip: <raison>`.

## Les neuf playbooks

| Playbook | Pour |
| --- | --- |
| `changement-code` | un changement de code ordinaire, du plan à la livraison |
| `correction-bug` | reproduire un défaut avant de le corriger |
| `investigation` | une question en lecture seule, aucune écriture |
| `surface-humaine` | un changement qu'un utilisateur va voir ou toucher |
| `prototype` | code jetable en scope isolé pour trancher une question par la mesure |
| `release` | pousser, ouvrir une PR, fusionner, déployer sous garde-fous |
| `run-autonome` | un travail long avec un prédicat de sortie déclaré |
| `reprise-de-session` | reprendre un travail interrompu depuis la dernière preuve |
| `babysit-pr` | mener une PR jusqu'à mergeable : conflits, threads, CI |

`prototype` ne produit rien de livrable : il retourne un verdict
d'investigation et le résultat de la mesure, jamais un `verified` de
livraison.

## Sticky et opt-out

`/azd` reste actif d'un tour à l'autre une fois invoqué. Dites simplement que
vous voulez sortir pour reprendre une conversation ordinaire.

## Toujours invocables seuls

Les dix-sept skills existants restent utilisables directement, par exemple
`$prouver-resultat-azd`, sans passer par `/azd`. `/azd` les compose, il ne les
remplace pas. Voir la [référence des skills](../reference-skills.md).

Suivant : [Comprendre la confiance](03-confiance.md).
