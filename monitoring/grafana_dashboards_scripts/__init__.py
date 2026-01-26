"""
Scripts de création automatique des dashboards Grafana.

Ce module contient tous les scripts nécessaires pour créer et configurer
automatiquement les dashboards Grafana pour l'application e-commerce A/B test.
"""

__version__ = "1.0.0"
__author__ = "E-Commerce A/B Test Dashboard Team"

# Expose les scripts comme des modules importables
__all__ = [
    "create_dashboards_1_3",
    "create_dashboards_4_6",
    "create_bi_dashboard",
    "create_full_dashboard",
    "create_monitoring_dashboard",
    "create_prometheus_dashboard",
]
