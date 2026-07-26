---
name: conserver-apprentissages-azd
description: "Conserver des apprentissages bornés et falsifiables à partir des preuves de run, de la mémoire ou recherche optionnelle, des corrections, reviews, incidents et décisions. Utiliser pour capturer une connaissance traçable sans transformer une anecdote, une préférence ou une source invérifiable en règle universelle."
---

# Étape 13 · Conserver les apprentissages

Capture des apprentissages gouvernables, pas des mythes. Capture bounded knowledge, not universal claims. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$conserver-apprentissages-azd "Extrait les apprentissages du run R42 et propose seulement ce qui est prouve."`

Verdict attendu: candidats `keep`, `discard`, `rollback` ou `insufficient-evidence`, avec provenance, scope, confidence, counterexample, expiry, future decision et memory_authority.

## Utiliser quand / Use when

Utilise ce skill apres un run, une correction utilisateur, une review, un incident, une recherche optionnelle ou une decision acceptee qui peut influencer un futur choix.

## Procedure courte

1. Résoudre les pointeurs repo-locaux définis par le setup; ne pas inventer un vault physique.
2. Lis les preuves du `source run`, corrections utilisateur, review findings, incidents et décisions acceptées.
3. Consomme une mémoire optionnelle (`optional memory`) ou recherche seulement si elle est pertinente et traçable; no memory dependency, daemon, database or durable service.
4. Sépare capture, promotion et récupération. Une observation entre d'abord comme `candidate`, jamais directement comme politique.
5. Note la `provenance` exacte: run, commit, artefact, auteur, oracle et date.
6. Marque `insufficient-evidence` pour anecdote, single preference ou source unverifiable; never promote anecdotal evidence to universal policy.
7. Écris un `claim` falsifiable avec le `scope` le plus étroit compatible avec les preuves.
8. Calibre `confidence` depuis qualité, répétition et indépendance des sources.
9. Ajoute `counterexample`, `expiry` ou `revalidation_condition`, et une `future decision` concrète.
10. Construis un `evidence_graph`: nœuds `claim`, `source`, `artifact`, `oracle`; arêtes `supports`, `contradicts`, `derived_from`, `supersedes`.
11. Classe le drift: `stale`, `superseded`, `contradicted`, `temporal_regression`, `negation_artifact`; utiliser le `revalidation_condition` au lieu de rendre une règle permanente.
12. Cherche chaque `conflict` avant acceptation; préserve l'historique au lieu d'écraser silencieusement.
13. Calcule `branch_scope`: `repo`, `branch`, `base_commit`, `head_commit`, `worktree`, `run_id`; branch_scope must match avant de réutiliser une learning existante.
14. Exécute `restart_safe_retrieval` avant écriture: retrouve les learnings par `retrieval_key` branch-scoped, recharge-les après resume, détecte drift/conflicts, puis seulement propose keep/discard/rollback.
15. Déclare les `host_capabilities` disponibles: `artifact_read`, `artifact_write`, `memory_read`, `memory_write`, `research_fetch`. Missing capability must fail closed.
16. Retire credentials, données personnelles et `secrets`; conserve un pointeur redacted et un `redaction_log`, jamais la valeur brute.
17. Faire passer chaque candidat par `candidate -> promote | revalidate | supersede | retract | expire`. Toute politique ou décision matérielle exige approbation humaine.
18. La récupération est bornée et en lecture seule: injecter seulement les éléments pertinents, avec provenance, scope et fraîcheur. La mémoire ne peut jamais contredire une preuve actuelle ou accorder une autorité.
19. Respecte `memory_authority`: propose localement par défaut, persiste seulement dans le périmètre autorisé.
20. Voir [learn-details.md](references/learn-details.md) pour les conflits, dispositions, retrieval restart-safe, redaction et séparation operational/policy.

## Sortie / Output

```yaml
learn:
  source_run: ""
  branch_scope:
    repo: ""
    branch: ""
    base_commit: ""
    head_commit: ""
    worktree: ""
    run_id: ""
  restart_safe_retrieval:
    retrieval_key: ""
    learning_store: []
    loaded_at_start: []
    reloaded_after_resume: []
    branch_scope_match: true
    drift_checked: true
  host_capabilities:
    artifact_read: present | missing
    artifact_write: present | missing
    memory_read: present | missing
    memory_write: present | missing
    research_fetch: present | missing
    capability_gap: []
  optional_sources:
    memory: []
    research: []
  evidence_graph:
    nodes: [{type: claim | source | artifact | oracle, id: ""}]
    edges: [{type: supports | contradicts | derived_from | supersedes, from: "", to: ""}]
    drift: [{type: stale | superseded | contradicted | temporal_regression | negation_artifact, revalidation_condition: ""}]
  candidates:
    - claim: ""
      type: operational | policy | preference | hypothesis | observed-fact
      scope: []
      provenance: []
      confidence: low | medium | high
      counterexample: ""
      expiry: ""
      future_decision: ""
      conflicts: []
      redaction_log: []
      disposition: keep | discard | rollback | insufficient-evidence
      lifecycle: candidate | promoted | revalidate | superseded | retracted | expired
  memory_authority: local | durable | none
  requires_daemon_or_db: false
  runtime_contract: "ordinary Markdown skill; no daemon; no database"
  persisted_paths: []
  verdict: accepted | local-only | rejected | insufficient-evidence | authority-request
```

Never make a universal rule from weak evidence. Sans autorite durable, rends un artefact local-only.
