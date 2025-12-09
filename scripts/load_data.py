"""
Script de chargement des données de test
Génère et charge des données fictives dans la base de données
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/ecommerce_db')
NUM_USERS = 1000
NUM_PRODUCTS = 100
NUM_TRANSACTIONS = 5000


def generate_users(n=NUM_USERS):
    """Générer des utilisateurs fictifs"""
    print(f"📝 Génération de {n} utilisateurs...")
    
    countries = ['France', 'USA', 'UK', 'Germany', 'Spain', 'Italy', 'Canada']
    segments = ['Premium', 'Regular', 'Occasional', 'New']
    
    users = pd.DataFrame({
        'user_id': range(1, n + 1),
        'email': [f'user{i}@example.com' for i in range(1, n + 1)],
        'created_at': [
            datetime.now() - timedelta(days=np.random.randint(1, 365))
            for _ in range(n)
        ],
        'country': np.random.choice(countries, n),
        'segment': np.random.choice(segments, n, p=[0.1, 0.4, 0.3, 0.2])
    })
    
    return users


def generate_products(n=NUM_PRODUCTS):
    """Générer des produits fictifs"""
    print(f"📦 Génération de {n} produits...")
    
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
    
    products = pd.DataFrame({
        'product_id': range(1, n + 1),
        'product_name': [f'Product {i}' for i in range(1, n + 1)],
        'category': np.random.choice(categories, n),
        'price': np.random.uniform(10, 500, n).round(2),
        'stock': np.random.randint(0, 100, n)
    })
    
    return products


def generate_sessions(users_df, n=NUM_TRANSACTIONS):
    """Générer des sessions utilisateur"""
    print(f"🌐 Génération de {n} sessions...")
    
    devices = ['Desktop', 'Mobile', 'Tablet']
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
    
    sessions = pd.DataFrame({
        'session_id': range(1, n + 1),
        'user_id': np.random.choice(users_df['user_id'], n),
        'session_start': [
            datetime.now() - timedelta(days=np.random.randint(1, 90), 
                                     hours=np.random.randint(0, 24))
            for _ in range(n)
        ],
        'pages_viewed': np.random.randint(1, 20, n),
        'device_type': np.random.choice(devices, n, p=[0.5, 0.4, 0.1]),
        'browser': np.random.choice(browsers, n)
    })
    
    # Ajouter session_end (80% des sessions se terminent)
    sessions['session_end'] = sessions.apply(
        lambda row: row['session_start'] + timedelta(minutes=np.random.randint(5, 120))
        if np.random.random() > 0.2 else None,
        axis=1
    )
    
    return sessions


def generate_transactions(sessions_df, n=NUM_TRANSACTIONS):
    """Générer des transactions"""
    print(f"💳 Génération de {n} transactions...")
    
    # Seulement 30% des sessions aboutissent à une transaction
    n_transactions = int(n * 0.3)
    selected_sessions = sessions_df.sample(n_transactions)
    
    payment_methods = ['Credit Card', 'PayPal', 'Debit Card', 'Bank Transfer']
    statuses = ['completed', 'pending', 'cancelled']
    
    transactions = pd.DataFrame({
        'transaction_id': range(1, n_transactions + 1),
        'user_id': selected_sessions['user_id'].values,
        'session_id': selected_sessions['session_id'].values,
        'transaction_date': selected_sessions['session_start'].values,
        'total_amount': np.random.uniform(20, 1000, n_transactions).round(2),
        'payment_method': np.random.choice(payment_methods, n_transactions),
        'status': np.random.choice(statuses, n_transactions, p=[0.85, 0.10, 0.05])
    })
    
    return transactions


def generate_transaction_items(transactions_df, products_df):
    """Générer les items de transaction"""
    print(f"🛒 Génération des items de transaction...")
    
    items = []
    item_id = 1
    
    for _, transaction in transactions_df.iterrows():
        # Nombre d'items par transaction (1-5)
        n_items = np.random.randint(1, 6)
        selected_products = products_df.sample(n_items)
        
        for _, product in selected_products.iterrows():
            items.append({
                'item_id': item_id,
                'transaction_id': transaction['transaction_id'],
                'product_id': product['product_id'],
                'quantity': np.random.randint(1, 4),
                'unit_price': product['price']
            })
            item_id += 1
    
    return pd.DataFrame(items)


def generate_ab_tests():
    """Générer des tests A/B"""
    print(f"🧪 Génération des tests A/B...")
    
    tests = pd.DataFrame({
        'test_id': [1, 2, 3],
        'test_name': [
            'Homepage Layout Test',
            'Checkout Button Color',
            'Product Page Description'
        ],
        'start_date': [
            datetime.now() - timedelta(days=60),
            datetime.now() - timedelta(days=45),
            datetime.now() - timedelta(days=30)
        ],
        'end_date': [
            datetime.now() - timedelta(days=30),
            None,
            None
        ],
        'variant_a_name': ['Original', 'Blue Button', 'Short Description'],
        'variant_b_name': ['New Layout', 'Green Button', 'Detailed Description'],
        'description': [
            'Testing new homepage layout with featured products',
            'Testing checkout button color impact on conversion',
            'Testing detailed vs short product descriptions'
        ],
        'is_active': [False, True, True]
    })
    
    return tests


def generate_ab_test_assignments(users_df, tests_df):
    """Générer les assignations de tests A/B"""
    print(f"🎲 Génération des assignations A/B...")
    
    assignments = []
    assignment_id = 1
    
    for _, test in tests_df.iterrows():
        # Assigner 50% des utilisateurs à ce test
        n_users = len(users_df) // 2
        selected_users = users_df.sample(n_users)
        
        for _, user in selected_users.iterrows():
            assignments.append({
                'assignment_id': assignment_id,
                'test_id': test['test_id'],
                'user_id': user['user_id'],
                'variant': np.random.choice(['A', 'B']),
                'assigned_at': test['start_date'] + timedelta(days=np.random.randint(0, 5))
            })
            assignment_id += 1
    
    return pd.DataFrame(assignments)


def generate_ab_test_results(assignments_df, transactions_df):
    """Générer les résultats de tests A/B"""
    print(f"📊 Génération des résultats A/B...")
    
    results = []
    result_id = 1
    
    for _, assignment in assignments_df.iterrows():
        # 25% des assignations aboutissent à une conversion
        if np.random.random() < 0.25:
            # Trouver une transaction pour cet utilisateur
            user_transactions = transactions_df[
                transactions_df['user_id'] == assignment['user_id']
            ]
            
            if not user_transactions.empty:
                transaction = user_transactions.sample(1).iloc[0]
                
                results.append({
                    'result_id': result_id,
                    'test_id': assignment['test_id'],
                    'user_id': assignment['user_id'],
                    'variant': assignment['variant'],
                    'converted': True,
                    'conversion_value': transaction['total_amount'],
                    'recorded_at': transaction['transaction_date']
                })
                result_id += 1
    
    return pd.DataFrame(results)


def load_to_database(dataframes, engine):
    """Charger les données dans la base de données"""
    print("\n📤 Chargement des données dans la base de données...")
    
    table_names = [
        'users', 'products', 'sessions', 'transactions',
        'transaction_items', 'ab_tests', 'ab_test_assignments', 'ab_test_results'
    ]
    
    for df, table_name in zip(dataframes, table_names):
        print(f"  → Chargement de {len(df)} enregistrements dans '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"    ✓ {table_name} chargée")
    
    print("\n✅ Toutes les données ont été chargées avec succès!")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  Génération et chargement des données de test")
    print("=" * 60)
    print()
    
    # Générer les données
    users_df = generate_users()
    products_df = generate_products()
    sessions_df = generate_sessions(users_df)
    transactions_df = generate_transactions(sessions_df)
    transaction_items_df = generate_transaction_items(transactions_df, products_df)
    ab_tests_df = generate_ab_tests()
    ab_test_assignments_df = generate_ab_test_assignments(users_df, ab_tests_df)
    ab_test_results_df = generate_ab_test_results(ab_test_assignments_df, transactions_df)
    
    # Se connecter à la base de données
    print("\n🔌 Connexion à la base de données...")
    engine = create_engine(DATABASE_URL)
    
    # Charger les données
    dataframes = [
        users_df, products_df, sessions_df, transactions_df,
        transaction_items_df, ab_tests_df, ab_test_assignments_df, ab_test_results_df
    ]
    
    load_to_database(dataframes, engine)
    
    print("\n" + "=" * 60)
    print("✨ Processus terminé avec succès!")
    print("=" * 60)
    print(f"\n📊 Statistiques:")
    print(f"  - {len(users_df)} utilisateurs")
    print(f"  - {len(products_df)} produits")
    print(f"  - {len(sessions_df)} sessions")
    print(f"  - {len(transactions_df)} transactions")
    print(f"  - {len(transaction_items_df)} items de transaction")
    print(f"  - {len(ab_tests_df)} tests A/B")
    print(f"  - {len(ab_test_assignments_df)} assignations A/B")
    print(f"  - {len(ab_test_results_df)} résultats A/B")


if __name__ == "__main__":
    main()
