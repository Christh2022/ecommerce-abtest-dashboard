# E-commerce Dashboard & A/B Testing 🚀

Plateforme d'analyse e-commerce avec dashboard interactif et outils d'A/B testing utilisant Python, Dash, PostgreSQL, Docker et Grafana.

## 📊 Vue d'ensemble

Ce projet analyse les données du dataset **RetailRocket** (2.7M événements, 1.4M utilisateurs, 235K produits) pour créer un dashboard de visualisation et des outils d'analyse de performance e-commerce.

### Objectifs

- 📈 **Dashboard interactif** : 12+ pages de visualisation en temps réel des KPIs e-commerce
- 🧪 **A/B Testing** : 16 scénarios de test simulés avec analyse statistique complète
- 📉 **Analyse de tendances** : Métriques quotidiennes, entonnoirs de conversion, performance produits
- 🎯 **Méthodologie** : Guide complet des bonnes pratiques en A/B testing
- 🐳 **Déploiement** : Application containerisée avec Docker, PostgreSQL et Grafana

---

## 🚀 Démarrage Rapide

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé et en cours d'exécution
- [Git](https://git-scm.com/downloads) installé
- Au moins 4 GB de RAM disponible
- 5 GB d'espace disque libre

### Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-username/ecommerce-abtest-dashboard.git
   cd ecommerce-abtest-dashboard
   ```

2. **Lancer tous les services**
   ```bash
   docker compose -f docker-compose.secure.yml up -d
   ```
   
   Cette commande va :
   - ✅ Construire les images Docker
   - ✅ Démarrer PostgreSQL avec les données pré-chargées
   - ✅ Lancer l'application Dash (Dashboard)
   - ✅ Démarrer Grafana, Prometheus, Loki (Monitoring)
   - ✅ Créer automatiquement les 11 dashboards Grafana

3. **Attendre le démarrage complet** (~2-3 minutes)
   ```bash
   # Vérifier l'état des services
   docker compose -f docker-compose.secure.yml ps
   ```

### Accès aux Services

Une fois les conteneurs démarrés, accédez aux différentes interfaces :

| Service | URL | Identifiants | Description |
|---------|-----|--------------|-------------|
| 🎨 **Dashboard Dash** | http://localhost:8050 | - | Application principale d'analyse |
| 📊 **Grafana** | http://localhost:3000 | admin / admin123 | 11 dashboards de monitoring |
| 🔍 **Prometheus** | http://localhost:9090 | - | Métriques temps réel |
| 🗄️ **PostgreSQL** | localhost:5432 | dashuser / dashpass | Base de données (ecommerce_db) |

### Arrêter le Projet

```bash
# Arrêter tous les services
docker compose -f docker-compose.secure.yml down

# Arrêter et supprimer les volumes (⚠️ efface les données)
docker compose -f docker-compose.secure.yml down -v
```

### Relancer le Projet

```bash
# Redémarrer les services existants
docker compose -f docker-compose.secure.yml up -d

# Reconstruire les images (après modification du code)
docker compose -f docker-compose.secure.yml up -d --build
```

### Charger les Données dans PostgreSQL

Les données CSV doivent être importées dans PostgreSQL après le démarrage :

```bash
# Option 1 : Importer depuis l'hôte (nécessite psycopg2)
python scripts/import_data_to_postgres.py

# Option 2 : Importer via Docker (recommandé sur Windows)
docker exec -i ecommerce-postgres psql -U dashuser -d ecommerce_db << EOF
\copy daily_metrics FROM '/docker-entrypoint-initdb.d/daily_metrics.csv' WITH CSV HEADER;
EOF

# Option 3 : Utiliser le script de migration complet
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -f /docker-entrypoint-initdb.d/01_init.sql
```

**Vérifier l'import** :
```bash
# Vérifier le nombre de lignes dans les tables
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -c "SELECT 'daily_metrics' as table, COUNT(*) FROM daily_metrics UNION ALL SELECT 'products_summary', COUNT(*) FROM products_summary;"
```

### Créer les Dashboards Grafana (Optionnel)

Les dashboards Grafana doivent être créés manuellement après le chargement des données :

```bash
# Attendre que tous les services soient démarrés (~2 minutes)
# Puis exécuter les scripts de création des dashboards :

# 1. Dashboards de base (Funnel, Segmentation, Produits)
python create_dashboards_1_3.py

# 2. Dashboards avancés (Cohortes, Real-Time, Prédictif)
python create_dashboards_4_6.py

# 3. Dashboard Business Intelligence
python create_bi_dashboard.py

# 4. Dashboard E-Commerce complet
python create_full_dashboard.py

# 5. Dashboard Monitoring
python create_monitoring_dashboard.py

# 6. Dashboard Prometheus
python create_prometheus_dashboard.py
```

**Note** : Les dashboards sont créés via l'API Grafana. Assurez-vous que Grafana est démarré et accessible sur http://localhost:3000 avant d'exécuter ces scripts.

---

## ✨ Démo en Ligne

**Dashboard accessible à** : http://localhost:8050

**Pages disponibles** :

- 🏠 Accueil - Vue d'ensemble et KPIs
- 👥 Trafic - Analyse des visiteurs
- 🖱️ Comportement - Patterns d'engagement
- 🛒 Conversions - Funnel analysis
- 📦 Produits - Performance et Pareto
- 🔄 Funnel - Visualisation tunnel
- 🧪 Simulations A/B - 16 scénarios
- 📊 Résultats A/B - Analyse statistique
- 🧮 Calculateur Z-Test - Outil interactif
- 📈 Visualisations - Graphiques avancés
- 📚 Méthodologie - Guide complet
- ℹ️ À Propos - Documentation projet

**Grafana Dashboards** : http://localhost:3000 (admin/admin123)

Après avoir exécuté les scripts ci-dessus, vous aurez accès à 10 dashboards :
- Business Intelligence & Decision Support
- Cohort Analysis & Retention
- Customer Journey & Funnel Analysis
- Customer Segmentation Analysis
- E-Commerce A/B Test Analytics
- E-Commerce Dashboard (Prometheus)
- E-Commerce Monitoring Dashboard
- Predictive Analytics & Forecasting
- Product Performance Analysis
- Real-Time Performance Monitoring

---

## 🎯 Milestone 1 : Dataset & Préparation des Données ✅

**Statut** : COMPLÉTÉ (8 issues)  
**Branche** : `feature/data-preprocessing`  
**Période** : Décembre 2025

### 📦 Dataset RetailRocket

Source : [Kaggle - RetailRocket E-commerce Dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)

**Caractéristiques :**

- **Période couverte** : 2015-05-03 → 2015-09-18 (137 jours / 19.6 semaines)
- **Événements totaux** : 2,755,641 (après nettoyage)
  - Views : 2,664,218 (96.7%)
  - Add-to-carts : 68,966 (2.5%)
  - Transactions : 22,457 (0.8%)
- **Utilisateurs uniques** : 1,407,580
- **Sessions uniques** : 1,649,534
- **Produits uniques** : 235,061
- **Revenu total** : 5,732,867.82 €
- **Taux de conversion global** : 0.84%

---

## 🔧 Issues Complétées

### Issue #1 : Télécharger le dataset RetailRocket ✅

**Fichiers créés :**

- `scripts/download_data.py` : Script de téléchargement via Kaggle API
- Données brutes (942 MB) → nettoyées (536 MB)

### Issue #2 : Inspecter les fichiers CSV ✅

**Fichiers créés :**

- `scripts/inspect_csv.py` : Analyse exploratoire des données
- Résultats : 460 doublons détectés dans `events.csv`

### Issue #3 : Nettoyer events.csv ✅

**Fichiers créés :**

- `scripts/clean_events.py` : Suppression des doublons
- `data/clean/events_cleaned.csv` : 2,755,641 lignes (460 doublons supprimés)

### Issue #4 : Nettoyer item_properties.csv ✅

**Fichiers créés :**

- `scripts/clean_item_properties.py` : Parsing et structuration
- `data/clean/item_properties_cleaned.csv` : 20,275,902 lignes, 9 colonnes typées

### Issue #5 : Fusionner les données ✅

**Fichiers créés :**

- `scripts/merge_data.py` : Fusion et enrichissement (515 lignes)
- **8 tables enrichies** (490 MB total) :
  - `events_enriched.csv` : 2.7M lignes, 12 colonnes (242 MB)
  - `sessions_enriched.csv` : 1.6M lignes, 10 colonnes (134 MB)
  - `transactions_enriched.csv` : 22K lignes, 13 colonnes (2 MB)
  - `daily_funnel.csv` : 139 jours, entonnoir de conversion
  - `hourly_analysis.csv` : 24 heures, activité horaire
  - `segment_performance.csv` : 4 segments utilisateurs
  - `user_journey.csv` : 1.4M parcours (105 MB)
  - `product_performance.csv` : 235K produits (7.5 MB)

### Issue #6 : Générer data_clean.csv ✅

**Fichiers créés :**

- `scripts/generate_data_clean_simple.py` : Consolidation optimisée par chunks
- `data/clean/data_clean.csv` : 2.7M lignes, 13 colonnes (229 MB)
- **Colonnes** : user_id, session_id, timestamp, date, hour, day_of_week, event_type, product_id, transaction_id, amount, segment, product_views, product_purchases

### Issue #7 : Générer daily_metrics.csv ✅

**Fichiers créés :**

- `scripts/generate_daily_metrics.py` : Métriques quotidiennes (224 lignes)
- `data/clean/daily_metrics.csv` : 139 jours, 29 colonnes (24 KB)
- **Métriques incluses** :
  - Base : users, sessions, produits, événements
  - Conversion : view→cart, view→purchase, cart→purchase
  - Revenus : daily_revenue, avg_order_value, min/max_order
  - Par utilisateur : events_per_user, sessions_per_user, revenue_per_user
  - Moyennes mobiles (MA7) : revenue, users, conversion
  - Segmentation : users_new, users_occasional, users_regular, users_premium
  - Temporel : day_of_week, week_number, month, is_weekend

### Issue #8 : Générer products_summary.csv ✅

**Fichiers créés :**

- `scripts/generate_products_summary.py` : Analyse produits (268 lignes)
- `data/clean/products_summary.csv` : 235K produits, 21 colonnes (20 MB)
- **Métriques incluses** :
  - Rang et catégorisation (Top Performer, High Revenue)
  - Engagement : views, add_to_carts, purchases, unique_users
  - Conversion : view→cart, view→purchase, cart→purchase
  - Revenus : total_revenue, avg_price, min/max_price
  - Performance : events_per_user, revenue_per_user, revenue_per_view

---

## 📊 KPIs Globaux

### Utilisateurs

- **Total** : 1,407,580 utilisateurs uniques
- **Sessions** : 1,649,534 (1.17 sessions/user en moyenne)
- **Segmentation** :
  - New : 70% (983K users)
  - Occasional : 17% (239K users)
  - Regular : 7% (99K users)
  - Premium : 6% (89K users)

### Événements

- **Total** : 2,755,641 événements
- **Par type** :
  - Views : 2,664,218 (96.7%)
  - Add-to-carts : 68,966 (2.5%)
  - Transactions : 22,457 (0.8%)
- **Moyenne** : 1.96 événements/utilisateur

### Conversion

- **View → Add-to-cart** : 2.59%
- **View → Purchase** : 0.84%
- **Cart → Purchase** : 32.56%

### Revenus

- **Total** : 5,732,867.82 €
- **Par jour** : 41,243.65 € (moyenne)
- **Panier moyen** : 255.28 €
- **Par utilisateur** : 4.07 €

### Produits

- **Catalogués** : 235,061 produits
- **Avec ventes** : 12,025 (5.1%)
- **Sans ventes** : 223,036 (94.9%)
- **Revenu moyen** : 24.39 €/produit
- **Top produit #461686** : 34,781.58 € (133 achats, 5.24% conversion)

### Meilleurs jours

- **Revenue max** : 2015-07-28
- **Utilisateurs max** : 2015-07-26
- **Conversion max** : 2015-07-28

---

## 📁 Structure des données

```
data/
├── raw/                          # Données brutes (942 MB)
│   ├── events.csv
│   ├── item_properties.csv
│   └── category_tree.csv
│
└── clean/                        # Données nettoyées et enrichies
    ├── events_cleaned.csv        # 2.7M événements nettoyés
    ├── data_clean.csv            # 2.7M lignes consolidées (229 MB)
    ├── daily_metrics.csv         # 139 jours de métriques (24 KB)
    ├── products_summary.csv      # 235K produits analysés (20 MB)
    │
    ├── events_enriched.csv       # Événements + segments + produits (242 MB)
    ├── sessions_enriched.csv     # Sessions + segments (134 MB)
    ├── transactions_enriched.csv # Transactions enrichies (2 MB)
    │
    ├── daily_funnel.csv          # Entonnoir quotidien
    ├── hourly_analysis.csv       # Activité horaire
    ├── segment_performance.csv   # Performance par segment
    ├── user_journey.csv          # Parcours utilisateurs (105 MB)
    └── product_performance.csv   # Performance produits (7.5 MB)
```

---

## 🛠️ Scripts développés

```
scripts/
├── download_data.py                    # Téléchargement Kaggle
├── inspect_csv.py                      # Exploration données
├── clean_events.py                     # Nettoyage événements
├── clean_item_properties.py            # Nettoyage propriétés
├── merge_data.py                       # Fusion et enrichissement
├── generate_data_clean_simple.py       # Consolidation données
├── generate_daily_metrics.py           # Métriques quotidiennes
└── generate_products_summary.py        # Analyse produits
```

---

## 🚀 Utilisation

### Prérequis

```bash
# Python 3.12+
pip install pandas numpy kaggle

# Configuration Kaggle API
export KAGGLE_USERNAME=<votre_username>
export KAGGLE_KEY=<votre_key>
```

### Télécharger et préparer les données

```bash
# 1. Télécharger le dataset
python scripts/download_data.py

# 2. Nettoyer les données
python scripts/clean_events.py
python scripts/clean_item_properties.py

# 3. Fusionner et enrichir
python scripts/merge_data.py

# 4. Générer les fichiers d'analyse
python scripts/generate_data_clean_simple.py
python scripts/generate_daily_metrics.py
python scripts/generate_products_summary.py
```

---

## 📈 Insights clés

### 1. Conversion en entonnoir classique

- **96.7%** des interactions sont des vues
- Seulement **2.5%** ajoutent au panier
- **32.6%** des paniers se convertissent en achat
- **Opportunité** : Optimiser la transition view → cart (+2.59% actuellement)

### 2. Segmentation utilisateurs

- **70% sont "New"** : Opportunité de rétention
- **Premium (6%)** représentent probablement une part disproportionnée du revenu
- **Stratégie** : Programmes de fidélisation pour convertir New → Occasional → Regular

### 3. Catalogue produits

- **94.9% des produits n'ont jamais été vendus** : Problème de merchandising
- **5.1% des produits génèrent 100% du revenu** : Concentration extrême
- **Top 4.7% ("Top Performers")** : Focus sur ces produits pour maximiser ROI

### 4. Saisonnalité

- **Pic d'activité** : Fin juillet 2015 (été)
- **Variation hebdomadaire** : Analyse des weekends vs semaine disponible
- **Tendances** : Moyennes mobiles (MA7) pour lisser les variations

---

## 🎯 Milestones du Projet

### ✅ Milestone 1 : Dataset & Préparation des Données

**Statut** : COMPLÉTÉ (8/8 issues)  
**Branche** : `feature/data-preprocessing`  
**Date** : Décembre 2025

**Livrables** :

- ✅ Téléchargement et nettoyage des données RetailRocket
- ✅ 8 tables enrichies (490 MB)
- ✅ Scripts de transformation et agrégation
- ✅ Métriques quotidiennes et analyse produits

---

### ✅ Milestone 2 : KPIs & Métriques Business

**Statut** : COMPLÉTÉ (6/6 issues)  
**Branche** : `feature/kpi-metrics`  
**Date** : Décembre 2025

**Livrables** :

- ✅ Calcul des KPIs principaux (conversion, revenu, engagement)
- ✅ Segmentation utilisateurs (New, Occasional, Regular, Premium)
- ✅ Analyse temporelle (daily, weekly, monthly)
- ✅ Moyennes mobiles et tendances
- ✅ Métriques par produit et catégorie

---

### ✅ Milestone 3 : A/B Testing & Simulations

**Statut** : COMPLÉTÉ (10/10 issues)  
**Branche** : `feature/ab-testing`  
**Date** : Décembre 2025

**Livrables** :

- ✅ 16 scénarios de test A/B simulés
- ✅ Simulations Monte Carlo (10,000 itérations/scenario)
- ✅ Tests statistiques (Chi-Square, Z-Test)
- ✅ Calcul puissance statistique (78-81%)
- ✅ Données de simulation sur 30 jours (480 lignes)
- ✅ Métriques : lift, confidence, p-value, ROI

---

### ✅ Milestone 4 : Dashboard Interactif

**Statut** : COMPLÉTÉ (19/19 issues)  
**Branche** : `feature/dashboard-home`  
**Date** : Décembre 2025

**Livrables** :

- ✅ Application Dash multi-pages (12 pages)
- ✅ Visualisations Plotly interactives (60+ graphiques)
- ✅ Filtres dynamiques (date, segment, produit)
- ✅ Page Accueil avec KPIs temps réel
- ✅ Pages d'analyse : Trafic, Comportement, Conversions
- ✅ Pages produits : Performance, Pareto, Funnel
- ✅ Pages A/B : Simulations, Résultats, Calculateur
- ✅ Page Visualisations avancées
- ✅ Page Méthodologie (guide complet)
- ✅ Page À Propos (documentation)
- ✅ Thème dark moderne avec Bootstrap 5
- ✅ Gestion d'erreurs et callbacks optimisés

**Technologies** :

- Python 3.12+
- Dash 2.14.2
- Plotly 5.18.0
- Pandas, NumPy, SciPy
- Bootstrap 5 + Font Awesome

---

### 🚧 Milestone 5 : Docker & Déploiement

**Statut** : EN COURS (11/14 issues complétées)  
**Branche** : `feature/docker-setup`  
**Date** : Décembre 2025

**Objectif** : Rendre l'application portable et exécutable avec Docker

#### Containerisation Dash App (Issues #28-31)

- [x] **#28** - Créer Dockerfile pour l'application Dash ✅
- [x] **#29** - Créer docker-compose.yml multi-services ✅
- [x] **#30** - Tester build de l'image Docker ✅
- [x] **#31** - Tester run et accès port 8050 ✅

#### PostgreSQL Integration (Issues #41-43)

- [x] **#41** - Créer service Postgres dans docker-compose ✅
- [x] **#42** - Créer script de migration/init SQL ✅
- [x] **#43** - Importer les KPIs dans Postgres automatiquement ✅

#### Grafana Monitoring (Issues #44-48)

- [x] **#44** - Ajouter Grafana dans docker-compose ✅
- [x] **#45** - Configurer datasource Postgres ✅
- [x] **#46** - Créer dashboard Grafana (JSON) ✅
- [ ] **#47** - Panels : sessions, conversion, revenues, erreurs
- [x] **#48** - Test accès http://localhost:3000 ✅

#### Sécurité & Monitoring (Issues #50, #52-53, #55-56)

- [x] **#50** - Optimiser volumes et réseaux ✅
- [x] **#52** - Configurer Falco pour monitoring sécurité ✅
- [x] **#53** - Ajouter Loki et Promtail pour collecte logs ✅
- [x] **#55** - Configurer Grafana pour afficher les logs de sécurité ✅
- [x] **#56** - Ajouter alertes (connexions suspectes, shell, modifications fichiers) ✅

#### Tests Complets (Issue #49)

- [ ] **#49** - docker-compose up — tests complets end-to-end

**Architecture cible** :

```
docker-compose.yml
├── dash-app (port 8050)
├── postgres (port 5432)
├── grafana (port 3000)
├── loki (logs)
└── promtail (agent)
```

---

## 🚀 Installation & Démarrage

### Prérequis

```bash
# Python 3.12+
pip install -r dashboard/requirements.txt
```

### Lancer le Dashboard

```bash
# Depuis le dossier racine
cd dashboard
python app.py

# Accéder au dashboard
http://127.0.0.1:8050
```

> **Note** : Les données sont déjà nettoyées et prêtes à l'emploi dans le dossier `data/clean/`. Aucune configuration Kaggle API n'est nécessaire pour utiliser le dashboard.

### Préparation des données (optionnel)

Si vous souhaitez télécharger et retraiter les données depuis zéro :

```bash
# 1. Configurer Kaggle API
export KAGGLE_USERNAME=votre_username
export KAGGLE_KEY=votre_key

# 2. Télécharger le dataset
python scripts/download_data.py

# 3. Nettoyer et enrichir les données
python scripts/clean_events.py
python scripts/clean_item_properties.py
python scripts/merge_data.py
python scripts/generate_data_clean_simple.py
python scripts/generate_daily_metrics.py
python scripts/generate_products_summary.py
```

### Avec Docker (à venir - Milestone 5)

```bash
# Build et run tous les services
docker-compose up --build

# Services disponibles
# - Dashboard: http://localhost:8050
# - Grafana: http://localhost:3000
# - PostgreSQL: localhost:5432
```

---

## 📦 Dépendances

```txt
dash==2.14.2
dash-bootstrap-components==1.5.0
plotly==5.18.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
```

---

## 👥 Équipe & Contribution

**Développé par** : Christh Mampassi  
**Email** : cmampassi273@gmail.com  
**Repository** : [Christh2022/ecommerce-abtest-dashboard](https://github.com/Christh2022/ecommerce-abtest-dashboard)  
**Branche main** : `main`  
**Branche dev** : `dev`

---

## 📝 License

Ce projet utilise le dataset RetailRocket sous licence publique Kaggle.

---

**Dernière mise à jour** : 11 décembre 2025  
**Version** : 1.0.0  
**Milestones complétés** : 4/5 ✅  
**Issues résolues** : 43/57
