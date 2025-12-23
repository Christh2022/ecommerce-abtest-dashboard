# -*- coding: utf-8 -*-
import json
import requests

dashboard = {
    "dashboard": {
        "title": "E-Commerce A/B Test Dashboard",
        "uid": "ecommerce-abtest",
        "tags": ["ecommerce", "abtest"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "refresh": "1m",
        "time": {
            "from": "2015-05-01T00:00:00Z",
            "to": "2015-10-01T00:00:00Z"
        },
        "panels": [
            {
                "id": 1,
                "type": "stat",
                "title": "Total Users",
                "gridPos": {"h": 5, "w": 6, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT SUM(total_users)::bigint as value FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01'",
                    "format": "table",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0}}
            },
            {
                "id": 2,
                "type": "stat",
                "title": "Total Revenue",
                "gridPos": {"h": 5, "w": 6, "x": 6, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT SUM(total_revenue)::numeric(12,2) as value FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01'",
                    "format": "table",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 0}}
            },
            {
                "id": 3,
                "type": "stat",
                "title": "Avg Conversion Rate",
                "gridPos": {"h": 5, "w": 6, "x": 12, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT AVG(conversion_rate) as value FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01'",
                    "format": "table",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {"defaults": {"unit": "percentunit", "decimals": 2}}
            },
            {
                "id": 4,
                "type": "stat",
                "title": "Avg Order Value",
                "gridPos": {"h": 5, "w": 6, "x": 18, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT AVG(avg_order_value) as value FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01'",
                    "format": "table",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 2}}
            },
            {
                "id": 5,
                "type": "timeseries",
                "title": "Daily Metrics",
                "gridPos": {"h": 9, "w": 24, "x": 0, "y": 5},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT date as time, total_users as \"Users\", total_sessions as \"Sessions\", total_conversions as \"Conversions\" FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01' ORDER BY date",
                    "format": "time_series",
                    "refId": "A"
                }],
                "options": {
                    "legend": {"displayMode": "table", "placement": "bottom", "calcs": ["mean", "last", "max"], "showLegend": True}
                },
                "fieldConfig": {
                    "defaults": {"custom": {"drawStyle": "line", "lineWidth": 2, "fillOpacity": 10}}
                }
            },
            {
                "id": 6,
                "type": "table",
                "title": "A/B Test Results",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 14},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT s.scenario_name as \"Test Name\", r.variant as \"Variant\", SUM(r.visitors)::bigint as \"Visitors\", SUM(r.conversions)::bigint as \"Conversions\", AVG(r.conversion_rate) as \"Conversion Rate\", SUM(r.revenue)::numeric(12,2) as \"Revenue\" FROM ab_test_results r JOIN ab_test_scenarios s ON r.scenario_id = s.scenario_id WHERE r.date >= '2015-05-01' AND r.date <= '2015-10-01' GROUP BY s.scenario_name, r.variant ORDER BY s.scenario_name, r.variant",
                    "format": "table",
                    "refId": "A"
                }],
                "fieldConfig": {
                    "overrides": [
                        {"matcher": {"id": "byName", "options": "Conversion Rate"}, "properties": [{"id": "unit", "value": "percentunit"}]},
                        {"matcher": {"id": "byName", "options": "Revenue"}, "properties": [{"id": "unit", "value": "currencyUSD"}]}
                    ]
                }
            }
        ]
    },
    "overwrite": True,
    "message": "Dashboard with timeFilter"
}

response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=dashboard,
    auth=('admin', 'admin123')
)

print("Status:", response.status_code)
print("Response:", response.json())

if response.status_code == 200:
    print("\nDashboard created successfully!")
    print("URL: http://localhost:3000/d/ecommerce-abtest")
