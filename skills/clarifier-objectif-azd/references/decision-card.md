# Carte de décision matérielle

Utiliser cette référence seulement lorsqu’une inconnue change le résultat, le
risque, l’autorité ou une décision difficilement réversible.

## Structure

Présenter au plus trois options :

1. recommandation;
2. meilleure alternative crédible;
3. statu quo.

Pour chaque option, rendre explicites :

- résultat attendu;
- coût et délai;
- complexité;
- risque et blast radius;
- réversibilité;
- impact sur le Project Decision Graph;
- preuve qui permettrait de l’accepter ou de la rejeter.

Terminer par une seule question. Elle doit retirer le plus grand risque restant,
pas collecter plusieurs préférences mineures.

## Exemple court

```text
Décision: où conserver les pièces jointes?

A — Stockage objet géré (recommandé)
    + robuste et mesurable
    - compte et coût externe
    preuve: upload/download, permissions, suppression, limite de taille

B — Disque local
    + rapide pour un prototype
    - non portable et risqué en production
    preuve: reprise après redémarrage et politique de sauvegarde

C — Statu quo
    + aucun changement
    - le claim "pièces jointes" reste hors périmètre
    preuve: documentation explicite du non-objectif

Question: faut-il viser un prototype local ou une première release partageable?
```

