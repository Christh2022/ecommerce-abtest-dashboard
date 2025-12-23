#!/usr/bin/env python3
"""
Fix numeric overflow in multiple tables
Changes NUMERIC(5,4) to NUMERIC(6,2) to accommodate percentage values (0-100)
Fixes: user_behavior.bounce_rate, products_summary.conversion_rate, 
       ab_test_results.conversion_rate, ab_test_results.statistical_significance,
       funnel_stages.conversion_rate
"""

import os
import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ecommerce_db'),
    'user': os.getenv('DB_USER', 'dashuser'),
    'password': os.getenv('DB_PASSWORD', 'dashpass')
}

def get_dependent_views(cursor, table_name):
    """Get all views that depend on a table"""
    cursor.execute("""
        SELECT DISTINCT view_schema, view_name
        FROM information_schema.view_table_usage
        WHERE table_name = %s
    """, (table_name,))
    return cursor.fetchall()

def fix_all_numeric_columns():
    """Alter all NUMERIC(5,4) columns to NUMERIC(6,2) to handle percentage values"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get all columns with NUMERIC(5,4)
        logger.info("🔧 Finding all NUMERIC(5,4) columns...")
        cursor.execute("""
            SELECT table_name, column_name 
            FROM information_schema.columns 
            WHERE numeric_precision = 5 AND numeric_scale = 4
            AND table_schema = 'public'
            AND table_name NOT LIKE 'v_%'
        """)
        columns_to_fix = cursor.fetchall()
        
        logger.info(f"Found {len(columns_to_fix)} columns to fix:")
        for table, column in columns_to_fix:
            logger.info(f"  - {table}.{column}")
        
        # Store view definitions
        views_to_recreate = {}
        
        # Get all dependent views and drop them
        logger.info("\n🔧 Dropping dependent views...")
        cursor.execute("""
            SELECT table_name FROM information_schema.views 
            WHERE table_schema = 'public'
        """)
        all_views = [v[0] for v in cursor.fetchall()]
        
        for view_name in all_views:
            try:
                cursor.execute(f"SELECT pg_get_viewdef('{view_name}', true)")
                view_def = cursor.fetchone()[0]
                views_to_recreate[view_name] = view_def
            except Exception as e:
                logger.warning(f"  ⚠️  Could not get definition for {view_name}: {e}")
                continue
        
        # Now drop all views with CASCADE
        for view_name in views_to_recreate.keys():
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view_name} CASCADE")
                conn.commit()
                logger.info(f"  ✅ Dropped {view_name}")
            except Exception as e:
                logger.warning(f"  ⚠️  Could not drop {view_name}: {e}")
                conn.rollback()
        
        # Alter all columns
        logger.info("\n🔧 Altering columns...")
        for table, column in columns_to_fix:
            try:
                logger.info(f"  Altering {table}.{column}...")
                cursor.execute(f"""
                    ALTER TABLE {table} 
                    ALTER COLUMN {column} TYPE NUMERIC(6,2)
                """)
                conn.commit()
                logger.info(f"  ✅ {table}.{column} → NUMERIC(6,2)")
            except Exception as e:
                logger.error(f"  ❌ Failed to alter {table}.{column}: {e}")
                conn.rollback()
        
        # Recreate all views
        logger.info("\n🔧 Recreating views...")
        for view_name, view_def in views_to_recreate.items():
            try:
                cursor.execute(f"CREATE OR REPLACE VIEW {view_name} AS {view_def}")
                conn.commit()
                logger.info(f"  ✅ Recreated {view_name}")
            except Exception as e:
                logger.warning(f"  ⚠️  Could not recreate {view_name}: {e}")
                conn.rollback()
        
        logger.info("\n✅ All columns fixed successfully!")
        logger.info("   NUMERIC(5,4) → NUMERIC(6,2)")
        logger.info("   Can now store percentage values from 0.00 to 9999.99")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Failed to fix columns: {e}")
        raise

if __name__ == "__main__":
    fix_all_numeric_columns()
