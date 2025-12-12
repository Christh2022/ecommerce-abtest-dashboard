# -*- coding: utf-8 -*-
import requests
import json

# Dashboard ultra-simple pour debug
dashboard = {
    "dashboard": {
        "title": "E-Commerce Test Simple",
        "uid": "ecommerce-test-simple",
        "tags": ["test"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "panels": [
            {
                "id": 1,
                "type": "table",
                "title": "Total Users (Table)",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT SUM(total_users)::bigint as \"Total Users\" FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01'",
                    "format": "table",
                    "refId": "A"
                }]
            },
            {
                "id": 2,
                "type": "table",
                "title": "Daily Data (Table)",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                "targets": [{
                    "datasource": {"type": "postgres", "uid": "postgres-ecommerce"},
                    "rawSql": "SELECT date, total_users, total_revenue FROM daily_metrics WHERE date >= '2015-05-01' AND date <= '2015-10-01' ORDER BY date LIMIT 10",
                    "format": "table",
                    "refId": "A"
                }]
            }
        ]
    },
    "overwrite": True,
    "message": "Simple test dashboard"
}

response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=dashboard,
    auth=('admin', 'admin123')
)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))

if response.status_code == 200:
    print("\nTest dashboard created!")
    print("URL: http://localhost:3000/d/ecommerce-test-simple")
