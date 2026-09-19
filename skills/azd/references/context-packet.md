# Context packet

Gabarit de brief pour tout sous-agent (`azd-scout`, `azd-builder`, `azd-verifier`, `azd-reviewer`, `azd-watcher`). Règle : pointeurs de fichiers, jamais de contexte inliné. Citer un chemin repo-local plutôt que coller un extrait de conversation.

```yaml
context_packet:
  role: scout | builder | verifier | reviewer | watcher
  card:
    id: ""
    path: repo-local path
  compass_excerpt:
    path: repo-local path
    section: ""
  proof_contract:
    path: repo-local path
  paths:
    read: []
    write: []
  write_scope: []
  worktree: repo-local path
  base_commit: git sha
  exit_condition: predicate observable
  return_format: path to the expected YAML shape for this role
  budget:
    tier: small | medium | large | unlimited
    max_turns: 0
```

## Format de retour

Chaque rôle rend au plus 30 lignes de YAML, jamais un transcript brut. Le format exact par rôle est dans `agents/azd-scout.md`, `agents/azd-builder.md`, `agents/azd-verifier.md`, `agents/azd-reviewer.md` et `agents/azd-watcher.md` à la racine du dépôt. Le routage `host:`/`cli:` de chaque rôle est dans [model-routing.md](model-routing.md).
