# Script de test rapide Kubernetes Local (PowerShell)
# E-Commerce A/B Test Dashboard

param(
    [string]$ClusterType = "minikube"  # minikube, docker-desktop, kind
)

Write-Host "🚀 Test Kubernetes Local - E-Commerce Dashboard" -ForegroundColor Green
Write-Host "Cluster: $ClusterType" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Green

$NAMESPACE = "ecommerce-abtest"

# Vérifier kubectl
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl non installé. Installez-le: choco install kubernetes-cli" -ForegroundColor Red
    exit 1
}

# Démarrer le cluster selon le type
switch ($ClusterType) {
    "minikube" {
        Write-Host "`n📦 Démarrage de Minikube..." -ForegroundColor Cyan
        minikube start --memory=4096 --cpus=2 --driver=docker
        
        Write-Host "`n🐳 Configuration Docker pour Minikube..." -ForegroundColor Cyan
        & minikube docker-env | Invoke-Expression
    }
    "kind" {
        Write-Host "`n📦 Création du cluster Kind..." -ForegroundColor Cyan
        kind create cluster --name ecommerce-local --config k8s/kind-config.yaml
    }
    "docker-desktop" {
        Write-Host "`n✅ Utilisation de Docker Desktop Kubernetes" -ForegroundColor Cyan
        Write-Host "Assurez-vous que Kubernetes est activé dans Docker Desktop!" -ForegroundColor Yellow
    }
}

# Vérifier la connexion
Write-Host "`n🔍 Vérification du cluster..." -ForegroundColor Cyan
kubectl cluster-info
kubectl get nodes

# Construire les images
Write-Host "`n🏗️ Construction des images Docker..." -ForegroundColor Cyan
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Créer le namespace
Write-Host "`n📁 Création du namespace..." -ForegroundColor Cyan
kubectl apply -f k8s/namespace.yaml

# Secrets et ConfigMaps
Write-Host "`n🔐 Configuration secrets et ConfigMaps..." -ForegroundColor Cyan
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml

# ConfigMap pour PostgreSQL init
Write-Host "`n📝 Script d'initialisation PostgreSQL..." -ForegroundColor Cyan
kubectl create configmap postgres-init-scripts `
  --from-file=.\scripts\init_db.sql `
  -n $NAMESPACE `
  --dry-run=client -o yaml | kubectl apply -f -

# PVCs
Write-Host "`n💾 Création des volumes..." -ForegroundColor Cyan
kubectl apply -f k8s/persistentvolumes.yaml
Start-Sleep -Seconds 5

# PostgreSQL
Write-Host "`n🐘 Déploiement PostgreSQL..." -ForegroundColor Cyan
kubectl apply -f k8s/postgres-deployment.yaml
Write-Host "⏳ Attente de PostgreSQL..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s

# Dashboard
Write-Host "`n🎨 Déploiement Dashboard..." -ForegroundColor Cyan
kubectl apply -f k8s/dashboard-deployment.yaml
Write-Host "⏳ Attente du Dashboard..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=dashboard -n $NAMESPACE --timeout=300s

# Prometheus (optionnel)
$deployMonitoring = Read-Host "`nDéployer Prometheus et Grafana? (y/n)"
if ($deployMonitoring -eq 'y' -or $deployMonitoring -eq 'Y') {
    Write-Host "`n📊 Déploiement Monitoring..." -ForegroundColor Cyan
    kubectl apply -f k8s/prometheus-deployment.yaml
    kubectl apply -f k8s/grafana-deployment.yaml
    kubectl apply -f k8s/exporters-deployment.yaml
}

# État final
Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "✅ Déploiement terminé!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

Write-Host "`n📋 État des pods:" -ForegroundColor Cyan
kubectl get pods -n $NAMESPACE

Write-Host "`n🌐 Services:" -ForegroundColor Cyan
kubectl get svc -n $NAMESPACE

# Instructions d'accès
Write-Host "`n🔗 Pour accéder aux services:" -ForegroundColor Cyan

switch ($ClusterType) {
    "minikube" {
        Write-Host "`nDashboard:" -ForegroundColor White
        Write-Host "  minikube service dashboard -n $NAMESPACE" -ForegroundColor Yellow
        Write-Host "OU" -ForegroundColor White
        Write-Host "  kubectl port-forward -n $NAMESPACE svc/dashboard 8050:80" -ForegroundColor Yellow
        Write-Host "  http://localhost:8050" -ForegroundColor Cyan
        
        if ($deployMonitoring -eq 'y') {
            Write-Host "`nGrafana:" -ForegroundColor White
            Write-Host "  kubectl port-forward -n $NAMESPACE svc/grafana 3000:80" -ForegroundColor Yellow
            Write-Host "  http://localhost:3000 (admin/admin123)" -ForegroundColor Cyan
            
            Write-Host "`nPrometheus:" -ForegroundColor White
            Write-Host "  kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090" -ForegroundColor Yellow
            Write-Host "  http://localhost:9090" -ForegroundColor Cyan
        }
    }
    default {
        Write-Host "`nDashboard:" -ForegroundColor White
        Write-Host "  kubectl port-forward -n $NAMESPACE svc/dashboard 8050:80" -ForegroundColor Yellow
        Write-Host "  http://localhost:8050" -ForegroundColor Cyan
        
        if ($deployMonitoring -eq 'y') {
            Write-Host "`nGrafana:" -ForegroundColor White
            Write-Host "  kubectl port-forward -n $NAMESPACE svc/grafana 3000:80" -ForegroundColor Yellow
            Write-Host "  http://localhost:3000 (admin/admin123)" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n📝 Commandes utiles:" -ForegroundColor Cyan
Write-Host "  • Voir les logs: kubectl logs -n $NAMESPACE -l app=dashboard -f" -ForegroundColor White
Write-Host "  • Shell dans un pod: kubectl exec -it -n $NAMESPACE deployment/dashboard -- /bin/bash" -ForegroundColor White
Write-Host "  • Scaler: kubectl scale deployment dashboard -n $NAMESPACE --replicas=3" -ForegroundColor White
Write-Host "  • État complet: kubectl get all -n $NAMESPACE" -ForegroundColor White
Write-Host "  • Supprimer tout: kubectl delete namespace $NAMESPACE" -ForegroundColor White

if ($ClusterType -eq "minikube") {
    Write-Host "`n🛑 Pour arrêter Minikube:" -ForegroundColor Cyan
    Write-Host "  minikube stop" -ForegroundColor White
}

Write-Host "`n🎉 Test Kubernetes prêt!" -ForegroundColor Green
Write-Host "📚 Voir k8s/LOCAL_TEST.md pour plus de détails" -ForegroundColor Yellow
