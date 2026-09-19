---
name: conserver-apprentissages-azd
description: "Conserver des apprentissages bornés et falsifiables à partir des preuves de run, de la mémoire ou recherche optionnelle, des corrections, reviews, incidents et décisions. Utiliser pour capturer une connaissance traçable sans transformer une anecdote, une préférence ou une source invérifiable en règle universelle."
---

# Étape 13 · Conserver les apprentissages

Capture des apprentissages gouvernables et falsifiables, jamais des mythes.

## Quick start

Invocation : `$conserver-apprentissages-azd "Extrait les apprentissages du run R42 et propose seulement ce qui est prouve."`

Artefact attendu : candidats `keep`, `discard`, `rollback` ou `insufficient-evidence`, avec provenance, scope, confidence, counterexample, expiry, future decision et memory_authority.

## Utiliser quand

- Un run, une correction utilisateur, une review ou un incident vient de se terminer.
- Une recherche optionnelle ou une décision acceptée peut influencer un futur choix.
- Une connaissance doit être capturée sans devenir une règle universelle non prouvée.

## Procédure

1. Résoudre les pointeurs repo-locaux définis par le setup, sans inventer un vault physique, puis lire les preuves du `source run`, corrections utilisateur, review findings, incidents et décisions acceptées.
2. Consommer une mémoire optionnelle (`optional memory`) ou une recherche seulement si elle est pertinente et traçable : no memory dependency, daemon, database or durable service.
3. Séparer capture, promotion et récupération : une observation entre d'abord comme `candidate`, jamais directement comme politique.
4. Noter la `provenance` exacte : run, commit, artefact, auteur, oracle et date.
5. Marquer `insufficient-evidence` pour anecdote, single preference ou source unverifiable ; never promote anecdotal evidence to universal policy.
6. Écrire un `claim` falsifiable avec le `scope` le plus étroit compatible avec les preuves, puis calibrer `confidence` depuis qualité, répétition et indépendance des sources.
7. Ajouter `counterexample`, `expiry` ou `revalidation_condition`, et une `future decision` concrète.
8. Construire un `evidence_graph` (nœuds `claim`, `source`, `artifact`, `oracle` ; arêtes `supports`, `contradicts`, `derived_from`, `supersedes`) et classer le drift (`stale`, `superseded`, `contradicted`, `temporal_regression`, `negation_artifact`) en utilisant `revalidation_condition` au lieu d'une règle permanente.
9. Chercher chaque `conflict` avant acceptation ; préserver l'historique au lieu d'écraser silencieusement.
10. Calculer `branch_scope` (`repo`, `branch`, `base_commit`, `head_commit`, `worktree`, `run_id`) : branch_scope must match avant de réutiliser une learning existante.
11. Exécuter `restart_safe_retrieval` avant écriture : retrouver les learnings par `retrieval_key` branch-scoped, recharge-les après resume, détecter drift/conflicts, puis seulement proposer keep/discard/rollback.
12. Déclarer les `host_capabilities` disponibles (`artifact_read`, `artifact_write`, `memory_read`, `memory_write`, `research_fetch`) : missing capability must fail closed.
13. Retirer credentials, données personnelles et `secrets` ; conserver un pointeur redacted et un `redaction_log`, jamais la valeur brute.
14. Faire passer chaque candidat par `candidate -> promote | revalidate | supersede | retract | expire` ; toute politique ou décision matérielle exige approbation humaine.
15. Limiter la récupération à un usage borné et en lecture seule : injecter seulement les éléments pertinents avec provenance, scope et fraîcheur ; la mémoire ne peut jamais contredire une preuve actuelle ni accorder une autorité.
16. Respecter `memory_authority` : proposer localement par défaut, persister seulement dans le périmètre autorisé.

Voir [learn-details.md](references/learn-details.md) pour les conflits, dispositions, retrieval restart-safe, redaction et séparation operational/policy.

## Sortie

Le skill rend un bloc `learn` documenté dans [learn-output.md](references/learn-output.md) : `source_run`, `branch_scope`, `restart_safe_retrieval`, `host_capabilities`, `optional_sources`, `evidence_graph`, `candidates`, `memory_authority`, `requires_daemon_or_db`, `runtime_contract`, `persisted_paths`, `verdict`.

## Arrêt et interdits

- Missing capability must fail closed, avec `capability_gap` documenté.
- Never promote anecdotal evidence to universal policy.
- branch_scope must match avant de réutiliser une learning ; sinon la préserver comme contexte historique et rester `insufficient-evidence` ou local-only.
- Retirer toute valeur brute de secrets, credentials ou données personnelles ; ne conserver que des pointeurs redacted.
- Sans autorité durable, rendre un artefact local-only.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
