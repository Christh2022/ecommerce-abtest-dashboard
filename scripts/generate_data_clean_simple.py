#!/usr/bin/env python3
"""
Script ultra-simple pour générer data_clean.csv
Copie events_enriched.csv avec colonnes renommées et réorganisées.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #6
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

print(f"\n{'='*80}")
print(f"  GENERATION DE DATA_CLEAN.CSV - Issue #6")
print(f"{'='*80}\n")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

start_time = datetime.now()

# Chemins
project_root = Path(__file__).parent.parent
data_dir = project_root / 'data' / 'clean'

print("Lecture de events_enriched.csv par chunks...")
print("(traitement optimisé pour fichiers volumineux)\n")

# Lire par chunks pour économiser la mémoire
chunk_size = 500000
chunks = []
i = 0

for chunk in pd.read_csv(data_dir / 'events_enriched.csv', chunksize=chunk_size):
    i += 1
    print(f"  Chunk {i}: {len(chunk):,} lignes")
    
    # Renommer les colonnes
    chunk.rename(columns={
        'visitorid': 'user_id',
        'itemid': 'product_id',
        'transactionid': 'transaction_id',
        'event': 'event_type',
        'view_count': 'product_views',
        'purchase_count': 'product_purchases'
    }, inplace=True)
    
    # Créer session_id
    chunk['session_id'] = chunk['user_id'].astype(str) + '_' + chunk['date'].astype(str)
    
    # Ajouter amount (NULL pour l'instant, sera enrichi plus tard si nécessaire)
    chunk['amount'] = None
    
    # Sélectionner et réordonner les colonnes
    final_cols = [
        'user_id', 'session_id', 'timestamp', 'date', 'hour', 'day_of_week',
        'event_type', 'product_id', 'transaction_id', 'amount', 'segment',
        'product_views', 'product_purchases'
    ]
    
    chunk = chunk[final_cols]
    chunks.append(chunk)

print(f"\nConcaténation de {len(chunks)} chunks...")
data_clean = pd.concat(chunks, ignore_index=True)

print(f"Tri par timestamp...")
data_clean = data_clean.sort_values('timestamp').reset_index(drop=True)

print(f"\n[RESULTAT] {len(data_clean):,} lignes x {len(data_clean.columns)} colonnes")

# Sauvegarder
print(f"\nSauvegarde...")
output_file = data_dir / 'data_clean.csv'
data_clean.to_csv(output_file, index=False)
file_size = output_file.stat().st_size / (1024 ** 2)

print(f"[OK] {output_file}")
print(f"     Taille: {file_size:.2f} MB")

# Statistiques rapides
print(f"\n{'='*80}")
print(f"  STATISTIQUES")
print(f"{'='*80}\n")

stats = {
    'timestamp': datetime.now().isoformat(),
    'source': 'events_enriched.csv',
    'total_rows': len(data_clean),
    'total_columns': len(data_clean.columns),
    'columns': list(data_clean.columns),
    'unique_users': int(data_clean['user_id'].nunique()),
    'unique_sessions': int(data_clean['session_id'].nunique()),
    'unique_products': int(data_clean['product_id'].nunique()),
    'events_by_type': data_clean['event_type'].value_counts().to_dict(),
    'users_by_segment': data_clean['segment'].value_counts().to_dict(),
    'period': {
        'start_date': str(data_clean['date'].min()),
        'end_date': str(data_clean['date'].max())
    },
    'file_size_mb': file_size
}

# Sauvegarder stats
with open(data_dir / 'data_clean_summary.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Lignes: {stats['total_rows']:,}")
print(f"Colonnes: {stats['total_columns']}")
print(f"Utilisateurs uniques: {stats['unique_users']:,}")
print(f"Sessions uniques: {stats['unique_sessions']:,}")
print(f"Produits uniques: {stats['unique_products']:,}")

print(f"\nÉvénements par type:")
for k, v in stats['events_by_type'].items():
    print(f"  - {k}: {v:,}")

print(f"\nUtilisateurs par segment:")
for k, v in stats['users_by_segment'].items():
    print(f"  - {k}: {v:,}")

print(f"\nPériode: {stats['period']['start_date']} → {stats['period']['end_date']}")

# Temps total
elapsed = (datetime.now() - start_time).total_seconds()
print(f"\n{'='*80}")
print(f"  TERMINE EN {elapsed:.1f} SECONDES")
print(f"{'='*80}\n")
