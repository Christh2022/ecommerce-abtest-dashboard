#!/usr/bin/env python3
"""
Load sample data from CSV files into PostgreSQL
"""
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'ecommerce-postgres'),
    port=5432,
    database='ecommerce_db',
    user='dashuser',
    password='dashpass'
)
cur = conn.cursor()

print("Loading sample data...")

# 1. Load AB Test Scenarios
print("\n1. Loading AB Test Scenarios...")
df_scenarios = pd.read_csv('data/clean/ab_test_scenarios.csv')
for _, row in df_scenarios.iterrows():
    cur.execute("""
        INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, hypothesis, status, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (scenario_id) DO NOTHING
    """, (
        row['id'],
        row['name'],
        row['description'],
        f"Expected lift: {row['expected_lift']*100:.1f}% on {row['target_metric']}",
        'active',
        datetime.now().date() - timedelta(days=30),
        datetime.now().date() + timedelta(days=30)
    ))
print(f"✓ Loaded {len(df_scenarios)} scenarios")

# 2. Load AB Test Results
print("\n2. Loading AB Test Results...")
df_results = pd.read_csv('data/clean/ab_test_simulation_results.csv')
for idx, row in df_results.head(100).iterrows():  # Limit to 100 rows for demo
    scenario_id = row['scenario_id']
    # Control group
    cur.execute("""
        INSERT INTO ab_test_results (scenario_id, variant, visitors, conversions, revenue, test_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        scenario_id,
        'control',
        int(row['sample_size_per_group']),
        int(row['sample_size_per_group'] * row['baseline_rate']),
        round(row['sample_size_per_group'] * row['baseline_rate'] * random.uniform(50, 150), 2),
        datetime.now().date() - timedelta(days=random.randint(1, 30))
    ))
    # Variant group
    cur.execute("""
        INSERT INTO ab_test_results (scenario_id, variant, visitors, conversions, revenue, test_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        scenario_id,
        'variant_a',
        int(row['sample_size_per_group']),
        int(row['sample_size_per_group'] * row['variant_rate']),
        round(row['sample_size_per_group'] * row['variant_rate'] * random.uniform(50, 150), 2),
        datetime.now().date() - timedelta(days=random.randint(1, 30))
    ))
print(f"✓ Loaded {df_results.head(100).shape[0] * 2} test results")

# 3. Load Daily Metrics
print("\n3. Loading Daily Metrics...")
df_traffic = pd.read_csv('data/clean/traffic_daily.csv')
for _, row in df_traffic.head(90).iterrows():  # Last 90 days
    cur.execute("""
        INSERT INTO daily_metrics (date, total_users, total_sessions, total_revenue, total_conversions, conversion_rate, avg_order_value)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING
    """, (
        row['date'],
        int(row['unique_users']),
        int(row['unique_sessions']),
        round(row['transactions'] * random.uniform(50, 150), 2),
        int(row['transactions']),
        row['conversion_rate'] / 100 if row['conversion_rate'] > 1 else row['conversion_rate'],
        round(random.uniform(45, 95), 2)
    ))
print(f"✓ Loaded {min(90, len(df_traffic))} daily metrics")

# 4. Load Products Summary
print("\n4. Loading Products Summary...")
try:
    df_products = pd.read_csv('data/clean/top_products_comprehensive.csv')
    for _, row in df_products.head(100).iterrows():
        cur.execute("""
            INSERT INTO products_summary (product_id, product_name, category, total_views, total_sales, revenue, avg_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            f"P{random.randint(1000,9999)}",
            row.get('product', f"Product {random.randint(1,1000)}"),
            row.get('category', 'General'),
            int(row.get('views', random.randint(100, 5000))),
            int(row.get('sales', random.randint(10, 500))),
            round(row.get('revenue', random.uniform(100, 5000)), 2),
            round(random.uniform(3.5, 5.0), 1)
        ))
    print(f"✓ Loaded {min(100, len(df_products))} products")
except Exception as e:
    print(f"⚠ Products loading error (optional): {e}")

# 5. Load User Behavior (sample data)
print("\n5. Creating user behavior data...")
for i in range(500):
    cur.execute("""
        INSERT INTO user_behavior (user_id, session_date, device_type, browser, country, page_views, session_duration, converted, revenue)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        f"U{random.randint(10000,99999)}",
        datetime.now().date() - timedelta(days=random.randint(0, 30)),
        random.choice(['mobile', 'desktop', 'tablet']),
        random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
        random.choice(['USA', 'UK', 'France', 'Germany', 'Spain']),
        random.randint(1, 20),
        random.randint(30, 1800),
        random.choice([True, False]),
        round(random.uniform(0, 200), 2) if random.random() > 0.7 else 0
    ))
print("✓ Loaded 500 user behavior records")

# 6. Load Funnel Stages
print("\n6. Creating funnel stages...")
funnel_steps = [
    ('homepage', 'Homepage Visit', 1, 10000),
    ('product_view', 'Product View', 2, 7500),
    ('add_to_cart', 'Add to Cart', 3, 2500),
    ('checkout', 'Checkout', 4, 1500),
    ('purchase', 'Purchase', 5, 1000)
]
for step_id, step_name, step_order, users in funnel_steps:
    cur.execute("""
        INSERT INTO funnel_stages (stage_id, stage_name, stage_order, users_count, conversion_rate)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (stage_id) DO UPDATE 
        SET users_count = EXCLUDED.users_count, conversion_rate = EXCLUDED.conversion_rate
    """, (
        step_id,
        step_name,
        step_order,
        users,
        round(users / 10000 * 100, 2)
    ))
print("✓ Loaded 5 funnel stages")

# Commit all changes
conn.commit()
cur.close()
conn.close()

print("\n" + "="*50)
print("✅ Sample data loaded successfully!")
print("="*50)
print("\nVerify with:")
print("  docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -c 'SELECT COUNT(*) FROM ab_test_results;'")
print("  docker restart ecommerce-exporter")
