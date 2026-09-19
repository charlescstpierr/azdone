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

`tests/test_trust_policy.py` vérifie la sémantique de `.azdone/trust.yaml` :
les quatre niveaux, la table `actions:`, la liste `always_pause` non
contournable, la confiance gagnée (promotion après 5 runs `verified`
consécutifs, rétrogradation immédiate sur `failed` ou rollback), et le
comportement du hook `hooks/azd-trust-guard.sh` via des entrées JSON
fabriquées (`declared` laisse passer, `enforced` bloque une action `ask` ou
`never`, `always_pause` bloque même si `actions.*: auto`).

`tests/test_entry_mode.py` vérifie le skill `azd` : son frontmatter, ses huit
playbooks, la classification par capacité et par risque, et l’absence
d’autorité accordée par un texte de skill.

`tests/test_plugin_packaging.py` vérifie l’empaquetage : les deux manifestes
et `marketplace.json` sont du JSON valide, portent la même version, cohérente
avec `CHANGELOG.md`; `scripts/install.sh` est exécutable, ne supprime jamais
rien, et passe `bash -n`; le guide `docs/guide/` est complet et ses liens
relatifs résolvent; le README mentionne `/azd`, `/azd-setup` et `trust.yaml`.

## Ce que la CI prouve

`.github/workflows/tests.yml` s'exécute sur `push` et `pull_request`, sur
Python 3.11 et 3.12. Elle prouve que la suite publique passe sur les deux
versions ciblées, que `scripts/install.sh` et `hooks/azd-trust-guard.sh`
passent `bash -n`, que `hooks/azd-trust-guard.py` compile
(`py_compile`), et que les trois manifestes (`plugin.json` Claude Code,
`marketplace.json`, `plugin.json` Cursor) sont du JSON valide. Elle ne
prouve rien de plus : ni le comportement du hook sur un vrai hôte, ni
l'installation par un humain.

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

