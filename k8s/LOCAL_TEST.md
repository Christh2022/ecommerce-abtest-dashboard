# Guide de Test Kubernetes en Local

# E-Commerce A/B Test Dashboard

## Prérequis

Choisir UNE de ces options:

### Option 1: Minikube (Recommandé)

```bash
# Installation Windows
choco install minikube kubernetes-cli

# Démarrer minikube
minikube start --memory=4096 --cpus=2 --driver=docker

# Vérifier
kubectl get nodes
minikube status
```

### Option 2: Docker Desktop

1. Ouvrir Docker Desktop
2. Settings → Kubernetes → Enable Kubernetes
3. Attendre l'activation (icône verte)
4. Vérifier: `kubectl get nodes`

### Option 3: Kind

```bash
choco install kind kubernetes-cli

# Créer un cluster
kind create cluster --name ecommerce-local --config k8s/kind-config.yaml
```

## Test Rapide - Déploiement Simplifié

### Étape 1: Construire les images localement

```bash
# Pour Minikube - utiliser le Docker de Minikube
minikube docker-env | Invoke-Expression  # PowerShell
# OU
eval $(minikube docker-env)  # Bash

# Construire les images
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Vérifier
docker images | grep ecommerce
```

### Étape 2: Créer le namespace

```bash
kubectl apply -f k8s/namespace.yaml
kubectl get namespaces
```

### Étape 3: Déployer les secrets et configs

```bash
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml

# Vérifier
kubectl get configmaps -n ecommerce-abtest
kubectl get secrets -n ecommerce-abtest
```

### Étape 4: Créer les volumes

```bash
kubectl apply -f k8s/persistentvolumes.yaml

# Vérifier - devrait être "Pending" puis "Bound"
kubectl get pvc -n ecommerce-abtest
kubectl get pvc -n ecommerce-abtest --watch
# Ctrl+C pour arrêter le watch
```

### Étape 5: Déployer PostgreSQL

```bash
# Créer le ConfigMap avec le script d'initialisation
kubectl create configmap postgres-init-scripts --from-file=scripts/init_db.sql -n ecommerce-abtest

# Déployer PostgreSQL
kubectl apply -f k8s/postgres-deployment.yaml

# Vérifier le déploiement
kubectl get pods -n ecommerce-abtest -w
# Attendre que le pod soit "Running" et "1/1 Ready"
# Ctrl+C pour arrêter

# Voir les logs
kubectl logs -n ecommerce-abtest -l app=postgres
```

### Étape 6: Tester PostgreSQL

```bash
# Se connecter à PostgreSQL
kubectl exec -it -n ecommerce-abtest deployment/postgres -- psql -U dashuser -d ecommerce_db

# Dans psql, tester:
\dt
SELECT COUNT(*) FROM users;
\q
```

### Étape 7: Déployer le Dashboard

```bash
kubectl apply -f k8s/dashboard-deployment.yaml

# Vérifier
kubectl get pods -n ecommerce-abtest -l app=dashboard
kubectl logs -n ecommerce-abtest -l app=dashboard -f
```

### Étape 8: Accéder au Dashboard

#### Avec Minikube:

```bash
# Option 1: Service URL
minikube service dashboard -n ecommerce-abtest

# Option 2: Port Forward
kubectl port-forward -n ecommerce-abtest svc/dashboard 8050:80

# Ouvrir: http://localhost:8050
```

#### Avec Docker Desktop ou Kind:

```bash
kubectl port-forward -n ecommerce-abtest svc/dashboard 8050:80

# Ouvrir: http://localhost:8050
```

### Étape 9: Déployer le Monitoring (Optionnel)

```bash
# Prometheus
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl port-forward -n ecommerce-abtest svc/prometheus 9090:9090
# Ouvrir: http://localhost:9090

# Grafana
kubectl apply -f k8s/grafana-deployment.yaml
kubectl port-forward -n ecommerce-abtest svc/grafana 3000:80
# Ouvrir: http://localhost:3000 (admin/admin123)

# Exporters
kubectl apply -f k8s/exporters-deployment.yaml
```

## Commandes Utiles pour Debug

### Voir l'état général

```bash
kubectl get all -n ecommerce-abtest
kubectl get pods -n ecommerce-abtest
kubectl get svc -n ecommerce-abtest
kubectl get pvc -n ecommerce-abtest
```

### Voir les logs

```bash
# Logs du dashboard
kubectl logs -n ecommerce-abtest -l app=dashboard -f

# Logs de PostgreSQL
kubectl logs -n ecommerce-abtest -l app=postgres -f

# Logs d'un pod spécifique
kubectl logs -n ecommerce-abtest <pod-name>
```

### Décrire une ressource (voir les events)

```bash
kubectl describe pod -n ecommerce-abtest <pod-name>
kubectl describe pvc -n ecommerce-abtest postgres-pvc
```

### Shell dans un pod

```bash
# Dashboard
kubectl exec -it -n ecommerce-abtest deployment/dashboard -- /bin/bash

# PostgreSQL
kubectl exec -it -n ecommerce-abtest deployment/postgres -- /bin/bash
```

### Voir les événements

```bash
kubectl get events -n ecommerce-abtest --sort-by='.lastTimestamp'
```

### Redémarrer un déploiement

```bash
kubectl rollout restart deployment/dashboard -n ecommerce-abtest
kubectl rollout status deployment/dashboard -n ecommerce-abtest
```

### Scaler un déploiement

```bash
# Augmenter à 3 réplicas
kubectl scale deployment dashboard -n ecommerce-abtest --replicas=3

# Vérifier
kubectl get pods -n ecommerce-abtest -l app=dashboard
```

## Problèmes Courants

### Pod en "ImagePullBackOff"

```bash
# Si les images ne sont pas trouvées
# Solution: Utiliser le Docker de Minikube
minikube docker-env | Invoke-Expression
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .

# OU changer imagePullPolicy dans les deployments
# imagePullPolicy: IfNotPresent
```

### PVC en "Pending"

```bash
# Vérifier le storageClass
kubectl get storageclass

# Pour Minikube, utiliser "standard"
# Pour Docker Desktop, utiliser "hostpath"
# Modifier dans k8s/persistentvolumes.yaml si nécessaire
```

### Pod CrashLoopBackOff

```bash
# Voir les logs
kubectl logs -n ecommerce-abtest <pod-name>
kubectl logs -n ecommerce-abtest <pod-name> --previous

# Voir les events
kubectl describe pod -n ecommerce-abtest <pod-name>
```

## Dashboard Kubernetes (UI Web)

### Installer le Dashboard Kubernetes

```bash
# Déployer le dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Créer un compte admin
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin

# Obtenir le token
kubectl -n kubernetes-dashboard create token dashboard-admin

# Démarrer le proxy
kubectl proxy

# Ouvrir: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
# Coller le token
```

## Nettoyage

### Supprimer tout

```bash
# Supprimer le namespace (supprime tout dedans)
kubectl delete namespace ecommerce-abtest

# OU supprimer individuellement
kubectl delete -f k8s/dashboard-deployment.yaml
kubectl delete -f k8s/postgres-deployment.yaml
kubectl delete -f k8s/persistentvolumes.yaml
# etc...
```

### Arrêter Minikube

```bash
minikube stop
minikube delete  # Supprime complètement le cluster
```

### Supprimer un cluster Kind

```bash
kind delete cluster --name ecommerce-local
```

## Prochaines Étapes

Une fois que vous maîtrisez le local:

1. Tester l'auto-scaling: `kubectl autoscale deployment dashboard --cpu-percent=50 --min=2 --max=5 -n ecommerce-abtest`
2. Tester les mises à jour: construire une nouvelle version et faire un `kubectl set image`
3. Simuler une panne: `kubectl delete pod <pod-name>` et voir qu'il redémarre automatiquement
4. Regarder les métriques: `kubectl top pods -n ecommerce-abtest`

## Ressources Utiles

- Kubernetes Documentation: https://kubernetes.io/docs/
- Minikube: https://minikube.sigs.k8s.io/docs/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- Lens (UI Desktop): https://k8slens.dev/
