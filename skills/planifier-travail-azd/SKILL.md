---
name: planifier-travail-azd
description: "Planifier le travail en convertissant un résultat approuvé en cartes progressives, Project Decision Graph, DAG de phases, contrats de preuve, responsabilités et ordre causal. Utiliser avant l'exécution quand dépendances, readiness, propriétaires, chevauchements, reprise, rollback ou contrats DevEx doivent être verrouillés."
---

# Étape 06 · Planifier le travail

Transformer le résultat accepté en ordre exécutable et vérifiable. Turn the accepted outcome into an executable, verifiable order.

Wayfinder est domain-agnostic: ne jamais faire de CLI/API/SDK la surface par défaut. Appliquer le plan à produit, backend, infra, data, mobile, desktop, web, CLI, librairie, docs, migration et incident.

## Quick start

```text
$planifier-travail-azd "Planifie les tâches pour corriger l'onboarding accessible et vérifier web + CLI"
```

Artefact attendu: `plan.verdict`, carte active, états et liens du graphe, DAG de phases, `requirement_to_proof`, Proof Contract verrouillé, Readiness Forecast frais, ownership et contrat DevEx seulement si pertinent.

## Utiliser quand / Use when

- plusieurs étapes, owners ou preuves dépendent les uns des autres;
- le projet est assez large pour nécessiter destination, fog/frontier, décisions persistées, tickets ou reprise;
- une CLI, API ou SDK existe dans le scope et exige alors un contrat DevEx précis avant exécution;
- l'overlap doit être détecté avant le parallèle;
- l'intégration ou le rollback doit être prévu avant les edits.

## Procédure / Procedure

1. Partir de la Boussole, du Language Pack, de la System Success Map, du contrat de résultat, des ADR et des preuves fraîches.
2. Maintenir le Project Decision Graph: nœuds typés, liens causaux, evidence, confiance, invalidation et impact descendant. Ne pas créer un second graphe concurrent.
3. Utiliser les cartes progressives `Draft -> Needs Grilling -> Ready -> In Progress -> Review -> Done`; conserver `Blocked`, `Needs Revalidation`, `Rejected` et `Superseded`. Griller la carte juste avant sa frontière d'exécution, pas tout le backlog en profondeur.
4. Toute découverte hors scope devient une carte `Draft` liée. Toute décision matérielle expose recommandation, meilleure alternative, statu quo et trade-offs.
5. Pour grand projet, activer Wayfinder: destination, fog, frontier, decision ticket, cartes HITL/AFK, claims, blocking, reprise et tracker configuré par le setup. Si le tracker configuré est indisponible, demander l'autorité avant de créer un tracker de secours repo-local.
6. Construire un DAG de phases avec gates cumulatifs et commits fonctionnels. Paralléliser uniquement des nœuds réellement indépendants.
7. Pour CLI/API/SDK seulement si cette surface existe, écrire le contrat DevEx exact avant les tâches: commands, flags, stdout, stderr, exit codes, config precedence, idempotency et examples.
8. Construire la `requirement-to-proof map`, le verification overlay par surface et verrouiller le Proof Contract avant `Ready`: claim, oracle indépendant, outil, environnement, données/accès, artefact, seuil, freshness et condition d'échec.
9. Appeler `$verifier-readiness-azd` pour chaque carte candidate à `Ready`. Un gap matériel crée une carte prérequise et laisse avancer seulement les cartes indépendantes.
10. Donner à chaque tâche action, `author_id`, `reviewer_id`, dépendances, repo-local paths, commandes exactes, write scope, test rouge, test vert, preuve/evidence, sortie et reprise: no vague steps.
11. Dimensionner le staffing par scope utile, risque, inconnues et indépendance — jamais par nombre brut de fichiers. Rapid: 0 par défaut, maximum 1 aide; Standard: 1 à 3 lanes; Critical: 2 à 5 lanes incluant un verifier indépendant. Ne pas hardcoder un modèle.
12. Porter un contexte frais minimal: Boussole pertinente, carte, Language Pack, ADR touchés, Proof Contract, Readiness Forecast et checkpoint. Ne pas transmettre tout l'historique par défaut.
13. Détecter l'overlap; sérialiser les écritures couplées et garder evaluator hors candidate write scope.
14. Fixer ordering, intégration, recovery, resume checkpoints, rollback et plan `frozen`; toute nouvelle preuve matérielle invalide explicitement les nœuds concernés.

Voir [planning-contract.md](references/planning-contract.md) pour les détails Wayfinder, DevEx et tâche.

## Sortie / Output

- dependency graph;
- requirement-to-proof map;
- wayfinder map si activée;
- contrat DevEx CLI/API/SDK seulement si pertinent;
- ownership et overlap decisions;
- ordering, intégration, reprise et rollback;
- verdict `ready`, `partial`, `blocked` ou `authority-request`.

```yaml
plan:
  frozen: true
  risk_level: rapid | standard | critical
  active_card: {id: "", state: Draft | Needs-Grilling | Ready | In-Progress | Review | Done | Blocked | Needs-Revalidation}
  project_decision_graph:
    nodes: [{id: "", type: goal | decision | requirement | ticket | dependency | risk | proof | artifact | opportunity}]
    edges: [{from: "", to: "", type: depends-on | enables | blocks | proves | contradicts | supersedes | impacts}]
  phase_dag: [{phase: "", depends_on: [], gate: [], functional_commit: ""}]
  wayfinder: {enabled: false, destination: "", fog: [], frontier: [], tickets: [], resume: {}}
  devex_contract: {applies: false, surface: cli | api | sdk | none, commands: [], flags: [], stdout: [], stderr: [], exit_codes: [], config_precedence: [], idempotency: [], examples: []}
  dependency_graph: []
  requirement_to_proof: []
  proof_contracts: [{claim: "", oracle: "", tool: "", environment: "", access_data: [], artifact: "", threshold: "", freshness: "", failure: ""}]
  readiness_forecast: {verdict: ready | at-risk | waiting | authority-required | blocked}
  context_packet: {compass: "", card: "", language_pack: "", adrs: [], proof_contract: "", readiness_forecast: "", checkpoint: ""}
  staffing: [{role: "", model_hint: "", reasoning_effort: "", expected_output: ""}]
  resume_context: {base_commit: "", branch: "", worktree: "", current_step: "", remaining_work: [], failed_approaches: [], resume_commands: [], next_safe_action: "", blockers: []}
  tasks: [{author_id: "", reviewer_id: "", paths: [], commands: [], write_scope: [], dependencies: [], red: "", green: "", proof: [], exit: "", resume: ""}]
  evaluator_scope: outside-candidate-write-scope
  recovery: []
  rollback: []
  verdict: ready | partial | blocked | authority-request
```

## Arrêt et interdits / Stop and forbidden

- Arrêter lorsque chaque exigence possède owner, dépendances, preuve et sortie.
- Interdire `Ready` si le Proof Contract ou le Readiness Forecast manque, est périmé ou laisse un moyen de preuve obligatoire impossible.
- No vague steps, missing paths, missing commands, hidden dependency, ownership gap, same-worktree parallel writes, evaluator overlap ou parallèle sans overlap analysis.
- Fail closed si `author_id == reviewer_id` pour une tâche qui écrit.
- Fail closed si un contrat CLI/API/SDK manque stdout/stderr/exit codes/config precedence/idempotency alors que ces surfaces existent et changent.
- Préserver le même sens en Français and English.
