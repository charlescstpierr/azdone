# Le guide AZDone

AZDone route une demande a travers seize skills ordinaires, sans runtime ni
service. `/azd` lit votre objectif, choisit un playbook, applique la politique
de confiance de `.azdone/trust.yaml`, et rend un verdict honnete. Ce guide
enseigne cette habitude avec des prompts reels.

Ce que vous allez apprendre :

1. [Installer AZDone](01-installation.md). Trois hotes, un script, ou le
   plugin.
2. [Router avec `/azd`](02-azd.md). Donnez un objectif, regardez le playbook
   se choisir.
3. [Comprendre la confiance](03-confiance.md). Les quatre niveaux, la liste
   toujours-pause, la confiance gagnee.
4. [Modeles et sous-agents](04-modeles-et-sous-agents.md). Cinq roles, un
   hote natif ou un adaptateur CLI par role.
5. [Comprendre et concevoir](05-comprendre-et-concevoir.md). Clarifier et
   inspecter avant de coder, concevoir seulement si l'humain voit un
   changement.
6. [Construire, prouver, livrer](06-construire-prouver-livrer.md). Le
   changement minimal, la preuve, la revue, la livraison.
7. [Lancer un run autonome](07-run-autonome.md). Un predicat de sortie
   declare, un journal, jamais de relachement silencieux.
8. [Recettes et pieges](08-recettes-et-pieges.md). Des prompts a copier et
   des erreurs a eviter.

Lisez les pages dans l'ordre la premiere fois. Ensuite, chacune se suffit a
elle-meme.

## Si vous ne retenez qu'une chose

Donnez a l'agent un objectif et une facon de verifier, dans vos mots :

```text
/azd l'export ecrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Vous n'avez pas besoin de nommer un playbook ni de lister des skills.
« reproduis d'abord » et un resultat verifiable suffisent comme signal de
routage. `/azd` choisit le playbook correction de bug, copie ses etapes dans
une liste de taches, et appelle les bons skills a chaque etape.

Suivant : [Installer AZDone](01-installation.md).
