# Recettes et pieges

Des prompts a copier, et des erreurs frequentes a eviter.

## Recettes

```text
investigation :     /azd pourquoi le cache survit-il a la deconnexion ? aucune ecriture.
correction de bug : /azd le compteur de notifications double apres un retry. reproduis, corrige, prouve.
surface humaine :   /azd le formulaire perd les donnees au retour arriere. propose une correction visible.
release :           /azd la PR 88 est verte et relue. livre-la selon la politique actuelle.
run autonome :      /azd je pars pour la nuit. migre les appelants restants, arrete-toi quand le check est a zero.
babysit :           /azd surveille la PR 123 jusqu'a mergeable. une relance CI maximum.
```

## Pieges

**N'enumerez pas les skills dans le prompt.** Ecrire « utilise
inspecter-projet-azd puis construire-solution-azd » reordonne ou saute des
etapes que le playbook aurait gardees. Nommez un skill seulement pour forcer
un choix precis.

**Ne confondez pas `declared` et `enforced`.** Sous Codex, la politique guide
l'agent mais rien ne la fait respecter mecaniquement. Sous Claude Code et
Cursor, activez `enforcement: enforced` si vous voulez un hook qui bloque
reellement les commandes interdites.

**Ne retirez pas une entree de `always_pause` en esperant qu'elle reste
retiree.** Le skill et le hook la reappliquent a chaque lecture de
`trust.yaml`.

**Une phrase comme « sois autonome » ne debloque pas les credentials ni les
suppressions de donnees.** Ces actions restent `ask` a tous les niveaux.

**Un test vert prouve un contrat, pas un projet reel.** La suite publique
verifie noms, contrats et garde-fous. Le Pilot 0 sur un vrai projet humain
n'a pas encore ete execute. Voir [Validation et limites des
preuves](../validation.md).

**Un skill invoque seul reste valide.** Vous n'etes jamais oblige de passer
par `/azd` ; les seize skills existants gardent leurs contrats et peuvent
etre appeles directement.

Retour : [Le guide AZDone](README.md).
