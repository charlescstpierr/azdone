# azd-trust-guard.sh

Hook de confiance AZDone. Il lit la commande shell qu'un agent s'apprête à exécuter, la compare à `.azdone/trust.yaml` et bloque celles que la politique n'autorise pas. Bash pur (awk/grep/sed); `jq` est utilisé s'il est présent, jamais requis. Il n'installe rien et n'est jamais requis pour invoquer un skill AZDone.

## Ce qu'il fait

1. Détecte le format d'entrée (Claude Code ou Cursor).
2. Cherche `.azdone/trust.yaml` en remontant depuis le `cwd` reçu, ou utilise `$AZD_TRUST_FILE` s'il est défini (utile aux tests).
3. Si le fichier est absent, ou si `enforcement: declared`, il autorise sans rien afficher.
4. Sinon, il classe la commande (`push`, `open_pr`, `merge`, `deploy`, `delete_data`, `install_global`, ou toujours-pause pour un force-push) et applique la valeur correspondante de `actions:` dans `trust.yaml` (`auto | conditional | ask | never`).
5. `conditional` n'autorise que si `.azdone/conditions-ok` existe et date de moins de 30 minutes; ce témoin est écrit par `prouver-resultat-azd` ou `reviser-qualite-azd` après CI verte et revue indépendante acceptée.
6. La liste toujours-pause (force-push sur branche partagée, suppression de données, etc.) bloque même si `actions.*: auto` ou `autonomy: full`.

Une commande non classée (`ls`, `rm -rf` sous `/tmp`, etc.) est autorisée sans aucune sortie.

## Entrée et sortie par hôte

| Hôte | Entrée (stdin JSON) | Blocage (stdout, exit 0) | Autorisation |
| --- | --- | --- | --- |
| Claude Code | `{"hook_event_name":"PreToolUse","tool_input":{"command":"..."},"cwd":"..."}` | `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}` | exit 0, aucune sortie |
| Cursor | `{"hook_event_name":"beforeShellExecution","command":"...","cwd":"...","workspace_roots":["..."],"sandbox":"...","conversation_id":"...","generation_id":"..."}` | `{"permission":"deny","user_message":"...","agent_message":"..."}` (`permission` accepte `allow \| ask \| deny`) | exit 0, aucune sortie |

Cursor envoie aussi `hook_event_name`; le hook reconnaît le format Claude Code à la présence de `tool_input`, ou à `hook_event_name == "PreToolUse"`, jamais à la seule présence de `hook_event_name`.

## Activer ou désactiver

- Activer: mettre `enforcement: enforced` dans `.azdone/trust.yaml` (proposé par `$azd-setup`).
- Désactiver: remettre `enforcement: declared`, ou retirer `hooks/hooks.json` / `hooks/cursor-hooks.json` de l'installation du plugin.
- Sans le hook, la politique reste déclarée et lisible dans `trust.yaml`; aucun skill ne dépend de son exécution.

## Codex

Codex n'a pas de mécanisme de hook équivalent couvert ici. La confiance y reste déclarée seulement (`enforcement: declared`); aucun hook ne s'exécute et aucune commande n'y est bloquée par ce mécanisme.
