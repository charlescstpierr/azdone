# Validation et limites des preuves

AZDone distingue la validité du package, la conformité des contrats et la
preuve sur un projet réel.

## Ce que la suite publique prouve

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Elle vérifie notamment :

- 16 dossiers de skills et leurs métadonnées;
- descriptions avec déclencheurs explicites;
- quick starts et prompts publics;
- références locales résolues;
- routage domain-agnostic;
- diagnostic sans patch;
- design conditionnel;
- readiness, reprise, progression et preuve;
- review indépendante;
- aucun script/runtime dans `skills/`.

## Ce que la validation structurelle prouve

Chaque dossier a aussi été passé dans le validateur officiel utilisé par
`skill-creator`. Cela prouve la forme du skill, pas son comportement futur sur
tous les hosts.

## Ce que les benchmarks internes ont observé

Le dépôt de construction interne possède des fixtures et oracles fail-closed,
ainsi que des campagnes comparatives bornées. Ces archives brutes ne sont pas
publiées dans ce dépôt parce qu’elles contiennent des chemins de machine, des
logs de host et des copies de sorties tierces.

Les résultats antérieurs restent des signaux locaux :

- B1–B3 : campagnes skill-layer synthétiques;
- B4 : pilote intégré synthétique `n=1`;
- rescores immuables séparés des résultats originaux;
- aucune conclusion de supériorité mondiale.

## Ce qui reste non prouvé

- installation propre par un nouvel utilisateur sans aide;
- projet réel conduit par l’humain de bout en bout;
- comportement équivalent sur Codex et Claude Code;
- qualité production sur site, SaaS, logiciel desktop, mobile ou Telegram;
- approbation par une plateforme externe;
- reprise longitudinale après plusieurs semaines;
- auto-amélioration complète sur une vraie mutation;
- efficacité ou supériorité générale face aux références.

## Règle de communication

Un test vert autorise :

> Le contrat testé passe dans cet environnement.

Il n’autorise pas :

> Le workflow réussira n’importe quel projet.

Le Pilot 0 est la prochaine preuve d’intégration principale.

