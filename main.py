import os
import json
import re
import argparse
from datetime import datetime

# Regex pour détecter les dates au format "YYYY-MM-DD HH:MM:SS"
DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

def convert_date_to_timestamp(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp() * 1000)

def process_json_file(file_path, backup=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON dans le fichier : {file_path}")
            return

    json_str = json.dumps(data)
    updated_json_str = DATE_PATTERN.sub(lambda m: str(convert_date_to_timestamp(m.group())), json_str)
    updated_data = json.loads(updated_json_str)

    if backup:
        os.makedirs('backup', exist_ok=True)
        backup_path = os.path.join('backup', os.path.basename(file_path))
        os.rename(file_path, backup_path)

    os.makedirs('transformed', exist_ok=True)
    with open(os.path.join('transformed', os.path.basename(file_path)), 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)

    print(f"Fichier traité : {file_path}")

def process_directory(directory, backup=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_json_file(file_path, backup=backup)

def main():
    parser = argparse.ArgumentParser(description="Convertir les dates dans les fichiers JSON en timestamps.")
    parser.add_argument('directory', help="Chemin du dossier contenant les fichiers JSON.")
    parser.add_argument('--backup', action='store_true', help="Créer une sauvegarde des fichiers originaux.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Le chemin spécifié n'est pas un dossier valide.")
        return

    process_directory(args.directory, backup=args.backup)

if __name__ == '__main__':
    main()