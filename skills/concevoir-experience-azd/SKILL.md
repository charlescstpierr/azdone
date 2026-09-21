---
name: concevoir-experience-azd
description: "Concevoir l'expérience de toute surface humaine: web, mobile, desktop, CLI, TUI, IDE, chat, rapport ou notification. Utiliser lorsque l'interaction, le contenu, l'accessibilité, la présentation, un prototype, une capture, un wireframe ou une conversation doivent être décidés avant l'implémentation."
---

# Étape 05 · Concevoir l'expérience

Concevoir la surface humaine avant que le code ne la fige, avec une discipline `evidence-first`.

## Quick start

```text
$concevoir-experience-azd "Conçois l'état empty/error/success du tableau de bord mobile"
```

Artefact attendu: `design.verdict: selected | partial | blocked | authority-request`, prototype ou wireframe, evidence visible et `UI acceptance matrix`.

## Utiliser quand

- un changement web, mobile, desktop, CLI, TUI, IDE, chat, report ou notification touche interaction, contenu, accessibility ou présentation;
- une décision matérielle de navigation, densité, IA, checkout, permissions, marque ou architecture d'information reste ouverte;
- un état loading, empty, error ou success doit être rendu vérifiable avant le handoff.

## Procédure

1. Lire Boussole (cadrage : utilisateur, problème, succès, limites), Language Pack (termes utiles à la carte active), design system existant, captures de la surface réelle et Proof Contract attendu, sans proposer une refonte à partir d'une surface imaginée.
2. Produire un `spec_review` (`placeholder_scan`, `ambiguity_scan`, `scope_check`, choix `authority-aware`, risques) avant tout prototype, en séparant faits, hypothèses, contraintes et décisions ouvertes.
3. Réutiliser les composants, tokens et patterns target-native du projet.
4. Produire le plus petit `professional prototype` qui rend la décision visible; comparer exactement trois directions seulement lorsqu'une décision matérielle touche navigation, densité, IA, checkout, permissions, marque ou architecture d'information (recommandation, alternative, statu quo, trade-offs pour chacune), sinon produire une seule direction.
5. Pour CLI/TUI, fournir obligatoirement un wireframe ASCII avant implementation; pour chat/report, fournir transcript ou rendu textuel équivalent.
6. Capturer screenshots desktop/mobile pour toute UI visuelle, et le transcript, wireframe ou rendu textuel pertinent pour CLI/TUI/chat/report.
7. Vérifier contenu, états loading, empty, error et success, navigation clavier, focus, contraste, zoom, reduced motion et lecture d'écran lorsque pertinents.
8. Produire une `UI acceptance matrix` avant le handoff: chaque état, interaction, viewport, artefact et exigence publique pointe vers son token/path/selector exact et vers un check exécutable; si le contrat impose `data-state`, un role ARIA ou un filename, conserver littéralement ce mécanisme.
9. Exiger que loading, empty, error et success existent réellement dans le prototype/DOM testable, même si un seul état est visible au chargement, et tester la transition et pas seulement la présence du texte.
10. Demander `human authority` avant un choix majeur de marque, navigation, prix, checkout, authentification, publication ou données sensibles.
11. Enregistrer la direction (`selected_direction`), l'evidence visible, les risques et le prochain skill.

## Sortie

Le skill rend `design` ([design-output.md](references/design-output.md)) avec les champs user_task, spec_review, directions, selected_direction, tradeoffs, prototype_paths, ascii_wireframes, screenshots, state_evidence, accessibility_checks, acceptance_matrix, authority_needed, verdict.

## Arrêt et interdits

- Arrêter quand une direction est visible, évaluée et autorisée pour l'implémentation.
- Ne pas déclarer un design accepté sans evidence visible, ni ignorer l'accessibility parce que l'UI paraît simple.
- Fail closed si screenshots ou checks a11y attendus ne peuvent pas être produits; marquer `partial` ou `blocked`.

Répondre dans la langue de l'utilisateur. Commandes, chemins, identifiants, gates et verdicts restent identiques en français et en anglais.
