### Run autonome

**Définir le prédicat de sortie avant la première itération, puis le conduire sans s'arrêter.**

1. Déclarer le prédicat de sortie observable (tests verts, reproduction corrigée, N PR livrées) avant toute itération. Il ne se relâche jamais pour déclarer une victoire.
2. Choisir le mécanisme de réveil : un événement (CI, merge, ref) reçoit un `azd-watcher` ; sinon un intervalle fixe dimensionné à la fréquence utile.
3. Chaque itération applique le plus petit changement justifié par la preuve via `$construire-solution-azd`, le vérifie via `$prouver-resultat-azd`, committe s'il avance, l'abandonne sinon.
4. Journaliser chaque itération dans `.azdone/decisions.tsv` : `horodatage | itération | changement | preuve | prédicat avancé (oui/non)`.
5. Traiter soi-même les découvertes réversibles en cours de run (skill cassé, bug lié, flaky). Ne réserver l'arrêt qu'à une action irréversible ou une décision produit sans expérience possible.
6. Un plateau n'est pas un arrêt. Changer d'approche. S'arrêter seulement sur prédicat atteint ou impasse réelle documentée.

Prédicat de sortie : le prédicat déclaré à l'étape 1 est vérifié avec preuve fraîche dans `.azdone/decisions.tsv`.

Réponse : le prédicat, les itérations menées, ce qui a été gardé ou abandonné, l'état final du prédicat.
