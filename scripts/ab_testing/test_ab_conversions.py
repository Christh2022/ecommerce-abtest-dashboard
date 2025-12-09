#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Issue #16 - Test des Conversions A vs B

Ce script effectue des tests statistiques rigoureux pour comparer les conversions
entre les groupes contrôle (A) et variant (B) pour chaque scénario A/B testing.

Tests implémentés:
- Chi-square test pour proportions (conversion rates)
- Z-test pour différence de proportions
- Intervalle de confiance à 95%
- Calcul de la puissance statistique (statistical power)
- Analyse de taille d'échantillon minimale
- Test de Fisher (pour petits échantillons)
- Bayesian A/B test (probabilité que B > A)

Auteur: Data Science Team
Date: 2025-12-09
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, norm, beta
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ABConversionTester:
    """Classe pour tester les conversions A vs B avec méthodes statistiques multiples"""
    
    def __init__(self, alpha=0.05, power=0.80):
        """
        Initialisation du testeur
        
        Args:
            alpha: Niveau de significativité (défaut: 0.05 = 95% confiance)
            power: Puissance statistique désirée (défaut: 0.80 = 80%)
        """
        self.alpha = alpha
        self.power = power
        self.z_alpha = norm.ppf(1 - alpha/2)  # Z-score pour IC 95%
        self.z_beta = norm.ppf(power)  # Z-score pour puissance
        
    def chi_square_test(self, control_conversions, control_total, 
                        variant_conversions, variant_total):
        """
        Test du Chi-carré pour comparer deux proportions
        
        Args:
            control_conversions: Nombre de conversions groupe A
            control_total: Taille échantillon groupe A
            variant_conversions: Nombre de conversions groupe B
            variant_total: Taille échantillon groupe B
            
        Returns:
            dict: Résultats du test (chi2, p-value, dof, expected)
        """
        # Table de contingence
        observed = np.array([
            [control_conversions, control_total - control_conversions],
            [variant_conversions, variant_total - variant_conversions]
        ])
        
        # Test chi-carré
        chi2, p_value, dof, expected = chi2_contingency(observed)
        
        return {
            'test_name': 'Chi-Square Test',
            'chi2_statistic': float(chi2),
            'p_value': float(p_value),
            'degrees_of_freedom': int(dof),
            'is_significant': p_value < self.alpha,
            'expected_frequencies': expected.tolist()
        }
    
    def z_test_proportions(self, control_conversions, control_total,
                           variant_conversions, variant_total):
        """
        Z-test pour différence de proportions (test bilatéral)
        
        Args:
            control_conversions: Nombre de conversions groupe A
            control_total: Taille échantillon groupe A
            variant_conversions: Nombre de conversions groupe B
            variant_total: Taille échantillon groupe B
            
        Returns:
            dict: Résultats du z-test (z-score, p-value, CI)
        """
        # Proportions
        p_control = control_conversions / control_total
        p_variant = variant_conversions / variant_total
        
        # Proportion poolée
        p_pooled = (control_conversions + variant_conversions) / (control_total + variant_total)
        
        # Erreur standard poolée
        se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_total + 1/variant_total))
        
        # Z-score
        z_score = (p_variant - p_control) / se_pooled if se_pooled > 0 else 0
        
        # P-value (test bilatéral)
        p_value = 2 * (1 - norm.cdf(abs(z_score)))
        
        # Intervalle de confiance à 95% pour la différence
        diff = p_variant - p_control
        se_diff = np.sqrt(p_control*(1-p_control)/control_total + 
                         p_variant*(1-p_variant)/variant_total)
        ci_lower = diff - self.z_alpha * se_diff
        ci_upper = diff + self.z_alpha * se_diff
        
        return {
            'test_name': 'Z-Test for Proportions',
            'z_score': float(z_score),
            'p_value': float(p_value),
            'is_significant': p_value < self.alpha,
            'control_rate': float(p_control),
            'variant_rate': float(p_variant),
            'difference': float(diff),
            'difference_pct': float(diff * 100),
            'confidence_interval_95': {
                'lower': float(ci_lower),
                'upper': float(ci_upper),
                'lower_pct': float(ci_lower * 100),
                'upper_pct': float(ci_upper * 100)
            },
            'standard_error': float(se_diff)
        }
    
    def fisher_exact_test(self, control_conversions, control_total,
                          variant_conversions, variant_total):
        """
        Test exact de Fisher (pour petits échantillons)
        
        Args:
            control_conversions: Nombre de conversions groupe A
            control_total: Taille échantillon groupe A
            variant_conversions: Nombre de conversions groupe B
            variant_total: Taille échantillon groupe B
            
        Returns:
            dict: Résultats du test de Fisher
        """
        # Table 2x2
        table = [
            [control_conversions, control_total - control_conversions],
            [variant_conversions, variant_total - variant_conversions]
        ]
        
        # Test de Fisher
        odds_ratio, p_value = stats.fisher_exact(table)
        
        return {
            'test_name': 'Fisher Exact Test',
            'odds_ratio': float(odds_ratio),
            'p_value': float(p_value),
            'is_significant': p_value < self.alpha
        }
    
    def bayesian_ab_test(self, control_conversions, control_total,
                         variant_conversions, variant_total, n_samples=100000):
        """
        Test bayésien A/B - calcule P(B > A)
        
        Utilise distribution Beta comme prior/posterior pour les taux de conversion
        
        Args:
            control_conversions: Nombre de conversions groupe A
            control_total: Taille échantillon groupe A
            variant_conversions: Nombre de conversions groupe B
            variant_total: Taille échantillon groupe B
            n_samples: Nombre d'échantillons Monte Carlo
            
        Returns:
            dict: Résultats bayésiens (prob B > A, expected loss)
        """
        # Prior non informatif: Beta(1, 1) = Uniform(0, 1)
        # Posterior: Beta(alpha + conversions, beta + non-conversions)
        
        alpha_control = 1 + control_conversions
        beta_control = 1 + (control_total - control_conversions)
        
        alpha_variant = 1 + variant_conversions
        beta_variant = 1 + (variant_total - variant_conversions)
        
        # Échantillonnage des posteriors
        samples_control = np.random.beta(alpha_control, beta_control, n_samples)
        samples_variant = np.random.beta(alpha_variant, beta_variant, n_samples)
        
        # P(B > A)
        prob_b_beats_a = np.mean(samples_variant > samples_control)
        
        # Expected loss si on choisit B (mais A est mieux)
        loss_if_choose_b = np.mean(np.maximum(samples_control - samples_variant, 0))
        
        # Expected loss si on choisit A (mais B est mieux)
        loss_if_choose_a = np.mean(np.maximum(samples_variant - samples_control, 0))
        
        # Lift relatif moyen
        relative_lift = np.mean((samples_variant - samples_control) / samples_control)
        
        return {
            'test_name': 'Bayesian A/B Test',
            'prob_b_beats_a': float(prob_b_beats_a),
            'prob_a_beats_b': float(1 - prob_b_beats_a),
            'expected_loss_choose_b': float(loss_if_choose_b),
            'expected_loss_choose_a': float(loss_if_choose_a),
            'relative_lift_mean': float(relative_lift),
            'relative_lift_pct': float(relative_lift * 100),
            'credible_interval_95': {
                'lower': float(np.percentile(samples_variant - samples_control, 2.5)),
                'upper': float(np.percentile(samples_variant - samples_control, 97.5)),
                'lower_pct': float(np.percentile((samples_variant - samples_control)/samples_control * 100, 2.5)),
                'upper_pct': float(np.percentile((samples_variant - samples_control)/samples_control * 100, 97.5))
            },
            'is_significant': prob_b_beats_a > 0.95 or prob_b_beats_a < 0.05
        }
    
    def calculate_statistical_power(self, control_rate, variant_rate, sample_size):
        """
        Calcule la puissance statistique pour un test donné
        
        Args:
            control_rate: Taux de conversion groupe A
            variant_rate: Taux de conversion groupe B
            sample_size: Taille d'échantillon par groupe
            
        Returns:
            float: Puissance statistique (0-1)
        """
        # Effet (différence de proportions)
        effect = variant_rate - control_rate
        
        # Erreur standard sous H1 (alternative hypothesis)
        se_h1 = np.sqrt(control_rate*(1-control_rate)/sample_size + 
                       variant_rate*(1-variant_rate)/sample_size)
        
        # Erreur standard sous H0 (null hypothesis, proportions égales)
        p_pooled = (control_rate + variant_rate) / 2
        se_h0 = np.sqrt(2 * p_pooled * (1 - p_pooled) / sample_size)
        
        # Z-score critique pour alpha
        z_critical = self.z_alpha
        
        # Z-score sous H1
        z_h1 = (abs(effect) - z_critical * se_h0) / se_h1 if se_h1 > 0 else 0
        
        # Puissance = P(rejeter H0 | H1 vraie)
        power = norm.cdf(z_h1)
        
        return float(power)
    
    def minimum_sample_size(self, control_rate, mde, power=None):
        """
        Calcule la taille minimale d'échantillon pour détecter un MDE donné
        
        Args:
            control_rate: Taux de conversion groupe A
            mde: Minimum Detectable Effect (différence absolue)
            power: Puissance désirée (défaut: self.power)
            
        Returns:
            int: Taille minimale d'échantillon par groupe
        """
        if power is None:
            power = self.power
        
        z_beta = norm.ppf(power)
        variant_rate = control_rate + mde
        
        # Formule classique
        numerator = (self.z_alpha * np.sqrt(2 * control_rate * (1 - control_rate)) + 
                    z_beta * np.sqrt(control_rate*(1-control_rate) + variant_rate*(1-variant_rate)))**2
        denominator = mde**2
        
        n = numerator / denominator if denominator > 0 else float('inf')
        
        return int(np.ceil(n))
    
    def comprehensive_test(self, control_conversions, control_total,
                          variant_conversions, variant_total):
        """
        Effectue tous les tests statistiques disponibles
        
        Args:
            control_conversions: Nombre de conversions groupe A
            control_total: Taille échantillon groupe A
            variant_conversions: Nombre de conversions groupe B
            variant_total: Taille échantillon groupe B
            
        Returns:
            dict: Tous les résultats de tests
        """
        results = {}
        
        # 1. Chi-square test
        results['chi_square'] = self.chi_square_test(
            control_conversions, control_total,
            variant_conversions, variant_total
        )
        
        # 2. Z-test
        results['z_test'] = self.z_test_proportions(
            control_conversions, control_total,
            variant_conversions, variant_total
        )
        
        # 3. Fisher exact (si échantillon < 1000)
        if min(control_total, variant_total) < 1000:
            results['fisher_exact'] = self.fisher_exact_test(
                control_conversions, control_total,
                variant_conversions, variant_total
            )
        
        # 4. Bayesian test
        results['bayesian'] = self.bayesian_ab_test(
            control_conversions, control_total,
            variant_conversions, variant_total
        )
        
        # 5. Statistical power
        control_rate = control_conversions / control_total
        variant_rate = variant_conversions / variant_total
        results['statistical_power'] = self.calculate_statistical_power(
            control_rate, variant_rate, min(control_total, variant_total)
        )
        
        # 6. Minimum sample size pour MDE = 10%
        mde = control_rate * 0.10  # 10% relative lift
        results['min_sample_size_mde_10pct'] = self.minimum_sample_size(
            control_rate, mde
        )
        
        # 7. Verdict final
        results['verdict'] = self.get_verdict(results)
        
        return results


    def get_verdict(self, test_results):
        """
        Détermine le verdict final basé sur tous les tests
        
        Args:
            test_results: Résultats de comprehensive_test()
            
        Returns:
            dict: Verdict et recommandation
        """
        # Compter le nombre de tests significatifs
        significant_tests = []
        if test_results['chi_square']['is_significant']:
            significant_tests.append('Chi-Square')
        if test_results['z_test']['is_significant']:
            significant_tests.append('Z-Test')
        if 'fisher_exact' in test_results and test_results['fisher_exact']['is_significant']:
            significant_tests.append('Fisher')
        if test_results['bayesian']['is_significant']:
            significant_tests.append('Bayesian')
        
        n_significant = len(significant_tests)
        total_tests = 4 if 'fisher_exact' in test_results else 3
        
        # Probabilité bayésienne que B > A
        prob_b_beats_a = test_results['bayesian']['prob_b_beats_a']
        
        # Puissance statistique
        power = test_results['statistical_power']
        
        # Verdict
        if n_significant >= 2 and prob_b_beats_a > 0.95:
            decision = 'WINNER_VARIANT'
            confidence = 'HIGH'
            recommendation = 'Implémenter le variant B immédiatement. Tous les tests confirment sa supériorité.'
        elif n_significant >= 2 and prob_b_beats_a < 0.05:
            decision = 'WINNER_CONTROL'
            confidence = 'HIGH'
            recommendation = 'Conserver le contrôle A. Le variant B est significativement moins performant.'
        elif n_significant >= 1 and 0.90 < prob_b_beats_a < 0.95:
            decision = 'LIKELY_WINNER_VARIANT'
            confidence = 'MEDIUM'
            recommendation = 'Variant B prometteur mais continuer le test pour augmenter la confiance.'
        elif n_significant >= 1 and 0.05 < prob_b_beats_a < 0.10:
            decision = 'LIKELY_WINNER_CONTROL'
            confidence = 'MEDIUM'
            recommendation = 'Contrôle A probablement meilleur. Continuer le test pour confirmation.'
        elif power < 0.80:
            decision = 'UNDERPOWERED'
            confidence = 'LOW'
            recommendation = f'Échantillon trop petit (puissance: {power:.1%}). Augmenter la taille pour {test_results["min_sample_size_mde_10pct"]} utilisateurs/groupe.'
        else:
            decision = 'INCONCLUSIVE'
            confidence = 'LOW'
            recommendation = 'Résultats non concluants. Continuer le test ou redéfinir les hypothèses.'
        
        return {
            'decision': decision,
            'confidence': confidence,
            'recommendation': recommendation,
            'significant_tests': significant_tests,
            'n_significant': n_significant,
            'total_tests': total_tests,
            'prob_b_beats_a': float(prob_b_beats_a),
            'statistical_power': float(power)
        }


def test_ab_conversions_all_scenarios(csv_path):
    """
    Teste les conversions A vs B pour tous les scénarios
    
    Args:
        csv_path: Chemin vers ab_test_simulation.csv
        
    Returns:
        dict: Résultats de tests pour chaque scénario et métrique
    """
    # Charger les données
    df = pd.read_csv(csv_path)
    
    # Initialiser le testeur
    tester = ABConversionTester(alpha=0.05, power=0.80)
    
    # Résultats par scénario
    results_by_scenario = {}
    
    # Métriques à tester
    conversion_metrics = [
        ('view_to_cart', 'control_carts', 'variant_carts', 'control_views', 'variant_views'),
        ('cart_to_purchase', 'control_purchases', 'variant_purchases', 'control_carts', 'variant_carts'),
        ('view_to_purchase', 'control_purchases', 'variant_purchases', 'control_views', 'variant_views')
    ]
    
    for scenario_id in df['scenario_id'].unique():
        scenario_df = df[df['scenario_id'] == scenario_id]
        scenario_name = scenario_df['scenario_name'].iloc[0]
        target_metric = scenario_df['target_metric'].iloc[0]
        
        print(f"\n{'='*80}")
        print(f"Scénario {scenario_id}: {scenario_name}")
        print(f"Métrique cible: {target_metric}")
        print(f"{'='*80}")
        
        results_by_scenario[scenario_id] = {
            'scenario_name': scenario_name,
            'target_metric': target_metric,
            'metrics': {}
        }
        
        # Tester chaque métrique de conversion
        for metric_name, conv_col_a, conv_col_b, total_col_a, total_col_b in conversion_metrics:
            # Agréger sur tous les jours
            control_conversions = scenario_df[conv_col_a].sum()
            control_total = scenario_df[total_col_a].sum()
            variant_conversions = scenario_df[conv_col_b].sum()
            variant_total = scenario_df[total_col_b].sum()
            
            print(f"\n--- Métrique: {metric_name} ---")
            print(f"Contrôle A: {control_conversions:,} / {control_total:,} = {control_conversions/control_total:.2%}")
            print(f"Variant B:  {variant_conversions:,} / {variant_total:,} = {variant_conversions/variant_total:.2%}")
            
            # Tests complets
            test_results = tester.comprehensive_test(
                control_conversions, control_total,
                variant_conversions, variant_total
            )
            
            # Affichage résumé
            sig_chi = "[SIGNIFICATIF]" if test_results['chi_square']['is_significant'] else "[NON SIGNIFICATIF]"
            print(f"\n- Chi-Square: p={test_results['chi_square']['p_value']:.4f} {sig_chi}")
            print(f"- Z-Test: z={test_results['z_test']['z_score']:.2f}, p={test_results['z_test']['p_value']:.4f}")
            print(f"  Difference: {test_results['z_test']['difference_pct']:.2f}% [{test_results['z_test']['confidence_interval_95']['lower_pct']:.2f}%, {test_results['z_test']['confidence_interval_95']['upper_pct']:.2f}%]")
            print(f"- Bayesian: P(B>A) = {test_results['bayesian']['prob_b_beats_a']:.1%}")
            print(f"  Lift relatif: {test_results['bayesian']['relative_lift_pct']:.2f}%")
            print(f"- Puissance: {test_results['statistical_power']:.1%}")
            print(f"\n>>> VERDICT: {test_results['verdict']['decision']} (confiance: {test_results['verdict']['confidence']})")
            print(f">>> {test_results['verdict']['recommendation']}")
            
            # Sauvegarder
            results_by_scenario[scenario_id]['metrics'][metric_name] = test_results
    
    return results_by_scenario


def generate_test_summary_table(results_by_scenario):
    """
    Génère un tableau résumé des tests pour tous les scénarios
    
    Args:
        results_by_scenario: Résultats de test_ab_conversions_all_scenarios()
        
    Returns:
        pd.DataFrame: Tableau résumé
    """
    rows = []
    
    for scenario_id, scenario_data in results_by_scenario.items():
        scenario_name = scenario_data['scenario_name']
        target_metric = scenario_data['target_metric']
        
        # Résultats pour la métrique cible
        if target_metric in scenario_data['metrics']:
            test_results = scenario_data['metrics'][target_metric]
            
            row = {
                'scenario_id': scenario_id,
                'scenario_name': scenario_name,
                'target_metric': target_metric,
                'control_rate': test_results['z_test']['control_rate'],
                'variant_rate': test_results['z_test']['variant_rate'],
                'lift_pct': test_results['z_test']['difference_pct'],
                'ci_95_lower': test_results['z_test']['confidence_interval_95']['lower_pct'],
                'ci_95_upper': test_results['z_test']['confidence_interval_95']['upper_pct'],
                'p_value_chi2': test_results['chi_square']['p_value'],
                'p_value_ztest': test_results['z_test']['p_value'],
                'prob_b_beats_a': test_results['bayesian']['prob_b_beats_a'],
                'statistical_power': test_results['statistical_power'],
                'decision': test_results['verdict']['decision'],
                'confidence': test_results['verdict']['confidence'],
                'n_significant_tests': test_results['verdict']['n_significant']
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def main():
    """Fonction principale"""
    print("="*80)
    print("Issue #16 - Test des Conversions A vs B")
    print("="*80)
    
    # Chemins
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    csv_path = data_dir / 'ab_test_simulation.csv'
    
    print(f"\nChargement: {csv_path}")
    
    # Tests complets
    print("\n" + "="*80)
    print("TESTS STATISTIQUES COMPLETS")
    print("="*80)
    
    results = test_ab_conversions_all_scenarios(csv_path)
    
    # Tableau résumé
    print("\n" + "="*80)
    print("TABLEAU RÉSUMÉ")
    print("="*80)
    
    summary_df = generate_test_summary_table(results)
    
    # Affichage
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(summary_df.to_string(index=False))
    
    # Sauvegarder résultats (convertir numpy types en Python natifs)
    output_json = output_dir / 'ab_test_conversion_tests.json'
    
    # Fonction pour convertir numpy types
    def convert_numpy(obj):
        if isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    results_clean = convert_numpy(results)
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results_clean, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Resultats sauvegardes: {output_json}")
    
    output_csv = output_dir / 'ab_test_conversion_tests_summary.csv'
    summary_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"[OK] Tableau resume sauvegarde: {output_csv}")
    
    # Statistiques finales
    print("\n" + "="*80)
    print("STATISTIQUES FINALES")
    print("="*80)
    
    n_winner_variant = (summary_df['decision'] == 'WINNER_VARIANT').sum()
    n_winner_control = (summary_df['decision'] == 'WINNER_CONTROL').sum()
    n_inconclusive = (~summary_df['decision'].isin(['WINNER_VARIANT', 'WINNER_CONTROL'])).sum()
    
    print(f"\nTotal scenarios testes: {len(summary_df)}")
    print(f"  -> Winner Variant (B): {n_winner_variant} ({n_winner_variant/len(summary_df):.0%})")
    print(f"  -> Winner Control (A): {n_winner_control} ({n_winner_control/len(summary_df):.0%})")
    print(f"  -> Inconclusive: {n_inconclusive} ({n_inconclusive/len(summary_df):.0%})")
    
    print(f"\nPuissance statistique moyenne: {summary_df['statistical_power'].mean():.1%}")
    print(f"P(B > A) moyen: {summary_df['prob_b_beats_a'].mean():.1%}")
    print(f"Lift moyen: {summary_df['lift_pct'].mean():.2f}%")
    
    print("\n" + "="*80)
    print("Tests termines avec succes!")
    print("="*80)


if __name__ == '__main__':
    main()
