# Recettes et pièges

Des prompts à copier, et des erreurs fréquentes à éviter.

## Recettes

```text
investigation :     /azd pourquoi le cache survit-il à la déconnexion ? aucune écriture.
correction de bug : /azd le compteur de notifications double après un retry. reproduis, corrige, prouve.
surface humaine :   /azd le formulaire perd les données au retour arrière. propose une correction visible.
release :           /azd la PR 88 est verte et relue. livre-la selon la politique actuelle.
run autonome :      /azd je pars pour la nuit. migre les appelants restants, arrête-toi quand le check est à zéro.
babysit :           /azd surveille la PR 123 jusqu'à mergeable. une relance CI maximum.
```

## Pièges

**N'énumérez pas les skills dans le prompt.** Écrire « utilise
inspecter-projet-azd puis construire-solution-azd » réordonne ou saute des
étapes que le playbook aurait gardées. Nommez un skill seulement pour forcer
un choix précis.

**Ne confondez pas `declared` et `enforced`.** Sous Codex, la politique guide
l'agent mais rien ne la fait respecter mécaniquement. Sous Claude Code et
Cursor, activez `enforcement: enforced` si vous voulez un hook qui bloque
réellement les commandes interdites.

**Ne retirez pas une entrée de `always_pause` en espérant qu'elle reste
retirée.** Le skill et le hook la réappliquent à chaque lecture de
`trust.yaml`.

**Une phrase comme « sois autonome » ne débloque pas les credentials ni les
suppressions de données.** Ces actions restent `ask` à tous les niveaux.

**Un test vert prouve un contrat, pas un projet réel.** La suite publique
vérifie noms, contrats et garde-fous. Le Pilot 0 sur un vrai projet humain
n'a pas encore été exécuté. Voir [Validation et limites des
preuves](../validation.md).

**Un skill invoqué seul reste valide.** Vous n'êtes jamais obligé de passer
par `/azd` ; les seize skills existants gardent leurs contrats et peuvent
être appelés directement.

Retour : [Le guide AZDone](README.md).
