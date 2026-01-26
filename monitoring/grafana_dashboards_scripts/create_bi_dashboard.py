# -*- coding: utf-8 -*-
import requests
import json
import os

# Configuration from environment variables
GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3000')
GRAFANA_USER = os.getenv('GRAFANA_USER', 'admin')
GRAFANA_PASSWORD = os.getenv('GRAFANA_PASSWORD', 'admin123')

dashboard = {
    "dashboard": {
        "title": "Business Intelligence & Decision Support",
        "uid": "ecommerce-bi",
        "tags": ["business-intelligence", "decisions", "strategy"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 0,
        "refresh": "1m",
        "panels": [
            # Title row
            {
                "id": 100,
                "type": "row",
                "title": "KPIs Strategiques",
                "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0},
                "collapsed": False
            },
            # Revenue per user - Important for customer value
            {
                "id": 1,
                "type": "stat",
                "title": "Revenue par Utilisateur",
                "description": "Metrique cle pour evaluer la valeur client moyenne",
                "gridPos": {"h": 5, "w": 6, "x": 0, "y": 1},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_bi_revenue_per_user",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "background",
                    "graphMode": "none",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "text": {"titleSize": 14, "valueSize": 28}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 2,
                        "color": {"mode": "thresholds"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 2, "color": "yellow"},
                            {"value": 3, "color": "green"},
                            {"value": 5, "color": "dark-green"}
                        ]}
                    }
                }
            },
            # Revenue per session
            {
                "id": 2,
                "type": "stat",
                "title": "Revenue par Session",
                "description": "Efficacite de monetisation par visite",
                "gridPos": {"h": 5, "w": 6, "x": 6, "y": 1},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_bi_revenue_per_session",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "background",
                    "graphMode": "none",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "text": {"titleSize": 14, "valueSize": 28}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 2,
                        "color": {"mode": "thresholds"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 2, "color": "yellow"},
                            {"value": 3, "color": "green"}
                        ]}
                    }
                }
            },
            # Conversion efficiency
            {
                "id": 3,
                "type": "stat",
                "title": "Efficacite Conversion",
                "description": "Ratio commandes / sessions (objectif: >2%)",
                "gridPos": {"h": 5, "w": 6, "x": 12, "y": 1},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_bi_conversion_efficiency",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "background",
                    "graphMode": "none",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "text": {"titleSize": 14, "valueSize": 28}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
                        "color": {"mode": "thresholds"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 1, "color": "orange"},
                            {"value": 1.5, "color": "yellow"},
                            {"value": 2, "color": "green"}
                        ]}
                    }
                }
            },
            # Total potential revenue
            {
                "id": 4,
                "type": "stat",
                "title": "Revenue Total",
                "description": "Performance globale actuelle",
                "gridPos": {"h": 5, "w": 6, "x": 18, "y": 1},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_total_revenue_dollars",
                    "refId": "A"
                }],
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "text": {"titleSize": 14, "valueSize": 28}
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 0,
                        "color": {"mode": "palette-classic"}
                    }
                }
            },
            # Decisions row
            {
                "id": 101,
                "type": "row",
                "title": "Decisions A/B Testing - Variantes Gagnantes",
                "gridPos": {"h": 1, "w": 24, "x": 0, "y": 6},
                "collapsed": False
            },
            # Winners table
            {
                "id": 5,
                "type": "table",
                "title": "Tests A/B - Variantes Gagnantes (Recommandations)",
                "description": "Les variantes avec le meilleur taux de conversion. ACTION: Deployer les variantes gagnantes en production",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 7},
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
                        "expr": "ecommerce_abtest_conversion_rate",
                        "refId": "B",
                        "format": "table",
                        "instant": True
                    },
                    {
                        "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                        "expr": "ecommerce_abtest_revenue_dollars",
                        "refId": "C",
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
                                "scenario": "Test",
                                "variant": "Variante",
                                "Value #A": "Visiteurs",
                                "Value #B": "Taux Conversion (%)",
                                "Value #C": "Revenue ($)"
                            }
                        }
                    },
                    {
                        "id": "sortBy",
                        "options": {
                            "sort": [{"field": "Taux Conversion (%)", "desc": True}]
                        }
                    }
                ],
                "fieldConfig": {
                    "defaults": {},
                    "overrides": [
                        {
                            "matcher": {"id": "byName", "options": "Taux Conversion (%)"},
                            "properties": [
                                {"id": "unit", "value": "percent"},
                                {"id": "decimals", "value": 2},
                                {"id": "custom.cellOptions", "value": {"type": "color-background"}},
                                {"id": "thresholds", "value": {
                                    "mode": "absolute",
                                    "steps": [
                                        {"value": None, "color": "red"},
                                        {"value": 25, "color": "yellow"},
                                        {"value": 30, "color": "green"},
                                        {"value": 35, "color": "dark-green"}
                                    ]
                                }}
                            ]
                        },
                        {
                            "matcher": {"id": "byName", "options": "Revenue ($)"},
                            "properties": [
                                {"id": "unit", "value": "currencyUSD"},
                                {"id": "decimals", "value": 0}
                            ]
                        }
                    ]
                }
            },
            # Strategies row
            {
                "id": 102,
                "type": "row",
                "title": "Strategies & Opportunites",
                "gridPos": {"h": 1, "w": 24, "x": 0, "y": 17},
                "collapsed": False
            },
            # Conversion comparison
            {
                "id": 6,
                "type": "bargauge",
                "title": "Performance Conversion par Variante",
                "description": "ACTION: Identifier et deployer les variantes avec taux >32%",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 18},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_conversion_rate",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "showUnfilled": True
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent",
                        "decimals": 2,
                        "min": 0,
                        "max": 40,
                        "color": {"mode": "thresholds"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 28, "color": "yellow"},
                            {"value": 32, "color": "green"}
                        ]}
                    }
                }
            },
            # Revenue comparison
            {
                "id": 7,
                "type": "bargauge",
                "title": "Performance Revenue par Variante",
                "description": "ACTION: Prioriser les variantes generant >$350K",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 18},
                "targets": [{
                    "datasource": {"type": "prometheus", "uid": "prometheus-ecommerce"},
                    "expr": "ecommerce_abtest_revenue_dollars",
                    "refId": "A",
                    "legendFormat": "{{scenario}} - {{variant}}"
                }],
                "options": {
                    "displayMode": "gradient",
                    "orientation": "horizontal",
                    "reduceOptions": {"values": False, "calcs": ["lastNotNull"]},
                    "showUnfilled": True
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": "currencyUSD",
                        "decimals": 0,
                        "color": {"mode": "thresholds"},
                        "thresholds": {"mode": "absolute", "steps": [
                            {"value": None, "color": "red"},
                            {"value": 300000, "color": "yellow"},
                            {"value": 350000, "color": "green"}
                        ]}
                    }
                }
            },
            # Recommendations panel
            {
                "id": 8,
                "type": "text",
                "title": "Recommandations Strategiques",
                "gridPos": {"h": 8, "w": 24, "x": 0, "y": 26},
                "options": {
                    "mode": "markdown",
                    "content": """
# Actions Recommandees

## 🎯 Priorite 1 - Deploiement Immediat
- **Deployer les variantes gagnantes** avec taux de conversion >32%
- **Arreter les tests Control** si variantes testees montrent >5% d'amelioration
- **Allouer 70% du budget** aux segments haute performance

## 💰 Priorite 2 - Optimisation Revenue
- **Augmenter AOV** - Objectif: $260+ par commande
- **Cross-selling**: Implementer sur variantes a fort taux de conversion
- **Up-selling**: Focus sur users avec revenue/session >$4

## 📊 Priorite 3 - Tests Futurs
- **Tester de nouvelles variantes** sur les scenarios performants
- **Segmentation**: Creer tests specifiques pour top 20% users
- **A/B/n testing**: Tester 3-4 variantes simultanement sur homepage

## 🔍 Indicateurs de Vigilance
- ⚠️ **Taux conversion <28%** - Revoir UX/funnel
- ⚠️ **Revenue/user <$3** - Probleme monetisation
- ⚠️ **Efficacite <1.5%** - Optimiser tunnel conversion

## 💡 Opportunites Identifiees
- Potentiel gain: **+15-20% revenue** avec deployment variantes gagnantes
- **ROI tests A/B**: Evaluable apres 2-3 semaines de production
- **Quick wins**: Homepage + Checkout optimises = impact immediat
"""
                }
            }
        ]
    },
    "overwrite": True,
    "message": "Business Intelligence Dashboard"
}

response = requests.post(
    'http://localhost:3000/api/dashboards/db',
    json=dashboard,
    auth=('admin', 'admin123')
)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))

if response.status_code == 200:
    print("\n=== Dashboard BI cree avec succes! ===")
    print("URL: http://localhost:3000/d/ecommerce-bi")
    print("\nContenu:")
    print("- KPIs strategiques (Revenue/user, Revenue/session, Efficacite)")
    print("- Variantes gagnantes avec recommandations")
    print("- Performance conversion et revenue par variante")
    print("- Recommandations strategiques actionnables")
