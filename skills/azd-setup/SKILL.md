---
name: azd-setup
description: "Configurer une fois la politique de confiance et le routage des modèles AZDone. Utiliser pour /azd-setup, $azd-setup, configurer la confiance, choisir les modèles, avant la première exécution de /azd ou pour changer de niveau d'autonomie."
---

# Configurer la confiance

Écrit `.azdone/trust.yaml` et amorce `.azdone/trust-ledger.md`. Rejouable sans perte: relire avant d'écraser.

Règle de langue: répondre dans la langue de l'utilisateur; commandes, chemins, identifiants et verdicts restent identiques dans les deux langues.

## Quick start

```text
$azd-setup repository=.
```

Artefact attendu: `.azdone/trust.yaml` montré puis écrit, `.azdone/trust-ledger.md` amorcé, verdict `configured | already-configured | authority-required | blocked`.

## Utiliser quand

Avant la première exécution de `/azd` sans politique déclarée, ou pour changer de niveau d'autonomie, de budget de modèles ou d'adaptateurs CLI.

## Procédure

1. Détecter l'hôte (Claude Code, Cursor ou Codex) et confirmer que `repository` est un dépôt Git.
2. Lire `.azdone/trust.yaml` s'il existe déjà; ne jamais l'écraser sans montrer le contenu proposé et obtenir un accord explicite.
3. Si aucun setup AZDone n'existe (aucun fichier de contrôle, aucun `.azdone/`), appeler `$initialiser-projet-azd` avant de continuer.
4. Poser une seule question sur le niveau d'autonomie: recommandation `autonomous`, alternative `assisted`, statu quo le niveau déjà en place ou `guided`. Montrer le tableau des quatre niveaux (référence: [trust.example.yaml](references/trust.example.yaml)).
5. Poser une seule question sur le budget de modèles: `small | medium | large | unlimited`.
6. Chercher `codex`, `claude`, `agent` (CLI Cursor ; `cursor-agent` en repli) sur le PATH. Pour chaque CLI trouvée, exécuter `<cli> --help` et confirmer les drapeaux réels avant d'écrire une commande d'adaptateur. Ne jamais écrire une commande d'adaptateur non confirmée par `--help`; à défaut, laisser l'adaptateur absent et le signaler dans la réponse.
7. Construire le fichier complet à partir du gabarit [trust.example.yaml](references/trust.example.yaml), avec les choix de l'humain et les seuls adaptateurs confirmés.
8. Montrer le fichier complet avant toute écriture. Écrire `.azdone/trust.yaml`, puis amorcer `.azdone/trust-ledger.md` avec l'en-tête de [trust-ledger.example.md](references/trust-ledger.example.md) (en-tête seul, sans les lignes d'exemple).
9. Sur Claude Code ou Cursor, vérifier qu'un hook est réellement enregistré (plugin installé, ou `.claude/settings.json` / `.cursor/hooks.json` référençant `azd-trust-guard.sh`). Si oui, proposer `enforcement: enforced` et expliquer le hook `hooks/azd-trust-guard.sh`: il bloque push/merge/deploy interdits, ne bloque jamais en silence, et la liste toujours-pause reste non contournable. Sinon, écrire `enforcement: declared`, expliquer comment enregistrer le hook (bloc affiché par `scripts/install.sh`) et le dire explicitement dans la réponse.
10. Sur Claude Code, si l'humain accepte, ajouter une ligne pointeur dans le fichier de contrôle existant (`CLAUDE.md` ou `AGENTS.md`): « Toute tâche non triviale passe par /azd (voir .azdone/trust.yaml) ». Ne jamais créer de second fichier de contrôle.
11. Rendre le bloc de sortie et le verdict.

## Sortie

```yaml
azd_setup:
  host: claude-code | cursor | codex
  trust_path: .azdone/trust.yaml
  autonomy: guided | assisted | autonomous | full
  enforcement: declared | enforced
  adapters_available: []
  next_safe_action: ""
  verdict: configured | already-configured | authority-required | blocked
```

## Arrêt et interdits

- Ne jamais écrire une commande d'adaptateur CLI non confirmée par `--help`.
- Ne jamais élargir `actions.*` au-delà de ce que l'humain a approuvé; `never` et `always_pause` restent non modifiables par ce skill.
- Ne jamais écraser un `trust.yaml` existant sans montrer le contenu et obtenir un accord.
- Ne jamais installer de dépendance ni activer un hook sans le dire explicitement.
- Ne jamais écrire `enforcement: enforced` sans preuve qu'un hook est enregistré.
