# Historique des versions

Toutes les modifications notables du package public sont documentées ici.

## Unreleased

- Licence stable à sélectionner.
- Pilot 0 humain à exécuter sur un dépôt frais.
- Compatibilité comportementale Claude Code à vérifier.

## 0.2.0-preview — 2026-09-19

- Couche d'entrée `/azd` et `/azd-setup` par-dessus les 16 skills existants,
  avec huit playbooks et cinq rôles de sous-agents (`azd-scout`,
  `azd-builder`, `azd-verifier`, `azd-reviewer`, `azd-watcher`).
- Politique de confiance déclarative `.azdone/trust.yaml` : quatre niveaux
  (`guided`, `assisted`, `autonomous`, `full`), liste toujours-pause non
  contournable, confiance gagnée après 5 runs `verified` consécutifs.
- `enforcement: enforced` optionnel sous Claude Code et Cursor via
  `hooks/azd-trust-guard.sh`; Codex reste en politique déclarée.
- Adaptateurs de modèles `host:` et `cli:codex|claude|cursor` pour router
  chaque rôle vers un sous-agent natif ou un CLI externe.
- Manifestes `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
  et `.cursor-plugin/plugin.json`; installation en plugin ou via
  `scripts/install.sh <claude|cursor|codex>`.
- Guide `docs/guide/` en neuf pages, mis à jour de l'installation, de
  l'architecture, de la référence des skills et de la validation.
- Section « Trust policy » dans `CONTRACTS.md`.
- Suite `tests/test_plugin_packaging.py`.

## 0.1.0-preview — 2026-07-26

- Première édition publique propre.
- 16 skills AZDone avec tokens français `<verbe>-<objet>-azd`.
- Initialisation repo-locale une seule fois.
- Readiness transversale, cartes, Project Decision Graph et langage partagé.
- Documentation Codex et Claude Code.
- Suite publique de contrats sans dépendance Python externe.
- Templates GitHub, contribution, support et sécurité.

