# Journal de confiance AZDone

Une ligne par run. La promotion et la rétrogradation sont calculées à partir des dernières lignes, selon `earn.promote_after` et `earn.demote_on` dans `trust.yaml`. Ajouter seulement; ne jamais réordonner ni éditer une ligne existante.

| date | run_id | risk | verdict | actions auto exécutées | rollback | niveau effectif | streak |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-10 | run-041 | standard | verified | commit, push | non | assisted | 4 |
| 2026-09-11 | run-042 | standard | verified | commit, push, open_pr | non | autonomous | 5 → promotion |
| 2026-09-14 | run-043 | standard | failed | commit | oui | assisted | 0 → rétrogradation |

`run-042` porte le cinquième `verified` consécutif sans rollback: `autonomy` passe de `assisted` à `autonomous` dans `trust.yaml`, et la ligne le signale par `→ promotion`. `run-043` échoue avec rollback: `autonomy` redescend immédiatement à `assisted` et la ligne le signale par `→ rétrogradation`.
