#!/usr/bin/env python3
"""
Script de fusion des données nettoyées
Crée des tables enrichies et des vues analytiques pour le dashboard.

Auteur: E-commerce Dashboard Team
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import sys

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def load_cleaned_data(data_dir):
    """Charge tous les fichiers nettoyés"""
    print_separator("CHARGEMENT DES DONNEES NETTOYEES")
    
    files_to_load = {
        'users': 'users.csv',
        'products': 'products.csv',
        'sessions': 'sessions.csv',
        'transactions': 'transactions.csv',
        'events': 'events_cleaned.csv'
    }
    
    data = {}
    
    for name, filename in files_to_load.items():
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"[WARNING] Fichier non trouve: {filepath}")
            print(f"  Certaines fonctionnalites seront limitees")
            data[name] = None
        else:
            # Pour products, charger seulement les 3 premières colonnes pour économiser la mémoire
            if name == 'products':
                df = pd.read_csv(filepath, usecols=['product_id', 'view_count', 'purchase_count'])
            else:
                df = pd.read_csv(filepath)
            data[name] = df
            print(f"[OK] {filename}: {len(df):,} lignes")
    
    return data

def enrich_events(events_df, users_df, products_df):
    """Enrichit les événements avec les données utilisateurs et produits"""
    print_separator("ENRICHISSEMENT DES EVENEMENTS")
    
    if events_df is None:
        print("[ERROR] Donnees events manquantes")
        return None
    
    events_enriched = events_df.copy()
    
    # Enrichir avec les utilisateurs
    if users_df is not None:
        print("Fusion avec users (segment utilisateur)...")
        events_enriched = events_enriched.merge(
            users_df[['user_id', 'segment']],
            left_on='visitorid',
            right_on='user_id',
            how='left'
        )
        events_enriched.drop('user_id', axis=1, inplace=True)
        print(f"  [OK] Colonne 'segment' ajoutee")
    
    # Enrichir avec les produits
    if products_df is not None:
        print("Fusion avec products (statistiques produits)...")
        events_enriched = events_enriched.merge(
            products_df[['product_id', 'view_count', 'purchase_count']],
            left_on='itemid',
            right_on='product_id',
            how='left'
        )
        events_enriched.drop('product_id', axis=1, inplace=True)
        print(f"  [OK] Colonnes produits ajoutees")
    
    # Convertir timestamp en datetime
    print("Conversion du timestamp...")
    events_enriched['datetime'] = pd.to_datetime(events_enriched['timestamp'], unit='ms')
    events_enriched['date'] = events_enriched['datetime'].dt.date
    events_enriched['hour'] = events_enriched['datetime'].dt.hour
    events_enriched['day_of_week'] = events_enriched['datetime'].dt.day_name()
    print(f"  [OK] Colonnes temporelles ajoutees")
    
    print(f"\n[RESULTAT] Events enrichis: {len(events_enriched):,} lignes x {len(events_enriched.columns)} colonnes")
    
    return events_enriched

def enrich_sessions(sessions_df, users_df):
    """Enrichit les sessions avec les données utilisateurs"""
    print_separator("ENRICHISSEMENT DES SESSIONS")
    
    if sessions_df is None:
        print("[ERROR] Donnees sessions manquantes")
        return None
    
    sessions_enriched = sessions_df.copy()
    
    # Enrichir avec les utilisateurs
    if users_df is not None:
        print("Fusion avec users (segment utilisateur)...")
        sessions_enriched = sessions_enriched.merge(
            users_df[['user_id', 'segment', 'total_events']],
            on='user_id',
            how='left',
            suffixes=('_session', '_user')
        )
        print(f"  [OK] Colonnes utilisateurs ajoutees")
    
    print(f"\n[RESULTAT] Sessions enrichies: {len(sessions_enriched):,} lignes x {len(sessions_enriched.columns)} colonnes")
    
    return sessions_enriched

def enrich_transactions(transactions_df, users_df, products_df):
    """Enrichit les transactions avec les données utilisateurs et produits"""
    print_separator("ENRICHISSEMENT DES TRANSACTIONS")
    
    if transactions_df is None:
        print("[ERROR] Donnees transactions manquantes")
        return None
    
    transactions_enriched = transactions_df.copy()
    
    # Enrichir avec les utilisateurs
    if users_df is not None:
        print("Fusion avec users (segment utilisateur)...")
        transactions_enriched = transactions_enriched.merge(
            users_df[['user_id', 'segment', 'total_events']],
            on='user_id',
            how='left'
        )
        print(f"  [OK] Segment utilisateur ajoute")
    
    # Enrichir avec les produits
    if products_df is not None:
        print("Fusion avec products (statistiques produits)...")
        transactions_enriched = transactions_enriched.merge(
            products_df[['product_id', 'view_count', 'purchase_count']],
            on='product_id',
            how='left'
        )
        print(f"  [OK] Statistiques produits ajoutees")
    
    print(f"\n[RESULTAT] Transactions enrichies: {len(transactions_enriched):,} lignes x {len(transactions_enriched.columns)} colonnes")
    
    return transactions_enriched

def create_daily_funnel(events_enriched):
    """Crée un entonnoir de conversion par jour"""
    print_separator("CREATION: ENTONNOIR QUOTIDIEN")
    
    if events_enriched is None or 'date' not in events_enriched.columns:
        print("[ERROR] Donnees insuffisantes")
        return None
    
    print("Calcul des metriques par jour...")
    
    daily_stats = events_enriched.groupby('date').agg({
        'visitorid': 'nunique',
        'itemid': 'nunique',
        'timestamp': 'count'
    }).rename(columns={
        'visitorid': 'unique_users',
        'itemid': 'unique_products',
        'timestamp': 'total_events'
    })
    
    # Compter par type d'événement
    event_counts = events_enriched.groupby(['date', 'event']).size().unstack(fill_value=0)
    
    # Fusionner
    daily_funnel = daily_stats.join(event_counts)
    
    # Calculer les taux de conversion
    if 'view' in daily_funnel.columns:
        daily_funnel['addtocart_rate'] = (daily_funnel.get('addtocart', 0) / daily_funnel['view'] * 100).round(2)
        daily_funnel['transaction_rate'] = (daily_funnel.get('transaction', 0) / daily_funnel['view'] * 100).round(2)
    
    if 'addtocart' in daily_funnel.columns and 'transaction' in daily_funnel.columns:
        daily_funnel['cart_to_purchase'] = (daily_funnel['transaction'] / daily_funnel['addtocart'] * 100).round(2)
    
    print(f"[OK] Entonnoir quotidien cree: {len(daily_funnel)} jours")
    
    return daily_funnel

def create_hourly_analysis(events_enriched):
    """Analyse horaire de l'activité"""
    print_separator("CREATION: ANALYSE HORAIRE")
    
    if events_enriched is None or 'hour' not in events_enriched.columns:
        print("[ERROR] Donnees insuffisantes")
        return None
    
    print("Calcul des metriques par heure...")
    
    hourly_stats = events_enriched.groupby('hour').agg({
        'visitorid': 'nunique',
        'timestamp': 'count'
    }).rename(columns={
        'visitorid': 'unique_users',
        'timestamp': 'total_events'
    })
    
    # Compter par type d'événement
    event_counts = events_enriched.groupby(['hour', 'event']).size().unstack(fill_value=0)
    hourly_analysis = hourly_stats.join(event_counts)
    
    # Taux de conversion horaire
    if 'view' in hourly_analysis.columns and 'transaction' in hourly_analysis.columns:
        hourly_analysis['conversion_rate'] = (hourly_analysis['transaction'] / hourly_analysis['view'] * 100).round(2)
    
    print(f"[OK] Analyse horaire creee: 24 heures")
    
    return hourly_analysis

def create_segment_performance(transactions_enriched):
    """Performance par segment utilisateur"""
    print_separator("CREATION: PERFORMANCE PAR SEGMENT")
    
    if transactions_enriched is None or 'segment' not in transactions_enriched.columns:
        print("[ERROR] Donnees insuffisantes")
        return None
    
    print("Calcul des KPIs par segment...")
    
    segment_stats = transactions_enriched.groupby('segment').agg({
        'user_id': 'nunique',
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    
    segment_stats.columns = ['num_users', 'total_revenue', 'avg_transaction', 'num_transactions']
    
    # Calculer le revenu par utilisateur
    segment_stats['revenue_per_user'] = (segment_stats['total_revenue'] / segment_stats['num_users']).round(2)
    
    print(f"[OK] Performance par segment creee: {len(segment_stats)} segments")
    
    return segment_stats

def create_user_journey(events_enriched):
    """Analyse du parcours utilisateur"""
    print_separator("CREATION: PARCOURS UTILISATEUR")
    
    if events_enriched is None:
        print("[ERROR] Donnees insuffisantes")
        return None
    
    print("Calcul des sequences d'evenements...")
    
    # Trier par utilisateur et timestamp
    events_sorted = events_enriched.sort_values(['visitorid', 'timestamp'])
    
    # Analyser les séquences
    user_journey = events_sorted.groupby('visitorid').agg({
        'event': lambda x: ' -> '.join(x.head(10)),  # Premières 10 étapes
        'timestamp': ['min', 'max', 'count'],
        'segment': 'first'
    })
    
    user_journey.columns = ['journey', 'first_event_time', 'last_event_time', 'total_events', 'segment']
    
    # Calculer la durée du parcours (en heures)
    user_journey['first_event_time'] = pd.to_datetime(user_journey['first_event_time'], unit='ms')
    user_journey['last_event_time'] = pd.to_datetime(user_journey['last_event_time'], unit='ms')
    user_journey['journey_duration_hours'] = (
        (user_journey['last_event_time'] - user_journey['first_event_time']).dt.total_seconds() / 3600
    ).round(2)
    
    print(f"[OK] Parcours utilisateur cree: {len(user_journey):,} utilisateurs")
    
    return user_journey

def create_product_performance(events_enriched, transactions_enriched):
    """Performance détaillée des produits"""
    print_separator("CREATION: PERFORMANCE PRODUITS")
    
    if events_enriched is None:
        print("[ERROR] Donnees insuffisantes")
        return None
    
    print("Calcul des metriques produits...")
    
    # Statistiques d'événements par produit
    product_events = events_enriched.groupby('itemid').agg({
        'timestamp': 'count',
        'visitorid': 'nunique'
    }).rename(columns={
        'timestamp': 'total_events',
        'visitorid': 'unique_viewers'
    })
    
    # Compter par type d'événement
    event_counts = events_enriched.groupby(['itemid', 'event']).size().unstack(fill_value=0)
    product_performance = product_events.join(event_counts)
    
    # Ajouter les revenus si transactions disponibles
    if transactions_enriched is not None and 'amount' in transactions_enriched.columns:
        revenue_stats = transactions_enriched.groupby('product_id').agg({
            'amount': ['sum', 'mean', 'count']
        })
        revenue_stats.columns = ['total_revenue', 'avg_price', 'num_sales']
        
        product_performance = product_performance.join(revenue_stats, how='left')
        product_performance['total_revenue'] = product_performance['total_revenue'].fillna(0)
        product_performance['num_sales'] = product_performance['num_sales'].fillna(0)
    
    # Calculer les taux de conversion produit
    if 'view' in product_performance.columns and 'transaction' in product_performance.columns:
        product_performance['view_to_purchase_rate'] = (
            product_performance['transaction'] / product_performance['view'] * 100
        ).round(2)
    
    if 'addtocart' in product_performance.columns and 'transaction' in product_performance.columns:
        product_performance['cart_to_purchase_rate'] = (
            product_performance['transaction'] / product_performance['addtocart'] * 100
        ).round(2)
    
    print(f"[OK] Performance produits creee: {len(product_performance):,} produits")
    
    return product_performance

def save_merged_data(output_dir, **dataframes):
    """Sauvegarde toutes les tables créées"""
    print_separator("SAUVEGARDE DES DONNEES")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    
    for name, df in dataframes.items():
        if df is not None and len(df) > 0:
            filepath = output_dir / f"{name}.csv"
            df.to_csv(filepath, index=True if df.index.name else False)
            file_size = filepath.stat().st_size / 1024**2
            print(f"[OK] {name}.csv: {len(df):,} lignes, {file_size:.2f} MB")
            saved_files.append(name)
        else:
            print(f"[SKIP] {name}: pas de donnees")
    
    return saved_files

def generate_statistics(data, enriched_data, output_dir):
    """Génère des statistiques globales"""
    print_separator("GENERATION DES STATISTIQUES")
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'source_files': {},
        'enriched_tables': {},
        'analysis_tables': {},
        'global_kpis': {}
    }
    
    # Stats des fichiers sources
    for name, df in data.items():
        if df is not None:
            stats['source_files'][name] = {
                'rows': len(df),
                'columns': len(df.columns)
            }
    
    # Stats des tables enrichies
    for name in ['events_enriched', 'sessions_enriched', 'transactions_enriched']:
        if name in enriched_data and enriched_data[name] is not None:
            df = enriched_data[name]
            stats['enriched_tables'][name] = {
                'rows': len(df),
                'columns': len(df.columns)
            }
    
    # Stats des tables d'analyse
    for name in ['daily_funnel', 'hourly_analysis', 'segment_performance', 
                 'user_journey', 'product_performance']:
        if name in enriched_data and enriched_data[name] is not None:
            df = enriched_data[name]
            stats['analysis_tables'][name] = {
                'rows': len(df),
                'columns': len(df.columns)
            }
    
    # KPIs globaux
    if data['events'] is not None:
        events_df = data['events']
        stats['global_kpis']['total_events'] = len(events_df)
        stats['global_kpis']['unique_users'] = events_df['visitorid'].nunique()
        stats['global_kpis']['unique_products'] = events_df['itemid'].nunique()
        
        # Compter par type
        event_counts = events_df['event'].value_counts().to_dict()
        stats['global_kpis']['event_breakdown'] = event_counts
        
        # Taux de conversion global
        if 'view' in event_counts and 'transaction' in event_counts:
            conversion = (event_counts['transaction'] / event_counts['view'] * 100)
            stats['global_kpis']['conversion_rate'] = f"{conversion:.2f}%"
    
    if data['transactions'] is not None:
        trans_df = data['transactions']
        if 'amount' in trans_df.columns:
            stats['global_kpis']['total_revenue'] = f"{trans_df['amount'].sum():.2f}"
            stats['global_kpis']['avg_order_value'] = f"{trans_df['amount'].mean():.2f}"
            stats['global_kpis']['total_transactions'] = len(trans_df)
    
    # Période
    if data['events'] is not None and 'timestamp' in data['events'].columns:
        events_df = data['events']
        events_df['datetime'] = pd.to_datetime(events_df['timestamp'], unit='ms')
        stats['global_kpis']['period_start'] = events_df['datetime'].min().strftime('%Y-%m-%d')
        stats['global_kpis']['period_end'] = events_df['datetime'].max().strftime('%Y-%m-%d')
        duration = (events_df['datetime'].max() - events_df['datetime'].min()).days
        stats['global_kpis']['period_days'] = duration
    
    # Sauvegarder les stats
    stats_file = output_dir / 'merge_statistics.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Statistiques sauvegardees: {stats_file}")
    
    # Afficher les KPIs
    print("\n[KPIS GLOBAUX]")
    for key, value in stats['global_kpis'].items():
        if key != 'event_breakdown':
            print(f"  {key}: {value}")
    
    return stats

def main():
    """Fonction principale"""
    print_separator("FUSION DES DONNEES - Issue #5")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'clean'
    output_dir = data_dir
    
    # Étape 1: Charger les données
    data = load_cleaned_data(data_dir)
    
    # Vérifier qu'on a au moins les events
    if data['events'] is None:
        print("\n[ERROR] Impossible de continuer sans events_cleaned.csv")
        sys.exit(1)
    
    # Étape 2: Enrichir les données
    enriched_data = {}
    
    enriched_data['events_enriched'] = enrich_events(
        data['events'], data['users'], data['products']
    )
    
    enriched_data['sessions_enriched'] = enrich_sessions(
        data['sessions'], data['users']
    )
    
    enriched_data['transactions_enriched'] = enrich_transactions(
        data['transactions'], data['users'], data['products']
    )
    
    # Étape 3: Créer les tables d'analyse
    enriched_data['daily_funnel'] = create_daily_funnel(enriched_data['events_enriched'])
    
    enriched_data['hourly_analysis'] = create_hourly_analysis(enriched_data['events_enriched'])
    
    enriched_data['segment_performance'] = create_segment_performance(
        enriched_data['transactions_enriched']
    )
    
    enriched_data['user_journey'] = create_user_journey(enriched_data['events_enriched'])
    
    enriched_data['product_performance'] = create_product_performance(
        enriched_data['events_enriched'],
        enriched_data['transactions_enriched']
    )
    
    # Étape 4: Sauvegarder
    saved_files = save_merged_data(output_dir, **enriched_data)
    
    # Étape 5: Générer les statistiques
    stats = generate_statistics(data, enriched_data, output_dir)
    
    # Résumé
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print_separator("FUSION TERMINEE AVEC SUCCES")
    print(f"Temps d'execution: {elapsed:.1f} secondes")
    print(f"Fichiers generes: {len(saved_files)}")
    print(f"\nFichiers disponibles dans: {output_dir}")
    print("\nTables enrichies:")
    for name in ['events_enriched', 'sessions_enriched', 'transactions_enriched']:
        if name in saved_files:
            print(f"  - {name}.csv")
    print("\nTables d'analyse:")
    for name in ['daily_funnel', 'hourly_analysis', 'segment_performance', 
                 'user_journey', 'product_performance']:
        if name in saved_files:
            print(f"  - {name}.csv")
    print(f"\nStatistiques: merge_statistics.json")
    print()

if __name__ == "__main__":
    main()
