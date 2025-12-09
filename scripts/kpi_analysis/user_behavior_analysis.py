#!/usr/bin/env python3
"""
Script d'analyse du comportement utilisateur - Issue #10
Génère des analyses détaillées du comportement, engagement et parcours utilisateur.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #10 - Analyse comportement utilisateur
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
    """Analyse du comportement utilisateur: engagement, parcours, patterns"""
    print_separator("ANALYSE COMPORTEMENT UTILISATEUR - ISSUE #10")
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
    
    # Charger segment_performance.csv
    print("\nChargement de segment_performance.csv...")
    segments = pd.read_csv(data_dir / 'segment_performance.csv')
    print(f"[OK] {len(segments)} segments chargés")
    
    # Charger daily_funnel.csv
    funnel_file = data_dir / 'daily_funnel.csv'
    if funnel_file.exists():
        print("\nChargement de daily_funnel.csv...")
        funnel = pd.read_csv(funnel_file)
        print(f"[OK] {len(funnel)} jours chargés")
    else:
        funnel = None
        print("\n[INFO] daily_funnel.csv non trouvé")
    
    print_separator("ANALYSE DU COMPORTEMENT UTILISATEUR")
    
    # 1. METRIQUES D'ENGAGEMENT GLOBALES
    print("1. Calcul des métriques d'engagement...")
    
    behavior_summary = {
        'engagement_metrics': {
            'avg_events_per_user': float(daily_metrics['events_per_user'].mean()),
            'median_events_per_user': float(daily_metrics['events_per_user'].median()),
            'max_events_per_user': float(daily_metrics['events_per_user'].max()),
            'min_events_per_user': float(daily_metrics['events_per_user'].min()),
            'total_events': int(daily_metrics['total_events'].sum()),
            'total_views': int(daily_metrics['views'].sum()),
            'total_add_to_carts': int(daily_metrics['add_to_carts'].sum()),
            'total_transactions': int(daily_metrics['transactions'].sum())
        }
    }
    
    # Calculer les taux de conversion moyens
    behavior_summary['conversion_rates'] = {
        'avg_view_to_cart': float(daily_metrics['view_to_cart_rate'].mean()),
        'avg_view_to_purchase': float(daily_metrics['view_to_purchase_rate'].mean()),
        'avg_cart_to_purchase': float(daily_metrics['cart_to_purchase_rate'].mean()),
        'overall_conversion': float(daily_metrics['transactions'].sum() / daily_metrics['unique_users'].sum() * 100)
    }
    
    print(f"   Événements/utilisateur (moyenne): {behavior_summary['engagement_metrics']['avg_events_per_user']:.2f}")
    print(f"   Taux view → cart: {behavior_summary['conversion_rates']['avg_view_to_cart']:.2f}%")
    print(f"   Taux view → purchase: {behavior_summary['conversion_rates']['avg_view_to_purchase']:.2f}%")
    print(f"   Taux cart → purchase: {behavior_summary['conversion_rates']['avg_cart_to_purchase']:.2f}%")
    print(f"   Conversion globale: {behavior_summary['conversion_rates']['overall_conversion']:.2f}%")
    
    # 2. ANALYSE PAR SEGMENT UTILISATEUR
    print("\n2. Analyse comportementale par segment...")
    
    segment_behavior = {}
    total_users = segments['num_users'].sum()
    total_revenue = segments['total_revenue'].sum()
    
    for _, row in segments.iterrows():
        segment_name = row['segment'].lower()
        segment_behavior[segment_name] = {
            'users': int(row['num_users']),
            'users_pct': float(row['num_users'] / total_users * 100),
            'revenue': float(row['total_revenue']),
            'revenue_pct': float(row['total_revenue'] / total_revenue * 100),
            'revenue_per_user': float(row['revenue_per_user']),
            'transactions': int(row['num_transactions']),
            'avg_transaction': float(row['avg_transaction']),
            'transactions_per_user': float(row['num_transactions'] / row['num_users'])
        }
    
    behavior_summary['segments'] = segment_behavior
    
    print("\n   Segment Performance:")
    for seg, data in segment_behavior.items():
        print(f"   • {seg.capitalize():12s}: {data['users']:6,} users ({data['users_pct']:5.1f}%) | "
              f"€{data['revenue_per_user']:7.2f}/user | {data['transactions_per_user']:.2f} trans/user")
    
    # 3. ANALYSE DU FUNNEL DE CONVERSION
    print("\n3. Analyse du funnel de conversion...")
    
    if funnel is not None and len(funnel) > 0:
        # Calculer les métriques du funnel
        total_funnel = {
            'viewers': int(funnel['unique_viewers'].sum()) if 'unique_viewers' in funnel.columns else int(daily_metrics['unique_users'].sum()),
            'cart_users': int(funnel['unique_cart_users'].sum()) if 'unique_cart_users' in funnel.columns else int(daily_metrics['add_to_carts'].sum()),
            'buyers': int(funnel['unique_buyers'].sum()) if 'unique_buyers' in funnel.columns else int(daily_metrics['transactions'].sum())
        }
    else:
        # Estimer à partir des daily_metrics
        total_funnel = {
            'viewers': int(daily_metrics['unique_users'].sum()),
            'cart_users': int(daily_metrics['add_to_carts'].sum()),
            'buyers': int(daily_metrics['transactions'].sum())
        }
    
    # Calcul des drop-offs
    total_funnel['viewer_to_cart_rate'] = (total_funnel['cart_users'] / total_funnel['viewers'] * 100) if total_funnel['viewers'] > 0 else 0
    total_funnel['cart_to_buyer_rate'] = (total_funnel['buyers'] / total_funnel['cart_users'] * 100) if total_funnel['cart_users'] > 0 else 0
    total_funnel['viewer_to_buyer_rate'] = (total_funnel['buyers'] / total_funnel['viewers'] * 100) if total_funnel['viewers'] > 0 else 0
    
    total_funnel['dropoff_viewer_to_cart'] = 100 - total_funnel['viewer_to_cart_rate']
    total_funnel['dropoff_cart_to_buyer'] = 100 - total_funnel['cart_to_buyer_rate']
    
    behavior_summary['funnel'] = total_funnel
    
    print(f"   Viewers: {total_funnel['viewers']:,}")
    print(f"   → Cart users: {total_funnel['cart_users']:,} ({total_funnel['viewer_to_cart_rate']:.2f}%)")
    print(f"     Drop-off: {total_funnel['dropoff_viewer_to_cart']:.2f}%")
    print(f"   → Buyers: {total_funnel['buyers']:,} ({total_funnel['cart_to_buyer_rate']:.2f}%)")
    print(f"     Drop-off: {total_funnel['dropoff_cart_to_buyer']:.2f}%")
    print(f"   Conversion globale: {total_funnel['viewer_to_buyer_rate']:.2f}%")
    
    # 4. PATTERNS TEMPORELS DE COMPORTEMENT
    print("\n4. Analyse des patterns temporels...")
    
    daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
    
    # Comportement semaine vs week-end
    weekday_behavior = daily_metrics[~daily_metrics['is_weekend']].agg({
        'events_per_user': 'mean',
        'view_to_cart_rate': 'mean',
        'view_to_purchase_rate': 'mean',
        'cart_to_purchase_rate': 'mean',
        'revenue_per_user': 'mean'
    })
    
    weekend_behavior = daily_metrics[daily_metrics['is_weekend']].agg({
        'events_per_user': 'mean',
        'view_to_cart_rate': 'mean',
        'view_to_purchase_rate': 'mean',
        'cart_to_purchase_rate': 'mean',
        'revenue_per_user': 'mean'
    })
    
    behavior_summary['temporal_patterns'] = {
        'weekday': {
            'events_per_user': float(weekday_behavior['events_per_user']),
            'view_to_cart_rate': float(weekday_behavior['view_to_cart_rate']),
            'view_to_purchase_rate': float(weekday_behavior['view_to_purchase_rate']),
            'cart_to_purchase_rate': float(weekday_behavior['cart_to_purchase_rate']),
            'revenue_per_user': float(weekday_behavior['revenue_per_user'])
        },
        'weekend': {
            'events_per_user': float(weekend_behavior['events_per_user']),
            'view_to_cart_rate': float(weekend_behavior['view_to_cart_rate']),
            'view_to_purchase_rate': float(weekend_behavior['view_to_purchase_rate']),
            'cart_to_purchase_rate': float(weekend_behavior['cart_to_purchase_rate']),
            'revenue_per_user': float(weekend_behavior['revenue_per_user'])
        }
    }
    
    # Calculer les variations week-end
    for metric in ['events_per_user', 'view_to_cart_rate', 'revenue_per_user']:
        weekday_val = behavior_summary['temporal_patterns']['weekday'][metric]
        weekend_val = behavior_summary['temporal_patterns']['weekend'][metric]
        variation = ((weekend_val / weekday_val - 1) * 100) if weekday_val > 0 else 0
        behavior_summary['temporal_patterns'][f'{metric}_weekend_variation'] = float(variation)
    
    print(f"   Engagement semaine: {weekday_behavior['events_per_user']:.2f} événements/user")
    print(f"   Engagement week-end: {weekend_behavior['events_per_user']:.2f} événements/user")
    print(f"   Variation: {behavior_summary['temporal_patterns']['events_per_user_weekend_variation']:+.1f}%")
    
    # 5. EVOLUTION DU COMPORTEMENT
    print("\n5. Analyse de l'évolution temporelle...")
    
    # Diviser en périodes
    daily_metrics = daily_metrics.sort_values('date')
    n_days = len(daily_metrics)
    period1 = daily_metrics.iloc[:n_days//3]
    period2 = daily_metrics.iloc[n_days//3:2*n_days//3]
    period3 = daily_metrics.iloc[2*n_days//3:]
    
    evolution = {
        'period1': {
            'dates': f"{period1['date'].min().strftime('%Y-%m-%d')} → {period1['date'].max().strftime('%Y-%m-%d')}",
            'events_per_user': float(period1['events_per_user'].mean()),
            'conversion_rate': float(period1['view_to_purchase_rate'].mean()),
            'revenue_per_user': float(period1['revenue_per_user'].mean())
        },
        'period2': {
            'dates': f"{period2['date'].min().strftime('%Y-%m-%d')} → {period2['date'].max().strftime('%Y-%m-%d')}",
            'events_per_user': float(period2['events_per_user'].mean()),
            'conversion_rate': float(period2['view_to_purchase_rate'].mean()),
            'revenue_per_user': float(period2['revenue_per_user'].mean())
        },
        'period3': {
            'dates': f"{period3['date'].min().strftime('%Y-%m-%d')} → {period3['date'].max().strftime('%Y-%m-%d')}",
            'events_per_user': float(period3['events_per_user'].mean()),
            'conversion_rate': float(period3['view_to_purchase_rate'].mean()),
            'revenue_per_user': float(period3['revenue_per_user'].mean())
        }
    }
    
    behavior_summary['evolution'] = evolution
    
    print(f"   Période 1 ({evolution['period1']['dates']}):")
    print(f"     Engagement: {evolution['period1']['events_per_user']:.2f} evt/user | "
          f"Conversion: {evolution['period1']['conversion_rate']:.2f}%")
    print(f"   Période 3 ({evolution['period3']['dates']}):")
    print(f"     Engagement: {evolution['period3']['events_per_user']:.2f} evt/user | "
          f"Conversion: {evolution['period3']['conversion_rate']:.2f}%")
    
    print_separator("GENERATION DES FICHIERS")
    
    # Sauvegarder le résumé JSON
    output_json = output_dir / 'user_behavior_summary.json'
    print(f"Sauvegarde de {output_json.name}...")
    behavior_summary['metadata'] = {
        'generated_at': datetime.now().isoformat(),
        'script': 'user_behavior_analysis.py',
        'issue': '#10'
    }
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(behavior_summary, f, indent=2, ensure_ascii=False)
    print(f"[OK] {output_json}")
    
    # Créer behavior_daily.csv avec métriques comportementales
    print("\nGénération de behavior_daily.csv...")
    behavior_daily = daily_metrics[[
        'date', 'day_of_week', 'is_weekend',
        'unique_users', 'total_events', 'views', 'add_to_carts', 'transactions',
        'events_per_user', 'view_to_cart_rate', 'view_to_purchase_rate', 
        'cart_to_purchase_rate', 'revenue_per_user',
        'users_new', 'users_occasional', 'users_regular', 'users_premium'
    ]].copy()
    
    # Ajouter métriques dérivées
    behavior_daily['engagement_score'] = (
        (behavior_daily['events_per_user'] - behavior_daily['events_per_user'].min()) /
        (behavior_daily['events_per_user'].max() - behavior_daily['events_per_user'].min()) * 100
    ).round(2)
    
    behavior_daily['conversion_score'] = (
        (behavior_daily['view_to_purchase_rate'] - behavior_daily['view_to_purchase_rate'].min()) /
        (behavior_daily['view_to_purchase_rate'].max() - behavior_daily['view_to_purchase_rate'].min()) * 100
    ).round(2)
    
    # Moyennes mobiles 7 jours
    behavior_daily['ma7_engagement'] = behavior_daily['events_per_user'].rolling(window=7, min_periods=1).mean().round(2)
    behavior_daily['ma7_view_to_cart'] = behavior_daily['view_to_cart_rate'].rolling(window=7, min_periods=1).mean().round(2)
    behavior_daily['ma7_conversion'] = behavior_daily['view_to_purchase_rate'].rolling(window=7, min_periods=1).mean().round(2)
    
    output_csv = output_dir / 'behavior_daily.csv'
    behavior_daily.to_csv(output_csv, index=False)
    print(f"[OK] {output_csv}")
    print(f"     {len(behavior_daily)} jours, {len(behavior_daily.columns)} colonnes")
    
    # Créer segment_behavior_comparison.csv
    print("\nGénération de segment_behavior_comparison.csv...")
    segment_comparison = segments.copy()
    segment_comparison['transactions_per_user'] = (segment_comparison['num_transactions'] / 
                                                    segment_comparison['num_users']).round(2)
    segment_comparison['revenue_share'] = (segment_comparison['total_revenue'] / 
                                           segment_comparison['total_revenue'].sum() * 100).round(2)
    segment_comparison['user_share'] = (segment_comparison['num_users'] / 
                                        segment_comparison['num_users'].sum() * 100).round(2)
    segment_comparison['value_index'] = (segment_comparison['revenue_share'] / 
                                         segment_comparison['user_share']).round(2)
    
    # Réordonner par revenue_per_user
    segment_comparison = segment_comparison.sort_values('revenue_per_user', ascending=False)
    
    output_segment = output_dir / 'segment_behavior_comparison.csv'
    segment_comparison.to_csv(output_segment, index=False)
    print(f"[OK] {output_segment}")
    print(f"     {len(segment_comparison)} segments, {len(segment_comparison.columns)} colonnes")
    
    # Créer conversion_funnel_analysis.csv
    print("\nGénération de conversion_funnel_analysis.csv...")
    funnel_analysis = pd.DataFrame([
        {
            'stage': 'Viewers',
            'users': total_funnel['viewers'],
            'percentage_of_initial': 100.0,
            'drop_off_rate': 0.0,
            'conversion_to_next': total_funnel['viewer_to_cart_rate']
        },
        {
            'stage': 'Cart Users',
            'users': total_funnel['cart_users'],
            'percentage_of_initial': round(total_funnel['cart_users'] / total_funnel['viewers'] * 100, 2),
            'drop_off_rate': round(total_funnel['dropoff_viewer_to_cart'], 2),
            'conversion_to_next': total_funnel['cart_to_buyer_rate']
        },
        {
            'stage': 'Buyers',
            'users': total_funnel['buyers'],
            'percentage_of_initial': round(total_funnel['buyers'] / total_funnel['viewers'] * 100, 2),
            'drop_off_rate': round(total_funnel['dropoff_cart_to_buyer'], 2),
            'conversion_to_next': 0.0
        }
    ])
    
    output_funnel = output_dir / 'conversion_funnel_analysis.csv'
    funnel_analysis.to_csv(output_funnel, index=False)
    print(f"[OK] {output_funnel}")
    print(f"     {len(funnel_analysis)} étapes, {len(funnel_analysis.columns)} colonnes")
    
    # Créer behavior_evolution.csv
    print("\nGénération de behavior_evolution.csv...")
    evolution_df = pd.DataFrame([
        {
            'period': 'Période 1',
            'dates': evolution['period1']['dates'],
            'days': len(period1),
            'avg_events_per_user': evolution['period1']['events_per_user'],
            'avg_conversion_rate': evolution['period1']['conversion_rate'],
            'avg_revenue_per_user': evolution['period1']['revenue_per_user']
        },
        {
            'period': 'Période 2',
            'dates': evolution['period2']['dates'],
            'days': len(period2),
            'avg_events_per_user': evolution['period2']['events_per_user'],
            'avg_conversion_rate': evolution['period2']['conversion_rate'],
            'avg_revenue_per_user': evolution['period2']['revenue_per_user']
        },
        {
            'period': 'Période 3',
            'dates': evolution['period3']['dates'],
            'days': len(period3),
            'avg_events_per_user': evolution['period3']['events_per_user'],
            'avg_conversion_rate': evolution['period3']['conversion_rate'],
            'avg_revenue_per_user': evolution['period3']['revenue_per_user']
        }
    ])
    
    # Calculer les variations
    evolution_df['engagement_change_pct'] = (
        (evolution_df['avg_events_per_user'] / evolution_df['avg_events_per_user'].iloc[0] - 1) * 100
    ).round(2)
    evolution_df['conversion_change_pct'] = (
        (evolution_df['avg_conversion_rate'] / evolution_df['avg_conversion_rate'].iloc[0] - 1) * 100
    ).round(2)
    evolution_df['revenue_change_pct'] = (
        (evolution_df['avg_revenue_per_user'] / evolution_df['avg_revenue_per_user'].iloc[0] - 1) * 100
    ).round(2)
    
    output_evolution = output_dir / 'behavior_evolution.csv'
    evolution_df.to_csv(output_evolution, index=False)
    print(f"[OK] {output_evolution}")
    print(f"     {len(evolution_df)} périodes, {len(evolution_df.columns)} colonnes")
    
    print_separator("RESUME FINAL")
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ Analyse du comportement utilisateur terminée avec succès!")
    print(f"\n📊 Métriques d'engagement:")
    print(f"   • Événements/utilisateur: {behavior_summary['engagement_metrics']['avg_events_per_user']:.2f}")
    print(f"   • Taux view → cart: {behavior_summary['conversion_rates']['avg_view_to_cart']:.2f}%")
    print(f"   • Taux view → purchase: {behavior_summary['conversion_rates']['avg_view_to_purchase']:.2f}%")
    print(f"   • Taux cart → purchase: {behavior_summary['conversion_rates']['avg_cart_to_purchase']:.2f}%")
    print(f"   • Conversion globale: {behavior_summary['conversion_rates']['overall_conversion']:.2f}%")
    print(f"\n🎯 Funnel de conversion:")
    print(f"   • Viewers → Cart: {total_funnel['viewer_to_cart_rate']:.2f}% (drop-off: {total_funnel['dropoff_viewer_to_cart']:.2f}%)")
    print(f"   • Cart → Buyers: {total_funnel['cart_to_buyer_rate']:.2f}% (drop-off: {total_funnel['dropoff_cart_to_buyer']:.2f}%)")
    print(f"\n👥 Top segment (valeur/user):")
    top_segment = max(segment_behavior.items(), key=lambda x: x[1]['revenue_per_user'])
    print(f"   • {top_segment[0].capitalize()}: €{top_segment[1]['revenue_per_user']:.2f}/user")
    print(f"\n📁 Fichiers générés:")
    print(f"   • user_behavior_summary.json")
    print(f"   • behavior_daily.csv ({len(behavior_daily)} lignes)")
    print(f"   • segment_behavior_comparison.csv ({len(segment_comparison)} lignes)")
    print(f"   • conversion_funnel_analysis.csv ({len(funnel_analysis)} lignes)")
    print(f"   • behavior_evolution.csv ({len(evolution_df)} lignes)")
    print(f"\n⏱️  Temps d'exécution: {execution_time:.2f}s")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
