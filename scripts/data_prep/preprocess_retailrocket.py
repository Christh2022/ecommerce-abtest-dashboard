"""
Script de préprocessing du dataset RetailRocket
Transforme les données brutes en format exploitable pour le dashboard
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_CLEAN_DIR = PROJECT_ROOT / "data" / "clean"


def load_events():
    """Charger et préprocesser le fichier events.csv"""
    print("\n📥 Chargement de events.csv...")
    
    events_file = DATA_RAW_DIR / "events.csv"
    if not events_file.exists():
        print(f"❌ Fichier non trouvé: {events_file}")
        return None
    
    # Charger les données
    df = pd.read_csv(events_file)
    print(f"  ✓ {len(df):,} événements chargés")
    
    # Afficher les premières lignes
    print(f"\n📋 Aperçu des colonnes: {list(df.columns)}")
    print(f"📊 Types d'événements: {df['event'].unique().tolist() if 'event' in df.columns else 'N/A'}")
    
    # Convertir timestamp en datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        print(f"  ✓ Timestamps convertis")
        print(f"  📅 Période: {df['timestamp'].min()} à {df['timestamp'].max()}")
    
    return df


def load_item_properties():
    """Charger et fusionner les fichiers de propriétés des items"""
    print("\n📥 Chargement des propriétés des items...")
    
    part1_file = DATA_RAW_DIR / "item_properties_part1.csv"
    part2_file = DATA_RAW_DIR / "item_properties_part2.csv"
    
    dfs = []
    
    if part1_file.exists():
        df1 = pd.read_csv(part1_file)
        dfs.append(df1)
        print(f"  ✓ Part 1: {len(df1):,} lignes")
    
    if part2_file.exists():
        df2 = pd.read_csv(part2_file)
        dfs.append(df2)
        print(f"  ✓ Part 2: {len(df2):,} lignes")
    
    if not dfs:
        print("  ❌ Aucun fichier de propriétés trouvé")
        return None
    
    # Fusionner les parties
    df = pd.concat(dfs, ignore_index=True)
    print(f"  ✓ Total: {len(df):,} propriétés")
    print(f"  📋 Colonnes: {list(df.columns)}")
    
    return df


def load_category_tree():
    """Charger l'arborescence des catégories"""
    print("\n📥 Chargement de category_tree.csv...")
    
    category_file = DATA_RAW_DIR / "category_tree.csv"
    if not category_file.exists():
        print(f"  ❌ Fichier non trouvé")
        return None
    
    df = pd.read_csv(category_file)
    print(f"  ✓ {len(df):,} catégories chargées")
    print(f"  📋 Colonnes: {list(df.columns)}")
    
    return df


def analyze_events(df_events):
    """Analyser les événements"""
    print("\n📊 ANALYSE DES ÉVÉNEMENTS")
    print("=" * 60)
    
    if df_events is None or df_events.empty:
        print("  ❌ Pas de données à analyser")
        return
    
    # Statistiques par type d'événement
    if 'event' in df_events.columns:
        print("\n📈 Distribution des événements:")
        event_counts = df_events['event'].value_counts()
        for event_type, count in event_counts.items():
            percentage = (count / len(df_events)) * 100
            print(f"  • {event_type}: {count:,} ({percentage:.1f}%)")
    
    # Statistiques utilisateurs
    if 'visitorid' in df_events.columns:
        n_users = df_events['visitorid'].nunique()
        print(f"\n👥 Utilisateurs uniques: {n_users:,}")
        
        # Événements par utilisateur
        events_per_user = df_events.groupby('visitorid').size()
        print(f"  • Moyenne: {events_per_user.mean():.1f} événements/utilisateur")
        print(f"  • Médiane: {events_per_user.median():.0f} événements/utilisateur")
    
    # Statistiques produits
    if 'itemid' in df_events.columns:
        n_items = df_events['itemid'].nunique()
        print(f"\n📦 Produits uniques: {n_items:,}")
        
        # Top produits
        top_items = df_events['itemid'].value_counts().head(10)
        print(f"\n🏆 Top 10 produits les plus consultés:")
        for rank, (item_id, count) in enumerate(top_items.items(), 1):
            print(f"  {rank}. Item {item_id}: {count:,} vues")
    
    # Statistiques temporelles
    if 'date' in df_events.columns:
        print(f"\n📅 Période couverte: {df_events['date'].min()} à {df_events['date'].max()}")
        n_days = (df_events['date'].max() - df_events['date'].min()).days
        print(f"  • Durée: {n_days} jours")
        print(f"  • Événements par jour: {len(df_events) / n_days:,.0f}")


def create_users_table(df_events):
    """Créer une table utilisateurs à partir des événements"""
    print("\n🔨 Création de la table users...")
    
    if df_events is None or 'visitorid' not in df_events.columns:
        print("  ❌ Données insuffisantes")
        return None
    
    users = df_events.groupby('visitorid').agg({
        'timestamp': ['min', 'max', 'count']
    }).reset_index()
    
    users.columns = ['user_id', 'first_visit', 'last_visit', 'total_events']
    
    # Ajouter des segments basiques
    users['segment'] = pd.cut(
        users['total_events'],
        bins=[0, 5, 20, 100, float('inf')],
        labels=['New', 'Occasional', 'Regular', 'Premium']
    )
    
    print(f"  ✓ {len(users):,} utilisateurs créés")
    return users


def create_products_table(df_events, df_properties):
    """Créer une table produits"""
    print("\n🔨 Création de la table products...")
    
    if df_events is None or 'itemid' not in df_events.columns:
        print("  ❌ Données insuffisantes")
        return None
    
    # Statistiques de base par produit
    products = df_events.groupby('itemid').agg({
        'visitorid': 'count',
        'event': lambda x: (x == 'transaction').sum() if 'transaction' in x.values else 0
    }).reset_index()
    
    products.columns = ['product_id', 'view_count', 'purchase_count']
    
    # Ajouter les propriétés si disponibles
    if df_properties is not None and 'itemid' in df_properties.columns:
        # Pivot des propriétés (simplification)
        props_pivot = df_properties.pivot_table(
            index='itemid',
            columns='property',
            values='value',
            aggfunc='first'
        ).reset_index()
        
        products = products.merge(props_pivot, left_on='product_id', right_on='itemid', how='left')
    
    print(f"  ✓ {len(products):,} produits créés")
    return products


def create_sessions_table(df_events):
    """Créer une table de sessions"""
    print("\n🔨 Création de la table sessions...")
    
    if df_events is None:
        print("  ❌ Données insuffisantes")
        return None
    
    # Grouper par utilisateur et date pour créer des sessions
    sessions = df_events.groupby(['visitorid', 'date']).agg({
        'timestamp': ['min', 'max', 'count'],
        'itemid': 'nunique'
    }).reset_index()
    
    sessions.columns = ['user_id', 'session_date', 'session_start', 'session_end', 'events_count', 'unique_items']
    
    # Ajouter un ID de session
    sessions['session_id'] = range(1, len(sessions) + 1)
    
    print(f"  ✓ {len(sessions):,} sessions créées")
    return sessions


def create_transactions_table(df_events):
    """Créer une table de transactions"""
    print("\n🔨 Création de la table transactions...")
    
    if df_events is None or 'event' not in df_events.columns:
        print("  ❌ Données insuffisantes")
        return None
    
    # Filtrer les événements de type 'transaction'
    transactions = df_events[df_events['event'] == 'transaction'].copy()
    
    if transactions.empty:
        print("  ⚠️  Aucune transaction trouvée dans les données")
        return None
    
    transactions['transaction_id'] = range(1, len(transactions) + 1)
    transactions = transactions.rename(columns={
        'visitorid': 'user_id',
        'itemid': 'product_id',
        'timestamp': 'transaction_date'
    })
    
    # Générer des montants fictifs (le dataset n'a pas de prix)
    np.random.seed(42)
    transactions['amount'] = np.random.uniform(10, 500, len(transactions)).round(2)
    
    print(f"  ✓ {len(transactions):,} transactions créées")
    print(f"  💰 CA total (simulé): {transactions['amount'].sum():,.2f}€")
    
    return transactions


def save_cleaned_data(users, products, sessions, transactions):
    """Sauvegarder les données nettoyées"""
    print("\n💾 Sauvegarde des données nettoyées...")
    
    DATA_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    
    datasets = {
        'users': users,
        'products': products,
        'sessions': sessions,
        'transactions': transactions
    }
    
    for name, df in datasets.items():
        if df is not None:
            filepath = DATA_CLEAN_DIR / f"{name}.csv"
            df.to_csv(filepath, index=False)
            print(f"  ✓ {name}.csv ({len(df):,} lignes)")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  PREPROCESSING DATASET RETAILROCKET")
    print("=" * 60)
    
    # Charger les données brutes
    df_events = load_events()
    df_properties = load_item_properties()
    df_categories = load_category_tree()
    
    if df_events is None:
        print("\n❌ Impossible de continuer sans le fichier events.csv")
        return 1
    
    # Analyser les données
    analyze_events(df_events)
    
    # Créer les tables nettoyées
    users = create_users_table(df_events)
    products = create_products_table(df_events, df_properties)
    sessions = create_sessions_table(df_events)
    transactions = create_transactions_table(df_events)
    
    # Sauvegarder
    save_cleaned_data(users, products, sessions, transactions)
    
    print("\n" + "=" * 60)
    print("✨ PREPROCESSING TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print(f"\n📂 Données disponibles dans: {DATA_CLEAN_DIR}")
    print("\n🔜 Prochaine étape:")
    print("   python scripts/setup_db.py")
    print("   Puis charger les données nettoyées dans PostgreSQL")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
