#!/usr/bin/env python3
"""
Script de nettoyage du fichier item_properties.csv
Parse les valeurs mixtes, supprime les doublons et structure les données.

Auteur: E-commerce Dashboard Team
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import re

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def load_item_properties(data_dir):
    """Charge les fichiers item_properties part1 et part2"""
    print_separator("CHARGEMENT DES DONNEES")
    
    part1_path = data_dir / 'raw' / 'item_properties_part1.csv'
    part2_path = data_dir / 'raw' / 'item_properties_part2.csv'
    
    if not part1_path.exists():
        print(f"[ERREUR] Fichier non trouve: {part1_path}")
        sys.exit(1)
    
    if not part2_path.exists():
        print(f"[ERREUR] Fichier non trouve: {part2_path}")
        sys.exit(1)
    
    print("Chargement de item_properties_part1.csv...")
    df1 = pd.read_csv(part1_path)
    print(f"  Part 1: {len(df1):,} lignes")
    
    print("Chargement de item_properties_part2.csv...")
    df2 = pd.read_csv(part2_path)
    print(f"  Part 2: {len(df2):,} lignes")
    
    print("\nConcatenation des deux parties...")
    df = pd.concat([df1, df2], ignore_index=True)
    print(f"[OK] Total: {len(df):,} lignes chargees")
    print(f"Colonnes: {', '.join(df.columns.tolist())}")
    print(f"Memoire: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    return df

def analyze_before_cleaning(df):
    """Analyse l'état des données avant nettoyage"""
    print_separator("ANALYSE AVANT NETTOYAGE")
    
    # Dimensions
    print(f"Dimensions: {df.shape[0]:,} lignes x {df.shape[1]} colonnes")
    
    # Valeurs manquantes
    print("\n[VALEURS MANQUANTES]")
    missing = df.isnull().sum()
    for col in df.columns:
        if missing[col] > 0:
            pct = (missing[col] / len(df)) * 100
            print(f"  {col}: {missing[col]:,} ({pct:.2f}%)")
        else:
            print(f"  {col}: 0")
    
    # Doublons
    print("\n[DOUBLONS]")
    n_duplicates = df.duplicated().sum()
    print(f"  Lignes dupliquees (toutes colonnes): {n_duplicates:,}")
    
    # Doublons par clé (timestamp + itemid + property)
    key_cols = ['timestamp', 'itemid', 'property']
    n_key_duplicates = df.duplicated(subset=key_cols).sum()
    print(f"  Lignes dupliquees (timestamp+itemid+property): {n_key_duplicates:,}")
    
    # Statistiques sur les propriétés
    print("\n[PROPRIETES]")
    print(f"  Proprietes uniques: {df['property'].nunique():,}")
    print(f"  Produits uniques: {df['itemid'].nunique():,}")
    print(f"  Proprietes par produit (moyenne): {len(df) / df['itemid'].nunique():.2f}")
    
    # Top propriétés
    print("\n  Top 10 proprietes les plus frequentes:")
    top_props = df['property'].value_counts().head(10)
    for prop, count in top_props.items():
        pct = (count / len(df)) * 100
        print(f"    {prop}: {count:,} ({pct:.2f}%)")
    
    # Analyse des valeurs
    print("\n[ANALYSE DES VALEURS]")
    
    # Valeurs numériques simples
    numeric_pattern = re.compile(r'^-?\d+\.?\d*$')
    numeric_count = df['value'].astype(str).apply(lambda x: bool(numeric_pattern.match(x))).sum()
    print(f"  Valeurs numeriques simples: {numeric_count:,} ({numeric_count/len(df)*100:.2f}%)")
    
    # Valeurs avec 'n' (ex: n240.000)
    n_pattern = re.compile(r'^n-?\d+\.?\d*')
    n_count = df['value'].astype(str).apply(lambda x: bool(n_pattern.search(x))).sum()
    print(f"  Valeurs avec 'n' prefix: {n_count:,} ({n_count/len(df)*100:.2f}%)")
    
    # Valeurs multiples (avec espaces)
    multi_count = df['value'].astype(str).apply(lambda x: ' ' in x).sum()
    print(f"  Valeurs multiples (avec espaces): {multi_count:,} ({multi_count/len(df)*100:.2f}%)")
    
    # Validation des timestamps
    print("\n[VALIDATION DES DONNEES]")
    invalid_ts = (df['timestamp'] <= 0).sum()
    print(f"  Timestamps invalides (<= 0): {invalid_ts:,}")
    
    invalid_itemid = (df['itemid'] < 0).sum()
    print(f"  itemid invalides (< 0): {invalid_itemid:,}")
    
    return {
        'total_rows': len(df),
        'duplicates': n_duplicates,
        'key_duplicates': n_key_duplicates,
        'missing': missing.sum(),
        'unique_items': df['itemid'].nunique(),
        'unique_properties': df['property'].nunique()
    }

def clean_duplicates(df):
    """Supprime les doublons"""
    print_separator("NETTOYAGE DES DOUBLONS")
    
    initial_count = len(df)
    
    # Stratégie: Garder la dernière occurrence (la plus récente par timestamp)
    print("Suppression des doublons exacts (toutes colonnes)...")
    df_sorted = df.sort_values('timestamp')
    df_cleaned = df_sorted.drop_duplicates(keep='last')
    duplicates_removed = initial_count - len(df_cleaned)
    
    print(f"Lignes avant: {initial_count:,}")
    print(f"Doublons supprimes: {duplicates_removed:,}")
    print(f"Lignes apres: {len(df_cleaned):,}")
    print(f"Taux de doublons: {(duplicates_removed/initial_count)*100:.4f}%")
    
    return df_cleaned, duplicates_removed

def clean_invalid_data(df):
    """Supprime les données invalides"""
    print_separator("NETTOYAGE DES DONNEES INVALIDES")
    
    initial_count = len(df)
    issues = []
    
    # Supprimer les timestamps invalides
    invalid_ts = df['timestamp'] <= 0
    if invalid_ts.sum() > 0:
        df = df[~invalid_ts]
        issues.append(f"Timestamps invalides: {invalid_ts.sum():,}")
    
    # Supprimer les itemid négatifs
    invalid_itemid = df['itemid'] < 0
    if invalid_itemid.sum() > 0:
        df = df[~invalid_itemid]
        issues.append(f"itemid invalides: {invalid_itemid.sum():,}")
    
    # Supprimer les lignes avec valeurs manquantes
    missing_mask = df[['timestamp', 'itemid', 'property', 'value']].isnull().any(axis=1)
    if missing_mask.sum() > 0:
        df = df[~missing_mask]
        issues.append(f"Lignes avec valeurs manquantes: {missing_mask.sum():,}")
    
    # Supprimer les valeurs vides
    empty_values = df['value'].astype(str).str.strip() == ''
    if empty_values.sum() > 0:
        df = df[~empty_values]
        issues.append(f"Valeurs vides: {empty_values.sum():,}")
    
    rows_removed = initial_count - len(df)
    
    if rows_removed > 0:
        print(f"Lignes avant: {initial_count:,}")
        print(f"Problemes detectes:")
        for issue in issues:
            print(f"  - {issue}")
        print(f"Lignes supprimees: {rows_removed:,}")
        print(f"Lignes apres: {len(df):,}")
    else:
        print("[OK] Aucune donnee invalide detectee")
    
    return df, rows_removed

def parse_value_field(value_str):
    """Parse le champ value pour extraire les informations structurées"""
    value_str = str(value_str).strip()
    
    # Pattern pour détecter les valeurs avec 'n' (ex: n240.000, n24.000)
    n_pattern = re.compile(r'n(-?\d+\.?\d*)')
    
    # Pattern pour les nombres simples
    number_pattern = re.compile(r'^-?\d+\.?\d*$')
    
    # Si c'est un nombre simple
    if number_pattern.match(value_str):
        return {
            'value_type': 'numeric',
            'value_numeric': float(value_str),
            'value_text': None,
            'has_n_prefix': False,
            'value_count': 1
        }
    
    # Si contient 'n' prefix
    if n_pattern.search(value_str):
        # Extraire tous les nombres avec 'n'
        n_values = n_pattern.findall(value_str)
        # Extraire les nombres sans 'n'
        clean_str = n_pattern.sub('', value_str)
        other_numbers = [x.strip() for x in clean_str.split() if x.strip() and re.match(r'^\d+\.?\d*$', x.strip())]
        
        return {
            'value_type': 'mixed',
            'value_numeric': None,
            'value_text': value_str,
            'has_n_prefix': True,
            'value_count': len(n_values) + len(other_numbers)
        }
    
    # Si contient plusieurs valeurs séparées par des espaces
    parts = value_str.split()
    if len(parts) > 1:
        return {
            'value_type': 'multiple',
            'value_numeric': None,
            'value_text': value_str,
            'has_n_prefix': False,
            'value_count': len(parts)
        }
    
    # Sinon, valeur texte simple
    return {
        'value_type': 'text',
        'value_numeric': None,
        'value_text': value_str,
        'has_n_prefix': False,
        'value_count': 1
    }

def structure_data(df):
    """Structure les données en parsant le champ value"""
    print_separator("STRUCTURATION DES DONNEES")
    
    print("Parsing du champ 'value' (peut prendre plusieurs minutes)...")
    
    # Parser chaque valeur
    parsed_data = df['value'].apply(parse_value_field)
    
    # Extraire les composants dans de nouvelles colonnes
    df['value_type'] = parsed_data.apply(lambda x: x['value_type'])
    df['value_numeric'] = parsed_data.apply(lambda x: x['value_numeric'])
    df['value_text'] = parsed_data.apply(lambda x: x['value_text'])
    df['has_n_prefix'] = parsed_data.apply(lambda x: x['has_n_prefix'])
    df['value_count'] = parsed_data.apply(lambda x: x['value_count'])
    
    print("[OK] Parsing termine")
    
    # Statistiques
    print("\n[DISTRIBUTION DES TYPES DE VALEURS]")
    type_counts = df['value_type'].value_counts()
    for val_type, count in type_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {val_type}: {count:,} ({pct:.2f}%)")
    
    print(f"\n[VALEURS AVEC PREFIX 'n']")
    n_prefix_count = df['has_n_prefix'].sum()
    print(f"  Total: {n_prefix_count:,} ({n_prefix_count/len(df)*100:.2f}%)")
    
    print(f"\n[VALEURS MULTIPLES]")
    multi_values = df[df['value_count'] > 1]
    print(f"  Lignes avec valeurs multiples: {len(multi_values):,}")
    print(f"  Valeurs par ligne (moyenne): {df['value_count'].mean():.2f}")
    print(f"  Valeurs par ligne (max): {df['value_count'].max()}")
    
    return df

def create_property_pivot(df):
    """Crée une table pivot des propriétés par produit"""
    print_separator("CREATION DE LA TABLE PIVOT")
    
    print("Creation d'une vue pivot des proprietes par produit...")
    
    # Garder seulement les propriétés les plus récentes pour chaque produit
    df_sorted = df.sort_values('timestamp')
    df_latest = df_sorted.groupby(['itemid', 'property']).tail(1)
    
    print(f"  Proprietes uniques par produit: {len(df_latest):,}")
    
    # Créer un dictionnaire des propriétés par produit
    print("  Aggregation des proprietes...")
    product_props = df_latest.groupby('itemid').agg({
        'property': lambda x: list(x),
        'value': lambda x: list(x),
        'timestamp': 'max'
    }).reset_index()
    
    product_props.columns = ['itemid', 'properties_list', 'values_list', 'last_updated']
    product_props['properties_count'] = product_props['properties_list'].apply(len)
    
    print(f"[OK] {len(product_props):,} produits avec proprietes")
    print(f"  Proprietes par produit (moyenne): {product_props['properties_count'].mean():.2f}")
    print(f"  Proprietes par produit (mediane): {product_props['properties_count'].median():.0f}")
    print(f"  Proprietes par produit (max): {product_props['properties_count'].max()}")
    
    return product_props

def sort_by_timestamp(df):
    """Trie les données par timestamp"""
    print_separator("TRI DES DONNEES")
    
    print("Tri par timestamp et itemid...")
    df = df.sort_values(['timestamp', 'itemid', 'property']).reset_index(drop=True)
    print(f"[OK] {len(df):,} lignes triees")
    
    return df

def analyze_after_cleaning(df, stats_before):
    """Analyse l'état des données après nettoyage"""
    print_separator("ANALYSE APRES NETTOYAGE")
    
    print(f"Dimensions: {df.shape[0]:,} lignes x {df.shape[1]} colonnes")
    
    # Changements
    rows_removed = stats_before['total_rows'] - len(df)
    pct_removed = (rows_removed / stats_before['total_rows']) * 100
    
    print(f"\n[RESUME DES CHANGEMENTS]")
    print(f"  Lignes avant: {stats_before['total_rows']:,}")
    print(f"  Lignes apres: {len(df):,}")
    print(f"  Lignes supprimees: {rows_removed:,} ({pct_removed:.4f}%)")
    
    # Validation finale
    print(f"\n[VALIDATION FINALE]")
    print(f"  Doublons restants: {df.duplicated().sum():,}")
    print(f"  Valeurs manquantes: {df[['timestamp', 'itemid', 'property', 'value']].isnull().sum().sum():,}")
    print(f"  Produits uniques: {df['itemid'].nunique():,}")
    print(f"  Proprietes uniques: {df['property'].nunique():,}")
    
    # Statistiques temporelles
    df_temp = df.copy()
    df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'], unit='ms')
    print(f"\n[PERIODE TEMPORELLE]")
    print(f"  Debut: {df_temp['timestamp'].min()}")
    print(f"  Fin: {df_temp['timestamp'].max()}")
    duration = df_temp['timestamp'].max() - df_temp['timestamp'].min()
    print(f"  Duree: {duration.days} jours")

def save_cleaned_data(df, product_props, output_dir):
    """Sauvegarde les données nettoyées"""
    print_separator("SAUVEGARDE DES DONNEES")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fichier principal (toutes les propriétés)
    main_file = output_dir / 'item_properties_cleaned.csv'
    print(f"Sauvegarde de item_properties_cleaned.csv...")
    df.to_csv(main_file, index=False)
    file_size = main_file.stat().st_size / 1024**2
    print(f"[OK] {main_file}")
    print(f"  Taille: {file_size:.2f} MB")
    print(f"  Lignes: {len(df):,}")
    
    # Fichier pivot (propriétés par produit)
    pivot_file = output_dir / 'product_properties_summary.csv'
    print(f"\nSauvegarde de product_properties_summary.csv...")
    product_props.to_csv(pivot_file, index=False)
    pivot_size = pivot_file.stat().st_size / 1024**2
    print(f"[OK] {pivot_file}")
    print(f"  Taille: {pivot_size:.2f} MB")
    print(f"  Lignes: {len(product_props):,}")

def generate_cleaning_report(stats_before, duplicates_removed, invalid_removed, df_final, output_dir):
    """Génère un rapport de nettoyage"""
    print_separator("GENERATION DU RAPPORT")
    
    report_path = output_dir / 'ITEM_PROPERTIES_CLEANING_REPORT.txt'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("  RAPPORT DE NETTOYAGE - item_properties.csv\n")
        f.write("="*80 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Script: clean_item_properties.py\n\n")
        
        f.write("-"*80 + "\n")
        f.write("RESUME DES OPERATIONS\n")
        f.write("-"*80 + "\n\n")
        
        f.write(f"Lignes initiales:        {stats_before['total_rows']:>12,}\n")
        f.write(f"Doublons supprimes:      {duplicates_removed:>12,}\n")
        f.write(f"Donnees invalides:       {invalid_removed:>12,}\n")
        f.write(f"Lignes finales:          {len(df_final):>12,}\n")
        
        total_removed = stats_before['total_rows'] - len(df_final)
        pct_removed = (total_removed / stats_before['total_rows']) * 100
        f.write(f"Total supprime:          {total_removed:>12,} ({pct_removed:.4f}%)\n\n")
        
        f.write("-"*80 + "\n")
        f.write("VALIDATION FINALE\n")
        f.write("-"*80 + "\n\n")
        
        f.write(f"Doublons restants:       {df_final.duplicated().sum():>12,}\n")
        f.write(f"Valeurs manquantes:      {df_final.isnull().sum().sum():>12,}\n")
        f.write(f"Produits uniques:        {df_final['itemid'].nunique():>12,}\n")
        f.write(f"Proprietes uniques:      {df_final['property'].nunique():>12,}\n")
        
        if 'value_type' in df_final.columns:
            f.write(f"\nDistribution des types de valeurs:\n")
            type_counts = df_final['value_type'].value_counts()
            for val_type, count in type_counts.items():
                pct = (count / len(df_final)) * 100
                f.write(f"  {val_type:15} {count:>12,} ({pct:>6.2f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("NETTOYAGE TERMINE AVEC SUCCES\n")
        f.write("="*80 + "\n")
    
    print(f"[OK] Rapport genere: {report_path}")

def main():
    """Fonction principale"""
    print_separator("NETTOYAGE DES FICHIERS item_properties")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    output_dir = data_dir / 'clean'
    
    # Étape 1: Charger les données
    df = load_item_properties(data_dir)
    
    # Étape 2: Analyser avant nettoyage
    stats_before = analyze_before_cleaning(df)
    
    # Étape 3: Nettoyer les doublons
    df_cleaned, duplicates_removed = clean_duplicates(df)
    
    # Étape 4: Nettoyer les données invalides
    df_cleaned, invalid_removed = clean_invalid_data(df_cleaned)
    
    # Étape 5: Structurer les données (parser le champ value)
    df_cleaned = structure_data(df_cleaned)
    
    # Étape 6: Créer la table pivot
    product_props = create_property_pivot(df_cleaned)
    
    # Étape 7: Trier par timestamp
    df_cleaned = sort_by_timestamp(df_cleaned)
    
    # Étape 8: Analyser après nettoyage
    analyze_after_cleaning(df_cleaned, stats_before)
    
    # Étape 9: Sauvegarder
    save_cleaned_data(df_cleaned, product_props, output_dir)
    
    # Étape 10: Générer le rapport
    generate_cleaning_report(stats_before, duplicates_removed, invalid_removed, df_cleaned, output_dir)
    
    print_separator("[TERMINE] NETTOYAGE TERMINE AVEC SUCCES")
    print("Fichiers generes:")
    print("  1. data/clean/item_properties_cleaned.csv")
    print("  2. data/clean/product_properties_summary.csv")
    print("  3. data/clean/ITEM_PROPERTIES_CLEANING_REPORT.txt")
    print("\nProchaines etapes:")
    print("  1. Utiliser item_properties_cleaned.csv pour les analyses")
    print("  2. Utiliser product_properties_summary.csv pour un acces rapide")
    print("  3. Charger les donnees dans PostgreSQL")
    print()

if __name__ == "__main__":
    main()
