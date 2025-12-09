#!/usr/bin/env python3
"""
Script de génération ab_test_simulation.csv - Issue #15
Génère un fichier CSV détaillé combinant les résultats de simulation A/B 
avec des métriques jour par jour pour visualisation et analyse.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #15 - Générer ab_test_simulation.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json

def print_separator(title=""):
    """Affiche un séparateur formaté"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def generate_ab_test_daily_simulation(baseline_data, scenarios, simulation_results, days=30):
    """
    Génère une simulation jour par jour pour chaque scénario A/B
    
    Args:
        baseline_data: DataFrame avec les données baseline quotidiennes
        scenarios: Liste des scénarios de test
        simulation_results: Résultats des simulations Monte Carlo
        days: Nombre de jours à simuler (défaut 30)
    
    Returns:
        DataFrame avec simulation quotidienne détaillée
    """
    all_simulations = []
    
    # Date de début de simulation (aujourd'hui)
    start_date = datetime.now()
    
    # Métriques baseline moyennes
    baseline_users = baseline_data['unique_users'].mean()
    baseline_views = baseline_data['view'].mean()
    baseline_carts = baseline_data['addtocart'].mean()
    baseline_purchases = baseline_data['transaction'].mean()
    
    # Pour chaque scénario
    for scenario in scenarios:
        scenario_id = scenario['id']
        scenario_name = scenario['name']
        
        # Récupérer les résultats de simulation
        sim_result = next((r for r in simulation_results if r['scenario_id'] == scenario_id), None)
        if not sim_result:
            continue
        
        # Générer les données jour par jour
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Variation journalière réaliste (-10% à +15%)
            daily_variance = np.random.uniform(0.9, 1.15)
            
            # Groupe Contrôle (Baseline)
            control_users = int(baseline_users * daily_variance * 0.5)  # 50% split
            control_views = int(baseline_views * daily_variance * 0.5)
            control_carts = int(control_views * scenario['baseline'])
            control_purchases = int(control_carts * (baseline_purchases / baseline_carts))
            
            control_view_to_cart = (control_carts / control_views * 100) if control_views > 0 else 0
            control_cart_to_purchase = (control_purchases / control_carts * 100) if control_carts > 0 else 0
            control_view_to_purchase = (control_purchases / control_views * 100) if control_views > 0 else 0
            
            # Groupe Variant (Optimisé)
            variant_users = int(baseline_users * daily_variance * 0.5)  # 50% split
            variant_views = int(baseline_views * daily_variance * 0.5)
            
            # Appliquer le lift attendu avec un peu de bruit
            lift_noise = np.random.normal(1.0, 0.05)  # ±5% de variance
            effective_variant_rate = scenario['variant'] * lift_noise
            
            variant_carts = int(variant_views * effective_variant_rate)
            variant_purchases = int(variant_carts * (baseline_purchases / baseline_carts))
            
            variant_view_to_cart = (variant_carts / variant_views * 100) if variant_views > 0 else 0
            variant_cart_to_purchase = (variant_purchases / variant_carts * 100) if variant_carts > 0 else 0
            variant_view_to_purchase = (variant_purchases / variant_views * 100) if variant_views > 0 else 0
            
            # Calcul des lifts
            lift_view_to_cart = ((variant_view_to_cart - control_view_to_cart) / control_view_to_cart * 100) if control_view_to_cart > 0 else 0
            lift_cart_to_purchase = ((variant_cart_to_purchase - control_cart_to_purchase) / control_cart_to_purchase * 100) if control_cart_to_purchase > 0 else 0
            lift_view_to_purchase = ((variant_view_to_purchase - control_view_to_purchase) / control_view_to_purchase * 100) if control_view_to_purchase > 0 else 0
            
            # Calcul du revenue (AOV moyen = 255.36€)
            aov = 255.36
            control_revenue = control_purchases * aov
            variant_revenue = variant_purchases * aov
            revenue_lift = variant_revenue - control_revenue
            revenue_lift_pct = (revenue_lift / control_revenue * 100) if control_revenue > 0 else 0
            
            # Test statistique simplifié (Chi-square approximation)
            # Calcul du p-value basé sur la différence observée
            pooled_rate = (control_carts + variant_carts) / (control_views + variant_views)
            pooled_se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_views + 1/variant_views))
            z_score = (variant_view_to_cart/100 - control_view_to_cart/100) / pooled_se if pooled_se > 0 else 0
            
            # P-value approximation (two-tailed)
            from scipy import stats as sp_stats
            p_value = 2 * (1 - sp_stats.norm.cdf(abs(z_score)))
            is_significant = p_value < 0.05
            
            # Confiance (basé sur la taille d'échantillon cumulée)
            cumulative_sample = control_users * (day + 1)
            confidence = min(95, 50 + (cumulative_sample / scenario['sample_size_per_group'] * 45))
            
            # Statut du test
            if day < scenario['test_duration_days']:
                test_status = 'running'
            elif is_significant:
                test_status = 'winner_variant' if lift_view_to_cart > 0 else 'winner_control'
            else:
                test_status = 'inconclusive'
            
            # Enregistrement
            simulation_row = {
                # Métadonnées
                'date': current_date.strftime('%Y-%m-%d'),
                'day_number': day + 1,
                'scenario_id': scenario_id,
                'scenario_name': scenario_name,
                'priority': scenario['priority'],
                'target_metric': scenario['target_metric'],
                'test_status': test_status,
                
                # Groupe Contrôle
                'control_users': control_users,
                'control_views': control_views,
                'control_carts': control_carts,
                'control_purchases': control_purchases,
                'control_revenue': round(control_revenue, 2),
                'control_view_to_cart_pct': round(control_view_to_cart, 2),
                'control_cart_to_purchase_pct': round(control_cart_to_purchase, 2),
                'control_view_to_purchase_pct': round(control_view_to_purchase, 2),
                
                # Groupe Variant
                'variant_users': variant_users,
                'variant_views': variant_views,
                'variant_carts': variant_carts,
                'variant_purchases': variant_purchases,
                'variant_revenue': round(variant_revenue, 2),
                'variant_view_to_cart_pct': round(variant_view_to_cart, 2),
                'variant_cart_to_purchase_pct': round(variant_cart_to_purchase, 2),
                'variant_view_to_purchase_pct': round(variant_view_to_purchase, 2),
                
                # Lifts
                'lift_view_to_cart_pct': round(lift_view_to_cart, 2),
                'lift_cart_to_purchase_pct': round(lift_cart_to_purchase, 2),
                'lift_view_to_purchase_pct': round(lift_view_to_purchase, 2),
                'revenue_lift': round(revenue_lift, 2),
                'revenue_lift_pct': round(revenue_lift_pct, 2),
                
                # Statistiques
                'p_value': round(p_value, 4),
                'is_significant': is_significant,
                'confidence_level': round(confidence, 1),
                'z_score': round(z_score, 2),
                'sample_size_control': control_users,
                'sample_size_variant': variant_users,
                'sample_size_total': control_users + variant_users,
                
                # Métriques cumulées
                'cumulative_revenue_lift': round(revenue_lift * (day + 1), 2),
                'days_running': day + 1,
                
                # Informations scénario
                'expected_lift_pct': round(scenario['expected_lift'] * 100, 2),
                'implementation_cost': scenario['implementation_cost'],
                'implementation_weeks': scenario['implementation_weeks']
            }
            
            all_simulations.append(simulation_row)
    
    return pd.DataFrame(all_simulations)

def main():
    """Génération du fichier ab_test_simulation.csv"""
    print_separator("GÉNÉRATION AB_TEST_SIMULATION.CSV - ISSUE #15")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    print_separator("CHARGEMENT DES DONNÉES")
    
    # Charger les données de simulation existantes
    print("1. Chargement de ab_test_simulation_summary.json...")
    with open(data_dir / 'ab_test_simulation_summary.json', 'r', encoding='utf-8') as f:
        simulation_data = json.load(f)
    print(f"   ✅ {len(simulation_data['scenarios'])} scénarios chargés")
    
    print("\n2. Chargement de funnel_daily_detailed.csv...")
    funnel_daily = pd.read_csv(data_dir / 'funnel_daily_detailed.csv')
    print(f"   ✅ {len(funnel_daily)} jours de données baseline")
    
    print("\n3. Extraction des métadonnées...")
    scenarios = simulation_data['scenarios']
    simulation_results = simulation_data['simulation_results']
    baseline_metrics = simulation_data['baseline_metrics']
    
    print(f"   ✅ Baseline view→cart: {baseline_metrics['view_to_cart_pct']}%")
    print(f"   ✅ Baseline cart→purchase: {baseline_metrics['cart_to_purchase_pct']}%")
    
    print_separator("GÉNÉRATION SIMULATION QUOTIDIENNE")
    
    # Générer 30 jours de simulation pour chaque scénario
    print("Génération de 30 jours de simulation pour 8 scénarios...")
    print("(240 lignes de données détaillées)\n")
    
    simulation_df = generate_ab_test_daily_simulation(
        baseline_data=funnel_daily,
        scenarios=scenarios,
        simulation_results=simulation_results,
        days=30
    )
    
    print(f"✅ Simulation générée: {len(simulation_df)} lignes")
    print(f"   • 8 scénarios × 30 jours")
    print(f"   • Contrôle vs Variant quotidien")
    print(f"   • Lifts et significativité statistique")
    
    print_separator("STATISTIQUES DE LA SIMULATION")
    
    # Statistiques par scénario
    print("\nRésumé par scénario (30 jours):\n")
    
    for scenario_id in simulation_df['scenario_id'].unique():
        scenario_data = simulation_df[simulation_df['scenario_id'] == scenario_id]
        scenario_name = scenario_data['scenario_name'].iloc[0]
        
        # Métriques finales (jour 30)
        final_day = scenario_data[scenario_data['day_number'] == 30].iloc[0]
        
        # Moyennes sur la période
        avg_lift = scenario_data['lift_view_to_cart_pct'].mean()
        avg_revenue_lift = scenario_data['revenue_lift'].mean()
        total_revenue_lift = scenario_data['cumulative_revenue_lift'].iloc[-1]
        
        # Significativité
        significant_days = scenario_data['is_significant'].sum()
        
        print(f"{scenario_id} - {scenario_name}:")
        print(f"   Lift moyen: {avg_lift:+.1f}%")
        print(f"   Revenue lift/jour: €{avg_revenue_lift:,.0f}")
        print(f"   Revenue lift cumulé (30j): €{total_revenue_lift:,.0f}")
        print(f"   Jours significatifs: {significant_days}/30")
        print(f"   Statut final: {final_day['test_status']}")
        print()
    
    print_separator("EXPORT DES RÉSULTATS")
    
    # Export CSV principal
    print("1. Export de ab_test_simulation.csv...")
    output_file = output_dir / 'ab_test_simulation.csv'
    simulation_df.to_csv(output_file, index=False)
    print(f"   ✅ {output_file.name}")
    print(f"   • {len(simulation_df)} lignes")
    print(f"   • {len(simulation_df.columns)} colonnes")
    print(f"   • {output_file.stat().st_size / 1024:.1f} KB")
    
    # Export résumé par scénario
    print("\n2. Export de ab_test_summary_by_scenario.csv...")
    
    summary_by_scenario = simulation_df.groupby(['scenario_id', 'scenario_name', 'priority']).agg({
        'lift_view_to_cart_pct': 'mean',
        'lift_cart_to_purchase_pct': 'mean',
        'lift_view_to_purchase_pct': 'mean',
        'revenue_lift': 'sum',
        'control_purchases': 'sum',
        'variant_purchases': 'sum',
        'is_significant': 'sum',
        'confidence_level': 'max',
        'implementation_cost': 'first',
        'expected_lift_pct': 'first'
    }).reset_index()
    
    summary_by_scenario.columns = [
        'scenario_id', 'scenario_name', 'priority',
        'avg_lift_view_to_cart_pct', 'avg_lift_cart_to_purchase_pct', 
        'avg_lift_view_to_purchase_pct', 'total_revenue_lift_30d',
        'total_control_purchases', 'total_variant_purchases',
        'days_significant', 'max_confidence_level',
        'implementation_cost', 'expected_lift_pct'
    ]
    
    # Calcul du ROI sur 30 jours
    summary_by_scenario['roi_30d_pct'] = (
        (summary_by_scenario['total_revenue_lift_30d'] - summary_by_scenario['implementation_cost']) 
        / summary_by_scenario['implementation_cost'] * 100
    ).round(2)
    
    # Annualisé
    summary_by_scenario['annual_revenue_lift'] = (summary_by_scenario['total_revenue_lift_30d'] * 12.17).round(2)
    summary_by_scenario['annual_roi_pct'] = (
        (summary_by_scenario['annual_revenue_lift'] - summary_by_scenario['implementation_cost'])
        / summary_by_scenario['implementation_cost'] * 100
    ).round(2)
    
    output_file = output_dir / 'ab_test_summary_by_scenario.csv'
    summary_by_scenario.to_csv(output_file, index=False)
    print(f"   ✅ {output_file.name} ({len(summary_by_scenario)} scénarios)")
    
    # Export données quotidiennes agrégées
    print("\n3. Export de ab_test_daily_aggregate.csv...")
    
    daily_aggregate = simulation_df.groupby('day_number').agg({
        'control_purchases': 'sum',
        'variant_purchases': 'sum',
        'control_revenue': 'sum',
        'variant_revenue': 'sum',
        'revenue_lift': 'sum',
        'sample_size_total': 'sum',
        'is_significant': 'sum'
    }).reset_index()
    
    daily_aggregate['total_lift_pct'] = (
        (daily_aggregate['variant_revenue'] - daily_aggregate['control_revenue'])
        / daily_aggregate['control_revenue'] * 100
    ).round(2)
    
    output_file = output_dir / 'ab_test_daily_aggregate.csv'
    daily_aggregate.to_csv(output_file, index=False)
    print(f"   ✅ {output_file.name} ({len(daily_aggregate)} jours)")
    
    # Durée d'exécution
    duration = (datetime.now() - start_time).total_seconds()
    
    print_separator("GÉNÉRATION TERMINÉE")
    print(f"✅ Fichiers générés avec succès")
    print(f"📊 3 fichiers créés dans {output_dir}")
    print(f"⏱️  Durée: {duration:.2f}s")
    print(f"\n📁 FICHIERS:")
    print(f"   1. ab_test_simulation.csv - {len(simulation_df)} lignes (simulation complète)")
    print(f"   2. ab_test_summary_by_scenario.csv - {len(summary_by_scenario)} scénarios (résumé)")
    print(f"   3. ab_test_daily_aggregate.csv - {len(daily_aggregate)} jours (agrégat quotidien)")
    print(f"\n🎯 PRÊT POUR VISUALISATION:")
    print(f"   • Dashboard Power BI / Tableau")
    print(f"   • Graphiques de tendances")
    print(f"   • Comparaison contrôle vs variant")
    print(f"   • Analyse de significativité")
    print_separator()

if __name__ == '__main__':
    main()
