### Reprise de session

**Le travail précédent fait autorité. Ne pas le refaire, reprendre depuis la dernière transition prouvée.**

1. Recharger `resume_context` : `base_commit`, `branch`, `worktree`, `current_step`, `remaining_work`, `next_safe_action`.
2. Vérifier l'état Git réel (`git status`, `git log`, `git diff` contre la base) et préserver tout changement utilisateur non intégré.
3. Rafraîchir les preuves périmées avant toute nouvelle écriture. Ne jamais recalculer `next_safe_action` depuis la seule mémoire.
4. Router le travail restant vers le playbook correspondant (`changement-code.md`, `correction-bug.md`, `run-autonome.md`) et continuer depuis la dernière transition prouvée.
5. `$prouver-resultat-azd` revérifie les claims hérités sur l'artefact réel avant de les considérer acquis.

Prédicat de sortie : chaque claim hérité a une preuve fraîche ou est explicitement recalculé. Rien n'est refait inutilement.

Réponse : où le travail précédent s'est arrêté, ce qui a été repris tel quel, ce qui a été revérifié, le point de reprise.
