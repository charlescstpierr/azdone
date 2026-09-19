# Comprendre et concevoir

Avant de coder, `/azd` clarifie l'inconnue qui compte et inspecte le depot.
Il ne conçoit une surface humaine que si l'utilisateur va vraiment la voir.

## Investigation pure

Une question en lecture seule ne declenche aucune ecriture :

```text
/azd pourquoi le webhook de paiement retente trois fois avant d'echouer ? aucune ecriture, je veux juste comprendre.
```

Le playbook `investigation` appelle `clarifier-objectif-azd` puis
`inspecter-projet-azd`, et parfois `diagnostiquer-probleme-azd` si une cause
reste ouverte. La reponse cite ses sources : fichiers, commandes, logs.

## Clarifier seulement ce qui change le resultat

`clarifier-objectif-azd` pose une question materielle a la fois, avec une
recommandation, la meilleure alternative et le statu quo. Il ne demande
jamais ce qu'une inspection peut observer elle-meme.

## Inspecter avant de juger

`inspecter-projet-azd` etablit les faits du depot : conventions existantes,
capacites disponibles, ecarts. Le diagnostic, la conception et le plan
s'appuient dessus, jamais sur une supposition.

## Concevoir seulement pour l'humain

```text
/azd le formulaire d'inscription perd les donnees saisies si l'utilisateur revient en arriere. propose une correction visible.
```

Le playbook `surface-humaine` ajoute `concevoir-experience-azd` a la route
normale : directions, prototype ou wireframe proportionne, decision
tracee. Un changement purement interne (refactor, migration de donnees sans
UI) ne passe jamais par cette etape.

## Ce que vous devriez observer

- une inconnue reelle declenche une question, pas une supposition silencieuse ;
- une reponse d'investigation ne modifie aucun fichier ;
- une conception reste absente quand rien de visible ne change ;
- chaque affirmation porte sa preuve ou son etiquette (observe, infere,
  suppose).

Suivant : [Construire, prouver, livrer](06-construire-prouver-livrer.md).
