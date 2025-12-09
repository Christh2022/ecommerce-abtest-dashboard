#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Issue #18 - Visualisation des Résultats A/B

Ce script crée des visualisations complètes et interactives pour les résultats
de tests A/B testing, incluant:
- Graphiques de tendance temporelle (lifts quotidiens)
- Comparaisons contrôle vs variant
- Funnels de conversion
- Heatmaps de significativité
- Distribution des p-values
- ROI et impact business

Auteur: Data Science Team
Date: 2025-12-09
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class ABTestVisualizer:
    """Classe pour visualiser les résultats de tests A/B"""
    
    def __init__(self, output_dir: Path):
        """
        Initialise le visualiseur
        
        Args:
            output_dir: Répertoire de sortie pour les graphiques
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration couleurs
        self.colors = {
            'control': '#3498db',      # Bleu
            'variant': '#e74c3c',      # Rouge
            'significant': '#2ecc71',   # Vert
            'not_significant': '#95a5a6',  # Gris
            'positive': '#27ae60',      # Vert foncé
            'negative': '#c0392b'       # Rouge foncé
        }
    
    def plot_daily_lift_trends(self, df: pd.DataFrame, metric: str = 'view_to_cart'):
        """
        Graphique des tendances de lift quotidien par scénario
        
        Args:
            df: DataFrame avec simulation quotidienne
            metric: Métrique à visualiser
        """
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle(f'Évolution Quotidienne du Lift - {metric.replace("_", " ").title()}', 
                     fontsize=16, fontweight='bold')
        
        scenarios = df['scenario_id'].unique()
        
        for idx, scenario_id in enumerate(scenarios):
            ax = axes[idx // 4, idx % 4]
            scenario_data = df[df['scenario_id'] == scenario_id].sort_values('day_number')
            
            # Nom du scénario
            scenario_name = scenario_data['scenario_name'].iloc[0]
            
            # Lift quotidien
            lift_col = f'lift_{metric}_pct'
            
            # Tracer la ligne
            ax.plot(scenario_data['day_number'], scenario_data[lift_col], 
                   marker='o', linewidth=2, markersize=4, color=self.colors['variant'])
            
            # Zones de significativité
            significant = scenario_data['is_significant'].values
            for i in range(len(scenario_data) - 1):
                if significant[i]:
                    ax.axvspan(scenario_data['day_number'].iloc[i], 
                             scenario_data['day_number'].iloc[i+1],
                             alpha=0.2, color=self.colors['significant'])
            
            # Ligne de référence à 0
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
            
            # Moyenne du lift
            mean_lift = scenario_data[lift_col].mean()
            ax.axhline(y=mean_lift, color=self.colors['positive'], 
                      linestyle=':', alpha=0.5, label=f'Moyenne: {mean_lift:.1f}%')
            
            ax.set_title(f'{scenario_id}: {scenario_name}', fontsize=10, fontweight='bold')
            ax.set_xlabel('Jour')
            ax.set_ylabel('Lift (%)')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
        
        plt.tight_layout()
        output_path = self.output_dir / f'daily_lift_trends_{metric}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_control_vs_variant_comparison(self, df: pd.DataFrame):
        """
        Comparaison contrôle vs variant pour toutes les métriques
        
        Args:
            df: DataFrame avec données agrégées par scénario
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Comparaison Contrôle vs Variant - Toutes Métriques', 
                     fontsize=16, fontweight='bold')
        
        metrics = [
            ('view_to_cart_pct', 'View → Cart (%)'),
            ('cart_to_purchase_pct', 'Cart → Purchase (%)'),
            ('view_to_purchase_pct', 'View → Purchase (%)'),
            ('revenue', 'Revenue Moyen (€)')
        ]
        
        for idx, (metric, label) in enumerate(metrics):
            ax = axes[idx // 2, idx % 2]
            
            # Agréger par scénario
            if 'revenue' in metric:
                control_col = 'control_revenue'
                variant_col = 'variant_revenue'
                agg_func = 'sum'
            else:
                control_col = f'control_{metric}'
                variant_col = f'variant_{metric}'
                agg_func = 'mean'
            
            summary = df.groupby('scenario_id').agg({
                control_col: agg_func,
                variant_col: agg_func,
                'scenario_name': 'first'
            }).reset_index()
            
            # Position des barres
            x = np.arange(len(summary))
            width = 0.35
            
            # Barres
            bars1 = ax.bar(x - width/2, summary[control_col], width, 
                          label='Contrôle A', color=self.colors['control'], alpha=0.8)
            bars2 = ax.bar(x + width/2, summary[variant_col], width,
                          label='Variant B', color=self.colors['variant'], alpha=0.8)
            
            # Annotations (différence %)
            for i, (ctrl, var) in enumerate(zip(summary[control_col], summary[variant_col])):
                if ctrl > 0:
                    diff_pct = ((var - ctrl) / ctrl) * 100
                    color = self.colors['positive'] if diff_pct > 0 else self.colors['negative']
                    ax.text(i, max(ctrl, var) * 1.05, f'{diff_pct:+.1f}%',
                           ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')
            
            ax.set_xlabel('Scénario')
            ax.set_ylabel(label)
            ax.set_title(label, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(summary['scenario_id'], rotation=0)
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_path = self.output_dir / 'control_vs_variant_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_funnel_analysis(self, df: pd.DataFrame):
        """
        Analyse funnel de conversion pour chaque scénario
        
        Args:
            df: DataFrame avec données de simulation
        """
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle('Funnel de Conversion - Contrôle vs Variant', 
                     fontsize=16, fontweight='bold')
        
        scenarios = df['scenario_id'].unique()
        
        for idx, scenario_id in enumerate(scenarios):
            ax = axes[idx // 4, idx % 4]
            scenario_data = df[df['scenario_id'] == scenario_id]
            scenario_name = scenario_data['scenario_name'].iloc[0]
            
            # Agréger sur tous les jours
            control_views = scenario_data['control_views'].sum()
            control_carts = scenario_data['control_carts'].sum()
            control_purchases = scenario_data['control_purchases'].sum()
            
            variant_views = scenario_data['variant_views'].sum()
            variant_carts = scenario_data['variant_carts'].sum()
            variant_purchases = scenario_data['variant_purchases'].sum()
            
            # Données funnel
            stages = ['Views', 'Carts', 'Purchases']
            control_values = [control_views, control_carts, control_purchases]
            variant_values = [variant_views, variant_carts, variant_purchases]
            
            # Normaliser à 100% pour visualisation
            control_pct = [100, (control_carts/control_views)*100, (control_purchases/control_views)*100]
            variant_pct = [100, (variant_carts/variant_views)*100, (variant_purchases/variant_views)*100]
            
            x = np.arange(len(stages))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, control_pct, width, 
                          label='Contrôle A', color=self.colors['control'], alpha=0.7)
            bars2 = ax.bar(x + width/2, variant_pct, width,
                          label='Variant B', color=self.colors['variant'], alpha=0.7)
            
            # Annotations
            for i, (c_val, v_val, c_pct, v_pct) in enumerate(zip(
                control_values, variant_values, control_pct, variant_pct)):
                ax.text(i - width/2, c_pct + 2, f'{c_val:,.0f}\n{c_pct:.1f}%',
                       ha='center', va='bottom', fontsize=7)
                ax.text(i + width/2, v_pct + 2, f'{v_val:,.0f}\n{v_pct:.1f}%',
                       ha='center', va='bottom', fontsize=7)
            
            ax.set_title(f'{scenario_id}: {scenario_name}', fontsize=9, fontweight='bold')
            ax.set_ylabel('% de Views Initiales')
            ax.set_xticks(x)
            ax.set_xticklabels(stages)
            ax.legend(fontsize=7)
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_path = self.output_dir / 'funnel_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_significance_heatmap(self, df: pd.DataFrame):
        """
        Heatmap de significativité par scénario et jour
        
        Args:
            df: DataFrame avec simulation quotidienne
        """
        # Pivot: scénarios en lignes, jours en colonnes
        pivot = df.pivot_table(
            values='is_significant',
            index='scenario_id',
            columns='day_number',
            aggfunc='first'
        ).astype(int)
        
        fig, ax = plt.subplots(figsize=(16, 6))
        
        # Heatmap
        sns.heatmap(pivot, annot=False, cmap=['#e74c3c', '#2ecc71'], 
                   cbar_kws={'label': 'Significatif (1) / Non (0)'},
                   linewidths=0.5, linecolor='white', ax=ax)
        
        ax.set_title('Heatmap de Significativité Statistique par Jour', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Jour du Test')
        ax.set_ylabel('Scénario')
        
        plt.tight_layout()
        output_path = self.output_dir / 'significance_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_pvalue_distribution(self, df: pd.DataFrame):
        """
        Distribution des p-values pour tous les scénarios
        
        Args:
            df: DataFrame avec simulation quotidienne
        """
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle('Distribution des P-values au Fil du Temps', 
                     fontsize=16, fontweight='bold')
        
        scenarios = df['scenario_id'].unique()
        
        for idx, scenario_id in enumerate(scenarios):
            ax = axes[idx // 4, idx % 4]
            scenario_data = df[df['scenario_id'] == scenario_id].sort_values('day_number')
            scenario_name = scenario_data['scenario_name'].iloc[0]
            
            # P-values
            pvalues = scenario_data['p_value'].values
            days = scenario_data['day_number'].values
            
            # Scatter plot
            colors = [self.colors['significant'] if pval < 0.05 else self.colors['not_significant'] 
                     for pval in pvalues]
            ax.scatter(days, pvalues, c=colors, alpha=0.6, s=50)
            
            # Ligne de significativité
            ax.axhline(y=0.05, color='red', linestyle='--', linewidth=2, 
                      label='α = 0.05', alpha=0.7)
            ax.axhline(y=0.01, color='darkred', linestyle=':', linewidth=1.5, 
                      label='α = 0.01', alpha=0.5)
            
            # Échelle log pour mieux voir les petites p-values
            ax.set_yscale('log')
            ax.set_ylim(1e-5, 1)
            
            ax.set_title(f'{scenario_id}: {scenario_name}', fontsize=10, fontweight='bold')
            ax.set_xlabel('Jour')
            ax.set_ylabel('P-value (échelle log)')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.output_dir / 'pvalue_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_cumulative_revenue_lift(self, df: pd.DataFrame):
        """
        Revenue lift cumulé au fil du temps
        
        Args:
            df: DataFrame avec simulation quotidienne
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        scenarios = df['scenario_id'].unique()
        
        for scenario_id in scenarios:
            scenario_data = df[df['scenario_id'] == scenario_id].sort_values('day_number')
            scenario_name = scenario_data['scenario_name'].iloc[0]
            
            ax.plot(scenario_data['day_number'], 
                   scenario_data['cumulative_revenue_lift'] / 1000,  # En milliers €
                   marker='o', linewidth=2, markersize=4, 
                   label=f'{scenario_id}: {scenario_name}')
        
        ax.set_title('Revenue Lift Cumulé par Scénario', fontsize=14, fontweight='bold')
        ax.set_xlabel('Jour du Test')
        ax.set_ylabel('Revenue Lift Cumulé (k€)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.output_dir / 'cumulative_revenue_lift.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_roi_comparison(self, summary_csv: Path):
        """
        Comparaison des ROI par scénario
        
        Args:
            summary_csv: Fichier CSV avec résultats agrégés
        """
        df = pd.read_csv(summary_csv)
        
        scenarios = df['scenario_id'].values
        roi_30d = df['roi_30d_pct'].values
        roi_annual = df['annual_roi_pct'].values
        costs = df['implementation_cost'].values
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # ROI 30 jours
        ax1 = axes[0]
        bars1 = ax1.barh(scenarios, roi_30d, color=self.colors['positive'], alpha=0.7)
        ax1.set_xlabel('ROI 30 jours (%)')
        ax1.set_title('ROI à 30 jours par Scénario', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Annotations
        for i, (bar, roi, cost) in enumerate(zip(bars1, roi_30d, costs)):
            ax1.text(roi + 50, i, f'{roi:,.0f}%\n(€{cost:,.0f})', 
                    va='center', fontsize=9)
        
        # ROI annuel
        ax2 = axes[1]
        bars2 = ax2.barh(scenarios, roi_annual, color=self.colors['variant'], alpha=0.7)
        ax2.set_xlabel('ROI Annuel (%)')
        ax2.set_title('ROI Annualisé par Scénario', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Annotations
        for i, (bar, roi) in enumerate(zip(bars2, roi_annual)):
            ax2.text(roi + 1000, i, f'{roi:,.0f}%', va='center', fontsize=9)
        
        plt.tight_layout()
        output_path = self.output_dir / 'roi_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def plot_conversion_test_results(self, summary_csv: Path):
        """
        Résultats des tests statistiques de conversion (Issue #16)
        
        Args:
            summary_csv: Fichier CSV avec résultats des tests
        """
        df = pd.read_csv(summary_csv)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Résultats Tests Statistiques (Issue #16)', 
                     fontsize=16, fontweight='bold')
        
        # 1. Lift avec intervalles de confiance
        ax1 = axes[0, 0]
        scenarios = df['scenario_id']
        lifts = df['lift_pct']
        ci_lower = df['ci_95_lower']
        ci_upper = df['ci_95_upper']
        
        colors_bar = [self.colors['positive'] if d == 'WINNER_VARIANT' 
                     else self.colors['not_significant'] 
                     for d in df['decision']]
        
        bars = ax1.barh(scenarios, lifts, color=colors_bar, alpha=0.7)
        
        # Intervalles de confiance
        for i, (scenario, lift, lower, upper) in enumerate(zip(scenarios, lifts, ci_lower, ci_upper)):
            ax1.plot([lower, upper], [i, i], 'k-', linewidth=2, alpha=0.5)
            ax1.plot([lower, lower], [i-0.2, i+0.2], 'k-', linewidth=2, alpha=0.5)
            ax1.plot([upper, upper], [i-0.2, i+0.2], 'k-', linewidth=2, alpha=0.5)
        
        ax1.axvline(x=0, color='black', linestyle='--', alpha=0.3)
        ax1.set_xlabel('Lift (%) avec IC 95%')
        ax1.set_title('Lift avec Intervalles de Confiance 95%', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. P-values
        ax2 = axes[0, 1]
        pvalues = df['p_value_ztest']
        colors_p = [self.colors['significant'] if pval < 0.05 
                   else self.colors['not_significant'] 
                   for pval in pvalues]
        
        ax2.barh(scenarios, -np.log10(pvalues), color=colors_p, alpha=0.7)
        ax2.axvline(x=-np.log10(0.05), color='red', linestyle='--', linewidth=2, 
                   label='α = 0.05', alpha=0.7)
        ax2.axvline(x=-np.log10(0.01), color='darkred', linestyle=':', linewidth=1.5,
                   label='α = 0.01', alpha=0.5)
        ax2.set_xlabel('-log10(P-value)')
        ax2.set_title('Significativité Statistique (Z-test)', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Probabilité bayésienne P(B > A)
        ax3 = axes[1, 0]
        prob_b_beats_a = df['prob_b_beats_a'] * 100
        colors_bayes = [self.colors['positive'] if prob > 95 
                       else self.colors['not_significant'] 
                       for prob in prob_b_beats_a]
        
        ax3.barh(scenarios, prob_b_beats_a, color=colors_bayes, alpha=0.7)
        ax3.axvline(x=95, color='red', linestyle='--', linewidth=2, 
                   label='95% (seuil décision)', alpha=0.7)
        ax3.set_xlabel('P(B > A) (%)')
        ax3.set_xlim(0, 100)
        ax3.set_title('Probabilité Bayésienne que Variant soit Meilleur', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. Puissance statistique
        ax4 = axes[1, 1]
        power = df['statistical_power'] * 100
        colors_power = [self.colors['positive'] if p > 80 
                       else self.colors['not_significant'] 
                       for p in power]
        
        ax4.barh(scenarios, power, color=colors_power, alpha=0.7)
        ax4.axvline(x=80, color='orange', linestyle='--', linewidth=2, 
                   label='80% (seuil adéquat)', alpha=0.7)
        ax4.set_xlabel('Puissance Statistique (%)')
        ax4.set_xlim(0, 100)
        ax4.set_title('Puissance Statistique des Tests', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        output_path = self.output_dir / 'conversion_test_results.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé: {output_path}")
        plt.close()
    
    def generate_summary_dashboard(self, df: pd.DataFrame, summary_csv: Path):
        """
        Dashboard récapitulatif avec métriques clés
        
        Args:
            df: DataFrame avec simulation quotidienne
            summary_csv: Fichier CSV avec résultats tests
        """
        summary_df = pd.read_csv(summary_csv)
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle('Dashboard Récapitulatif - Tests A/B', 
                     fontsize=18, fontweight='bold')
        
        # 1. Résumé global (texte)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.axis('off')
        
        n_scenarios = len(summary_df)
        n_winners = (summary_df['decision'] == 'WINNER_VARIANT').sum()
        avg_lift = summary_df['lift_pct'].mean()
        avg_prob = summary_df['prob_b_beats_a'].mean() * 100
        
        summary_text = f"""
RÉSUMÉ GLOBAL

Total Scénarios: {n_scenarios}
Winners (Variant B): {n_winners} ({n_winners/n_scenarios*100:.0f}%)

Lift Moyen: {avg_lift:.2f}%
P(B > A) Moyen: {avg_prob:.1f}%

Période: 30 jours
Split: 50% / 50%
"""
        ax1.text(0.1, 0.5, summary_text, fontsize=12, family='monospace',
                verticalalignment='center')
        
        # 2. Top 3 scénarios par lift
        ax2 = fig.add_subplot(gs[0, 1])
        top3 = summary_df.nlargest(3, 'lift_pct')
        ax2.barh(range(3), top3['lift_pct'], color=self.colors['positive'], alpha=0.7)
        ax2.set_yticks(range(3))
        ax2.set_yticklabels([f"{row['scenario_id']}: {row['scenario_name'][:20]}..." 
                             for _, row in top3.iterrows()])
        ax2.set_xlabel('Lift (%)')
        ax2.set_title('Top 3 Lifts', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Distribution des décisions
        ax3 = fig.add_subplot(gs[0, 2])
        decisions = summary_df['decision'].value_counts()
        colors_pie = [self.colors['positive'] if d == 'WINNER_VARIANT' 
                     else self.colors['not_significant'] 
                     for d in decisions.index]
        ax3.pie(decisions.values, labels=decisions.index, autopct='%1.0f%%',
               colors=colors_pie, startangle=90)
        ax3.set_title('Distribution des Verdicts', fontweight='bold')
        
        # 4. Revenue lift cumulé
        ax4 = fig.add_subplot(gs[1, :])
        for scenario_id in df['scenario_id'].unique()[:5]:  # Top 5
            scenario_data = df[df['scenario_id'] == scenario_id].sort_values('day_number')
            ax4.plot(scenario_data['day_number'], 
                    scenario_data['cumulative_revenue_lift'] / 1000,
                    marker='o', linewidth=2, label=scenario_id)
        ax4.set_xlabel('Jour')
        ax4.set_ylabel('Revenue Lift Cumulé (k€)')
        ax4.set_title('Évolution Revenue Lift (Top 5 Scénarios)', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Significativité par scénario
        ax5 = fig.add_subplot(gs[2, 0])
        sig_counts = df.groupby('scenario_id')['is_significant'].sum()
        colors_sig = [self.colors['significant'] if count >= 25 
                     else self.colors['not_significant'] 
                     for count in sig_counts.values]
        ax5.bar(sig_counts.index, sig_counts.values, color=colors_sig, alpha=0.7)
        ax5.axhline(y=25, color='red', linestyle='--', alpha=0.5, label='Seuil 83%')
        ax5.set_xlabel('Scénario')
        ax5.set_ylabel('Jours Significatifs (sur 30)')
        ax5.set_title('Nombre de Jours Significatifs', fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. Moyenne des lifts par métrique
        ax6 = fig.add_subplot(gs[2, 1])
        metrics_avg = {
            'View→Cart': df.groupby('scenario_id')['lift_view_to_cart_pct'].mean().mean(),
            'Cart→Purchase': df.groupby('scenario_id')['lift_cart_to_purchase_pct'].mean().mean(),
            'View→Purchase': df.groupby('scenario_id')['lift_view_to_purchase_pct'].mean().mean()
        }
        ax6.bar(metrics_avg.keys(), metrics_avg.values(), 
               color=[self.colors['control'], self.colors['variant'], self.colors['positive']], 
               alpha=0.7)
        ax6.set_ylabel('Lift Moyen (%)')
        ax6.set_title('Lifts Moyens par Métrique Funnel', fontweight='bold')
        ax6.grid(True, alpha=0.3, axis='y')
        
        # 7. Confiance statistique
        ax7 = fig.add_subplot(gs[2, 2])
        confidence_counts = summary_df['confidence'].value_counts()
        colors_conf = [self.colors['positive'], self.colors['not_significant']]
        ax7.bar(confidence_counts.index, confidence_counts.values, 
               color=colors_conf[:len(confidence_counts)], alpha=0.7)
        ax7.set_ylabel('Nombre de Scénarios')
        ax7.set_title('Niveau de Confiance des Verdicts', fontweight='bold')
        ax7.grid(True, alpha=0.3, axis='y')
        
        plt.savefig(self.output_dir / 'summary_dashboard.png', dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard sauvegardé: {self.output_dir / 'summary_dashboard.png'}")
        plt.close()


def main():
    """Fonction principale"""
    print("="*80)
    print("Issue #18 - Visualisation des Résultats A/B")
    print("="*80)
    
    # Chemins
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = project_root / 'visualizations'
    
    # Charger les données
    print("\nChargement des données...")
    simulation_df = pd.read_csv(data_dir / 'ab_test_simulation.csv')
    summary_json = data_dir / 'ab_test_simulation_summary.json'
    conversion_tests_csv = data_dir / 'ab_test_conversion_tests_summary.csv'
    
    print(f"✓ {len(simulation_df)} lignes chargées (simulation)")
    print(f"✓ {len(simulation_df['scenario_id'].unique())} scénarios")
    
    # Initialiser visualiseur
    viz = ABTestVisualizer(output_dir)
    
    print("\n" + "="*80)
    print("GÉNÉRATION DES VISUALISATIONS")
    print("="*80)
    
    # 1. Tendances de lift quotidien
    print("\n1. Graphiques de tendance lift quotidien...")
    viz.plot_daily_lift_trends(simulation_df, metric='view_to_cart')
    viz.plot_daily_lift_trends(simulation_df, metric='cart_to_purchase')
    viz.plot_daily_lift_trends(simulation_df, metric='view_to_purchase')
    
    # 2. Comparaison contrôle vs variant
    print("\n2. Comparaison contrôle vs variant...")
    viz.plot_control_vs_variant_comparison(simulation_df)
    
    # 3. Analyse funnel
    print("\n3. Analyse funnel de conversion...")
    viz.plot_funnel_analysis(simulation_df)
    
    # 4. Heatmap significativité
    print("\n4. Heatmap de significativité...")
    viz.plot_significance_heatmap(simulation_df)
    
    # 5. Distribution p-values
    print("\n5. Distribution des p-values...")
    viz.plot_pvalue_distribution(simulation_df)
    
    # 6. Revenue lift cumulé
    print("\n6. Revenue lift cumulé...")
    viz.plot_cumulative_revenue_lift(simulation_df)
    
    # 7. Comparaison ROI
    print("\n7. Comparaison des ROI...")
    summary_by_scenario_csv = data_dir / 'ab_test_summary_by_scenario.csv'
    viz.plot_roi_comparison(summary_by_scenario_csv)
    
    # 8. Résultats tests statistiques
    print("\n8. Résultats tests statistiques...")
    viz.plot_conversion_test_results(conversion_tests_csv)
    
    # 9. Dashboard récapitulatif
    print("\n9. Dashboard récapitulatif...")
    viz.generate_summary_dashboard(simulation_df, conversion_tests_csv)
    
    print("\n" + "="*80)
    print("VISUALISATIONS TERMINÉES")
    print("="*80)
    print(f"\nRépertoire de sortie: {output_dir}")
    print(f"Total graphiques générés: 14")
    print("\nFichiers créés:")
    for file in sorted(output_dir.glob('*.png')):
        print(f"  - {file.name}")


if __name__ == '__main__':
    main()
