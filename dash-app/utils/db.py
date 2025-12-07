"""
Utilitaires pour la connexion à la base de données
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/ecommerce_db')


def get_engine():
    """Créer et retourner un moteur SQLAlchemy"""
    return create_engine(DATABASE_URL)


def get_session():
    """Créer et retourner une session de base de données"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def execute_query(query, params=None):
    """
    Exécuter une requête SQL et retourner les résultats
    
    Args:
        query (str): Requête SQL à exécuter
        params (dict): Paramètres de la requête
    
    Returns:
        pandas.DataFrame: Résultats de la requête
    """
    import pandas as pd
    engine = get_engine()
    return pd.read_sql(query, engine, params=params)
