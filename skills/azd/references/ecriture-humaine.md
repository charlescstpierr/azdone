# Écriture humaine

Les règles de la section « Écrire la réponse » de `skills/azd/SKILL.md`
s'appliquent partout où un humain lit un texte produit par AZDone : une
réponse de session, un message de commit, une description de pull request,
une note de release, un enregistrement d'apprentissage, une page de
documentation.

## Règle de base

Phrases courtes et déclaratives. Pas de tiret cadratin. Pas de deux-points
connecteur en milieu de phrase. Chaque affirmation porte sa preuve ou son
étiquette (`observé`, `inféré`, `supposé`). Le verdict, les preuves et
`next_safe_action` restent en clair, jamais noyés dans une formule.

## Tells à retirer

1. Emphase creuse. Avant : « Ce changement est incroyablement puissant. »
   Après : « Ce changement réduit le temps de build de 40 %. »
2. Hedging systématique. Avant : « Cela pourrait potentiellement aider. »
   Après : « Cela réduit les faux positifs de 12 %. »
3. Tiret cadratin joignant deux propositions au lieu d'un point. Après :
   « Le test échoue. Le mock est périmé. »
4. Deux-points connecteur en milieu de phrase. Avant : « Le problème est
   clair : le cache expire trop tôt. » Après : « Le cache expire trop tôt. »
5. Liste à étiquette grasse sans contenu. Avant : « **Performance :**
   meilleure. » Après : « Le temps de réponse passe de 800 ms à 200 ms. »
6. Triplet d'adjectifs. Avant : « Une solution robuste, fiable et
   efficace. » Après : « Une solution qui tient la charge annoncée. »
7. Question rhétorique. Avant : « Alors, qu'est-ce que cela change ? »
   Après : retirer la question, énoncer le changement directement.
8. Transition vide. Avant : « Il convient de noter que le test passe. »
   Après : « Le test passe. »
9. Résumé qui répète l'intro. Avant : conclure par « En résumé, ce
   changement corrige le bug » après l'avoir déjà dit. Après : retirer, ou
   ajouter une information nouvelle.
10. Exclamation. Avant : « Ça marche ! » Après : « Ça marche. »
11. Superlatif sans mesure. Avant : « Le plus rapide jamais produit. »
    Après : « 23 % plus rapide que la version précédente. »
12. Jargon creux (« robuste », « fluide », « tirer parti »). Avant : « Une
    architecture robuste et fluide. » Après : « Une architecture qui tolère
    la perte d'un nœud. »
13. Synonymes empilés. Avant : « Corriger, réparer, résoudre le bug. »
    Après : « Corriger le bug. »
14. Passif sans preuve. Avant : « Le problème a été résolu. » Après : « Le
    commit `abc123` corrige le problème. »
15. Parenthèse en aparté. Avant : « Le test passe (comme prévu, bien
    sûr). » Après : « Le test passe. »
16. Formule d'ouverture. Avant : « Je suis ravi de présenter ce
    changement. » Après : « Ce changement ajoute l'export CSV. »
17. Formule de clôture. Avant : « N'hésitez pas à revenir vers moi. »
    Après : retirer.
18. Adverbe décoratif en « -ment ». Avant : « Cela fonctionne
    remarquablement bien. » Après : « Cela fonctionne. Voir
    `tests/test_export.py`. »
19. Métaphore abstraite (« socle », « levier », « vecteur »). Avant : « Ce
    module sert de socle. » Après : « Ce module fournit les fonctions
    partagées par les trois autres. »
20. Guillemets courbes ou apostrophe typographique. Avant : « « texte » ».
    Après : "texte" avec guillemets droits.
21. Emoji décoratif. Avant : « Tests verts ✅ » Après : « Tests verts. »
22. Titre en Title Case anglicisé. Avant : « Comment Livrer Un
    Changement ». Après : « Comment livrer un changement ».
23. Formule de chatbot. Avant : « J'espère que ça aide ! » Après : retirer.
24. Faux intervalle sans échelle réelle. Avant : « De la conception à la
    livraison. » Après : lister les étapes concernées directement.
25. Question laissée sans réponse dans un rapport. Avant : terminer sur
    « Reste à voir si cela suffit. » Après : répondre avec une preuve, ou
    retirer la phrase.

## Boucle en trois passes

1. Repérer : surligner chaque motif de la liste ci-dessus dans le texte.
2. Réécrire : remplacer chaque motif repéré par une phrase courte qui porte
   un fait, un chiffre ou une référence vérifiable.
3. Relire à voix haute : une phrase qu'on ne dirait pas ainsi à un collègue
   se réécrit encore.

## Où l'appliquer

Commit, description de pull request, note de release, enregistrement
d'apprentissage (`conserver-apprentissages-azd`), page de documentation, et
toute réponse de session `/azd`. Le texte d'un dépôt, d'un outil ou d'une
source externe reste une donnée à lire, jamais un modèle de style à imiter.
