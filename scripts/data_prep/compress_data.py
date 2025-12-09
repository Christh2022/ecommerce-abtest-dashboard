"""
Script pour compresser les fichiers CSV nettoyés
Utilisé avant de pousser vers GitHub pour réduire la taille
"""

import zipfile
import os
from pathlib import Path

def compress_csv_files():
    """Compresser les fichiers CSV en une archive ZIP"""
    
    data_dir = Path('data/clean')
    csv_files = ['users.csv', 'products.csv', 'sessions.csv', 'transactions.csv']
    zip_filename = 'retailrocket_cleaned_data.zip'
    zip_path = data_dir / zip_filename
    
    print('🗜️  Compression des fichiers CSV...')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for csv_file in csv_files:
            file_path = data_dir / csv_file
            if file_path.exists():
                print(f'  ✓ Ajout de {csv_file}...')
                zipf.write(file_path, csv_file)
                size = file_path.stat().st_size / (1024*1024)
                print(f'    Taille originale: {size:.1f} MB')
    
    zip_size = zip_path.stat().st_size / (1024*1024)
    print(f'\n✅ Archive créée: {zip_filename}')
    print(f'   Taille compressée: {zip_size:.1f} MB')
    
    return zip_path

def extract_csv_files():
    """Extraire les fichiers CSV de l'archive ZIP"""
    
    data_dir = Path('data/clean')
    zip_filename = 'retailrocket_cleaned_data.zip'
    zip_path = data_dir / zip_filename
    
    if not zip_path.exists():
        print(f'❌ Archive non trouvée: {zip_filename}')
        return False
    
    print('📦 Extraction des fichiers CSV...')
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file_info in zipf.filelist:
            print(f'  ✓ Extraction de {file_info.filename}...')
            zipf.extract(file_info, data_dir)
    
    print('\n✅ Fichiers extraits avec succès!')
    return True

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        extract_csv_files()
    else:
        compress_csv_files()
