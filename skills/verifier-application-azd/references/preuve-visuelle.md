# Preuve visuelle annotée

Protocole seulement. Aucun script n'accompagne cette référence : l'outil
d'enregistrement, quand il existe, appartient au dépôt ou à l'hôte, jamais à
`verifier-application-azd`. Ce protocole encadre le mode `executer` (étape 8)
et tout enregistrement optionnel qui l'accompagne.

## Dossier de run

Chaque run de vérification écrit `.azdone/proofs/<date ISO>/`, avec :

- `manifest.json` : l'index structuré de chaque étape observée.
- `report.md` : le même contenu, lisible par un humain.
- un artefact par assertion : capture, extrait vidéo, transcript ou réponse
  brute, référencé par `manifest.json`.

Un seul `manifest.json` par run. Un nouveau run ouvre un nouveau dossier
`<date ISO>`, jamais une réécriture du précédent.

## Schéma de `manifest.json`

```json
{
  "run_id": "",
  "commit": "",
  "app": "",
  "started_at": "",
  "entries": [
    {
      "feature": "",
      "surface": "web | api | cli | tui | mobile | desktop | chat | data",
      "started_at": "",
      "steps": [
        {
          "t": "",
          "kind": "test_start | action | assertion | result",
          "text": "",
          "expected": "",
          "observed": "",
          "status": "pass | fail | blocked",
          "artifact": ""
        }
      ]
    }
  ]
}
```

`t` est un horodatage UTC (`started_at`, `entries[].started_at` et `steps[].t`
partagent le même format). `expected` et `observed` restent vides pour un
`kind: test_start` ou `action`; ils sont obligatoires pour `assertion` et
`result`.

## `report.md`

Un tableau généré depuis `manifest.json`, jamais tenu à la main : une ligne
par fonctionnalité, avec ses étapes, son statut et ses artefacts.

| Fonctionnalité | Étapes | Statut | Artefacts |
| --- | --- | --- | --- |
| `<feature>` | `<n> steps, dernier kind: result` | `pass \| fail \| blocked` | `<chemins>` |

## Enregistrement d'écran optionnel

Quand l'outil existe déjà sur la machine ou dans le dépôt, l'utiliser plutôt
qu'un simple relevé texte :

- Web : vidéo Playwright de la session pilotée.
- CLI ou TUI : session `asciinema`, ou à défaut un transcript stdout/stderr
  horodaté.
- Mobile : capture du simulateur ou de l'appareil.

Les annotations (`test_start`, `action`, `assertion`, `result`) s'incrustent
dans la vidéo quand l'outil le permet. Sans incrustation possible, une
capture horodatée par assertion tient lieu d'annotation visuelle et vit à
côté de la vidéo, référencée depuis le même `step`.

## Repli sans outil d'écran

Sans outil d'enregistrement disponible : un transcript texte horodaté de la
session (commandes, sorties, actions) plus une capture par assertion. Ce
repli reste une preuve de premier ordre, pas un pis-aller silencieux ; le dire
dans la réponse.

## Règles

- Horodatage UTC partout dans `manifest.json` et dans les noms de fichiers
  d'artefact.
- Un `manifest.json` par run, jamais partagé entre deux runs.
- Jamais d'envoi vers un hébergeur public : les artefacts restent dans
  `.azdone/proofs/<date ISO>/`, sous le contrôle du dépôt.
- Toute valeur sensible (identifiant, jeton, donnée personnelle visible à
  l'écran) devient `redacted` avant d'écrire l'artefact ou le manifest.
- L'artefact est la preuve. Le manifest est son index : il pointe vers
  l'artefact, il ne le remplace jamais.
