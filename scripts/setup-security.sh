#!/bin/bash
# Setup script for git hooks and security tools
# Run this script after cloning the repository

set -e

echo "🔧 Configuration des outils de sécurité..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python
echo -e "\n${YELLOW}📦 Vérification de Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python détecté: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✅ Python détecté: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python non trouvé. Installez Python 3.11+${NC}"
    exit 1
fi

# Install pre-commit
echo -e "\n${YELLOW}📦 Installation de pre-commit...${NC}"
$PYTHON_CMD -m pip install --quiet pre-commit detect-secrets
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ pre-commit installé${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation de pre-commit${NC}"
    exit 1
fi

# Install pre-commit hooks
echo -e "\n${YELLOW}🎣 Installation des hooks Git...${NC}"
pre-commit install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Hooks Git installés${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des hooks${NC}"
    exit 1
fi

# Generate secrets baseline
echo -e "\n${YELLOW}🔍 Génération du baseline de détection de secrets...${NC}"
if [ -f ".secrets.baseline" ]; then
    echo -e "${YELLOW}⚠️  Baseline existant trouvé, conservation...${NC}"
else
    detect-secrets scan --baseline .secrets.baseline
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Baseline créé${NC}"
    else
        echo -e "${YELLOW}⚠️  Erreur lors de la création du baseline (non critique)${NC}"
    fi
fi

# Create .env if not exists
echo -e "\n${YELLOW}📝 Configuration de l'environnement...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Fichier .env existant trouvé${NC}"
else
    cp .env.example .env
    echo -e "${GREEN}✅ Fichier .env créé depuis .env.example${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Éditez .env et changez les mots de passe!${NC}"
fi

# Run pre-commit on all files
echo -e "\n${YELLOW}🧪 Test des hooks sur tous les fichiers...${NC}"
echo -e "${CYAN}   (Ceci peut prendre quelques minutes la première fois)${NC}"
pre-commit run --all-files || true

# Summary
echo -e "\n${CYAN}========================================================================${NC}"
echo -e "${GREEN}✅ Configuration terminée!${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "\n${YELLOW}📋 Prochaines étapes:${NC}"
echo "   1. Éditez .env et changez tous les mots de passe"
echo "   2. Lisez docs/SECRETS_MANAGEMENT.md pour les bonnes pratiques"
echo "   3. Les hooks Git vont maintenant vérifier chaque commit"
echo "   4. Lancez l'application: docker-compose -f docker-compose.secure.yml up -d"

echo -e "\n${YELLOW}🔐 Sécurité:${NC}"
echo -e "   ${RED}- Ne commitez JAMAIS le fichier .env${NC}"
echo "   - Utilisez des mots de passe forts (>= 16 caractères)"
echo "   - Activez la 2FA sur GitHub"

echo ""
