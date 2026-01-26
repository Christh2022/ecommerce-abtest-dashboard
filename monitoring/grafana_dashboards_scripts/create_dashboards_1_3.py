# -*- coding: utf-8 -*-
import requests
import json
import os

# Configuration from environment variables
GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3000')
GRAFANA_USER = os.getenv('GRAFANA_USER', 'admin')
GRAFANA_PASSWORD = os.getenv('GRAFANA_PASSWORD', 'admin123')

dashboards = []

# 1. Product Performance Dashboard
dashboards.append({
    "dashboard": {
        "title": "Product Performance Analysis",
        "uid": "ecommerce-products",
        "tags": ["products", "performance", "catalog"],
        "schemaVersion": 38,
        "refresh": "1m",
        "panels": [
            {
                "id": 1,
                "type": "stat",
                "title": "Top Product Revenue",
                "gridPos": {"h": 4, "w": 8, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "topk(1, ecommerce_product_revenue)",
                    "refId": "A"
                }],
                "options": {"colorMode": "value", "graphMode": "area"},
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 0}}
            },
            {
                "id": 2,
                "type": "stat",
                "title": "Total Products Tracked",
                "gridPos": {"h": 4, "w": 8, "x": 8, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "count(ecommerce_product_revenue)",
                    "refId": "A"
                }],
                "options": {"colorMode": "value", "graphMode": "none"},
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0}}
            },
            {
                "id": 3,
                "type": "stat",
                "title": "Most Viewed Product",
                "gridPos": {"h": 4, "w": 8, "x": 16, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "topk(1, ecommerce_product_views)",
                    "refId": "A"
                }],
                "options": {"colorMode": "value", "graphMode": "area"},
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0}}
            },
            {
                "id": 4,
                "type": "barchart",
                "title": "Top 15 Products by Revenue",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 4},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "topk(15, ecommerce_product_revenue)",
                    "refId": "A",
                    "legendFormat": "{{product_name}}"
                }],
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 0, "color": {"mode": "palette-classic"}}}
            },
            {
                "id": 5,
                "type": "barchart",
                "title": "Top 15 Products by Conversions",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 4},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "topk(15, ecommerce_product_conversions)",
                    "refId": "A",
                    "legendFormat": "{{product_name}}"
                }],
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0, "color": {"mode": "palette-classic"}}}
            },
            {
                "id": 6,
                "type": "piechart",
                "title": "Revenue by Category",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 14},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "sum by (category) (ecommerce_product_revenue)",
                    "refId": "A",
                    "legendFormat": "{{category}}"
                }],
                "options": {"legend": {"displayMode": "table", "placement": "right", "calcs": ["sum"]}},
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 0}}
            },
            {
                "id": 7,
                "type": "table",
                "title": "Category Performance Summary",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 14},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_category_performance",
                    "refId": "A",
                    "format": "table",
                    "instant": True
                }],
                "transformations": [
                    {"id": "organize", "options": {"excludeByName": {"Time": True, "job": True, "instance": True}}}
                ]
            }
        ]
    },
    "uid": "ecommerce-products"
})

# 2. Customer Segmentation Dashboard
dashboards.append({
    "dashboard": {
        "title": "Customer Segmentation Analysis",
        "uid": "ecommerce-segments",
        "tags": ["customers", "segmentation", "rfm"],
        "schemaVersion": 38,
        "refresh": "1m",
        "panels": [
            {
                "id": 1,
                "type": "piechart",
                "title": "Users by Segment",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_segment_users",
                    "refId": "A",
                    "legendFormat": "{{segment}}"
                }],
                "options": {"legend": {"displayMode": "table", "placement": "right", "calcs": ["sum", "percent"]}},
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0}}
            },
            {
                "id": 2,
                "type": "barchart",
                "title": "Revenue by Segment",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_segment_revenue",
                    "refId": "A",
                    "legendFormat": "{{segment}}"
                }],
                "fieldConfig": {"defaults": {"unit": "currencyUSD", "decimals": 0, "color": {"mode": "palette-classic"}}}
            },
            {
                "id": 3,
                "type": "bargauge",
                "title": "Conversion Rate by Segment",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 10},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_segment_conversion",
                    "refId": "A",
                    "legendFormat": "{{segment}}"
                }],
                "options": {"displayMode": "gradient", "orientation": "horizontal"},
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
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
                "type": "table",
                "title": "Segment Performance Details",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 10},
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_segment_users",
                        "refId": "A",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_segment_revenue",
                        "refId": "B",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_segment_conversion",
                        "refId": "C",
                        "format": "table",
                        "instant": True
                    }
                ],
                "transformations": [
                    {"id": "merge"},
                    {
                        "id": "organize",
                        "options": {
                            "excludeByName": {"Time": True, "job": True, "instance": True},
                            "renameByName": {
                                "segment": "Segment",
                                "Value #A": "Users",
                                "Value #B": "Revenue ($)",
                                "Value #C": "Conversion (%)"
                            }
                        }
                    }
                ]
            }
        ]
    },
    "uid": "ecommerce-segments"
})

# 3. Customer Journey & Funnel Dashboard
dashboards.append({
    "dashboard": {
        "title": "Customer Journey & Funnel Analysis",
        "uid": "ecommerce-funnel",
        "tags": ["funnel", "journey", "conversion"],
        "schemaVersion": 38,
        "refresh": "1m",
        "panels": [
            {
                "id": 1,
                "type": "bargauge",
                "title": "Funnel - Users at Each Step",
                "gridPos": {"h": 12, "w": 12, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_funnel_users",
                    "refId": "A",
                    "legendFormat": "{{step}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal",
                    "showUnfilled": True
                },
                "fieldConfig": {"defaults": {"unit": "short", "decimals": 0, "color": {"mode": "continuous-GrYlRd"}}}
            },
            {
                "id": 2,
                "type": "bargauge",
                "title": "Conversion Rate by Step",
                "gridPos": {"h": 12, "w": 12, "x": 12, "y": 0},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_funnel_conversion",
                    "refId": "A",
                    "legendFormat": "{{step}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal"
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
                        "max": 100,
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 30, "color": "yellow"},
                            {"value": 60, "color": "green"},
                            {"value": 80, "color": "dark-green"}
                        ]}
                    }
                }
            },
            {
                "id": 3,
                "type": "table",
                "title": "Funnel Detailed Analysis",
                "description": "Identify drop-off points and optimization opportunities",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 12},
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_funnel_users",
                        "refId": "A",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_funnel_conversion",
                        "refId": "B",
                        "format": "table",
                        "instant": True
                    }
                ],
                "transformations": [
                    {"id": "merge"},
                    {
                        "id": "organize",
                        "options": {
                            "excludeByName": {"Time": True, "job": True, "instance": True},
                            "renameByName": {
                                "step": "Funnel Step",
                                "Value #A": "Users",
                                "Value #B": "Conversion Rate (%)"
                            }
                        }
                    }
                ],
                "fieldConfig": {
                    "overrides": [
                        {
                            "matcher": {"id": "byName", "options": "Conversion Rate (%)"},
                            "properties": [
                                {"id": "unit", "value": "percent"},
                                {"id": "custom.cellOptions", "value": {"type": "color-background"}},
                                {"id": "thresholds", "value": {
                                    "mode": "absolute",
                                    "steps": [
                                        {"value": None, "color": "red"},
                                        {"value": 30, "color": "yellow"},
                                        {"value": 60, "color": "green"}
                                    ]
                                }}
                            ]
                        }
                    ]
                }
            }
        ]
    },
    "uid": "ecommerce-funnel"
})

# Create all dashboards
for dashboard_config in dashboards:
    response = requests.post(
        f'{GRAFANA_URL}/api/dashboards/db',
        json={"dashboard": dashboard_config["dashboard"], "overwrite": True},
        auth=(GRAFANA_USER, GRAFANA_PASSWORD)
    )
    
    title = dashboard_config["dashboard"]["title"]
    uid = dashboard_config["uid"]
    
    if response.status_code == 200:
        print(f"✓ {title}")
        print(f"  URL: http://localhost:3000/d/{uid}")
    else:
        print(f"✗ {title}: Error {response.status_code}")

print("\n=== 3 premiers dashboards crees ===")
