#!/usr/bin/env python3
"""
Script d'analyse du funnel view → cart → purchase - Issue #13
Génère des analyses détaillées du parcours d'achat et des points de friction.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #13 - Funnel view → cart → purchase
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
    """Analyse détaillée du funnel de conversion view → cart → purchase"""
    print_separator("ANALYSE DU FUNNEL VIEW → CART → PURCHASE - ISSUE #13")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    print_separator("CHARGEMENT DES DONNEES")
    
    # Charger les données
    print("Chargement de daily_funnel.csv...")
    daily_funnel = pd.read_csv(data_dir / 'daily_funnel.csv')
    print(f"[OK] {len(daily_funnel)} jours chargés")
    
    print("\nChargement de daily_metrics.csv...")
    daily_metrics = pd.read_csv(data_dir / 'daily_metrics.csv')
    print(f"[OK] {len(daily_metrics)} jours chargés")
    
    print("\nChargement de segment_performance.csv...")
    segments = pd.read_csv(data_dir / 'segment_performance.csv')
    print(f"[OK] {len(segments)} segments chargés")
    
    print("\nChargement de products_summary.csv...")
    products = pd.read_csv(data_dir / 'products_summary.csv')
    print(f"[OK] {len(products)} produits chargés")
    
    print_separator("ANALYSE DU FUNNEL GLOBAL")
    
    # 1. FUNNEL GLOBAL - Vue d'ensemble
    print("1. Calcul des métriques du funnel global...")
    
    total_views = daily_funnel['view'].sum()
    total_carts = daily_funnel['addtocart'].sum()
    total_purchases = daily_funnel['transaction'].sum()
    unique_users_total = daily_metrics['unique_users'].sum()
    
    # Taux de conversion par étape
    view_to_cart_rate = (total_carts / total_views) * 100 if total_views > 0 else 0
    cart_to_purchase_rate = (total_purchases / total_carts) * 100 if total_carts > 0 else 0
    view_to_purchase_rate = (total_purchases / total_views) * 100 if total_views > 0 else 0
    
    # Drop-off par étape
    view_to_cart_dropoff = 100 - view_to_cart_rate
    cart_to_purchase_dropoff = 100 - cart_to_purchase_rate
    
    funnel_summary = {
        'period': {
            'start_date': str(daily_funnel['date'].min()),
            'end_date': str(daily_funnel['date'].max()),
            'days': len(daily_funnel)
        },
        'funnel_stages': {
            'view': {
                'total': int(total_views),
                'avg_daily': float(total_views / len(daily_funnel)),
                'unique_users': int(unique_users_total),
                'percentage_of_users': 100.0
            },
            'cart': {
                'total': int(total_carts),
                'avg_daily': float(total_carts / len(daily_funnel)),
                'percentage_of_views': float(view_to_cart_rate),
                'dropoff_from_view': float(view_to_cart_dropoff)
            },
            'purchase': {
                'total': int(total_purchases),
                'avg_daily': float(total_purchases / len(daily_funnel)),
                'percentage_of_carts': float(cart_to_purchase_rate),
                'percentage_of_views': float(view_to_purchase_rate),
                'dropoff_from_cart': float(cart_to_purchase_dropoff)
            }
        },
        'conversion_rates': {
            'view_to_cart': float(view_to_cart_rate),
            'cart_to_purchase': float(cart_to_purchase_rate),
            'view_to_purchase': float(view_to_purchase_rate),
            'overall_efficiency': float(view_to_purchase_rate)
        },
        'drop_off_analysis': {
            'view_to_cart_loss': {
                'rate': float(view_to_cart_dropoff),
                'absolute': int(total_views - total_carts)
            },
            'cart_to_purchase_loss': {
                'rate': float(cart_to_purchase_dropoff),
                'absolute': int(total_carts - total_purchases)
            },
            'total_loss_from_view': {
                'rate': float(100 - view_to_purchase_rate),
                'absolute': int(total_views - total_purchases)
            }
        }
    }
    
    print(f"   Vue → Panier: {view_to_cart_rate:.2f}% (perte: {view_to_cart_dropoff:.2f}%)")
    print(f"   Panier → Achat: {cart_to_purchase_rate:.2f}% (perte: {cart_to_purchase_dropoff:.2f}%)")
    print(f"   Vue → Achat: {view_to_purchase_rate:.2f}%")
    print(f"   Perte totale: {total_views - total_purchases:,} événements")
    
    # 2. FUNNEL PAR JOUR - Évolution temporelle
    print("\n2. Analyse du funnel par jour...")
    
    daily_funnel['date'] = pd.to_datetime(daily_funnel['date'])
    daily_funnel['weekday'] = daily_funnel['date'].dt.day_name()
    daily_funnel['week'] = daily_funnel['date'].dt.isocalendar().week
    daily_funnel['month'] = daily_funnel['date'].dt.to_period('M').astype(str)
    
    # Calculer les taux de conversion quotidiens
    daily_funnel['view_to_cart_pct'] = (daily_funnel['addtocart'] / daily_funnel['view'] * 100).fillna(0)
    daily_funnel['cart_to_purchase_pct'] = (daily_funnel['transaction'] / daily_funnel['addtocart'] * 100).fillna(0)
    daily_funnel['view_to_purchase_pct'] = (daily_funnel['transaction'] / daily_funnel['view'] * 100).fillna(0)
    
    # Statistiques sur les variations
    funnel_summary['daily_statistics'] = {
        'view_to_cart': {
            'mean': float(daily_funnel['view_to_cart_pct'].mean()),
            'median': float(daily_funnel['view_to_cart_pct'].median()),
            'std': float(daily_funnel['view_to_cart_pct'].std()),
            'min': float(daily_funnel['view_to_cart_pct'].min()),
            'max': float(daily_funnel['view_to_cart_pct'].max())
        },
        'cart_to_purchase': {
            'mean': float(daily_funnel['cart_to_purchase_pct'].mean()),
            'median': float(daily_funnel['cart_to_purchase_pct'].median()),
            'std': float(daily_funnel['cart_to_purchase_pct'].std()),
            'min': float(daily_funnel['cart_to_purchase_pct'].min()),
            'max': float(daily_funnel['cart_to_purchase_pct'].max())
        },
        'view_to_purchase': {
            'mean': float(daily_funnel['view_to_purchase_pct'].mean()),
            'median': float(daily_funnel['view_to_purchase_pct'].median()),
            'std': float(daily_funnel['view_to_purchase_pct'].std()),
            'min': float(daily_funnel['view_to_purchase_pct'].min()),
            'max': float(daily_funnel['view_to_purchase_pct'].max())
        }
    }
    
    print(f"   Variation view→cart: {daily_funnel['view_to_cart_pct'].std():.2f}% std")
    print(f"   Meilleur jour: {daily_funnel['view_to_cart_pct'].max():.2f}%")
    print(f"   Pire jour: {daily_funnel['view_to_cart_pct'].min():.2f}%")
    
    # 3. FUNNEL PAR JOUR DE SEMAINE
    print("\n3. Analyse du funnel par jour de semaine...")
    
    weekday_funnel = daily_funnel.groupby('weekday').agg({
        'view': 'sum',
        'addtocart': 'sum',
        'transaction': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    weekday_funnel['view_to_cart_pct'] = (weekday_funnel['addtocart'] / weekday_funnel['view'] * 100).round(2)
    weekday_funnel['cart_to_purchase_pct'] = (weekday_funnel['transaction'] / weekday_funnel['addtocart'] * 100).round(2)
    weekday_funnel['view_to_purchase_pct'] = (weekday_funnel['transaction'] / weekday_funnel['view'] * 100).round(2)
    weekday_funnel['views_per_user'] = (weekday_funnel['view'] / weekday_funnel['unique_users']).round(2)
    weekday_funnel['carts_per_user'] = (weekday_funnel['addtocart'] / weekday_funnel['unique_users']).round(2)
    weekday_funnel['purchases_per_user'] = (weekday_funnel['transaction'] / weekday_funnel['unique_users']).round(2)
    
    # Ordonner les jours
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_funnel['weekday'] = pd.Categorical(weekday_funnel['weekday'], categories=weekday_order, ordered=True)
    weekday_funnel = weekday_funnel.sort_values('weekday')
    
    best_day = weekday_funnel.loc[weekday_funnel['view_to_purchase_pct'].idxmax(), 'weekday']
    worst_day = weekday_funnel.loc[weekday_funnel['view_to_purchase_pct'].idxmin(), 'weekday']
    
    funnel_summary['weekday_analysis'] = {
        'best_conversion_day': str(best_day),
        'best_conversion_rate': float(weekday_funnel['view_to_purchase_pct'].max()),
        'worst_conversion_day': str(worst_day),
        'worst_conversion_rate': float(weekday_funnel['view_to_purchase_pct'].min()),
        'weekend_vs_weekday': {
            'weekend_avg': float(weekday_funnel[weekday_funnel['weekday'].isin(['Saturday', 'Sunday'])]['view_to_purchase_pct'].mean()),
            'weekday_avg': float(weekday_funnel[~weekday_funnel['weekday'].isin(['Saturday', 'Sunday'])]['view_to_purchase_pct'].mean())
        }
    }
    
    print(f"   Meilleur jour: {best_day} ({weekday_funnel['view_to_purchase_pct'].max():.2f}%)")
    print(f"   Pire jour: {worst_day} ({weekday_funnel['view_to_purchase_pct'].min():.2f}%)")
    
    # 4. FUNNEL PAR SEGMENT UTILISATEUR
    print("\n4. Analyse du funnel par segment utilisateur...")
    
    # Calculer les métriques par segment en utilisant daily_metrics
    daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
    
    segment_funnel = []
    total_users = segments['num_users'].sum()
    total_revenue = segments['total_revenue'].sum()
    
    for _, seg in segments.iterrows():
        segment_name = seg['segment']
        
        # Calculer les pourcentages
        user_pct = (seg['num_users'] / total_users * 100) if total_users > 0 else 0
        revenue_pct = (seg['total_revenue'] / total_revenue * 100) if total_revenue > 0 else 0
        
        # Calculer les événements moyens
        avg_transactions_per_user = seg['num_transactions'] / seg['num_users'] if seg['num_users'] > 0 else 0
        
        segment_funnel.append({
            'segment': segment_name,
            'num_users': int(seg['num_users']),
            'user_percentage': round(user_pct, 2),
            'num_transactions': int(seg['num_transactions']),
            'transactions_per_user': round(avg_transactions_per_user, 2),
            'revenue_per_user': round(seg['revenue_per_user'], 2),
            'total_revenue': round(seg['total_revenue'], 2),
            'revenue_percentage': round(revenue_pct, 2),
            'avg_transaction_value': round(seg['avg_transaction'], 2),
            'conversion_rate': round((seg['num_transactions'] / seg['num_users'] * 100) if seg['num_users'] > 0 else 0, 2)
        })
    
    segment_funnel_df = pd.DataFrame(segment_funnel)
    segment_funnel_df = segment_funnel_df.sort_values('revenue_per_user', ascending=False)
    
    # Meilleur et pire segment
    best_segment = segment_funnel_df.iloc[0]
    worst_segment = segment_funnel_df.iloc[-1]
    
    funnel_summary['segment_analysis'] = {
        'best_segment': {
            'name': str(best_segment['segment']),
            'revenue_per_user': float(best_segment['revenue_per_user']),
            'conversion_rate': float(best_segment['conversion_rate']),
            'transactions_per_user': float(best_segment['transactions_per_user'])
        },
        'worst_segment': {
            'name': str(worst_segment['segment']),
            'revenue_per_user': float(worst_segment['revenue_per_user']),
            'conversion_rate': float(worst_segment['conversion_rate']),
            'transactions_per_user': float(worst_segment['transactions_per_user'])
        },
        'segment_comparison': segment_funnel_df.to_dict('records')
    }
    
    print(f"   Meilleur segment: {best_segment['segment']} (€{best_segment['revenue_per_user']:.2f}/user)")
    print(f"   Pire segment: {worst_segment['segment']} (€{worst_segment['revenue_per_user']:.2f}/user)")
    
    # 5. ANALYSE DES PRODUITS DANS LE FUNNEL
    print("\n5. Analyse des produits dans le funnel...")
    
    # Produits avec vues mais sans ajout au panier
    products_no_cart = products[(products['views'] > 0) & (products['add_to_carts'] == 0)]
    
    # Produits avec panier mais sans achat
    products_no_purchase = products[(products['add_to_carts'] > 0) & (products['purchases'] == 0)]
    
    # Produits avec bon taux de conversion view→cart (utiliser les colonnes existantes)
    # Les taux sont déjà calculés dans le CSV
    high_view_to_cart = products[products['view_to_cart_rate'] >= 10].sort_values('total_revenue', ascending=False).head(50)
    high_cart_to_purchase = products[products['cart_to_purchase_rate'] >= 50].sort_values('total_revenue', ascending=False).head(50)
    
    funnel_summary['product_analysis'] = {
        'viewed_not_carted': {
            'count': int(len(products_no_cart)),
            'total_views': int(products_no_cart['views'].sum()),
            'percentage_of_catalog': float(len(products_no_cart) / len(products) * 100)
        },
        'carted_not_purchased': {
            'count': int(len(products_no_purchase)),
            'total_carts': int(products_no_purchase['add_to_carts'].sum()),
            'percentage_of_catalog': float(len(products_no_purchase) / len(products) * 100)
        },
        'high_performers': {
            'high_view_to_cart_count': int(len(high_view_to_cart)),
            'high_cart_to_purchase_count': int(len(high_cart_to_purchase)),
            'avg_view_to_cart_top50': float(high_view_to_cart['view_to_cart_rate'].mean()) if len(high_view_to_cart) > 0 else 0,
            'avg_cart_to_purchase_top50': float(high_cart_to_purchase['cart_to_purchase_rate'].mean()) if len(high_cart_to_purchase) > 0 else 0
        }
    }
    
    print(f"   Produits vus mais jamais ajoutés au panier: {len(products_no_cart):,} ({len(products_no_cart)/len(products)*100:.1f}%)")
    print(f"   Produits en panier mais jamais achetés: {len(products_no_purchase):,} ({len(products_no_purchase)/len(products)*100:.1f}%)")
    print(f"   Produits avec taux view→cart ≥10%: {len(high_view_to_cart):,}")
    
    # 6. ANALYSE TEMPORELLE DÉTAILLÉE
    print("\n6. Analyse de l'évolution temporelle du funnel...")
    
    # Par semaine
    weekly_funnel = daily_funnel.groupby('week').agg({
        'view': 'sum',
        'addtocart': 'sum',
        'transaction': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    weekly_funnel['view_to_cart_pct'] = (weekly_funnel['addtocart'] / weekly_funnel['view'] * 100).round(2)
    weekly_funnel['cart_to_purchase_pct'] = (weekly_funnel['transaction'] / weekly_funnel['addtocart'] * 100).round(2)
    weekly_funnel['view_to_purchase_pct'] = (weekly_funnel['transaction'] / weekly_funnel['view'] * 100).round(2)
    
    # Par mois
    monthly_funnel = daily_funnel.groupby('month').agg({
        'view': 'sum',
        'addtocart': 'sum',
        'transaction': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    monthly_funnel['view_to_cart_pct'] = (monthly_funnel['addtocart'] / monthly_funnel['view'] * 100).round(2)
    monthly_funnel['cart_to_purchase_pct'] = (monthly_funnel['transaction'] / monthly_funnel['addtocart'] * 100).round(2)
    monthly_funnel['view_to_purchase_pct'] = (monthly_funnel['transaction'] / monthly_funnel['view'] * 100).round(2)
    
    # Tendances
    first_week_conv = weekly_funnel.iloc[0]['view_to_purchase_pct']
    last_week_conv = weekly_funnel.iloc[-1]['view_to_purchase_pct']
    conv_evolution = ((last_week_conv - first_week_conv) / first_week_conv * 100) if first_week_conv > 0 else 0
    
    funnel_summary['temporal_evolution'] = {
        'first_week_conversion': float(first_week_conv),
        'last_week_conversion': float(last_week_conv),
        'conversion_evolution_pct': float(conv_evolution),
        'weekly_volatility': float(weekly_funnel['view_to_purchase_pct'].std()),
        'monthly_volatility': float(monthly_funnel['view_to_purchase_pct'].std())
    }
    
    print(f"   Évolution conversion (première→dernière semaine): {conv_evolution:+.1f}%")
    print(f"   Volatilité hebdomadaire: {weekly_funnel['view_to_purchase_pct'].std():.2f}%")
    
    # 7. POINTS DE FRICTION ET OPPORTUNITÉS
    print("\n7. Identification des points de friction...")
    
    # Critères pour identifier les frictions
    avg_view_to_cart = daily_funnel['view_to_cart_pct'].mean()
    avg_cart_to_purchase = daily_funnel['cart_to_purchase_pct'].mean()
    
    # Jours avec forte friction (conversion < moyenne - 1 std)
    std_view_to_cart = daily_funnel['view_to_cart_pct'].std()
    std_cart_to_purchase = daily_funnel['cart_to_purchase_pct'].std()
    
    friction_threshold_cart = avg_view_to_cart - std_view_to_cart
    friction_threshold_purchase = avg_cart_to_purchase - std_cart_to_purchase
    
    high_friction_days = daily_funnel[
        (daily_funnel['view_to_cart_pct'] < friction_threshold_cart) |
        (daily_funnel['cart_to_purchase_pct'] < friction_threshold_purchase)
    ]
    
    funnel_summary['friction_points'] = {
        'high_friction_days_count': int(len(high_friction_days)),
        'high_friction_days_pct': float(len(high_friction_days) / len(daily_funnel) * 100),
        'avg_conversion_friction_days': float(high_friction_days['view_to_purchase_pct'].mean()) if len(high_friction_days) > 0 else 0,
        'avg_conversion_normal_days': float(daily_funnel[~daily_funnel.index.isin(high_friction_days.index)]['view_to_purchase_pct'].mean()),
        'friction_impact': {
            'view_to_cart_threshold': float(friction_threshold_cart),
            'cart_to_purchase_threshold': float(friction_threshold_purchase)
        }
    }
    
    # Opportunités d'amélioration
    # Si on ramène view→cart à +1 std
    potential_carts_gain = total_views * ((avg_view_to_cart + std_view_to_cart) / 100) - total_carts
    potential_purchases_gain = (total_carts + potential_carts_gain) * ((avg_cart_to_purchase + std_cart_to_purchase) / 100) - total_purchases
    
    funnel_summary['improvement_opportunities'] = {
        'view_to_cart_improvement': {
            'current_rate': float(view_to_cart_rate),
            'target_rate': float(avg_view_to_cart + std_view_to_cart),
            'potential_additional_carts': int(potential_carts_gain),
            'potential_additional_carts_pct': float(potential_carts_gain / total_carts * 100) if total_carts > 0 else 0
        },
        'cart_to_purchase_improvement': {
            'current_rate': float(cart_to_purchase_rate),
            'target_rate': float(avg_cart_to_purchase + std_cart_to_purchase),
            'potential_additional_purchases': int(potential_purchases_gain),
            'potential_additional_purchases_pct': float(potential_purchases_gain / total_purchases * 100) if total_purchases > 0 else 0
        }
    }
    
    print(f"   Jours avec forte friction: {len(high_friction_days)} ({len(high_friction_days)/len(daily_funnel)*100:.1f}%)")
    print(f"   Gain potentiel paniers: +{potential_carts_gain:,.0f} ({potential_carts_gain/total_carts*100:.1f}%)")
    print(f"   Gain potentiel achats: +{potential_purchases_gain:,.0f} ({potential_purchases_gain/total_purchases*100:.1f}%)")
    
    print_separator("EXPORT DES RÉSULTATS")
    
    # Export JSON summary
    print("1. Export du résumé JSON...")
    output_file = output_dir / 'funnel_analysis_summary.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(funnel_summary, f, indent=2, ensure_ascii=False)
    print(f"   [OK] {output_file.name} ({output_file.stat().st_size / 1024:.1f} KB)")
    
    # Export funnel daily avec calculs
    print("\n2. Export du funnel quotidien détaillé...")
    funnel_daily_export = daily_funnel[[
        'date', 'weekday', 'week', 'month',
        'unique_users', 'view', 'addtocart', 'transaction',
        'view_to_cart_pct', 'cart_to_purchase_pct', 'view_to_purchase_pct'
    ]].copy()
    
    output_file = output_dir / 'funnel_daily_detailed.csv'
    funnel_daily_export.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(funnel_daily_export)} lignes)")
    
    # Export funnel par jour de semaine
    print("\n3. Export du funnel par jour de semaine...")
    output_file = output_dir / 'funnel_by_weekday.csv'
    weekday_funnel.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(weekday_funnel)} lignes)")
    
    # Export funnel par segment
    print("\n4. Export du funnel par segment...")
    output_file = output_dir / 'funnel_by_segment.csv'
    segment_funnel_df.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(segment_funnel_df)} lignes)")
    
    # Export funnel hebdomadaire
    print("\n5. Export du funnel hebdomadaire...")
    output_file = output_dir / 'funnel_weekly.csv'
    weekly_funnel.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(weekly_funnel)} lignes)")
    
    # Export funnel mensuel
    print("\n6. Export du funnel mensuel...")
    output_file = output_dir / 'funnel_monthly.csv'
    monthly_funnel.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(monthly_funnel)} lignes)")
    
    # Export produits avec problèmes de funnel
    print("\n7. Export des produits bloqués dans le funnel...")
    
    # Top produits vus mais jamais en panier (triés par vues)
    products_blocked_cart = products_no_cart.nlargest(1000, 'views')[[
        'product_id', 'category', 'views', 'add_to_carts', 'purchases',
        'total_revenue', 'avg_price', 'view_to_purchase_rate'
    ]].copy()
    products_blocked_cart['blocking_stage'] = 'view_to_cart'
    
    output_file = output_dir / 'funnel_blocked_products.csv'
    products_blocked_cart.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(products_blocked_cart)} produits)")
    
    # Export jours avec friction
    print("\n8. Export des jours avec forte friction...")
    if len(high_friction_days) > 0:
        friction_export = high_friction_days[[
            'date', 'weekday', 'unique_users', 'view', 'addtocart', 'transaction',
            'view_to_cart_pct', 'cart_to_purchase_pct', 'view_to_purchase_pct'
        ]].copy()
        
        output_file = output_dir / 'funnel_high_friction_days.csv'
        friction_export.to_csv(output_file, index=False)
        print(f"   [OK] {output_file.name} ({len(friction_export)} jours)")
    
    # Export top produits performants
    print("\n9. Export des produits top performers du funnel...")
    
    # Combiner les deux listes
    top_funnel_products = pd.concat([
        high_view_to_cart[['product_id', 'category', 'views', 'add_to_carts', 
                           'purchases', 'total_revenue', 'view_to_cart_rate', 
                           'cart_to_purchase_rate', 'view_to_purchase_rate']].assign(performance_type='High View→Cart'),
        high_cart_to_purchase[['product_id', 'category', 'views', 'add_to_carts',
                                'purchases', 'total_revenue', 'view_to_cart_rate',
                                'cart_to_purchase_rate', 'view_to_purchase_rate']].assign(performance_type='High Cart→Purchase')
    ]).drop_duplicates(subset=['product_id'])
    
    output_file = output_dir / 'funnel_top_performers.csv'
    top_funnel_products.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(top_funnel_products)} produits)")
    
    # Durée d'exécution
    duration = (datetime.now() - start_time).total_seconds()
    
    print_separator("ANALYSE TERMINÉE")
    print(f"✅ Funnel analysé avec succès")
    print(f"📊 9 fichiers générés dans {output_dir}")
    print(f"⏱️  Durée: {duration:.2f}s")
    print(f"\n🎯 POINTS CLÉS:")
    print(f"   • Vue → Panier: {view_to_cart_rate:.2f}% (perte: {view_to_cart_dropoff:.2f}%)")
    print(f"   • Panier → Achat: {cart_to_purchase_rate:.2f}% (perte: {cart_to_purchase_dropoff:.2f}%)")
    print(f"   • Vue → Achat: {view_to_purchase_rate:.2f}%")
    print(f"   • Produits bloqués vue→panier: {len(products_no_cart):,}")
    print(f"   • Produits bloqués panier→achat: {len(products_no_purchase):,}")
    print(f"   • Gain potentiel: +{potential_purchases_gain:,.0f} achats")
    print_separator()

if __name__ == '__main__':
    main()
