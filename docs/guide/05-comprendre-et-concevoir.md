# Comprendre et concevoir

Avant de coder, `/azd` clarifie l'inconnue qui compte et inspecte le dépôt.
Il ne conçoit une surface humaine que si l'utilisateur va vraiment la voir.

## Investigation pure

Une question en lecture seule ne déclenche aucune écriture :

```text
/azd pourquoi le webhook de paiement retente trois fois avant d'échouer ? aucune écriture, je veux juste comprendre.
```

Le playbook `investigation` appelle `clarifier-objectif-azd` puis
`inspecter-projet-azd`, et parfois `diagnostiquer-probleme-azd` si une cause
reste ouverte. La réponse cite ses sources : fichiers, commandes, logs.

## Clarifier seulement ce qui change le résultat

`clarifier-objectif-azd` pose une question matérielle à la fois, avec une
recommandation, la meilleure alternative et le statu quo. Il ne demande
jamais ce qu'une inspection peut observer elle-même.

## Inspecter avant de juger

`inspecter-projet-azd` établit les faits du dépôt : conventions existantes,
capacités disponibles, écarts. Le diagnostic, la conception et le plan
s'appuient dessus, jamais sur une supposition.

## Concevoir seulement pour l'humain

```text
/azd le formulaire d'inscription perd les données saisies si l'utilisateur revient en arrière. propose une correction visible.
```

Le playbook `surface-humaine` ajoute `concevoir-experience-azd` à la route
normale : directions, prototype ou wireframe proportionné, décision
tracée. Un changement purement interne (refactor, migration de données sans
UI) ne passe jamais par cette étape.

## Ce que vous devriez observer

- une inconnue réelle déclenche une question, pas une supposition silencieuse ;
- une réponse d'investigation ne modifie aucun fichier ;
- une conception reste absente quand rien de visible ne change ;
- chaque affirmation porte sa preuve ou son étiquette (observé, inféré,
  supposé).

Suivant : [Construire, prouver, livrer](06-construire-prouver-livrer.md).
