# 📚 INDEX - Documentation Complète

## 🚀 Démarrage Rapide

**Pour commencer rapidement** → [QUICKSTART.md](QUICKSTART.md)

---

## 📖 Documentation par Catégorie

### 🏗️ Architecture et Structure

| Document | Description | Niveau |
|----------|-------------|--------|
| [ORGANISATION_PROJET.md](ORGANISATION_PROJET.md) | Vue complète de la structure du projet | ⭐⭐⭐ |
| [RECAPITULATIF_REORGANISATION.md](RECAPITULATIF_REORGANISATION.md) | Récapitulatif de la réorganisation | ⭐⭐ |
| [README.md](README.md) | Documentation principale du projet | ⭐⭐⭐ |

### 📊 Dashboards Grafana

| Document | Description | Niveau |
|----------|-------------|--------|
| [grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md) | Guide complet des dashboards | ⭐⭐⭐ |
| [GUIDE_DASHBOARDS.md](GUIDE_DASHBOARDS.md) | Guide de développement | ⭐⭐ |
| [MIGRATION_DASHBOARDS.md](MIGRATION_DASHBOARDS.md) | Guide de migration | ⭐ |

### 🐳 Docker et Déploiement

| Document | Description | Niveau |
|----------|-------------|--------|
| [docker/README.md](docker/README.md) | Dockerfiles et containerisation | ⭐⭐⭐ |
| [docker-compose.secure.yml](docker-compose.secure.yml) | Configuration Docker Compose | ⭐⭐ |
| [k8s/README.md](k8s/README.md) | Déploiement Kubernetes | ⭐⭐⭐ |
| [k8s/LOCAL_TEST.md](k8s/LOCAL_TEST.md) | Tests locaux Kubernetes | ⭐⭐ |
| [k8s/HELM.md](k8s/HELM.md) | Déploiement avec Helm | ⭐⭐ |

### 🔧 Scripts et Outils

| Document | Description | Niveau |
|----------|-------------|--------|
| [bin/README.md](bin/README.md) | Scripts exécutables wrapper | ⭐⭐ |
| [tools/README.md](tools/README.md) | Utilitaires Python | ⭐⭐ |
| [scripts/README.md](scripts/README.md) | Scripts SQL et migrations | ⭐⭐ |

### 🔐 Sécurité

| Document | Description | Niveau |
|----------|-------------|--------|
| [SECURITY.md](SECURITY.md) | Politique de sécurité | ⭐⭐⭐ |
| [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md) | Architecture d'authentification | ⭐⭐⭐ |
| [docs/AUTHENTICATION_SETUP.md](docs/AUTHENTICATION_SETUP.md) | Configuration de l'authentification | ⭐⭐ |
| [docs/DDOS_PROTECTION_REPORT.md](docs/DDOS_PROTECTION_REPORT.md) | Protection contre les attaques DDoS | ⭐⭐ |
| [docs/FEATURE_FORCE_PASSWORD_CHANGE.md](docs/FEATURE_FORCE_PASSWORD_CHANGE.md) | Changement de mot de passe forcé | ⭐ |
| [docs/FALCO_ATTACK_DETECTION.md](docs/FALCO_ATTACK_DETECTION.md) | Détection d'intrusions avec Falco | ⭐⭐ |
| [docs/INTRUSION_TEST_RESULTS.md](docs/INTRUSION_TEST_RESULTS.md) | Résultats des tests d'intrusion | ⭐ |
| [dashboard/AUTH_README.md](dashboard/AUTH_README.md) | Authentification de l'application | ⭐⭐ |

### 📊 Données

| Document | Description | Niveau |
|----------|-------------|--------|
| [docs/DATASET.md](docs/DATASET.md) | Description du dataset | ⭐⭐⭐ |
| [scripts/MIGRATIONS.md](scripts/MIGRATIONS.md) | Migrations de base de données | ⭐⭐ |

### 🔍 Monitoring et Observabilité

| Document | Description | Niveau |
|----------|-------------|--------|
| [grafana/README.md](grafana/README.md) | Configuration Grafana | ⭐⭐ |
| [grafana/README_ALERTING.md](grafana/README_ALERTING.md) | Alertes Grafana | ⭐⭐ |
| [promtail/README.md](promtail/README.md) | Collecte de logs avec Promtail | ⭐⭐ |
| [loki/README.md](loki/README.md) | Agrégation de logs avec Loki | ⭐⭐ |
| [falco/README.md](falco/README.md) | Détection de sécurité avec Falco | ⭐⭐ |

### 🎨 Interface et Landing Page

| Document | Description | Niveau |
|----------|-------------|--------|
| [docs/LANDING_PAGE_MODERNE.md](docs/LANDING_PAGE_MODERNE.md) | Design de la landing page | ⭐ |

### 📋 Récapitulatifs

| Document | Description | Niveau |
|----------|-------------|--------|
| [docs/SECURITY_DOCUMENTATION_SUMMARY.md](docs/SECURITY_DOCUMENTATION_SUMMARY.md) | Résumé de la documentation sécurité | ⭐⭐ |

---

## 🎯 Par Cas d'Usage

### Je veux...

#### 🚀 **Démarrer le projet rapidement**
1. [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
2. [README.md](README.md) - Documentation principale
3. Lancer : `docker-compose -f docker-compose.secure.yml up -d`

#### 📊 **Créer ou modifier des dashboards Grafana**
1. [grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md) - Documentation des scripts
2. [GUIDE_DASHBOARDS.md](GUIDE_DASHBOARDS.md) - Guide de développement
3. Créer tous les dashboards : `bin\run_all_dashboards.bat`

#### 🐳 **Déployer avec Docker**
1. [docker/README.md](docker/README.md) - Documentation Docker
2. [docker-compose.secure.yml](docker-compose.secure.yml) - Configuration
3. Build : `docker-compose -f docker-compose.secure.yml build`

#### ☸️ **Déployer sur Kubernetes**
1. [k8s/README.md](k8s/README.md) - Guide Kubernetes
2. [k8s/LOCAL_TEST.md](k8s/LOCAL_TEST.md) - Tests locaux
3. Déployer : `./k8s/deploy.sh` ou `.\k8s\deploy.ps1`

#### 🔐 **Configurer la sécurité**
1. [SECURITY.md](SECURITY.md) - Politique de sécurité
2. [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md) - Architecture
3. [docs/AUTHENTICATION_SETUP.md](docs/AUTHENTICATION_SETUP.md) - Configuration
4. [dashboard/AUTH_README.md](dashboard/AUTH_README.md) - Auth de l'app

#### 📊 **Comprendre les données**
1. [docs/DATASET.md](docs/DATASET.md) - Description complète
2. [scripts/MIGRATIONS.md](scripts/MIGRATIONS.md) - Migrations DB
3. [scripts/README.md](scripts/README.md) - Scripts SQL

#### 🔍 **Mettre en place le monitoring**
1. [grafana/README.md](grafana/README.md) - Configuration Grafana
2. [grafana/README_ALERTING.md](grafana/README_ALERTING.md) - Alertes
3. [tools/README.md](tools/README.md) - Exporteur Prometheus

#### 📝 **Contribuer au projet**
1. [ORGANISATION_PROJET.md](ORGANISATION_PROJET.md) - Structure du projet
2. [RECAPITULATIF_REORGANISATION.md](RECAPITULATIF_REORGANISATION.md) - Réorganisation
3. Valider : `python tools/validate_dashboard_organization.py`

#### 🐛 **Déboguer un problème**
1. [QUICKSTART.md](QUICKSTART.md) - Section "Résolution Rapide"
2. [README.md](README.md) - Troubleshooting
3. Logs : `docker-compose -f docker-compose.secure.yml logs -f`

#### 🛡️ **Tester la sécurité**
1. [docs/INTRUSION_TEST_RESULTS.md](docs/INTRUSION_TEST_RESULTS.md) - Résultats des tests
2. [docs/FALCO_ATTACK_DETECTION.md](docs/FALCO_ATTACK_DETECTION.md) - Détection
3. [docs/DDOS_PROTECTION_REPORT.md](docs/DDOS_PROTECTION_REPORT.md) - Protection DDoS

---

## 📂 Navigation par Dossier

### Structure Principale

```
📁 ecommerce-abtest-dashboard/
│
├── 📊 grafana_dashboards_scripts/   → [README.md](grafana_dashboards_scripts/README.md)
│
├── 🐳 docker/                       → [README.md](docker/README.md)
│
├── 🔧 bin/                          → [README.md](bin/README.md)
│
├── 🛠️ tools/                        → [README.md](tools/README.md)
│
├── 📱 dashboard/                    → [AUTH_README.md](dashboard/AUTH_README.md)
│
├── 📊 grafana/                      → [README.md](grafana/README.md)
│
├── ☸️ k8s/                          → [README.md](k8s/README.md)
│
├── 📜 scripts/                      → [README.md](scripts/README.md)
│
├── 📝 promtail/                     → [README.md](promtail/README.md)
│
├── 📜 loki/                         → [README.md](loki/README.md)
│
├── 🛡️ falco/                        → [README.md](falco/README.md)
│
└── 📚 docs/                         → Voir section "Sécurité" et "Données"
```

---

## 🌟 Documents Essentiels (À Lire en Premier)

### Top 5 - Pour Tout le Monde

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡
   - Guide de démarrage en 5 minutes

2. **[README.md](README.md)** 📖
   - Vue d'ensemble complète du projet

3. **[ORGANISATION_PROJET.md](ORGANISATION_PROJET.md)** 🏗️
   - Structure et organisation

4. **[grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md)** 📊
   - Documentation des dashboards

5. **[SECURITY.md](SECURITY.md)** 🔐
   - Politique de sécurité

### Top 3 - Pour les Développeurs

1. **[docker/README.md](docker/README.md)** 🐳
   - Développement avec Docker

2. **[tools/README.md](tools/README.md)** 🛠️
   - Outils de développement

3. **[GUIDE_DASHBOARDS.md](GUIDE_DASHBOARDS.md)** 📊
   - Développement de dashboards

### Top 3 - Pour les DevOps

1. **[k8s/README.md](k8s/README.md)** ☸️
   - Déploiement Kubernetes

2. **[docker-compose.secure.yml](docker-compose.secure.yml)** 🐳
   - Orchestration Docker

3. **[grafana/README_ALERTING.md](grafana/README_ALERTING.md)** 🔔
   - Alertes et monitoring

---

## 🔍 Recherche Rapide

### Par Mots-Clés

- **Dashboard** → [grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md), [GUIDE_DASHBOARDS.md](GUIDE_DASHBOARDS.md)
- **Docker** → [docker/README.md](docker/README.md), [docker-compose.secure.yml](docker-compose.secure.yml)
- **Kubernetes** → [k8s/README.md](k8s/README.md), [k8s/LOCAL_TEST.md](k8s/LOCAL_TEST.md)
- **Sécurité** → [SECURITY.md](SECURITY.md), [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md)
- **Monitoring** → [grafana/README.md](grafana/README.md), [tools/README.md](tools/README.md)
- **Données** → [docs/DATASET.md](docs/DATASET.md), [scripts/README.md](scripts/README.md)
- **Scripts** → [bin/README.md](bin/README.md), [tools/README.md](tools/README.md)
- **Tests** → [docs/INTRUSION_TEST_RESULTS.md](docs/INTRUSION_TEST_RESULTS.md)

---

## 📊 Légende des Niveaux

- ⭐⭐⭐ **Essentiel** - À lire en priorité
- ⭐⭐ **Important** - À lire pour une compréhension complète
- ⭐ **Optionnel** - Pour des cas spécifiques

---

## 🆘 Besoin d'Aide ?

### Par Ordre de Priorité

1. **[QUICKSTART.md](QUICKSTART.md)** - Résolution rapide
2. **[README.md](README.md)** - FAQ et troubleshooting
3. **Documentation du dossier concerné** - Voir structure ci-dessus
4. **Logs** - `docker-compose logs -f`
5. **Validation** - `python tools/validate_dashboard_organization.py`

---

## ✅ Checklist de Lecture Recommandée

### Pour Débuter
- [ ] [QUICKSTART.md](QUICKSTART.md)
- [ ] [README.md](README.md)
- [ ] [ORGANISATION_PROJET.md](ORGANISATION_PROJET.md)

### Pour Développer
- [ ] [grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md)
- [ ] [docker/README.md](docker/README.md)
- [ ] [tools/README.md](tools/README.md)
- [ ] [GUIDE_DASHBOARDS.md](GUIDE_DASHBOARDS.md)

### Pour Déployer
- [ ] [docker-compose.secure.yml](docker-compose.secure.yml)
- [ ] [k8s/README.md](k8s/README.md)
- [ ] [k8s/LOCAL_TEST.md](k8s/LOCAL_TEST.md)

### Pour Sécuriser
- [ ] [SECURITY.md](SECURITY.md)
- [ ] [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md)
- [ ] [docs/DDOS_PROTECTION_REPORT.md](docs/DDOS_PROTECTION_REPORT.md)

---

**Dernière mise à jour** : Réorganisation 2.0  
**Total de documents** : 30+ fichiers de documentation  
**Statut** : ✅ Complet et à jour
