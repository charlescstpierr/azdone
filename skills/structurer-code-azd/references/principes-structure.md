# Dix principes de structure

Dix principes courts qui guident la procédure de `structurer-code-azd`. Chacun porte son terrain d'application et un exemple d'une ligne.

## 1. Formes de données d'abord

Nommer les formes de données avant d'écrire une fonction: la structure suit la donnée, pas l'inverse.
Quand il s'applique: dès qu'une nouvelle entité, un nouvel état ou un nouveau champ apparaît dans le changement.
Exemple: nommer `PaymentAttempt` avant d'écrire la fonction qui le traite.

## 2. Modéliser le domaine dans une structure

Un concept métier répété doit vivre dans un type ou une table, pas dans une suite de conditions dispersées.
Quand il s'applique: la même règle métier apparaît à plus de deux endroits du code.
Exemple: remplacer trois `if status == "paid"` par un type `PaymentStatus` fermé.

## 3. Frontières nettes

Valider aux bords, faire confiance aux types à l'intérieur, garder la logique pure au centre sans effet de bord caché.
Quand il s'applique: une fonction interne revalide des données déjà validées à l'entrée.
Exemple: le handler HTTP valide le payload une fois, le service qui suit ne revalide jamais.

## 4. Types qui interdisent les états illégaux

Choisir un type qui rend une combinaison impossible plutôt qu'un commentaire qui la déconseille.
Quand il s'applique: deux champs optionnels ne devraient jamais être vides ou remplis en même temps.
Exemple: une union `Draft | Published` plutôt que deux booléens `is_draft` et `is_published`.

## 5. Opérations idempotentes

Une opération rejouée avec la même entrée produit le même résultat observable, sans effet de bord dupliqué.
Quand il s'applique: un retry, un webhook ou une reprise après crash peut réexécuter l'opération.
Exemple: une clé d'idempotence sur la création de facture évite une facture en double.

## 6. Séparer avant de sérialiser l'état partagé

Isoler ce que des acteurs concurrents lisent ou écrivent ensemble avant de choisir son format de transport.
Quand il s'applique: deux workers ou deux requêtes touchent la même ressource en parallèle.
Exemple: séparer le compteur partagé du panier avant de décider s'il passe par JSON ou par une file.

## 7. Charge de lecture minimale

Compter les couches et l'état caché qu'un lecteur doit tenir en tête; supprimer une enveloppe qui n'a qu'un seul appelant.
Quand il s'applique: une abstraction ajoute une couche sans réduire de duplication réelle.
Exemple: écraser un wrapper à un seul appelant dans la fonction qui l'utilise.

## 8. Supprimer avant d'ajouter

Lister ce que la structure retenue permet de retirer avant d'écrire le nouveau code.
Quand il s'applique: une nouvelle structure remplace un mécanisme existant plutôt que de le compléter.
Exemple: retirer l'ancien registre de flags avant d'introduire la nouvelle machine à états.

## 9. Migrer les appelants puis supprimer l'ancien

Faire passer tous les appelants sur la nouvelle structure avant d'effacer l'ancienne, en une vague suivie.
Quand il s'applique: une structure change de forme publique et plusieurs appelants existent déjà.
Exemple: migrer les trois appelants d'une fonction avant de supprimer son ancienne signature.

## 10. Découper en unités vérifiables

Ordonner la structure retenue en tranches qui portent chacune sa propre preuve, jamais un bloc monolithique.
Quand il s'applique: la structure choisie touche plus d'un fichier ou plus d'une couche.
Exemple: une unité pour le nouveau type, une pour le premier appelant migré, une pour la suppression de l'ancien.
