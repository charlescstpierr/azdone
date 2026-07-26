# Manifeste de l’édition publique

L’édition GitHub est une copie propre du package utilisateur, pas un push brut
du dépôt de construction.

## Inclus

- `skills/` complet;
- README français et anglais;
- documentation d’installation, d’architecture, de référence et de validation;
- contrats publics `CONTRACTS.md` et `HOW_IT_WORKS.md`;
- 63 tests de contrats publics;
- fichiers GitHub de contribution, support et sécurité;
- changelog et gitignore public.

## Exclus

- résultats et logs bruts d’évaluations externes;
- caches et captures;
- chemins locaux de machine;
- copies de sorties tierces;
- recherches de marque et archives de nommage;
- cartes internes Wayfinder et artefacts builder-only;
- état OMX et état de sessions;
- Doctor, daemon et vault non implémentés.

## Pourquoi

Les archives internes améliorent l’audit du builder, mais elles contiennent des
chemins privés, des données de host et des matériaux tiers inutiles pour
installer les skills. Le package public conserve les contrats et les preuves
reproductibles minimales sans transformer ces archives en surface produit.
