# Architecture d’AZDone

AZDone sépare le **contrat de décision** du **moteur d’exécution**.

```text
Humain
  │ objectif, décisions, autorité
  ▼
/azd, /azd-setup : couche d’entrée
  │ lit trust.yaml, classe la demande, choisit un playbook
  ▼
Host compatible : Codex, Claude Code, Cursor, autre host Agent Skills
  │ charge les skills et exécute Git, shell, navigateur, tests, subagents
  ▼
AZDone : 18 SKILL.md + références, agents/*, hooks/* optionnels
  │ prescrit routes, cartes, gates, preuves, handoffs et limites
  ▼
Dépôt utilisateur
    .azdone/trust.yaml ─ trust-ledger.md ─ decisions.tsv ─ conditions-ok (témoin, jetable)
    Boussole ─ Langage partagé ─ System Success Map
         └──── Project Decision Graph ────┐
                                          ▼
                              Readiness Forecast
                                          │
                                          ▼
                                  preuves et verdict
```

## Couche d’entrée

`/azd` (couche par-dessus les 18 skills, ne les remplace pas) lit
`.azdone/trust.yaml`, classe la demande par capacité et par risque, choisit un
des huit playbooks, et applique la politique de confiance à chaque action
sensible. `/azd-setup` écrit ou met à jour ce fichier de façon idempotente.
Les huit playbooks vivent dans `skills/azd/playbooks/`. Les agents
(`agents/azd-scout.md`, `azd-builder.md`, `azd-verifier.md`,
`azd-reviewer.md`, `azd-watcher.md`) portent les cinq rôles de délégation.
Les hooks (`hooks/`) sont optionnels : sous Claude Code et Cursor, ils font
respecter `trust.yaml` en `enforcement: enforced` ; ils ne sont jamais requis
pour invoquer un skill, et leur suppression ne bloque rien.
`.azdone/conditions-ok` est un témoin jetable écrit par la review finale et
lu par le hook pour un `merge` `conditional` ; `.azdone/trust-ledger.md` est
l'historique append-only des runs et des promotions/rétrogradations
d'`autonomy:`, écrit uniquement par `azd-trust-guard.py record`.

## Trois frontières

### 1. Installation

Les skills sont copiés dans `.agents/skills` ou l’emplacement reconnu par
l’hôte. Cette couche est remplaçable et versionnable.

### 2. État du projet

Les décisions, cartes, preuves et checkpoints restent repo-locaux. Une
installation globale ne crée jamais d’état global partagé entre projets.
Le skill `verifier-application-azd` prolonge cette règle : il écrit le skill
repo-local `verifier-<app>` et les artefacts `.azdone/proofs/` directement
dans le dépôt utilisateur, jamais dans l'installation AZDone elle-même.

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
- installateur ou updater automatisé au-delà de `scripts/install.sh`;
- preuve Pilot 0.

Ces absences sont des limites, pas des fonctions implicites.

