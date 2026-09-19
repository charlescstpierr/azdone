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
| credentials, delete_data, rewrite_shared_history, always_pause | ask | ask | ask | ask |

`autonomous` est le niveau par défaut recommandé par `/azd-setup`. Une
valeur explicite dans `actions:` prime sur le niveau, sauf pour `never` et la
liste toujours-pause.

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

Suivant : [Modèles et sous-agents](04-modeles-et-sous-agents.md).
