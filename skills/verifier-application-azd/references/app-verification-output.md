# Sortie `app_verification`

```yaml
app_verification:
  mode: generer | executer | maintenir
  app: ""                        # nom court du projet, identique au suffixe de verifier-<app>
  skill_path: ""                 # chemin repo-local du skill généré (.claude/skills/verifier-<app>/SKILL.md, .cursor/skills/..., .agents/skills/...)
  commit: ""                     # commit vérifié
  started:
    command: ""
    isolation: port dédié | données de test | conteneur | simulateur | none
    health: ""                   # condition observée (URL 200, ligne de log, prompt affiché)
    status: ok | failed | not-applicable
  matrix:
    - feature: ""
      surface: web | mobile | backend | api | infra | data | library | cli | tui | chat | docs
      observation: ""            # ce qui a été fait : commande, parcours, requête, saisie
      expected: ""
      observed: ""
      artifact: ""               # .azdone/proofs/<date>/<fichier>
      status: verified | partial | blocked | failed
  non_nominal_covered: []        # vide, erreur, saisie invalide, interruption, 80x24...
  feature_map_updated: true | false
  gaps:
    - capability: ""             # navigateur, simulateur, fixture, compte de test
      recommendation: ""
      fallback: ""
      authority: automatic | human-required
  stopped: true | false
  verdict: verified | partial | blocked | failed
  next_safe_action: ""
```

## Règles de verdict

- `verified` : chaque fonctionnalité demandée a `status: verified` avec un artefact frais sur le commit vérifié.
- `partial` : au moins une fonctionnalité prouvée, au moins une non prouvée avec sa raison.
- `blocked` : l'application n'a pas pu démarrer en isolation, ou un moyen d'observation manque ; `gaps` et `next_safe_action` sont obligatoires.
- `failed` : une observation contredit le résultat attendu ; `prouver-resultat-azd` identifie la gate de retour.

## Artefacts

Les artefacts vivent sous `.azdone/proofs/<date ISO>/`, nommés `<feature>-<surface>.<ext>` (png, txt, json, log). Ils sont référencés par la feature map et par la matrice de `prouver-resultat-azd`. Ils ne contiennent ni secret ni donnée personnelle ; une valeur sensible est remplacée par `redacted`.
