# Contrat de bootstrap AZDone

## Installation et initialisation

L'installation rend les skills AZDone disponibles. L'initialisation se déroule
une seule fois lors de la première entrée dans le dépôt et fixe leurs conventions
communes. Ne jamais confondre la présence des skills avec une initialisation
réussie.

Si une preuve d'initialisation existe déjà, rendre `already-initialized` sans
écriture. Une modification ultérieure passe par une carte de migration, jamais
par une réinitialisation silencieuse.

## Artefacts logiques requis

| Artefact | Rôle | Autorité |
| --- | --- | --- |
| Constitution AZDone | règles communes courtes et pointeurs repo-locaux | humain pour les changements matériels |
| Boussole | résultat, utilisateur, succès, contraintes et refus | humain pour les décisions matérielles |
| Atlas universel | vocabulaire commun AZDone | core AZDone, extensible localement |
| Lexique métier | mots propres au projet | projet |
| Lexique technique | architecture et domaine ciblés | preuves locales et sources primaires |
| Language Bridge | traduction humain, métier, technique, preuve | projet |
| System Success Map | couverture produit, technique, opérationnelle, commerciale | projet |
| Project Decision Graph | liens entre objectifs, décisions, tickets, risques et preuves | projet |
| Route Pack | pointeurs de contexte utiles | aucune autorité d'action |
| Readiness Forecast | prérequis et moyens de preuve | recalculé quand invalidé |
| Checkpoint | reprise exacte et fraîche | projet |

Le fichier de contrôle agent contient la Constitution AZDone sous forme d'un
bloc court et de pointeurs. Les
détails vivent dans des fichiers repo-locaux éditables par l'humain. Les autres
skills parlent en termes abstraits comme `backlog`, `Boussole`, `glossaire`,
`ADR`, `preuve` ou `readiness`, puis résolvent ces termes via les pointeurs du
setup au lieu de coder des chemins en dur.

Les chemins physiques suivent les conventions du dépôt. Le défaut `.azdone/`
n'est autorisé que si aucun emplacement plus naturel n'existe.

Le skill set peut être installé globalement, mais son état n'est jamais global:
Boussole, cartes, ADR, graphe, forecasts, preuves et checkpoints appartiennent
au dépôt. Pour un projet Standard ou Critical comportant plusieurs inconnues
indépendantes, un Bootstrap Council borné peut inspecter architecture, risques,
preuve et opportunités. Il reste optionnel et son staffing dépend du scope
utile, du risque et de l'indépendance, jamais du nombre de fichiers.

## Questions de grilling

Avant chaque question, montrer les faits déjà établis. Pour une décision
matérielle, proposer au plus trois choix:

1. recommandation;
2. meilleure alternative;
3. statu quo.

Pour chaque choix, exposer les trade-offs: coût, délai, complexité, risque,
réversibilité, impact sur le graphe et preuve nécessaire. Poser une seule
question par tour.

## Fraîcheur

Une modification de Boussole, architecture, environnement, dépendance,
écosystème cible, autorité, oracle ou contrat public invalide les artefacts
descendants concernés. Les skills courants marquent `stale` et recalculent les
artefacts affectés sans relancer l'init ni réécrire silencieusement une
convention approuvée.

## Gate de sortie

`ready-for-workflow` exige:

- backlog, cycle des cartes et labels résolus;
- Constitution dans un fichier de contrôle unique et pointeurs résolus;
- conventions Git, risque et autorité;
- emplacements du langage, des ADR, de la Boussole, du graphe et des preuves;
- amorces minimales sans fausse complétude;
- premier préflight global exécuté;
- aucune autorité critique inventée.
