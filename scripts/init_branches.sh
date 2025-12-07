#!/bin/bash
# Script d'initialisation des branches Git pour le projet E-commerce Dashboard

echo "🚀 Initialisation du projet E-commerce Dashboard & A/B Testing"
echo "============================================================="

# Couleurs pour l'output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si nous sommes dans un repository Git
if [ ! -d .git ]; then
    echo -e "${YELLOW}Initialisation du repository Git...${NC}"
    git init
    echo -e "${GREEN}✓ Repository Git initialisé${NC}"
fi

# Créer un commit initial si nécessaire
if [ -z "$(git log 2>/dev/null)" ]; then
    echo -e "${YELLOW}Création du commit initial...${NC}"
    git add .
    git commit -m "chore: initial commit - project structure"
    echo -e "${GREEN}✓ Commit initial créé${NC}"
fi

# Liste des branches à créer
branches=(
    "feature/data-preprocessing"
    "feature/data-cleaning"
    "feature/data-exploration"
    "feature/kpi-metrics"
    "feature/ab-testing"
    "feature/dashboard-home"
    "feature/dashboard-behavior"
    "feature/dashboard-products"
    "feature/dashboard-abtest"
    "feature/dashboard-cohorts"
    "feature/docker-setup"
    "feature/docs-writing"
    "feature/refactor"
    "feature/tests"
    "feature/security-intrusion"
)

echo ""
echo -e "${BLUE}Création des branches feature...${NC}"
echo ""

# Créer chaque branche
for branch in "${branches[@]}"; do
    if git show-ref --verify --quiet "refs/heads/$branch"; then
        echo -e "${YELLOW}⊙ Branche '$branch' existe déjà${NC}"
    else
        git branch "$branch"
        echo -e "${GREEN}✓ Branche '$branch' créée${NC}"
    fi
done

echo ""
echo -e "${GREEN}=============================================================${NC}"
echo -e "${GREEN}✓ Initialisation terminée avec succès!${NC}"
echo ""
echo -e "${BLUE}Branches créées:${NC}"
git branch | grep feature/
echo ""
echo -e "${YELLOW}Pour commencer à travailler sur une branche:${NC}"
echo "  git checkout feature/nom-de-la-branche"
echo ""
echo -e "${YELLOW}Branche actuelle:${NC}"
git branch --show-current
