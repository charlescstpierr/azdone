---
name: initialiser-projet-azd
description: "Configurer AZDone une seule fois lors de la première entrée dans un dépôt. Utiliser après l'installation du skill set et avant tout autre skill AZDone pour fixer les conventions repo-locales: backlog, cartes, langage, décisions, architecture, preuve, readiness, Git, autorité et emplacement des artefacts."
---

# Étape 00 · Initialiser le projet

Construire une seule fois le socle de conventions partagé dont les autres skills AZDone ont besoin. Ce skill configure le projet; il n'installe ni OMX, ni daemon, ni dépendance globale.

Lire [bootstrap-contract.md](references/bootstrap-contract.md) avant toute écriture.

## Quick start

```text
$initialiser-projet-azd repository=. authority="conventions repo-locales seulement"
```

Artefact attendu: une Constitution AZDone courte dans l'unique fichier de contrôle, des pointeurs repo-locaux éditables, un premier `readiness_forecast` et le verdict `ready-for-workflow | needs-grilling | already-initialized | authority-required | blocked`.

## Déclencheur unique

Lancer au premier usage d'AZDone dans un projet neuf ou existant. Si un setup AZDone existe déjà, le lire et arrêter avec `already-initialized`. Ne jamais le réexécuter automatiquement.

Un futur changement de convention devient une carte de migration explicite, avec impact, rollback et approbation humaine. Il ne déclenche pas un nouvel init.

## Principe

L'init est progressive:

1. inspecter les faits et conventions locales avant de questionner l'humain;
2. proposer les conventions les plus compatibles avec le dépôt;
3. griller une seule décision matérielle à la fois;
4. présenter une recommandation, la meilleure alternative et le statu quo;
5. expliquer coûts, délai, complexité, risque, réversibilité et impact sur les décisions liées;
6. écrire seulement les décisions approuvées et conserver les inconnues comme telles.

## Procédure

1. Détecter le dépôt, son état Git, ses remotes, son fichier de contrôle agent, son tracker, ses docs, ses conventions, ses surfaces et l'autorité disponible.
2. Chercher une preuve de setup AZDone existant. S'il existe, ne rien réécrire; rendre ses pointeurs et `already-initialized`.
3. Choisir un seul fichier de contrôle déjà présent (`AGENTS.md`, `CLAUDE.md` ou équivalent). S'il n'existe pas, demander lequel créer. Y inscrire une **Constitution AZDone** courte et des pointeurs; ne jamais maintenir deux sources de vérité concurrentes.
4. Fixer les **conventions de travail**:
   - backlog et création de cartes;
   - états `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done`;
   - labels ou équivalents;
   - Git, branches, worktrees, commits, review, livraison et rollback;
   - niveaux `Rapid | Standard | Critical`;
   - bornes d'autorité et actions qui exigent l'humain.
5. Fixer les **conventions de connaissance**:
   - Atlas universel: `ship`, `PR`, `commit`, `worktree`, `QA`, `runtime`, `API`, preuve, oracle, rollback;
   - emplacement du `CONTEXT.md` ou de son équivalent;
   - emplacement des ADR et règles de décision;
   - lexique métier du projet;
   - lexique technique du domaine et de l'architecture;
   - pont `langage humain -> terme métier -> terme technique -> moyen de preuve`.
6. Fixer les **conventions d'architecture et de réussite**:
   - emplacement de la Boussole;
   - System Success Map produit, technique, opérationnelle et commerciale/distribution;
   - Project Decision Graph et liens entre décisions, tickets, dépendances, risques et preuves;
   - Route Pack de langage, architecture, recherche et preuve.
7. Fixer les **conventions de preuve et readiness**:
   - où vivent Proof Contracts, Readiness Forecasts et evidence bundles;
   - comment distinguer Functional Proof, Approval Readiness et External Approval;
   - comment invalider et revalider un artefact périmé.
8. Pour un projet `Standard` ou `Critical` seulement si plusieurs inconnues indépendantes le justifient, constituer un **Bootstrap Council** borné: architecture, risques, preuve et opportunités. Dimensionner ses lanes par scope utile, risque et indépendance, jamais par nombre de fichiers. Si les subagents sont indisponibles ou inutiles, inspecter directement; leur absence ne bloque pas l'init.
9. Amorcer seulement le minimum connu de la Boussole, du langage, de la System Success Map et du graphe. Les skills suivants les enrichiront sans relancer l'init.
10. Pour chaque convention matérielle non résolue, poser une seule question avec recommandation, meilleure alternative, statu quo et trade-offs.
11. Montrer le bloc de contrôle et les fichiers proposés avant écriture. Ne pas écraser un fichier humain existant sans décision explicite.
12. Écrire les conventions et pointeurs repo-locaux en suivant les pratiques du dépôt. Utiliser `.azdone/` seulement si aucun emplacement plus approprié n'existe. Le skill set demeure globalement installable; Boussole, cartes, décisions, forecasts et preuves restent repo-locaux.
13. Appeler `$verifier-readiness-azd` une première fois, créer le checkpoint initial et remettre le contrôle à `$piloter-workflow-azd`.

## Politique de recherche et capacités

- Réutiliser d'abord dépôt, documentation, outils, skills et mémoire locale.
- Chercher en ligne seulement quand l'information est instable, externe, inconnue ou qu'une meilleure pratique actuelle peut changer la décision.
- Préférer documentation officielle, standards et dépôts sources. X, Hacker News et tendances sont des signaux, pas des preuves.
- Ne jamais installer un outil, accepter une licence, créer un compte, utiliser des credentials ou toucher la production sans l'autorité requise.
- Si une capacité manque, créer un gap explicite avec recommandation et solution de repli; ne pas attendre l'exécution du ticket pour l'annoncer.

## Sortie

```yaml
azdone_init:
  status: initialized | already-initialized | authority-required | blocked
  repository: ""
  control_file: ""
  constitution: {path: "", block: ""}
  state_root: ""
  conventions:
    backlog: ""
    card_states: []
    git_delivery: ""
    risk_policy: ""
    authority_policy: ""
    knowledge_layout: ""
    decision_layout: ""
    proof_layout: ""
  compass: {status: draft | approved | stale, path: ""}
  shared_language:
    atlas: ""
    business_lexicon: ""
    technical_lexicon: ""
    bridge: ""
  system_success_map: {path: "", unknowns: []}
  decision_graph: {path: "", nodes: 0, edges: 0}
  route_pack: {language: [], architecture: [], research: [], proof: []}
  readiness_forecast: {verdict: ready | at-risk | waiting | authority-required | blocked}
  cards: [{id: "", state: Draft | Needs-Grilling | Ready, blocked_by: []}]
  decisions_requiring_human: []
  checkpoint: ""
  bootstrap_council: {used: false, lanes: [], reason: ""}
  verdict: ready-for-workflow | needs-grilling | already-initialized | authority-required | blocked
```

## Bornes

- Ne pas implémenter le produit pendant l'init ni relancer automatiquement l'init comme maintenance continue.
- Ne pas prétendre qu'un projet est complet parce que ses conventions existent.
- Ne pas inventer une architecture universelle: activer les modules selon le projet réel.
- Ne pas créer le vault Obsidian physique, le daemon Doctor ou le moteur d'auto-évolution; ces surfaces sont différées. Doctor reste un outil de diagnostic du builder après un pilote, jamais une partie de l'init ou du workflow utilisateur.
