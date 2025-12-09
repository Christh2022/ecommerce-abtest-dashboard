"""
Script d'initialisation de la base de données PostgreSQL
Crée les tables nécessaires pour le projet E-commerce Dashboard
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/ecommerce_db')

Base = declarative_base()


# Définition des modèles
class User(Base):
    """Modèle pour les utilisateurs"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    country = Column(String(100))
    segment = Column(String(50))


class Session(Base):
    """Modèle pour les sessions utilisateur"""
    __tablename__ = 'sessions'
    
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_start = Column(DateTime, nullable=False)
    session_end = Column(DateTime)
    pages_viewed = Column(Integer, default=0)
    device_type = Column(String(50))
    browser = Column(String(100))


class Product(Base):
    """Modèle pour les produits"""
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)


class Transaction(Base):
    """Modèle pour les transactions"""
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(Integer)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50))
    status = Column(String(50), default='completed')


class TransactionItem(Base):
    """Modèle pour les items de transaction"""
    __tablename__ = 'transaction_items'
    
    item_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)


class ABTest(Base):
    """Modèle pour les tests A/B"""
    __tablename__ = 'ab_tests'
    
    test_id = Column(Integer, primary_key=True)
    test_name = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    variant_a_name = Column(String(100))
    variant_b_name = Column(String(100))
    description = Column(Text)
    is_active = Column(Boolean, default=True)


class ABTestAssignment(Base):
    """Modèle pour les assignations de tests A/B"""
    __tablename__ = 'ab_test_assignments'
    
    assignment_id = Column(Integer, primary_key=True)
    test_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    variant = Column(String(10), nullable=False)  # 'A' or 'B'
    assigned_at = Column(DateTime, default=datetime.utcnow)


class ABTestResult(Base):
    """Modèle pour les résultats de tests A/B"""
    __tablename__ = 'ab_test_results'
    
    result_id = Column(Integer, primary_key=True)
    test_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    variant = Column(String(10), nullable=False)
    converted = Column(Boolean, default=False)
    conversion_value = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)


def create_database():
    """Créer toutes les tables dans la base de données"""
    try:
        print("🔌 Connexion à la base de données...")
        engine = create_engine(DATABASE_URL)
        
        print("📊 Création des tables...")
        Base.metadata.create_all(engine)
        
        print("✅ Tables créées avec succès!")
        print("\nTables créées:")
        for table in Base.metadata.tables.keys():
            print(f"  - {table}")
        
        return engine
    
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        sys.exit(1)


def verify_tables(engine):
    """Vérifier que les tables ont été créées"""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n🔍 Vérification des tables...")
    expected_tables = [
        'users', 'sessions', 'products', 'transactions',
        'transaction_items', 'ab_tests', 'ab_test_assignments', 'ab_test_results'
    ]
    
    for table in expected_tables:
        if table in tables:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} - MANQUANTE")
    
    print(f"\n📈 Total: {len(tables)} tables créées")


if __name__ == "__main__":
    print("=" * 60)
    print("  Initialisation de la base de données E-commerce")
    print("=" * 60)
    print()
    
    engine = create_database()
    verify_tables(engine)
    
    print("\n" + "=" * 60)
    print("✨ Initialisation terminée avec succès!")
    print("=" * 60)
