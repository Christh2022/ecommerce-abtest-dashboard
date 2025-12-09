#!/usr/bin/env python3
"""
Script de génération du fichier products_summary.csv
Résumé des performances produits pour le dashboard.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #8
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
    """Génération de products_summary.csv"""
    print_separator("GENERATION DE PRODUCTS_SUMMARY.CSV - Issue #8")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    
    print_separator("CHARGEMENT DES DONNEES")
    
    # Charger data_clean.csv par chunks pour extraire les métriques produits
    print("Chargement de data_clean.csv par chunks...")
    chunk_size = 500000
    all_products = []
    
    for i, chunk in enumerate(pd.read_csv(data_dir / 'data_clean.csv', chunksize=chunk_size), 1):
        print(f"  Chunk {i}: {len(chunk):,} lignes")
        
        # Métriques par produit dans ce chunk
        product_metrics = chunk.groupby('product_id').agg({
            'user_id': 'nunique',
            'session_id': 'nunique',
            'timestamp': 'count',
            'event_type': lambda x: (x == 'view').sum(),
        }).reset_index()
        
        product_metrics.columns = ['product_id', 'unique_users', 'unique_sessions', 'total_events', 'views']
        
        # Compter addtocart et transactions
        addtocart_counts = chunk[chunk['event_type'] == 'addtocart'].groupby('product_id').size()
        transaction_counts = chunk[chunk['event_type'] == 'transaction'].groupby('product_id').size()
        
        product_metrics = product_metrics.merge(
            addtocart_counts.rename('add_to_carts'),
            left_on='product_id',
            right_index=True,
            how='left'
        )
        
        product_metrics = product_metrics.merge(
            transaction_counts.rename('purchases'),
            left_on='product_id',
            right_index=True,
            how='left'
        )
        
        product_metrics['add_to_carts'] = product_metrics['add_to_carts'].fillna(0).astype(int)
        product_metrics['purchases'] = product_metrics['purchases'].fillna(0).astype(int)
        
        all_products.append(product_metrics)
    
    print("\nAgrégation des métriques par produit...")
    products_summary = pd.concat(all_products, ignore_index=True)
    
    # Agréger tous les chunks
    products_summary = products_summary.groupby('product_id').agg({
        'unique_users': 'sum',
        'unique_sessions': 'sum',
        'total_events': 'sum',
        'views': 'sum',
        'add_to_carts': 'sum',
        'purchases': 'sum'
    }).reset_index()
    
    print(f"[OK] {len(products_summary):,} produits uniques")
    
    # Charger transactions pour les revenus
    print("\nChargement de transactions.csv pour les revenus...")
    trans_df = pd.read_csv(data_dir / 'transactions.csv')
    print(f"[OK] {len(trans_df):,} transactions")
    
    # Calculer revenus par produit
    revenue_metrics = trans_df.groupby('product_id')['amount'].agg([
        ('total_revenue', 'sum'),
        ('avg_price', 'mean'),
        ('min_price', 'min'),
        ('max_price', 'max'),
        ('num_purchases', 'count')
    ]).reset_index()
    
    # Fusionner avec products_summary
    products_summary = products_summary.merge(revenue_metrics, on='product_id', how='left')
    
    # Remplir les valeurs manquantes
    revenue_cols = ['total_revenue', 'avg_price', 'min_price', 'max_price', 'num_purchases']
    for col in revenue_cols:
        products_summary[col] = products_summary[col].fillna(0)
    
    print_separator("CALCUL DES METRIQUES")
    
    # Taux de conversion
    print("Calcul des taux de conversion...")
    products_summary['view_to_cart_rate'] = (
        products_summary['add_to_carts'] / products_summary['views'] * 100
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    products_summary['view_to_purchase_rate'] = (
        products_summary['purchases'] / products_summary['views'] * 100
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    products_summary['cart_to_purchase_rate'] = (
        products_summary['purchases'] / products_summary['add_to_carts'] * 100
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    # Métriques d'engagement
    print("Calcul des métriques d'engagement...")
    products_summary['events_per_user'] = (
        products_summary['total_events'] / products_summary['unique_users']
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    products_summary['sessions_per_user'] = (
        products_summary['unique_sessions'] / products_summary['unique_users']
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    products_summary['revenue_per_user'] = (
        products_summary['total_revenue'] / products_summary['unique_users']
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    products_summary['revenue_per_view'] = (
        products_summary['total_revenue'] / products_summary['views']
    ).replace([np.inf, -np.inf], 0).fillna(0).round(2)
    
    # Catégorisation des produits
    print("Catégorisation des produits par performance...")
    
    # Top performers (par revenu)
    revenue_threshold_high = products_summary['total_revenue'].quantile(0.75)
    revenue_threshold_low = products_summary['total_revenue'].quantile(0.25)
    
    def categorize_product(row):
        if row['total_revenue'] >= revenue_threshold_high and row['view_to_purchase_rate'] >= 1.0:
            return 'Top Performer'
        elif row['total_revenue'] >= revenue_threshold_high:
            return 'High Revenue'
        elif row['view_to_purchase_rate'] >= 2.0:
            return 'High Conversion'
        elif row['views'] >= 100:
            return 'Popular'
        elif row['total_revenue'] > 0:
            return 'Low Performer'
        else:
            return 'No Sales'
    
    products_summary['category'] = products_summary.apply(categorize_product, axis=1)
    
    # Trier par revenu décroissant
    products_summary = products_summary.sort_values('total_revenue', ascending=False).reset_index(drop=True)
    
    # Ajouter un rang
    products_summary['rank'] = products_summary.index + 1
    
    # Réorganiser les colonnes
    col_order = [
        'rank', 'product_id', 'category',
        'unique_users', 'unique_sessions', 'total_events',
        'views', 'add_to_carts', 'purchases',
        'view_to_cart_rate', 'view_to_purchase_rate', 'cart_to_purchase_rate',
        'total_revenue', 'avg_price', 'min_price', 'max_price', 'num_purchases',
        'events_per_user', 'sessions_per_user', 'revenue_per_user', 'revenue_per_view'
    ]
    
    products_summary = products_summary[col_order]
    
    print(f"\n[RESULTAT] {len(products_summary):,} produits x {len(products_summary.columns)} colonnes")
    
    # Sauvegarder
    print_separator("SAUVEGARDE")
    output_file = data_dir / 'products_summary.csv'
    products_summary.to_csv(output_file, index=False)
    file_size = output_file.stat().st_size / 1024
    
    print(f"[OK] {output_file}")
    print(f"     Taille: {file_size:.2f} KB")
    
    # Statistiques
    print_separator("STATISTIQUES")
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'source': 'data_clean.csv + transactions.csv',
        'total_products': len(products_summary),
        'total_columns': len(products_summary.columns),
        'columns': list(products_summary.columns),
        'categories': products_summary['category'].value_counts().to_dict(),
        'summary': {
            'products_with_sales': int((products_summary['purchases'] > 0).sum()),
            'products_no_sales': int((products_summary['purchases'] == 0).sum()),
            'total_revenue': float(products_summary['total_revenue'].sum()),
            'avg_revenue_per_product': float(products_summary['total_revenue'].mean()),
            'avg_conversion_rate': float(products_summary['view_to_purchase_rate'].mean()),
            'top_product': {
                'id': int(products_summary.iloc[0]['product_id']),
                'revenue': float(products_summary.iloc[0]['total_revenue']),
                'views': int(products_summary.iloc[0]['views']),
                'purchases': int(products_summary.iloc[0]['purchases'])
            }
        },
        'file_size_kb': file_size
    }
    
    # Sauvegarder stats
    with open(data_dir / 'products_summary_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Total produits: {stats['total_products']:,}")
    print(f"Colonnes: {stats['total_columns']}")
    
    print(f"\nCatégories:")
    for cat, count in stats['categories'].items():
        print(f"  - {cat}: {count:,} ({count/stats['total_products']*100:.1f}%)")
    
    print(f"\nProduits avec ventes: {stats['summary']['products_with_sales']:,}")
    print(f"Produits sans ventes: {stats['summary']['products_no_sales']:,}")
    print(f"Revenu total: {stats['summary']['total_revenue']:.2f} €")
    print(f"Revenu moyen/produit: {stats['summary']['avg_revenue_per_product']:.2f} €")
    print(f"Taux conversion moyen: {stats['summary']['avg_conversion_rate']:.2f}%")
    
    print(f"\nTop produit (#{stats['summary']['top_product']['id']}):")
    print(f"  - Revenu: {stats['summary']['top_product']['revenue']:.2f} €")
    print(f"  - Vues: {stats['summary']['top_product']['views']:,}")
    print(f"  - Achats: {stats['summary']['top_product']['purchases']:,}")
    
    # Temps total
    elapsed = (datetime.now() - start_time).total_seconds()
    print_separator(f"TERMINE EN {elapsed:.1f} SECONDES")

if __name__ == "__main__":
    main()
