---
name: initialiser-projet-azd
description: "Configurer AZDone une seule fois lors de la première entrée dans un dépôt. Utiliser après l'installation du skill set et avant tout autre skill AZDone pour fixer les conventions repo-locales: backlog, cartes, langage, décisions, architecture, preuve, readiness, Git, autorité et emplacement des artefacts."
---

# Étape 00 · Initialiser le projet

Construire une seule fois le socle de conventions AZDone : inspecter les faits locaux avant de questionner l'humain, proposer les conventions les plus compatibles avec le dépôt, et n'écrire que les décisions approuvées. Ce skill configure le projet ; il n'installe ni OMX, ni daemon, ni dépendance globale.

## Quick start

Invocation : `$initialiser-projet-azd repository=. authority="conventions repo-locales seulement"`

Artefact attendu : une Constitution AZDone courte dans l'unique fichier de contrôle, des pointeurs repo-locaux éditables, un premier `readiness_forecast` et le verdict `ready-for-workflow | needs-grilling | already-initialized | authority-required | blocked`.

Lire [bootstrap-contract.md](references/bootstrap-contract.md) avant toute écriture.

## Utiliser quand

- Au premier usage d'AZDone dans un projet neuf ou existant ; si un setup existe déjà, le lire et arrêter avec `already-initialized` sans jamais le réexécuter automatiquement.
- Un futur changement de convention devient une carte de migration explicite avec impact, rollback et approbation humaine, jamais un nouvel init.

## Procédure

1. Détecter le dépôt, son état Git, ses remotes, son fichier de contrôle agent, son tracker, ses docs, ses conventions, ses surfaces et l'autorité disponible.
2. Chercher une preuve de setup AZDone existant ; s'il existe, ne rien réécrire et rendre ses pointeurs avec `already-initialized`.
3. Choisir un seul fichier de contrôle déjà présent (`AGENTS.md`, `CLAUDE.md` ou équivalent), demander lequel créer s'il n'existe pas, y inscrire une Constitution AZDone courte et des pointeurs, sans jamais maintenir deux sources de vérité concurrentes.
4. Fixer les conventions de travail : backlog et création de cartes, états `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done`, labels ou équivalents, Git/branches/worktrees/commits/review/livraison/rollback, niveaux `Rapid | Standard | Critical`, bornes d'autorité et actions qui exigent l'humain.
5. Fixer les conventions de connaissance : Atlas universel (`ship`, `PR`, `commit`, `worktree`, `QA`, `runtime`, `API`, preuve, oracle, rollback), emplacement du `CONTEXT.md` ou équivalent, emplacement des ADR et règles de décision, lexique métier, lexique technique et pont langage humain -> terme métier -> terme technique -> moyen de preuve.
6. Fixer les conventions d'architecture et de réussite : emplacement de la Boussole, System Success Map produit/technique/opérationnelle/commerciale, Project Decision Graph et Route Pack de langage, architecture, recherche et preuve.
7. Fixer les conventions de preuve et readiness : emplacement des Proof Contracts, Readiness Forecasts et evidence bundles, distinction entre Functional Proof, Approval Readiness et External Approval, et règle d'invalidation/revalidation d'un artefact périmé.
8. Pour un projet `Standard` ou `Critical` seulement, si plusieurs inconnues indépendantes le justifient, constituer un Bootstrap Council borné (architecture, risques, preuve, opportunités), dimensionné par scope utile, risque et indépendance, jamais par nombre de fichiers ; son absence ou indisponibilité ne bloque pas l'init.
9. Amorcer seulement le minimum connu de la Boussole, du langage, de la System Success Map et du graphe ; les skills suivants les enrichiront sans relancer l'init.
10. Pour chaque convention matérielle non résolue, griller une seule décision à la fois avec recommandation, meilleure alternative, statu quo et trade-offs (coût, délai, complexité, risque, réversibilité, impact sur le graphe).
11. Montrer le bloc de contrôle et les fichiers proposés avant écriture ; ne jamais écraser un fichier humain existant sans décision explicite.
12. Écrire les conventions et pointeurs repo-locaux en suivant les pratiques du dépôt, en utilisant `.azdone/` seulement si aucun emplacement plus approprié n'existe ; le skill set reste globalement installable mais Boussole, cartes, décisions, forecasts et preuves restent repo-locaux.
13. Appeler `$verifier-readiness-azd` une première fois, créer le checkpoint initial et remettre le contrôle à `$piloter-workflow-azd`.

## Sortie

Le skill rend un bloc `azdone_init` documenté dans [init-output.md](references/init-output.md) : `status`, `repository`, `control_file`, `constitution`, `state_root`, `conventions`, `compass`, `shared_language`, `system_success_map`, `decision_graph`, `route_pack`, `readiness_forecast`, `cards`, `decisions_requiring_human`, `checkpoint`, `bootstrap_council`, `verdict`.

## Arrêt et interdits

- Ne pas implémenter le produit pendant l'init ni relancer automatiquement l'init comme maintenance continue.
- Ne pas prétendre qu'un projet est complet parce que ses conventions existent.
- Ne pas inventer une architecture universelle : activer les modules selon le projet réel.
- Ne pas créer le vault Obsidian physique, le daemon Doctor ou le moteur d'auto-évolution ; ces surfaces sont différées, et Doctor reste un outil de diagnostic du builder après un pilote, jamais une partie de l'init ou du workflow utilisateur.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
