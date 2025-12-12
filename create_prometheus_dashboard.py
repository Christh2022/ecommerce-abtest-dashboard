# -*- coding: utf-8 -*-
import requests
import json

dashboard = {
    "dashboard": {
        "title": "E-Commerce Dashboard (Prometheus)",
        "uid": "ecommerce-prometheus",
        "tags": ["ecommerce", "prometheus"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "refresh": "30s",
        "panels": [
            {
                "id": 1,
                "type": "stat",
                "title": "Total Users",
                "gridPos": {"h": 5, "w": 6, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_total_users",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "short", "decimals": 0, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 2,
                "type": "stat",
                "title": "Total Revenue",
                "gridPos": {"h": 5, "w": 6, "x": 6, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_total_revenue_dollars",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "currencyUSD", "decimals": 0, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 3,
                "type": "stat",
                "title": "Avg Conversion Rate",
                "gridPos": {"h": 5, "w": 6, "x": 12, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_avg_conversion_rate",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "percent", "decimals": 2, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 4,
                "type": "stat",
                "title": "Avg Order Value",
                "gridPos": {"h": 5, "w": 6, "x": 18, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_avg_order_value_dollars",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "currencyUSD", "decimals": 2, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 5,
                "type": "stat",
                "title": "Total Orders",
                "gridPos": {"h": 5, "w": 6, "x": 0, "y": 5},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_total_orders",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "short", "decimals": 0, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 6,
                "type": "stat",
                "title": "Total Sessions",
                "gridPos": {"h": 5, "w": 6, "x": 6, "y": 5},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_total_sessions",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {"unit": "short", "decimals": 0, "color": {"mode": "thresholds"}}
                }
            },
            {
                "id": 7,
                "type": "table",
                "title": "A/B Test Results",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 10},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_visitors",
                    "refId": "A",
                    "format": "table",
                    "instant": True
                }],
                "transformations": [
                    {
                        "id": "organize",
                        "options": {
                            "excludeByName": {"Time": True, "job": True, "instance": True, "__name__": True},
                            "indexByName": {},
                            "renameByName": {
                                "scenario": "Test Name",
                                "variant": "Variant",
                                "Value": "Visitors"
                            }
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {},
                    "overrides": []
                }
            }
        ]
    },
    "overwrite": True,
    "message": "Prometheus-based dashboard"
}

response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=dashboard,
    auth=('admin', 'admin123')
)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))

if response.status_code == 200:
    print("\nDashboard created successfully!")
    print("URL: http://localhost:3000/d/ecommerce-prometheus")
