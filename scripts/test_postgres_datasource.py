#!/usr/bin/env python3
"""
Test PostgreSQL Datasource Configuration
Validates connection and queries for the dashboard
"""

import sys
import os
from pathlib import Path

# Add dashboard directory to path
dashboard_dir = Path(__file__).parent.parent / 'dashboard'
sys.path.insert(0, str(dashboard_dir))

from db import (
    test_connection,
    get_database_stats,
    get_kpi_summary,
    get_daily_kpis,
    get_top_products,
    get_ab_test_summary,
    get_funnel_analysis,
    get_traffic_sources
)

def print_section(title):
    """Print section header"""
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)

def test_datasource():
    """Test all database functions"""
    
    print("\n" + "🚀 Testing PostgreSQL Datasource Configuration" + "\n")
    
    # Test 1: Connection
    print_section("Test 1: Database Connection")
    if test_connection():
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        sys.exit(1)
    
    # Test 2: Database Stats
    print_section("Test 2: Database Statistics")
    try:
        stats = get_database_stats()
        print("\n📈 Row Counts:")
        for table, count in stats.items():
            status = "✅" if count > 0 else "⚠️"
            print(f"  {status} {table}: {count:,} rows")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False
    
    # Test 3: KPI Summary
    print_section("Test 3: KPI Summary")
    try:
        kpis = get_kpi_summary()
        print("\n📊 Overall KPIs:")
        print(f"  Total Users: {kpis['total_users'].iloc[0]:,}")
        print(f"  Total Sessions: {kpis['total_sessions'].iloc[0]:,}")
        print(f"  Total Revenue: €{kpis['total_revenue'].iloc[0]:,.2f}")
        print(f"  Total Conversions: {kpis['total_conversions'].iloc[0]:,}")
        print(f"  Avg Conversion Rate: {kpis['avg_conversion_rate'].iloc[0]:.2f}%")
        print(f"  Avg Order Value: €{kpis['avg_order_value'].iloc[0]:.2f}")
        print("✅ KPI summary query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Daily KPIs
    print_section("Test 4: Daily KPIs (Last 5 Days)")
    try:
        daily = get_daily_kpis()
        print(f"\n📅 Retrieved {len(daily)} days")
        print("\nLatest 5 days:")
        for _, row in daily.head(5).iterrows():
            print(f"  {row['date']}: {row['total_users']} users, "
                  f"€{row['total_revenue']:.2f} revenue, "
                  f"{row['conversion_rate']:.2f}% conv")
        print("✅ Daily KPIs query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Top Products
    print_section("Test 5: Top Products")
    try:
        products = get_top_products(limit=5)
        print(f"\n🏆 Retrieved {len(products)} products")
        print("\nTop 5 by revenue:")
        for _, row in products.head(5).iterrows():
            print(f"  {row['product_id']}: €{row['total_revenue']:.2f} "
                  f"({row['total_purchases']} purchases)")
        print("✅ Products query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 6: A/B Test Summary
    print_section("Test 6: A/B Test Summary")
    try:
        ab_tests = get_ab_test_summary()
        print(f"\n🧪 Retrieved {len(ab_tests)} A/B test scenarios")
        for _, row in ab_tests.iterrows():
            print(f"  {row['scenario_id']}: {row['scenario_name']}")
            print(f"    Status: {row['status']}")
            print(f"    Control: {row['variant_a_conv_rate']:.2f}% | "
                  f"Variant: {row['variant_b_conv_rate']:.2f}%")
            if row['variant_a_conv_rate'] and row['variant_b_conv_rate']:
                lift = ((row['variant_b_conv_rate'] - row['variant_a_conv_rate']) / 
                       row['variant_a_conv_rate'] * 100)
                print(f"    Lift: {lift:+.2f}% | Significance: {row['max_significance']:.2f}%")
        print("✅ A/B test summary query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 7: Funnel Analysis
    print_section("Test 7: Funnel Analysis")
    try:
        funnel = get_funnel_analysis()
        print(f"\n🔄 Retrieved {len(funnel)} funnel stages")
        for _, row in funnel.iterrows():
            print(f"  Stage {row['stage_order']}: {row['stage_name']}")
            print(f"    Avg Visitors: {row['avg_visitors']:.0f} | "
                  f"Drop-off: {row['avg_drop_off']:.0f} | "
                  f"Conv Rate: {row['avg_conversion_rate']:.2f}%")
        print("✅ Funnel analysis query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 8: Traffic Sources
    print_section("Test 8: Traffic Sources")
    try:
        traffic = get_traffic_sources()
        print(f"\n🚦 Retrieved {len(traffic)} traffic sources")
        for _, row in traffic.head(5).iterrows():
            print(f"  {row['source']} / {row['medium']}")
            print(f"    Sessions: {row['total_sessions']:,} | "
                  f"Revenue: €{row['total_revenue']:.2f} | "
                  f"Conv: {row['conversion_rate']:.2f}%")
        print("✅ Traffic sources query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Summary
    print_section("✅ All Tests Passed!")
    print("\n🎉 PostgreSQL datasource is correctly configured and operational")
    print("📊 All queries executed successfully")
    print("🚀 Dashboard is ready to use PostgreSQL data\n")
    
    return True


if __name__ == "__main__":
    success = test_datasource()
    sys.exit(0 if success else 1)
