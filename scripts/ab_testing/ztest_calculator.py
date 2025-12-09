#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Issue #17 - Implémentation Z-test et P-value

Module utilitaire pour calculs statistiques Z-test et p-values
pour tests A/B testing et comparaisons de proportions.

Ce module peut être utilisé de manière standalone ou importé dans d'autres scripts.

Auteur: Data Science Team
Date: 2025-12-09
"""

import numpy as np
from scipy import stats
from scipy.stats import norm
import pandas as pd
from typing import Tuple, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class ZTestCalculator:
    """
    Calculateur Z-test et p-values pour tests A/B
    
    Implémente:
    - Z-test pour différence de proportions (2 échantillons)
    - Z-test pour une proportion (1 échantillon)
    - Calcul p-values (unilatéral et bilatéral)
    - Intervalles de confiance
    - Effect size (Cohen's h)
    - Minimum detectable effect (MDE)
    """
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialise le calculateur
        
        Args:
            alpha: Niveau de significativité (défaut: 0.05 pour 95% confiance)
        """
        self.alpha = alpha
        self.z_critical = norm.ppf(1 - alpha/2)  # Z-score critique pour IC bilateral
        
    def two_sample_z_test(self, 
                          conversions_a: int, 
                          total_a: int,
                          conversions_b: int, 
                          total_b: int,
                          alternative: str = 'two-sided') -> Dict:
        """
        Z-test pour comparer deux proportions (test A vs B)
        
        Args:
            conversions_a: Nombre de conversions groupe A
            total_a: Taille échantillon groupe A
            conversions_b: Nombre de conversions groupe B
            total_b: Taille échantillon groupe B
            alternative: Type de test ('two-sided', 'greater', 'less')
            
        Returns:
            dict: Résultats complets du test
        """
        # Calcul des proportions
        p_a = conversions_a / total_a
        p_b = conversions_b / total_b
        
        # Proportion poolée (sous H0: p_a = p_b)
        p_pooled = (conversions_a + conversions_b) / (total_a + total_b)
        
        # Erreur standard poolée
        se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1/total_a + 1/total_b))
        
        # Z-score
        if se_pooled > 0:
            z_score = (p_b - p_a) / se_pooled
        else:
            z_score = 0.0
        
        # P-value selon type de test
        if alternative == 'two-sided':
            p_value = 2 * (1 - norm.cdf(abs(z_score)))
        elif alternative == 'greater':
            p_value = 1 - norm.cdf(z_score)
        elif alternative == 'less':
            p_value = norm.cdf(z_score)
        else:
            raise ValueError("alternative doit être 'two-sided', 'greater' ou 'less'")
        
        # Intervalle de confiance pour la différence
        diff = p_b - p_a
        se_diff = np.sqrt(p_a*(1-p_a)/total_a + p_b*(1-p_b)/total_b)
        ci_lower = diff - self.z_critical * se_diff
        ci_upper = diff + self.z_critical * se_diff
        
        # Effect size (Cohen's h)
        cohen_h = 2 * (np.arcsin(np.sqrt(p_b)) - np.arcsin(np.sqrt(p_a)))
        
        # Interprétation effect size
        if abs(cohen_h) < 0.2:
            effect_size_interpretation = 'Small'
        elif abs(cohen_h) < 0.5:
            effect_size_interpretation = 'Medium'
        else:
            effect_size_interpretation = 'Large'
        
        return {
            'z_score': float(z_score),
            'p_value': float(p_value),
            'is_significant': p_value < self.alpha,
            'alpha': self.alpha,
            'alternative': alternative,
            'proportion_a': float(p_a),
            'proportion_b': float(p_b),
            'difference': float(diff),
            'difference_pct': float(diff * 100),
            'relative_lift': float((p_b - p_a) / p_a) if p_a > 0 else 0.0,
            'relative_lift_pct': float(((p_b - p_a) / p_a) * 100) if p_a > 0 else 0.0,
            'confidence_interval': {
                'lower': float(ci_lower),
                'upper': float(ci_upper),
                'lower_pct': float(ci_lower * 100),
                'upper_pct': float(ci_upper * 100),
                'level': 1 - self.alpha
            },
            'standard_error': {
                'pooled': float(se_pooled),
                'difference': float(se_diff)
            },
            'effect_size': {
                'cohen_h': float(cohen_h),
                'interpretation': effect_size_interpretation
            },
            'sample_sizes': {
                'group_a': total_a,
                'group_b': total_b,
                'total': total_a + total_b
            }
        }
    
    def one_sample_z_test(self,
                         conversions: int,
                         total: int,
                         expected_proportion: float,
                         alternative: str = 'two-sided') -> Dict:
        """
        Z-test pour une proportion vs valeur attendue
        
        Args:
            conversions: Nombre de conversions observées
            total: Taille échantillon
            expected_proportion: Proportion attendue sous H0
            alternative: Type de test ('two-sided', 'greater', 'less')
            
        Returns:
            dict: Résultats du test
        """
        # Proportion observée
        p_observed = conversions / total
        
        # Erreur standard sous H0
        se = np.sqrt(expected_proportion * (1 - expected_proportion) / total)
        
        # Z-score
        if se > 0:
            z_score = (p_observed - expected_proportion) / se
        else:
            z_score = 0.0
        
        # P-value
        if alternative == 'two-sided':
            p_value = 2 * (1 - norm.cdf(abs(z_score)))
        elif alternative == 'greater':
            p_value = 1 - norm.cdf(z_score)
        elif alternative == 'less':
            p_value = norm.cdf(z_score)
        else:
            raise ValueError("alternative doit être 'two-sided', 'greater' ou 'less'")
        
        # Intervalle de confiance
        ci_lower = p_observed - self.z_critical * se
        ci_upper = p_observed + self.z_critical * se
        
        return {
            'z_score': float(z_score),
            'p_value': float(p_value),
            'is_significant': p_value < self.alpha,
            'alpha': self.alpha,
            'alternative': alternative,
            'observed_proportion': float(p_observed),
            'expected_proportion': float(expected_proportion),
            'difference': float(p_observed - expected_proportion),
            'confidence_interval': {
                'lower': float(ci_lower),
                'upper': float(ci_upper),
                'level': 1 - self.alpha
            },
            'standard_error': float(se),
            'sample_size': total
        }
    
    def calculate_minimum_sample_size(self,
                                     baseline_rate: float,
                                     mde: float,
                                     power: float = 0.80,
                                     ratio: float = 1.0) -> Dict:
        """
        Calcule la taille minimale d'échantillon pour détecter un MDE donné
        
        Args:
            baseline_rate: Taux de conversion baseline (groupe A)
            mde: Minimum Detectable Effect (différence absolue)
            power: Puissance statistique désirée (défaut: 0.80)
            ratio: Ratio taille groupe B / groupe A (défaut: 1.0 pour split 50/50)
            
        Returns:
            dict: Tailles d'échantillon requises
        """
        variant_rate = baseline_rate + mde
        
        # Z-scores
        z_alpha = norm.ppf(1 - self.alpha/2)
        z_beta = norm.ppf(power)
        
        # Formule pour échantillon groupe A
        numerator = (z_alpha * np.sqrt((1 + 1/ratio) * baseline_rate * (1 - baseline_rate)) + 
                    z_beta * np.sqrt(baseline_rate*(1-baseline_rate) + variant_rate*(1-variant_rate)/ratio))**2
        denominator = mde**2
        
        n_a = numerator / denominator if denominator > 0 else float('inf')
        n_b = n_a * ratio
        
        return {
            'sample_size_group_a': int(np.ceil(n_a)),
            'sample_size_group_b': int(np.ceil(n_b)),
            'total_sample_size': int(np.ceil(n_a + n_b)),
            'baseline_rate': float(baseline_rate),
            'variant_rate': float(variant_rate),
            'mde_absolute': float(mde),
            'mde_relative_pct': float(mde / baseline_rate * 100) if baseline_rate > 0 else 0.0,
            'power': power,
            'alpha': self.alpha,
            'ratio': ratio
        }
    
    def calculate_confidence_interval(self,
                                     conversions: int,
                                     total: int,
                                     confidence_level: Optional[float] = None) -> Dict:
        """
        Calcule l'intervalle de confiance pour une proportion
        
        Args:
            conversions: Nombre de conversions
            total: Taille échantillon
            confidence_level: Niveau de confiance (défaut: 1 - alpha)
            
        Returns:
            dict: Intervalle de confiance
        """
        if confidence_level is None:
            confidence_level = 1 - self.alpha
        
        p = conversions / total
        z = norm.ppf(1 - (1 - confidence_level)/2)
        se = np.sqrt(p * (1 - p) / total)
        
        ci_lower = p - z * se
        ci_upper = p + z * se
        
        return {
            'proportion': float(p),
            'confidence_level': confidence_level,
            'confidence_interval': {
                'lower': float(max(0, ci_lower)),
                'upper': float(min(1, ci_upper)),
                'lower_pct': float(max(0, ci_lower) * 100),
                'upper_pct': float(min(1, ci_upper) * 100)
            },
            'margin_of_error': float(z * se),
            'margin_of_error_pct': float(z * se * 100),
            'standard_error': float(se),
            'sample_size': total
        }
    
    def quick_test(self, 
                   conversions_a: int, 
                   total_a: int,
                   conversions_b: int, 
                   total_b: int) -> str:
        """
        Test rapide avec résumé textuel
        
        Args:
            conversions_a: Conversions groupe A
            total_a: Total groupe A
            conversions_b: Conversions groupe B
            total_b: Total groupe B
            
        Returns:
            str: Résumé formaté du test
        """
        result = self.two_sample_z_test(conversions_a, total_a, conversions_b, total_b)
        
        summary = f"""
=== Z-TEST RÉSULTATS ===

Groupe A: {conversions_a:,} / {total_a:,} = {result['proportion_a']:.2%}
Groupe B: {conversions_b:,} / {total_b:,} = {result['proportion_b']:.2%}

Différence: {result['difference_pct']:.2f}% (absolue)
Lift relatif: {result['relative_lift_pct']:.2f}%

Z-score: {result['z_score']:.3f}
P-value: {result['p_value']:.4f}

Intervalle de confiance 95%: [{result['confidence_interval']['lower_pct']:.2f}%, {result['confidence_interval']['upper_pct']:.2f}%]

Effect size (Cohen's h): {result['effect_size']['cohen_h']:.3f} ({result['effect_size']['interpretation']})

Verdict: {'✓ SIGNIFICATIF' if result['is_significant'] else '✗ NON SIGNIFICATIF'} (α={self.alpha})
"""
        return summary


def demo_z_test():
    """Démonstration d'utilisation du module"""
    
    print("="*80)
    print("DÉMONSTRATION Z-TEST ET P-VALUE")
    print("="*80)
    
    # Initialiser le calculateur
    calc = ZTestCalculator(alpha=0.05)
    
    # Exemple 1: Test A/B simple
    print("\n" + "="*80)
    print("EXEMPLE 1: Test A/B - Amélioration Photos Produits")
    print("="*80)
    
    conversions_a = 7652
    total_a = 296175
    conversions_b = 9847
    total_b = 296175
    
    result = calc.two_sample_z_test(conversions_a, total_a, conversions_b, total_b)
    
    print(f"\nGroupe A (Control): {conversions_a:,} / {total_a:,} = {result['proportion_a']:.2%}")
    print(f"Groupe B (Variant): {conversions_b:,} / {total_b:,} = {result['proportion_b']:.2%}")
    print(f"\nDifférence absolue: {result['difference_pct']:.2f}%")
    print(f"Lift relatif: {result['relative_lift_pct']:.2f}%")
    print(f"\nZ-score: {result['z_score']:.3f}")
    print(f"P-value: {result['p_value']:.6f}")
    print(f"IC 95%: [{result['confidence_interval']['lower_pct']:.2f}%, {result['confidence_interval']['upper_pct']:.2f}%]")
    print(f"\nEffect size: {result['effect_size']['cohen_h']:.3f} ({result['effect_size']['interpretation']})")
    print(f"\nVERDICT: {'✓ SIGNIFICATIF' if result['is_significant'] else '✗ NON SIGNIFICATIF'}")
    
    # Exemple 2: Test unilatéral (B > A ?)
    print("\n" + "="*80)
    print("EXEMPLE 2: Test unilatéral - B est-il meilleur que A ?")
    print("="*80)
    
    result_greater = calc.two_sample_z_test(
        conversions_a, total_a, 
        conversions_b, total_b,
        alternative='greater'
    )
    
    print(f"\nH0: B ≤ A")
    print(f"H1: B > A")
    print(f"\nP-value (unilatéral): {result_greater['p_value']:.6f}")
    print(f"VERDICT: {'✓ B est significativement meilleur' if result_greater['is_significant'] else '✗ Pas de preuve que B meilleur'}")
    
    # Exemple 3: Taille d'échantillon minimale
    print("\n" + "="*80)
    print("EXEMPLE 3: Calcul taille minimale échantillon")
    print("="*80)
    
    baseline = 0.0258  # 2.58% taux baseline
    mde = 0.0026  # Détecter différence de +0.26% (10% relatif)
    
    sample_size = calc.calculate_minimum_sample_size(baseline, mde, power=0.80)
    
    print(f"\nBaseline: {baseline:.2%}")
    print(f"MDE: {mde:.2%} absolu (+{sample_size['mde_relative_pct']:.1f}% relatif)")
    print(f"Puissance: {sample_size['power']:.0%}")
    print(f"Alpha: {sample_size['alpha']:.2f}")
    print(f"\nTaille requise groupe A: {sample_size['sample_size_group_a']:,}")
    print(f"Taille requise groupe B: {sample_size['sample_size_group_b']:,}")
    print(f"Total requis: {sample_size['total_sample_size']:,}")
    
    # Exemple 4: Test une proportion
    print("\n" + "="*80)
    print("EXEMPLE 4: Test une proportion vs attendu")
    print("="*80)
    
    conversions_observed = 850
    total_observed = 30000
    expected_rate = 0.025  # 2.5% attendu
    
    result_one = calc.one_sample_z_test(
        conversions_observed, 
        total_observed, 
        expected_rate
    )
    
    print(f"\nObservé: {conversions_observed:,} / {total_observed:,} = {result_one['observed_proportion']:.2%}")
    print(f"Attendu: {expected_rate:.2%}")
    print(f"Différence: {result_one['difference']:.2%}")
    print(f"\nZ-score: {result_one['z_score']:.3f}")
    print(f"P-value: {result_one['p_value']:.4f}")
    print(f"\nVERDICT: {'✓ Différent de l\'attendu' if result_one['is_significant'] else '✗ Conforme à l\'attendu'}")
    
    # Exemple 5: Intervalle de confiance
    print("\n" + "="*80)
    print("EXEMPLE 5: Intervalle de confiance")
    print("="*80)
    
    ci = calc.calculate_confidence_interval(conversions_b, total_b, confidence_level=0.95)
    
    print(f"\nProportion: {ci['proportion']:.2%}")
    print(f"IC 95%: [{ci['confidence_interval']['lower_pct']:.2f}%, {ci['confidence_interval']['upper_pct']:.2f}%]")
    print(f"Marge d'erreur: ±{ci['margin_of_error_pct']:.2f}%")
    
    # Exemple 6: Quick test
    print("\n" + "="*80)
    print("EXEMPLE 6: Quick test (méthode rapide)")
    print("="*80)
    
    print(calc.quick_test(conversions_a, total_a, conversions_b, total_b))
    
    print("="*80)
    print("FIN DÉMONSTRATION")
    print("="*80)


def batch_test_from_csv(csv_path: str, alpha: float = 0.05) -> pd.DataFrame:
    """
    Effectue des Z-tests en batch depuis un fichier CSV
    
    Args:
        csv_path: Chemin vers CSV avec colonnes:
                  control_conversions, control_total, variant_conversions, variant_total
        alpha: Niveau de significativité
        
    Returns:
        pd.DataFrame: Résultats de tous les tests
    """
    df = pd.read_csv(csv_path)
    calc = ZTestCalculator(alpha=alpha)
    
    results = []
    for idx, row in df.iterrows():
        result = calc.two_sample_z_test(
            int(row['control_conversions']),
            int(row['control_total']),
            int(row['variant_conversions']),
            int(row['variant_total'])
        )
        
        results.append({
            'test_id': idx + 1,
            'z_score': result['z_score'],
            'p_value': result['p_value'],
            'is_significant': result['is_significant'],
            'proportion_a': result['proportion_a'],
            'proportion_b': result['proportion_b'],
            'lift_pct': result['relative_lift_pct'],
            'ci_lower': result['confidence_interval']['lower_pct'],
            'ci_upper': result['confidence_interval']['upper_pct']
        })
    
    return pd.DataFrame(results)


if __name__ == '__main__':
    # Exécuter la démonstration
    demo_z_test()
