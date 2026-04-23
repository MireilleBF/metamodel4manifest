import json
from pathlib import Path

import yaml

from tools.toFile import save_in_file


#@todo : add validation of the yaml file against a schema before transformation, to ensure that the input is correct and avoid errors during transformation.

def yaml_to_json(yaml_file_path, outputdir) -> Path:
    path = Path(yaml_file_path)
    #get the name of the file without extension
    filename = path.stem

    # 1. Charger le YAML
    with open(path, 'r', encoding='utf-8') as f:
        # Loader=yaml.SafeLoader est crucial pour la sécurité
        data = yaml.load(f, Loader=yaml.SafeLoader)

    # 2. Définir le nom de sortie
    #output_path = path.with_suffix('.json')
    output_path = Path(outputdir) / f"{filename}.json"

    # 3. Écrire le JSON
    save_in_file(str(output_path.parent),
                 output_path.name,
                 json.dumps(data, indent=4, ensure_ascii=False))
  #  with open(output_path, 'w', encoding='utf-8') as f:
        # indent=4 pour que ce soit lisible, ensure_ascii=False pour les accents
  #      json.dump(data, f, indent=4, ensure_ascii=False)

    return output_path