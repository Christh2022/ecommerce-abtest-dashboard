"""
Script de chargement des données RetailRocket nettoyées dans PostgreSQL
"""

import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATA_CLEAN_DIR = PROJECT_ROOT / "data" / "clean"

# Configuration de la base de données
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/ecommerce_db')


def get_engine():
    """Créer une connexion à la base de données"""
    try:
        engine = create_engine(DATABASE_URL)
        # Tester la connexion
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connexion à la base de données établie")
        return engine
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("\n💡 Assurez-vous que PostgreSQL est démarré:")
        print("   docker-compose up -d postgres")
        sys.exit(1)


def load_csv_file(filename):
    """Charger un fichier CSV"""
    filepath = DATA_CLEAN_DIR / filename
    
    if not filepath.exists():
        print(f"  ⚠️  Fichier non trouvé: {filename}")
        return None
    
    try:
        df = pd.read_csv(filepath)
        print(f"  ✓ {filename}: {len(df):,} lignes chargées")
        return df
    except Exception as e:
        print(f"  ❌ Erreur lors du chargement de {filename}: {e}")
        return None


def truncate_tables(engine, tables):
    """Vider les tables existantes"""
    print("\n🗑️  Nettoyage des tables existantes...")
    
    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
                conn.commit()
                print(f"  ✓ Table {table} vidée")
            except Exception as e:
                print(f"  ⚠️  Impossible de vider {table}: {e}")


def load_users(df, engine):
    """Charger les données utilisateurs"""
    if df is None:
        return
    
    print("\n👥 Chargement des utilisateurs...")
    
    # Adapter les colonnes au schéma de la base
    df_users = pd.DataFrame({
        'user_id': df['user_id'],
        'email': df['user_id'].apply(lambda x: f'user{x}@retailrocket.com'),
        'created_at': df['first_visit'],
        'country': 'Unknown',  # Non disponible dans le dataset
        'segment': df['segment']
    })
    
    try:
        df_users.to_sql('users', engine, if_exists='append', index=False)
        print(f"  ✓ {len(df_users):,} utilisateurs chargés")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def load_products(df, engine):
    """Charger les données produits"""
    if df is None:
        return
    
    print("\n📦 Chargement des produits...")
    
    # Adapter les colonnes au schéma de la base
    df_products = pd.DataFrame({
        'product_id': df['product_id'],
        'product_name': df['product_id'].apply(lambda x: f'Product {x}'),
        'category': 'General',  # Simplification
        'price': df.get('price', pd.Series([50.0] * len(df))),  # Prix par défaut si absent
        'stock': df.get('view_count', 100)  # Utiliser les vues comme proxy du stock
    })
    
    # Limiter aux 100k premiers produits pour éviter les problèmes de mémoire
    if len(df_products) > 100000:
        print(f"  ⚠️  Limitation à 100,000 produits (sur {len(df_products):,})")
        df_products = df_products.head(100000)
    
    try:
        df_products.to_sql('products', engine, if_exists='append', index=False)
        print(f"  ✓ {len(df_products):,} produits chargés")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def load_sessions(df, engine):
    """Charger les données de sessions"""
    if df is None:
        return
    
    print("\n🌐 Chargement des sessions...")
    
    # Adapter les colonnes au schéma de la base
    df_sessions = pd.DataFrame({
        'session_id': df['session_id'],
        'user_id': df['user_id'],
        'session_start': df['session_start'],
        'session_end': df.get('session_end'),
        'pages_viewed': df.get('events_count', 0),
        'device_type': 'Desktop',  # Non disponible dans le dataset
        'browser': 'Chrome'  # Non disponible dans le dataset
    })
    
    try:
        df_sessions.to_sql('sessions', engine, if_exists='append', index=False)
        print(f"  ✓ {len(df_sessions):,} sessions chargées")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def load_transactions(df, engine):
    """Charger les données de transactions"""
    if df is None:
        return
    
    print("\n💳 Chargement des transactions...")
    
    # Adapter les colonnes au schéma de la base
    df_transactions = pd.DataFrame({
        'transaction_id': df['transaction_id'],
        'user_id': df['user_id'],
        'session_id': df.get('session_id'),
        'transaction_date': df['transaction_date'],
        'total_amount': df['amount'],
        'payment_method': 'Credit Card',
        'status': 'completed'
    })
    
    try:
        df_transactions.to_sql('transactions', engine, if_exists='append', index=False)
        print(f"  ✓ {len(df_transactions):,} transactions chargées")
        print(f"  💰 CA total: {df_transactions['total_amount'].sum():,.2f}€")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def load_transaction_items(df_transactions, engine):
    """Créer les items de transaction"""
    if df_transactions is None:
        return
    
    print("\n🛒 Création des items de transaction...")
    
    # Créer un item par transaction (simplification)
    df_items = pd.DataFrame({
        'transaction_id': df_transactions['transaction_id'],
        'product_id': df_transactions['product_id'],
        'quantity': 1,
        'unit_price': df_transactions['amount']
    })
    
    df_items['item_id'] = range(1, len(df_items) + 1)
    
    try:
        df_items.to_sql('transaction_items', engine, if_exists='append', index=False)
        print(f"  ✓ {len(df_items):,} items chargés")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def verify_data(engine):
    """Vérifier les données chargées"""
    print("\n🔍 Vérification des données...")
    
    tables = ['users', 'products', 'sessions', 'transactions', 'transaction_items']
    
    with engine.connect() as conn:
        for table in tables:
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  ✓ {table}: {count:,} enregistrements")
            except Exception as e:
                print(f"  ❌ {table}: Erreur - {e}")


def create_indexes(engine):
    """Créer des index pour optimiser les performances"""
    print("\n⚡ Création des index...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_segment ON users(segment)",
        "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_start)",
        "CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)",
        "CREATE INDEX IF NOT EXISTS idx_transaction_items_trans_id ON transaction_items(transaction_id)",
        "CREATE INDEX IF NOT EXISTS idx_transaction_items_product_id ON transaction_items(product_id)",
    ]
    
    with engine.connect() as conn:
        for idx_sql in indexes:
            try:
                conn.execute(text(idx_sql))
                conn.commit()
                print(f"  ✓ Index créé")
            except Exception as e:
                print(f"  ⚠️  Erreur: {e}")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  CHARGEMENT DES DONNÉES RETAILROCKET EN BASE")
    print("=" * 60)
    
    # Connexion à la base
    engine = get_engine()
    
    # Charger les fichiers CSV
    print("\n📥 Chargement des fichiers CSV...")
    users_df = load_csv_file('users.csv')
    products_df = load_csv_file('products.csv')
    sessions_df = load_csv_file('sessions.csv')
    transactions_df = load_csv_file('transactions.csv')
    
    if not any([users_df is not None, transactions_df is not None]):
        print("\n❌ Aucune donnée à charger")
        print("💡 Exécutez d'abord: python scripts/preprocess_retailrocket.py")
        return 1
    
    # Vider les tables existantes
    truncate_tables(engine, [
        'transaction_items', 'transactions', 'sessions', 
        'products', 'users'
    ])
    
    # Charger les données
    load_users(users_df, engine)
    load_products(products_df, engine)
    load_sessions(sessions_df, engine)
    load_transactions(transactions_df, engine)
    load_transaction_items(transactions_df, engine)
    
    # Vérifier les données
    verify_data(engine)
    
    # Créer les index
    create_indexes(engine)
    
    print("\n" + "=" * 60)
    print("✨ CHARGEMENT TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print("\n🎉 Les données RetailRocket sont prêtes à être analysées!")
    print("\n🔜 Prochaine étape:")
    print("   Démarrer le dashboard: docker-compose up -d dash-app")
    print("   Accéder à: http://localhost:8050")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
