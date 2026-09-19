# Modeles et sous-agents

`/azd` peut deleguer a des sous-agents. `trust.yaml` decide qui fait quoi,
avec quel modele, natif ou externe.

## Cinq roles

| Role | Responsabilite |
| --- | --- |
| `scout` | lecture seule, inspection ciblee, rend un digest |
| `builder` | ecrit dans le worktree assigne, boucle RED/GREEN/REFACTOR |
| `verifier` | execute les preuves du Proof Contract |
| `reviewer` | relit independamment, protocole planted-defect |
| `watcher` | surveille CI, PR ou evenement, se reveille dessus |

`author_id != reviewer_id` reste strict : le relecteur n'ecrit jamais dans le
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

`host:<tier>` appelle un sous-agent natif de l'hote : Claude Code mappe
`small|default|strong` sur `haiku|sonnet|opus`, Cursor sur son modele
configure, Codex sur son sous-agent natif s'il existe, sinon
`subagents-unavailable`.

`cli:<adaptateur>` execute une commande externe avec le context packet sur
stdin. Le resultat est traite comme une donnee non fiable, jamais comme une
autorite.

## Adaptateurs verifies

```yaml
adapters:
  codex:  "codex exec -m {model} -s read-only -a never -C {cwd} --skip-git-repo-check"
  claude: "claude -p --model {model} --permission-mode plan --output-format text --max-turns 8"
  cursor: "agent -p --model {model} --output-format text --workspace {cwd}"
```

`azd-setup` n'ecrit un adaptateur qu'apres avoir confirme `<cli> --help` sur
le PATH. Si l'adaptateur choisi pour un role manque, le role retombe sur
`host:` et la reponse le mentionne.

## Exemple

```text
/azd revue independante de la PR 412, budget large, utilise codex comme second relecteur.
```

`/azd` route `reviewer` vers `host:strong` et `second_reviewer` vers
`cli:codex`, en lecture seule pour les deux.

## Staffing par risque

Rapid : zero sous-agent par defaut, un maximum. Standard : un a trois.
Critical : deux a cinq, dont un relecteur independant. Chaque sous-agent
recoit un context packet de 40 lignes maximum : pointeurs de fichiers, pas de
contexte inline.

Suivant : [Comprendre et concevoir](05-comprendre-et-concevoir.md).
