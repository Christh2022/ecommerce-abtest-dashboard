# Dockerfiles du Projet E-Commerce A/B Test Dashboard

Ce dossier contient tous les Dockerfiles nécessaires pour construire les images Docker du projet.

## 📦 Fichiers

### 1. `Dockerfile`

**Image principale de l'application Dash**

- **Base**: Python 3.12-slim
- **Port**: 8050
- **Services**: Application Dash interactive avec authentification
- **Utilisation**:
  ```bash
  docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
  ```

**Contenu**:

- Application Dash (dashboard/)
- Pages et composants interactifs
- Système d'authentification
- Protection DDoS
- Assets et visualizations

### 2. `Dockerfile.exporter`

**Image de l'exporteur Prometheus**

- **Base**: Python 3.11-slim
- **Port**: 9200
- **Services**: Exporteur de métriques Prometheus
- **Utilisation**:
  ```bash
  docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .
  ```

**Contenu**:

- Script tools/ecommerce_exporter.py
- Métriques personnalisées pour Prometheus
- Connexion à PostgreSQL
- Export des KPIs e-commerce

### 3. `Dockerfile.dashboard-init`

**Image d'initialisation des dashboards Grafana**

- **Base**: Python 3.11-slim
- **Services**: Création automatique des dashboards Grafana
- **Utilisation**: Automatique via Docker Compose
- **Exécution**: Une fois au démarrage

**Contenu**:

- Scripts de création de dashboards (grafana_dashboards_scripts/)
- Script d'initialisation (scripts/init_grafana_dashboards.sh)
- Attend que Grafana soit prêt
- Crée les 10 dashboards automatiquement

## 🚀 Utilisation

### Construction des Images

```bash
# Depuis la racine du projet

# Image principale Dash
docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .

# Image de l'exporteur Prometheus
docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .

# Image d'initialisation des dashboards (utilisée automatiquement par Docker Compose)
docker build -t ecommerce-dashboard-init:latest -f docker/Dockerfile.dashboard-init .
```

### Avec Docker Compose

Les Dockerfiles sont référencés automatiquement dans `docker-compose.secure.yml`:

```bash
docker-compose -f docker-compose.secure.yml up -d --build
```

Docker Compose construit automatiquement les images avec les bons Dockerfiles.

## 📋 Structure des Images

### Dockerfile (Application Dash)

```
FROM python:3.12-slim
│
├── Installation des dépendances système
├── Copie des fichiers de l'application
├── Installation des dépendances Python
├── Configuration des utilisateurs et permissions
├── Healthcheck
└── CMD: gunicorn pour servir l'application
```

### Dockerfile.exporter (Exporteur Prometheus)

```
FROM python:3.11-slim
│
├── Installation de psycopg2-binary
├── Copie du script exporter (tools/)
├── Copie des fichiers de données
├── Exposition du port 9200
└── CMD: python ecommerce_exporter.py
```

### Dockerfile.dashboard-init (Init Grafana)

```
FROM python:3.11-slim
│
├── Installation de curl
├── Copie des scripts de dashboards
├── Copie du script d'initialisation
├── Installation des dépendances
└── CMD: Exécution du script d'init
```

## 🔧 Configuration

### Variables d'Environnement

Les Dockerfiles utilisent les variables d'environnement définies dans `docker-compose.secure.yml`:

**Dockerfile (Dash)**:

- `DATABASE_URL`: Connexion PostgreSQL
- `FLASK_DEBUG`: Mode debug (False en production)
- `FLASK_ENV`: Environnement (production)
- `SECRET_KEY`: Clé secrète pour les sessions

**Dockerfile.exporter**:

- `DB_HOST`: Hôte PostgreSQL
- `DB_NAME`: Nom de la base de données
- `DB_USER`: Utilisateur de la base
- `DB_PASSWORD`: Mot de passe

**Dockerfile.dashboard-init**:

- `GRAFANA_URL`: URL de Grafana
- `GRAFANA_USER`: Utilisateur Grafana
- `GRAFANA_PASSWORD`: Mot de passe Grafana

## 📊 Ports Exposés

| Image                     | Port | Service                      |
| ------------------------- | ---- | ---------------------------- |
| Dockerfile                | 8050 | Application Dash             |
| Dockerfile.exporter       | 9200 | Métriques Prometheus         |
| Dockerfile.dashboard-init | -    | Pas de port (init seulement) |

## 🛡️ Sécurité

Toutes les images suivent les bonnes pratiques de sécurité:

- ✅ Images slim pour réduire la surface d'attaque
- ✅ Utilisateur non-root
- ✅ Pas de secrets dans les images
- ✅ Healthchecks pour le monitoring
- ✅ Isolation réseau
- ✅ Volumes pour les données persistantes

## 🔄 Mise à Jour des Images

```bash
# Reconstruire toutes les images
docker-compose -f docker-compose.secure.yml build

# Reconstruire une image spécifique
docker-compose -f docker-compose.secure.yml build dash-app
docker-compose -f docker-compose.secure.yml build prometheus-exporter

# Forcer la reconstruction sans cache
docker-compose -f docker-compose.secure.yml build --no-cache
```

## 📖 Documentation

- [README.md](../README.md) - Documentation principale
- [docker-compose.secure.yml](../docker-compose.secure.yml) - Configuration Docker Compose
- [k8s/README.md](../k8s/README.md) - Déploiement Kubernetes

## 💡 Conseils

1. **Build Context**: Tous les Dockerfiles utilisent la racine du projet comme contexte
2. **Cache Layers**: Organisez vos commandes pour optimiser le cache Docker
3. **Multi-stage**: Considérez les builds multi-stage pour des images plus petites
4. **Tags**: Utilisez des tags de version pour les images en production

## 🐳 Docker Compose

Les services dans `docker-compose.secure.yml` référencent ces Dockerfiles:

```yaml
services:
  dash-app:
    build:
      context: .
      dockerfile: docker/Dockerfile

  prometheus-exporter:
    build:
      context: .
      dockerfile: docker/Dockerfile.exporter

  dashboard-init:
    build:
      context: .
      dockerfile: docker/Dockerfile.dashboard-init
```

## 📝 Changelog

### v1.0.0 (2025-12-23)

- ✅ Organisation des Dockerfiles dans le dossier docker/
- ✅ Documentation complète du dossier
- ✅ Mise à jour des références dans docker-compose.secure.yml
- ✅ Mise à jour des scripts Kubernetes

---

**Note**: Après avoir déplacé les Dockerfiles dans ce dossier, tous les fichiers de configuration ont été mis à jour pour référencer les nouveaux chemins.
