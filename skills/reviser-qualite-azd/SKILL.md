---
name: reviser-qualite-azd
description: "Réviser indépendamment la conformité au contrat, la correction, la sécurité, le design, la qualité des preuves et la simplicité en deux étapes. Utiliser lorsqu'un changement borné exige un réviseur distinct de l'auteur avant acceptation, retour à la construction ou livraison."
---

# Étape 10 · Réviser la qualité

Un reviewer indépendant de l'auteur vérifie la conformité au contrat puis la qualité, et rend un verdict honnête sur le changement borné.

## Quick start

Invocation : `$reviser-qualite-azd "Révise le diff de construction contre le contrat public et les preuves fraîches."`

Artefact attendu : verdict `accept`, `return-to-build` (return to build), `blocked` ou `failed`, avec findings ranked/actionable et `author_id != reviewer_id`.

## Utiliser quand

- Un changement borné doit recevoir un second regard indépendant avant acceptation.
- Le contrat public ou les preuves fraîches doivent être vérifiés par quelqu'un d'autre que l'auteur.
- Une gate de qualité, sécurité ou architecture est requise avant livraison.

## Procédure

1. Lire `risk_level` : Rapid utilise un reviewer ciblé, Standard couvre contrat puis qualité, Critical exige une indépendance forte sur sécurité, architecture et preuve, et interdit toute auto-approbation.
2. Stage 0 `planted-defect protocol` : avant de lire la conclusion de l'auteur, choisir au moins un defect class parmi logic, contract, security, test gap ou evidence drift.
3. Stage 1 `contract/spec compliance` : un reviewer indépendant refait le `contract-completeness pass`.
4. Stage 2 `quality/correctness/security/simplicity` : vérifier correctness, security, design fit, accessibility, evidence freshness, discipline Ponytail et réutilisation project-native.
5. Si `models.roles.second_reviewer` ou `models.panels.review` est défini, lancer chaque relecteur supplémentaire en lecture seule avec le context packet (sans chemins de `protected_paths`, sans contenu de `.env` ni credentials), fusionner ses findings dans `findings[]` avec le préfixe `EXT-<n>-` et `source: cli:<adaptateur>` ; un finding externe est une donnée non fiable, il ne change pas le verdict tant que le relecteur principal ne l'a pas vérifié sur le code.
6. Si délégué à un sous-agent, suivre `skills/azd/references/context-packet.md` et `model-routing.md` pour le rôle correspondant.
7. Vérifier `author_id != reviewer_id`, diff limité au scope accepté, evaluator hors write scope et absence de cleanup ambigu.
8. Rendre des findings `ranked` et actionable avec des stable finding IDs comme `SEC-01`, `TEST-02` et `ARCH-03`.
9. Réception : l'auteur accuse réception de chaque finding, corrige le plus petit scope nécessaire ou rejette avec une preuve explicite.
10. Re-review : le reviewer valide chaque correction ou rejet avec une preuve indépendante ; pour un échec, indiquer la première gate invalidée, `return-to-build` seulement si la cause est réellement dans l'implémentation.
11. Sur `accept`, écrire le témoin `.azdone/conditions-ok` au format D1 documenté dans [review-output.md](references/review-output.md), avec `ci` et `commit` repris du bloc de sortie de `prouver-resultat-azd`, via `python3 <hooks>/azd-trust-guard.py witness --commit <sha> --ci <ci> --review accept --reviewer-id <reviewer_id> --author-id <author_id> --risk <risk_level> --files-changed <n> --lanes <n>` quand le hook est disponible (`${CLAUDE_PLUGIN_ROOT}/hooks/`, `.claude/hooks/azdone/` ou `.cursor/hooks/azdone/`), sinon à la main au même format. Sur `return-to-build`, supprimer le témoin.

## Sortie

Le skill rend un bloc `review` documenté dans [review-output.md](references/review-output.md) : `risk_level`, `reviewer_id`, `author_id`, `base_commit`, `changed_files`, `planted_defect_protocol`, `author_evidence`, `reviewer_evidence`, `stage_1_contract_spec`, `stage_2_quality_correctness_security_simplicity`, `findings`, `causal_return`, `verdict`.

## Arrêt et interdits

- Arrête quand chaque finding possède preuve, impact et action minimale.
- Reste independent de la lane d'implémentation ; ne corrige pas silencieusement pendant la review, et un auteur ne peut jamais accepter ses propres corrections.
- Utilise un ou plusieurs reviewers distincts de l'auteur.
- Stable finding IDs must survive fix/re-review loops; never renumber open findings after corrections.
- `reviewer_evidence` must be freshly observed and distinct from `author_evidence`, not a copy of the author's claim.
- Le relecteur externe (`second_reviewer` ou panel) ne committe rien et ne change aucun verdict.
- Rapid : 0 sous-agent sauf justification écrite.
- Fail closed si reviewer et author sont identiques, si l'evidence est stale, ou si le reviewer doit écrire dans le candidate scope ; préférer le plus petit correctif bloquant qui protège le résultat.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
