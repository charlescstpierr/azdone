# Feature map (gabarit)

Registre repo-local des fonctionnalités et de leur dernière preuve fonctionnelle observée. Amorcé une fois par `initialiser-projet-azd` (étape 7), mis à jour par `prouver-resultat-azd` après chaque `functional_proof`.

```yaml
features:
  - feature: ""
    comment_observer: ""
    surface: web | mobile | backend | api | infra | data | library | cli | tui | docs | workflow
    derniere_verification:
      commit: ""
      date: ""
      artefact: ""
    statut: verified | stale | never
```

## Champs

- `feature` : nom court et stable de la fonctionnalité, identique dans le temps.
- `comment_observer` : la commande, le scénario ou le chemin qui permet de constater le comportement (pas une affirmation, un moyen).
- `surface` : la surface livrée, au sens de `prouver-resultat-azd`.
- `derniere_verification.commit` : le commit vérifié lors de la dernière preuve fonctionnelle.
- `derniere_verification.date` : horodatage ISO-8601 de cette preuve.
- `derniere_verification.artefact` : chemin repo-local vers l'evidence (log, capture, rapport).
- `statut` : `verified` si la dernière preuve est fraîche et couvre le commit courant, `stale` si le commit a changé depuis, `never` si la fonctionnalité n'a jamais été prouvée.

## Règles

- Une entrée est amorcée par `initialiser-projet-azd` avec `statut: never` dès qu'une fonctionnalité connue existe dans le System Success Map ou le contrat public.
- `prouver-resultat-azd` met à jour l'entrée correspondante à chaque `functional_proof` rendu, jamais à partir d'une déclaration non vérifiée.
- La feature map n'est jamais un substitut à une preuve fraîche : un `statut: verified` périmé (commit différent, environnement changé) doit être relu comme `stale` avant tout usage dans un verdict.
- Aucune fonctionnalité listée ici ne peut justifier `Done` sans une preuve fraîche correspondante dans le run courant.
