# AZDone

AZDone est un workflow de réalisation composé de **16 Agent Skills ordinaires**.
Il aide un agent et un humain à transformer une idée, un changement ou un
incident en résultat clarifié, construit, prouvé, révisé et livré.

[English overview](README.en.md)

## Statut

**Aperçu public, skill-only.**

- Aucun runtime AZDone, daemon, dashboard ou service propriétaire.
- Aucun besoin d’OMX pour utiliser les skills.
- L’état du projet reste dans le dépôt utilisateur.
- Les 16 dossiers passent les contrôles structurels et la suite de contrats
  locale.
- Le Pilot 0 sur un vrai projet humain n’a pas encore été exécuté.
- AZDone ne revendique ni supériorité générale ni approbation Apple, Google,
  Microsoft, OpenAI ou Anthropic.

## Démarrage rapide avec Codex

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd votre-projet
mkdir -p .agents/skills
cp -R ../azdone/skills/. .agents/skills/
```

Redémarrez Codex si les skills n’apparaissent pas, puis invoquez une seule fois :

```text
$initialiser-projet-azd
```

Ensuite, donnez votre objectif au pilote :

```text
$piloter-workflow-azd "Construis un SaaS qui permet à une petite équipe de suivre ses demandes clients."
```

Codex documente officiellement les skills de dépôt sous
`.agents/skills`. Claude Code accepte les skills de projet sous
`.claude/skills`; voir le [guide d’installation](docs/installation.md) pour les
deux hôtes et leurs limites actuelles.

## Ce que le workflow fait

```text
00 Init une fois
   │
   ▼
01 Piloter
   ├─ 02 Clarifier
   ├─ 03 Inspecter
   ├─ 04 Diagnostiquer, si la cause est inconnue
   ├─ 05 Concevoir, si une surface humaine change
   ├─ 06 Planifier
   ├─ 07 Isoler, si des lanes indépendantes le justifient
   ├─ 08 Construire
   ├─ 09 Prouver
   ├─ 10 Réviser
   ├─ 11 Livrer
   ├─ 12 Surveiller, si une release existe
   ├─ 13 Conserver les apprentissages
   └─ 14 Améliorer, seulement après des signaux répétés

Socle transversal : verifier-readiness-azd
```

Le pilote ne force pas toutes les étapes. Il choisit le plus petit parcours
adapté au risque, aux inconnues, à la surface touchée et aux preuves nécessaires.

## Pourquoi AZDone

- Une question matérielle à la fois pendant le grilling.
- Une recommandation, une alternative et le statu quo avec leurs trade-offs.
- Un langage partagé entre l’humain, le métier, la technique et la preuve.
- Un preflight qui révèle tôt outils, comptes, accès, données et moyens de test.
- Des cartes liées par un Project Decision Graph au lieu d’une liste plate.
- Des subagents seulement lorsque le travail est réellement indépendant.
- Une séparation stricte entre fait observé, inférence, décision et preuve.
- Des verdicts honnêtes : `verified`, `partial`, `blocked` ou `failed`.

## Documentation

- [Premier projet](docs/demarrage-rapide.md)
- [Installation, mise à jour et désinstallation](docs/installation.md)
- [Architecture du workflow](docs/architecture.md)
- [Référence des 16 skills](docs/reference-skills.md)
- [Validation et limites des preuves](docs/validation.md)
- [Fonctionnement détaillé](HOW_IT_WORKS.md)
- [Contribuer](CONTRIBUTING.md)
- [Sécurité](SECURITY.md)
- [Support](SUPPORT.md)
- [Historique des versions](CHANGELOG.md)

## Vérifier le package

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

La suite publique vérifie les noms, déclencheurs, contrats, garde-fous,
références et l’absence de runtime dans les skills. Elle ne prouve pas à elle
seule le comportement d’un agent sur un projet réel.

## Licence

Aucune licence de réutilisation n’est encore sélectionnée. Le dépôt public est
un aperçu auditable, mais **public ne signifie pas encore open source**. Le choix
MIT, Apache-2.0 ou autre doit être fait explicitement avant une version stable.
