# Positionnement d'AZDone

Ce fichier dit ce qu'AZDone cherche à être, et surtout ce qu'il ne cherche pas
à être. Il sert à décider si AZDone est le bon outil pour un besoin donné, et à
trancher les demandes d'évolution sans élargir le périmètre par accident.

## Le créneau

AZDone est **la voie multi-hôtes et la confiance vérifiable**.

Claude Code, Cursor et Codex. Un objectif mène à un verdict prouvé, sous une
politique d'autorité que l'humain écrit et versionne dans son propre dépôt.

Ce qui fait la valeur propre d'AZDone :

- `.azdone/trust.yaml` : la matrice action par niveau, la valeur `never` qu'aucun
  niveau ni aucune phrase de session ne lève, et la liste toujours-pause
  réappliquée par le skill et par le hook si une entrée est retirée.
- L'enforcement optionnel : sous les hôtes qui exposent des hooks,
  `hooks/azd-trust-guard.py` bloque les commandes shell que la politique refuse.
  Sous les autres, la politique reste déclarée, et cette limite est dite.
- Le ledger append-only des runs, et la confiance gagnée par runs `verified`
  consécutifs, dont la seule voie d'écriture est
  `azd-trust-guard.py record`.
- Les verdicts `verified | partial | blocked | failed`, chacun avec sa preuve et
  sa `next_safe_action`.
- Les cartes, le readiness forecast et le graphe de décisions, qui gardent
  l'état du projet repo-local et lisible par un humain.
- La portabilité entre hôtes : un seul jeu de skills, trois cibles
  d'installation, aucun runtime propriétaire.

## Non-objectifs

AZDone ne cherche pas à couvrir :

- **Les piles de PR outillées.** Pas de résolution de relations head/base, pas
  de découverte d'ancêtres et de descendants, pas de vérification programmatique
  du SHA de tête. La livraison passe par les capacités Git et GitHub de l'hôte,
  sous la politique de confiance.
- **Un catalogue de principes d'ingénierie.** Les décisions de méthode vivent
  dans les 18 skills et dans les conventions que `initialiser-projet-azd` écrit
  dans le dépôt, pas dans un corpus de principes nommables à part.
- **Un runtime.** Ni daemon, ni dashboard, ni base de données, ni service. Voir
  [HOW_IT_WORKS.md](../HOW_IT_WORKS.md) et la section « No hidden runtime » de
  [CONTRACTS.md](../CONTRACTS.md).
- **Une orchestration multi-worktree outillée.** `isoler-travail-azd` n'isole
  que les lanes réellement indépendantes, avec les outils de l'hôte.

Ces absences sont des choix, pas des manques à combler. Une demande qui exige
l'un de ces points relève d'un outil dédié à ce créneau, pas d'un
élargissement d'AZDone.

## Règle d'évolution

Avant d'ajouter une capacité, deux questions :

1. Est-ce que cette capacité a besoin de la politique de confiance pour avoir
   du sens ? Si non, elle est probablement hors créneau.
2. Est-ce que cette capacité tient sur les trois hôtes ? Si elle n'existe que
   sous un seul, elle appartient à un outil spécifique à cet hôte.

Ce qui touche l'autorité, la preuve et le verdict est au cœur d'AZDone. Ce qui
touche la mécanique outillée d'un hôte particulier ne l'est pas.

## Cohabitation avec d'autres jeux de skills

AZDone est conçu pour coexister :

- Les invocations sont namespacées quand AZDone est installé comme plugin :
  `/azdone:azd`, `/azdone:azd-setup`.
- L'état reste confiné dans `.azdone/`, à exclure des commits.
- N'activez pas deux modes de réalisation concurrents dans la même tâche. Deux
  vocabulaires de verdicts et deux conventions de modèles rendent le résultat
  illisible.
