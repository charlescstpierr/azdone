# Glossaire des concepts AZDone

Ce glossaire ne renomme rien. Les contrats et les tests gardent leurs noms actuels.
Les identifiants dans les verdicts et dans les fichiers restent en anglais.
Les concepts eux-mêmes sont en français ou en anglais selon leur origine.

**Atlas** (Atlas universel, vocabulaire commun). Vocabulaire commun d'AZDone : `ship`, `PR`, `commit`, `worktree`, `QA`, `runtime`, `API`, preuve, oracle, rollback. Où il vit : `skills/initialiser-projet-azd/`.

**Bootstrap Council** (conseil d'amorçage borné). Petit conseil borné, réuni seulement à l'init d'un projet Standard ou Critical avec plusieurs inconnues indépendantes, qui inspecte architecture, risques, preuve et opportunités. Son absence ne bloque jamais l'init. Où il vit : `skills/initialiser-projet-azd/`.

**Boussole** (cadrage). Objet de cadrage qui fixe utilisateur, problème, succès, écosystèmes cibles, non-négociables, refus et non-objectifs. Elle s'enrichit pendant clarification, inspection et planification. Où il vit : amorcée par `initialiser-projet-azd`, citée par la plupart des skills.

**Carte**. Unité de travail qui traverse le cycle `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done`, avec les états annexes `Blocked`, `Needs Revalidation`, `Rejected` et `Superseded`. Une seule carte active à la fois. Où il vit : `skills/planifier-travail-azd/`, `HOW_IT_WORKS.md`.

**conditions-ok** (témoin conditions-ok). Fichier témoin jetable `.azdone/conditions-ok`, écrit par la dernière étape de review, qui atteste commit, CI, review et bornes de risque pour autoriser un `merge` `conditional`. Supprimé sur `return-to-build`. Où il vit : `skills/azd/references/trust-policy.md`.

**Constitution AZDone**. Règles communes courtes et pointeurs repo-locaux écrits dans le fichier de contrôle agent existant (`AGENTS.md`, `CLAUDE.md` ou équivalent), changés seulement par une décision humaine matérielle. Où il vit : `skills/initialiser-projet-azd/`.

**context packet**. Brief d'au plus 40 lignes donné à un sous-agent ou à un adaptateur CLI externe : carte, extrait de Boussole, Proof Contract, chemins, write scope, condition de sortie, format de retour. Jamais de chemin protégé ni de credential. Où il vit : `skills/azd/references/context-packet.md`.

**Decision Stack** (pile de décisions). Pile des décisions en cours, séparée de l'Opportunity Inbox. Une idée externe n'interrompt que si elle change matériellement le risque, le coût, la réversibilité ou la valeur. Où il vit : `skills/piloter-workflow-azd/`.

**Destroyer** (lecture des failles). Deuxième des trois lectures d'une opportunité repérée par l'Opportunity Radar : cherche les failles d'une idée, après le Dreamer. Où il vit : `skills/inspecter-projet-azd/`.

**Dreamer** (lecture de la valeur). Première des trois lectures d'une opportunité : montre la valeur potentielle d'une idée, avant le passage par le Destroyer et l'Investor. Où il vit : `skills/inspecter-projet-azd/`.

**evidence bundle** (paquet de preuve). Ensemble des artefacts qui accompagnent une carte vers `Done` : preuve fonctionnelle, readiness et traçabilité, verrouillé au moment de la review finale. Où il vit : `skills/initialiser-projet-azd/`, `HOW_IT_WORKS.md`.

**feature map**. Table `statut: never | verified | stale` par fonctionnalité connue d'une application, amorcée par `verifier-application-azd generer` et mise à jour uniquement par une preuve fonctionnelle fraîche. Où il vit : `skills/verifier-application-azd/references/feature-map-template.md`.

**frozen evaluator** (évaluateur gelé). Évaluateur, oracle caché et régressions protégées, gelés hors du write scope d'un candidat pendant une comparaison de lanes ou l'évolution d'un skill, pour empêcher qu'un candidat s'auto-note. Où il vit : `skills/isoler-travail-azd/`, `skills/ameliorer-workflow-azd/`.

**Grilling**. Passage d'une carte par une question matérielle unique, avec faits déjà établis, recommandation, meilleure alternative, statu quo et trade-offs, avant qu'elle passe de `Draft` à `Ready`. Où il vit : `skills/initialiser-projet-azd/references/bootstrap-contract.md`.

**Investor** (lecture du coût et du risque). Troisième des trois lectures d'une opportunité : chiffre le coût et le risque, après le Dreamer et le Destroyer. Où il vit : `skills/inspecter-projet-azd/`.

**lane**. Worktree Git isolé confié à un agent ou sous-agent pour une hypothèse, une tranche indépendante ou une review adversariale. Deux lanes n'écrivent jamais dans le même worktree. Où il vit : `skills/isoler-travail-azd/`, `skills/piloter-workflow-azd/`.

**Language Bridge** (pont langage). Traduction entre terme humain, terme métier, terme technique et moyen de preuve, fixée à l'init et réutilisée par les autres skills. Où il vit : `skills/initialiser-projet-azd/references/bootstrap-contract.md`.

**Language Pack** (termes utiles à la carte active). Ensemble borné à la carte active de termes humains, termes métier, termes techniques, éléments d'architecture touchés et moyens de preuve, chaque terme défini brièvement au premier usage. Où il vit : `skills/clarifier-objectif-azd/`.

**Opportunity Inbox** (boîte à idées). Boîte des idées externes ou hors périmètre, séparée de la Decision Stack. Une idée retenue devient une carte `Draft` liée, jamais une modification silencieuse de la carte active. Où il vit : `skills/piloter-workflow-azd/`.

**Opportunity Radar** (une à trois idées à fort signal). Recherche bornée, menée aux fenêtres utiles seulement, d'une à trois idées à fort signal. Chaque idée passe par Dreamer, Destroyer et Investor avant de devenir une carte. Où il vit : `skills/inspecter-projet-azd/`.

**playbook**. Fiche de 10 à 30 lignes que `/azd` copie telle quelle dans la liste de tâches d'une demande classée, avec prédicat de sortie et contenu de réponse attendu. Où il vit : `skills/azd/playbooks/`.

**Ponytail** (supprimer avant d'ajouter, réutiliser avant d'inventer). Discipline de soustraction : supprimer avant d'ajouter, réutiliser avant d'inventer, refuser toute abstraction sans complexité réelle à couvrir. Où il vit : `skills/construire-solution-azd/`, `skills/reviser-qualite-azd/`.

**Project Decision Graph** (graphe de décisions). Graphe qui relie objectifs, décisions, tickets, dépendances, risques, preuves, artefacts et opportunités d'un projet. Où il vit : amorcé par `initialiser-projet-azd`, cité par `planifier-travail-azd` et `verifier-readiness-azd`.

**Proof Contract** (contrat de preuve). Contrat verrouillé avant `Ready` : claim, oracle indépendant, outil, environnement, données/accès, artefact, seuil, fraîcheur et condition d'échec. Où il vit : `skills/planifier-travail-azd/`, `skills/prouver-resultat-azd/`.

**Readiness Forecast** (prévision de préparation). Prévision des prérequis et moyens de preuve nécessaires avant `Ready`, recalculée dès qu'un changement matériel la périme. Où il vit : `skills/verifier-readiness-azd/`.

**Route Pack** (pointeurs de contexte). Ensemble traçable de pointeurs de contexte utiles, avec routes rejetées et raison d'arrêt, sans autorité d'action propre. Où il vit : `skills/verifier-readiness-azd/references/knowledge-routes.md`.

**System Success Map** (carte de réussite système). Carte des éléments produit, techniques, opérationnels et commerciaux d'un projet, classés indispensable, recommandé, plus tard, hors périmètre ou inconnu. Où il vit : amorcée par `initialiser-projet-azd`, citée par `planifier-travail-azd` et `verifier-application-azd`.

**trust-ledger**. Historique append-only des runs (`.azdone/trust-ledger.md`) : `date | run_id | risk | verdict | actions_auto | rollback | override | niveau_effectif | série | événement`. `/azd` s'en sert pour calculer promotion et rétrogradation. Où il vit : `skills/azd/references/trust-policy.md`.

**Wayfinder** (navigation d'un grand projet : destination, brouillard, frontière). Mode de navigation pour un grand projet : destination observable, carte de décisions persistée, brouillard (`fog`) et frontière (`frontier`) de ce qui reste à découvrir, tickets de décision et reprise. Domain-agnostic, activé seulement quand une carte de navigation apporte une valeur réelle. Où il vit : `skills/planifier-travail-azd/`.

**zero-assumption gate** (porte anti-hypothèse). Porte qui retourne `blocked` plutôt que d'avancer sur une hypothèse non vérifiée, quand une clarification ne peut pas progresser autrement. Où il vit : `skills/clarifier-objectif-azd/`.
