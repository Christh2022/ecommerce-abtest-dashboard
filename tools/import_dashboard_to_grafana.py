#!/usr/bin/env python3
"""
Create and import a working Security Attacks dashboard into Grafana
"""

import requests
import json
import time

GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASS = "admin123"

# Dashboard JSON
dashboard = {
    "dashboard": {
        "id": None,
        "uid": "security-attacks-v2",
        "title": "🚨 Security Attacks - Real-Time Monitoring",
        "tags": ["security", "attacks"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "refresh": "10s",
        "time": {
            "from": "now-15m",
            "to": "now"
        },
        "panels": [
            {
                "id": 1,
                "title": "🚨 Total Attacks (Last 5 min)",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
                "targets": [{
                    "expr": "max(security_attacks_total)",
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "reduceOptions": {
                        "values": False,
                        "calcs": ["lastNotNull"]
                    },
                    "orientation": "horizontal",
                    "textMode": "value_and_name",
                    "colorMode": "background",
                    "graphMode": "area"
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "short",
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 10, "color": "yellow"},
                                {"value": 30, "color": "red"}
                            ]
                        }
                    }
                }
            },
            {
                "id": 2,
                "title": "🔴 Critical Attacks",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
                "targets": [{
                    "expr": 'security_attack_by_severity{severity="critical"}',
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "orientation": "horizontal",
                    "textMode": "value_and_name",
                    "colorMode": "background",
                    "graphMode": "area"
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "fixed", "fixedColor": "dark-red"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"value": None, "color": "dark-red"}]
                        }
                    }
                }
            },
            {
                "id": 3,
                "title": "🟠 High Severity Attacks",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 12, "y": 0},
                "targets": [{
                    "expr": 'security_attack_by_severity{severity="high"}',
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "orientation": "horizontal",
                    "textMode": "value_and_name",
                    "colorMode": "background",
                    "graphMode": "area"
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "fixed", "fixedColor": "dark-orange"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"value": None, "color": "dark-orange"}]
                        }
                    }
                }
            },
            {
                "id": 4,
                "title": "🟡 Medium Severity Attacks",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0},
                "targets": [{
                    "expr": 'security_attack_by_severity{severity="medium"}',
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "orientation": "horizontal",
                    "textMode": "value_and_name",
                    "colorMode": "background",
                    "graphMode": "area"
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "fixed", "fixedColor": "dark-yellow"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"value": None, "color": "dark-yellow"}]
                        }
                    }
                }
            },
            {
                "id": 5,
                "title": "🎯 Attacks by Category",
                "type": "piechart",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 8},
                "targets": [{
                    "expr": "security_attack_by_category",
                    "refId": "A",
                    "legendFormat": "{{category}}",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "legend": {"displayMode": "table", "placement": "right", "values": ["value"]},
                    "pieType": "donut",
                    "displayLabels": ["name", "percent"]
                }
            },
            {
                "id": 6,
                "title": "⚠️ Attacks by Severity",
                "type": "piechart",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 8},
                "targets": [{
                    "expr": "security_attack_by_severity",
                    "refId": "A",
                    "legendFormat": "{{severity}}",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "legend": {"displayMode": "table", "placement": "right", "values": ["value"]},
                    "pieType": "donut",
                    "displayLabels": ["name", "percent"]
                }
            },
            {
                "id": 7,
                "title": "📊 Top Attack Types",
                "type": "table",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 18},
                "targets": [{
                    "expr": "security_attack_by_type",
                    "refId": "A",
                    "format": "table",
                    "instant": True,
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "showHeader": True,
                    "sortBy": [{"displayName": "Value", "desc": True}]
                },
                "transformations": [
                    {
                        "id": "organize",
                        "options": {
                            "excludeByName": {"Time": True, "job": True, "instance": True},
                            "renameByName": {"type": "Attack Type", "Value": "Count"}
                        }
                    }
                ]
            },
            {
                "id": 8,
                "title": "📈 Attack Timeline (Real-Time)",
                "type": "timeseries",
                "gridPos": {"h": 9, "w": 12, "x": 0, "y": 28},
                "targets": [{
                    "expr": "rate(security_attacks_total[1m]) * 60",
                    "refId": "A",
                    "legendFormat": "Attacks per minute",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "lineWidth": 2,
                            "fillOpacity": 20,
                            "gradientMode": "hue",
                            "spanNulls": True
                        },
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 5, "color": "yellow"},
                                {"value": 10, "color": "red"}
                            ]
                        }
                    }
                },
                "options": {
                    "tooltip": {"mode": "multi"},
                    "legend": {"displayMode": "list", "placement": "bottom"}
                },
                "alert": {
                    "name": "🚨 High Attack Rate Detected",
                    "message": "ALERTE: Taux d'attaques élevé détecté! Plus de 10 attaques par minute.",
                    "frequency": "1m",
                    "for": "1m",
                    "conditions": [{
                        "evaluator": {"type": "gt", "params": [10]},
                        "operator": {"type": "and"},
                        "query": {"params": ["A", "1m", "now"]},
                        "reducer": {"type": "avg"}
                    }],
                    "notifications": []
                }
            },
            {
                "id": 9,
                "title": "🔥 Attack Intensity Heatmap",
                "type": "bargauge",
                "gridPos": {"h": 9, "w": 12, "x": 12, "y": 28},
                "targets": [{
                    "expr": "security_attack_by_severity",
                    "refId": "A",
                    "legendFormat": "{{severity}}",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "continuous-RdYlGr"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 5, "color": "yellow"},
                                {"value": 10, "color": "orange"},
                                {"value": 15, "color": "red"}
                            ]
                        },
                        "min": 0
                    }
                },
                "options": {
                    "orientation": "horizontal",
                    "displayMode": "gradient",
                    "showUnfilled": True
                }
            },
            {
                "id": 10,
                "title": "⚡ Live Attack Feed (Last 5 min)",
                "type": "timeseries",
                "gridPos": {"h": 9, "w": 12, "x": 0, "y": 37},
                "targets": [
                    {
                        "expr": 'security_attack_by_category{category="injection"}',
                        "refId": "A",
                        "legendFormat": "💉 Injection Attacks",
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                    },
                    {
                        "expr": 'security_attack_by_category{category="file"}',
                        "refId": "B",
                        "legendFormat": "📁 File Attacks",
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                    },
                    {
                        "expr": 'security_attack_by_category{category="docker"}',
                        "refId": "C",
                        "legendFormat": "🐳 Docker Attacks",
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                    },
                    {
                        "expr": 'security_attack_by_category{category="advanced"}',
                        "refId": "D",
                        "legendFormat": "🎯 Advanced Attacks",
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "lineWidth": 2,
                            "fillOpacity": 30,
                            "gradientMode": "opacity"
                        }
                    }
                },
                "options": {
                    "tooltip": {"mode": "multi"},
                    "legend": {"displayMode": "table", "placement": "bottom", "values": ["value", "max"]}
                },
                "alert": {
                    "name": "🔴 Injection Attack Detected",
                    "message": "ALERTE: Attaque par injection détectée! Vérifiez immédiatement les logs de sécurité.",
                    "frequency": "30s",
                    "for": "30s",
                    "conditions": [{
                        "evaluator": {"type": "gt", "params": [0]},
                        "operator": {"type": "and"},
                        "query": {"params": ["A", "30s", "now"]},
                        "reducer": {"type": "last"}
                    }],
                    "notifications": []
                }
            },
            {
                "id": 11,
                "title": "🛡️ Attack Detection Counter",
                "type": "stat",
                "gridPos": {"h": 9, "w": 12, "x": 12, "y": 37},
                "targets": [{
                    "expr": "increase(security_attacks_total[5m])",
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"}
                }],
                "options": {
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "orientation": "auto",
                    "textMode": "value_and_name",
                    "colorMode": "background",
                    "graphMode": "area"
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 1, "color": "yellow"},
                                {"value": 5, "color": "orange"},
                                {"value": 10, "color": "red"}
                            ]
                        },
                        "unit": "short",
                        "decimals": 0
                    }
                },
                "alert": {
                    "name": "⚠️ New Attacks Detected",
                    "message": "ALERTE: Nouvelles attaques informatiques détectées dans les 5 dernières minutes!",
                    "frequency": "30s",
                    "for": "10s",
                    "conditions": [{
                        "evaluator": {"type": "gt", "params": [0]},
                        "operator": {"type": "and"},
                        "query": {"params": ["A", "30s", "now"]},
                        "reducer": {"type": "last"}
                    }],
                    "notifications": []
                }
            }
        ],
        "annotations": {
            "list": [
                {
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "enable": True,
                    "expr": "ALERTS{alertname=~\".*Attack.*\"}",
                    "name": "Security Alerts",
                    "iconColor": "red",
                    "tagKeys": "alertname,severity"
                }
            ]
        }
    },
    "overwrite": True,
    "message": "Security Attacks Dashboard - Auto-imported with Alerts"
}

def import_dashboard():
    """Import dashboard into Grafana"""
    try:
        url = f"{GRAFANA_URL}/api/dashboards/db"
        response = requests.post(
            url,
            json=dashboard,
            auth=(GRAFANA_USER, GRAFANA_PASS),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            dashboard_url = f"{GRAFANA_URL}{data.get('url', '')}"
            print(f"[OK] Dashboard imported successfully!")
            print(f"[OK] Access it at: {dashboard_url}")
            print(f"\nℹ️  If you still see 'No data', wait 10-30 seconds for Prometheus to scrape metrics")
            return True
        else:
            print(f"[ERROR] Failed to import: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to Grafana. Is it running on http://localhost:3000?")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == '__main__':
    print("[*] Importing Security Attacks Dashboard to Grafana...")
    time.sleep(2)  # Wait for Grafana to be ready
    
    if import_dashboard():
        print("\n✅ Done! Refresh your Grafana page to see the new dashboard with data")
    else:
        print("\n❌ Failed to import dashboard")
