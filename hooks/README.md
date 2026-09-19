# azd-trust-guard

Hook de confiance AZDone. Il lit la commande shell qu'un agent s'apprête à exécuter, la compare à `.azdone/trust.yaml` et refuse celles que la politique n'autorise pas. Deux fichiers : `azd-trust-guard.sh` (wrapper bash, builtins seulement) et `azd-trust-guard.py` (classifieur, bibliothèque standard Python 3, aucune dépendance). Il n'installe rien et n'est jamais requis pour invoquer un skill AZDone.

## Ce qu'il fait

1. Détecte le format d'entrée (Claude Code ou Cursor) et décode le JSON avec un vrai parseur, jamais par expression régulière.
2. Cherche `.azdone/trust.yaml` en remontant depuis le `cwd` reçu, ou utilise `$AZD_TRUST_FILE` s'il est défini (tests).
3. Fichier absent ou `enforcement: declared` : autorise sans rien afficher. Politique `enforced` illisible : refuse (fail-closed).
4. Découpe la commande sur `&&`, `||`, `;`, `|`, sauts de ligne, `$( )`, et ouvre `bash -c "..."` et `eval`. Chaque segment est classé ; le premier refus l'emporte.
5. Applique `actions.<action>` (`auto | conditional | ask | never`) avec les défauts du niveau `autonomy` quand la clé manque. `conditional` n'autorise que si le témoin `.azdone/conditions-ok` satisfait `conditions:` (voir « Témoin » ci-dessous).
6. La liste toujours-pause refuse quel que soit `actions.*` ou `autonomy: full`.

## Ce que le hook classe

| Classe | Exemples détectés | Décision |
| --- | --- | --- |
| toujours-pause : force-push | `git push --force`, `-f`, `--force-with-lease`, `--mirror`, refspec `+main`, `+HEAD:main` | refus |
| toujours-pause : suppression | `rm -r*` hors `/tmp` et hors dossiers d'artefacts (`node_modules`, `dist`, `build`, `.cache`, `target`, `.venv`...), tout chemin contenant `..`, `git branch -D`, `git push --delete` ou `:branche`, `git clean -f`, `find -delete`, `DROP TABLE`, `TRUNCATE TABLE`, `DELETE FROM` ou `UPDATE ... SET` sans `WHERE`, `gh repo delete` | refus |
| toujours-pause : credentials | `aws configure`, `gh auth`, `gcloud auth`, `az login`, `op`, `vault`, `docker login`, `npm login`, `git credential`, affectation `*_TOKEN=`, `*_SECRET=`, `*PASSWORD=`, `*API_KEY=` | refus |
| toujours-pause : historique partagé | `git filter-branch`, `filter-repo`, `reflog expire`, `gc --prune` | refus |
| toujours-pause : trust.yaml | toute écriture vers `.azdone/trust.yaml` (`>>`, `sed -i`, `cp`, `mv`...) | refus |
| toujours-pause : message client | e-mail, SMS et messagerie client (`sendmail`, `mail`, SendGrid, Twilio, Mailgun, Postmark, Intercom, Customer.io...) | refus |
| `commit` | `git commit` | selon politique |
| `push` | `git push` vers une branche de travail | selon politique |
| `open_pr` | `gh pr create`, `glab mr create` | selon politique |
| `merge` | `gh pr merge`, `glab mr merge`, `git merge` quand la branche courante est `main`/`master`/`develop`/`release*`, `git push` ciblant une de ces branches | selon politique |
| `deploy` | `terraform apply`, `kubectl apply`, `helm upgrade`, `vercel --prod`, `fly deploy`, `cdk deploy`, `pulumi up`, `gcloud run deploy`, `wrangler deploy`, `firebase deploy`, `docker push`, `npm publish`, `cargo publish`, `twine upload`, `make deploy`, `npm run deploy`, `./deploy.sh`, `gh release create`... | selon politique |
| `install_global` | `sudo`, `npm i -g`, `pip install --user`, `pipx`, `brew`, `apt`, `dnf`, `pacman`, `cargo install`, `go install`, `gem install`, `curl ... \| sh` | selon politique |
| `external_message` | `gh pr comment`, `gh pr review`, `gh issue comment`, `gh api` non GET, webhooks Slack, Discord, Telegram, Teams, `curl`/`wget`/`http` non GET vers un hôte externe (localhost exclu) | selon politique |
| `spawn_agent` | `codex exec` sans `-s read-only`, `claude -p` sans `--permission-mode plan` ni `--allowedTools`, `agent -p` (CLI Cursor, sans mode lecture seule) | selon politique (ask par défaut, auto en `full`) |
| `record_run` | `azd-trust-guard.py record`, `witness`, `status` | toujours auto |
| chemin protégé | écriture (`>`, `cp`, `mv`, `sed -i`, script...) vers une entrée de `protected_paths` ; la lecture (`cat`, `grep`, `git diff`...) passe | refus (ask) |
| hors dépôt | écriture (`>`, `>>`, `tee`, `cp`, `mv`, `sed -i`) vers un chemin absolu ou `~` hors de la racine du dépôt et hors `/tmp` | refus (ask) |
| outils natifs Write/Edit (Claude Code) | même règles pour `tool_input.file_path` : trust.yaml en toujours-pause, `protected_paths` et hors dépôt en ask | refus |

Le mot `deploy` seul ne déclenche rien : `cat docs/deploy.md` et `git push origin feature/deploy-fix` passent. Une commande non classée (`ls`, `npm test`, `pip install -r requirements.txt`) passe sans aucune sortie.

Limites connues, volontaires : `git rebase`, `git reset --hard`, `git checkout -- <fichier>` et `rm <fichier>` sans récursion ne sont pas gouvernés (travail local ordinaire, récupérable ou trop fréquent). Sous Cursor, les éditions de fichiers par l'outil natif ne sont pas interceptées (aucun événement bloquant avant édition n'est vérifié, `afterFileEdit` arrive après) ; seul le shell l'est. Un agent externe lancé en écriture (`spawn_agent`) exécute ses propres commandes hors du garde, d'où l'action dédiée. Le hook ne remplace ni la revue ni la politique déclarée que les skills appliquent d'eux-mêmes.

## Témoin `.azdone/conditions-ok`

Écrit par `reviser-qualite-azd` sur `accept`, via `python3 <hooks>/azd-trust-guard.py witness --commit <sha> --ci green --review accept --reviewer-id <id> --author-id <id> --risk <r> --files-changed <n> --lanes <n>`. Fichier `clé: valeur` (`commit`, `ci`, `review`, `reviewer_id`, `author_id`, `risk`, `files_changed`, `lanes`, `written_at`). Pour une action `conditional`, le hook vérifie : moins de 30 minutes ; `commit` égal à `HEAD` du dépôt ; `ci: green` si `conditions.require_green_ci` ; `review: accept` et `reviewer_id` différent de `author_id` si `conditions.require_independent_review` ; `risk` au plus `conditions.risk_ceiling` ; `files_changed` au plus `conditions.max_files_changed` ; `lanes` au plus `conditions.max_lanes`. La première condition violée est nommée dans le refus. `witness --review return-to-build` supprime le témoin. `conditions.budget_tokens` n'est pas vérifié par le hook, `/azd` l'applique.

## Ledger et promotion : `record`

`python3 <hooks>/azd-trust-guard.py record --run-id <id> --risk <r> --verdict verified|partial|blocked|failed [--rollback] [--override "<phrase>"] [--actions "<liste>"]` ajoute une ligne au ledger (`earn.ledger`, tableau Markdown `| date | run_id | risk | verdict | actions_auto | rollback | override | niveau_effectif | série | événement |`), calcule la série de runs `verified` consécutifs sans rollback depuis la dernière promotion ou rétrogradation, puis, si `earn.enabled`, monte `autonomy:` d'un cran à `earn.promote_after` (borné par `ceiling`) ou descend d'un cran sur `failed` ou `--rollback`. Il ne réécrit que la ligne `autonomy:` de `trust.yaml`. C'est la seule écriture de `trust.yaml` que le hook autorise à l'agent ; toute autre reste toujours-pause. `status` affiche niveau, plafond, mode, série, validité du témoin et intégrité. `setup` journalise le niveau courant après `/azd-setup` et réaligne le ledger. Sans hook (Codex, mode déclaré), `/azd` applique la même règle à la main.

`<hooks>` vaut `${CLAUDE_PLUGIN_ROOT}/hooks` en plugin, `.claude/hooks/azdone` ou `.cursor/hooks/azdone` après `scripts/install.sh`, `.agents/azdone` sous Codex.

## Entrée et sortie par hôte

| Hôte | Entrée (stdin JSON) | Refus (stdout, exit 0) | Autorisation |
| --- | --- | --- | --- |
| Claude Code | `{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"..."},"cwd":"..."}` ou, pour `Write`/`Edit`, `"tool_input":{"file_path":"..."}` | `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}` | exit 0, aucune sortie |
| Cursor | `{"hook_event_name":"beforeShellExecution","command":"...","cwd":"...","workspace_roots":["..."]}` | `{"permission":"deny","user_message":"...","agent_message":"..."}` | exit 0, aucune sortie |

Cursor envoie aussi `hook_event_name` ; le format Claude Code se reconnaît à la présence de `tool_input` ou à `hook_event_name == "PreToolUse"`.

## Intégrité de trust.yaml

Le hook compare `autonomy:` de `trust.yaml` au dernier `niveau_effectif` du ledger. S'ils diffèrent, le fichier a été modifié hors du circuit `record` (édition manuelle, script, patch) : toute action gouvernée est refusée jusqu'à ce qu'un humain relance `/azd-setup` ou `azd-trust-guard.py setup`. Les commandes non gouvernées (`ls`, tests) passent. Cette vérification ne repose sur aucun secret : un agent qui falsifie à la fois `trust.yaml` et le ledger le fait délibérément, et les deux fichiers sont versionnés, donc visibles dans `git diff`. Le hook n'a jamais accès au contenu d'un script exécuté : `python3 script.py` reste non classé ; c'est cette vérification d'intégrité, et non la classification, qui couvre ce cas.

## Sans python3

Le wrapper bash n'utilise que des builtins. Sans `python3` sur le PATH : aucune politique `enforced` trouvée, il autorise ; politique `enforced` trouvée, il refuse en expliquant que `python3` est requis ou qu'il faut repasser en `enforcement: declared`. Jamais d'autorisation silencieuse d'une politique qu'il ne peut pas appliquer.

## Activer, enregistrer, désactiver

- Plugin Claude Code ou Cursor : `hooks/hooks.json` et `hooks/cursor-hooks.json` enregistrent le hook automatiquement.
- Installation par `scripts/install.sh` : le script copie le hook dans `.claude/hooks/azdone/` ou `.cursor/hooks/azdone/` et affiche le bloc à ajouter dans `.claude/settings.json` ou `.cursor/hooks.json`. Il ne modifie jamais ces fichiers lui-même.
- `$azd-setup` n'écrit `enforcement: enforced` qu'après avoir vérifié qu'un hook est réellement enregistré.
- Désactiver : remettre `enforcement: declared`, ou retirer l'entrée de hook. Sans le hook, la politique reste déclarée et lisible ; aucun skill ne dépend de son exécution.

## Codex

Codex n'a pas de mécanisme de hook couvert ici. La confiance y reste déclarée seulement (`enforcement: declared`) ; aucune commande n'y est bloquée par ce mécanisme.
