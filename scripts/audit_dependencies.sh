#!/bin/bash
# Audit des dépendances Python avec pip-audit
# Usage: ./scripts/audit_dependencies.sh [OPTIONS]
#
# Options:
#   --fix          Tenter de corriger automatiquement les vulnérabilités
#   --json         Sortie au format JSON
#   --format       Format de sortie (json, cyclonedx-json, cyclonedx-xml)
#   --output FILE  Sauvegarder le rapport dans un fichier
#   --requirement  Fichier requirements.txt spécifique (par défaut: requirements.txt)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🔒 Audit de Sécurité des Dépendances${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if pip-audit is installed
if ! command -v pip-audit &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip-audit n'est pas installé. Installation...${NC}"
    pip install pip-audit
    echo ""
fi

# Parse arguments
FIX_VULNERABILITIES=false
OUTPUT_FORMAT="columns"
OUTPUT_FILE=""
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
EXTRA_ARGS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX_VULNERABILITIES=true
            shift
            ;;
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --requirement)
            REQUIREMENTS_FILE="$2"
            shift 2
            ;;
        *)
            EXTRA_ARGS="$EXTRA_ARGS $1"
            shift
            ;;
    esac
done

# Audit root requirements.txt
echo -e "${BLUE}📋 Audit: $REQUIREMENTS_FILE${NC}"
echo ""

AUDIT_CMD="pip-audit --requirement $REQUIREMENTS_FILE --format $OUTPUT_FORMAT"

if [ "$FIX_VULNERABILITIES" = true ]; then
    AUDIT_CMD="$AUDIT_CMD --fix"
fi

if [ -n "$OUTPUT_FILE" ]; then
    AUDIT_CMD="$AUDIT_CMD --output $OUTPUT_FILE"
fi

AUDIT_CMD="$AUDIT_CMD $EXTRA_ARGS"

# Run audit
if eval $AUDIT_CMD; then
    echo ""
    echo -e "${GREEN}✅ Aucune vulnérabilité détectée dans $REQUIREMENTS_FILE${NC}"
    ROOT_STATUS=0
else
    ROOT_STATUS=$?
    echo ""
    echo -e "${RED}❌ Vulnérabilités trouvées dans $REQUIREMENTS_FILE${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"

# Audit dashboard requirements.txt if exists
DASHBOARD_REQ="$PROJECT_DIR/dashboard/requirements.txt"
if [ -f "$DASHBOARD_REQ" ]; then
    echo ""
    echo -e "${BLUE}📋 Audit: dashboard/requirements.txt${NC}"
    echo ""
    
    DASHBOARD_AUDIT_CMD="pip-audit --requirement $DASHBOARD_REQ --format $OUTPUT_FORMAT"
    
    if [ "$FIX_VULNERABILITIES" = true ]; then
        DASHBOARD_AUDIT_CMD="$DASHBOARD_AUDIT_CMD --fix"
    fi
    
    if [ -n "$OUTPUT_FILE" ]; then
        DASHBOARD_OUTPUT="${OUTPUT_FILE%.txt}_dashboard.txt"
        DASHBOARD_AUDIT_CMD="$DASHBOARD_AUDIT_CMD --output $DASHBOARD_OUTPUT"
    fi
    
    DASHBOARD_AUDIT_CMD="$DASHBOARD_AUDIT_CMD $EXTRA_ARGS"
    
    if eval $DASHBOARD_AUDIT_CMD; then
        echo ""
        echo -e "${GREEN}✅ Aucune vulnérabilité détectée dans dashboard/requirements.txt${NC}"
        DASHBOARD_STATUS=0
    else
        DASHBOARD_STATUS=$?
        echo ""
        echo -e "${RED}❌ Vulnérabilités trouvées dans dashboard/requirements.txt${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}========================================${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}📊 Résumé de l'Audit${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $ROOT_STATUS -eq 0 ] && [ ${DASHBOARD_STATUS:-0} -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les fichiers requirements.txt sont sécurisés${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Des vulnérabilités ont été détectées${NC}"
    echo ""
    echo -e "${YELLOW}💡 Actions recommandées:${NC}"
    echo "   1. Examiner les vulnérabilités ci-dessus"
    echo "   2. Mettre à jour les packages vulnérables:"
    echo "      pip install --upgrade <package-name>"
    echo "   3. Ou utiliser l'option --fix:"
    echo "      ./scripts/audit_dependencies.sh --fix"
    echo ""
    exit 1
fi
