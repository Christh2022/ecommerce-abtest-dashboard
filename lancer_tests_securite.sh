#!/bin/bash
# ========================================
# Script de test des attaques de securite
# Usage: ./lancer_tests_securite.sh
# ========================================

echo ""
echo "========================================"
echo "TEST DES ATTAQUES DE SECURITE"
echo "========================================"
echo ""

# Verifier que les services Docker sont en cours d'execution
echo "[1/4] Verification des services Docker..."
if ! docker ps | grep -q ecommerce-pushgateway; then
    echo "❌ ERREUR: Les services Docker ne sont pas en cours d'execution"
    echo "Lancez d'abord: docker-compose -f docker-compose.secure.yml up -d"
    exit 1
fi
echo "✓ Services Docker: OK"
echo ""

# Verifier que Pushgateway est accessible
echo "[2/4] Verification de Pushgateway..."
if ! curl -s http://localhost:9091/metrics >/dev/null 2>&1; then
    echo "❌ ERREUR: Pushgateway n'est pas accessible sur le port 9091"
    exit 1
fi
echo "✓ Pushgateway: OK"
echo ""

# Lancer les tests de securite
echo "[3/4] Lancement des tests de securite..."
echo ""
python3 test_security_simple.py --target http://localhost:8050
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERREUR: Les tests ont echoue"
    exit 1
fi
echo ""

# Afficher les resultats
echo "[4/4] Tests termines avec succes!"
echo ""
echo "========================================"
echo "PROCHAINES ETAPES:"
echo "========================================"
echo ""
echo "1. Ouvrez Grafana: http://localhost:3000"
echo "2. Allez dans 'Dashboards' > 'Security Attacks Dashboard'"
echo "3. Attendez 10-15 secondes pour voir les donnees"
echo "4. Verifiez les alertes: http://localhost:3000/alerting/list"
echo ""
echo "Les rapports sont sauvegardes dans:"
echo "security-reports/attack-results/"
echo ""
