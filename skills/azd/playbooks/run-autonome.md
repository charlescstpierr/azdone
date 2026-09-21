### Run autonome

**Définir le prédicat de sortie avant la première itération, puis le conduire sans s'arrêter.**

1. Déclarer le prédicat de sortie observable (tests verts, reproduction corrigée, N PR livrées) avant toute itération. Il ne se relâche jamais pour déclarer une victoire.
2. Choisir le mécanisme de réveil selon l'hôte : un événement (CI, merge, ref) reçoit un `agents/azd-watcher.md` réveillé par `/loop` sur Claude Code et Cursor ; sur Codex, aucun réveil vérifié, sonder par relance manuelle à un intervalle fixe.
3. Chaque itération applique le plus petit changement justifié par la preuve via `$construire-solution-azd`, le vérifie via `$prouver-resultat-azd`, committe s'il avance, l'abandonne sinon.
4. Créer `.azdone/` à la volée s'il n'existe pas encore, avec pour seul contenu `.azdone/decisions.tsv`, et le dire. Journaliser chaque itération dans ce fichier, tabulations, en-tête `ts	run_id	iteration	decision	alternative_rejetee	preuve	predicat_avance`.
5. Traiter soi-même les découvertes réversibles en cours de run (skill cassé, bug lié, flaky). Ne réserver l'arrêt qu'à une action irréversible ou une décision produit sans expérience possible.
6. Un plateau n'est pas un arrêt. Changer d'approche. S'arrêter seulement sur prédicat atteint ou impasse réelle documentée.
7. En fin de run long, proposer `$conserver-apprentissages-azd` sans l'imposer. Ne jamais écrire ou modifier un skill sans l'accord explicite de l'humain.
8. Journaliser le run avec `azd-trust-guard.py record` (ou à la main sans hook, voir [../references/trust-policy.md](../references/trust-policy.md)).

Prédicat de sortie : le prédicat déclaré à l'étape 1 est vérifié avec preuve fraîche dans `.azdone/decisions.tsv`.

Réponse : le prédicat, les itérations menées, ce qui a été gardé ou abandonné, l'état final du prédicat.
