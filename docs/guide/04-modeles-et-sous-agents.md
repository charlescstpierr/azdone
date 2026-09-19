# Modèles et sous-agents

`/azd` peut déléguer à des sous-agents. `trust.yaml` décide qui fait quoi,
avec quel modèle, natif ou externe.

## Cinq rôles

| Rôle | Responsabilité |
| --- | --- |
| `scout` | lecture seule, inspection ciblée, rend un digest |
| `builder` | écrit dans le worktree assigné, boucle RED/GREEN/REFACTOR |
| `verifier` | exécute les preuves du Proof Contract |
| `reviewer` | relit indépendamment, protocole planted-defect |
| `watcher` | surveille CI, PR ou événement, se réveille dessus |

`author_id != reviewer_id` reste strict : le relecteur n'écrit jamais dans le
scope de l'auteur.

## `host:` ou `cli:`

```yaml
models:
  roles:
    scout: host:small
    builder: host:default
    verifier: host:default
    reviewer: host:strong
    second_reviewer: cli:codex
    watcher: host:small
```

`host:<tier>` appelle un sous-agent natif de l'hôte : Claude Code mappe
`small|default|strong` sur `haiku|sonnet|opus`, Cursor sur son modèle
configuré, Codex sur son sous-agent natif s'il existe, sinon
`subagents-unavailable`.

`cli:<adaptateur>` exécute une commande externe avec le context packet sur
stdin. Le résultat est traité comme une donnée non fiable, jamais comme une
autorité.

## Adaptateurs vérifiés

```yaml
adapters:
  codex:  "codex exec -m {model} -s read-only -a never -C {cwd} --skip-git-repo-check"
  claude: "claude -p --model {model} --permission-mode plan --output-format text --max-turns 8"
  cursor: "agent -p --model {model} --output-format text --workspace {cwd}"
```

`azd-setup` n'écrit un adaptateur qu'après avoir confirmé `<cli> --help` sur
le PATH. Le binaire de Cursor est `agent` (`cursor-agent` en repli s'il est
introuvable). Si l'adaptateur choisi pour un rôle manque, le rôle retombe sur
`host:` et la réponse le mentionne.

## Exemple

```text
/azd revue indépendante de la PR 412, budget large, utilise codex comme second relecteur.
```

`/azd` route `reviewer` vers `host:strong` et `second_reviewer` vers
`cli:codex`, en lecture seule pour les deux.

## Staffing par risque

Rapid : zéro sous-agent par défaut, un maximum. Standard : un à trois.
Critical : deux à cinq, dont un relecteur indépendant. Chaque sous-agent
reçoit un context packet de 40 lignes maximum : pointeurs de fichiers, pas de
contexte inline.

Suivant : [Comprendre et concevoir](05-comprendre-et-concevoir.md).
