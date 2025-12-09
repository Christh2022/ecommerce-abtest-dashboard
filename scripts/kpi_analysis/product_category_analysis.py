#!/usr/bin/env python3
"""
Script d'analyse des catégories et produits - Issue #12
Génère des analyses détaillées de la performance des catégories et produits.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #12 - Analyse des catégories / produits
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

def print_separator(title=""):
    """Affiche un séparateur formaté"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def main():
    """Analyse détaillée des catégories et produits: performance, distribution, insights"""
    print_separator("ANALYSE CATEGORIES & PRODUITS - ISSUE #12")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    print_separator("CHARGEMENT DES DONNEES")
    
    # Charger products_summary.csv
    print("Chargement de products_summary.csv...")
    products = pd.read_csv(data_dir / 'products_summary.csv')
    print(f"[OK] {len(products):,} produits chargés")
    
    # Charger daily_metrics pour contexte
    print("\nChargement de daily_metrics.csv...")
    daily_metrics = pd.read_csv(data_dir / 'daily_metrics.csv')
    print(f"[OK] {len(daily_metrics)} jours chargés")
    
    print_separator("ANALYSE DES CATEGORIES")
    
    # 1. PERFORMANCE PAR CATEGORIE
    print("1. Calcul des métriques par catégorie...")
    
    category_stats = products.groupby('category').agg({
        'product_id': 'count',
        'unique_users': 'sum',
        'views': 'sum',
        'add_to_carts': 'sum',
        'purchases': 'sum',
        'total_revenue': 'sum',
        'view_to_cart_rate': 'mean',
        'view_to_purchase_rate': 'mean',
        'cart_to_purchase_rate': 'mean',
        'avg_price': 'mean',
        'revenue_per_user': 'mean',
        'revenue_per_view': 'mean'
    }).round(2)
    
    category_stats.columns = ['num_products', 'total_users', 'total_views', 'total_carts', 
                               'total_purchases', 'total_revenue', 'avg_view_to_cart', 
                               'avg_view_to_purchase', 'avg_cart_to_purchase', 'avg_price',
                               'avg_revenue_per_user', 'avg_revenue_per_view']
    
    # Calcul métriques supplémentaires
    category_stats['revenue_share'] = (category_stats['total_revenue'] / 
                                        category_stats['total_revenue'].sum() * 100).round(2)
    category_stats['product_share'] = (category_stats['num_products'] / 
                                        category_stats['num_products'].sum() * 100).round(2)
    category_stats['conversion_rate'] = (category_stats['total_purchases'] / 
                                          category_stats['total_users'] * 100).round(2)
    category_stats['avg_revenue_per_product'] = (category_stats['total_revenue'] / 
                                                   category_stats['num_products']).round(2)
    
    category_summary = {}
    for cat in category_stats.index:
        category_summary[cat] = {
            'num_products': int(category_stats.loc[cat, 'num_products']),
            'product_share': float(category_stats.loc[cat, 'product_share']),
            'total_users': int(category_stats.loc[cat, 'total_users']),
            'total_views': int(category_stats.loc[cat, 'total_views']),
            'total_purchases': int(category_stats.loc[cat, 'total_purchases']),
            'total_revenue': float(category_stats.loc[cat, 'total_revenue']),
            'revenue_share': float(category_stats.loc[cat, 'revenue_share']),
            'conversion_rate': float(category_stats.loc[cat, 'conversion_rate']),
            'avg_price': float(category_stats.loc[cat, 'avg_price']),
            'avg_revenue_per_product': float(category_stats.loc[cat, 'avg_revenue_per_product']),
            'avg_revenue_per_user': float(category_stats.loc[cat, 'avg_revenue_per_user'])
        }
    
    print("\n   Performance par catégorie:")
    for cat, data in category_summary.items():
        print(f"   • {cat:20s}: {data['num_products']:6,} produits ({data['product_share']:5.1f}%) | "
              f"€{data['total_revenue']:,.0f} ({data['revenue_share']:5.1f}%) | "
              f"Conv: {data['conversion_rate']:.2f}%")
    
    # 2. ANALYSE DES PRODUITS TOP PERFORMERS
    print("\n2. Analyse des Top Performers...")
    
    top_performers = products[products['category'] == 'Top Performer'].copy()
    high_revenue = products[products['category'] == 'High Revenue'].copy()
    
    top_stats = {
        'count': len(top_performers),
        'avg_users': float(top_performers['unique_users'].mean()),
        'avg_views': float(top_performers['views'].mean()),
        'avg_purchases': float(top_performers['purchases'].mean()),
        'avg_revenue': float(top_performers['total_revenue'].mean()),
        'avg_conversion': float(top_performers['view_to_purchase_rate'].mean()),
        'total_revenue': float(top_performers['total_revenue'].sum()),
        'revenue_share': float(top_performers['total_revenue'].sum() / products['total_revenue'].sum() * 100)
    }
    
    print(f"   Top Performer: {top_stats['count']:,} produits ({top_stats['count']/len(products)*100:.1f}%)")
    print(f"   Revenue moyen/produit: €{top_stats['avg_revenue']:,.2f}")
    print(f"   Revenue total: €{top_stats['total_revenue']:,.0f} ({top_stats['revenue_share']:.1f}%)")
    print(f"   Conversion moyenne: {top_stats['avg_conversion']:.2f}%")
    
    # 3. DISTRIBUTION DE LA PERFORMANCE PRODUITS
    print("\n3. Analyse de la distribution des produits...")
    
    # Créer des segments de performance basés sur le revenue
    # Utiliser des bins manuels au lieu de quantiles à cause des nombreux zéros
    products['revenue_percentile'] = pd.cut(products['total_revenue'], 
                                             bins=[-0.01, 0.01, 10, 50, 200, 1000, 5000, float('inf')], 
                                             labels=['Aucun', 'Très faible', 'Faible', 'Moyen', 
                                                     'Bon', 'Très bon', 'Excellent'])
    
    revenue_distribution = products.groupby('revenue_percentile').agg({
        'product_id': 'count',
        'total_revenue': ['sum', 'mean', 'min', 'max'],
        'purchases': 'sum',
        'views': 'sum',
        'unique_users': 'sum'
    }).round(2)
    
    # Produits avec/sans ventes
    products_with_sales = (products['purchases'] > 0).sum()
    products_without_sales = (products['purchases'] == 0).sum()
    
    distribution_summary = {
        'total_products': len(products),
        'products_with_sales': int(products_with_sales),
        'products_with_sales_pct': float(products_with_sales / len(products) * 100),
        'products_without_sales': int(products_without_sales),
        'products_without_sales_pct': float(products_without_sales / len(products) * 100),
        'avg_revenue_per_product': float(products['total_revenue'].mean()),
        'median_revenue_per_product': float(products['total_revenue'].median()),
        'top_1pct_products': int(len(products) * 0.01),
        'top_1pct_revenue': float(products.nlargest(int(len(products) * 0.01), 'total_revenue')['total_revenue'].sum()),
        'top_1pct_revenue_share': float(products.nlargest(int(len(products) * 0.01), 'total_revenue')['total_revenue'].sum() / 
                                         products['total_revenue'].sum() * 100)
    }
    
    print(f"   Produits avec ventes: {distribution_summary['products_with_sales']:,} "
          f"({distribution_summary['products_with_sales_pct']:.1f}%)")
    print(f"   Produits sans ventes: {distribution_summary['products_without_sales']:,} "
          f"({distribution_summary['products_without_sales_pct']:.1f}%)")
    print(f"   Revenue moyen/produit: €{distribution_summary['avg_revenue_per_product']:,.2f}")
    print(f"   Revenue médian/produit: €{distribution_summary['median_revenue_per_product']:.2f}")
    print(f"   Top 1% des produits ({distribution_summary['top_1pct_products']:,}): "
          f"€{distribution_summary['top_1pct_revenue']:,.0f} "
          f"({distribution_summary['top_1pct_revenue_share']:.1f}% du revenue)")
    
    # 4. ANALYSE DE PRIX
    print("\n4. Analyse des prix...")
    
    price_analysis = {
        'avg_price': float(products['avg_price'].mean()),
        'median_price': float(products['avg_price'].median()),
        'min_price': float(products['min_price'].min()),
        'max_price': float(products['max_price'].max()),
        'std_price': float(products['avg_price'].std())
    }
    
    # Segmentation par tranche de prix
    products['price_range'] = pd.cut(products['avg_price'], 
                                      bins=[0, 50, 100, 150, 200, 300, 500],
                                      labels=['0-50€', '50-100€', '100-150€', '150-200€', 
                                              '200-300€', '300-500€'])
    
    price_segments = products.groupby('price_range', observed=True).agg({
        'product_id': 'count',
        'total_revenue': 'sum',
        'purchases': 'sum',
        'view_to_purchase_rate': 'mean'
    }).round(2)
    
    print(f"   Prix moyen: €{price_analysis['avg_price']:.2f}")
    print(f"   Prix médian: €{price_analysis['median_price']:.2f}")
    print(f"   Range: €{price_analysis['min_price']:.2f} - €{price_analysis['max_price']:.2f}")
    print("\n   Distribution par tranche de prix:")
    for idx in price_segments.index:
        print(f"     {idx}: {int(price_segments.loc[idx, 'product_id']):,} produits, "
              f"€{price_segments.loc[idx, 'total_revenue']:,.0f} revenue")
    
    # 5. TOP 20 PRODUITS
    print("\n5. Identification des top produits...")
    
    top_20_revenue = products.nlargest(20, 'total_revenue')
    top_20_conversion = products.nlargest(20, 'view_to_purchase_rate')
    top_20_users = products.nlargest(20, 'unique_users')
    
    print(f"   Top produit (revenue): Product #{top_20_revenue.iloc[0]['product_id']} - "
          f"€{top_20_revenue.iloc[0]['total_revenue']:,.2f}")
    print(f"   Top produit (conversion): Product #{top_20_conversion.iloc[0]['product_id']} - "
          f"{top_20_conversion.iloc[0]['view_to_purchase_rate']:.2f}%")
    print(f"   Top produit (popularité): Product #{top_20_users.iloc[0]['product_id']} - "
          f"{int(top_20_users.iloc[0]['unique_users']):,} users")
    
    # 6. ANALYSE DE LA LONGUE TRAINE
    print("\n6. Analyse de la longue traîne...")
    
    products_sorted = products.sort_values('total_revenue', ascending=False).reset_index(drop=True)
    products_sorted['cumulative_revenue'] = products_sorted['total_revenue'].cumsum()
    products_sorted['cumulative_revenue_pct'] = (products_sorted['cumulative_revenue'] / 
                                                   products_sorted['total_revenue'].sum() * 100)
    
    # Trouver combien de produits font 80% du revenue (règle de Pareto)
    products_for_80pct = (products_sorted['cumulative_revenue_pct'] <= 80).sum()
    products_for_50pct = (products_sorted['cumulative_revenue_pct'] <= 50).sum()
    
    long_tail = {
        'products_for_50pct_revenue': int(products_for_50pct),
        'products_for_50pct_pct': float(products_for_50pct / len(products) * 100),
        'products_for_80pct_revenue': int(products_for_80pct),
        'products_for_80pct_pct': float(products_for_80pct / len(products) * 100),
        'remaining_products': int(len(products) - products_for_80pct),
        'remaining_products_revenue_share': float(100 - 80)
    }
    
    print(f"   {long_tail['products_for_50pct_revenue']:,} produits "
          f"({long_tail['products_for_50pct_pct']:.2f}%) génèrent 50% du revenue")
    print(f"   {long_tail['products_for_80pct_revenue']:,} produits "
          f"({long_tail['products_for_80pct_pct']:.2f}%) génèrent 80% du revenue (Pareto)")
    print(f"   {long_tail['remaining_products']:,} produits restants "
          f"({100-long_tail['products_for_80pct_pct']:.2f}%) génèrent 20% du revenue")
    
    print_separator("GENERATION DES FICHIERS")
    
    # Préparer le summary global
    analysis_summary = {
        'categories': category_summary,
        'top_performers': top_stats,
        'distribution': distribution_summary,
        'price_analysis': price_analysis,
        'long_tail': long_tail,
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'script': 'product_category_analysis.py',
            'issue': '#12',
            'total_products_analyzed': len(products)
        }
    }
    
    # Sauvegarder le résumé JSON
    output_json = output_dir / 'product_category_summary.json'
    print(f"Sauvegarde de {output_json.name}...")
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(analysis_summary, f, indent=2, ensure_ascii=False)
    print(f"[OK] {output_json}")
    
    # Créer category_performance.csv
    print("\nGénération de category_performance.csv...")
    category_perf = category_stats.reset_index()
    category_perf = category_perf.round(2)
    
    output_cat = output_dir / 'category_performance.csv'
    category_perf.to_csv(output_cat, index=False)
    print(f"[OK] {output_cat}")
    print(f"     {len(category_perf)} catégories, {len(category_perf.columns)} colonnes")
    
    # Créer product_segments.csv
    print("\nGénération de product_segments.csv...")
    
    # Segmenter les produits
    products['performance_segment'] = pd.cut(
        products['total_revenue'],
        bins=[0, 100, 500, 1000, 5000, float('inf')],
        labels=['Très faible', 'Faible', 'Moyen', 'Bon', 'Excellent']
    )
    
    segment_stats = products.groupby('performance_segment', observed=True).agg({
        'product_id': 'count',
        'total_revenue': ['sum', 'mean'],
        'purchases': ['sum', 'mean'],
        'views': 'sum',
        'unique_users': 'sum',
        'view_to_purchase_rate': 'mean',
        'avg_price': 'mean'
    }).round(2)
    
    segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns.values]
    segment_stats = segment_stats.reset_index()
    segment_stats.columns = ['segment', 'num_products', 'total_revenue', 'avg_revenue',
                              'total_purchases', 'avg_purchases', 'total_views', 
                              'total_users', 'avg_conversion', 'avg_price']
    
    output_segments = output_dir / 'product_segments.csv'
    segment_stats.to_csv(output_segments, index=False)
    print(f"[OK] {output_segments}")
    print(f"     {len(segment_stats)} segments, {len(segment_stats.columns)} colonnes")
    
    # Créer top_products_comprehensive.csv
    print("\nGénération de top_products_comprehensive.csv...")
    
    top_products = products.nlargest(200, 'total_revenue')[[
        'rank', 'product_id', 'category', 'unique_users', 'views', 'add_to_carts', 'purchases',
        'view_to_cart_rate', 'view_to_purchase_rate', 'cart_to_purchase_rate',
        'total_revenue', 'avg_price', 'revenue_per_user', 'revenue_per_view',
        'events_per_user'
    ]].copy()
    
    output_top = output_dir / 'top_products_comprehensive.csv'
    top_products.to_csv(output_top, index=False)
    print(f"[OK] {output_top}")
    print(f"     {len(top_products)} produits, {len(top_products.columns)} colonnes")
    
    # Créer price_segment_analysis.csv
    print("\nGénération de price_segment_analysis.csv...")
    
    price_seg_df = price_segments.reset_index()
    price_seg_df.columns = ['price_range', 'num_products', 'total_revenue', 
                             'total_purchases', 'avg_conversion']
    price_seg_df['revenue_per_product'] = (price_seg_df['total_revenue'] / 
                                            price_seg_df['num_products']).round(2)
    price_seg_df['revenue_share'] = (price_seg_df['total_revenue'] / 
                                      price_seg_df['total_revenue'].sum() * 100).round(2)
    
    output_price = output_dir / 'price_segment_analysis.csv'
    price_seg_df.to_csv(output_price, index=False)
    print(f"[OK] {output_price}")
    print(f"     {len(price_seg_df)} tranches de prix, {len(price_seg_df.columns)} colonnes")
    
    # Créer pareto_analysis.csv
    print("\nGénération de pareto_analysis.csv...")
    
    pareto_milestones = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100]
    pareto_data = []
    
    for milestone in pareto_milestones:
        if milestone == 100:
            num_products = len(products_sorted)
        else:
            num_products = (products_sorted['cumulative_revenue_pct'] <= milestone).sum()
        
        revenue = products_sorted.iloc[:num_products]['total_revenue'].sum()
        purchases = products_sorted.iloc[:num_products]['purchases'].sum()
        
        pareto_data.append({
            'revenue_milestone_pct': milestone,
            'num_products': num_products,
            'products_pct': round(num_products / len(products) * 100, 2),
            'cumulative_revenue': round(revenue, 2),
            'cumulative_purchases': int(purchases)
        })
    
    pareto_df = pd.DataFrame(pareto_data)
    
    output_pareto = output_dir / 'pareto_analysis.csv'
    pareto_df.to_csv(output_pareto, index=False)
    print(f"[OK] {output_pareto}")
    print(f"     {len(pareto_df)} milestones, {len(pareto_df.columns)} colonnes")
    
    # Créer underperforming_products.csv
    print("\nGénération de underperforming_products.csv...")
    
    # Produits avec des vues mais peu/pas de conversions
    underperformers = products[
        (products['views'] >= 10) & 
        (products['view_to_purchase_rate'] < 0.5)
    ].nlargest(500, 'views')[[
        'rank', 'product_id', 'category', 'unique_users', 'views', 'add_to_carts', 'purchases',
        'view_to_cart_rate', 'view_to_purchase_rate', 'total_revenue', 'avg_price'
    ]].copy()
    
    output_under = output_dir / 'underperforming_products.csv'
    underperformers.to_csv(output_under, index=False)
    print(f"[OK] {output_under}")
    print(f"     {len(underperformers)} produits, {len(underperformers.columns)} colonnes")
    
    print_separator("RESUME FINAL")
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ Analyse des catégories et produits terminée avec succès!")
    print(f"\n📊 Catégories:")
    for cat, data in category_summary.items():
        print(f"   • {cat}: {data['num_products']:,} produits ({data['revenue_share']:.1f}% revenue)")
    print(f"\n🏆 Top Performers:")
    print(f"   • {top_stats['count']:,} produits ({top_stats['count']/len(products)*100:.1f}%)")
    print(f"   • €{top_stats['total_revenue']:,.0f} revenue ({top_stats['revenue_share']:.1f}%)")
    print(f"\n📈 Distribution:")
    print(f"   • Top 1% ({distribution_summary['top_1pct_products']:,} produits): "
          f"{distribution_summary['top_1pct_revenue_share']:.1f}% revenue")
    print(f"   • {distribution_summary['products_without_sales_pct']:.1f}% produits sans ventes")
    print(f"\n💰 Prix:")
    print(f"   • Prix moyen: €{price_analysis['avg_price']:.2f}")
    print(f"   • Range: €{price_analysis['min_price']:.2f} - €{price_analysis['max_price']:.2f}")
    print(f"\n📊 Pareto:")
    print(f"   • {long_tail['products_for_80pct_pct']:.1f}% produits → 80% revenue")
    print(f"\n📁 Fichiers générés:")
    print(f"   • product_category_summary.json")
    print(f"   • category_performance.csv ({len(category_perf)} lignes)")
    print(f"   • product_segments.csv ({len(segment_stats)} lignes)")
    print(f"   • top_products_comprehensive.csv ({len(top_products)} lignes)")
    print(f"   • price_segment_analysis.csv ({len(price_seg_df)} lignes)")
    print(f"   • pareto_analysis.csv ({len(pareto_df)} lignes)")
    print(f"   • underperforming_products.csv ({len(underperformers)} lignes)")
    print(f"\n⏱️  Temps d'exécution: {execution_time:.2f}s")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
