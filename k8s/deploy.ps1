# Script de déploiement rapide Kubernetes pour Windows PowerShell
# E-Commerce A/B Test Dashboard

$NAMESPACE = "ecommerce-abtest"
$REGISTRY = $env:DOCKER_REGISTRY  # Définir votre registry Docker

Write-Host "🚀 Déploiement du E-Commerce A/B Test Dashboard sur Kubernetes" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

# Vérifier que kubectl est installé
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl n'est pas installé. Installez-le d'abord." -ForegroundColor Red
    exit 1
}

# Vérifier la connexion au cluster
try {
    kubectl cluster-info | Out-Null
    Write-Host "✅ Cluster Kubernetes détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Impossible de se connecter au cluster Kubernetes" -ForegroundColor Red
    exit 1
}

# Étape 1: Construire les images Docker
Write-Host "`n📦 Construction des images Docker..." -ForegroundColor Cyan
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Si un registry est défini, tag et push
if ($REGISTRY) {
    Write-Host "📤 Push des images vers $REGISTRY..." -ForegroundColor Cyan
    docker tag ecommerce-dashboard:latest "$REGISTRY/ecommerce-dashboard:latest"
    docker tag ecommerce-exporter:latest "$REGISTRY/ecommerce-exporter:latest"
    docker push "$REGISTRY/ecommerce-dashboard:latest"
    docker push "$REGISTRY/ecommerce-exporter:latest"
}

# Étape 2: Créer le namespace
Write-Host "`n📁 Création du namespace $NAMESPACE..." -ForegroundColor Cyan
kubectl apply -f k8s/namespace.yaml

# Étape 3: Créer les secrets et ConfigMaps
Write-Host "`n🔐 Déploiement des secrets et ConfigMaps..." -ForegroundColor Cyan
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml

# Créer le ConfigMap pour les scripts d'initialisation PostgreSQL
Write-Host "📝 Création du ConfigMap pour les scripts PostgreSQL..." -ForegroundColor Cyan
kubectl create configmap postgres-init-scripts `
  --from-file=.\scripts\init_db.sql `
  -n $NAMESPACE `
  --dry-run=client -o yaml | kubectl apply -f -

# Étape 4: Créer les PVCs
Write-Host "`n💾 Création des PersistentVolumeClaims..." -ForegroundColor Cyan
kubectl apply -f k8s/persistentvolumes.yaml

# Attendre que les PVCs soient bound
Write-Host "⏳ Attente de la création des PVCs..." -ForegroundColor Yellow
kubectl wait --for=condition=Bound pvc --all -n $NAMESPACE --timeout=120s

# Étape 5: Déployer PostgreSQL
Write-Host "`n🐘 Déploiement de PostgreSQL..." -ForegroundColor Cyan
kubectl apply -f k8s/postgres-deployment.yaml

# Attendre que PostgreSQL soit prêt
Write-Host "⏳ Attente du démarrage de PostgreSQL..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s

# Étape 6: Déployer Prometheus
Write-Host "`n📊 Déploiement de Prometheus..." -ForegroundColor Cyan
kubectl apply -f k8s/prometheus-deployment.yaml

# Étape 7: Déployer les exporters
Write-Host "`n📈 Déploiement des exporters..." -ForegroundColor Cyan
kubectl apply -f k8s/exporters-deployment.yaml

# Étape 8: Déployer Grafana
Write-Host "`n📉 Déploiement de Grafana..." -ForegroundColor Cyan
kubectl apply -f k8s/grafana-deployment.yaml

# Étape 9: Déployer le Dashboard
Write-Host "`n🎨 Déploiement du Dashboard..." -ForegroundColor Cyan
kubectl apply -f k8s/dashboard-deployment.yaml

# Attendre que le dashboard soit prêt
Write-Host "⏳ Attente du démarrage du Dashboard..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=dashboard -n $NAMESPACE --timeout=300s

# Optionnel: Déployer l'Ingress
$deployIngress = Read-Host "Voulez-vous déployer l'Ingress? (y/n)"
if ($deployIngress -eq 'y' -or $deployIngress -eq 'Y') {
    Write-Host "🌐 Déploiement de l'Ingress..." -ForegroundColor Cyan
    kubectl apply -f k8s/ingress.yaml
}

# Afficher l'état final
Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "✅ Déploiement terminé!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

Write-Host "`n📋 État des pods:" -ForegroundColor Cyan
kubectl get pods -n $NAMESPACE

Write-Host "`n🌐 Services:" -ForegroundColor Cyan
kubectl get svc -n $NAMESPACE

Write-Host "`n🔗 Accès aux applications:" -ForegroundColor Cyan

# Obtenir l'IP externe du dashboard
$DASHBOARD_IP = kubectl get svc dashboard -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
if ($DASHBOARD_IP) {
    Write-Host "  📊 Dashboard: http://$DASHBOARD_IP" -ForegroundColor White
} else {
    Write-Host "  📊 Dashboard: kubectl port-forward -n $NAMESPACE svc/dashboard 8050:80" -ForegroundColor White
}

# Obtenir l'IP externe de Grafana
$GRAFANA_IP = kubectl get svc grafana -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
if ($GRAFANA_IP) {
    Write-Host "  📉 Grafana: http://$GRAFANA_IP (admin/admin123)" -ForegroundColor White
} else {
    Write-Host "  📉 Grafana: kubectl port-forward -n $NAMESPACE svc/grafana 3000:80" -ForegroundColor White
}

Write-Host "  📊 Prometheus: kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090" -ForegroundColor White

Write-Host "`n📝 Commandes utiles:" -ForegroundColor Cyan
Write-Host "  • Voir les logs du dashboard: kubectl logs -n $NAMESPACE -l app=dashboard -f" -ForegroundColor White
Write-Host "  • Voir tous les pods: kubectl get pods -n $NAMESPACE" -ForegroundColor White
Write-Host "  • Scaler le dashboard: kubectl scale deployment dashboard -n $NAMESPACE --replicas=3" -ForegroundColor White

Write-Host "`n🎉 Déploiement réussi!" -ForegroundColor Green
