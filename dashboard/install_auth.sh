#!/bin/bash
# Script d'installation du système d'authentification
# Usage: bash install_auth.sh

echo "================================================"
echo "Installation du système d'authentification"
echo "================================================"
echo ""

# Navigate to dashboard directory
cd "$(dirname "$0")"

echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo ""
echo "🔐 Vérification du module d'authentification..."
python -c "from auth import AuthManager; print('✅ Module auth chargé avec succès')"

if [ $? -eq 0 ]; then
    echo "✅ Module d'authentification opérationnel"
else
    echo "❌ Erreur lors du chargement du module d'authentification"
    exit 1
fi

echo ""
echo "================================================"
echo "✅ Installation terminée avec succès!"
echo "================================================"
echo ""
echo "Pour démarrer le dashboard:"
echo "  cd dashboard"
echo "  python app.py"
echo ""
echo "Comptes par défaut:"
echo "  Admin: admin / admin123"
echo "  User:  user / user123"
echo ""
echo "Documentation: dashboard/AUTH_README.md"
echo "================================================"
