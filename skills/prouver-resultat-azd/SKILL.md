---
name: prouver-resultat-azd
description: "Prouver chaque affirmation avec des preuves fraîches adaptées à la surface, des oracles gelés, une provenance et des verdicts honnêtes. Utiliser avant de déclarer terminé un changement, une livraison, un benchmark, une interface, une API, une CLI/TUI, des données, une infrastructure, une documentation ou un workflow."
---

# Étape 09 · Prouver le résultat

Prouve chaque affirmation avec une evidence fraiche et adaptee a la surface reelle. Prove each claim with fresh, surface-appropriate evidence. Interfaces publiques equivalentes: Français and English.

## Quick start

Invocation: `$prouver-resultat-azd "Verifie le commit courant contre public-contract.json et la UI acceptance matrix."`

Verdict attendu: matrice claim-by-claim, commandes exactes, artefacts, provenance commit/agent, statut `verified`, `partial`, `blocked` ou `failed`.

## Utiliser quand / Use when

Utilise ce skill lorsqu'un changement, une release ou une affirmation doit etre verifie contre ses exigences actuelles.

## Procedure

1. Relire le Proof Contract verrouillé et le Readiness Forecast; confirmer que les outils, accès, données, environnements et oracles prévus ont réellement été utilisés.
2. Mappe chaque exigence vers un check et son oracle.
3. Confirme que l'oracle/evaluator est gelé et hors candidate write scope.
4. Détecte la surface livrée: `web`, `mobile`, `backend`, `API`, `infra`, `data`, `library`, `CLI`, `TUI`, docs, workflow ou mixte.
5. Choisis les gates natifs qui prouvent cette surface: fresh tests, lint, types, build, runtime, visual, screenshots, accessibility, conversation humaine, contract, migration, schema, performance ou observability.
6. Exécute un `contract-completeness pass` littéral sur tokens, selectors, attributs, paths, schema fields, IDs, rôles, viewports et artefacts publics.
7. Pour UI, parcours loading/empty/error/success; exerce clavier, focus persistant et live region. Pour chat/agent, rejoue des conversations représentatives et inspecte réponse, latence, continuité, récupération et friction.
8. Exécute le `carryover_gate`, incluant le `discovery carryover gate`, sans perdre `discovery.contradictions`, staleness/divergences de version, `discovery.blind_spots`, risks et failure modes avec path/source, puis oracles, findings, rollback ou claims incomplètes.
9. Vérifie CLI/TUI seulement si la surface existe: `80x24`, `120x40`, clavier sans souris, stdout/stderr séparés, exit codes, SIGINT/interruption/annulation/timeout et texte non tronqué.
10. Enregistre provenance: `agent_id`, role, worktree, commit vérifié, commit evaluator/oracle, commandes, environnement et artefacts.
11. Construis un `evidence_graph`.
12. Rendre trois verdicts distincts:
    - `functional_proof`: le produit fait-il ce qui est promis?
    - `approval_readiness`: le bundle satisfait-il les exigences actuelles des écosystèmes ciblés?
    - `external_approval`: une autorité externe l'a-t-elle réellement approuvé? Sans soumission et verdict observé, rester `not-requested`.
13. En cas d'échec, identifier la première hypothèse causalement invalidée et la gate de retour. Ne pas renvoyer systématiquement au build.
14. Classe le drift et marque toute affirmation non prouvée `partial`, `blocked` ou `failed`.

## Sortie / Output

Rends une `claim-by-claim evidence matrix` avec `claim`, `status`, `evidence`, `freshness`, `oracle` et `risk`.

```yaml
verification:
  commit: ""
  worktree: ""
  provenance:
    agent_id: ""
    agent_role: ""
    verified_commit: ""
    evaluator_commit: ""
    commands: []
    artifacts: []
  detected_surfaces: []
  surface_gates:
    web: []
    mobile: []
    backend: []
    api: []
    infra: []
    data: []
    library: []
    cli_tui: []
    docs_workflow: []
  evaluator:
    frozen: true
    outside_candidate_write_scope: true
  carryover_gate:
    checked_transitions: []
    dropped_fields: []
    freshness_boundaries: []
    status: pass | fail | blocked
  evidence_graph:
    nodes: [{type: claim | source | artifact | oracle, id: ""}]
    edges: [{type: supports | contradicts | derived_from | supersedes, from: "", to: ""}]
    drift: [{type: stale | superseded | contradicted | temporal_regression | negation_artifact, revalidation_condition: ""}]
  matrix:
    - claim: ""
      status: passed | partial | blocked | failed
      evidence: ""
      freshness: ""
      oracle: ""
      risk: ""
  readiness_usage:
    forecast: ""
    planned_tools: []
    tools_actually_used: []
    missing_means: []
  functional_proof: verified | partial | blocked | failed
  approval_readiness:
    target_ecosystems: []
    status: ready | partial | blocked | not-applicable
    evidence: []
  external_approval:
    status: not-requested | submitted | approved | rejected | blocked
    evidence: []
  causal_return: none | readiness | understanding | diagnosis | design | plan | build
  status: verified | partial | blocked | failed
```

## Interdits / Forbidden

- Ne jamais utiliser de stale logs ni declarer complet un travail inverifiable.
- Fail closed si un `dropped_field` requis existe ou si sa freshness boundary ne correspond plus au commit/environnement vérifié.
- Ne pas remplacer un check impossible par une supposition; expliquer le blocker et la prochaine action sure.
- Fail closed si l'evaluator a ete modifie par l'auteur candidat ou si l'environnement ne correspond pas au claim.
- Ne jamais présenter une conformité locale, une checklist ou une readiness comme l'approbation réelle de Google, Apple, Microsoft, OpenAI, Anthropic ou toute autre autorité.
- Keep commands, paths, identifiers and verdicts identical in Français and English.
