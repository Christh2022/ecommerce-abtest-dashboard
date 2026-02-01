#!/usr/bin/env python3
"""
Script de simulation A/B Testing - Issue #14
Simule différents scénarios d'optimisation basés sur les analyses précédentes.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #14 - Créer simulation A/B
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from scipy import stats

def print_separator(title=""):
    """Affiche un séparateur formaté"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.80):
    """
    Calcule la taille d'échantillon nécessaire pour un test A/B
    
    Args:
        baseline_rate: Taux de conversion actuel (proportion)
        mde: Minimum Detectable Effect (amélioration minimale à détecter)
        alpha: Niveau de signification (défaut 0.05)
        power: Puissance statistique (défaut 0.80)
    
    Returns:
        Taille d'échantillon par groupe
    """
    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    # Variance poolée
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    p_pooled = (p1 + p2) / 2
    
    # Formule de taille d'échantillon
    n = (2 * p_pooled * (1 - p_pooled) * (z_alpha + z_beta)**2) / (p1 - p2)**2
    
    return int(np.ceil(n))

def simulate_ab_test(baseline_conversion, variant_conversion, sample_size, simulations=10000):
    """
    Simule un test A/B avec Monte Carlo
    
    Args:
        baseline_conversion: Taux de conversion du groupe contrôle
        variant_conversion: Taux de conversion du groupe variant
        sample_size: Nombre d'utilisateurs par groupe
        simulations: Nombre de simulations Monte Carlo
    
    Returns:
        Dict avec résultats de simulation
    """
    # Simulation Monte Carlo
    control_conversions = np.random.binomial(sample_size, baseline_conversion, simulations)
    variant_conversions = np.random.binomial(sample_size, variant_conversion, simulations)
    
    # Calcul des taux de conversion simulés
    control_rates = control_conversions / sample_size
    variant_rates = variant_conversions / sample_size
    
    # Test de significativité pour chaque simulation
    p_values = []
    for i in range(simulations):
        # Chi-square test
        contingency_table = [
            [control_conversions[i], sample_size - control_conversions[i]],
            [variant_conversions[i], sample_size - variant_conversions[i]]
        ]
        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
        p_values.append(p_value)
    
    p_values = np.array(p_values)
    
    # Calcul de la puissance statistique (proportion de tests significatifs)
    power = np.mean(p_values < 0.05)
    
    # Lift moyen
    avg_lift = np.mean((variant_rates - control_rates) / control_rates * 100)
    
    return {
        'baseline_rate': baseline_conversion,
        'variant_rate': variant_conversion,
        'sample_size_per_group': sample_size,
        'simulations': simulations,
        'statistical_power': power,
        'avg_lift_pct': avg_lift,
        'control_rate_mean': np.mean(control_rates),
        'control_rate_std': np.std(control_rates),
        'variant_rate_mean': np.mean(variant_rates),
        'variant_rate_std': np.std(variant_rates),
        'significant_tests_pct': power * 100
    }

def main():
    """Simulation A/B Testing basée sur les analyses précédentes"""
    print_separator("SIMULATION A/B TESTING - ISSUE #14")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    print_separator("CHARGEMENT DES DONNÉES BASELINE")
    
    # Charger les métriques actuelles
    print("Chargement de funnel_analysis_summary.json...")
    with open(data_dir / 'funnel_analysis_summary.json', 'r', encoding='utf-8') as f:
        funnel_data = json.load(f)
    
    print("Chargement de conversion_analysis_summary.json...")
    with open(data_dir / 'conversion_analysis_summary.json', 'r', encoding='utf-8') as f:
        conversion_data = json.load(f)
    
    print("Chargement de daily_metrics.csv...")
    daily_metrics = pd.read_csv(data_dir / 'daily_metrics.csv')
    
    # Métriques baseline
    baseline_view_to_cart = funnel_data['conversion_rates']['view_to_cart'] / 100
    baseline_cart_to_purchase = funnel_data['conversion_rates']['cart_to_purchase'] / 100
    baseline_view_to_purchase = funnel_data['conversion_rates']['view_to_purchase'] / 100
    
    total_users = daily_metrics['unique_users'].sum()
    total_transactions = daily_metrics['transactions'].sum()
    avg_order_value = daily_metrics['avg_order_value'].mean()
    
    print(f"\n Données chargées")
    print(f"   Total utilisateurs: {total_users:,}")
    print(f"   Total transactions: {total_transactions:,}")
    print(f"   AOV moyen: €{avg_order_value:.2f}")
    print(f"   Baseline view→cart: {baseline_view_to_cart*100:.2f}%")
    print(f"   Baseline cart→purchase: {baseline_cart_to_purchase*100:.2f}%")
    
    print_separator("DÉFINITION DES SCÉNARIOS A/B")
    
    # Définir les scénarios d'optimisation basés sur Issue #13
    scenarios = []
    
    # Scénario 1: Amélioration photos produits (impact view→cart)
    scenarios.append({
        'id': 'S1',
        'name': 'Amélioration Photos Produits',
        'description': 'Photos HD, multi-angles, zoom, vidéos produits',
        'target_metric': 'view_to_cart',
        'baseline': baseline_view_to_cart,
        'expected_lift': 0.30,  # +30%
        'variant': baseline_view_to_cart * 1.30,
        'implementation_cost': 30000,
        'implementation_weeks': 4,
        'affected_products_pct': 100,
        'priority': 'HIGH'
    })
    
    # Scénario 2: Système de reviews clients (impact view→cart + cart→purchase)
    scenarios.append({
        'id': 'S2',
        'name': 'Système Reviews Clients',
        'description': 'Avis vérifiés, ratings, photos clients, Q&A',
        'target_metric': 'view_to_cart',
        'baseline': baseline_view_to_cart,
        'expected_lift': 0.40,  # +40%
        'variant': baseline_view_to_cart * 1.40,
        'implementation_cost': 15000,
        'implementation_weeks': 3,
        'affected_products_pct': 100,
        'priority': 'HIGH'
    })
    
    # Scénario 3: Simplification checkout (impact cart→purchase)
    scenarios.append({
        'id': 'S3',
        'name': 'Checkout Simplifié',
        'description': 'Réduction 5→3 étapes, auto-fill, guest checkout',
        'target_metric': 'cart_to_purchase',
        'baseline': baseline_cart_to_purchase,
        'expected_lift': 0.25,  # +25%
        'variant': baseline_cart_to_purchase * 1.25,
        'implementation_cost': 25000,
        'implementation_weeks': 6,
        'affected_products_pct': 100,
        'priority': 'MEDIUM'
    })
    
    # Scénario 4: Optimisation prix (impact view→cart + cart→purchase)
    scenarios.append({
        'id': 'S4',
        'name': 'Optimisation Prix Compétitifs',
        'description': 'Price matching, promotions dynamiques, bundling',
        'target_metric': 'view_to_cart',
        'baseline': baseline_view_to_cart,
        'expected_lift': 0.50,  # +50%
        'variant': baseline_view_to_cart * 1.50,
        'implementation_cost': 20000,
        'implementation_weeks': 8,
        'affected_products_pct': 80,
        'priority': 'HIGH'
    })
    
    # Scénario 5: Options paiement (impact cart→purchase)
    scenarios.append({
        'id': 'S5',
        'name': 'Options Paiement Multiples',
        'description': 'PayPal, Apple Pay, Google Pay, Buy Now Pay Later',
        'target_metric': 'cart_to_purchase',
        'baseline': baseline_cart_to_purchase,
        'expected_lift': 0.15,  # +15%
        'variant': baseline_cart_to_purchase * 1.15,
        'implementation_cost': 10000,
        'implementation_weeks': 2,
        'affected_products_pct': 100,
        'priority': 'MEDIUM'
    })
    
    # Scénario 6: Optimisation weekend (impact global)
    scenarios.append({
        'id': 'S6',
        'name': 'Optimisation Weekend',
        'description': 'Promotions weekend, support dédié, UX mobile',
        'target_metric': 'view_to_purchase',
        'baseline': baseline_view_to_purchase,
        'expected_lift': 0.40,  # +40%
        'variant': baseline_view_to_purchase * 1.40,
        'implementation_cost': 18000,
        'implementation_weeks': 3,
        'affected_products_pct': 100,
        'priority': 'HIGH'
    })
    
    # Scénario 7: Programme de fidélité (impact récurrence)
    scenarios.append({
        'id': 'S7',
        'name': 'Programme Fidélité',
        'description': 'Points, rewards, VIP tiers, early access',
        'target_metric': 'cart_to_purchase',
        'baseline': baseline_cart_to_purchase,
        'expected_lift': 0.20,  # +20%
        'variant': baseline_cart_to_purchase * 1.20,
        'implementation_cost': 25000,
        'implementation_weeks': 12,
        'affected_products_pct': 100,
        'priority': 'MEDIUM'
    })
    
    # Scénario 8: Nettoyage catalogue (impact indirect via focus)
    scenarios.append({
        'id': 'S8',
        'name': 'Nettoyage Catalogue',
        'description': 'Retrait 211K produits morts, focus top 10%',
        'target_metric': 'view_to_cart',
        'baseline': baseline_view_to_cart,
        'expected_lift': 0.35,  # +35%
        'variant': baseline_view_to_cart * 1.35,
        'implementation_cost': 5000,
        'implementation_weeks': 2,
        'affected_products_pct': 10,
        'priority': 'CRITICAL'
    })
    
    print(f" {len(scenarios)} scénarios définis\n")
    for s in scenarios:
        print(f"   {s['id']}: {s['name']} (Priorité: {s['priority']})")
    
    print_separator("CALCUL DES TAILLES D'ÉCHANTILLON")
    
    # Paramètres de test
    alpha = 0.05  # Niveau de signification (5%)
    power = 0.80  # Puissance statistique (80%)
    mde = 0.10    # Minimum Detectable Effect (10%)
    
    # Calculer pour chaque scénario
    for scenario in scenarios:
        baseline = scenario['baseline']
        expected_improvement = scenario['expected_lift']
        
        # Taille d'échantillon nécessaire
        sample_size = calculate_sample_size(baseline, expected_improvement, alpha, power)
        
        # Durée estimée du test (basé sur le trafic quotidien moyen)
        avg_daily_users = daily_metrics['unique_users'].mean()
        days_needed = int(np.ceil(sample_size * 2 / avg_daily_users))  # *2 car contrôle + variant
        weeks_needed = int(np.ceil(days_needed / 7))
        
        scenario['sample_size_per_group'] = sample_size
        scenario['total_sample_size'] = sample_size * 2
        scenario['test_duration_days'] = days_needed
        scenario['test_duration_weeks'] = weeks_needed
        
        print(f"\n{scenario['id']} - {scenario['name']}:")
        print(f"   Baseline: {baseline*100:.2f}%")
        print(f"   Variant attendu: {scenario['variant']*100:.2f}% (+{expected_improvement*100:.0f}%)")
        print(f"   Échantillon/groupe: {sample_size:,} utilisateurs")
        print(f"   Durée test: {weeks_needed} semaines ({days_needed} jours)")
    
    print_separator("SIMULATION MONTE CARLO (10,000 SIMULATIONS)")
    
    simulation_results = []
    
    for scenario in scenarios:
        print(f"\nSimulation {scenario['id']} - {scenario['name']}...")
        
        # Simulation
        sim_result = simulate_ab_test(
            baseline_conversion=scenario['baseline'],
            variant_conversion=scenario['variant'],
            sample_size=scenario['sample_size_per_group'],
            simulations=10000
        )
        
        # Ajouter les infos du scénario
        sim_result.update({
            'scenario_id': scenario['id'],
            'scenario_name': scenario['name'],
            'target_metric': scenario['target_metric'],
            'expected_lift_pct': scenario['expected_lift'] * 100,
            'test_duration_weeks': scenario['test_duration_weeks'],
            'implementation_cost': scenario['implementation_cost'],
            'priority': scenario['priority']
        })
        
        simulation_results.append(sim_result)
        
        print(f"    Puissance statistique: {sim_result['statistical_power']*100:.1f}%")
        print(f"    Tests significatifs: {sim_result['significant_tests_pct']:.1f}%")
        print(f"    Lift moyen simulé: +{sim_result['avg_lift_pct']:.1f}%")
    
    print_separator("ESTIMATION IMPACT BUSINESS")
    
    business_impact = []
    
    for scenario in scenarios:
        sim_result = next(r for r in simulation_results if r['scenario_id'] == scenario['id'])
        
        # Calcul de l'impact
        metric = scenario['target_metric']
        
        if metric == 'view_to_cart':
            # Impact sur les ajouts au panier
            current_carts = daily_metrics['add_to_carts'].sum()
            current_views = daily_metrics['views'].sum()
            
            new_carts = current_views * scenario['variant']
            additional_carts = new_carts - current_carts
            
            # Conversion panier→achat reste constante
            additional_purchases = additional_carts * baseline_cart_to_purchase
            additional_revenue = additional_purchases * avg_order_value
            
        elif metric == 'cart_to_purchase':
            # Impact sur les achats depuis panier
            current_carts = daily_metrics['add_to_carts'].sum()
            current_purchases = daily_metrics['transactions'].sum()
            
            new_purchases = current_carts * scenario['variant']
            additional_purchases = new_purchases - current_purchases
            additional_revenue = additional_purchases * avg_order_value
            
        elif metric == 'view_to_purchase':
            # Impact direct sur conversion globale
            current_views = daily_metrics['views'].sum()
            current_purchases = daily_metrics['transactions'].sum()
            
            new_purchases = current_views * scenario['variant']
            additional_purchases = new_purchases - current_purchases
            additional_revenue = additional_purchases * avg_order_value
        
        # ROI
        roi = ((additional_revenue - scenario['implementation_cost']) / scenario['implementation_cost']) * 100
        
        # Annualisé (extrapolation sur 12 mois)
        days_in_data = len(daily_metrics)
        annual_multiplier = 365 / days_in_data
        annual_additional_revenue = additional_revenue * annual_multiplier
        annual_roi = ((annual_additional_revenue - scenario['implementation_cost']) / scenario['implementation_cost']) * 100
        
        impact = {
            'scenario_id': scenario['id'],
            'scenario_name': scenario['name'],
            'priority': scenario['priority'],
            'implementation_cost': scenario['implementation_cost'],
            'implementation_weeks': scenario['implementation_weeks'],
            'test_duration_weeks': scenario['test_duration_weeks'],
            'additional_purchases_period': int(additional_purchases),
            'additional_revenue_period': round(additional_revenue, 2),
            'roi_period': round(roi, 2),
            'annual_additional_revenue': round(annual_additional_revenue, 2),
            'annual_roi': round(annual_roi, 2),
            'payback_weeks': round((scenario['implementation_cost'] / (additional_revenue / days_in_data * 7)), 1) if additional_revenue > 0 else float('inf'),
            'confidence_level': sim_result['statistical_power']
        }
        
        business_impact.append(impact)
        
        print(f"\n{scenario['id']} - {scenario['name']}:")
        print(f"   Investissement: €{scenario['implementation_cost']:,}")
        print(f"   Achats additionnels (période): +{int(additional_purchases):,}")
        print(f"   Revenue additionnel (période): +€{additional_revenue:,.0f}")
        print(f"   ROI (période): {roi:+.0f}%")
        print(f"   Revenue annuel projeté: €{annual_additional_revenue:,.0f}")
        print(f"   ROI annuel: {annual_roi:+.0f}%")
        print(f"   Payback: {impact['payback_weeks']:.1f} semaines")
    
    print_separator("ROADMAP RECOMMANDÉE")
    
    # Trier par priorité et ROI
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    business_impact_sorted = sorted(
        business_impact,
        key=lambda x: (priority_order.get(x['priority'], 4), -x['annual_roi'])
    )
    
    print("\nOrdre d'exécution recommandé:\n")
    
    cumulative_cost = 0
    cumulative_revenue = 0
    cumulative_weeks = 0
    
    for rank, impact in enumerate(business_impact_sorted, 1):
        cumulative_cost += impact['implementation_cost']
        cumulative_revenue += impact['annual_additional_revenue']
        cumulative_weeks = max(cumulative_weeks, impact['implementation_weeks'] + impact['test_duration_weeks'])
        
        print(f"{rank}. {impact['scenario_id']} - {impact['scenario_name']}")
        print(f"   Priorité: {impact['priority']}")
        print(f"   Durée totale: {impact['implementation_weeks']}w implémentation + {impact['test_duration_weeks']}w test")
        print(f"   Investissement: €{impact['implementation_cost']:,}")
        print(f"   Revenue annuel: €{impact['annual_additional_revenue']:,.0f}")
        print(f"   ROI annuel: {impact['annual_roi']:+.0f}%")
        print(f"   Confiance: {impact['confidence_level']*100:.0f}%")
        print()
    
    print(f"TOTAL PROGRAMME:")
    print(f"   Investissement total: €{cumulative_cost:,}")
    print(f"   Revenue annuel total: €{cumulative_revenue:,.0f}")
    print(f"   ROI portfolio: {((cumulative_revenue - cumulative_cost) / cumulative_cost * 100):+.0f}%")
    
    print_separator("EXPORT DES RÉSULTATS")
    
    # Export 1: Résumé JSON
    print("1. Export du résumé de simulation...")
    
    summary = {
        'metadata': {
            'simulation_date': datetime.now().isoformat(),
            'baseline_period_days': len(daily_metrics),
            'total_users': int(total_users),
            'total_transactions': int(total_transactions),
            'avg_order_value': round(avg_order_value, 2)
        },
        'baseline_metrics': {
            'view_to_cart_pct': round(baseline_view_to_cart * 100, 2),
            'cart_to_purchase_pct': round(baseline_cart_to_purchase * 100, 2),
            'view_to_purchase_pct': round(baseline_view_to_purchase * 100, 2)
        },
        'test_parameters': {
            'alpha': alpha,
            'power': power,
            'mde': mde,
            'simulations_per_scenario': 10000
        },
        'scenarios': scenarios,
        'simulation_results': simulation_results,
        'business_impact': business_impact,
        'recommended_roadmap': business_impact_sorted,
        'portfolio_summary': {
            'total_investment': cumulative_cost,
            'total_annual_revenue': round(cumulative_revenue, 2),
            'portfolio_roi': round((cumulative_revenue - cumulative_cost) / cumulative_cost * 100, 2)
        }
    }
    
    output_file = output_dir / 'ab_test_simulation_summary.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"   [OK] {output_file.name} ({output_file.stat().st_size / 1024:.1f} KB)")
    
    # Export 2: Scenarios CSV
    print("\n2. Export des scénarios...")
    scenarios_df = pd.DataFrame(scenarios)
    output_file = output_dir / 'ab_test_scenarios.csv'
    scenarios_df.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(scenarios_df)} scénarios)")
    
    # Export 3: Simulation results CSV
    print("\n3. Export des résultats de simulation...")
    sim_results_df = pd.DataFrame(simulation_results)
    output_file = output_dir / 'ab_test_simulation_results.csv'
    sim_results_df.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(sim_results_df)} simulations)")
    
    # Export 4: Business impact CSV
    print("\n4. Export de l'impact business...")
    impact_df = pd.DataFrame(business_impact)
    output_file = output_dir / 'ab_test_business_impact.csv'
    impact_df.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(impact_df)} scénarios)")
    
    # Export 5: Roadmap recommandée
    print("\n5. Export de la roadmap...")
    roadmap_df = pd.DataFrame(business_impact_sorted)
    roadmap_df['rank'] = range(1, len(roadmap_df) + 1)
    roadmap_df['cumulative_cost'] = roadmap_df['implementation_cost'].cumsum()
    roadmap_df['cumulative_revenue'] = roadmap_df['annual_additional_revenue'].cumsum()
    roadmap_df['cumulative_roi'] = ((roadmap_df['cumulative_revenue'] - roadmap_df['cumulative_cost']) / roadmap_df['cumulative_cost'] * 100).round(2)
    
    output_file = output_dir / 'ab_test_roadmap.csv'
    roadmap_df.to_csv(output_file, index=False)
    print(f"   [OK] {output_file.name} ({len(roadmap_df)} scénarios)")
    
    # Durée d'exécution
    duration = (datetime.now() - start_time).total_seconds()
    
    print_separator("SIMULATION TERMINÉE")
    print(f" Simulation A/B terminée avec succès")
    print(f" 5 fichiers générés dans {output_dir}")
    print(f"⏱️  Durée: {duration:.2f}s")
    print(f"\n RECOMMANDATIONS:")
    print(f"   1. Commencer par {business_impact_sorted[0]['scenario_name']} (priorité {business_impact_sorted[0]['priority']})")
    print(f"   2. ROI portfolio: {summary['portfolio_summary']['portfolio_roi']:+.0f}%")
    print(f"   3. Revenue annuel potentiel: €{cumulative_revenue:,.0f}")
    print(f"   4. Investissement total: €{cumulative_cost:,}")
    print_separator()

if __name__ == '__main__':
    main()
