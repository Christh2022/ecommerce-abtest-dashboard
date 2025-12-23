# Scripts de Création de Dashboards Grafana

Ce dossier contient tous les scripts Python pour créer automatiquement les dashboards Grafana de l'application e-commerce A/B test.

## Scripts Disponibles

1. **create_dashboards_1_3.py** - Crée les dashboards 1-3 (Funnel, Segmentation, Products)
2. **create_dashboards_4_6.py** - Crée les dashboards 4-6 (Cohorts, Real-Time, Predictive)
3. **create_bi_dashboard.py** - Crée le dashboard Business Intelligence
4. **create_full_dashboard.py** - Crée le dashboard complet E-Commerce A/B Test Analytics
5. **create_monitoring_dashboard.py** - Crée le dashboard de monitoring
6. **create_prometheus_dashboard.py** - Crée le dashboard Prometheus

## Utilisation

### Exécution Individuelle

```bash
# Depuis le dossier racine du projet
python grafana_dashboards_scripts/create_dashboards_1_3.py
python grafana_dashboards_scripts/create_dashboards_4_6.py
python grafana_dashboards_scripts/create_bi_dashboard.py
python grafana_dashboards_scripts/create_full_dashboard.py
python grafana_dashboards_scripts/create_monitoring_dashboard.py
python grafana_dashboards_scripts/create_prometheus_dashboard.py
```

### Variables d'Environnement

Les scripts utilisent les variables d'environnement suivantes :

- `GRAFANA_URL` - URL de Grafana (défaut: http://localhost:3000)
- `GRAFANA_USER` - Utilisateur Grafana (défaut: admin)
- `GRAFANA_PASSWORD` - Mot de passe Grafana (défaut: admin123)

### Automatisation

Ces scripts sont automatiquement exécutés par :

- Le container `dashboard-init` via Docker Compose
- Le script `scripts/init_grafana_dashboards.sh`

## Prérequis

- Python 3.11+
- Module `requests` installé
- Grafana en cours d'exécution et accessible

## Structure

Tous les scripts suivent le même pattern :

1. Configuration des credentials Grafana via variables d'environnement
2. Définition de la structure JSON du dashboard
3. Envoi de la requête POST à l'API Grafana
4. Validation de la création
