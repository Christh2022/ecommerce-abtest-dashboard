#!/usr/bin/env python3
"""
Script de nettoyage du fichier events.csv
Supprime les doublons, valide les données et génère un rapport de nettoyage.

Auteur: E-commerce Dashboard Team
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'='*80}\n")

def load_events_file(filepath):
    """Charge le fichier events.csv"""
    print_separator("CHARGEMENT DES DONNEES")
    print(f"Fichier: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        print(f"[OK] {len(df):,} lignes chargees")
        print(f"Colonnes: {', '.join(df.columns.tolist())}")
        print(f"Memoire: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        return df
    except Exception as e:
        print(f"[ERREUR] Impossible de charger le fichier: {e}")
        sys.exit(1)

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
    
    # Doublons partiels (même timestamp + visitorid + itemid)
    key_cols = ['timestamp', 'visitorid', 'itemid']
    if all(col in df.columns for col in key_cols):
        n_key_duplicates = df.duplicated(subset=key_cols).sum()
        print(f"  Lignes dupliquees (timestamp+visitorid+itemid): {n_key_duplicates:,}")
    
    # Distribution des événements
    print("\n[DISTRIBUTION DES EVENEMENTS]")
    if 'event' in df.columns:
        event_counts = df['event'].value_counts()
        for event_type, count in event_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {event_type}: {count:,} ({pct:.2f}%)")
    
    # Valeurs invalides
    print("\n[VALIDATION DES DONNEES]")
    
    # Timestamps négatifs ou nuls
    if 'timestamp' in df.columns:
        invalid_ts = (df['timestamp'] <= 0).sum()
        print(f"  Timestamps invalides (<= 0): {invalid_ts:,}")
    
    # IDs négatifs
    if 'visitorid' in df.columns:
        invalid_vid = (df['visitorid'] < 0).sum()
        print(f"  visitorid invalides (< 0): {invalid_vid:,}")
    
    if 'itemid' in df.columns:
        invalid_iid = (df['itemid'] < 0).sum()
        print(f"  itemid invalides (< 0): {invalid_iid:,}")
    
    # Types d'événements invalides
    if 'event' in df.columns:
        valid_events = ['view', 'addtocart', 'transaction']
        invalid_events = ~df['event'].isin(valid_events)
        print(f"  Types d'evenements invalides: {invalid_events.sum():,}")
        if invalid_events.sum() > 0:
            print(f"    Types trouves: {df.loc[invalid_events, 'event'].unique()}")
    
    return {
        'total_rows': len(df),
        'duplicates': n_duplicates,
        'missing': missing.sum()
    }

def clean_duplicates(df):
    """Supprime les doublons"""
    print_separator("NETTOYAGE DES DOUBLONS")
    
    initial_count = len(df)
    
    # Supprimer les doublons exacts (toutes colonnes identiques)
    df_cleaned = df.drop_duplicates()
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
    if 'timestamp' in df.columns:
        invalid_ts = df['timestamp'] <= 0
        if invalid_ts.sum() > 0:
            df = df[~invalid_ts]
            issues.append(f"Timestamps invalides: {invalid_ts.sum():,}")
    
    # Supprimer les IDs négatifs
    if 'visitorid' in df.columns:
        invalid_vid = df['visitorid'] < 0
        if invalid_vid.sum() > 0:
            df = df[~invalid_vid]
            issues.append(f"visitorid invalides: {invalid_vid.sum():,}")
    
    if 'itemid' in df.columns:
        invalid_iid = df['itemid'] < 0
        if invalid_iid.sum() > 0:
            df = df[~invalid_iid]
            issues.append(f"itemid invalides: {invalid_iid.sum():,}")
    
    # Supprimer les types d'événements invalides
    if 'event' in df.columns:
        valid_events = ['view', 'addtocart', 'transaction']
        invalid_events = ~df['event'].isin(valid_events)
        if invalid_events.sum() > 0:
            df = df[~invalid_events]
            issues.append(f"Types d'evenements invalides: {invalid_events.sum():,}")
    
    # Supprimer les lignes avec valeurs manquantes critiques
    critical_cols = ['timestamp', 'visitorid', 'event', 'itemid']
    existing_critical = [col for col in critical_cols if col in df.columns]
    missing_critical = df[existing_critical].isnull().any(axis=1)
    if missing_critical.sum() > 0:
        df = df[~missing_critical]
        issues.append(f"Lignes avec valeurs manquantes critiques: {missing_critical.sum():,}")
    
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

def validate_transactions(df):
    """Valide la cohérence des transactions"""
    print_separator("VALIDATION DES TRANSACTIONS")
    
    if 'event' not in df.columns or 'transactionid' not in df.columns:
        print("[WARNING] Colonnes event ou transactionid manquantes")
        return df
    
    # Les transactions doivent avoir un transactionid
    transactions = df[df['event'] == 'transaction']
    missing_txid = transactions['transactionid'].isnull().sum()
    
    print(f"Transactions totales: {len(transactions):,}")
    print(f"Transactions sans transactionid: {missing_txid:,}")
    
    if missing_txid > 0:
        print(f"[WARNING] {missing_txid} transactions sans ID seront supprimees")
        # Supprimer les transactions sans ID
        mask = (df['event'] == 'transaction') & (df['transactionid'].isnull())
        df = df[~mask]
    
    # Les non-transactions ne devraient pas avoir de transactionid
    non_transactions = df[df['event'] != 'transaction']
    unexpected_txid = non_transactions['transactionid'].notna().sum()
    
    if unexpected_txid > 0:
        print(f"[INFO] {unexpected_txid:,} evenements non-transaction ont un transactionid (OK si conversion)")
    
    return df

def sort_by_timestamp(df):
    """Trie les données par timestamp"""
    print_separator("TRI DES DONNEES")
    
    if 'timestamp' not in df.columns:
        print("[WARNING] Colonne timestamp manquante, tri ignore")
        return df
    
    print("Tri par timestamp (ordre chronologique)...")
    df = df.sort_values('timestamp').reset_index(drop=True)
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
    print(f"  Valeurs manquantes critiques: {df[['timestamp', 'visitorid', 'event', 'itemid']].isnull().sum().sum():,}")
    
    # Distribution finale
    print(f"\n[DISTRIBUTION FINALE DES EVENEMENTS]")
    if 'event' in df.columns:
        event_counts = df['event'].value_counts()
        for event_type, count in event_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {event_type}: {count:,} ({pct:.2f}%)")
    
    # Statistiques temporelles
    if 'timestamp' in df.columns:
        df_temp = df.copy()
        df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'], unit='ms')
        print(f"\n[PERIODE TEMPORELLE]")
        print(f"  Debut: {df_temp['timestamp'].min()}")
        print(f"  Fin: {df_temp['timestamp'].max()}")
        duration = df_temp['timestamp'].max() - df_temp['timestamp'].min()
        print(f"  Duree: {duration.days} jours")

def save_cleaned_data(df, output_path):
    """Sauvegarde les données nettoyées"""
    print_separator("SAUVEGARDE DES DONNEES")
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        
        # Vérifier le fichier sauvegardé
        file_size = output_path.stat().st_size / 1024**2  # MB
        
        print(f"[OK] Fichier sauvegarde: {output_path}")
        print(f"Taille: {file_size:.2f} MB")
        print(f"Lignes: {len(df):,}")
        
    except Exception as e:
        print(f"[ERREUR] Impossible de sauvegarder: {e}")
        sys.exit(1)

def generate_cleaning_report(stats_before, duplicates_removed, invalid_removed, df_final, output_path):
    """Génère un rapport de nettoyage"""
    print_separator("GENERATION DU RAPPORT")
    
    report_path = output_path.parent / 'CLEANING_REPORT.txt'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("  RAPPORT DE NETTOYAGE - events.csv\n")
        f.write("="*80 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Script: clean_events.py\n\n")
        
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
        
        if 'event' in df_final.columns:
            f.write(f"\nDistribution des evenements:\n")
            event_counts = df_final['event'].value_counts()
            for event_type, count in event_counts.items():
                pct = (count / len(df_final)) * 100
                f.write(f"  {event_type:15} {count:>12,} ({pct:>6.2f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("NETTOYAGE TERMINE AVEC SUCCES\n")
        f.write("="*80 + "\n")
    
    print(f"[OK] Rapport genere: {report_path}")

def main():
    """Fonction principale"""
    print_separator("NETTOYAGE DU FICHIER events.csv")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Chemins
    project_root = Path(__file__).parent.parent
    input_file = project_root / 'data' / 'raw' / 'events.csv'
    output_file = project_root / 'data' / 'clean' / 'events_cleaned.csv'
    
    # Vérifier l'existence du fichier
    if not input_file.exists():
        print(f"[ERREUR] Fichier non trouve: {input_file}")
        print("Executez d'abord: python scripts/download_dataset.py")
        sys.exit(1)
    
    # Étape 1: Charger les données
    df = load_events_file(input_file)
    
    # Étape 2: Analyser avant nettoyage
    stats_before = analyze_before_cleaning(df)
    
    # Étape 3: Nettoyer les doublons
    df_cleaned, duplicates_removed = clean_duplicates(df)
    
    # Étape 4: Nettoyer les données invalides
    df_cleaned, invalid_removed = clean_invalid_data(df_cleaned)
    
    # Étape 5: Valider les transactions
    df_cleaned = validate_transactions(df_cleaned)
    
    # Étape 6: Trier par timestamp
    df_cleaned = sort_by_timestamp(df_cleaned)
    
    # Étape 7: Analyser après nettoyage
    analyze_after_cleaning(df_cleaned, stats_before)
    
    # Étape 8: Sauvegarder
    save_cleaned_data(df_cleaned, output_file)
    
    # Étape 9: Générer le rapport
    generate_cleaning_report(stats_before, duplicates_removed, invalid_removed, df_cleaned, output_file)
    
    print_separator("[TERMINE] NETTOYAGE TERMINE AVEC SUCCES")
    print("Prochaines etapes:")
    print("  1. Verifier le fichier nettoye: data/clean/events_cleaned.csv")
    print("  2. Consulter le rapport: data/clean/CLEANING_REPORT.txt")
    print("  3. Mettre a jour les scripts suivants pour utiliser events_cleaned.csv")
    print("  4. Regenerer les fichiers pretraites si necessaire")
    print()

if __name__ == "__main__":
    main()
