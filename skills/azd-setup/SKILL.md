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
4. Poser une seule question groupée sur `autonomy` et `ceiling`: recommandation `autonomy: autonomous`, `ceiling: full` par défaut. Contrainte stricte: `autonomy <= ceiling` (ordre `guided < assisted < autonomous < full`). Si l'humain choisit un `autonomy` supérieur au `ceiling` proposé, relever le `ceiling` d'autant ou refuser, et le dire. Montrer le tableau des quatre niveaux (référence: [trust.example.yaml](references/trust.example.yaml)).
5. Poser une seule question sur le budget de modèles: `small | medium | large | unlimited`.
6. Lire le cache de capacités par machine `~/.azdone/host-capabilities.json` (schéma, fraîcheur et interdits: [host-capabilities.md](references/host-capabilities.md)). Absent, illisible ou périmé, il est ignoré en silence et tout est sondé. Puis détecter les modèles par hôte, jamais en inventer: Claude Code -> `haiku`, `sonnet`, `opus` (alias natifs) plus `inherit`, toujours disponibles. Cursor -> `agent --list-models` si le CLI `agent` est présent, sinon `fast` et `inherit` seulement. Codex -> aucun listing vérifié; proposer `inherit` par défaut, n'accepter un slug exact que si l'humain le fournit et que `codex exec -m <slug> "<prompt trivial>"` réussit réellement (`--help` seul ne suffit pas).
6bis. Sous Codex, lire `~/.codex/config.toml` en lecture seule et y chercher `multi_agent = true`. Présent: les rôles `host:` sont des candidats réels et la question de l'étape 8 les propose. Absent ou fichier illisible: `subagents-unavailable`, proposer `cli:` pour `reviewer` et `second_reviewer`, et donner à l'humain la ligne exacte à ajouter lui-même. Ne jamais écrire dans `~/.codex/config.toml`: modifier une configuration globale relève de `install_global`, `ask` à tous les niveaux sauf `full`. Le flag rend les sous-agents natifs possibles, il ne les prouve pas: un run qui n'obtient pas de sous-agent retombe sur `subagents-unavailable` et le dit.
7. Chercher `codex`, `claude`, `agent` (CLI Cursor; `cursor-agent` en repli) sur le PATH pour les adaptateurs CLI. Pour chaque CLI trouvée, exécuter `<cli> --help` et confirmer les drapeaux réels avant d'écrire une commande d'adaptateur. Ne jamais écrire une commande d'adaptateur non confirmée par `--help`; à défaut, laisser l'adaptateur absent et le signaler dans la réponse. Un adaptateur du cache dont le binaire n'est plus sur le `PATH` est retiré et resondé; un `--help` ou un `codex exec` en cache depuis plus de 30 jours est rejoué, jamais réutilisé tel quel.
8. Poser une seule question groupée « Modèle par rôle » listant les six rôles (`scout`, `builder`, `verifier`, `reviewer`, `second_reviewer`, `watcher`) avec une recommandation par rôle (`scout: host:small`, `builder: host:default`, `verifier: host:default`, `reviewer: host:strong`, `second_reviewer: cli:codex` si `codex` confirmé à l'étape 7, sinon vide, `watcher: host:small`) et la liste des valeurs détectées à l'étape 6. Quand une valeur vient du cache, afficher son âge à côté. L'humain accepte le tout ou change des rôles un par un. Règle stricte: ne jamais écrire un slug non détecté à l'étape 6 ou non confirmé par l'humain.
9. Construire le fichier complet à partir du gabarit [trust.example.yaml](references/trust.example.yaml), avec les choix de l'humain (`autonomy`, `ceiling`, `models.roles`, `models.panels.review`) et les seuls adaptateurs confirmés. N'écrire sous `actions:` que les trois `never` et les surcharges explicitement demandées par l'humain ; les autres actions suivent le niveau et évoluent avec lui lors d'une promotion, une clé écrite les figerait.
10. Montrer le fichier complet avant toute écriture. Écrire `.azdone/trust.yaml`, puis amorcer `.azdone/trust-ledger.md` avec l'en-tête de [trust-ledger.example.md](references/trust-ledger.example.md) (en-tête seul, sans les lignes d'exemple), puis exécuter `python3 <hooks>/azd-trust-guard.py setup` quand l'outil est disponible pour journaliser le niveau initial (sans lui, ajouter à la main une ligne `setup` au format de l'exemple). Recommander d'ajouter `.azdone/conditions-ok` au `.gitignore` du projet, et de versionner `trust.yaml`, `trust-ledger.md` et `decisions.tsv`. Fusionner ensuite les faits sondés aux étapes 6, 6bis et 7 dans `~/.azdone/host-capabilities.json` et nommer ce chemin dans la réponse: une écriture hors du dépôt n'est jamais silencieuse. N'y écrire aucune décision.
11. Sur Claude Code ou Cursor, vérifier qu'un hook est réellement enregistré (plugin installé, ou `.claude/settings.json` / `.cursor/hooks.json` référençant `azd-trust-guard.sh`). Si oui, proposer `enforcement: enforced` et expliquer le hook `hooks/azd-trust-guard.sh`: il bloque push/merge/deploy interdits, ne bloque jamais en silence, et la liste toujours-pause reste non contournable. Sinon, écrire `enforcement: declared`, expliquer comment enregistrer le hook (bloc affiché par `scripts/install.sh`) et le dire explicitement dans la réponse.
12. Sur les trois hôtes, si l'humain accepte, ajouter une ligne pointeur dans le fichier de contrôle existant du projet (`CLAUDE.md` ou `AGENTS.md`): « Toute tâche non triviale passe par /azd (voir .azdone/trust.yaml) ». Ne jamais créer de second fichier de contrôle. Le fichier du projet passe toujours en premier. Un fichier de contrôle global (`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`) n'est touché que si l'humain le demande explicitement dans le tour courant, parce qu'il gouverne aussi ses dépôts sans `.azdone/`.
13. Rendre le bloc de sortie et le verdict.

## Sortie

```yaml
azd_setup:
  host: claude-code | cursor | codex
  trust_path: .azdone/trust.yaml
  autonomy: guided | assisted | autonomous | full
  ceiling: guided | assisted | autonomous | full
  enforcement: declared | enforced
  adapters_available: []
  host_capabilities_cache: read | written | absent | ignored
  codex_multi_agent: true | false | unknown | not-applicable
  next_safe_action: ""
  verdict: configured | already-configured | authority-required | blocked
```

## Arrêt et interdits

- Ne jamais écrire une commande d'adaptateur CLI non confirmée par `--help`.
- Ne jamais écrire un slug de modèle non détecté à l'étape 6 ou non confirmé par l'humain.
- Ne jamais élargir `actions.*` au-delà de ce que l'humain a approuvé; `never` et `always_pause` restent non modifiables par ce skill.
- Ne jamais écraser un `trust.yaml` existant sans montrer le contenu et obtenir un accord.
- Ne jamais installer de dépendance ni activer un hook sans le dire explicitement.
- Ne jamais écrire `enforcement: enforced` sans preuve qu'un hook est enregistré.
- Ne jamais écrire `autonomy` au-dessus de `ceiling`.
- Ne jamais écrire dans `~/.codex/config.toml`; `multi_agent` se détecte, se documente et s'ajoute par l'humain.
- Ne jamais écrire une décision (`autonomy`, `ceiling`, `enforcement`, `actions.*`, `models.*`) dans `~/.azdone/host-capabilities.json`; ce cache ne contient que des faits sondés.
- Ne jamais modifier un fichier de contrôle global sans demande explicite de l'humain dans le tour courant.
