# Matrice de preuve par surface

Choisir la plus petite preuve capable de falsifier le claim.

| Surface | Preuves typiques | Ne prouve pas à elle seule |
| --- | --- | --- |
| Web | test fonctionnel, navigateur réel, viewport, clavier, accessibilité | qualité visuelle complète ou production |
| API | schéma, requêtes réelles, erreurs, auth, idempotence | comportement de tous les clients |
| CLI/TUI | stdout/stderr, exit code, interruption, tailles terminal | ergonomie sur chaque shell |
| Mobile/desktop | build, appareil ou simulateur, permissions, reprise | approbation d’un store |
| Data | dataset versionné, invariant, qualité, lineage, rollback | absence de biais hors corpus |
| Infra | plan, environnement ciblé, health, rollback, observabilité | sécurité absolue |
| Documentation | commandes rejouées, liens, exemple frais | compréhension de tous les lecteurs |
| Agent/chat | conversations humaines, continuité, récupération, latence | généralisation à tous les prompts |

## Verdicts séparés

- `functional_proof` répond au claim produit.
- `approval_readiness` compare un bundle aux exigences connues.
- `external_approval` exige un verdict réellement reçu de l’autorité externe.

Si l’oracle, l’environnement ou l’accès manque, retourner `blocked` ou
`partial`. Ne jamais abaisser le claim après l’échec pour obtenir `verified`.

