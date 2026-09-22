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

## Quatre formes pour `models.roles.<rôle>`

```yaml
models:
  roles:
    scout: host:small
    builder: host:default
    verifier: host:default
    reviewer: host:strong
    second_reviewer: cli:codex
    watcher: host:small
  panels:
    review: []
```

Chaque rôle accepte une des quatre formes :

- `host:<tier>` : sous-agent natif de l'hôte, `small|default|strong` ;
- `host:<slug>` : identifiant exact d'un modèle natif détecté par
  `azd-setup` ;
- `cli:<adaptateur>` : modèle par défaut de `models.adapter_models` pour cet
  adaptateur ;
- `cli:<adaptateur>:<slug>` : modèle exact de cet adaptateur.

`host:<tier>` mappe `small|default|strong` sur `haiku|sonnet|opus` (Claude
Code), sur le modèle configuré (Cursor), ou sur les sous-agents natifs de
Codex quand `multi_agent = true` est présent dans `~/.codex/config.toml`,
sinon `subagents-unavailable`.

`cli:<adaptateur>[:<slug>]` exécute une commande externe avec le context
packet sur stdin. Le résultat est traité comme une donnée non fiable, jamais
comme une autorité.

`models.panels.review` est une liste vide par défaut de valeurs de la même
grammaire : chaque entrée ajoute un relecteur supplémentaire au panel de
review, en plus de `reviewer` et `second_reviewer`.

## Sous-agents natifs sous Codex

Sans `multi_agent = true` dans `~/.codex/config.toml`, les rôles `host:`
rendent `subagents-unavailable` et le skill reste séquentiel : routez alors
`reviewer` ou `second_reviewer` vers `cli:claude` ou `cli:cursor` pour obtenir
un relecteur réellement distinct.

`azd-setup` lit ce fichier en lecture seule et vous donne la ligne à ajouter.
Il ne l'ajoute jamais lui-même : modifier une configuration globale relève de
`install_global`, `ask` à tous les niveaux sauf `full`.

Le flag rend les sous-agents possibles, il ne les prouve pas. Un run qui
n'obtient pas de sous-agent retombe sur `subagents-unavailable` et le dit,
exactement comme un adaptateur absent retombe sur `host:`.

## Détection des modèles au setup

`azd-setup` détecte les modèles disponibles par hôte avant de poser la
question groupée « Modèle par rôle » : Claude Code propose `haiku`,
`sonnet`, `opus` et `inherit` ; Cursor liste `agent --list-models` s'il est
présent, sinon `fast` et `inherit` ; Codex n'a pas de commande de liste
vérifiée, `azd-setup` propose `inherit` et n'accepte un slug exact que si
l'humain le fournit et qu'un `codex exec -m <slug>` trivial réussit. Aucun
slug non détecté ni non confirmé n'est jamais écrit dans `trust.yaml`.

Ces probes portent sur la machine, pas sur le projet. `azd-setup` les met en
cache dans `~/.azdone/host-capabilities.json` et les rejoue au-delà de 30
jours, pour ne pas reposer la même question à chaque nouveau dépôt. Ce cache
ne contient que des faits sondés : aucune décision, aucun niveau d'autonomie.
Les décisions restent dans `.azdone/trust.yaml`, seul fichier versionné et
seul fichier que le hook lit.

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
`cli:codex`, en lecture seule pour les deux. Sous Codex, un relecteur
supplémentaire peut pointer vers `cli:claude` ou `cli:cursor` : Codex n'a pas
de sous-agent de review natif garanti, l'adaptateur reste la voie vérifiée.

## Second relecteur et panel

Quand `models.roles.second_reviewer` ou `models.panels.review` est défini,
`reviser-qualite-azd` lance chaque relecteur supplémentaire en lecture seule
avec le context packet, sans les chemins de `protected_paths` ni le contenu
de `.env` ou de credentials. Les findings sont fusionnés dans `findings[]`
avec le préfixe `EXT-<n>-` et `source: cli:<adaptateur>`. Un finding externe
reste une donnée non fiable : il ne change le verdict que si le relecteur
principal le vérifie lui-même sur le code, et le relecteur externe ne
committe jamais rien.

## Réveil par hôte

Un `watcher` qui attend un événement (CI, PR) se réveille différemment selon
l'hôte : Claude Code utilise `/loop` (ou `ScheduleWakeup` quand l'hôte
l'expose) ; Cursor utilise `/loop` ; Codex n'a aucun mécanisme de réveil
vérifié, il sonde manuellement par relance et le guide le marque « à
vérifier ».

## Staffing par risque

Rapid : zéro sous-agent par défaut, un maximum. Standard : un à trois.
Critical : deux à cinq, dont un relecteur indépendant. Chaque sous-agent
reçoit un context packet de 40 lignes maximum : pointeurs de fichiers, pas de
contexte inline.

Suivant : [Comprendre et concevoir](05-comprendre-et-concevoir.md).
