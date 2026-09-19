# Sortie `discovery` (Étape 03)

Contenu attendu :

- evidence citée et provenance;
- décision sur le `capability gap`;
- outil utilisé, observations locales, capability gap constaté et raison d'arrêt;
- repo paths, `base_commit`, `worktree`, capability status;
- verdict `proceed`, `authority-request` ou `blocked`.

```yaml
discovery:
  repository: ""
  base_commit: ""
  worktree: ""
  environment_preflight:
    repository_root: ""
    git_state: ""
    required_tools: []
    native_capabilities: []
    conflicts: []
    verdict: ready | warn | blocked
  evidence:
    - path_or_url: ""
      kind: repo | primary-source | tool | cache
      freshness: ""
  optional_retrieval:
    semantic_search: unused | used | unavailable
    memory: unused | used | unavailable
    notes: []
  system_success_map_delta:
    indispensable: []
    recommended: []
    later: []
    out_of_scope: []
    unknown: []
  capability_gaps:
    - capability: ""
      why: ""
      recommendation: ""
      fallback: ""
      authority: automatic | human-required
      lead_time: ""
  opportunity_radar:
    ran: false
    candidates: [{idea: "", dreamer: "", destroyer: "", investor: "", disposition: draft-card | discard}]
  contradictions: []
  blind_spots: []
  prioritized_fix_or_doc: ""
  capability_gap: none | closed | authority-required | blocked
  verdict: proceed | authority-request | blocked
```
