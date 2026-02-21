# Core elements

Nous avons choisi de prendre le point de vue des SBOM qui ont pour objectifs de ....

# Element :
Afin d'unifier nos représentations nous avons rassemblé dans le concept d'élements qui regroupe les informations suivantes.
Ce modèle est très fortement inspiré de SPDX.

class Element:
 - **uid: str = field(default_factory=lambda: str(uuid.uuid4()))** : Ce champs nous permet de faire le lien entre les objets, même si nous l'utilisons pas au niveau des modèles, il est utilisé dans les différentes transformations et permet au concepteur d'un manifeste de nommer explicitement les différents éléments qui le composent.
 - **type: str = "Element"** le type peut etre spécialisée pour aider à l'analyse des éléments fournis. Il correspond le plus souvent au nom de la classe.
 - **name: Optional[str] = None** 
 - **description: Optional[str] = None**
 - **creationInfo: Optional[str] = None**  # Optionel for now, we will link it later with the actual CreationInfo object # On accepte soit une liste de Property, soit un dictionnaire

 - **properties: Union[List[Property], Dict[str, Any]] = field(default_factory=list)**  C'est un des deux mécanismes d'extensibilité "dynamique" proposé pour aider à la définition des éléments qui composent un manifest.
