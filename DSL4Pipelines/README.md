
## Demontration of DSL4Pipelines

Voir dans le fichier "demo"

### Validation d'un manifeste de construction d'un SML : un fichier yaml qui décrit les étapes du pipeline et leurs relations

   1. Definition de la manière dont le modele a été construit :
      - présentation du fichier yaml : manifeste du pipeline
      - présentation du code de construction du pipeline à partir du manifeste
     
   2. Viusalisation mermaid du manifeste
   3. vérification de la validité du manifeste 
      - choix de règles
      - production du rapport de validation
   4. Modification du manifeste pour résoudre des erreurs de validation
   5.  re-vérification de la validité du manifeste après modification

### Production d'un manifeste à partir d'un notebook jupyter

   1. Présentation du notebook jupyter qui décrit les étapes du pipeline et leurs relations
   2. Présentation du code de construction du manifeste à partir du notebook jupyter
   3. Visualisation mermaid du manifeste généré à partir du notebook jupyter
   4. vérification de la validité du manifeste généré à partir du notebook jupyter
      - choix de règles
      - production du rapport de validation

### Transformation d'un SBOM en un manifeste de pipeline
pas fait encore, mais on peut imaginer que le SBOM décrit les composants d'un SML et que le manifeste de pipeline décrit les étapes de construction du SML à partir de ces composants.

   1. Présentation du SBOM qui décrit les composants d'un SML
   2. Présentation du code de construction du manifeste à partir du SBOM
   3. Visualisation mermaid du manifeste généré à partir du SBOM
   4. vérification de la validité du manifeste généré à partir du SBOM
      - choix de règles
      - production du rapport de validation
   5. Modification du SBOM pour résoudre des erreurs de validation
   6. re-génération du manifeste à partir du SBOM après modification
   7. re-vérification de la validité du manifeste après modification

### Definitions de règles de validation personnalisées

1. Présentation de la syntaxe pour définir des règles de validation personnalisées
2. Présentation d'exemples de règles de validation personnalisées
3. Application de règles de validation personnalisées à un manifeste de pipeline
4. Production du rapport de validation avec les règles personnalisées

## Perspectives

- Permettre de faire référence à d'autres fichiers yaml pour favoriser la réutilisation de composants