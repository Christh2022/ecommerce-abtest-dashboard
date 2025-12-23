#!/bin/bash
# Script de configuration du firewall Docker
# Ce script configure iptables pour restreindre l'accès aux services Docker

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🔒 Configuration Firewall Docker${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Vérifier les privilèges root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    echo "Usage: sudo ./scripts/configure_firewall.sh"
    exit 1
fi

# Configuration
DOCKER_NETWORK="172.20.0.0/16"
ALLOWED_HOSTS_FILE="./config/allowed_hosts.txt"
LOCALHOST="127.0.0.1"

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "  Réseau Docker: $DOCKER_NETWORK"
echo "  Fichier hôtes autorisés: $ALLOWED_HOSTS_FILE"
echo ""

# Créer une chaîne Docker personnalisée
echo -e "${BLUE}1. Création de la chaîne DOCKER-USER personnalisée...${NC}"

# Nettoyer les règles existantes de la chaîne DOCKER-USER
iptables -F DOCKER-USER 2>/dev/null || true

# Règle par défaut: ACCEPTER le trafic entrant (sera restreint plus tard)
iptables -A DOCKER-USER -j RETURN

echo -e "${GREEN}✅ Chaîne DOCKER-USER configurée${NC}"
echo ""

# Bloquer les ports d'administration par défaut
echo -e "${BLUE}2. Restriction des ports d'administration...${NC}"

# Bloquer PostgreSQL (5432) depuis l'extérieur - seulement localhost autorisé
iptables -I DOCKER-USER -p tcp --dport 5432 ! -s $LOCALHOST -j DROP
echo -e "${GREEN}✅ Port 5432 (PostgreSQL) - Accès restreint à localhost${NC}"

# Bloquer Prometheus (9090) - seulement localhost
iptables -I DOCKER-USER -p tcp --dport 9090 ! -s $LOCALHOST -j DROP
echo -e "${GREEN}✅ Port 9090 (Prometheus) - Accès restreint à localhost${NC}"

# Bloquer Loki (3100) - seulement localhost
iptables -I DOCKER-USER -p tcp --dport 3100 ! -s $LOCALHOST -j DROP
echo -e "${GREEN}✅ Port 3100 (Loki) - Accès restreint à localhost${NC}"

# Bloquer Postgres Exporter (9187) - seulement réseau Docker
iptables -I DOCKER-USER -p tcp --dport 9187 ! -s $DOCKER_NETWORK -j DROP
echo -e "${GREEN}✅ Port 9187 (Postgres Exporter) - Accès restreint au réseau Docker${NC}"

# Bloquer Custom Exporter (9200) - seulement réseau Docker
iptables -I DOCKER-USER -p tcp --dport 9200 ! -s $DOCKER_NETWORK -j DROP
echo -e "${GREEN}✅ Port 9200 (Custom Exporter) - Accès restreint au réseau Docker${NC}"

echo ""

# Configurer l'accès à Grafana (3000)
echo -e "${BLUE}3. Configuration de l'accès à Grafana (port 3000)...${NC}"

if [ -f "$ALLOWED_HOSTS_FILE" ]; then
    echo -e "${YELLOW}📄 Lecture des hôtes autorisés depuis $ALLOWED_HOSTS_FILE${NC}"
    
    while IFS= read -r host; do
        # Ignorer les lignes vides et les commentaires
        [[ -z "$host" || "$host" =~ ^# ]] && continue
        
        # Autoriser l'hôte spécifié
        iptables -I DOCKER-USER -p tcp --dport 3000 -s "$host" -j ACCEPT
        echo -e "${GREEN}✅ Hôte autorisé pour Grafana: $host${NC}"
    done < "$ALLOWED_HOSTS_FILE"
else
    echo -e "${YELLOW}⚠️  Fichier $ALLOWED_HOSTS_FILE non trouvé${NC}"
    echo -e "${YELLOW}   Autorisation de localhost uniquement${NC}"
fi

# Autoriser localhost pour Grafana
iptables -I DOCKER-USER -p tcp --dport 3000 -s $LOCALHOST -j ACCEPT
echo -e "${GREEN}✅ Localhost autorisé pour Grafana${NC}"

echo ""

# Configurer l'accès au Dashboard Dash (8050)
echo -e "${BLUE}4. Configuration de l'accès au Dashboard (port 8050)...${NC}"

if [ -f "$ALLOWED_HOSTS_FILE" ]; then
    while IFS= read -r host; do
        [[ -z "$host" || "$host" =~ ^# ]] && continue
        
        iptables -I DOCKER-USER -p tcp --dport 8050 -s "$host" -j ACCEPT
        echo -e "${GREEN}✅ Hôte autorisé pour Dashboard: $host${NC}"
    done < "$ALLOWED_HOSTS_FILE"
fi

# Autoriser localhost pour Dashboard
iptables -I DOCKER-USER -p tcp --dport 8050 -s $LOCALHOST -j ACCEPT
echo -e "${GREEN}✅ Localhost autorisé pour Dashboard${NC}"

echo ""

# Protection contre les scans de ports
echo -e "${BLUE}5. Configuration de la protection anti-scan...${NC}"

# Limiter les nouvelles connexions (protection DDoS basique)
iptables -I DOCKER-USER -p tcp --syn -m limit --limit 10/s --limit-burst 20 -j ACCEPT
iptables -I DOCKER-USER -p tcp --syn -j DROP
echo -e "${GREEN}✅ Limite de connexions configurée (10 conn/s, burst 20)${NC}"

# Bloquer les scans SYN
iptables -I DOCKER-USER -p tcp --tcp-flags ALL NONE -j DROP
iptables -I DOCKER-USER -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
iptables -I DOCKER-USER -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
echo -e "${GREEN}✅ Protection contre scans SYN activée${NC}"

echo ""

# Sauvegarder les règles
echo -e "${BLUE}6. Sauvegarde des règles iptables...${NC}"

# Créer le répertoire de sauvegarde
mkdir -p /etc/iptables

# Sauvegarder les règles
if command -v iptables-save &> /dev/null; then
    iptables-save > /etc/iptables/docker-firewall.rules
    echo -e "${GREEN}✅ Règles sauvegardées dans /etc/iptables/docker-firewall.rules${NC}"
else
    echo -e "${YELLOW}⚠️  iptables-save non disponible${NC}"
fi

echo ""

# Afficher les règles configurées
echo -e "${BLUE}7. Règles iptables DOCKER-USER configurées:${NC}"
echo -e "${YELLOW}========================================${NC}"
iptables -L DOCKER-USER -n --line-numbers
echo -e "${YELLOW}========================================${NC}"
echo ""

# Créer un script de restauration
cat > /etc/iptables/restore-docker-firewall.sh << 'RESTORE_SCRIPT'
#!/bin/bash
# Script de restauration automatique des règles firewall Docker
if [ -f /etc/iptables/docker-firewall.rules ]; then
    iptables-restore < /etc/iptables/docker-firewall.rules
    echo "✅ Règles firewall Docker restaurées"
else
    echo "❌ Fichier de règles non trouvé"
    exit 1
fi
RESTORE_SCRIPT

chmod +x /etc/iptables/restore-docker-firewall.sh
echo -e "${GREEN}✅ Script de restauration créé: /etc/iptables/restore-docker-firewall.sh${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Configuration du firewall terminée!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}📋 Résumé de la configuration:${NC}"
echo "  • Port 5432 (PostgreSQL) - Localhost uniquement"
echo "  • Port 9090 (Prometheus) - Localhost uniquement"
echo "  • Port 3100 (Loki) - Localhost uniquement"
echo "  • Port 9187 (Postgres Exporter) - Réseau Docker uniquement"
echo "  • Port 9200 (Custom Exporter) - Réseau Docker uniquement"
echo "  • Port 3000 (Grafana) - Hôtes autorisés + localhost"
echo "  • Port 8050 (Dashboard) - Hôtes autorisés + localhost"
echo "  • Protection anti-scan activée"
echo "  • Limite de connexions: 10/s (burst 20)"
echo ""
echo -e "${YELLOW}💡 Pour restaurer les règles après redémarrage:${NC}"
echo "   sudo /etc/iptables/restore-docker-firewall.sh"
echo ""
echo -e "${YELLOW}💡 Pour voir les règles actuelles:${NC}"
echo "   sudo iptables -L DOCKER-USER -n --line-numbers"
echo ""
echo -e "${YELLOW}💡 Pour supprimer toutes les règles:${NC}"
echo "   sudo iptables -F DOCKER-USER"
echo ""
