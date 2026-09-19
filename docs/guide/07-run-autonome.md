# Lancer un run autonome

Le playbook `run-autonome` mene un travail long sans que vous restiez a
cote, sans jamais relacher son predicat de sortie.

## Donnez un predicat verifiable

```text
/azd je pars pour la nuit. migre chaque appelant du store synchrone vers le nouveau store async, garde le comportement identique. continue jusqu'a ce que le check de migration rapporte zero appelant restant.
```

« continue jusqu'a ce que X rapporte zero » est le predicat de sortie. `/azd`
le declare explicitement au debut du run et ne le redefinit jamais en cours
de route pour se faciliter la tache.

## Ce qui est journalise

Chaque decision materielle est ecrite dans `.azdone/decisions.tsv` : quoi,
pourquoi, alternative rejetee, preuve. Chaque run se termine dans
`.azdone/trust-ledger.md` avec son verdict, ses actions automatiques
executees, et s'il y a eu rollback.

## Phrases reconnues

« ne t'arrete pas », « jusqu'au bout », « sois autonome », « run until
done » elevent la session au niveau `full` pour les actions reversibles.
`always_pause` et les actions `never` restent bloquees quoi que vous disiez :
credentials, suppression de donnees, message a un tiers, elargissement de
`trust.yaml`.

## Iteration

Le run boucle : construire, prouver, ajuster si le verdict n'est pas
`verified`, puis re-verifier. Il s'arrete quand le predicat est atteint, ou
quand une action `always_pause` se presente, avec une `next_safe_action`
precise pour vous au reveil.

## Reprendre apres coupure

```text
/azd reprends le run d'hier soir sur la migration du store. verifie l'etat git avant de continuer.
```

Le playbook `reprise-de-session` recharge `resume_context`, verifie l'etat
Git, rafraichit les preuves perimees, et continue depuis la derniere
transition prouvee plutot que depuis la memoire seule.

Suivant : [Recettes et pieges](08-recettes-et-pieges.md).
