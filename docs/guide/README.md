# Le guide AZDone

AZDone route une demande à travers dix-sept skills ordinaires, sans runtime ni
service. `/azd` lit votre objectif, choisit un playbook, applique la politique
de confiance de `.azdone/trust.yaml`, et rend un verdict honnête. Ce guide
enseigne cette habitude avec des prompts réels.

Ce que vous allez apprendre :

1. [Installer AZDone](01-installation.md). Trois hôtes, un script, ou le
   plugin.
2. [Router avec `/azd`](02-azd.md). Donnez un objectif, regardez le playbook
   se choisir.
3. [Comprendre la confiance](03-confiance.md). Les quatre niveaux, la liste
   toujours-pause, la confiance gagnée.
4. [Modèles et sous-agents](04-modeles-et-sous-agents.md). Cinq rôles, un
   hôte natif ou un adaptateur CLI par rôle.
5. [Comprendre et concevoir](05-comprendre-et-concevoir.md). Clarifier et
   inspecter avant de coder, concevoir seulement si l'humain voit un
   changement.
6. [Construire, prouver, livrer](06-construire-prouver-livrer.md). Le
   changement minimal, la preuve, la revue, la livraison.
7. [Lancer un run autonome](07-run-autonome.md). Un prédicat de sortie
   déclaré, un journal, jamais de relâchement silencieux.
8. [Recettes et pièges](08-recettes-et-pieges.md). Des prompts à copier et
   des erreurs à éviter.

Lisez les pages dans l'ordre la première fois. Ensuite, chacune se suffit à
elle-même.

## Si vous ne retenez qu'une chose

Donnez à l'agent un objectif et une façon de vérifier, dans vos mots :

```text
/azd l'export écrit des lignes en double quand un retry tombe en plein run. Reproduis d'abord, puis corrige et prouve.
```

Vous n'avez pas besoin de nommer un playbook ni de lister des skills.
« reproduis d'abord » et un résultat vérifiable suffisent comme signal de
routage. `/azd` choisit le playbook correction de bug, copie ses étapes dans
une liste de tâches, et appelle les bons skills à chaque étape.

Suivant : [Installer AZDone](01-installation.md).
