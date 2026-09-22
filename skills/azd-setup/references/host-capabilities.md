# Cache de capacités par machine

Les probes des étapes 6 et 7 (`<cli> --help`, `agent --list-models`,
`codex exec -m <slug>`) portent sur la machine, pas sur le projet. Sans cache,
chaque nouveau dépôt les rejoue à l'identique et repose la même question.

Ce fichier décrit le seul cache autorisé. Il contient **des faits sondés**,
jamais une décision.

## Emplacement

`~/.azdone/host-capabilities.json`, un seul fichier pour les trois hôtes.

Hors du dépôt, donc hors de la promesse « l'état du projet et de la confiance
reste dans `.azdone/` ». C'est pour cela qu'il ne peut contenir aucune
politique : il n'est ni versionné, ni relu en revue, ni lu par le hook.

## Schéma

```json
{
  "schema": 1,
  "probed_at": "2026-09-22T14:03:11Z",
  "hosts_seen": ["claude-code", "codex"],
  "adapters": {
    "codex": {"path": "/usr/local/bin/codex", "help_confirmed": true,
              "command": "codex exec -m {model} -s read-only -a never -C {cwd} --skip-git-repo-check"},
    "claude": {"path": "/opt/node22/bin/claude", "help_confirmed": true,
               "command": "claude -p --model {model} --permission-mode plan --output-format text --max-turns 8"}
  },
  "models_probed_ok": {"codex": ["<slug confirmé par un run réel>"], "cursor": []},
  "codex_multi_agent": true
}
```

`codex_multi_agent` enregistre la présence de `multi_agent = true` dans
`~/.codex/config.toml`, lu en lecture seule. Absent du fichier de config, la
clé vaut `false`. Config illisible ou absente, la clé vaut `null`.

## Ce qui n'y entre jamais

`autonomy`, `ceiling`, `enforcement`, `actions.*`, `models.roles`,
`models.panels`, `models.budget`, ni aucune préférence humaine. Ces clés sont
des décisions : elles restent dans `.azdone/trust.yaml`, seul fichier
versionné et seul fichier que `hooks/azd-trust-guard.py` lit.

Un cache qui contiendrait l'une de ces clés est traité comme corrompu et
ignoré.

## Lecture

1. Fichier absent, illisible, JSON invalide, ou `schema` différent de `1` :
   ignorer en silence et sonder normalement. Un cache ne fait jamais échouer
   `azd-setup`.
2. Revalider la présence sur le `PATH` de chaque adaptateur du cache. Un
   adaptateur dont le binaire a disparu est retiré des propositions et
   resondé.
3. `probed_at` de plus de 30 jours : resonder au lieu de réutiliser. Un slug
   confirmé il y a un an ne prouve rien sur l'abonnement d'aujourd'hui.
4. Le cache sert à **pré-remplir** la question groupée « Modèle par rôle » et
   à afficher son âge. Il ne remplace jamais l'accord humain, et la règle de
   l'étape 6 tient sans exception : aucun slug non détecté ou non confirmé
   n'entre dans `trust.yaml`.

## Écriture

Après ses propres probes, `azd-setup` fusionne les nouveaux faits dans le
cache et le dit explicitement dans sa réponse, en nommant le chemin. Une
écriture hors du dépôt n'est jamais silencieuse.

Le cache n'est jamais écrit par un autre skill, ni par le hook, ni par un
sous-agent. `azd-setup` en est le seul auteur.

## Retrait

`rm -f ~/.azdone/host-capabilities.json` suffit, et `rmdir ~/.azdone` si le
dossier est vide. Rien d'autre n'en dépend : le prochain `azd-setup` resonde.
