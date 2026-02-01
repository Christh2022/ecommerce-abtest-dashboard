"""
Script de téléchargement du dataset RetailRocket depuis Kaggle
Dataset: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

Prérequis:
1. Installer kaggle: pip install kaggle
2. Configurer l'API Kaggle:
   - Créer un compte sur kaggle.com
   - Aller dans Account > API > Create New API Token
   - Télécharger kaggle.json
   - Placer dans ~/.kaggle/ (Linux/Mac) ou C:\Users\<username>\.kaggle\ (Windows)
"""

import os
import sys
import zipfile
from pathlib import Path
import subprocess

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
KAGGLE_DATASET = "retailrocket/ecommerce-dataset"


def check_kaggle_installed():
    """Vérifier si kaggle CLI est installé"""
    try:
        import kaggle
        print(" Kaggle API installée")
        return True
    except ImportError:
        print(" Kaggle API non installée")
        print("\n Installation de Kaggle API...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            print(" Kaggle API installée avec succès")
            return True
        except:
            print(" Erreur lors de l'installation de Kaggle API")
            return False


def check_kaggle_credentials():
    """Vérifier si les credentials Kaggle sont configurées"""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        print(f" Credentials Kaggle trouvées: {kaggle_json}")
        return True
    else:
        print(f" Credentials Kaggle non trouvées")
        print(f"\n Instructions de configuration:")
        print(f"1. Créer un compte sur https://www.kaggle.com")
        print(f"2. Aller dans Account > API > Create New API Token")
        print(f"3. Télécharger le fichier kaggle.json")
        print(f"4. Placer dans: {kaggle_dir}")
        print(f"5. Sur Linux/Mac: chmod 600 {kaggle_json}")
        return False


def download_dataset():
    """Télécharger le dataset depuis Kaggle"""
    print(f"\n Téléchargement du dataset: {KAGGLE_DATASET}")
    print(f" Destination: {DATA_RAW_DIR}")
    
    # Créer le répertoire si nécessaire
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Télécharger le dataset
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        print("⏳ Téléchargement en cours...")
        api.dataset_download_files(
            KAGGLE_DATASET,
            path=DATA_RAW_DIR,
            unzip=True
        )
        
        print(" Téléchargement terminé!")
        return True
        
    except Exception as e:
        print(f" Erreur lors du téléchargement: {e}")
        print("\n Alternative: Téléchargement manuel")
        print(f"1. Aller sur: https://www.kaggle.com/datasets/{KAGGLE_DATASET}")
        print(f"2. Cliquer sur 'Download' (connexion requise)")
        print(f"3. Extraire le fichier ZIP dans: {DATA_RAW_DIR}")
        return False


def verify_files():
    """Vérifier que les fichiers ont été téléchargés"""
    print("\n Vérification des fichiers...")
    
    expected_files = [
        "events.csv",
        "item_properties_part1.csv",
        "item_properties_part2.csv",
        "category_tree.csv"
    ]
    
    missing_files = []
    found_files = []
    
    for filename in expected_files:
        filepath = DATA_RAW_DIR / filename
        if filepath.exists():
            size = filepath.stat().st_size / (1024 * 1024)  # MB
            print(f"   {filename} ({size:.1f} MB)")
            found_files.append(filename)
        else:
            print(f"   {filename} - MANQUANT")
            missing_files.append(filename)
    
    print(f"\n Résumé: {len(found_files)}/{len(expected_files)} fichiers présents")
    
    if missing_files:
        print(f"\n️  Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True


def show_dataset_info():
    """Afficher des informations sur le dataset"""
    print("\n" + "=" * 60)
    print(" DATASET RETAILROCKET - E-COMMERCE")
    print("=" * 60)
    print("\n Description:")
    print("  Dataset de comportement utilisateur sur un site e-commerce")
    print("  Période: 4.5 mois")
    print("  Source: RetailRocket recommender system")
    print("\n Fichiers:")
    print("  • events.csv - Événements utilisateur (views, addtocart, transaction)")
    print("  • item_properties_part1.csv - Propriétés des produits (partie 1)")
    print("  • item_properties_part2.csv - Propriétés des produits (partie 2)")
    print("  • category_tree.csv - Arborescence des catégories")
    print("\n Lien: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset")
    print("=" * 60)


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  TÉLÉCHARGEMENT DATASET RETAILROCKET")
    print("=" * 60)
    
    show_dataset_info()
    
    # Vérifications
    if not check_kaggle_installed():
        return 1
    
    if not check_kaggle_credentials():
        return 1
    
    # Téléchargement
    if not download_dataset():
        return 1
    
    # Vérification
    if not verify_files():
        return 1
    
    print("\n" + "=" * 60)
    print(" TÉLÉCHARGEMENT TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print(f"\n Fichiers disponibles dans: {DATA_RAW_DIR}")
    print("\n Prochaine étape:")
    print("   python scripts/preprocess_retailrocket.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
