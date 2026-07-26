# AZDone

AZDone is a delivery workflow made of **16 ordinary Agent Skills**. It helps an
agent and a human turn an idea, change, or incident into a clarified, built,
proven, reviewed, and delivered outcome.

[Documentation française](README.md)

## Status

**Public, skill-only preview.**

- No AZDone runtime, daemon, dashboard, or proprietary service.
- OMX is not required.
- Project state stays inside the user repository.
- The 16 skill folders pass local structural and contract checks.
- Pilot 0 on a real human-led project has not run yet.
- AZDone does not claim general superiority or external platform approval.

## Quick start with Codex

```bash
git clone https://github.com/charlescstpierr/azdone.git
cd your-project
mkdir -p .agents/skills
cp -R ../azdone/skills/. .agents/skills/
```

Restart Codex if the skills do not appear, then invoke once:

```text
$initialiser-projet-azd
```

Give the pilot a normal goal:

```text
$piloter-workflow-azd "Build a SaaS that helps a small team track customer requests."
```

Codex officially loads repository skills from `.agents/skills`. Claude Code
uses `.claude/skills` for project skills. The detailed
[installation guide](docs/installation.md) covers both locations and current
validation limits.

## Core route

```text
initialize once → pilot → clarify → inspect → diagnose if needed
                → design if human-facing → plan → isolate if useful
                → build → prove → review → deliver
                → monitor if released → learn → evolve if justified
```

`verifier-readiness-azd` is the transversal readiness gate. The pilot skips
irrelevant steps and scales the route to uncertainty, risk, surface, and proof.

## Documentation

- [French quickstart](docs/demarrage-rapide.md)
- [Installation and removal](docs/installation.md)
- [Architecture](docs/architecture.md)
- [16-skill reference](docs/reference-skills.md)
- [Validation and evidence limits](docs/validation.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)

## Verify the package

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The public suite checks names, triggers, contracts, guardrails, references, and
the absence of a skill runtime. It does not by itself prove real-project agent
behavior.

## License

No reuse license has been selected yet. This repository is a public auditable
preview, but **public does not yet mean open source**. MIT, Apache-2.0, or
another license must be chosen explicitly before a stable release.

