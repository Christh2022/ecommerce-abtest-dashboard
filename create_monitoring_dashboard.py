import requests
import json

# Dashboard configuration
dashboard = {
    "dashboard": {
        "title": "E-Commerce Monitoring Dashboard",
        "uid": "ecommerce-monitoring",
        "tags": ["monitoring", "ecommerce"],
        "timezone": "browser",
        "refresh": "30s",
        "time": {
            "from": "now-1h",
            "to": "now"
        },
        "panels": [
            # Panel 1: Sessions
            {
                "id": 1,
                "title": "Sessions",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_realtime_sessions_today",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "short",
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 1000000, "color": "yellow"},
                                {"value": 2000000, "color": "red"}
                            ]
                        }
                    }
                },
                "options": {
                    "reduceOptions": {
                        "values": False,
                        "calcs": ["lastNotNull"]
                    },
                    "orientation": "auto",
                    "textMode": "auto",
                    "colorMode": "value",
                    "graphMode": "area",
                    "justifyMode": "auto"
                }
            },
            
            # Panel 2: Conversion Rate
            {
                "id": 2,
                "title": "Conversion Rate",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_realtime_conversion_rate",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "red"},
                                {"value": 1, "color": "yellow"},
                                {"value": 2, "color": "green"}
                            ]
                        }
                    }
                },
                "options": {
                    "reduceOptions": {
                        "values": False,
                        "calcs": ["lastNotNull"]
                    },
                    "orientation": "auto",
                    "textMode": "auto",
                    "colorMode": "value",
                    "graphMode": "area",
                    "justifyMode": "auto"
                }
            },
            
            # Panel 3: Revenue
            {
                "id": 3,
                "title": "Total Revenue",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 12, "y": 0},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_total_revenue_dollars",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 5000000, "color": "yellow"},
                                {"value": 10000000, "color": "red"}
                            ]
                        }
                    }
                },
                "options": {
                    "reduceOptions": {
                        "values": False,
                        "calcs": ["lastNotNull"]
                    },
                    "orientation": "auto",
                    "textMode": "auto",
                    "colorMode": "value",
                    "graphMode": "area",
                    "justifyMode": "auto"
                }
            },
            
            # Panel 4: Errors
            {
                "id": 4,
                "title": "Errors",
                "type": "stat",
                "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_error_count",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "short",
                        "color": {"mode": "thresholds"},
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"value": None, "color": "green"},
                                {"value": 10, "color": "yellow"},
                                {"value": 50, "color": "red"}
                            ]
                        }
                    }
                },
                "options": {
                    "reduceOptions": {
                        "values": False,
                        "calcs": ["lastNotNull"]
                    },
                    "orientation": "auto",
                    "textMode": "auto",
                    "colorMode": "value",
                    "graphMode": "none",
                    "justifyMode": "auto"
                }
            },
            
            # Panel 5: Sessions Trend
            {
                "id": 5,
                "title": "Sessions Trend",
                "type": "timeseries",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_realtime_sessions_today",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        },
                        "editorMode": "code",
                        "range": True,
                        "instant": False
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "drawStyle": "line",
                            "lineInterpolation": "linear",
                            "lineWidth": 2,
                            "fillOpacity": 10,
                            "showPoints": "never"
                        },
                        "unit": "short",
                        "color": {"mode": "palette-classic"}
                    }
                },
                "options": {
                    "tooltip": {"mode": "single"},
                    "legend": {"showLegend": False}
                }
            },
            
            # Panel 6: Revenue Trend
            {
                "id": 6,
                "title": "Revenue Trend",
                "type": "timeseries",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_total_revenue_dollars",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        },
                        "editorMode": "code",
                        "range": True,
                        "instant": False
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "drawStyle": "line",
                            "lineInterpolation": "linear",
                            "lineWidth": 2,
                            "fillOpacity": 10,
                            "showPoints": "never"
                        },
                        "unit": "currencyUSD",
                        "color": {"mode": "palette-classic"}
                    }
                },
                "options": {
                    "tooltip": {"mode": "single"},
                    "legend": {"showLegend": False}
                }
            },
            
            # Panel 7: Conversion Rate Trend
            {
                "id": 7,
                "title": "Conversion Rate Trend",
                "type": "timeseries",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_realtime_conversion_rate",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        },
                        "editorMode": "code",
                        "range": True,
                        "instant": False
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "drawStyle": "line",
                            "lineInterpolation": "linear",
                            "lineWidth": 2,
                            "fillOpacity": 10,
                            "showPoints": "never"
                        },
                        "unit": "percent",
                        "color": {"mode": "palette-classic"}
                    }
                },
                "options": {
                    "tooltip": {"mode": "single"},
                    "legend": {"showLegend": False}
                }
            },
            
            # Panel 8: Errors Over Time
            {
                "id": 8,
                "title": "Errors Over Time",
                "type": "timeseries",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
                "datasource": {
                    "type": "prometheus",
                    "uid": "prometheus-ecommerce"
                },
                "targets": [
                    {
                        "expr": "ecommerce_error_count",
                        "refId": "A",
                        "datasource": {
                            "type": "prometheus",
                            "uid": "prometheus-ecommerce"
                        },
                        "editorMode": "code",
                        "range": True,
                        "instant": False
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "drawStyle": "line",
                            "lineInterpolation": "linear",
                            "lineWidth": 2,
                            "fillOpacity": 20,
                            "showPoints": "never"
                        },
                        "unit": "short",
                        "color": {"mode": "fixed", "fixedColor": "red"}
                    }
                },
                "options": {
                    "tooltip": {"mode": "single"},
                    "legend": {"showLegend": False}
                }
            }
        ]
    },
    "overwrite": True
}

# Upload to Grafana
url = 'http://localhost:3000/api/dashboards/db'
auth = ('admin', 'admin123')

response = requests.post(url, json=dashboard, auth=auth)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Dashboard 'E-Commerce Monitoring Dashboard' créé avec succès!")
    print(f"   URL: http://localhost:3000/d/{result['uid']}")
    print(f"   Version: {result['version']}")
    print(f"\n📊 Panels créés:")
    print(f"   1. Sessions (stat)")
    print(f"   2. Conversion Rate (stat)")
    print(f"   3. Total Revenue (stat)")
    print(f"   4. Errors (stat)")
    print(f"   5. Sessions Trend (timeseries)")
    print(f"   6. Revenue Trend (timeseries)")
    print(f"   7. Conversion Rate Trend (timeseries)")
    print(f"   8. Errors Over Time (timeseries)")
else:
    print(f"❌ Erreur: {response.status_code}")
    print(response.text)
