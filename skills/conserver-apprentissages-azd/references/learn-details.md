# Détails des apprentissages AZDone

## Dispositions

Use keep only when a learning is supported and has a concrete future decision. Use discard when evidence is insufficient, unverifiable, or contradicted. Use rollback when an existing learning should be withdrawn or restored because fresh evidence refutes it.

## Conflicts

If two learnings conflict, preserve both only when their scopes differ. Otherwise request resolution or more evidence. Link replacements, invalidations, and historical records explicitly.

## Restart-safe branch-scoped retrieval

Learning retrieval is keyed by `branch_scope`: repo, branch, base_commit, head_commit, worktree, and run_id. The `retrieval_key` must include that branch scope, not just a global topic name. On resume, reload the learning_store by the same key, compare it with in-memory candidates, and mark drift or conflict before proposing keep, discard, or rollback.

If branch_scope does not match, do not reuse the learning as current policy. Preserve it as historical context, narrow the scope, or return local-only with insufficient-evidence.

## Redaction and provenance

Every accepted learning keeps provenance for source run, commit, artifact, author, oracle, and date. Credentials, personal data, and secrets are never stored raw; replace them with redacted pointers and record the reason in redaction_log.

## Operational Versus Policy

Keep operational_learnings separate from policy_learnings. A workflow observation does not become governance without explicit authority and independent evidence.
