#!/usr/bin/env python3
"""
Script de génération du fichier daily_metrics.csv
Métriques quotidiennes enrichies pour le dashboard et A/B testing.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #7
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

def print_separator(title=""):
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def main():
    """Génération de daily_metrics.csv avec métriques enrichies"""
    print_separator("GENERATION DE DAILY_METRICS.CSV - Issue #7")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    
    print_separator("CHARGEMENT DES DONNEES")
    
    # Charger data_clean.csv par chunks
    print("Chargement de data_clean.csv par chunks...")
    chunk_size = 500000
    chunks = []
    
    for chunk in pd.read_csv(data_dir / 'data_clean.csv', chunksize=chunk_size):
        chunks.append(chunk)
        print(f"  Chunk chargé: {len(chunk):,} lignes")
    
    data_clean = pd.concat(chunks, ignore_index=True)
    print(f"\n[OK] {len(data_clean):,} lignes totales chargées")
    
    # Charger transactions pour les montants
    print("\nChargement de transactions.csv...")
    trans_df = pd.read_csv(data_dir / 'transactions.csv')
    print(f"[OK] {len(trans_df):,} transactions chargées")
    
    print_separator("CALCUL DES METRIQUES QUOTIDIENNES")
    
    print("Calcul des métriques par jour...")
    
    # Grouper par date
    daily_metrics = data_clean.groupby('date').agg({
        'user_id': 'nunique',
        'session_id': 'nunique',
        'product_id': 'nunique',
        'timestamp': 'count'
    }).reset_index()
    
    daily_metrics.columns = ['date', 'unique_users', 'unique_sessions', 'unique_products', 'total_events']
    
    # Métriques par type d'événement
    print("  - Événements par type...")
    event_counts = data_clean.groupby(['date', 'event_type']).size().unstack(fill_value=0)
    daily_metrics = daily_metrics.merge(event_counts, left_on='date', right_index=True, how='left')
    
    # Renommer les colonnes d'événements
    if 'view' in daily_metrics.columns:
        daily_metrics.rename(columns={'view': 'views'}, inplace=True)
    if 'addtocart' in daily_metrics.columns:
        daily_metrics.rename(columns={'addtocart': 'add_to_carts'}, inplace=True)
    if 'transaction' in daily_metrics.columns:
        daily_metrics.rename(columns={'transaction': 'transactions'}, inplace=True)
    
    # Métriques par segment
    print("  - Utilisateurs par segment...")
    segment_counts = data_clean.groupby(['date', 'segment'])['user_id'].nunique().unstack(fill_value=0)
    segment_counts.columns = [f'users_{col.lower()}' for col in segment_counts.columns]
    daily_metrics = daily_metrics.merge(segment_counts, left_on='date', right_index=True, how='left')
    
    # Ajouter les revenus quotidiens
    print("  - Revenus et montants...")
    # transactions.csv a déjà une colonne 'date'
    revenue_metrics = trans_df.groupby('date')['amount'].agg([
        ('daily_revenue', 'sum'),
        ('avg_order_value', 'mean'),
        ('min_order', 'min'),
        ('max_order', 'max')
    ]).reset_index()
    
    daily_metrics = daily_metrics.merge(revenue_metrics, on='date', how='left')
    
    # Remplir les valeurs manquantes de revenus avec 0
    revenue_cols = ['daily_revenue', 'avg_order_value', 'min_order', 'max_order']
    for col in revenue_cols:
        if col in daily_metrics.columns:
            daily_metrics[col] = daily_metrics[col].fillna(0)
    
    # Calculer les taux de conversion
    print("  - Taux de conversion...")
    if 'views' in daily_metrics.columns and 'add_to_carts' in daily_metrics.columns:
        daily_metrics['view_to_cart_rate'] = (daily_metrics['add_to_carts'] / daily_metrics['views'] * 100).round(2)
    
    if 'views' in daily_metrics.columns and 'transactions' in daily_metrics.columns:
        daily_metrics['view_to_purchase_rate'] = (daily_metrics['transactions'] / daily_metrics['views'] * 100).round(2)
    
    if 'add_to_carts' in daily_metrics.columns and 'transactions' in daily_metrics.columns:
        daily_metrics['cart_to_purchase_rate'] = (daily_metrics['transactions'] / daily_metrics['add_to_carts'] * 100).round(2)
    
    # Calculer les métriques par utilisateur
    print("  - Métriques par utilisateur...")
    daily_metrics['events_per_user'] = (daily_metrics['total_events'] / daily_metrics['unique_users']).round(2)
    daily_metrics['sessions_per_user'] = (daily_metrics['unique_sessions'] / daily_metrics['unique_users']).round(2)
    
    if 'daily_revenue' in daily_metrics.columns and 'transactions' in daily_metrics.columns:
        daily_metrics['revenue_per_user'] = (daily_metrics['daily_revenue'] / daily_metrics['unique_users']).round(2)
    
    # Ajouter des colonnes temporelles
    print("  - Colonnes temporelles...")
    daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
    daily_metrics['day_of_week'] = daily_metrics['date'].dt.day_name()
    daily_metrics['week_number'] = daily_metrics['date'].dt.isocalendar().week
    daily_metrics['month'] = daily_metrics['date'].dt.month
    daily_metrics['is_weekend'] = daily_metrics['day_of_week'].isin(['Saturday', 'Sunday'])
    
    # Convertir date en string pour le CSV
    daily_metrics['date'] = daily_metrics['date'].dt.strftime('%Y-%m-%d')
    
    # Calculer les moyennes mobiles (7 jours)
    print("  - Moyennes mobiles (7 jours)...")
    daily_metrics = daily_metrics.sort_values('date')
    daily_metrics['ma7_revenue'] = daily_metrics['daily_revenue'].rolling(window=7, min_periods=1).mean().round(2)
    daily_metrics['ma7_users'] = daily_metrics['unique_users'].rolling(window=7, min_periods=1).mean().round(2)
    daily_metrics['ma7_conversion'] = daily_metrics['view_to_purchase_rate'].rolling(window=7, min_periods=1).mean().round(2)
    
    # Trier les colonnes pour une meilleure lisibilité
    col_order = [
        'date', 'day_of_week', 'week_number', 'month', 'is_weekend',
        'unique_users', 'unique_sessions', 'unique_products', 'total_events',
        'views', 'add_to_carts', 'transactions',
        'view_to_cart_rate', 'view_to_purchase_rate', 'cart_to_purchase_rate',
        'daily_revenue', 'avg_order_value', 'min_order', 'max_order',
        'events_per_user', 'sessions_per_user', 'revenue_per_user',
        'ma7_revenue', 'ma7_users', 'ma7_conversion'
    ]
    
    # Ajouter les colonnes de segments
    segment_cols = [col for col in daily_metrics.columns if col.startswith('users_')]
    col_order.extend(segment_cols)
    
    # Sélectionner seulement les colonnes qui existent
    existing_cols = [col for col in col_order if col in daily_metrics.columns]
    daily_metrics = daily_metrics[existing_cols]
    
    print(f"\n[RESULTAT] {len(daily_metrics)} jours x {len(daily_metrics.columns)} colonnes")
    
    # Sauvegarder
    print_separator("SAUVEGARDE")
    output_file = data_dir / 'daily_metrics.csv'
    daily_metrics.to_csv(output_file, index=False)
    file_size = output_file.stat().st_size / 1024
    
    print(f"[OK] {output_file}")
    print(f"     Taille: {file_size:.2f} KB")
    
    # Statistiques
    print_separator("STATISTIQUES")
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'source': 'data_clean.csv + transactions.csv',
        'total_days': len(daily_metrics),
        'total_columns': len(daily_metrics.columns),
        'columns': list(daily_metrics.columns),
        'date_range': {
            'start': str(daily_metrics['date'].min()),
            'end': str(daily_metrics['date'].max())
        },
        'summary': {
            'total_users': int(daily_metrics['unique_users'].sum()),
            'avg_daily_users': int(daily_metrics['unique_users'].mean()),
            'total_transactions': int(daily_metrics['transactions'].sum()) if 'transactions' in daily_metrics.columns else 0,
            'total_revenue': float(daily_metrics['daily_revenue'].sum()) if 'daily_revenue' in daily_metrics.columns else 0,
            'avg_conversion_rate': float(daily_metrics['view_to_purchase_rate'].mean()) if 'view_to_purchase_rate' in daily_metrics.columns else 0,
            'best_day': {
                'revenue': str(daily_metrics.loc[daily_metrics['daily_revenue'].idxmax(), 'date']) if 'daily_revenue' in daily_metrics.columns else None,
                'users': str(daily_metrics.loc[daily_metrics['unique_users'].idxmax(), 'date']),
                'conversion': str(daily_metrics.loc[daily_metrics['view_to_purchase_rate'].idxmax(), 'date']) if 'view_to_purchase_rate' in daily_metrics.columns else None
            }
        },
        'file_size_kb': file_size
    }
    
    # Sauvegarder stats
    with open(data_dir / 'daily_metrics_summary.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Période: {stats['date_range']['start']} → {stats['date_range']['end']}")
    print(f"Jours: {stats['total_days']}")
    print(f"Colonnes: {stats['total_columns']}")
    print(f"\nMoyennes quotidiennes:")
    print(f"  - Utilisateurs: {stats['summary']['avg_daily_users']:,}")
    print(f"  - Transactions: {stats['summary']['total_transactions'] / stats['total_days']:.0f}")
    print(f"  - Revenu: {stats['summary']['total_revenue'] / stats['total_days']:.2f} €")
    print(f"  - Taux de conversion: {stats['summary']['avg_conversion_rate']:.2f}%")
    
    print(f"\nMeilleurs jours:")
    print(f"  - Revenu max: {stats['summary']['best_day']['revenue']}")
    print(f"  - Utilisateurs max: {stats['summary']['best_day']['users']}")
    print(f"  - Conversion max: {stats['summary']['best_day']['conversion']}")
    
    # Temps total
    elapsed = (datetime.now() - start_time).total_seconds()
    print_separator(f"TERMINE EN {elapsed:.1f} SECONDES")

if __name__ == "__main__":
    main()
