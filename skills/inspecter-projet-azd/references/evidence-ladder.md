# Échelle de preuve et arrêt de recherche

Utiliser la source la plus proche du comportement réellement décidé.

## Ordre par défaut

1. état observable du dépôt et du runtime;
2. tests, contrats machine-readable et manifestes versionnés;
3. code source primaire ou documentation officielle de la version utilisée;
4. ADR, README et documentation locale;
5. mémoire repo-locale sourcée;
6. dépôts, articles ou signaux externes secondaires;
7. popularité, X ou Hacker News comme découverte seulement.

L’ordre peut changer si une source est stale, hors version ou contredite par un
contrat plus autoritatif. Enregistrer la contradiction au lieu de choisir
silencieusement le texte préféré.

## Condition d’arrêt

Arrêter lorsque la décision possède :

- un fait local ou une absence confirmée;
- la version ou fraîcheur pertinente;
- une source primaire si le comportement externe compte;
- le failure mode principal;
- une prochaine action qui ne dépend plus d’une recherche spéculative.

Continuer seulement si la nouvelle source peut changer le choix, le risque,
l’autorité ou le moyen de preuve.

