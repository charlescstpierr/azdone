---
name: livrer-changement-azd
description: "Livrer un changement accepté en intégrant le travail, en prouvant le résultat combiné et en préparant checkpoint, handoff, notes de livraison et rollback. Utiliser pour intégrer des branches ou préparer ou exécuter un push, une pull request, un merge, un déploiement ou une conservation locale sous autorité explicite."
---

# Étape 11 · Livrer le changement

Intègre et prépare une livraison sans perdre de travail : ne livre que le résultat vérifié intégré.

## Quick start

Invocation : `$livrer-changement-azd "Integre les branches acceptees en dependency order et prepare une pull request sans merge."`

Artefact attendu : `checkpoint`, `fresh verification` sur l'`integrated result`, `release notes`, `remaining risks`, action `keep-local`, `open-pr`, `merge`, `deploy` ou `authority-request`.

## Utiliser quand

- Après `$prouver-resultat-azd` et `$reviser-qualite-azd`, pour intégrer un travail accepté.
- Pour documenter et préparer une livraison locale (checkpoint, handoff, release notes).
- Pour exécuter `push`, `pull request`, `merge` ou `deploy` déjà autorisés.

## Procédure

1. Charger les exigences gelées, le DAG et le `dependency order`, le Readiness Forecast, le Functional Proof, l'Approval Readiness, les verdicts de review et la politique d'`explicit authority`.
2. Confirmer que chaque candidat est accepté, rattaché au bon base commit, et que `author_id != reviewer_id`.
3. Inventorier dirty state, worktrees, branches rejetées et artefacts récupérables ; préserver tout travail utilisateur ambigu.
4. Créer ou valider un `checkpoint` (base commit, dirty-state inventory, diff attendu, artefacts, commandes passées/restantes) et un `resume_context` (`base_commit`, `branch`, `worktree`, `current_step`, `remaining_work`, `failed_approaches`, `resume_commands`, `next_safe_action`, `blockers`).
5. Intégrer avec des opérations Git réversibles ; résoudre un conflit seulement si le comportement attendu est prouvé, puis comparer le diff final aux scopes acceptés et signaler toute modification inattendue.
6. Lancer une `fresh verification` sur le vrai `integrated result`, jamais seulement sur les branches sources ou des stale logs, en rejouant les checks natifs pertinents (tests, protected suite, types, lint, build, migrations, smoke et visuel si applicable).
7. Produire un `context handoff` autonome avec état, commandes, artefacts, risques, prochaine transition, rollback conditions et le dernier `handoff_carryover` ; aucun champ requis ne peut être reconstruit silencieusement.
8. Préparer documentation utile, migration/rollback guidance, `release notes`, canary, monitoring et `remaining risks` ; écrire les `release notes` et le corps de la pull request selon `skills/azd/references/ecriture-humaine.md`.
9. Gate séparément `push`, `pull request`, `merge`, `submit-for-approval` et `deploy` ; sans autorité, retourner `authority-request`. L'autorité explicite se lit dans `.azdone/trust.yaml` (`actions.<action>`) quand ce fichier existe ; sinon `authority-request`.
10. Traiter une soumission externe et son verdict comme des événements distincts : ne jamais transformer `approval_readiness: ready` en `external_approval: approved`.

Voir [ship-details.md](references/ship-details.md) pour les règles complètes d'intégration, authority et rollback.

## Sortie

Le skill rend un bloc `ship` documenté dans [ship-output.md](references/ship-output.md) : `author_id`, `reviewer_id`, `integrated_commit`, `progress_snapshot`, `checkpoint`, `resume_context`, `context_handoff`, `authority`, `functional_proof`, `approval_readiness`, `external_approval`, `action`, `verification`, `canary`, `monitoring`, `rollback`, `verdict`.

## Arrêt et interdits

- Fail closed avant intégration si `author_id` et `reviewer_id` sont manquants ou identiques.
- Ne jamais convertir `partial`, `blocked` ou `failed` en livré.
- Ne jamais transformer `approval_readiness: ready` en `external_approval: approved` sans verdict externe réellement observé.
- Sans autorité explicite sur une action sensible, retourner `authority-request` plutôt que d'agir.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
