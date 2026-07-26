# Contribuer à AZDone

Merci de contribuer par un changement petit, testable et traçable.

## Avant d’ouvrir une pull request

1. ouvrez ou liez une issue;
2. décrivez le problème observable, pas seulement la solution souhaitée;
3. bornez les skills et contrats touchés;
4. ajoutez ou adaptez un test de régression;
5. exécutez la suite publique;
6. documentez les limites et preuves manquantes.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Règles de conception

- Garder les skills ordinaires et indépendants.
- Préférer les instructions aux scripts.
- Ne pas ajouter runtime, daemon, base de données ou dépendance sans décision
  explicite.
- Conserver les tokens publics `<verbe>-<objet>-azd`.
- Préserver le français et l’anglais dans les surfaces publiques du skill.
- Séparer preuve locale, inférence et revendication comparative.
- Ne jamais modifier un oracle pour faire passer un candidat.
- Ajouter une référence seulement si elle réduit réellement le contexte du
  `SKILL.md`.

## Pull request

La description doit contenir :

- problème et résultat visé;
- fichiers et contrats touchés;
- preuve RED puis GREEN, si applicable;
- commandes exécutées et résultats;
- risques, compatibilité et rollback;
- ce qui reste `partial`, `blocked` ou non prouvé.

Les contributions de sécurité ne doivent pas passer par une issue publique.
Voir [SECURITY.md](SECURITY.md).

## Licence des contributions

Le projet n’a pas encore choisi sa licence stable. N’envoyez pas de contribution
substantielle avant que ce choix soit publié, sauf si vous acceptez qu’elle
reste en attente sans droit de redistribution implicite.

