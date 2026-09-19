# Trust ledger AZDone

Une ligne par run, plus une ligne par promotion, rétrogradation ou override de session. Ajouter seulement; ne jamais réordonner ni éditer une ligne existante.

| date | run_id | risk | verdict | actions_auto | rollback | override | niveau_effectif | série | événement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-10T14:03:00Z | run-041 | standard | verified | commit,push | non | - | assisted | 4 | run |
| 2026-09-11T09:12:00Z | run-042 | standard | verified | commit,push,open_pr | non | - | assisted | 5 | run |
| 2026-09-11T09:12:00Z | run-042 | standard | verified | - | non | - | autonomous | 0 | promotion:assisted->autonomous |
| 2026-09-14T16:47:00Z | run-043 | standard | failed | commit | oui | - | autonomous | 0 | run |
| 2026-09-14T16:47:00Z | run-043 | standard | failed | - | oui | - | assisted | 0 | demotion:autonomous->assisted |

`événement` vaut `run`, `promotion:<de>-><vers>`, `demotion:<de>-><vers>` ou `override-session`. `run-042` porte le cinquième `verified` consécutif sans rollback: `autonomy` passe de `assisted` à `autonomous` dans `trust.yaml`, journalisé par la ligne `promotion`. `run-043` échoue avec rollback: `autonomy` redescend immédiatement à `assisted`, journalisé par la ligne `demotion`.

Écriture par voie outillée seulement: `python3 <hooks>/azd-trust-guard.py record --run-id <id> --risk <r> --verdict <v> [--rollback] [--override "<phrase>"] --actions "<liste>"`. Cette commande ajoute les lignes ci-dessus et ne réécrit que la ligne `autonomy:` de `trust.yaml`. Sans `hooks/` disponible (Codex, mode déclaré), le skill écrit la ligne de ledger à la main au même format et applique la même règle de promotion ou de rétrogradation, en éditant seulement `autonomy:`.
