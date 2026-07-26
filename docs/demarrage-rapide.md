# Premier projet avec AZDone

Ce tutoriel part d’un dépôt Git existant et mène à la première carte de travail.
Il ne suppose ni OMX ni service AZDone.

## 1. Installer les skills dans le projet

Depuis le parent de votre dépôt :

```bash
git clone https://github.com/charlescstpierr/azdone.git
mkdir -p mon-projet/.agents/skills
cp -R azdone/skills/. mon-projet/.agents/skills/
cd mon-projet
```

Ouvrez ou redémarrez Codex dans `mon-projet`. Avec `/skills`, confirmez que
`initialiser-projet-azd`, `piloter-workflow-azd` et
`verifier-readiness-azd` sont visibles.

## 2. Initialiser une seule fois

```text
$initialiser-projet-azd
```

L’agent inspecte d’abord le dépôt. Il doit ensuite proposer les conventions
repo-locales : backlog, cartes, autorité, Git, preuve, Boussole, langage partagé,
System Success Map, Project Decision Graph et Readiness Forecast.

L’emplacement dépend des conventions existantes. `.azdone/` n’est qu’un repli
si le dépôt ne possède aucun emplacement plus naturel.

Résultat attendu :

```text
status: ready-for-workflow | blocked | authority-request
initialization: created | already-initialized
control_file: <chemin>
pointers:
  compass: <chemin>
  language: <chemin>
  decision_graph: <chemin>
  readiness: <chemin>
next_safe_action: <action concrète>
```

Une deuxième invocation doit répondre `already-initialized` sans réécrire les
conventions. Un changement futur passe par une carte de migration.

## 3. Donner un objectif normal

```text
$piloter-workflow-azd "Je veux un petit SaaS où un client dépose une demande et voit son statut."
```

Le pilote devrait :

1. clarifier seulement les inconnues qui changent réellement le résultat;
2. inspecter le dépôt et les capacités déjà disponibles;
3. établir les claims et les moyens de preuve;
4. créer des cartes liées et un ordre d’exécution;
5. demander l’autorité avant compte, secret, coût, publication ou production.

Pendant le grilling, l’agent pose une question à la fois. Pour une décision
matérielle, il présente :

- sa recommandation;
- la meilleure alternative;
- le statu quo;
- les coûts, délais, risques, réversibilité et preuves de chaque choix.

## 4. Lire le premier verdict

AZDone distingue :

- `verified` : tous les claims requis ont une preuve fraîche suffisante;
- `partial` : résultat utile mais preuve ou travail encore manquant;
- `blocked` : aucun prochain pas sûr sans information, moyen ou autorité;
- `failed` : une gate a échoué;
- `authority-request` : une action sensible attend une décision humaine.

Un verdict `partial` ou `blocked` doit fournir une `next_safe_action` précise.

## 5. Ce qu’il faut observer pendant le premier essai

Notez si l’agent :

- comprend votre vocabulaire sans inventer;
- détecte tôt Playwright, simulateur, client Telegram, API, compte ou dataset
  nécessaire;
- évite un prototype UI lorsqu’aucune surface humaine ne change;
- isole réellement les lanes avant d’appeler des subagents;
- prouve le résultat sur sa surface réelle;
- vous dit honnêtement ce qui reste non prouvé.

Ces observations alimenteront le Pilot 0 et non une prétendue preuve de
supériorité.

