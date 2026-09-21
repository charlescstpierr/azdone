# Sortie · azdone_init

Bloc de sortie complet du skill `initialiser-projet-azd`.

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
