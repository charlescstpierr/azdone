---
name: prouver-resultat-azd
description: "Prouver chaque affirmation avec des preuves fraîches adaptées à la surface, des oracles gelés, une provenance et des verdicts honnêtes. Utiliser avant de déclarer terminé un changement, une livraison, un benchmark, une interface, une API, une CLI/TUI, des données, une infrastructure, une documentation ou un workflow."
---

# Étape 09 · Prouver le résultat

Prouve chaque affirmation avec une evidence fraiche et adaptee a la surface reelle.

## Quick start

Invocation : `$prouver-resultat-azd "Verifie le commit courant contre public-contract.json et la UI acceptance matrix."`

Artefact attendu : `claim-by-claim evidence matrix` avec commandes exactes, artefacts, provenance commit/agent, et statut `verified`, `partial`, `blocked` ou `failed`.

Lire [proof-matrix.md](references/proof-matrix.md) pour choisir une preuve adaptée à la surface sans confondre test local, readiness et approbation externe.

## Utiliser quand

- Un changement, une livraison ou une affirmation doit être vérifié contre ses exigences actuelles.
- Le Proof Contract est verrouillé et il faut confirmer que les gates ont réellement tourné.
- Un verdict honnête (`verified`, `partial`, `blocked`, `failed`) doit remplacer une déclaration de complétude non prouvée.

## Procédure

1. Relire le Proof Contract verrouillé et le Readiness Forecast ; confirmer que les outils, accès, données, environnements et oracles prévus ont réellement été utilisés.
2. Mapper chaque exigence vers un check et son oracle, et confirmer que l'oracle/evaluator est gelé et hors candidate write scope.
3. Détecter la surface livrée : `web`, `mobile`, `backend`, `API`, `infra`, `data`, `library`, `CLI`, `TUI`, docs, workflow ou mixte.
4. Choisir les gates natifs qui prouvent cette surface : `fresh tests`, `lint`, `types`, `build`, `runtime`, `visual`, screenshots, accessibility, conversation humaine, contract, migration, schema, performance ou observability.
5. Exécuter un `contract-completeness pass` littéral sur tokens, selectors, attributs, paths, schema fields, IDs, rôles, viewports et artefacts publics.
6. Pour UI, parcourir loading/empty/error/success, exercer clavier, focus persistant et live region ; pour chat/agent, rejouer des conversations représentatives et inspecter réponse, latence, continuité, récupération et friction.
7. Exécuter le `carryover_gate`, incluant le discovery carryover gate, sans perdre `discovery.contradictions`, staleness/divergences de version, `discovery.blind_spots`, risks et failure modes avec path/source, puis oracles, findings, rollback ou claims incomplètes ; tout champ requis manquant va dans `dropped_fields`.
8. Vérifier CLI/TUI seulement si la surface existe : `80x24`, `120x40`, clavier sans souris, stdout/stderr séparés, exit codes, SIGINT/interruption/annulation/timeout et texte non tronqué.
9. Enregistrer la provenance : `agent_id`, role, worktree, commit vérifié, commit evaluator/oracle, commandes, environnement et artefacts.
10. Construire un `evidence_graph` (claim, source, artifact, oracle ; supports, contradicts, derived_from, supersedes ; stale, superseded, contradicted, `revalidation_condition`).
11. Rendre trois verdicts distincts : `functional_proof` (le produit fait-il ce qui est promis), `approval_readiness` (le bundle satisfait-il les exigences actuelles des écosystèmes ciblés) et `external_approval` (une autorité externe l'a-t-elle réellement approuvé ; sans soumission et verdict observé, rester `not-requested`).
12. En cas d'échec, identifier la première hypothèse causalement invalidée et la gate de retour, sans renvoyer systématiquement au build.
13. Classer le drift et marquer toute affirmation non prouvée `partial`, `blocked` ou `failed`.

## Sortie

Le skill rend un bloc `verification` documenté dans [verify-output.md](references/verify-output.md) : `commit`, `worktree`, `provenance`, `detected_surfaces`, `surface_gates`, `evaluator`, `carryover_gate`, `evidence_graph`, `matrix`, `readiness_usage`, `functional_proof`, `approval_readiness`, `external_approval`, `causal_return`, `status`. Le coeur en est une `claim-by-claim evidence matrix` avec `claim`, `status`, `evidence`, `freshness`, `oracle` et `risk`.

## Arrêt et interdits

- Ne jamais utiliser de stale logs ni déclarer complet un travail invérifiable.
- Fail closed si un `dropped_field` requis existe ou si sa freshness boundary ne correspond plus au commit/environnement vérifié, ou si l'evaluator a été modifié par l'auteur candidat.
- Ne pas remplacer un check impossible par une supposition ; expliquer le blocker et la prochaine action sûre.
- Ne jamais présenter une conformité locale, une checklist ou une readiness comme l'approbation réelle de Google, Apple, Microsoft, OpenAI, Anthropic ou toute autre autorité.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
