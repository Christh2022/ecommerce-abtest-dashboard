#!/bin/bash

# Script de déploiement rapide Kubernetes
# E-Commerce A/B Test Dashboard

set -e

NAMESPACE="ecommerce-abtest"
REGISTRY="${DOCKER_REGISTRY:-}"  # Définir votre registry Docker

echo "🚀 Déploiement du E-Commerce A/B Test Dashboard sur Kubernetes"
echo "=============================================================="

# Vérifier que kubectl est installé
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl n'est pas installé. Installez-le d'abord."
    exit 1
fi

# Vérifier la connexion au cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Impossible de se connecter au cluster Kubernetes"
    exit 1
fi

echo "✅ Cluster Kubernetes détecté"

# Étape 1: Construire les images Docker
echo ""
echo "📦 Construction des images Docker..."
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Si un registry est défini, tag et push
if [ -n "$REGISTRY" ]; then
    echo "📤 Push des images vers $REGISTRY..."
    docker tag ecommerce-dashboard:latest $REGISTRY/ecommerce-dashboard:latest
    docker tag ecommerce-exporter:latest $REGISTRY/ecommerce-exporter:latest
    docker push $REGISTRY/ecommerce-dashboard:latest
    docker push $REGISTRY/ecommerce-exporter:latest
fi

# Étape 2: Créer le namespace
echo ""
echo "📁 Création du namespace $NAMESPACE..."
kubectl apply -f k8s/namespace.yaml

# Étape 3: Créer les secrets et ConfigMaps
echo ""
echo "🔐 Déploiement des secrets et ConfigMaps..."
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml

# Créer le ConfigMap pour les scripts d'initialisation PostgreSQL
echo "📝 Création du ConfigMap pour les scripts PostgreSQL..."
kubectl create configmap postgres-init-scripts \
  --from-file=./scripts/init_db.sql \
  -n $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

# Étape 4: Créer les PVCs
echo ""
echo "💾 Création des PersistentVolumeClaims..."
kubectl apply -f k8s/persistentvolumes.yaml

# Attendre que les PVCs soient bound
echo "⏳ Attente de la création des PVCs..."
kubectl wait --for=condition=Bound pvc --all -n $NAMESPACE --timeout=120s || true

# Étape 5: Déployer PostgreSQL
echo ""
echo "🐘 Déploiement de PostgreSQL..."
kubectl apply -f k8s/postgres-deployment.yaml

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente du démarrage de PostgreSQL..."
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s

# Étape 6: Déployer Prometheus
echo ""
echo "📊 Déploiement de Prometheus..."
kubectl apply -f k8s/prometheus-deployment.yaml

# Étape 7: Déployer les exporters
echo ""
echo "📈 Déploiement des exporters..."
kubectl apply -f k8s/exporters-deployment.yaml

# Étape 8: Déployer Grafana
echo ""
echo "📉 Déploiement de Grafana..."
kubectl apply -f k8s/grafana-deployment.yaml

# Étape 9: Déployer le Dashboard
echo ""
echo "🎨 Déploiement du Dashboard..."
kubectl apply -f k8s/dashboard-deployment.yaml

# Attendre que le dashboard soit prêt
echo "⏳ Attente du démarrage du Dashboard..."
kubectl wait --for=condition=ready pod -l app=dashboard -n $NAMESPACE --timeout=300s || true

# Optionnel: Déployer l'Ingress
read -p "Voulez-vous déployer l'Ingress? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Déploiement de l'Ingress..."
    kubectl apply -f k8s/ingress.yaml
fi

# Afficher l'état final
echo ""
echo "=============================================================="
echo "✅ Déploiement terminé!"
echo "=============================================================="
echo ""
echo "📋 État des pods:"
kubectl get pods -n $NAMESPACE

echo ""
echo "🌐 Services:"
kubectl get svc -n $NAMESPACE

echo ""
echo "🔗 Accès aux applications:"
echo ""

# Obtenir l'IP externe du dashboard
DASHBOARD_IP=$(kubectl get svc dashboard -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")
if [ "$DASHBOARD_IP" != "pending" ] && [ -n "$DASHBOARD_IP" ]; then
    echo "  📊 Dashboard: http://$DASHBOARD_IP"
else
    echo "  📊 Dashboard: kubectl port-forward -n $NAMESPACE svc/dashboard 8050:80"
fi

# Obtenir l'IP externe de Grafana
GRAFANA_IP=$(kubectl get svc grafana -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")
if [ "$GRAFANA_IP" != "pending" ] && [ -n "$GRAFANA_IP" ]; then
    echo "  📉 Grafana: http://$GRAFANA_IP (admin/admin123)"
else
    echo "  📉 Grafana: kubectl port-forward -n $NAMESPACE svc/grafana 3000:80"
fi

echo "  📊 Prometheus: kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090"

echo ""
echo "📝 Commandes utiles:"
echo "  • Voir les logs du dashboard: kubectl logs -n $NAMESPACE -l app=dashboard -f"
echo "  • Voir tous les pods: kubectl get pods -n $NAMESPACE"
echo "  • Scaler le dashboard: kubectl scale deployment dashboard -n $NAMESPACE --replicas=3"
echo ""
echo "🎉 Déploiement réussi!"
