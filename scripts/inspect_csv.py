#!/usr/bin/env python3
"""
Script d'inspection des fichiers CSV RetailRocket
Analyse les données brutes et nettoyées pour identifier les problèmes de qualité.

Auteur: E-commerce Dashboard Team
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def inspect_basic_info(df, filename):
    """Affiche les informations de base sur le DataFrame"""
    print(f"[FICHIER] {filename}")
    print(f"   Dimensions: {df.shape[0]:,} lignes × {df.shape[1]} colonnes")
    print(f"   Colonnes: {', '.join(df.columns.tolist())}")
    print(f"   Mémoire utilisée: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print()

def inspect_missing_values(df, filename):
    """Analyse les valeurs manquantes"""
    print(f"[VALEURS MANQUANTES] {filename}:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    if missing.sum() == 0:
        print("   [OK] Aucune valeur manquante detectee")
    else:
        for col in missing[missing > 0].index:
            print(f"   [WARNING] {col}: {missing[col]:,} ({missing_pct[col]:.2f}%)")
    print()

def inspect_duplicates(df, filename):
    """Analyse les doublons"""
    print(f"[DOUBLONS] {filename}:")
    n_duplicates = df.duplicated().sum()
    
    if n_duplicates == 0:
        print("   [OK] Aucun doublon detecte")
    else:
        print(f"   [WARNING] {n_duplicates:,} lignes dupliquees ({n_duplicates/len(df)*100:.2f}%)")
    print()

def inspect_data_types(df, filename):
    """Affiche les types de données"""
    print(f"[TYPES DE DONNEES] {filename}:")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")
    print()

def inspect_statistics(df, filename):
    """Affiche les statistiques descriptives"""
    print(f"[STATISTIQUES] {filename}:")
    
    # Colonnes numériques
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print("\n   Colonnes numériques:")
        stats = df[numeric_cols].describe()
        print(stats.to_string(max_cols=None))
    
    # Colonnes catégorielles
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        print("\n   Colonnes catégorielles:")
        for col in categorical_cols:
            n_unique = df[col].nunique()
            most_common = df[col].value_counts().head(3)
            print(f"\n   {col}:")
            print(f"      Valeurs uniques: {n_unique:,}")
            print(f"      Top 3:")
            for val, count in most_common.items():
                print(f"         - {val}: {count:,} ({count/len(df)*100:.2f}%)")
    print()

def inspect_timestamp_column(df, filename, col_name='timestamp'):
    """Analyse spécifique pour les colonnes timestamp"""
    if col_name not in df.columns:
        return
    
    print(f"[ANALYSE TEMPORELLE] {filename}:")
    
    # Convertir en datetime si nécessaire
    if df[col_name].dtype == 'int64':
        df[col_name] = pd.to_datetime(df[col_name], unit='ms')
    
    print(f"   Periode: {df[col_name].min()} -> {df[col_name].max()}")
    duration = df[col_name].max() - df[col_name].min()
    print(f"   Durée: {duration.days} jours")
    
    # Distribution par jour de la semaine
    weekday_counts = df[col_name].dt.day_name().value_counts()
    print(f"\n   Distribution par jour de la semaine:")
    for day, count in weekday_counts.items():
        print(f"      {day}: {count:,}")
    
    # Distribution par heure
    hour_counts = df[col_name].dt.hour.value_counts().sort_index()
    print(f"\n   Heures les plus actives:")
    for hour, count in hour_counts.nlargest(5).items():
        print(f"      {hour}h: {count:,}")
    print()

def inspect_events_file(filepath):
    """Inspection spécifique pour events.csv"""
    print_separator("INSPECTION: events.csv")
    
    df = pd.read_csv(filepath)
    
    inspect_basic_info(df, "events.csv")
    inspect_data_types(df, "events.csv")
    inspect_missing_values(df, "events.csv")
    inspect_duplicates(df, "events.csv")
    
    # Analyse des événements
    if 'event' in df.columns:
        print("[DISTRIBUTION EVENEMENTS]:")
        event_counts = df['event'].value_counts()
        for event_type, count in event_counts.items():
            print(f"   {event_type}: {count:,} ({count/len(df)*100:.2f}%)")
        print()
    
    inspect_timestamp_column(df, "events.csv")
    
    # Statistiques par utilisateur
    if 'visitorid' in df.columns:
        print("[STATISTIQUES UTILISATEURS]:")
        events_per_user = df.groupby('visitorid').size()
        print(f"   Utilisateurs uniques: {df['visitorid'].nunique():,}")
        print(f"   Événements par utilisateur (moyenne): {events_per_user.mean():.2f}")
        print(f"   Événements par utilisateur (médiane): {events_per_user.median():.0f}")
        print(f"   Max événements d'un utilisateur: {events_per_user.max():,}")
        print()
    
    # Statistiques par produit
    if 'itemid' in df.columns:
        print("[STATISTIQUES PRODUITS]:")
        events_per_item = df.groupby('itemid').size()
        print(f"   Produits uniques: {df['itemid'].nunique():,}")
        print(f"   Événements par produit (moyenne): {events_per_item.mean():.2f}")
        print(f"   Événements par produit (médiane): {events_per_item.median():.0f}")
        print(f"   Produits les plus consultés (top 5):")
        for item, count in events_per_item.nlargest(5).items():
            print(f"      Item {item}: {count:,} événements")
        print()

def inspect_item_properties_file(filepath):
    """Inspection spécifique pour item_properties_part1.csv et part2.csv"""
    print_separator("INSPECTION: item_properties")
    
    # Charger les deux parties
    df1 = pd.read_csv(str(filepath))
    df2_path = str(filepath).replace("item_properties_part1.csv", "item_properties_part2.csv")
    df2 = pd.read_csv(df2_path)
    df = pd.concat([df1, df2], ignore_index=True)
    
    inspect_basic_info(df, "item_properties (combiné)")
    inspect_data_types(df, "item_properties")
    inspect_missing_values(df, "item_properties")
    inspect_duplicates(df, "item_properties")
    
    # Analyse des propriétés
    if 'property' in df.columns:
        print("[TYPES DE PROPRIETES]:")
        prop_counts = df['property'].value_counts()
        print(f"   Propriétés uniques: {df['property'].nunique():,}")
        print(f"\n   Top 10 propriétés les plus fréquentes:")
        for prop, count in prop_counts.head(10).items():
            print(f"      {prop}: {count:,}")
        print()
    
    # Produits avec propriétés
    if 'itemid' in df.columns:
        print("[PRODUITS AVEC PROPRIETES]:")
        items_with_props = df.groupby('itemid').size()
        print(f"   Produits uniques: {df['itemid'].nunique():,}")
        print(f"   Propriétés par produit (moyenne): {items_with_props.mean():.2f}")
        print(f"   Propriétés par produit (médiane): {items_with_props.median():.0f}")
        print()
    
    inspect_timestamp_column(df, "item_properties")

def inspect_category_tree_file(filepath):
    """Inspection spécifique pour category_tree.csv"""
    print_separator("INSPECTION: category_tree.csv")
    
    df = pd.read_csv(filepath)
    
    inspect_basic_info(df, "category_tree.csv")
    inspect_data_types(df, "category_tree.csv")
    inspect_missing_values(df, "category_tree.csv")
    inspect_duplicates(df, "category_tree.csv")
    
    # Analyse de la hiérarchie
    if 'categoryid' in df.columns and 'parentid' in df.columns:
        print("[STRUCTURE HIERARCHIQUE]:")
        print(f"   Catégories uniques: {df['categoryid'].nunique():,}")
        
        # Catégories racines (sans parent)
        root_categories = df[df['parentid'].isna()]
        print(f"   Catégories racines: {len(root_categories)}")
        
        # Profondeur de l'arbre
        def get_depth(row, df):
            depth = 0
            parent = row['parentid']
            while pd.notna(parent):
                depth += 1
                parent_row = df[df['categoryid'] == parent]
                if len(parent_row) == 0:
                    break
                parent = parent_row.iloc[0]['parentid']
            return depth
        
        if len(df) < 10000:  # Seulement si le dataset n'est pas trop grand
            df['depth'] = df.apply(lambda row: get_depth(row, df), axis=1)
            print(f"   Profondeur maximale: {df['depth'].max()}")
            print(f"   Profondeur moyenne: {df['depth'].mean():.2f}")
        print()

def inspect_clean_files(data_dir):
    """Inspection des fichiers nettoyés"""
    print_separator("INSPECTION DES FICHIERS NETTOYÉS")
    
    clean_files = {
        'users.csv': 'users',
        'products.csv': 'products',
        'sessions.csv': 'sessions',
        'transactions.csv': 'transactions'
    }
    
    for filename, description in clean_files.items():
        filepath = data_dir / 'clean' / filename
        
        if not filepath.exists():
            print(f"[WARNING] Fichier {filename} non trouve dans data/clean/")
            print(f"   Executez: python scripts/preprocess_retailrocket.py\n")
            continue
        
        print_separator(f"FICHIER: {filename}")
        
        df = pd.read_csv(filepath)
        
        inspect_basic_info(df, filename)
        inspect_data_types(df, filename)
        inspect_missing_values(df, filename)
        inspect_duplicates(df, filename)
        inspect_statistics(df, filename)

def main():
    """Fonction principale"""
    print_separator("INSPECTION DES FICHIERS CSV - RetailRocket Dataset")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Répertoires
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    raw_dir = data_dir / 'raw'
    
    # Vérifier que les fichiers existent
    events_file = raw_dir / 'events.csv'
    item_props_file = raw_dir / 'item_properties_part1.csv'
    category_file = raw_dir / 'category_tree.csv'
    
    # Inspection des fichiers bruts
    print_separator("PHASE 1: FICHIERS BRUTS")
    
    if events_file.exists():
        inspect_events_file(events_file)
    else:
        print(f"[WARNING] Fichier events.csv non trouve dans {raw_dir}/")
        print(f"   Executez: python scripts/download_dataset.py\n")
    
    if item_props_file.exists():
        inspect_item_properties_file(item_props_file)
    else:
        print(f"[WARNING] Fichiers item_properties non trouves dans {raw_dir}/")
    
    if category_file.exists():
        inspect_category_tree_file(category_file)
    else:
        print(f"[WARNING] Fichier category_tree.csv non trouve dans {raw_dir}/")
    
    # Inspection des fichiers nettoyés
    print_separator("PHASE 2: FICHIERS NETTOYÉS")
    inspect_clean_files(data_dir)
    
    print_separator("[TERMINE] INSPECTION TERMINEE")
    print("Rapport d'inspection genere avec succes!")
    print("\nProchaines étapes:")
    print("  1. Examiner les valeurs manquantes identifiées")
    print("  2. Traiter les doublons si nécessaire")
    print("  3. Valider les types de données")
    print("  4. Analyser les anomalies détectées")
    print()

if __name__ == "__main__":
    main()
