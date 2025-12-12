"""
PostgreSQL Database Connection Module
Handles all database connections and queries for the dashboard
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration from environment variables
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://dashuser:dashpass@localhost:5432/ecommerce_db'
)

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False  # Set to True for SQL debug logging
)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Automatically handles connection closing
    
    Usage:
        with get_db_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM table", conn)
    """
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


def test_connection():
    """Test database connection"""
    try:
        with get_db_connection() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def execute_query(query, params=None):
    """
    Execute a SQL query and return results as DataFrame
    
    Args:
        query (str): SQL query to execute
        params (dict, optional): Query parameters
    
    Returns:
        pd.DataFrame: Query results
    """
    try:
        with get_db_connection() as conn:
            if params:
                df = pd.read_sql_query(text(query), conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logger.error(f"❌ Query execution failed: {e}")
        raise


# =============================================================================
# KPI QUERIES
# =============================================================================

def get_daily_metrics(start_date=None, end_date=None):
    """Get daily metrics with optional date filtering"""
    query = """
    SELECT 
        date,
        total_users,
        total_sessions,
        total_revenue,
        total_conversions,
        conversion_rate,
        avg_order_value,
        avg_session_duration
    FROM daily_metrics
    WHERE 1=1
    """
    
    if start_date:
        query += f" AND date >= '{start_date}'"
    if end_date:
        query += f" AND date <= '{end_date}'"
    
    query += " ORDER BY date"
    
    return execute_query(query)


def get_kpi_summary():
    """Get overall KPI summary"""
    query = """
    SELECT 
        SUM(total_users) as total_users,
        SUM(total_sessions) as total_sessions,
        SUM(total_revenue) as total_revenue,
        SUM(total_conversions) as total_conversions,
        ROUND(AVG(conversion_rate), 2) as avg_conversion_rate,
        ROUND(AVG(avg_order_value), 2) as avg_order_value
    FROM daily_metrics
    """
    return execute_query(query)


def get_daily_kpis():
    """Get daily KPIs using the view"""
    query = "SELECT * FROM v_daily_kpis ORDER BY date DESC LIMIT 30"
    return execute_query(query)


# =============================================================================
# PRODUCT QUERIES
# =============================================================================

def get_top_products(limit=20):
    """Get top products by revenue"""
    query = f"""
    SELECT * FROM v_top_products
    WHERE total_purchases > 0
    LIMIT {limit}
    """
    return execute_query(query)


def get_products_by_category():
    """Get product performance by category"""
    query = """
    SELECT 
        category,
        COUNT(*) as product_count,
        SUM(total_purchases) as total_purchases,
        SUM(total_revenue) as total_revenue,
        ROUND(AVG(conversion_rate), 2) as avg_conversion_rate
    FROM products_summary
    WHERE category IS NOT NULL
    GROUP BY category
    ORDER BY total_revenue DESC
    """
    return execute_query(query)


def get_product_details(product_id):
    """Get details for a specific product"""
    query = """
    SELECT * FROM products_summary
    WHERE product_id = :product_id
    """
    return execute_query(query, params={'product_id': product_id})


# =============================================================================
# A/B TEST QUERIES
# =============================================================================

def get_ab_test_scenarios():
    """Get all A/B test scenarios"""
    query = """
    SELECT 
        scenario_id,
        scenario_name,
        description,
        hypothesis,
        status,
        start_date,
        end_date
    FROM ab_test_scenarios
    ORDER BY scenario_id
    """
    return execute_query(query)


def get_ab_test_summary():
    """Get A/B test summary using the view"""
    query = "SELECT * FROM v_ab_test_summary ORDER BY max_significance DESC"
    return execute_query(query)


def get_ab_test_results(scenario_id=None):
    """Get A/B test results with optional scenario filtering"""
    query = """
    SELECT 
        r.date,
        r.scenario_id,
        s.scenario_name,
        r.variant,
        r.visitors,
        r.conversions,
        r.conversion_rate,
        r.revenue,
        r.avg_order_value,
        r.statistical_significance
    FROM ab_test_results r
    JOIN ab_test_scenarios s ON r.scenario_id = s.scenario_id
    """
    
    if scenario_id:
        query += f" WHERE r.scenario_id = '{scenario_id}'"
    
    query += " ORDER BY r.date, r.scenario_id, r.variant"
    
    return execute_query(query)


def get_ab_test_comparison(scenario_id):
    """Get detailed comparison for a specific A/B test"""
    query = """
    SELECT 
        variant,
        SUM(visitors) as total_visitors,
        SUM(conversions) as total_conversions,
        ROUND(AVG(conversion_rate), 2) as avg_conversion_rate,
        SUM(revenue) as total_revenue,
        ROUND(AVG(avg_order_value), 2) as avg_aov,
        MAX(statistical_significance) as max_significance
    FROM ab_test_results
    WHERE scenario_id = :scenario_id
    GROUP BY variant
    ORDER BY variant
    """
    return execute_query(query, params={'scenario_id': scenario_id})


# =============================================================================
# FUNNEL QUERIES
# =============================================================================

def get_funnel_analysis():
    """Get conversion funnel analysis"""
    query = """
    SELECT 
        stage_name,
        stage_order,
        AVG(visitors) as avg_visitors,
        AVG(drop_off) as avg_drop_off,
        AVG(conversion_rate) as avg_conversion_rate
    FROM funnel_stages
    GROUP BY stage_name, stage_order
    ORDER BY stage_order
    """
    return execute_query(query)


def get_funnel_daily(start_date=None, end_date=None):
    """Get daily funnel data"""
    query = """
    SELECT 
        date,
        stage_name,
        visitors,
        drop_off,
        conversion_rate
    FROM funnel_stages
    WHERE 1=1
    """
    
    if start_date:
        query += f" AND date >= '{start_date}'"
    if end_date:
        query += f" AND date <= '{end_date}'"
    
    query += " ORDER BY date, stage_order"
    
    return execute_query(query)


# =============================================================================
# TRAFFIC QUERIES
# =============================================================================

def get_traffic_sources():
    """Get traffic source analysis"""
    query = """
    SELECT 
        source,
        medium,
        SUM(sessions) as total_sessions,
        SUM(users) as total_users,
        SUM(conversions) as total_conversions,
        SUM(revenue) as total_revenue,
        ROUND(AVG(conversions::DECIMAL / NULLIF(sessions, 0) * 100), 2) as conversion_rate
    FROM traffic_sources
    GROUP BY source, medium
    ORDER BY total_revenue DESC
    """
    return execute_query(query)


def get_traffic_daily(start_date=None, end_date=None):
    """Get daily traffic data"""
    query = """
    SELECT 
        date,
        source,
        sessions,
        users,
        conversions,
        revenue
    FROM traffic_sources
    WHERE 1=1
    """
    
    if start_date:
        query += f" AND date >= '{start_date}'"
    if end_date:
        query += f" AND date <= '{end_date}'"
    
    query += " ORDER BY date"
    
    return execute_query(query)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_table_row_count(table_name):
    """Get row count for a table"""
    query = f"SELECT COUNT(*) as count FROM {table_name}"
    result = execute_query(query)
    return result['count'].iloc[0] if not result.empty else 0


def get_database_stats():
    """Get database statistics"""
    stats = {
        'daily_metrics': get_table_row_count('daily_metrics'),
        'products_summary': get_table_row_count('products_summary'),
        'ab_test_scenarios': get_table_row_count('ab_test_scenarios'),
        'ab_test_results': get_table_row_count('ab_test_results'),
        'funnel_stages': get_table_row_count('funnel_stages'),
        'traffic_sources': get_table_row_count('traffic_sources'),
    }
    return stats


# Initialize connection on module import
if __name__ != "__main__":
    test_connection()
