"# 🛒 E-commerce Dashboard & A/B Testing

> **Tableau de bord analytique avancé avec tests A/B, monitoring de sécurité et visualisation en temps réel**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.14-orange.svg)](https://dash.plotly.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Grafana](https://img.shields.io/badge/Grafana-Latest-orange.svg)](https://grafana.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Stack Technique](#-stack-technique)
- [Structure du Projet](#-structure-du-projet)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Milestones](#-milestones)
- [Branches & Workflow](#-branches--workflow)
- [Captures d'écran](#-captures-décran)
- [Documentation](#-documentation)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🎯 Vue d'ensemble

Ce projet est une **plateforme analytique complète** pour un site e-commerce, combinant :

- 📊 **Dashboard multi-pages interactif** avec Plotly Dash
- 🧪 **Framework de tests A/B** pour optimiser les conversions
- 🗃️ **Base de données PostgreSQL** pour la persistance
- 📈 **Visualisation temps réel** avec Grafana
- 🔒 **Monitoring de sécurité** avec Falco (IDS)
- 📝 **Agrégation de logs** avec Loki + Promtail
- 🐳 **Architecture conteneurisée** avec Docker

### Fonctionnalités principales

✅ Analyse du comportement utilisateur  
✅ KPIs e-commerce (taux de conversion, panier moyen, CLV)  
✅ Tests A/B statistiquement robustes (tests de Student, Chi-2)  
✅ Analyse de cohortes  
✅ Détection d'intrusions en temps réel  
✅ Dashboards Grafana pour monitoring système

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                        │
│  ┌─────────────────────┐        ┌─────────────────────┐   │
│  │   Dash Dashboard    │        │      Grafana        │   │
│  │   (Port 8050)       │        │    (Port 3000)      │   │
│  └──────────┬──────────┘        └──────────┬──────────┘   │
└─────────────┼─────────────────────────────┼───────────────┘
              │                              │
              ▼                              ▼
    ┌─────────────────┐          ┌─────────────────┐
    │   PostgreSQL    │          │      Loki       │
    │   (Port 5432)   │          │   (Port 3100)   │
    └─────────────────┘          └────────▲────────┘
                                          │
                                   ┌──────┴──────┐
                                   │  Promtail   │
                                   └──────▲──────┘
                                          │
              ┌───────────────────────────┴─────────┐
              │                                     │
         ┌────┴──────┐                      ┌──────┴─────┐
         │   Falco   │                      │ App Logs   │
         │   (IDS)   │                      │            │
         └───────────┘                      └────────────┘
```

### Flux de données

1. **Ingestion** : Données brutes → PostgreSQL
2. **Transformation** : Scripts Python → Données nettoyées
3. **Analyse** : KPIs, A/B tests → Métriques calculées
4. **Visualisation** : Dash + Grafana → Dashboards interactifs
5. **Monitoring** : Falco → Loki → Grafana → Alertes sécurité

---

## 🛠️ Stack Technique

### Backend & Data

- **Python 3.11** - Langage principal
- **Pandas / NumPy** - Manipulation de données
- **SQLAlchemy** - ORM pour PostgreSQL
- **SciPy / Statsmodels** - Tests statistiques

### Frontend & Visualisation

- **Plotly Dash** - Framework de dashboard interactif
- **Dash Bootstrap Components** - UI moderne
- **Plotly.js** - Graphiques interactifs

### Infrastructure

- **Docker & Docker Compose** - Conteneurisation
- **PostgreSQL 15** - Base de données relationnelle
- **Grafana** - Monitoring et alerting
- **Loki** - Agrégation de logs
- **Promtail** - Collecte de logs
- **Falco** - Système de détection d'intrusions

---

## 📁 Structure du Projet

```
ecommerce-abtest-dashboard/
│
├── dash-app/                    # Application Dash
│   ├── pages/                   # Pages du dashboard
│   │   ├── __init__.py
│   │   ├── home.py             # Page d'accueil
│   │   ├── behavior.py         # Analyse comportementale
│   │   ├── products.py         # Analyse produits
│   │   ├── ab_testing.py       # Tests A/B
│   │   └── cohorts.py          # Analyse de cohortes
│   ├── assets/                  # CSS, images, JS
│   │   └── styles.css
│   ├── utils/                   # Utilitaires
│   │   ├── __init__.py
│   │   ├── db.py               # Connexion DB
│   │   └── charts.py           # Générateurs de graphiques
│   └── app.py                   # Point d'entrée Dash
│
├── data/                        # Données
│   ├── raw/                     # Données brutes
│   └── clean/                   # Données nettoyées
│
├── src/                         # Code source
│   ├── preprocessing/           # Nettoyage de données
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── validator.py
│   ├── kpis/                    # Calcul des KPIs
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── aggregations.py
│   └── ab_testing/              # Tests A/B
│       ├── __init__.py
│       ├── statistical_tests.py
│       └── sample_size.py
│
├── docker/                      # Configurations Docker
│   ├── falco/
│   │   ├── falco.yaml
│   │   └── rules/
│   │       └── custom-rules.yaml
│   ├── loki/
│   │   └── loki-config.yml
│   └── promtail/
│       └── promtail-config.yml
│
├── grafana/                     # Grafana provisioning
│   ├── datasources/
│   │   └── datasources.yml
│   └── dashboards/
│       ├── dashboard-provider.yml
│       └── security-dashboard.json
│
├── docs/                        # Documentation
│   ├── diagrams/                # Diagrammes d'architecture
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
├── scripts/                     # Scripts utilitaires
│   ├── init_branches.sh         # Création des branches
│   ├── setup_db.py              # Initialisation DB
│   └── load_data.py             # Chargement des données
│
├── tests/                       # Tests unitaires
│   ├── test_kpis.py
│   ├── test_ab_testing.py
│   └── test_preprocessing.py
│
├── docker-compose.yml           # Orchestration Docker
├── Dockerfile                   # Image Dash
├── requirements.txt             # Dépendances Python
├── .env.example                 # Variables d'environnement
├── .gitignore
└── README.md                    # Ce fichier
```

---

## 🚀 Installation

### Prérequis

- **Docker** & **Docker Compose** installés
- **Git** configuré
- **Python 3.11+** (optionnel, pour développement local)

### Installation rapide

```bash
# 1. Cloner le repository
git clone https://github.com/Christh2022/ecommerce-abtest-dashboard.git
cd ecommerce-abtest-dashboard

# 2. Copier le fichier d'environnement
cp .env.example .env

# 3. Initialiser les branches Git
bash scripts/init_branches.sh

# 4. Lancer l'infrastructure
docker-compose up -d

# 5. Attendre que les services démarrent (30-60s)
docker-compose ps

# 6. Accéder aux interfaces
# - Dash Dashboard: http://localhost:8050
# - Grafana: http://localhost:3000 (admin/admin123)
# - PostgreSQL: localhost:5432
```

### Installation pour développement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python scripts/setup_db.py

# Charger les données de test
python scripts/load_data.py

# Lancer l'application en mode dev
python dash-app/app.py
```

---

## 💻 Utilisation

### Accès aux services

| Service            | URL                   | Credentials      |
| ------------------ | --------------------- | ---------------- |
| **Dash Dashboard** | http://localhost:8050 | -                |
| **Grafana**        | http://localhost:3000 | admin / admin123 |
| **PostgreSQL**     | localhost:5432        | admin / admin123 |
| **Loki**           | http://localhost:3100 | -                |

### Commandes Docker utiles

```bash
# Voir les logs
docker-compose logs -f dash-app

# Redémarrer un service
docker-compose restart grafana

# Arrêter tous les services
docker-compose down

# Supprimer les volumes (⚠️ perte de données)
docker-compose down -v

# Rebuild après modification
docker-compose up -d --build
```

### Workflow de développement

```bash
# Créer une nouvelle branche feature
git checkout -b feature/nouvelle-fonctionnalite

# Développer et tester
python dash-app/app.py

# Tests unitaires
pytest tests/

# Commit et push
git add .
git commit -m "feat: ajout nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

---

## 🎯 Milestones

### Milestone 1 : Dataset & Préparation

- [x] Structure du projet
- [ ] Collecte des données brutes
- [ ] Nettoyage et validation
- [ ] Import dans PostgreSQL

### Milestone 2 : KPIs & Exploration

- [ ] Calcul des métriques clés
- [ ] Analyse exploratoire
- [ ] Détection d'anomalies

### Milestone 3 : A/B Testing

- [ ] Framework de tests statistiques
- [ ] Calcul de tailles d'échantillon
- [ ] Analyse de significativité

### Milestone 4 : Dashboard Multi-Pages

- [ ] Page d'accueil
- [ ] Page comportement utilisateur
- [ ] Page produits
- [ ] Page A/B testing
- [ ] Page cohortes

### Milestone 5 : Dockerisation

- [x] Configuration Docker Compose
- [x] Dockerfile pour Dash
- [x] Configuration PostgreSQL
- [x] Configuration Grafana

### Milestone 6 : Documentation & Livraison

- [x] README complet
- [ ] Documentation API
- [ ] Guide de déploiement
- [ ] Rapport PDF

### Milestone 7 : Sécurité & Intrusion

- [x] Configuration Falco
- [x] Intégration Loki/Promtail
- [x] Dashboard Grafana sécurité
- [ ] Règles d'alerting

---

## 🌳 Branches & Workflow

### Branches principales

- `main` - Production stable
- `develop` - Branche de développement

### Branches features

```bash
feature/data-preprocessing      # Nettoyage des données
feature/data-cleaning           # Validation des données
feature/data-exploration        # Analyse exploratoire
feature/kpi-metrics            # Calcul des KPIs
feature/ab-testing             # Tests A/B
feature/dashboard-home         # Page d'accueil
feature/dashboard-behavior     # Page comportement
feature/dashboard-products     # Page produits
feature/dashboard-abtest       # Page tests A/B
feature/dashboard-cohorts      # Page cohortes
feature/docker-setup           # Configuration Docker
feature/docs-writing           # Documentation
feature/refactor               # Refactoring
feature/tests                  # Tests unitaires
feature/security-intrusion     # Sécurité & monitoring
```

### Workflow Git

```
feature/* → develop → main
     ↓         ↓        ↓
   Tests    Review  Production
```

---

## 📸 Captures d'écran

### Dashboard Principal

```
[Screenshot placeholder: Dashboard home page with KPIs]
```

### Analyse A/B Testing

```
[Screenshot placeholder: A/B test results visualization]
```

### Monitoring Sécurité (Grafana)

```
[Screenshot placeholder: Grafana security dashboard]
```

---

## 📚 Documentation

- [Architecture détaillée](docs/ARCHITECTURE.md)
- [Documentation API](docs/API.md)
- [Guide de déploiement](docs/DEPLOYMENT.md)
- [Diagrammes](docs/diagrams/)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'feat: Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

### Standards de code

- **PEP 8** pour le Python
- **Black** pour le formatage
- **Tests unitaires** obligatoires
- **Documentation** des fonctions

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Votre Nom**

- GitHub: [@Christh2022](https://github.com/Christh2022)
- Email: votre.email@example.com

---

## 🙏 Remerciements

- [Plotly Dash](https://dash.plotly.com/) pour le framework de dashboard
- [Grafana](https://grafana.com/) pour les outils de visualisation
- [Falco](https://falco.org/) pour la détection d'intrusions
- La communauté open-source

---

<p align="center">
  Made with ❤️ for e-commerce analytics
</p>"
