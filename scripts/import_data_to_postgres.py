#!/usr/bin/env python3
"""
KPI Data Import Script for PostgreSQL
Automatically imports CSV data from data/clean/ into PostgreSQL database
Imports: Daily Metrics, Products, Traffic, A/B Tests, Funnel data
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import logging
from pathlib import Path

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

DATA_DIR = Path(__file__).parent.parent / 'data' / 'clean'


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
        simulations_file = DATA_DIR / 'ab_test_simulation.csv'
        results_file = DATA_DIR / 'ab_test_simulation_results.csv'
        scenarios_file = DATA_DIR / 'ab_test_scenarios.csv'
        
        if not simulations_file.exists():
            logger.warning("⚠️  A/B test simulation CSV not found, skipping...")
            return
        
        cursor = conn.cursor()
        
        # Import scenarios from scenarios file or results file
        if scenarios_file.exists():
            df_scenarios = pd.read_csv(scenarios_file)
            for _, row in df_scenarios.iterrows():
                cursor.execute("""
                    INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, hypothesis, status)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (scenario_id) DO UPDATE
                    SET scenario_name = EXCLUDED.scenario_name,
                        description = EXCLUDED.description,
                        hypothesis = EXCLUDED.hypothesis,
                        status = EXCLUDED.status
                """, (
                    row['id'],  # Column is 'id' not 'scenario_id'
                    row['name'],  # Column is 'name' not 'scenario_name'
                    row.get('description', ''),
                    f"Expected lift: {row.get('expected_lift', 0)*100:.1f}% on {row.get('target_metric', 'conversion')}",
                    'active'
                ))
            logger.info(f"✅ Imported {len(df_scenarios)} A/B test scenarios from scenarios file")
        elif results_file.exists():
            df_results = pd.read_csv(results_file)
            scenarios = df_results[['scenario_id', 'scenario_name']].drop_duplicates()
            
            for _, row in scenarios.iterrows():
                cursor.execute("""
                    INSERT INTO ab_test_scenarios (scenario_id, scenario_name, status)
                    VALUES (%s, %s, 'active')
                    ON CONFLICT (scenario_id) DO UPDATE
                    SET scenario_name = EXCLUDED.scenario_name
                """, (row['scenario_id'], row['scenario_name']))
            logger.info(f"✅ Imported {len(scenarios)} A/B test scenarios from results file")
        
        
        # Import daily results - transform control/variant structure
        df_sim = pd.read_csv(simulations_file)
        df_sim['date'] = pd.to_datetime(df_sim['date']).dt.date
        
        records = []
        for _, row in df_sim.iterrows():
            # Skip rows with NaN values
            if pd.isna(row.get('control_users')) or pd.isna(row.get('variant_users')):
                continue
                
            # Control variant (A)
            control_conv_rate = row.get('control_view_to_purchase_pct', 0)
            control_revenue = row.get('control_revenue', 0)
            control_purchases = row.get('control_purchases', 0)
            control_users = row.get('control_users', 0)
            control_aov = control_revenue / control_purchases if control_purchases > 0 else 0
            
            records.append((
                row['scenario_id'],
                row['date'],
                'A',  # Control
                int(control_users),
                int(control_purchases),
                float(control_conv_rate),
                float(control_revenue),
                float(control_aov),
                0.0  # No significance for control
            ))
            
            # Variant (B)
            variant_conv_rate = row.get('variant_view_to_purchase_pct', 0)
            variant_revenue = row.get('variant_revenue', 0)
            variant_purchases = row.get('variant_purchases', 0)
            variant_users = row.get('variant_users', 0)
            variant_aov = variant_revenue / variant_purchases if variant_purchases > 0 else 0
            p_value = row.get('p_value', 1.0)
            significance = (1 - p_value) * 100 if p_value < 1 else 0
            
            records.append((
                row['scenario_id'],
                row['date'],
                'B',  # Variant
                int(variant_users),
                int(variant_purchases),
                float(variant_conv_rate),
                float(variant_revenue),
                float(variant_aov),
                float(significance)
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
                revenue = EXCLUDED.revenue,
                avg_order_value = EXCLUDED.avg_order_value,
                statistical_significance = EXCLUDED.statistical_significance
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} A/B test result records ({len(records)//2} days x 2 variants)")
        
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
    """Import daily metrics from CSV"""
    try:
        logger.info("📈 Importing daily metrics from CSV...")
        
        csv_file = DATA_DIR / 'daily_metrics.csv'
        
        if not csv_file.exists():
            logger.warning("⚠️  daily_metrics.csv not found, skipping...")
            return
        
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        cursor = conn.cursor()
        records = []
        
        for _, row in df.iterrows():
            # Conversion rate in CSV is percentage (e.g., 32.56), but DB expects decimal (0-100)
            # So we keep it as is since DECIMAL(5,4) can hold 0-9.9999
            # But cart_to_purchase_rate is actually in percentage already, so we use it directly
            conv_rate = float(row.get('cart_to_purchase_rate', 0))
            # If it's > 10, it's already in percentage format, just cap at 100
            if conv_rate > 100:
                conv_rate = 100.0
            
            records.append((
                row['date'],
                int(row['unique_users']),
                int(row['unique_sessions']),
                float(row.get('daily_revenue', 0)),
                int(row.get('transactions', 0)),
                conv_rate,
                float(row.get('avg_order_value', 0))
            ))
        
        execute_values(cursor, """
            INSERT INTO daily_metrics 
            (date, total_users, total_sessions, total_revenue, total_conversions, 
             conversion_rate, avg_order_value)
            VALUES %s
            ON CONFLICT (date) DO UPDATE
            SET total_users = EXCLUDED.total_users,
                total_sessions = EXCLUDED.total_sessions,
                total_revenue = EXCLUDED.total_revenue,
                total_conversions = EXCLUDED.total_conversions,
                conversion_rate = EXCLUDED.conversion_rate,
                avg_order_value = EXCLUDED.avg_order_value
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} daily metric records")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import daily metrics: {e}")
        raise


def import_products_summary(conn):
    """Import products summary from CSV"""
    try:
        logger.info("📦 Importing products summary...")
        
        csv_file = DATA_DIR / 'products_summary.csv'
        
        if not csv_file.exists():
            logger.warning("⚠️  products_summary.csv not found, skipping...")
            return
        
        df = pd.read_csv(csv_file)
        
        cursor = conn.cursor()
        records = []
        
        for _, row in df.iterrows():
            records.append((
                str(row['product_id']),
                row.get('product_name', f"Product {row['product_id']}"),
                row.get('category', 'Unknown'),
                int(row.get('total_views', 0)),
                int(row.get('total_purchases', 0)),
                float(row.get('total_revenue', 0)),
                float(row.get('avg_rating', 0)),
                float(row.get('conversion_rate', 0))
            ))
        
        execute_values(cursor, """
            INSERT INTO products_summary 
            (product_id, product_name, category, total_views, total_purchases,
             total_revenue, avg_rating, conversion_rate)
            VALUES %s
            ON CONFLICT (product_id) DO UPDATE
            SET total_views = EXCLUDED.total_views,
                total_purchases = EXCLUDED.total_purchases,
                total_revenue = EXCLUDED.total_revenue,
                avg_rating = EXCLUDED.avg_rating,
                conversion_rate = EXCLUDED.conversion_rate
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} product records")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import products: {e}")
        raise


def import_traffic_sources(conn):
    """Import traffic data from CSV"""
    try:
        logger.info("🚦 Importing traffic data...")
        
        csv_file = DATA_DIR / 'traffic_daily.csv'
        
        if not csv_file.exists():
            logger.warning("⚠️  traffic_daily.csv not found, skipping...")
            return
        
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        cursor = conn.cursor()
        records = []
        
        for _, row in df.iterrows():
            records.append((
                row['date'],
                'organic',  # default source
                'direct',   # default medium
                'none',     # default campaign
                int(row.get('unique_sessions', 0)),
                int(row.get('unique_users', 0)),
                int(row.get('transactions', 0)),
                float(row.get('daily_revenue', 0))
            ))
        
        execute_values(cursor, """
            INSERT INTO traffic_sources 
            (date, source, medium, campaign, sessions, users, conversions, revenue)
            VALUES %s
            ON CONFLICT (date, source, medium, campaign) DO UPDATE
            SET sessions = EXCLUDED.sessions,
                users = EXCLUDED.users,
                conversions = EXCLUDED.conversions,
                revenue = EXCLUDED.revenue
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} traffic records")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import traffic data: {e}")
        raise


def import_funnel_stages(conn):
    """Import funnel stages from CSV"""
    try:
        logger.info("🔄 Importing funnel data...")
        
        csv_file = DATA_DIR / 'daily_funnel.csv'
        
        if not csv_file.exists():
            logger.warning("⚠️  daily_funnel.csv not found, skipping...")
            return
        
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        cursor = conn.cursor()
        records = []
        
        # Create funnel stages from the data
        for _, row in df.iterrows():
            # View stage
            records.append((
                row['date'],
                'view',
                1,
                int(row.get('unique_viewers', 0)),
                int(row.get('unique_viewers', 0)) - int(row.get('unique_add_to_carts', 0)),
                100.0
            ))
            # Cart stage
            records.append((
                row['date'],
                'add_to_cart',
                2,
                int(row.get('unique_add_to_carts', 0)),
                int(row.get('unique_add_to_carts', 0)) - int(row.get('unique_purchasers', 0)),
                float(row.get('view_to_cart_rate', 0))
            ))
            # Purchase stage
            records.append((
                row['date'],
                'purchase',
                3,
                int(row.get('unique_purchasers', 0)),
                0,
                float(row.get('view_to_purchase_rate', 0))
            ))
        
        execute_values(cursor, """
            INSERT INTO funnel_stages 
            (date, stage_name, stage_order, visitors, drop_off, conversion_rate)
            VALUES %s
            ON CONFLICT (date, stage_name) DO UPDATE
            SET visitors = EXCLUDED.visitors,
                drop_off = EXCLUDED.drop_off,
                conversion_rate = EXCLUDED.conversion_rate
        """, records)
        
        conn.commit()
        logger.info(f"✅ Imported {len(records)} funnel stage records")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Failed to import funnel data: {e}")
        raise


def verify_import(conn):
    """Verify imported data"""
    try:
        logger.info("\n🔍 Verifying imported data...")
        
        cursor = conn.cursor()
        
        tables = [
            'daily_metrics',
            'products_summary',
            'traffic_sources',
            'funnel_stages',
            'ab_test_scenarios',
            'ab_test_results'
        ]
        
        logger.info("\n  📊 Row Counts:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️"
            logger.info(f"    {status} {table}: {count:,} rows")
        
        logger.info("\n✅ Data verification completed")
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")


def main():
    """Main import process"""
    logger.info("="*80)
    logger.info("🚀 Starting Automated KPI Data Import to PostgreSQL")
    logger.info("="*80)
    
    conn = get_db_connection()
    
    try:
        # Import all KPI data
        logger.info("\n📊 Importing KPI datasets...")
        import_daily_metrics(conn)
        import_products_summary(conn)
        import_traffic_sources(conn)
        import_funnel_stages(conn)
        import_ab_test_simulations(conn)
        
        # Verify
        verify_import(conn)
        
        # Show sample data
        logger.info("\n📈 Sample Data Preview:")
        cursor = conn.cursor()
        
        # Show latest daily metrics
        cursor.execute("""
            SELECT date, total_users, total_revenue, conversion_rate 
            FROM daily_metrics 
            ORDER BY date DESC LIMIT 5
        """)
        logger.info("\n  Latest Daily Metrics:")
        for row in cursor.fetchall():
            logger.info(f"    {row[0]}: {row[1]} users, €{row[2]:.2f} revenue, {row[3]:.2f}% conv")
        
        # Show top products
        cursor.execute("""
            SELECT product_id, total_revenue, total_purchases
            FROM products_summary 
            ORDER BY total_revenue DESC LIMIT 5
        """)
        logger.info("\n  Top Products by Revenue:")
        for row in cursor.fetchall():
            logger.info(f"    Product {row[0]}: €{row[1]:.2f} ({row[2]} purchases)")
        
        logger.info("\n" + "="*80)
        logger.info("✅ KPI Data Import Completed Successfully!")
        logger.info("="*80)
        
    except Exception as e:
        logger.error(f"\n❌ Import process failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        conn.close()
        logger.info("🔒 Database connection closed")


if __name__ == "__main__":
    main()
