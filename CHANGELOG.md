# Historique des versions

Toutes les modifications notables du package public sont documentées ici.

## Unreleased

- Licence stable à sélectionner.
- Pilot 0 humain à exécuter sur un dépôt frais.
- Compatibilité comportementale Claude Code à vérifier.

## 0.2.0-preview (2026-09-19)

- Couche d'entrée `/azd` et `/azd-setup` par-dessus les 17 skills existants,
  avec neuf playbooks (dont `prototype`, code jetable pour trancher une
  question par la mesure) et cinq rôles de sous-agents (`azd-scout`,
  `azd-builder`, `azd-verifier`, `azd-reviewer`, `azd-watcher`).
- Politique de confiance déclarative `.azdone/trust.yaml` : quatre niveaux
  (`guided`, `assisted`, `autonomous`, `full`), action `spawn_agent` pour un
  CLI d'agent externe hors lecture seule, liste toujours-pause non
  bypassable, valeur `never` (refusé, un humain l'exécute lui-même) pour
  `credentials`, `delete_data` et `rewrite_shared_history`, confiance gagnée
  après 5 runs `verified` consécutifs.
- Nouveau skill `verifier-application-azd` : génère un skill repo-local
  `verifier-<app>` qui lance et exerce l'application réelle en isolation ;
  `prouver-resultat-azd` l'exécute pour tout claim sur une surface
  exécutable ; feature map déplacée dans ce skill.
- Témoin `.azdone/conditions-ok`, écrit par la review finale et vérifié par
  le hook contre `conditions:` pour un `merge` `conditional`; promotion et
  rétrogradation automatiques d'`autonomy:` par la seule voie outillée
  `azd-trust-guard.py record`, qui journalise aussi `trust-ledger.md`.
- Phrases de session reconnues uniquement dans un message humain direct, qui
  n'élargissent que `commit`, `push`, `open_pr` et `merge`.
- `enforcement: enforced` optionnel sous Claude Code et Cursor via
  `hooks/azd-trust-guard.sh`; Codex reste en politique déclarée. Sous
  Cursor, le hook couvre les commandes shell, pas les éditions de fichiers
  natives (limite documentée).
- Modèles par rôle à quatre formes (`host:<tier>`, `host:<slug>`,
  `cli:<adaptateur>`, `cli:<adaptateur>:<slug>`), détection des modèles par
  hôte au setup, `models.panels.review` pour des relecteurs supplémentaires,
  et réveil de `azd-watcher` par hôte (`/loop` sous Claude Code et Cursor).
- Manifestes `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
  et `.cursor-plugin/plugin.json`; installation en plugin ou via
  `scripts/install.sh <claude|cursor|codex>`.
- CI GitHub Actions (`.github/workflows/tests.yml`) sur Python 3.11 et 3.12 :
  suite publique, syntaxe des scripts, compilation du hook Python, et
  validation JSON des manifestes.
- Guide `docs/guide/` en neuf pages, mis à jour de l'installation, de
  l'architecture, de la référence des skills et de la validation.
- Section « Trust policy » dans `CONTRACTS.md`.
- Suite `tests/test_plugin_packaging.py`.
- Protocole de preuve visuelle annotée dans `verifier-application-azd` :
  `.azdone/proofs/<date ISO>/` avec `manifest.json` (schéma pas à pas) et
  `report.md` généré, repli transcript horodaté plus captures quand aucun
  outil d'enregistrement n'existe.
- Référence partagée `skills/azd/references/ecriture-humaine.md` : tells
  d'IA à retirer avec exemple avant/après, boucle en trois passes, étendue
  aux commits, PR, notes de release et apprentissages.
- `inspecter-projet-azd` inventorie PR ouvertes, branches actives et travail
  non commité avant tout plan ; un chevauchement direct rend `blocked`.
- `docs/parcours.md` : le parcours AZDone en cinq temps sur une page, avec
  une section à copier en `PARCOURS.md` repo-local.

## 0.1.0-preview — 2026-07-26

- Première édition publique propre.
- 16 skills AZDone avec tokens français `<verbe>-<objet>-azd`.
- Initialisation repo-locale une seule fois.
- Readiness transversale, cartes, Project Decision Graph et langage partagé.
- Documentation Codex et Claude Code.
- Suite publique de contrats sans dépendance Python externe.
- Templates GitHub, contribution, support et sécurité.

