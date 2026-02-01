#!/bin/bash
# Script d'initialisation automatique des dashboards Grafana
# Ce script s'exécute après le démarrage de Grafana pour créer tous les dashboards

set -e

echo "=== Initialisation des Dashboards Grafana ==="

# Attendre que Grafana soit prêt
echo " Attente de Grafana..."
GRAFANA_URL="${GRAFANA_URL:-http://grafana:3000}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-changeme}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -sf "${GRAFANA_URL}/api/health" > /dev/null 2>&1; then
        echo " Grafana est prêt!"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "   Tentative ${RETRY_COUNT}/${MAX_RETRIES}..."
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo " Timeout: Grafana n'est pas accessible"
    exit 1
fi

# Attendre un peu plus pour s'assurer que l'API est complètement prête
sleep 5

echo ""
echo " Création des dashboards..."

# Export des variables pour tous les scripts Python
export GRAFANA_URL
export GRAFANA_USER
export GRAFANA_PASSWORD

echo "DEBUG: GRAFANA_URL=$GRAFANA_URL"

# Dashboards 1-3: Funnel, Segments, Products
echo "  → Dashboards 1-3 (Funnel, Segmentation, Products)..."
python /app/grafana_dashboards_scripts/create_dashboards_1_3.py
sleep 2

# Dashboards 4-6: Cohorts, Real-Time, Predictive
echo "  → Dashboards 4-6 (Cohorts, Real-Time, Predictive)..."
python /app/grafana_dashboards_scripts/create_dashboards_4_6.py
sleep 2

# Business Intelligence Dashboard
echo "  → Business Intelligence Dashboard..."
python /app/grafana_dashboards_scripts/create_bi_dashboard.py
sleep 2

# Full E-Commerce Dashboard
echo "  → E-Commerce A/B Test Analytics Dashboard..."
python /app/grafana_dashboards_scripts/create_full_dashboard.py
sleep 2

# Monitoring Dashboard
echo "  → Monitoring Dashboard..."
python /app/grafana_dashboards_scripts/create_monitoring_dashboard.py
sleep 2

# Prometheus Dashboard
echo "  → Prometheus Dashboard..."
python /app/grafana_dashboards_scripts/create_prometheus_dashboard.py

echo ""
echo " Tous les dashboards ont été créés avec succès!"
echo ""
echo " Accédez à Grafana: http://localhost:3000"
echo "   Utilisateur: \$GRAFANA_USER"
echo "   Mot de passe: Voir variable d'environnement GRAFANA_PASSWORD"
echo ""
