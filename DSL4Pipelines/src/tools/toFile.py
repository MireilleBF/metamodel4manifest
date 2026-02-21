import os


def save_in_file(path: str, file_name: str, input: str):
    file_path = os.path.join(path, file_name)
    # 2. On crée le dossier s'il n'existe pas
    # exist_ok=True évite une erreur si le dossier est déjà là
    os.makedirs(path, exist_ok=True)
    # 3. On écrit le fichier
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(input)

    print(f"Fichier sauvegardé dans : {file_path}")