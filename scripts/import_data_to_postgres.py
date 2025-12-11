#!/usr/bin/env python3
"""
Data Import Script for PostgreSQL
Imports CSV data from data/clean/ into PostgreSQL database
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ecommerce_db'),
    'user': os.getenv('DB_USER', 'dashuser'),
    'password': os.getenv('DB_PASSWORD', 'dashpass')
}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'clean')


def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("✅ Database connection established")
        return conn
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        sys.exit(1)


def import_ab_test_simulations(conn):
    """Import A/B test simulation data"""
    try:
        logger.info("📊 Importing A/B test simulations...")
        
        # Read CSV files
        simulations_file = os.path.join(DATA_DIR, 'ab_test_simulation.csv')
        results_file = os.path.join(DATA_DIR, 'ab_test_simulation_results.csv')
        
        if not os.path.exists(simulations_file) or not os.path.exists(results_file):
            logger.warning("⚠️  A/B test CSV files not found, skipping...")
            return
        
        # Read simulations data
        df_sim = pd.read_csv(simulations_file)
        df_results = pd.read_csv(results_file)
        
        cursor = conn.cursor()
        
        # Import scenarios (unique from results)
        scenarios = df_results[['scenario_id', 'scenario_name', 'description', 'hypothesis']].drop_duplicates()
        
        for _, row in scenarios.iterrows():
            cursor.execute("""
                INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, hypothesis, status)
                VALUES (%s, %s, %s, %s, 'active')
                ON CONFLICT (scenario_id) DO UPDATE
                SET scenario_name = EXCLUDED.scenario_name,
                    description = EXCLUDED.description,
                    hypothesis = EXCLUDED.hypothesis
            """, (row['scenario_id'], row['scenario_name'], row['description'], row['hypothesis']))
        
        logger.info(f"✅ Imported {len(scenarios)} A/B test scenarios")
        
        # Import daily results
        df_sim['date'] = pd.to_datetime(df_sim['date']).dt.date
        
        records = []
        for _, row in df_sim.iterrows():
            records.append((
                row['scenario_id'],
                row['date'],
                row['variant'],
                row['visitors'],
                row['conversions'],
                row['conversion_rate'],
                row['revenue'],
                row.get('avg_order_value', 0),
                row.get('statistical_significance', 0)
            ))
        
        execute_values(cursor, """
            INSERT INTO ab_test_results 
            (scenario_id, date, variant, visitors, conversions, conversion_rate, 
             revenue, avg_order_value, statistical_significance)
            VALUES %s
            ON CONFLICT (scenario_id, date, variant) DO UPDATE
            SET visitors = EXCLUDED.visitors,
                conversions = EXCLUDED.conversions,
                conversion_rate = EXCLUDED.conversion_rate,
                revenue = EXCLUDED.revenue
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} A/B test result records")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import A/B test data: {e}")
        raise


def import_user_behavior(conn):
    """Import user behavior data from main dataset"""
    try:
        logger.info("👥 Importing user behavior data...")
        
        main_file = os.path.join(DATA_DIR, 'ecommerce_behavior_data_cleaned.csv')
        
        if not os.path.exists(main_file):
            logger.warning("⚠️  Main dataset not found, skipping...")
            return
        
        # Read in chunks to handle large file
        chunk_size = 50000
        total_imported = 0
        
        cursor = conn.cursor()
        
        for chunk in pd.read_csv(main_file, chunksize=chunk_size):
            chunk['event_time'] = pd.to_datetime(chunk['event_time'])
            chunk['date'] = chunk['event_time'].dt.date
            
            # Aggregate by user and date
            user_daily = chunk.groupby(['user_id', 'date']).agg({
                'event_type': 'count',  # page views
                'price': 'sum',  # revenue
                'event_time': lambda x: (x.max() - x.min()).total_seconds() / 60  # session duration
            }).reset_index()
            
            user_daily.columns = ['user_id', 'session_date', 'page_views', 'revenue', 'session_duration']
            user_daily['converted'] = user_daily['revenue'] > 0
            
            records = []
            for _, row in user_daily.iterrows():
                records.append((
                    str(row['user_id']),
                    row['session_date'],
                    'desktop',  # default, can be enhanced
                    'unknown',
                    'unknown',
                    'unknown',
                    int(row['page_views']),
                    int(row['session_duration']),
                    0,
                    row['converted'],
                    float(row['revenue'])
                ))
            
            execute_values(cursor, """
                INSERT INTO user_behavior 
                (user_id, session_date, device_type, browser, country, city,
                 page_views, session_duration, bounce_rate, converted, revenue)
                VALUES %s
            """, records)
            
            total_imported += len(records)
            logger.info(f"  📦 Imported {total_imported} user behavior records...")
            
            # Commit every chunk
            conn.commit()
            
            # Limit for demo purposes
            if total_imported >= 100000:
                logger.info("  ⏹️  Reached import limit (100k records)")
                break
        
        logger.info(f"✅ Total user behavior records imported: {total_imported}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import user behavior: {e}")
        raise


def import_daily_metrics(conn):
    """Calculate and import daily metrics"""
    try:
        logger.info("📈 Calculating daily metrics...")
        
        cursor = conn.cursor()
        
        # Calculate metrics from user_behavior table
        cursor.execute("""
            INSERT INTO daily_metrics 
            (date, total_users, total_sessions, total_revenue, total_conversions, 
             conversion_rate, avg_order_value, avg_session_duration)
            SELECT 
                session_date as date,
                COUNT(DISTINCT user_id) as total_users,
                COUNT(*) as total_sessions,
                SUM(revenue) as total_revenue,
                SUM(CASE WHEN converted THEN 1 ELSE 0 END) as total_conversions,
                ROUND(
                    SUM(CASE WHEN converted THEN 1 ELSE 0 END)::DECIMAL / 
                    NULLIF(COUNT(*), 0) * 100, 
                    4
                ) as conversion_rate,
                ROUND(
                    SUM(revenue) / 
                    NULLIF(SUM(CASE WHEN converted THEN 1 ELSE 0 END), 0), 
                    2
                ) as avg_order_value,
                ROUND(AVG(session_duration), 2) as avg_session_duration
            FROM user_behavior
            GROUP BY session_date
            ON CONFLICT (date) DO UPDATE
            SET total_users = EXCLUDED.total_users,
                total_sessions = EXCLUDED.total_sessions,
                total_revenue = EXCLUDED.total_revenue,
                total_conversions = EXCLUDED.total_conversions,
                conversion_rate = EXCLUDED.conversion_rate,
                avg_order_value = EXCLUDED.avg_order_value,
                avg_session_duration = EXCLUDED.avg_session_duration
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM daily_metrics")
        count = cursor.fetchone()[0]
        logger.info(f"✅ Daily metrics calculated: {count} days")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to calculate daily metrics: {e}")
        raise


def verify_import(conn):
    """Verify imported data"""
    try:
        logger.info("\n🔍 Verifying imported data...")
        
        cursor = conn.cursor()
        
        tables = [
            'ab_test_scenarios',
            'ab_test_results',
            'user_behavior',
            'daily_metrics'
        ]
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"  📊 {table}: {count:,} rows")
        
        logger.info("\n✅ Data verification completed")
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")


def main():
    """Main import process"""
    logger.info("="*60)
    logger.info("🚀 Starting PostgreSQL Data Import")
    logger.info("="*60)
    
    conn = get_db_connection()
    
    try:
        # Import data in order
        import_ab_test_simulations(conn)
        import_user_behavior(conn)
        import_daily_metrics(conn)
        
        # Verify
        verify_import(conn)
        
        logger.info("\n" + "="*60)
        logger.info("✅ Data import completed successfully!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"\n❌ Import process failed: {e}")
        sys.exit(1)
    finally:
        conn.close()
        logger.info("🔒 Database connection closed")


if __name__ == "__main__":
    main()
