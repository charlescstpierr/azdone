---
name: ameliorer-workflow-azd
description: "Améliorer le workflow par une expérience longitudinale protégée avec worktrees isolés, baselines et évaluateurs gelés, séparation train/held-out/protected, détection de dérive, rollback et double review indépendante. Utiliser seulement lorsque des preuves répétées justifient une mutation contrôlée et une décision mesurable."
---

# Étape 14 · Améliorer le workflow

Teste une mutation de skill seulement quand des preuves répétées la justifient, dans un protocole isolé et réversible.

## Quick start

Invocation : `$ameliorer-workflow-azd "Teste si prouver-resultat-azd gagne en précision sur les évaluations protégées sans changer l'evaluator."`

Artefact attendu : `falsifiable hypothesis`, `candidate branch`, `isolated worktree`, baseline/evaluator gelés, résultats train/held-out/hidden oracle/protected regressions, deux reviews indépendantes, observation window, drift check, rollback proof, décision `keep | discard | rollback | human-gate | insufficient-evidence | fail-closed`.

## Utiliser quand

- Un signal répété, un benchmark confirmé ou une régression prouvent qu'une mutation contrôlée vaut le coût.
- Une hypothèse falsifiable sur un skill existant doit être testée sans mutation immédiate.
- Ne jamais l'activer automatiquement pendant un projet utilisateur ; le futur builder de self-evolution reste différé.

## Procédure

1. Charger la baseline acceptée, les source runs et les apprentissages gouvernés ; geler baseline snapshot, contrat de comportement, evaluator, thresholds, prompts, fixtures et rollback bundle avant tout edit candidat.
2. Formuler une `falsifiable hypothesis` unique : population cible, effet attendu, métriques, seuil minimal et rejet ; arrêter avec `insufficient-evidence` si l'idée vient d'une préférence ponctuelle.
3. Créer une `candidate branch` dans un `isolated worktree` du same repository, écritures limitées aux skills candidats, baseline commit enregistré.
4. Lier `author_id`, `reviewer_id` et `second_reviewer_id` distincts ; fail closed si l'auteur évalue, sélectionne les cas, modifie l'evaluator ou accepte sa propre candidate.
5. Garder `frozen evaluator`, oracles, `hidden oracle`, `protected regressions`, reviewer briefs et promotion criteria `outside_candidate_write_scope`, avec versions, paths et hashes.
6. Séparer strictement `train`, `held_out_eval`, `hidden_oracle` et `protected_regressions` avant l'essai ; l'auteur candidat ne voit que train.
7. Ajouter des forward-tests clean-room (nominal, edge, rejet) pour tout nouveau skill ou comportement public, hors write scope candidat.
8. Comparer baseline et candidate sous conditions identiques : runtime, model, authority, budgets, seeds, snapshots et host evidence capture.
9. Mesurer correctness et gates protégées before scoring/before comparing cost, latency, tokens, tool calls et interruptions.
10. Invalider toute évaluation `incomplete or interrupted` ; persister un resume checkpoint et rejouer la comparaison gelée complète depuis le dernier checkpoint de confiance avant toute promotion.
11. Traiter evaluator edits, oracle access, skipped cases, selective reruns, threshold changes, prompt leakage, reviewer collusion ou proxy optimisation comme `reward hacking` et `discard`.
12. Exiger deux reviews indépendantes avant promotion ; un désaccord donne `human-gate` ou `discard`. L'autorité explicite se lit dans `.azdone/trust.yaml` (`actions.<action>`) quand ce fichier existe ; sinon `authority-request`.
13. Traiter la promotion comme provisoire : ouvrir une observation window après `keep`, comparer le drift à la baseline, garder le rollback bundle prêt jusqu'à la fermeture de la fenêtre.
14. Si l'observation, le drift, les protected regressions ou la vérification du commit promu échouent, `rollback` vers la dernière baseline et prouver la récupération avec une preuve fraîche.
15. Toute preuve manquante, host evidence absente, conflit d'identité author/reviewer, artefact gelé modifié, run interrompu sans preuve de resume, ou exposition du hidden-oracle donne `fail-closed`.

Voir [evolve-details.md](references/evolve-details.md) pour les cohortes, l'indépendance, les verdicts, l'anti-reward-hacking, l'observation/drift/rollback, le resume et l'evidence host complets.

## Sortie

Le skill rend un bloc `evolve` documenté dans [evolve-output.md](references/evolve-output.md) : `hypothesis`, `baseline_commit`, `baseline_snapshot`, `author_id`, `reviewer_id`, `second_reviewer_id`, `independence`, `candidate`, `evaluator`, `cohorts`, `forward_tests`, `host_evidence`, `resume`, `raw_results`, `independent_reviews`, `anti_reward_hacking`, `deltas`, `promotion_observation_window`, `rollback`, `fail_closed_reason`, `verdict`.

## Arrêt et interdits

- Une candidate cannot broaden its own authority policy and must not touch evaluators, reviewers, forward-tests, fixtures or promotion criteria.
- Fail closed si l'auteur et un reviewer sont identiques, ou si l'evaluator/oracle est modifié après le freeze.
- Reward hacking (edits gelés, skip, selective reruns, proxy optimisation) donne toujours `discard`.
- Keep reste provisoire jusqu'à la fin de l'observation window sans drift ni régression.
- Ne jamais activer ce skill automatiquement pendant un projet utilisateur.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
