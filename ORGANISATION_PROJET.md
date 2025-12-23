# 📁 Organisation du Projet E-commerce A/B Test Dashboard

## 🎯 Vue d'Ensemble

Ce document décrit la nouvelle structure organisée du projet pour une meilleure maintenabilité et clarté.

## 📂 Structure des Dossiers

```
ecommerce-abtest-dashboard/
│
├── 📊 grafana_dashboards_scripts/    # Scripts de création de dashboards Grafana
│   ├── create_dashboards_1_3.py
│   ├── create_dashboards_4_6.py
│   ├── create_bi_dashboard.py
│   ├── create_full_dashboard.py
│   ├── create_monitoring_dashboard.py
│   ├── create_prometheus_dashboard.py
│   ├── __init__.py
│   └── README.md
│
├── 🐳 docker/                        # Dockerfiles
│   ├── Dockerfile                    # Application Dash principale
│   ├── Dockerfile.exporter          # Exporteur Prometheus
│   ├── Dockerfile.dashboard-init    # Initialisation dashboards Grafana
│   └── README.md
│
├── 🔧 bin/                           # Scripts exécutables
│   ├── run_all_dashboards.bat       # Windows: créer tous les dashboards
│   ├── run_all_dashboards.sh        # Unix: créer tous les dashboards
│   ├── run_tests.bat                # Windows: exécuter les tests
│   ├── run_tests.sh                 # Unix: exécuter les tests
│   └── README.md
│
├── 🛠️ tools/                         # Utilitaires Python
│   ├── ecommerce_exporter.py        # Exporteur Prometheus
│   ├── import_dashboard.py          # Import de dashboards
│   ├── import_dashboard_to_grafana.py # Import avancé de dashboards
│   ├── validate_dashboard_organization.py # Validation de la structure
│   └── README.md
│
├── 📱 dashboard/                     # Application Dash principale
│   ├── app.py                       # Point d'entrée de l'application
│   ├── auth.py                      # Système d'authentification
│   ├── db.py                        # Connexion base de données
│   ├── ddos_protection.py           # Protection DDoS
│   ├── components/                  # Composants Dash réutilisables
│   ├── pages/                       # Pages de l'application
│   └── assets/                      # CSS, JS, images
│
├── 📊 grafana/                       # Configuration Grafana
│   ├── dashboards/                  # Dashboards JSON
│   ├── provisioning/                # Configuration de provisioning
│   └── README.md
│
├── 🔍 prometheus/                    # Configuration Prometheus
│   └── prometheus.yml
│
├── 📜 loki/                          # Configuration Loki (logs)
│   └── loki-config.yml
│
├── 📝 promtail/                      # Configuration Promtail (collecte logs)
│   ├── promtail-config.yml
│   └── promtail-falco.yml
│
├── 🛡️ falco/                         # Règles de sécurité Falco
│   ├── falco.yaml
│   └── security_attack_rules_v2.yaml
│
├── ☸️ k8s/                           # Déploiement Kubernetes
│   ├── namespace.yaml
│   ├── configmaps.yaml
│   ├── secrets.yaml
│   ├── persistentvolumes.yaml
│   ├── postgres-deployment.yaml
│   ├── prometheus-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── dashboard-deployment.yaml
│   ├── exporters-deployment.yaml
│   ├── ingress.yaml
│   ├── deploy.sh / deploy.ps1
│   └── README.md
│
├── 📜 scripts/                       # Scripts SQL et utilitaires DB
│   ├── init_db.sql
│   ├── create_dashboard_tables.sql
│   ├── load_data.sql
│   ├── import_data_to_postgres.py
│   └── run_migrations.py
│
├── 📦 data/                          # Données
│   └── clean/                       # Données nettoyées
│
├── 📚 docs/                          # Documentation
│   ├── AUTHENTICATION_ARCHITECTURE.md
│   ├── AUTHENTICATION_SETUP.md
│   ├── DATASET.md
│   ├── DDOS_PROTECTION_REPORT.md
│   ├── SECURITY_DOCUMENTATION_SUMMARY.md
│   └── ...
│
├── 📝 Fichiers racine
│   ├── docker-compose.secure.yml    # Orchestration Docker
│   ├── run_all_dashboards.py        # Script principal de création dashboards
│   ├── run_tests.py                 # Script principal de tests
│   ├── requirements.txt             # Dépendances Python
│   ├── README.md                    # Documentation principale
│   ├── SECURITY.md                  # Politique de sécurité
│   └── ORGANISATION_PROJET.md       # Ce fichier
│
└── ⚙️ config/                        # Configuration
    └── allowed_hosts.txt            # Hosts autorisés
```

## 🎯 Logique d'Organisation

### 1. **grafana_dashboards_scripts/** - Scripts Grafana
- **Objectif** : Centraliser tous les scripts de création de dashboards Grafana
- **Avantages** :
  - Séparation claire du code métier
  - Facilite la maintenance des dashboards
  - Scripts modulaires et réutilisables
  - Documentation centralisée

### 2. **docker/** - Dockerfiles
- **Objectif** : Regrouper toutes les définitions d'images Docker
- **Avantages** :
  - Structure claire pour les builds
  - Facilite les références dans docker-compose
  - Simplifie les déploiements K8s
  - Documentation centralisée des images

### 3. **bin/** - Scripts Exécutables
- **Objectif** : Scripts wrapper pour Windows et Unix
- **Avantages** :
  - Point d'entrée clair pour les utilisateurs
  - Support multi-plateforme
  - Abstraction des commandes Python
  - Vérification automatique des dépendances

### 4. **tools/** - Utilitaires
- **Objectif** : Outils Python annexes et utilitaires
- **Avantages** :
  - Séparation entre application et outils
  - Facilite la réutilisation
  - Scripts de maintenance centralisés
  - Validation et monitoring

## 🚀 Flux de Travail

### Démarrage Rapide

1. **Créer tous les dashboards Grafana** :
   ```bash
   # Windows
   bin\run_all_dashboards.bat
   
   # Unix/Mac
   ./bin/run_all_dashboards.sh
   ```

2. **Lancer l'application complète** :
   ```bash
   docker-compose -f docker-compose.secure.yml up -d
   ```

3. **Valider l'organisation** :
   ```bash
   python tools/validate_dashboard_organization.py
   ```

4. **Exécuter les tests** :
   ```bash
   # Windows
   bin\run_tests.bat
   
   # Unix/Mac
   ./bin/run_tests.sh
   ```

### Workflows Communs

#### Créer un nouveau dashboard Grafana
1. Créer un nouveau script dans `grafana_dashboards_scripts/`
2. Suivre le template des scripts existants
3. Mettre à jour `run_all_dashboards.py` si nécessaire
4. Documenter dans `grafana_dashboards_scripts/README.md`

#### Modifier l'image Docker
1. Éditer le Dockerfile approprié dans `docker/`
2. Rebuild avec `docker-compose build <service>`
3. Tester localement
4. Mettre à jour `docker/README.md` si nécessaire

#### Ajouter un nouvel outil
1. Créer le script dans `tools/`
2. Documenter dans `tools/README.md`
3. Ajouter les dépendances dans `requirements.txt`
4. Créer un wrapper dans `bin/` si nécessaire

## 📚 Documentation Complète

### Documentation par Dossier

| Dossier | Documentation | Description |
|---------|--------------|-------------|
| **grafana_dashboards_scripts/** | [README.md](grafana_dashboards_scripts/README.md) | Création et gestion des dashboards |
| **docker/** | [README.md](docker/README.md) | Images Docker et containerisation |
| **bin/** | [README.md](bin/README.md) | Scripts exécutables et wrappers |
| **tools/** | [README.md](tools/README.md) | Utilitaires et scripts de maintenance |
| **k8s/** | [README.md](k8s/README.md) | Déploiement Kubernetes |
| **dashboard/** | [AUTH_README.md](dashboard/AUTH_README.md) | Application Dash et authentification |
| **grafana/** | [README.md](grafana/README.md) | Configuration Grafana |
| **promtail/** | [README.md](promtail/README.md) | Collecte de logs |
| **loki/** | [README.md](loki/README.md) | Agrégation de logs |
| **scripts/** | [README.md](scripts/README.md) | Scripts SQL et migrations |

### Documentation Thématique

| Type | Fichier | Sujet |
|------|---------|-------|
| **Sécurité** | [SECURITY.md](SECURITY.md) | Politique de sécurité |
| **Sécurité** | [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md) | Architecture d'authentification |
| **Sécurité** | [docs/DDOS_PROTECTION_REPORT.md](docs/DDOS_PROTECTION_REPORT.md) | Protection DDoS |
| **Données** | [docs/DATASET.md](docs/DATASET.md) | Structure et description des données |
| **Général** | [README.md](README.md) | Vue d'ensemble du projet |

## 🔧 Commandes Utiles

### Développement

```bash
# Valider la structure du projet
python tools/validate_dashboard_organization.py

# Créer tous les dashboards
python run_all_dashboards.py

# Exécuter les tests
python run_tests.py

# Lancer l'exporteur Prometheus
python tools/ecommerce_exporter.py
```

### Docker

```bash
# Build toutes les images
docker-compose -f docker-compose.secure.yml build

# Lancer tous les services
docker-compose -f docker-compose.secure.yml up -d

# Voir les logs
docker-compose -f docker-compose.secure.yml logs -f

# Rebuild un service spécifique
docker-compose -f docker-compose.secure.yml build dashboard
```

### Kubernetes

```bash
# Déployer sur K8s (Unix)
./k8s/deploy.sh

# Déployer sur K8s (Windows)
.\k8s\deploy.ps1

# Test local avec Kind
kind create cluster --config k8s/kind-config.yaml
```

## 🎓 Bonnes Pratiques

### Ajout de Nouveaux Fichiers

1. **Scripts Grafana** → `grafana_dashboards_scripts/`
2. **Dockerfiles** → `docker/`
3. **Scripts exécutables** → `bin/` (avec versions .bat et .sh)
4. **Utilitaires Python** → `tools/`
5. **Pages Dash** → `dashboard/pages/`
6. **Composants Dash** → `dashboard/components/`
7. **Scripts SQL** → `scripts/`
8. **Documentation** → `docs/` ou README.md du dossier concerné

### Conventions de Nommage

- **Scripts Python** : `snake_case.py`
- **Scripts Shell** : `kebab-case.sh`
- **Scripts Batch** : `kebab-case.bat`
- **Documentation** : `UPPERCASE_WITH_UNDERSCORES.md`
- **Dossiers** : `lowercase_with_underscores/`

### Git Workflow

```bash
# Avant chaque commit
python tools/validate_dashboard_organization.py
python run_tests.py

# Commit avec message descriptif
git add .
git commit -m "feat: ajout du dashboard XYZ"
git push
```

## 🔍 Validation

Pour valider que l'organisation du projet est correcte :

```bash
python tools/validate_dashboard_organization.py
```

Ce script vérifie :
- ✅ Présence des dossiers requis
- ✅ Présence des fichiers essentiels
- ✅ Structure correcte des fichiers
- ✅ Références dans docker-compose.yml
- ✅ Documentation complète

## 📞 Support

Pour toute question sur l'organisation du projet :
1. Consulter la documentation dans chaque dossier
2. Vérifier ce fichier ORGANISATION_PROJET.md
3. Lire le README.md principal
4. Contacter l'équipe de développement

---

**Dernière mise à jour** : Réorganisation complète du projet
**Version** : 2.0
**Statut** : ✅ Production Ready
