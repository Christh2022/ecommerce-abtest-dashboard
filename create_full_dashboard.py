# -*- coding: utf-8 -*-
import requests
import json

dashboard = {
    "dashboard": {
        "title": "E-Commerce A/B Test Analytics",
        "uid": "ecommerce-full",
        "tags": ["ecommerce", "abtest", "analytics"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "refresh": "30s",
        "panels": [
            # Row 1: KPIs principaux
            {
                "id": 1,
                "type": "stat",
                "title": "Total Users",
                "gridPos": {"h": 4, "w": 4, "x": 0, "y": 0},
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
                    "defaults": {
                        "unit": "short",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "green"}
                        ]}
                    }
                }
            },
            {
                "id": 2,
                "type": "stat",
                "title": "Total Revenue",
                "gridPos": {"h": 4, "w": 4, "x": 4, "y": 0},
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
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "green"}
                        ]}
                    }
                }
            },
            {
                "id": 3,
                "type": "stat",
                "title": "Conversion Rate",
                "gridPos": {"h": 4, "w": 4, "x": 8, "y": 0},
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
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
                        "color": {"mode": "palette-classic"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 20, "color": "yellow"},
                            {"value": 30, "color": "green"}
                        ]}
                    }
                }
            },
            {
                "id": 4,
                "type": "stat",
                "title": "Avg Order Value",
                "gridPos": {"h": 4, "w": 4, "x": 12, "y": 0},
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
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 2,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            {
                "id": 5,
                "type": "stat",
                "title": "Total Orders",
                "gridPos": {"h": 4, "w": 4, "x": 16, "y": 0},
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
                    "defaults": {
                        "unit": "short",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            {
                "id": 6,
                "type": "stat",
                "title": "Total Sessions",
                "gridPos": {"h": 4, "w": 4, "x": 20, "y": 0},
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
                    "defaults": {
                        "unit": "short",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            # Row 2: A/B Test Visitors
            {
                "id": 7,
                "type": "bargauge",
                "title": "A/B Test - Visitors by Variant",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_visitors",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "short",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            # Row 2: A/B Test Conversion Rate
            {
                "id": 8,
                "type": "bargauge",
                "title": "A/B Test - Conversion Rate by Variant",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_conversion_rate",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
                        "color": {"mode": "palette-classic"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 20, "color": "yellow"},
                            {"value": 30, "color": "green"}
                        ]}
                    }
                }
            },
            # Row 3: A/B Test Revenue
            {
                "id": 9,
                "type": "barchart",
                "title": "A/B Test - Revenue by Variant",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_revenue_dollars",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            # Row 3: A/B Test Conversions
            {
                "id": 10,
                "type": "barchart",
                "title": "A/B Test - Conversions by Variant",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_conversions",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "fieldConfig": {
                    "defaults": {
                        "unit": "short",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            # Row 4: Table détaillée
            {
                "id": 11,
                "type": "table",
                "title": "A/B Test Results - Detailed View",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 20},
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_abtest_visitors",
                        "refId": "A",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_abtest_conversions",
                        "refId": "B",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_abtest_conversion_rate",
                        "refId": "C",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_abtest_revenue_dollars",
                        "refId": "D",
                        "format": "table",
                        "instant": True
                    }
                ],
                "transformations": [
                    {
                        "id": "merge",
                        "options": {}
                    },
                    {
                        "id": "organize",
                        "options": {
                            "excludeByName": {"Time": True, "job": True, "instance": True},
                            "renameByName": {
                                "scenario": "Test Name",
                                "variant": "Variant",
                                "Value #A": "Visitors",
                                "Value #B": "Conversions",
                                "Value #C": "Conversion Rate (%)",
                                "Value #D": "Revenue ($)"
                            }
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {},
                    "overrides": [
                        {
                            "matcher": {"id": "byName", "options": "Conversion Rate (%)"},
                            "properties": [{"id": "unit", "value": "percent"}, {"id": "decimals", "value": 2}]
                        },
                        {
                            "matcher": {"id": "byName", "options": "Revenue ($)"},
                            "properties": [{"id": "unit", "value": "currencyUSD"}, {"id": "decimals", "value": 0}]
                        }
                    ]
                }
            }
        ]
    },
    "overwrite": True,
    "message": "Complete A/B test dashboard with Prometheus"
}

response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=dashboard,
    auth=('admin', 'admin123')
)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))

if response.status_code == 200:
    print("\n=== Dashboard cree avec succes! ===")
    print("URL: http://localhost:3000/d/ecommerce-full")
    print("\nLe dashboard contient:")
    print("- 6 KPIs principaux (Users, Revenue, Conversion Rate, AOV, Orders, Sessions)")
    print("- Visualisations des visiteurs par variante")
    print("- Taux de conversion par variante")
    print("- Revenue par variante")
    print("- Conversions par variante")
    print("- Tableau detaille avec toutes les metriques A/B test")
