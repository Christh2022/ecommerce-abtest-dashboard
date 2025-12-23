#!/bin/bash
# Script de test pour Linux/Mac
# Lance la suite de tests de l'application

echo "========================================"
echo "  E-Commerce A/B Test Dashboard"
echo "  Suite de tests"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo "Installez Python depuis https://www.python.org/"
    exit 1
fi

# Installer les dépendances si nécessaire
echo "Installation des dépendances..."
pip3 install -q requests
echo ""

# Lancer les tests
echo "Lancement des tests..."
echo ""
python3 run_tests.py

exit $?
