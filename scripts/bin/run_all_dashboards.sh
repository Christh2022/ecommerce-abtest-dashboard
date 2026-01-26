#!/bin/bash
# Script shell pour exécuter tous les scripts de création de dashboards
# Usage: ./run_all_dashboards.sh

set -e  # Arrêter en cas d'erreur

echo "========================================"
echo "Création de tous les dashboards Grafana"
echo "========================================"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[ERREUR] Python n'est pas installé"
    echo "Veuillez installer Python 3.x et réessayer"
    exit 1
fi

# Déterminer la commande Python à utiliser
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Exécuter le script Python
$PYTHON_CMD run_all_dashboards.py

# Capturer le code de retour
if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCÈS] Tous les dashboards ont été créés avec succès!"
    exit 0
else
    echo ""
    echo "[ERREUR] Certains dashboards n'ont pas pu être créés"
    echo "Vérifiez que Grafana est accessible et que les credentials sont corrects"
    exit 1
fi
