# Comment fonctionne AZDone

AZDone est une série de skills Markdown ordinaires. Il n'ajoute ni runtime,
daemon, dashboard, base de données ni dépendance obligatoire. Le host compatible
exécute les outils, Git et les éventuels subagents; les skills prescrivent les
décisions, gates, artefacts et preuves.

## Première entrée dans un dépôt

Après installation du skill set, lancer une seule fois:

```text
$initialiser-projet-azd
```

L'étape 00 inspecte le dépôt puis fixe les conventions partagées: backlog,
cycle des cartes, labels, Git/livraison, risque, autorité, langage, ADR,
Boussole, graphe de décisions, readiness et preuve. Elle écrit un pointeur court
dans le fichier de contrôle agent existant et garde les détails dans des fichiers
repo-locaux éditables par l'humain.

Si le setup existe, l'init retourne `already-initialized` sans écrire. Un futur
changement de convention passe par une carte de migration explicite; AZDone ne
se réinitialise jamais automatiquement.

## Parcours normal

```text
Objectif
  │
  ▼
01 Piloter
  ├─ 02 Clarifier ── Boussole, langage, risque, une question matérielle
  ├─ 03 Inspecter ── dépôt, sources, capacités, opportunités
  ├─ 04 Diagnostiquer ── si la cause est inconnue
  ├─ 05 Concevoir ── si une surface humaine change
  ├─ 06 Planifier ── cartes, graphe, DAG, preuve, readiness
  ├─ 07 Isoler ── seulement les lanes réellement indépendantes
  ├─ 08 Construire ── plus petit changement valide
  ├─ 09 Prouver ── preuve fonctionnelle et readiness d'approbation
  ├─ 10 Réviser ── review indépendante proportionnée au risque
  ├─ 11 Livrer ── intégration et actions externes sous autorité
  ├─ 12 Surveiller ── si une livraison doit être observée
  ├─ 13 Conserver ── apprentissages prouvés et bornés
  └─ 14 Améliorer ── seulement après un signal répété
```

`$verifier-readiness-azd` est un socle transversal. Il s'exécute au bootstrap,
après un changement matériel, avant `Ready`, avant exécution si son forecast est
périmé et avant `Done`.

## Cartes et grilling

```text
Draft → Needs Grilling → Ready → In Progress → Review → Done
           │                │                      │
           └─ 1 question    └─ preuve verrouillée └─ evidence bundle
```

`Blocked`, `Needs Revalidation`, `Rejected` et `Superseded` préservent
l'historique. Avant une question, l'agent cherche les faits. Il présente une
recommandation, la meilleure alternative et le statu quo, avec coût, délai,
complexité, risque, réversibilité, impact sur le graphe et preuve nécessaire.

Une découverte hors périmètre ou une idée externe devient une carte `Draft`
liée. Elle ne gonfle jamais silencieusement la carte active.

## Architecture de réussite

L'init amorce quatre objets vivants:

- la **Boussole**: utilisateur, problème, succès, écosystèmes cibles,
  non-négociables, refus et non-objectifs;
- le **langage partagé**: Atlas universel, lexique métier, lexique technique et
  pont humain → métier → technique → preuve;
- la **System Success Map**: éléments produit, techniques, opérationnels et
  commerciaux, classés indispensable/recommandé/plus tard/hors périmètre/inconnu;
- le **Project Decision Graph**: liens entre objectifs, décisions, tickets,
  dépendances, risques, preuves, artefacts et opportunités.

Ces objets s'enrichissent pendant clarification, inspection et planification.
Ils ne sont pas tous figés au setup.

## Readiness et preuve

Avant `Ready`, chaque claim doit posséder:

```text
claim → oracle → outil → environnement → accès/données → artefact → seuil
```

Le preflight remonte tôt les besoins comme Playwright pour un site, un client
isolé pour Telegram, les comptes ou API, les appareils/simulateurs mobiles, les
datasets, licences, coûts et délais. Il recommande une option et un repli, mais
n'installe rien et n'utilise aucun credential sans autorité.

Trois verdicts restent distincts:

1. `functional_proof`: le produit remplit-il ses claims?
2. `approval_readiness`: le bundle semble-t-il satisfaire les exigences
   actuelles des écosystèmes ciblés?
3. `external_approval`: une autorité externe a-t-elle réellement approuvé?

Une checklist locale ne devient jamais une approbation Apple, Google,
Microsoft, OpenAI, Anthropic ou autre.

## Risque, contexte et subagents

- Rapid: zéro lane par défaut, une aide maximum.
- Standard: une à trois lanes indépendantes.
- Critical: deux à cinq lanes pertinentes, avec verifier indépendant.

Le staffing dépend du scope utile, des inconnues, du risque et de l'indépendance,
jamais du nombre brut de fichiers. Chaque lane reçoit un contexte frais minimal:
Boussole pertinente, carte, Language Pack, ADR, Proof Contract, Readiness
Forecast et checkpoint. Deux agents n'écrivent jamais dans le même worktree.

## Recherche, opportunités et mémoire

AZDone réutilise d'abord le dépôt, les outils et la mémoire locale. Il consulte
ensuite documentation officielle, standards et code source primaire lorsque
l'information externe peut changer la décision. X, Hacker News et tendances ne
sont que des signaux.

L'Opportunity Radar propose au plus trois idées à fort signal et les passe par
Dreamer, Destroyer et Investor. La mémoire repo-locale capture des candidats,
puis les promeut, revalide, supersède, retire ou expire. Elle reste bornée,
sourcée, non autoritative et sans daemon. Le vault Obsidian physique est différé.

## Échec et reprise

Après un échec de preuve, AZDone revient à la première hypothèse invalidée:
readiness, compréhension, diagnostic, design, plan ou build. Il ne renvoie pas
automatiquement au code et n'affaiblit jamais le claim ou l'oracle pour passer.

Chaque pause produit un checkpoint frais et une `next_safe_action`. Doctor ne
fait pas partie de ce parcours: c'est un futur outil du builder pour auditer un
pilote après coup.

La [référence publique](docs/reference-skills.md) décrit la responsabilité de
chaque skill. La traçabilité décision par décision, y compris les tickets
différés, bloqués, supersédés et les contrats Doctor non implémentés, reste un
artefact builder-only exclu de l’édition publique.
