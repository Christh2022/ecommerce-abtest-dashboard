# Configuration Helm pour le déploiement Kubernetes (optionnel)
# Si vous préférez utiliser Helm, créez un chart Helm

# Structure d'un chart Helm:
# ecommerce-abtest-chart/
#   Chart.yaml
#   values.yaml
#   templates/
#     namespace.yaml
#     configmap.yaml
#     secret.yaml
#     postgres-deployment.yaml
#     dashboard-deployment.yaml
#     etc...

# Pour créer un chart Helm:
# helm create ecommerce-abtest-chart

# Voir k8s/README.md pour les instructions complètes
