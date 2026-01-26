# Guide de déploiement Kubernetes - E-Commerce A/B Test Dashboard

## Prérequis

- Cluster Kubernetes fonctionnel (minikube, kind, AKS, EKS, GKE, etc.)
- `kubectl` configuré
- Docker pour construire les images

## Étape 1: Construire les images Docker

```bash
# Image du dashboard
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .

# Image de l'exporter
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Si vous utilisez un registry privé, tag et push
docker tag ecommerce-dashboard:latest your-registry.com/ecommerce-dashboard:latest
docker push your-registry.com/ecommerce-dashboard:latest

docker tag ecommerce-exporter:latest your-registry.com/ecommerce-exporter:latest
docker push your-registry.com/ecommerce-exporter:latest
```

## Étape 2: Créer le namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

## Étape 3: Déployer les secrets et ConfigMaps

```bash
# IMPORTANT: Modifiez les mots de passe dans secrets.yaml avant de déployer!
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml
```

## Étape 4: Créer les PersistentVolumeClaims

```bash
kubectl apply -f k8s/persistentvolumes.yaml

# Vérifier que les PVC sont créés
kubectl get pvc -n ecommerce-abtest
```

## Étape 5: Déployer la base de données PostgreSQL

```bash
# Créer le ConfigMap avec les scripts d'initialisation
kubectl create configmap postgres-init-scripts \
  --from-file=./scripts/init_db.sql \
  -n ecommerce-abtest

# Déployer PostgreSQL
kubectl apply -f k8s/postgres-deployment.yaml

# Vérifier le statut
kubectl get pods -n ecommerce-abtest -l app=postgres
kubectl logs -n ecommerce-abtest -l app=postgres
```

## Étape 6: Déployer le monitoring (Prometheus, Grafana, Exporters)

```bash
# Prometheus
kubectl apply -f k8s/prometheus-deployment.yaml

# Grafana
kubectl apply -f k8s/grafana-deployment.yaml

# Exporters
kubectl apply -f k8s/exporters-deployment.yaml

# Vérifier
kubectl get pods -n ecommerce-abtest -l tier=monitoring
```

## Étape 7: Déployer le Dashboard

```bash
kubectl apply -f k8s/dashboard-deployment.yaml

# Vérifier
kubectl get pods -n ecommerce-abtest -l app=dashboard
kubectl get svc -n ecommerce-abtest
```

## Étape 8: Configurer l'Ingress (optionnel)

Si vous utilisez un Ingress controller (NGINX, Traefik, etc.):

```bash
# Installer NGINX Ingress Controller si nécessaire
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

# Modifier ingress.yaml avec vos domaines
kubectl apply -f k8s/ingress.yaml
```

## Accès aux services

### Avec LoadBalancer:

```bash
# Dashboard
kubectl get svc dashboard -n ecommerce-abtest
# Accéder via l'EXTERNAL-IP

# Grafana
kubectl get svc grafana -n ecommerce-abtest
```

### Avec Port-Forward (pour test local):

```bash
# Dashboard
kubectl port-forward -n ecommerce-abtest svc/dashboard 8050:80

# Grafana
kubectl port-forward -n ecommerce-abtest svc/grafana 3000:80

# Prometheus
kubectl port-forward -n ecommerce-abtest svc/prometheus 9090:9090
```

## Commandes utiles

### Vérifier l'état des déploiements

```bash
kubectl get all -n ecommerce-abtest
kubectl get pods -n ecommerce-abtest -w
```

### Voir les logs

```bash
# Dashboard
kubectl logs -n ecommerce-abtest -l app=dashboard -f

# PostgreSQL
kubectl logs -n ecommerce-abtest -l app=postgres -f

# Prometheus
kubectl logs -n ecommerce-abtest -l app=prometheus -f
```

### Scaling

```bash
# Augmenter le nombre de réplicas du dashboard
kubectl scale deployment dashboard -n ecommerce-abtest --replicas=3
```

### Mettre à jour une image

```bash
kubectl set image deployment/dashboard dashboard=ecommerce-dashboard:v2 -n ecommerce-abtest
kubectl rollout status deployment/dashboard -n ecommerce-abtest
```

### Redémarrer un déploiement

```bash
kubectl rollout restart deployment/dashboard -n ecommerce-abtest
```

## Configuration spécifique par environnement

### Minikube

```bash
# Démarrer minikube
minikube start --memory=4096 --cpus=2

# Activer l'addon ingress
minikube addons enable ingress

# Obtenir l'IP de minikube
minikube ip

# Ajouter à /etc/hosts (Linux/Mac) ou C:\Windows\System32\drivers\etc\hosts (Windows)
<minikube-ip> dashboard.example.com
<minikube-ip> grafana.example.com
```

### Kind (Kubernetes in Docker)

```bash
# Créer un cluster
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF

# Installer NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

### Cloud Provider (AWS EKS, Azure AKS, Google GKE)

Adapter le `storageClassName` dans `persistentvolumes.yaml`:

- AWS EKS: `gp2` ou `gp3`
- Azure AKS: `managed-premium` ou `default`
- Google GKE: `standard-rwo` ou `premium-rwo`

## Nettoyage

```bash
# Supprimer tous les ressources
kubectl delete namespace ecommerce-abtest

# Ou supprimer individuellement
kubectl delete -f k8s/dashboard-deployment.yaml
kubectl delete -f k8s/grafana-deployment.yaml
kubectl delete -f k8s/prometheus-deployment.yaml
kubectl delete -f k8s/exporters-deployment.yaml
kubectl delete -f k8s/postgres-deployment.yaml
kubectl delete -f k8s/persistentvolumes.yaml
kubectl delete -f k8s/configmaps.yaml
kubectl delete -f k8s/secrets.yaml
kubectl delete -f k8s/namespace.yaml
```

## Monitoring et Debug

### Vérifier les ressources

```bash
kubectl top pods -n ecommerce-abtest
kubectl top nodes
```

### Exécuter des commandes dans un pod

```bash
# Accéder à PostgreSQL
kubectl exec -it -n ecommerce-abtest deployment/postgres -- psql -U dashuser -d ecommerce_db

# Shell dans le dashboard
kubectl exec -it -n ecommerce-abtest deployment/dashboard -- /bin/bash
```

### Voir les événements

```bash
kubectl get events -n ecommerce-abtest --sort-by='.lastTimestamp'
```

## Sécurité

1. **Changer tous les mots de passe par défaut** dans `secrets.yaml`
2. Utiliser des **Secrets chiffrés** (sealed-secrets, SOPS, etc.)
3. Activer **Network Policies** pour isoler les pods
4. Configurer **RBAC** pour limiter les accès
5. Scanner les images avec **Trivy** ou **Snyk**
6. Utiliser **Pod Security Policies** ou **Pod Security Standards**

## Production Checklist

- [ ] Mots de passe sécurisés et gérés par un gestionnaire de secrets
- [ ] Limites de ressources configurées
- [ ] Health checks configurés
- [ ] Backup automatique de PostgreSQL configuré
- [ ] Monitoring et alertes configurés (Prometheus AlertManager)
- [ ] Logs centralisés (Loki, ELK, etc.)
- [ ] TLS/SSL configuré sur l'Ingress
- [ ] Network Policies activées
- [ ] RBAC configuré
- [ ] Images stockées dans un registry privé sécurisé
