#!/bin/bash
# Test de résistance DDoS sur application locale
# AVERTISSEMENT: Utilisez UNIQUEMENT sur vos propres systèmes !

TARGET="http://localhost:8050"
THREADS=100
DURATION=60  # secondes

echo "🎯 TEST DE RÉSISTANCE DDoS"
echo "=========================="
echo "Target: $TARGET"
echo "Threads: $THREADS"
echo "Duration: ${DURATION}s"
echo ""
echo "⚠️  ATTENTION: Test sur VOTRE système uniquement!"
echo "Press Ctrl+C to stop"
echo ""
sleep 3

# Fonction d'attaque HTTP Flood
http_flood() {
    local id=$1
    local count=0
    local start_time=$(date +%s)
    
    while [ $(($(date +%s) - start_time)) -lt $DURATION ]; do
        curl -s -o /dev/null "$TARGET" 2>&1
        ((count++))
    done
    
    echo "Thread $id: $count requests sent"
}

# Lancer les threads
echo "[*] Lancement de $THREADS threads d'attaque..."
for i in $(seq 1 $THREADS); do
    http_flood $i &
done

# Attendre la fin
echo "[*] Attaque en cours pendant ${DURATION}s..."
sleep $DURATION

# Nettoyer
echo ""
echo "[*] Arrêt de l'attaque..."
pkill -P $$ 2>/dev/null

echo ""
echo "✅ Test terminé!"
echo ""
echo "Vérifications à faire:"
echo "1. L'application répond-elle encore?"
echo "2. Vérifier les logs: docker logs ecommerce-dashboard --tail 100"
echo "3. Vérifier Grafana pour les métriques"
echo "4. Vérifier la mémoire: docker stats ecommerce-dashboard --no-stream"
