---
name: concevoir-experience-azd
description: "Concevoir l'expérience de toute surface humaine: web, mobile, desktop, CLI, TUI, IDE, chat, rapport ou notification. Utiliser lorsque l'interaction, le contenu, l'accessibilité, la présentation, un prototype, une capture, un wireframe ou une conversation doivent être décidés avant l'implémentation."
---

# Étape 05 · Concevoir l'expérience

Concevoir la surface humaine avant que le code ne la fige, avec une discipline `evidence-first`. Design the human-facing surface before code hardens it.

## Quick start

```text
$concevoir-experience-azd "Conçois l'état empty/error/success du tableau de bord mobile"
```

Artefact attendu: `design.verdict: selected | partial | blocked | authority-request`, prototype ou wireframe, evidence visible et `UI acceptance matrix`.

## Utiliser quand / Use when

Utiliser pour tout changement web, mobile, desktop, CLI, TUI, IDE, chat, report or notification qui touche interaction, contenu, accessibility ou présentation.

## Procédure / Procedure

1. Lire Boussole, Language Pack, design system existant, captures de la surface réelle et Proof Contract attendu. Ne pas proposer une refonte à partir d'une surface imaginée.
2. Produire un `spec_review`: `placeholder_scan`, `ambiguity_scan`, `scope_check`, choix `authority-aware`, et risques avant prototype.
3. Séparer faits, hypothèses, contraintes et décisions ouvertes.
4. Réutiliser les composants, tokens et patterns target-native du projet.
5. Produire le plus petit `professional prototype` qui rend la décision visible; comparer exactement trois directions seulement lorsqu'une décision matérielle touche navigation, densité, IA, checkout, permissions, marque ou architecture d'information. Pour chaque direction: recommandation, alternative, statu quo et trade-offs. Sinon produire une seule direction.
6. Pour CLI/TUI, fournir obligatoirement un wireframe ASCII avant implementation; pour chat/report, fournir transcript ou rendu textuel équivalent.
7. Capturer screenshots desktop/mobile pour toute UI visuelle; pour CLI/TUI/chat/report, capturer le transcript, wireframe ou rendu textuel pertinent.
8. Vérifier contenu, états loading/empty/error/success, navigation clavier, focus, contraste, zoom, reduced motion et lecture d'écran lorsque pertinents.
9. Produire une `UI acceptance matrix` avant le handoff: chaque état, interaction, viewport, artefact et exigence publique doit pointer vers son token/path/selector exact et vers un check exécutable. Si le contrat impose `data-state`, un role ARIA ou un filename, conserver littéralement ce mécanisme au lieu de le remplacer par un équivalent visuel.
10. Exiger que loading, empty, error et success existent réellement dans le prototype/DOM testable, même si un seul état est visible au chargement; tester la transition et pas seulement la présence du texte.
11. Demander `human authority` avant un choix majeur de marque, navigation, prix, checkout, authentification, publication ou données sensibles.
12. Enregistrer la direction, l'evidence visible, les risques et le prochain skill.

## Sortie / Output

- design brief et non-objectifs;
- une ou trois directions selon incertitude, prototype(s) proportionné(s) et décision;
- screenshots/transcripts et preuve usability/accessibility;
- verdict `selected`, `partial`, `blocked` ou `authority-request`.

```yaml
design:
  user_task: ""
  spec_review:
    placeholder_scan: []
    ambiguity_scan: []
    scope_check: []
    authority-aware: []
  directions: []
  selected_direction: ""
  tradeoffs: [{direction: "", cost: "", delay: "", complexity: "", risk: "", reversibility: "", graph_impact: "", proof: ""}]
  prototype_paths: []
  ascii_wireframes: []
  screenshots: []
  state_evidence: []
  accessibility_checks: []
  acceptance_matrix: []
  authority_needed: []
  verdict: selected | partial | blocked | authority-request
```

## Arrêt et interdits / Stop and forbidden

- Arrêter quand une direction est visible, évaluée et autorisée pour l'implémentation.
- Ne pas déclarer un design accepté sans evidence visible, ni ignorer l'accessibility parce que l'UI paraît simple.
- Fail closed si screenshots ou checks a11y attendus ne peuvent pas être produits; marquer `partial` ou `blocked`.
- Garder critères et gates équivalents en Français and English.
