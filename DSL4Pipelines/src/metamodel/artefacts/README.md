# Artefacts

Les artefacts correspondent à des artefacts référencés, utilisés ou produits par les codes.

## Structure

### Core artefacts
A partir de SPDX (REFs) nous avons introduit les deux grandes familles d'artefacts  que nous avons un peu simplifiées
 - [Person](./artefacts.py) 
 - [SoftwareFile](artefacts.py) 

### ML artefacts
Nous avons spécialisé la notion de fichiers pour représenter des artefacts spécialisés en ML et leur ajouter des propriétés
  - [MLModel](./artefacts.py)
  - [Data](./artefacts.py)

### Metrics
Les métrics sont repris de la définition de ??C...??

Etant donné la forte évolutivité du domaine et donc d'extensibilité  et le besoin de vérifications 
nous exploitons les properties définies dans Element pour ajouter des informations et un catalogue pour définir et préciser les types de métrics, une méthode verify permet de verifier la validité des modèles et de compléter les catégories de metrics qi besoin...

## Technique
