# Comprendre la confiance

AZDone n'accorde jamais d'autorite depuis un texte de skill. Seul un humain,
ou `.azdone/trust.yaml` qu'il a ecrit ou approuve, en accorde. Ce fichier
fixe combien d'actions sensibles `/azd` peut faire sans vous demander.

## Les quatre niveaux

| Action | guided | assisted | autonomous | full |
| --- | --- | --- | --- | --- |
| lecture, checks natifs | auto | auto | auto | auto |
| ecriture worktree isole | ask | auto | auto | auto |
| ecriture worktree principal (scope accepte) | ask | auto | auto | auto |
| commit | ask | auto | auto | auto |
| push, open_pr | ask | ask | auto | auto |
| merge | ask | ask | conditional | auto |
| deploy | ask | ask | ask | conditional |
| install_global, external_message | ask | ask | ask | auto |
| credentials, delete_data, rewrite_shared_history, always_pause | ask | ask | ask | ask |

`autonomous` est le niveau par defaut recommande par `/azd-setup`. Une
valeur explicite dans `actions:` prime sur le niveau, sauf pour `never` et la
liste toujours-pause.

## La liste toujours-pause

Non configurable. Une entree retiree du fichier est reappliquee par le skill
et par le hook :

- force-push sur une branche partagee ;
- suppression de donnees ou de branches non fusionnees ;
- mutation de production sans rollback prouve ;
- message a un client ou a un tiers ;
- usage ou creation de credentials ;
- elargissement de `trust.yaml` par l'agent lui-meme.

## `enforcement: declared | enforced`

`declared` : la politique guide le comportement de l'agent, sans verification
externe. C'est le seul mode disponible sous Codex.

`enforced` : sous Claude Code et Cursor, un hook (`hooks/azd-trust-guard.sh`)
lit `trust.yaml` avant chaque commande shell sensible et bloque celles que la
politique refuse, meme si l'agent tente quand meme. `/azd-setup` propose ce
mode et explique comment le desactiver.

## Confiance gagnee

Active par defaut. Apres cinq runs `verified` consecutifs sans rollback,
`/azd` propose de monter d'un cran, jusqu'au plafond `ceiling`. Un `failed` ou
un rollback retrograde immediatement. Chaque changement est ecrit dans
`.azdone/trust-ledger.md` : une ligne par run. La seule ecriture que l'agent
peut faire lui-meme dans `trust.yaml` est le champ `autonomy:`, lors d'une
promotion journalisee.

## Phrases de session

Dire « ne t'arrete pas », « jusqu'au bout », « sois autonome » ou « run until
done » traite la session comme `full` pour les actions reversibles, sans
toucher `always_pause` ni `never`. C'est journalise dans le ledger.

Suivant : [Modeles et sous-agents](04-modeles-et-sous-agents.md).
