#!/usr/bin/env python3
"""
Script d'analyse des conversions - Issue #11
Génère des analyses approfondies des conversions multi-dimensionnelles.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #11 - Analyse des conversions
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
    """Analyse détaillée des conversions: patterns, segments, temporalité"""
    print_separator("ANALYSE DES CONVERSIONS - ISSUE #11")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    print_separator("CHARGEMENT DES DONNEES")
    
    # Charger daily_metrics.csv
    print("Chargement de daily_metrics.csv...")
    daily_metrics = pd.read_csv(data_dir / 'daily_metrics.csv')
    print(f"[OK] {len(daily_metrics)} jours chargés")
    
    # Charger daily_funnel.csv
    print("\nChargement de daily_funnel.csv...")
    daily_funnel = pd.read_csv(data_dir / 'daily_funnel.csv')
    print(f"[OK] {len(daily_funnel)} jours chargés")
    
    # Charger segment_performance.csv
    print("\nChargement de segment_performance.csv...")
    segments = pd.read_csv(data_dir / 'segment_performance.csv')
    print(f"[OK] {len(segments)} segments chargés")
    
    # Charger products_summary.csv (sample pour performance)
    print("\nChargement de products_summary.csv (échantillon)...")
    products = pd.read_csv(data_dir / 'products_summary.csv', nrows=50000)
    print(f"[OK] {len(products)} produits chargés")
    
    print_separator("ANALYSE DES CONVERSIONS")
    
    daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
    daily_funnel['date'] = pd.to_datetime(daily_funnel['date'])
    
    # 1. METRIQUES GLOBALES DE CONVERSION
    print("1. Calcul des métriques globales de conversion...")
    
    conversion_summary = {
        'global_metrics': {
            'total_users': int(daily_metrics['unique_users'].sum()),
            'total_views': int(daily_metrics['views'].sum()),
            'total_add_to_carts': int(daily_metrics['add_to_carts'].sum()),
            'total_transactions': int(daily_metrics['transactions'].sum()),
            'total_revenue': float(daily_metrics['daily_revenue'].sum()),
            'avg_order_value': float(daily_metrics['daily_revenue'].sum() / daily_metrics['transactions'].sum())
        }
    }
    
    # Calcul des taux de conversion globaux
    conversion_summary['conversion_rates'] = {
        'view_to_cart': float(daily_metrics['add_to_carts'].sum() / daily_metrics['views'].sum() * 100),
        'view_to_transaction': float(daily_metrics['transactions'].sum() / daily_metrics['views'].sum() * 100),
        'cart_to_transaction': float(daily_metrics['transactions'].sum() / daily_metrics['add_to_carts'].sum() * 100),
        'user_to_transaction': float(daily_metrics['transactions'].sum() / daily_metrics['unique_users'].sum() * 100)
    }
    
    print(f"   Total utilisateurs: {conversion_summary['global_metrics']['total_users']:,}")
    print(f"   Total transactions: {conversion_summary['global_metrics']['total_transactions']:,}")
    print(f"   Taux view → cart: {conversion_summary['conversion_rates']['view_to_cart']:.2f}%")
    print(f"   Taux view → transaction: {conversion_summary['conversion_rates']['view_to_transaction']:.2f}%")
    print(f"   Taux cart → transaction: {conversion_summary['conversion_rates']['cart_to_transaction']:.2f}%")
    print(f"   Taux user → transaction: {conversion_summary['conversion_rates']['user_to_transaction']:.2f}%")
    
    # 2. ANALYSE DE CONVERSION PAR SEGMENT
    print("\n2. Analyse de conversion par segment...")
    
    segment_conversion = {}
    for _, row in segments.iterrows():
        segment_name = row['segment'].lower()
        segment_conversion[segment_name] = {
            'users': int(row['num_users']),
            'transactions': int(row['num_transactions']),
            'conversion_rate': float(row['num_transactions'] / row['num_users'] * 100),
            'revenue': float(row['total_revenue']),
            'revenue_per_user': float(row['revenue_per_user']),
            'avg_transaction': float(row['avg_transaction']),
            'transactions_per_user': float(row['num_transactions'] / row['num_users'])
        }
    
    conversion_summary['by_segment'] = segment_conversion
    
    print("\n   Conversion par segment:")
    for seg, data in sorted(segment_conversion.items(), key=lambda x: x[1]['conversion_rate'], reverse=True):
        print(f"   • {seg.capitalize():12s}: {data['conversion_rate']:5.2f}% | "
              f"{data['transactions_per_user']:.2f} trans/user | €{data['revenue_per_user']:,.2f}/user")
    
    # 3. ANALYSE TEMPORELLE DES CONVERSIONS
    print("\n3. Analyse temporelle des conversions...")
    
    # Conversion par jour de la semaine
    weekday_conversion = daily_metrics.groupby('day_of_week').agg({
        'unique_users': 'sum',
        'views': 'sum',
        'add_to_carts': 'sum',
        'transactions': 'sum',
        'daily_revenue': 'sum'
    })
    
    weekday_conversion['conversion_rate'] = (weekday_conversion['transactions'] / 
                                              weekday_conversion['unique_users'] * 100)
    weekday_conversion['view_to_cart'] = (weekday_conversion['add_to_carts'] / 
                                           weekday_conversion['views'] * 100)
    weekday_conversion['cart_to_purchase'] = (weekday_conversion['transactions'] / 
                                               weekday_conversion['add_to_carts'] * 100)
    
    # Week-end vs semaine
    weekday_avg = daily_metrics[~daily_metrics['is_weekend']]['view_to_purchase_rate'].mean()
    weekend_avg = daily_metrics[daily_metrics['is_weekend']]['view_to_purchase_rate'].mean()
    
    conversion_summary['temporal'] = {
        'weekday_avg_conversion': float(weekday_avg),
        'weekend_avg_conversion': float(weekend_avg),
        'weekend_variation': float((weekend_avg / weekday_avg - 1) * 100),
        'best_day': weekday_conversion['conversion_rate'].idxmax(),
        'best_day_rate': float(weekday_conversion['conversion_rate'].max()),
        'worst_day': weekday_conversion['conversion_rate'].idxmin(),
        'worst_day_rate': float(weekday_conversion['conversion_rate'].min())
    }
    
    print(f"   Conversion semaine: {weekday_avg:.2f}%")
    print(f"   Conversion week-end: {weekend_avg:.2f}%")
    print(f"   Variation week-end: {conversion_summary['temporal']['weekend_variation']:+.1f}%")
    print(f"   Meilleur jour: {conversion_summary['temporal']['best_day']} ({conversion_summary['temporal']['best_day_rate']:.2f}%)")
    print(f"   Pire jour: {conversion_summary['temporal']['worst_day']} ({conversion_summary['temporal']['worst_day_rate']:.2f}%)")
    
    # 4. EVOLUTION DE LA CONVERSION
    print("\n4. Analyse de l'évolution de la conversion...")
    
    daily_metrics = daily_metrics.sort_values('date')
    
    # Moyennes mobiles 7 et 30 jours
    daily_metrics['ma7_conversion'] = daily_metrics['view_to_purchase_rate'].rolling(window=7, min_periods=1).mean()
    daily_metrics['ma30_conversion'] = daily_metrics['view_to_purchase_rate'].rolling(window=30, min_periods=1).mean()
    
    # Périodes
    n_days = len(daily_metrics)
    early_period = daily_metrics.iloc[:n_days//3]
    mid_period = daily_metrics.iloc[n_days//3:2*n_days//3]
    late_period = daily_metrics.iloc[2*n_days//3:]
    
    conversion_summary['evolution'] = {
        'early_period': {
            'dates': f"{early_period['date'].min().strftime('%Y-%m-%d')} → {early_period['date'].max().strftime('%Y-%m-%d')}",
            'avg_conversion': float(early_period['view_to_purchase_rate'].mean()),
            'avg_aov': float(early_period['avg_order_value'].mean())
        },
        'mid_period': {
            'dates': f"{mid_period['date'].min().strftime('%Y-%m-%d')} → {mid_period['date'].max().strftime('%Y-%m-%d')}",
            'avg_conversion': float(mid_period['view_to_purchase_rate'].mean()),
            'avg_aov': float(mid_period['avg_order_value'].mean())
        },
        'late_period': {
            'dates': f"{late_period['date'].min().strftime('%Y-%m-%d')} → {late_period['date'].max().strftime('%Y-%m-%d')}",
            'avg_conversion': float(late_period['view_to_purchase_rate'].mean()),
            'avg_aov': float(late_period['avg_order_value'].mean())
        }
    }
    
    # Calcul de la tendance
    conversion_change = ((late_period['view_to_purchase_rate'].mean() / 
                          early_period['view_to_purchase_rate'].mean() - 1) * 100)
    aov_change = ((late_period['avg_order_value'].mean() / 
                   early_period['avg_order_value'].mean() - 1) * 100)
    
    conversion_summary['evolution']['conversion_trend'] = float(conversion_change)
    conversion_summary['evolution']['aov_trend'] = float(aov_change)
    
    print(f"   Période initiale: {conversion_summary['evolution']['early_period']['avg_conversion']:.2f}%")
    print(f"   Période finale: {conversion_summary['evolution']['late_period']['avg_conversion']:.2f}%")
    print(f"   Tendance conversion: {conversion_change:+.1f}%")
    print(f"   Tendance AOV: {aov_change:+.1f}%")
    
    # 5. ANALYSE DE CONVERSION PAR VALEUR DE COMMANDE
    print("\n5. Analyse par tranche de valeur de commande...")
    
    # Calculer les statistiques par jour
    daily_metrics['revenue_per_transaction'] = daily_metrics['daily_revenue'] / daily_metrics['transactions']
    
    aov_stats = {
        'mean': float(daily_metrics['avg_order_value'].mean()),
        'median': float(daily_metrics['avg_order_value'].median()),
        'std': float(daily_metrics['avg_order_value'].std()),
        'min': float(daily_metrics['min_order'].min()),
        'max': float(daily_metrics['max_order'].max()),
        'p25': float(daily_metrics['avg_order_value'].quantile(0.25)),
        'p75': float(daily_metrics['avg_order_value'].quantile(0.75))
    }
    
    conversion_summary['aov_analysis'] = aov_stats
    
    print(f"   AOV moyen: €{aov_stats['mean']:.2f}")
    print(f"   AOV médian: €{aov_stats['median']:.2f}")
    print(f"   Commande min: €{aov_stats['min']:.2f}")
    print(f"   Commande max: €{aov_stats['max']:.2f}")
    print(f"   P25-P75: €{aov_stats['p25']:.2f} - €{aov_stats['p75']:.2f}")
    
    # 6. ANALYSE DES PRODUITS ET CONVERSION
    print("\n6. Analyse de conversion produits...")
    
    # Top produits par conversion
    top_converters = products.nlargest(10, 'view_to_purchase_rate')
    
    product_conversion = {
        'avg_product_conversion': float(products['view_to_purchase_rate'].mean()),
        'median_product_conversion': float(products['view_to_purchase_rate'].median()),
        'top_converter_rate': float(top_converters['view_to_purchase_rate'].iloc[0]),
        'products_with_purchases': int((products['purchases'] > 0).sum()),
        'products_without_purchases': int((products['purchases'] == 0).sum()),
        'conversion_rate_distribution': {
            'under_1pct': int((products['view_to_purchase_rate'] < 1).sum()),
            '1_to_5pct': int(((products['view_to_purchase_rate'] >= 1) & (products['view_to_purchase_rate'] < 5)).sum()),
            '5_to_10pct': int(((products['view_to_purchase_rate'] >= 5) & (products['view_to_purchase_rate'] < 10)).sum()),
            'over_10pct': int((products['view_to_purchase_rate'] >= 10).sum())
        }
    }
    
    conversion_summary['product_conversion'] = product_conversion
    
    print(f"   Conversion produit moyenne: {product_conversion['avg_product_conversion']:.2f}%")
    print(f"   Produits avec ventes: {product_conversion['products_with_purchases']:,}")
    print(f"   Produits sans ventes: {product_conversion['products_without_purchases']:,}")
    print(f"   Distribution conversion:")
    print(f"     < 1%: {product_conversion['conversion_rate_distribution']['under_1pct']:,} produits")
    print(f"     1-5%: {product_conversion['conversion_rate_distribution']['1_to_5pct']:,} produits")
    print(f"     5-10%: {product_conversion['conversion_rate_distribution']['5_to_10pct']:,} produits")
    print(f"     > 10%: {product_conversion['conversion_rate_distribution']['over_10pct']:,} produits")
    
    print_separator("GENERATION DES FICHIERS")
    
    # Sauvegarder le résumé JSON
    output_json = output_dir / 'conversion_analysis_summary.json'
    print(f"Sauvegarde de {output_json.name}...")
    conversion_summary['metadata'] = {
        'generated_at': datetime.now().isoformat(),
        'script': 'conversion_analysis.py',
        'issue': '#11'
    }
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(conversion_summary, f, indent=2, ensure_ascii=False)
    print(f"[OK] {output_json}")
    
    # Créer conversion_daily.csv
    print("\nGénération de conversion_daily.csv...")
    conversion_daily = daily_metrics[[
        'date', 'day_of_week', 'is_weekend', 'week_number', 'month',
        'unique_users', 'views', 'add_to_carts', 'transactions',
        'view_to_cart_rate', 'view_to_purchase_rate', 'cart_to_purchase_rate',
        'daily_revenue', 'avg_order_value', 'revenue_per_user'
    ]].copy()
    
    # Ajouter métriques calculées
    conversion_daily['conversion_efficiency'] = (
        (conversion_daily['view_to_purchase_rate'] / conversion_daily['view_to_purchase_rate'].max()) * 100
    ).round(2)
    
    conversion_daily['ma7_conversion'] = daily_metrics['ma7_conversion'].round(2)
    conversion_daily['ma30_conversion'] = daily_metrics['ma30_conversion'].round(2)
    conversion_daily['ma7_aov'] = daily_metrics['avg_order_value'].rolling(window=7, min_periods=1).mean().round(2)
    
    output_csv = output_dir / 'conversion_daily.csv'
    conversion_daily.to_csv(output_csv, index=False)
    print(f"[OK] {output_csv}")
    print(f"     {len(conversion_daily)} jours, {len(conversion_daily.columns)} colonnes")
    
    # Créer conversion_by_segment.csv
    print("\nGénération de conversion_by_segment.csv...")
    segment_conv_df = pd.DataFrame([
        {
            'segment': seg.capitalize(),
            'users': data['users'],
            'transactions': data['transactions'],
            'conversion_rate': round(data['conversion_rate'], 2),
            'transactions_per_user': round(data['transactions_per_user'], 2),
            'revenue': round(data['revenue'], 2),
            'revenue_per_user': round(data['revenue_per_user'], 2),
            'avg_transaction': round(data['avg_transaction'], 2),
            'revenue_per_transaction': round(data['revenue'] / data['transactions'], 2) if data['transactions'] > 0 else 0
        }
        for seg, data in segment_conversion.items()
    ])
    
    segment_conv_df = segment_conv_df.sort_values('conversion_rate', ascending=False)
    
    output_segment = output_dir / 'conversion_by_segment.csv'
    segment_conv_df.to_csv(output_segment, index=False)
    print(f"[OK] {output_segment}")
    print(f"     {len(segment_conv_df)} segments, {len(segment_conv_df.columns)} colonnes")
    
    # Créer conversion_by_weekday.csv
    print("\nGénération de conversion_by_weekday.csv...")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    weekday_conv_df = weekday_conversion.reset_index()
    weekday_conv_df['day_order'] = weekday_conv_df['day_of_week'].map(
        {day: i for i, day in enumerate(weekday_order)}
    )
    weekday_conv_df = weekday_conv_df.sort_values('day_order').drop('day_order', axis=1)
    weekday_conv_df = weekday_conv_df.round(2)
    
    output_weekday = output_dir / 'conversion_by_weekday.csv'
    weekday_conv_df.to_csv(output_weekday, index=False)
    print(f"[OK] {output_weekday}")
    print(f"     {len(weekday_conv_df)} jours, {len(weekday_conv_df.columns)} colonnes")
    
    # Créer conversion_evolution.csv
    print("\nGénération de conversion_evolution.csv...")
    evolution_df = pd.DataFrame([
        {
            'period': 'Early',
            'dates': conversion_summary['evolution']['early_period']['dates'],
            'days': len(early_period),
            'avg_conversion_rate': round(conversion_summary['evolution']['early_period']['avg_conversion'], 2),
            'avg_aov': round(conversion_summary['evolution']['early_period']['avg_aov'], 2),
            'total_transactions': int(early_period['transactions'].sum()),
            'total_revenue': round(early_period['daily_revenue'].sum(), 2)
        },
        {
            'period': 'Mid',
            'dates': conversion_summary['evolution']['mid_period']['dates'],
            'days': len(mid_period),
            'avg_conversion_rate': round(conversion_summary['evolution']['mid_period']['avg_conversion'], 2),
            'avg_aov': round(conversion_summary['evolution']['mid_period']['avg_aov'], 2),
            'total_transactions': int(mid_period['transactions'].sum()),
            'total_revenue': round(mid_period['daily_revenue'].sum(), 2)
        },
        {
            'period': 'Late',
            'dates': conversion_summary['evolution']['late_period']['dates'],
            'days': len(late_period),
            'avg_conversion_rate': round(conversion_summary['evolution']['late_period']['avg_conversion'], 2),
            'avg_aov': round(conversion_summary['evolution']['late_period']['avg_aov'], 2),
            'total_transactions': int(late_period['transactions'].sum()),
            'total_revenue': round(late_period['daily_revenue'].sum(), 2)
        }
    ])
    
    # Ajouter variations
    evolution_df['conversion_change_pct'] = (
        (evolution_df['avg_conversion_rate'] / evolution_df['avg_conversion_rate'].iloc[0] - 1) * 100
    ).round(2)
    evolution_df['aov_change_pct'] = (
        (evolution_df['avg_aov'] / evolution_df['avg_aov'].iloc[0] - 1) * 100
    ).round(2)
    
    output_evolution = output_dir / 'conversion_evolution.csv'
    evolution_df.to_csv(output_evolution, index=False)
    print(f"[OK] {output_evolution}")
    print(f"     {len(evolution_df)} périodes, {len(evolution_df.columns)} colonnes")
    
    # Créer top_converting_products.csv
    print("\nGénération de top_converting_products.csv...")
    top_products = products.nlargest(100, 'view_to_purchase_rate')[[
        'rank', 'product_id', 'category', 'unique_users', 'views', 'purchases',
        'view_to_cart_rate', 'view_to_purchase_rate', 'cart_to_purchase_rate',
        'total_revenue', 'avg_price', 'revenue_per_user'
    ]].copy()
    
    output_top = output_dir / 'top_converting_products.csv'
    top_products.to_csv(output_top, index=False)
    print(f"[OK] {output_top}")
    print(f"     {len(top_products)} produits, {len(top_products.columns)} colonnes")
    
    print_separator("RESUME FINAL")
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ Analyse des conversions terminée avec succès!")
    print(f"\n📊 Métriques globales:")
    print(f"   • Taux view → cart: {conversion_summary['conversion_rates']['view_to_cart']:.2f}%")
    print(f"   • Taux view → transaction: {conversion_summary['conversion_rates']['view_to_transaction']:.2f}%")
    print(f"   • Taux cart → transaction: {conversion_summary['conversion_rates']['cart_to_transaction']:.2f}%")
    print(f"   • Taux user → transaction: {conversion_summary['conversion_rates']['user_to_transaction']:.2f}%")
    print(f"   • AOV moyen: €{conversion_summary['aov_analysis']['mean']:.2f}")
    print(f"\n📈 Evolution:")
    print(f"   • Tendance conversion: {conversion_summary['evolution']['conversion_trend']:+.1f}%")
    print(f"   • Tendance AOV: {conversion_summary['evolution']['aov_trend']:+.1f}%")
    print(f"\n👥 Meilleur segment:")
    best_seg = max(segment_conversion.items(), key=lambda x: x[1]['conversion_rate'])
    print(f"   • {best_seg[0].capitalize()}: {best_seg[1]['conversion_rate']:.2f}%")
    print(f"\n📁 Fichiers générés:")
    print(f"   • conversion_analysis_summary.json")
    print(f"   • conversion_daily.csv ({len(conversion_daily)} lignes)")
    print(f"   • conversion_by_segment.csv ({len(segment_conv_df)} lignes)")
    print(f"   • conversion_by_weekday.csv ({len(weekday_conv_df)} lignes)")
    print(f"   • conversion_evolution.csv ({len(evolution_df)} lignes)")
    print(f"   • top_converting_products.csv ({len(top_products)} lignes)")
    print(f"\n⏱️  Temps d'exécution: {execution_time:.2f}s")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
