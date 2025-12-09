#!/usr/bin/env python3
"""
Script d'analyse du trafic (visiteurs, sessions) - Issue #9
Génère traffic_analysis.csv avec métriques détaillées de trafic et comportement utilisateur.

Auteur: E-commerce Dashboard Team
Date: 2025-12-09
Issue: #9 - Analyse du trafic (visiteurs, sessions)
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
    """Analyse du trafic: visiteurs, sessions, engagement"""
    print_separator("ANALYSE DU TRAFIC - ISSUE #9")
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
    
    # Charger hourly_analysis.csv si disponible
    hourly_file = data_dir / 'hourly_analysis.csv'
    if hourly_file.exists():
        print("\nChargement de hourly_analysis.csv...")
        hourly_data = pd.read_csv(hourly_file)
        print(f"[OK] {len(hourly_data)} heures chargées")
    else:
        print("\n[INFO] hourly_analysis.csv non trouvé, analyse limitée aux données quotidiennes")
        hourly_data = None
    
    print_separator("CALCUL DES METRIQUES DE TRAFIC")
    
    # Convertir la date
    daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
    
    # 1. ANALYSE GLOBALE DU TRAFIC
    print("1. Calcul des métriques globales...")
    
    traffic_summary = {
        'period': {
            'start_date': daily_metrics['date'].min().strftime('%Y-%m-%d'),
            'end_date': daily_metrics['date'].max().strftime('%Y-%m-%d'),
            'total_days': len(daily_metrics),
            'weekdays': len(daily_metrics[~daily_metrics['is_weekend']]),
            'weekends': len(daily_metrics[daily_metrics['is_weekend']])
        },
        'visitors': {
            'total_unique_users': int(daily_metrics['unique_users'].sum()),
            'avg_daily_users': float(daily_metrics['unique_users'].mean()),
            'median_daily_users': float(daily_metrics['unique_users'].median()),
            'min_daily_users': int(daily_metrics['unique_users'].min()),
            'max_daily_users': int(daily_metrics['unique_users'].max()),
            'std_daily_users': float(daily_metrics['unique_users'].std())
        },
        'sessions': {
            'total_sessions': int(daily_metrics['unique_sessions'].sum()),
            'avg_daily_sessions': float(daily_metrics['unique_sessions'].mean()),
            'median_daily_sessions': float(daily_metrics['unique_sessions'].median()),
            'min_daily_sessions': int(daily_metrics['unique_sessions'].min()),
            'max_daily_sessions': int(daily_metrics['unique_sessions'].max()),
            'sessions_per_user': float(daily_metrics['sessions_per_user'].mean())
        },
        'engagement': {
            'total_events': int(daily_metrics['total_events'].sum()),
            'avg_events_per_day': float(daily_metrics['total_events'].mean()),
            'avg_events_per_user': float(daily_metrics['events_per_user'].mean()),
            'avg_events_per_session': float(daily_metrics['total_events'].sum() / daily_metrics['unique_sessions'].sum())
        }
    }
    
    print(f"   Visiteurs uniques totaux: {traffic_summary['visitors']['total_unique_users']:,}")
    print(f"   Sessions totales: {traffic_summary['sessions']['total_sessions']:,}")
    print(f"   Sessions par utilisateur: {traffic_summary['sessions']['sessions_per_user']:.2f}")
    print(f"   Événements par session: {traffic_summary['engagement']['avg_events_per_session']:.2f}")
    
    # 2. ANALYSE TEMPORELLE
    print("\n2. Analyse temporelle du trafic...")
    
    # Par jour de la semaine
    weekday_stats = daily_metrics.groupby('day_of_week').agg({
        'unique_users': ['mean', 'sum'],
        'unique_sessions': ['mean', 'sum'],
        'total_events': ['mean', 'sum'],
        'transactions': ['mean', 'sum']
    }).round(2)
    
    # Semaine vs Week-end
    weekend_comparison = daily_metrics.groupby('is_weekend').agg({
        'unique_users': ['mean', 'median', 'sum'],
        'unique_sessions': ['mean', 'median', 'sum'],
        'total_events': ['mean', 'median', 'sum'],
        'events_per_user': 'mean',
        'transactions': ['mean', 'sum']
    }).round(2)
    
    traffic_summary['temporal_patterns'] = {
        'weekday_avg_users': float(daily_metrics[~daily_metrics['is_weekend']]['unique_users'].mean()),
        'weekend_avg_users': float(daily_metrics[daily_metrics['is_weekend']]['unique_users'].mean()),
        'weekday_avg_sessions': float(daily_metrics[~daily_metrics['is_weekend']]['unique_sessions'].mean()),
        'weekend_avg_sessions': float(daily_metrics[daily_metrics['is_weekend']]['unique_sessions'].mean()),
        'weekend_uplift_users': float((daily_metrics[daily_metrics['is_weekend']]['unique_users'].mean() / 
                                       daily_metrics[~daily_metrics['is_weekend']]['unique_users'].mean() - 1) * 100),
        'weekend_uplift_sessions': float((daily_metrics[daily_metrics['is_weekend']]['unique_sessions'].mean() / 
                                          daily_metrics[~daily_metrics['is_weekend']]['unique_sessions'].mean() - 1) * 100)
    }
    
    print(f"   Moyenne visiteurs semaine: {traffic_summary['temporal_patterns']['weekday_avg_users']:,.0f}")
    print(f"   Moyenne visiteurs week-end: {traffic_summary['temporal_patterns']['weekend_avg_users']:,.0f}")
    print(f"   Uplift week-end: {traffic_summary['temporal_patterns']['weekend_uplift_users']:+.1f}%")
    
    # 3. ANALYSE PAR MOIS
    print("\n3. Analyse mensuelle du trafic...")
    
    monthly_stats = daily_metrics.groupby('month').agg({
        'unique_users': ['sum', 'mean', 'std'],
        'unique_sessions': ['sum', 'mean', 'std'],
        'total_events': ['sum', 'mean'],
        'transactions': ['sum', 'mean'],
        'daily_revenue': 'sum'
    }).round(2)
    
    # 4. TENDANCES ET CROISSANCE
    print("\n4. Calcul des tendances...")
    
    daily_metrics = daily_metrics.sort_values('date')
    
    # Croissance week-over-week
    daily_metrics['week_start'] = daily_metrics['date'] - pd.to_timedelta(daily_metrics['date'].dt.dayofweek, unit='d')
    weekly_stats = daily_metrics.groupby('week_start').agg({
        'unique_users': 'sum',
        'unique_sessions': 'sum',
        'total_events': 'sum',
        'transactions': 'sum',
        'daily_revenue': 'sum'
    })
    
    weekly_stats['users_growth'] = weekly_stats['unique_users'].pct_change() * 100
    weekly_stats['sessions_growth'] = weekly_stats['unique_sessions'].pct_change() * 100
    
    traffic_summary['growth'] = {
        'avg_weekly_user_growth': float(weekly_stats['users_growth'].mean()),
        'avg_weekly_session_growth': float(weekly_stats['sessions_growth'].mean()),
        'total_user_growth': float((weekly_stats['unique_users'].iloc[-1] / weekly_stats['unique_users'].iloc[0] - 1) * 100),
        'total_session_growth': float((weekly_stats['unique_sessions'].iloc[-1] / weekly_stats['unique_sessions'].iloc[0] - 1) * 100)
    }
    
    print(f"   Croissance hebdo moyenne visiteurs: {traffic_summary['growth']['avg_weekly_user_growth']:+.1f}%")
    print(f"   Croissance hebdo moyenne sessions: {traffic_summary['growth']['avg_weekly_session_growth']:+.1f}%")
    print(f"   Croissance totale visiteurs: {traffic_summary['growth']['total_user_growth']:+.1f}%")
    
    # 5. SEGMENTATION DES UTILISATEURS
    print("\n5. Analyse de la segmentation...")
    
    user_segments = daily_metrics[['date', 'users_new', 'users_occasional', 'users_regular', 'users_premium']].copy()
    user_segments['total_users'] = user_segments[['users_new', 'users_occasional', 'users_regular', 'users_premium']].sum(axis=1)
    
    segment_totals = {
        'new': int(user_segments['users_new'].sum()),
        'occasional': int(user_segments['users_occasional'].sum()),
        'regular': int(user_segments['users_regular'].sum()),
        'premium': int(user_segments['users_premium'].sum())
    }
    
    total_segment_users = sum(segment_totals.values())
    
    traffic_summary['user_segments'] = {
        'new_users': segment_totals['new'],
        'new_users_pct': float(segment_totals['new'] / total_segment_users * 100),
        'occasional_users': segment_totals['occasional'],
        'occasional_users_pct': float(segment_totals['occasional'] / total_segment_users * 100),
        'regular_users': segment_totals['regular'],
        'regular_users_pct': float(segment_totals['regular'] / total_segment_users * 100),
        'premium_users': segment_totals['premium'],
        'premium_users_pct': float(segment_totals['premium'] / total_segment_users * 100)
    }
    
    print(f"   Nouveaux: {traffic_summary['user_segments']['new_users_pct']:.1f}%")
    print(f"   Occasionnels: {traffic_summary['user_segments']['occasional_users_pct']:.1f}%")
    print(f"   Réguliers: {traffic_summary['user_segments']['regular_users_pct']:.1f}%")
    print(f"   Premium: {traffic_summary['user_segments']['premium_users_pct']:.1f}%")
    
    print_separator("GENERATION DES FICHIERS")
    
    # Sauvegarder le résumé JSON
    output_json = output_dir / 'traffic_analysis_summary.json'
    print(f"Sauvegarde de {output_json.name}...")
    traffic_summary['metadata'] = {
        'generated_at': datetime.now().isoformat(),
        'script': 'traffic_analysis.py',
        'issue': '#9'
    }
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(traffic_summary, f, indent=2, ensure_ascii=False)
    print(f"[OK] {output_json}")
    
    # Créer traffic_daily.csv avec métriques enrichies
    print("\nGénération de traffic_daily.csv...")
    traffic_daily = daily_metrics[[
        'date', 'day_of_week', 'is_weekend', 'week_number', 'month',
        'unique_users', 'unique_sessions', 'unique_products',
        'total_events', 'views', 'add_to_carts', 'transactions',
        'events_per_user', 'sessions_per_user',
        'users_new', 'users_occasional', 'users_regular', 'users_premium'
    ]].copy()
    
    # Calculer métriques additionnelles
    traffic_daily['events_per_session'] = (traffic_daily['total_events'] / 
                                            traffic_daily['unique_sessions']).round(2)
    traffic_daily['products_per_session'] = (traffic_daily['unique_products'] / 
                                              traffic_daily['unique_sessions']).round(2)
    traffic_daily['conversion_rate'] = (traffic_daily['transactions'] / 
                                         traffic_daily['unique_users'] * 100).round(2)
    
    # Moyennes mobiles 7 jours
    traffic_daily['ma7_users'] = traffic_daily['unique_users'].rolling(window=7, min_periods=1).mean().round(0)
    traffic_daily['ma7_sessions'] = traffic_daily['unique_sessions'].rolling(window=7, min_periods=1).mean().round(0)
    traffic_daily['ma7_events'] = traffic_daily['total_events'].rolling(window=7, min_periods=1).mean().round(0)
    
    output_csv = output_dir / 'traffic_daily.csv'
    traffic_daily.to_csv(output_csv, index=False)
    print(f"[OK] {output_csv}")
    print(f"     {len(traffic_daily)} jours, {len(traffic_daily.columns)} colonnes")
    
    # Créer traffic_weekly.csv
    print("\nGénération de traffic_weekly.csv...")
    traffic_weekly = weekly_stats.copy()
    traffic_weekly = traffic_weekly.reset_index()
    traffic_weekly.columns = ['week_start', 'total_users', 'total_sessions', 'total_events', 
                               'total_transactions', 'total_revenue', 'users_growth_pct', 'sessions_growth_pct']
    traffic_weekly['avg_users_per_day'] = (traffic_weekly['total_users'] / 7).round(0)
    traffic_weekly['avg_sessions_per_day'] = (traffic_weekly['total_sessions'] / 7).round(0)
    traffic_weekly['conversion_rate'] = (traffic_weekly['total_transactions'] / 
                                          traffic_weekly['total_users'] * 100).round(2)
    
    output_weekly = output_dir / 'traffic_weekly.csv'
    traffic_weekly.to_csv(output_weekly, index=False)
    print(f"[OK] {output_weekly}")
    print(f"     {len(traffic_weekly)} semaines, {len(traffic_weekly.columns)} colonnes")
    
    # Créer traffic_by_weekday.csv
    print("\nGénération de traffic_by_weekday.csv...")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    traffic_weekday = daily_metrics.groupby('day_of_week').agg({
        'unique_users': ['mean', 'std', 'min', 'max', 'sum'],
        'unique_sessions': ['mean', 'std', 'min', 'max', 'sum'],
        'total_events': ['mean', 'std', 'sum'],
        'events_per_user': 'mean',
        'sessions_per_user': 'mean',
        'transactions': ['mean', 'sum'],
        'daily_revenue': ['mean', 'sum']
    }).round(2)
    
    traffic_weekday.columns = ['_'.join(col).strip() for col in traffic_weekday.columns.values]
    traffic_weekday = traffic_weekday.reset_index()
    
    # Réordonner par jour de la semaine
    traffic_weekday['day_order'] = traffic_weekday['day_of_week'].map(
        {day: i for i, day in enumerate(weekday_order)}
    )
    traffic_weekday = traffic_weekday.sort_values('day_order').drop('day_order', axis=1)
    
    output_weekday = output_dir / 'traffic_by_weekday.csv'
    traffic_weekday.to_csv(output_weekday, index=False)
    print(f"[OK] {output_weekday}")
    print(f"     {len(traffic_weekday)} jours de semaine, {len(traffic_weekday.columns)} colonnes")
    
    print_separator("RESUME FINAL")
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ Analyse du trafic terminée avec succès!")
    print(f"\n📊 Métriques clés:")
    print(f"   • Visiteurs uniques: {traffic_summary['visitors']['total_unique_users']:,}")
    print(f"   • Visiteurs/jour (moyenne): {traffic_summary['visitors']['avg_daily_users']:,.0f}")
    print(f"   • Sessions totales: {traffic_summary['sessions']['total_sessions']:,}")
    print(f"   • Sessions/utilisateur: {traffic_summary['sessions']['sessions_per_user']:.2f}")
    print(f"   • Événements/session: {traffic_summary['engagement']['avg_events_per_session']:.2f}")
    print(f"\n📈 Croissance:")
    print(f"   • Croissance hebdo (visiteurs): {traffic_summary['growth']['avg_weekly_user_growth']:+.1f}%")
    print(f"   • Croissance totale (visiteurs): {traffic_summary['growth']['total_user_growth']:+.1f}%")
    print(f"\n👥 Segmentation:")
    print(f"   • Nouveaux: {traffic_summary['user_segments']['new_users_pct']:.1f}%")
    print(f"   • Premium: {traffic_summary['user_segments']['premium_users_pct']:.1f}%")
    print(f"\n📁 Fichiers générés:")
    print(f"   • traffic_analysis_summary.json")
    print(f"   • traffic_daily.csv ({len(traffic_daily)} lignes)")
    print(f"   • traffic_weekly.csv ({len(traffic_weekly)} lignes)")
    print(f"   • traffic_by_weekday.csv ({len(traffic_weekday)} lignes)")
    print(f"\n⏱️  Temps d'exécution: {execution_time:.2f}s")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
