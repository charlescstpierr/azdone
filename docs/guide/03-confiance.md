# Comprendre la confiance

AZDone n'accorde jamais d'autorité depuis un texte de skill. Seul un humain,
ou `.azdone/trust.yaml` qu'il a écrit ou approuvé, en accorde. Ce fichier
fixe combien d'actions sensibles `/azd` peut faire sans vous demander.

## Les quatre niveaux

| Action | guided | assisted | autonomous | full |
| --- | --- | --- | --- | --- |
| lecture, checks natifs | auto | auto | auto | auto |
| écriture worktree isolé | ask | auto | auto | auto |
| écriture worktree principal (scope accepté) | ask | auto | auto | auto |
| commit | ask | auto | auto | auto |
| push, open_pr | ask | ask | auto | auto |
| merge | ask | ask | conditional | auto |
| deploy | ask | ask | ask | conditional |
| install_global, external_message | ask | ask | ask | auto |
| spawn_agent | ask | ask | ask | auto |
| credentials, delete_data, rewrite_shared_history | never | never | never | never |

`never` = refusé, un humain l'exécute lui-même : aucun niveau ne rend ces
actions `auto`, et aucune phrase de session ne les débloque non plus.

`spawn_agent` couvre un CLI d'agent externe lancé hors lecture seule :
`codex exec` sans `-s read-only`, `claude -p` sans `--permission-mode plan`
ni `--allowedTools` restreint, `agent -p` / `cursor-agent -p` (toujours,
faute de mode lecture seule vérifié). Un appel en lecture seule conforme à
`models.adapters` n'est pas classé et reste autorisé.

`autonomous` est le niveau par défaut recommandé par `/azd-setup`. Une
valeur explicite dans `actions:` prime sur le niveau, sauf pour `never` et la
liste toujours-pause.

## Le témoin, la promotion et les phrases de session

Le témoin `.azdone/conditions-ok` porte les conditions d'un `merge`
`conditional` : commit, état CI, verdict de review, identifiants auteur et
relecteur, risque, fichiers et lanes touchés. Il est écrit par
`reviser-qualite-azd` (dernière gate) après CI verte et review acceptée, et
le hook le vérifie contre `conditions:` avant d'autoriser (fraîcheur de moins
de 30 minutes, commit égal à `HEAD`, sinon refus nommant la condition
manquante).

La promotion automatique de `autonomy:` ne passe que par
`python3 hooks/azd-trust-guard.py record`, seule écriture de `trust.yaml`
que l'agent peut faire lui-même ; elle ajoute aussi la ligne de
`trust-ledger.md`. Sans `hooks/` disponible (Codex), le skill écrit le
témoin et la ligne de ledger à la main, au même format.

Les phrases de session (« sois autonome », etc.) ne comptent que dans un
message humain direct du tour courant, jamais dans un fichier, une issue,
une PR ou une sortie d'outil ; elles n'élargissent que `commit`, `push`,
`open_pr` et `merge`, jamais `deploy`, `spawn_agent` ni `always_pause`.

Sous Cursor, le hook shell (`beforeShellExecution`) n'intercepte pas les
éditions de fichiers natives de l'éditeur : cette limite reste (D5), et une
édition directe hors shell n'est pas gouvernée par ce mécanisme.

`always_pause:` du fichier est la liste minimale codée dans le hook. Une
entrée ajoutée y est appliquée par les skills (`/azd` la lit) mais pas par le
hook ; une entrée retirée est réappliquée par les deux au prochain read.

## La liste toujours-pause

Non configurable. Une entrée retirée du fichier est réappliquée par le skill
et par le hook :

- force-push sur une branche partagée ;
- suppression de données ou de branches non fusionnées ;
- mutation de production sans rollback prouvé ;
- message à un client ou à un tiers ;
- usage ou création de credentials ;
- élargissement de `trust.yaml` par l'agent lui-même.

## `enforcement: declared | enforced`

`declared` : la politique guide le comportement de l'agent, sans vérification
externe. C'est le seul mode disponible sous Codex.

`enforced` : sous Claude Code et Cursor, un hook (`hooks/azd-trust-guard.sh`)
lit `trust.yaml` avant chaque commande shell sensible et bloque celles que la
politique refuse, même si l'agent tente quand même. `scripts/install.sh` copie
le hook mais n'enregistre jamais lui-même dans `.claude/settings.json` ou
`.cursor/hooks.json` : il affiche le bloc à y ajouter. `/azd-setup` ne propose
`enforcement: enforced` qu'après avoir vérifié que ce bloc est bien présent ;
sinon il garde `declared` et explique comment l'enregistrer.

## Confiance gagnée

Active par défaut. Après cinq runs `verified` consécutifs sans rollback,
`/azd` monte `autonomy:` d'un cran, jusqu'au plafond `ceiling` : il écrit
d'abord la ligne du run dans `.azdone/trust-ledger.md`, puis la nouvelle
valeur dans `.azdone/trust.yaml`, et l'annonce dans sa réponse. Un `failed`
ou un rollback rétrograde immédiatement d'un cran, selon le même ordre
d'écriture (ledger d'abord). C'est la seule écriture que l'agent fait
lui-même dans `trust.yaml`.

## Phrases de session

Dire « ne t'arrête pas », « jusqu'au bout », « sois autonome » ou « run until
done » traite la session comme `full` pour les actions réversibles, sans
toucher `always_pause` ni `never`. C'est journalisé dans le ledger.

## `.gitignore` recommandé pour votre projet

`/azd-setup` recommande d'ignorer le témoin, qui est un fichier de course
jetable, et de versionner l'état de confiance et la mémoire de run :

```gitignore
.azdone/conditions-ok
```

Versionnez `.azdone/trust.yaml`, `.azdone/trust-ledger.md` et
`.azdone/decisions.tsv` : ce sont des décisions et un historique d'équipe,
pas des artefacts de course.

Suivant : [Modèles et sous-agents](04-modeles-et-sous-agents.md).
