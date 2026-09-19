# AZDone

AZDone is an entry layer, `/azd`, on top of **16 ordinary Agent Skills**. It
routes a goal to a built, proven, reviewed, and delivered outcome, under a
declarative trust policy you control.

[Documentation française](README.md)

## Status

**Public, skill-only preview.**

- No AZDone runtime, daemon, dashboard, or proprietary service.
- OMX is not required.
- Project and trust state stays inside the user repository (`.azdone/`).
- The 16 skill folders pass local structural and contract checks.
- Pilot 0 on a real human-led project has not run yet.
- AZDone does not claim general superiority or external platform approval.
- This repository is public for audit purposes, but public does not yet mean
  open source: no reuse license has been selected.

## Get started in 3 commands

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd your-project
../azdone/scripts/install.sh claude .
```

```text
/azd-setup
```

```text
/azd the export writes duplicate rows when a retry lands mid-run. Reproduce first, then fix and prove it.
```

Replace `claude` with `cursor` or `codex` for your host. Under Codex the
commands are `$azd-setup` and `$azd`. See the [installation
guide](docs/installation.md) for all three hosts and the plugin.

## What happens

```text
/azd "<goal>"  →  reads trust.yaml, picks a playbook  →  calls the skills  →  honest verdict
```

`/azd` classifies the request, copies the chosen playbook's steps into a
todo list, applies the trust policy to every sensitive action, then returns a
verdict (`verified | partial | blocked | failed`) with its evidence and
`next_safe_action`. Details in the [guide](docs/guide/02-azd.md).

## Trust

`.azdone/trust.yaml` sets what an agent may do without asking. Only a human
who writes or approves it grants that authority; no skill text can.

| Action | guided | assisted | autonomous | full |
| --- | --- | --- | --- | --- |
| read, native checks | auto | auto | auto | auto |
| write in an isolated worktree | ask | auto | auto | auto |
| write in the main worktree (accepted scope) | ask | auto | auto | auto |
| commit | ask | auto | auto | auto |
| push, open_pr | ask | ask | auto | auto |
| merge | ask | ask | conditional | auto |
| deploy | ask | ask | ask | conditional |
| install_global, external_message | ask | ask | ask | auto |
| credentials, delete_data, rewrite_shared_history, always_pause | ask | ask | ask | ask |

An always-pause list stays non-bypassable at every level: force-push to a
shared branch, deleting unmerged data, a production mutation without a proven
rollback, messaging a third party, using credentials, or the agent widening
`trust.yaml` itself.

Earned trust is on by default: five consecutive `verified` runs without a
rollback raise the level one step, up to the configured `ceiling`, logged in
`.azdone/trust-ledger.md`. `enforcement: declared` guides the agent without
external checking (the only mode under Codex). `enforcement: enforced`,
under Claude Code and Cursor, adds a hook (`hooks/azd-trust-guard.sh`) that
blocks shell commands the policy refuses. Details in the [trust
guide](docs/guide/03-confiance.md).

## Models and subagents

Five roles: `scout`, `builder`, `verifier`, `reviewer`, `watcher`. Each role
points to `host:small|default|strong` (the host's native subagent) or
`cli:codex|claude|cursor` (an external adapter confirmed on the PATH). The
reviewer stays independent from the author. Details in the [models and
subagents guide](docs/guide/04-modeles-et-sous-agents.md).

## The 16 skills

Every skill stays invocable on its own, without going through `/azd`. See the
[16-skill reference](docs/reference-skills.md).

## Documentation

- [The AZDone guide](docs/guide/README.md)
- [Installation and removal](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Skill reference](docs/reference-skills.md)
- [Validation and evidence limits](docs/validation.md)
- [Public contracts](CONTRACTS.md)
- [How it works](HOW_IT_WORKS.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)

## Verify the package

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The public suite checks names, triggers, contracts, guardrails, references,
packaging manifests, and the absence of a skill runtime. It does not by
itself prove real-project agent behavior.

## License

No reuse license has been selected yet. This repository is a public auditable
preview, but public does not yet mean open source. MIT, Apache-2.0, or
another license must be chosen explicitly before a stable release.
