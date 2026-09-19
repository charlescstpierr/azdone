# Sortie · learn

Bloc de sortie complet du skill `conserver-apprentissages-azd`.

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
