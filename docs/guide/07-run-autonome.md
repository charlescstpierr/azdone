# Lancer un run autonome

Le playbook `run-autonome` mène un travail long sans que vous restiez à
côté, sans jamais relâcher son prédicat de sortie.

## Donnez un prédicat vérifiable

```text
/azd je pars pour la nuit. migre chaque appelant du store synchrone vers le nouveau store async, garde le comportement identique. continue jusqu'à ce que le check de migration rapporte zéro appelant restant.
```

« continue jusqu'à ce que X rapporte zéro » est le prédicat de sortie. `/azd`
le déclare explicitement au début du run et ne le redéfinit jamais en cours
de route pour se faciliter la tâche.

## Ce qui est journalisé

Chaque décision matérielle est écrite dans `.azdone/decisions.tsv` : quoi,
pourquoi, alternative rejetée, preuve. Chaque run se termine dans
`.azdone/trust-ledger.md` avec son verdict, ses actions automatiques
exécutées, et s'il y a eu rollback.

## Phrases reconnues

« ne t'arrête pas », « jusqu'au bout », « sois autonome », « run until
done » élèvent la session au niveau `full` pour les actions réversibles.
`always_pause` et les actions `never` restent bloquées quoi que vous disiez :
credentials, suppression de données, message à un tiers, élargissement de
`trust.yaml`.

## Itération

Le run boucle : construire, prouver, ajuster si le verdict n'est pas
`verified`, puis re-vérifier. Il s'arrête quand le prédicat est atteint, ou
quand une action `always_pause` se présente, avec une `next_safe_action`
précise pour vous au réveil.

## Reprendre après coupure

```text
/azd reprends le run d'hier soir sur la migration du store. vérifie l'état git avant de continuer.
```

Le playbook `reprise-de-session` recharge `resume_context`, vérifie l'état
Git, rafraîchit les preuves périmées, et continue depuis la dernière
transition prouvée plutôt que depuis la mémoire seule.

Suivant : [Recettes et pièges](08-recettes-et-pieges.md).
