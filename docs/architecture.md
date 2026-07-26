# Architecture d’AZDone

AZDone sépare le **contrat de décision** du **moteur d’exécution**.

```text
Humain
  │ objectif, décisions, autorité
  ▼
Host compatible : Codex, Claude Code, autre host Agent Skills
  │ charge les skills et exécute Git, shell, navigateur, tests, subagents
  ▼
AZDone : 16 SKILL.md + références
  │ prescrit routes, cartes, gates, preuves, handoffs et limites
  ▼
Dépôt utilisateur
    Boussole ─ Langage partagé ─ System Success Map
         └──── Project Decision Graph ────┐
                                          ▼
                              Readiness Forecast
                                          │
                                          ▼
                                  preuves et verdict
```

## Trois frontières

### 1. Installation

Les skills sont copiés dans `.agents/skills` ou l’emplacement reconnu par
l’hôte. Cette couche est remplaçable et versionnable.

### 2. État du projet

Les décisions, cartes, preuves et checkpoints restent repo-locaux. Une
installation globale ne crée jamais d’état global partagé entre projets.

### 3. Exécution

Le host fournit les capacités réelles. Un skill peut demander Playwright,
Telethon, un simulateur, un compte, une API ou un subagent, mais il ne prétend
pas les posséder. Readiness classe chaque moyen :

```text
available | authority-required | missing | not-applicable
```

## Cycle d’une carte

```text
Draft → Needs Grilling → Ready → In Progress → Review → Done
           │                │                      │
           └─ 1 question    └─ preuve verrouillée └─ evidence bundle
```

Une idée découverte pendant une session devient une carte `Draft` liée. Elle ne
gonfle pas silencieusement le ticket actif.

## Chaîne de preuve

Avant `Ready`, chaque claim doit posséder :

```text
claim → oracle → outil → environnement → accès/données → artefact → seuil
```

Cette chaîne permet au preflight de signaler tôt un moyen manquant. Elle sépare
aussi trois notions souvent confondues :

1. `functional_proof`;
2. `approval_readiness`;
3. `external_approval`.

Une checklist locale ne devient jamais une approbation externe.

## Langage partagé

L’initialisation crée ou pointe vers :

- un Atlas AZDone universel;
- un lexique métier;
- un lexique technique adapté au domaine;
- un Language Bridge humain → métier → technique → preuve.

Le vocabulaire est progressif. Le workflow ne charge que le pack nécessaire à
la carte active.

## Subagents et branches

Le staffing dépend de l’indépendance réelle, des inconnues et du risque, pas du
nombre de fichiers.

```text
Rapid    : 0 lane par défaut, 1 aide maximum
Standard : 1 à 3 lanes indépendantes
Critical : 2 à 5 lanes pertinentes + vérification indépendante
```

Chaque lane possède un owner, un scope d’écriture et un worktree distinct. Une
proposition de délégation n’est jamais présentée comme un subagent réellement
exécuté.

## Ce qui n’existe pas encore

- Doctor public;
- daemon d’observation;
- vault Obsidian physique;
- packs de conformité par plateforme;
- installateur ou updater;
- preuve Pilot 0;
- plugin de distribution.

Ces absences sont des limites, pas des fonctions implicites.

