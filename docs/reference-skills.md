# Référence des skills AZDone

Le numéro est un repère visuel. Le token public reste le nom français ASCII.

## Entrée

| Skill | À utiliser quand… | Sortie principale |
| --- | --- | --- |
| `azd` | point d’entrée pour toute demande de travail rigoureux (`/azd`, `$azd`) | playbook choisi, liste de tâches, verdict honnête |
| `azd-setup` | première configuration ou relecture de `.azdone/trust.yaml` (`/azd-setup`, `$azd-setup`) | trust.yaml écrit, adaptateurs détectés, `next_safe_action` |

## Les 18 skills

| Repère | Skill | À utiliser quand… | Sortie principale |
| --- | --- | --- | --- |
| 00 | `initialiser-projet-azd` | AZDone entre pour la première fois dans un dépôt | conventions et pointeurs repo-locaux |
| 01 | `piloter-workflow-azd` | un objectif doit être routé jusqu’à un verdict honnête | route, progression, verdict, prochaine action |
| 02 | `clarifier-objectif-azd` | une inconnue change le résultat, le risque ou l’autorité | Outcome Contract, Boussole, question matérielle |
| 03 | `inspecter-projet-azd` | une décision exige des faits du dépôt ou des sources | dossier de découverte et capability gaps |
| 04 | `diagnostiquer-probleme-azd` | la cause d’un échec est inconnue | diagnostic prouvé, sans patch |
| 05 | `concevoir-experience-azd` | une surface humaine ou son interaction change | directions, prototype ou wireframe, décision |
| 06 | `planifier-travail-azd` | dépendances, cartes, preuve ou reprise doivent être ordonnées | DAG, cartes, ownership, Proof Contract |
| 06b | `structurer-code-azd` | un changement traverse une frontière de module, ajoute une forme de donnée, ou laisse le choix entre plusieurs structures | formes de données, frontières, ADR, unités vérifiables |
| 07 | `isoler-travail-azd` | des tranches ou hypothèses sont réellement indépendantes | branches/worktrees, lane ledger, checkpoints |
| 08 | `construire-solution-azd` | un plan ou test rouge est prêt pour un patch minimal | changement RED-GREEN-REFACTOR |
| 09 | `prouver-resultat-azd` | un claim doit être déclaré terminé | matrice claim-by-claim et verdict |
| 10 | `reviser-qualite-azd` | un auteur doit être relu indépendamment | findings stables et accept/return-to-build |
| 11 | `livrer-changement-azd` | un changement accepté doit être intégré ou publié | delivery record, handoff, rollback |
| 12 | `surveiller-livraison-azd` | une release, un canary ou un incident doit être observé | observation, incident ou rollback evidence |
| 13 | `conserver-apprentissages-azd` | une preuve peut devenir un apprentissage borné | learning record sourcé et révocable |
| 14 | `ameliorer-workflow-azd` | des signaux répétés justifient une mutation protégée | keep, discard, rollback ou human-gate |
| Socle | `verifier-readiness-azd` | moyens, accès, données, outils ou preuve peuvent manquer | Readiness Forecast frais |
| Socle | `verifier-application-azd` | quand une fonctionnalité doit être prouvée sur l'application réelle | skill repo-local verifier-<app>, matrice app_verification, feature map |

## Composition

Chaque skill reste invocable seul. Le pilote compose seulement les étapes
utiles :

```text
code-change    : 02 → 03 → 06 → 08 → 09 → 10 → 11
investigation  : 02 → 03 → 04
human-surface  : route normale + 05
release-ops    : route normale + 11 → 12
skill-mutation : preuves répétées → 14
```

Ces routes sont indicatives. Une gate invalide renvoie à la première cause
touchée plutôt qu’automatiquement au code.

## Les 9 playbooks de `azd`

| Playbook | Pour |
| --- | --- |
| `changement-code` | un changement de code ordinaire, du plan à la livraison |
| `correction-bug` | reproduire un défaut avant de le corriger |
| `investigation` | une question en lecture seule, aucune écriture |
| `surface-humaine` | un changement qu’un utilisateur va voir ou toucher |
| `prototype` | code jetable en scope isolé pour trancher une question par la mesure |
| `release` | pousser, ouvrir une PR, fusionner, déployer sous garde-fous |
| `run-autonome` | un travail long avec un prédicat de sortie déclaré |
| `reprise-de-session` | reprendre un travail interrompu depuis la dernière preuve |
| `babysit-pr` | mener une PR jusqu’à mergeable : conflits, threads, CI |

## Invariants publics

- Une question matérielle maximum par tour.
- Inspection avant diagnostic, design, plan ou code.
- Diagnostic sans correction lorsque la demande est diagnostique.
- Design seulement pour une surface humaine.
- `author_id != reviewer_id` pour la review indépendante.
- Aucune action sensible sans autorité.
- `next_safe_action` pour `partial` et `blocked`.
- Preuve fraîche avant `verified`.
- Aucun runtime requis dans les dossiers de skills.

