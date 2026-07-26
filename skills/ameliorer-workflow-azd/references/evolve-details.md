# Détails d'évolution AZDone

This is a longitudinal skill-only protocol. It does not require a runtime, daemon, dependency, database, queue, scheduler, or background service. Longitudinal means the evidence spans baseline freeze, candidate comparison, provisional promotion, a post-promotion observation window, drift detection, and rollback proof.

## Frozen Baseline And Cohorts

Before candidate authoring, freeze the accepted baseline commit, behavior contract, evaluator implementation, evaluator prompts, thresholds, fixtures, hidden oracle, protected regressions, reviewer briefs, promotion criteria, and rollback bundle. Record paths, versions, and hashes.

Separate evidence into four cohorts:

- train: visible to the candidate author and allowed for iteration.
- held_out_eval: not visible to the candidate author until scoring.
- hidden_oracle: never visible to the candidate author; used only by independent evaluation.
- protected_regressions: not visible to the candidate author; must pass before scoring, cost comparison, or promotion.

If any cohort is missing, mixed, leaked, edited by the candidate, or selectively rerun, the result is fail-closed or discard.

## Independence

The candidate author, primary reviewer, and second reviewer must have distinct identities. Reviewers receive frozen reviewer briefs and review raw host-observed evidence, not author summaries alone. The author must not select held-out cases, approve the candidate, modify the evaluator, change thresholds, inspect hidden oracle cases, or run the final promotion decision.

Missing identity evidence, reviewer collision, reviewer collusion, or author-controlled acceptance is fail-closed.

## Verdicts

keep requires above-threshold improvement, all protected gates passing, complete host evidence, two passing independent reviews, promotion authority, and a successful provisional promotion observation window. discard covers ties, insufficient evidence, reward hacking, reviewer failure, or any candidate regression. rollback restores the last accepted baseline when a promoted version regresses during verification or observation. human-gate is required for security, data handling, governance, durable scope, or authority policy changes. fail-closed covers missing evidence, interrupted proof without trusted resume, modified frozen artifacts, leaked hidden oracle, identity conflicts, unavailable protected gates, or unverifiable host execution.

Keep is not final at merge time. It remains provisional until fresh post-promotion runs complete the observation window with no drift and all protected gates passing.

## Anti Reward Hacking

Reject candidates that edit the frozen evaluator, eval prompts, thresholds, hidden oracle, forward-tests, protected fixtures, reviewers, reviewer briefs, or promotion criteria after freeze. Reject skipped expensive tests, hidden unfavorable cases, selective reruns, threshold shopping, prompt leakage, author-visible hidden cases, reviewer collusion, and proxy optimization that harms correctness.

Anti-reward-hacking checks must run before aggregate scoring. Cost, latency, tokens, and tool-call improvements are ignored unless correctness and protected gates pass first.

## Observation, Drift, And Rollback

Promotion requires an observation window defined as a fixed number of fresh runs or a bounded duration. During this window, compare the promoted skill against the frozen baseline on fresh evidence. Track correctness drift, quality drift, regression recurrence, cost/latency drift, tool-call drift, interruption behavior, and host evidence completeness.

Drift detection fails closed when the observation window cannot complete, when fresh runs are incomplete, or when evidence is missing. If drift or regression appears, rollback to the last accepted baseline using the frozen rollback bundle and record recovery evidence.

## Resume After Interruption

Any interruption makes the current evaluation incomplete. Resume only from a trusted checkpoint that records baseline commit, candidate branch, frozen artifact hashes, cohort hashes, random seeds, budgets, authority, worktree paths, host evidence paths, and completed case IDs.

After resume, rerun the full frozen comparison or explicitly mark all non-rerun cases invalid. Never promote from partial, stale, or mixed pre/post-interruption evidence.

## Host Evidence And Fail-Closed States

Every decision must include host-observed evidence: agent IDs when agents were used, tool calls, commands, worktrees, artifacts, transcripts, exit statuses, raw results, and reviewer decisions. Do not simulate execution evidence.

Use fail-closed when the protocol cannot prove its own boundaries. Required fail-closed states include missing host evidence, modified frozen artifact, cohort leakage, candidate write-scope escape, author/reviewer identity conflict, interrupted run without full resume proof, unavailable protected regression suite, unverified rollback, or hidden authority expansion.

## Reversibility

Keep the accepted baseline, rollback bundle, raw runs, variance, failures, artifacts, versions, and post-promotion verification evidence. Promotion is not complete until the promoted commit passes fresh verification.
