# E-commerce Dashboard & A/B Testing 

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Dash](https://img.shields.io/badge/Dash-2.14.2-brightgreen.svg)](https://dash.plotly.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://github.com/Christh2022/ecommerce-abtest-dashboard)

> **Nouveau : Interface vocale interactive !** L'application intègre maintenant la reconnaissance vocale pour une navigation mains-libres. Dites "Explique l'accueil" pour une présentation guidée !

Plateforme d'analyse e-commerce avec dashboard interactif, assistant vocal intelligent et outils d'A/B testing utilisant Python, Dash, PostgreSQL, Docker et Grafana.

## Vue d'ensemble

Ce projet analyse les données du dataset **RetailRocket** (2.7M événements, 1.4M utilisateurs, 235K produits) pour créer un dashboard de visualisation et des outils d'analyse de performance e-commerce.

### Fonctionnalités Principales

- **Dashboard interactif** : 12+ pages de visualisation en temps réel des KPIs e-commerce
- **Assistant Vocal Intelligent** : Navigation vocale, explications guidées et commandes mains-libres
- **A/B Testing** : 16 scénarios de test simulés avec analyse statistique complète
- **Analyse de tendances** : Métriques quotidiennes, entonnoirs de conversion, performance produits
- **Méthodologie** : Guide complet des bonnes pratiques en A/B testing
- **Déploiement** : Application containerisée avec Docker, PostgreSQL et Grafana
- ️ **Sécurité** : Protection multicouche, tests automatisés, monitoring temps réel

### Assistant Vocal - Nouvelle Fonctionnalité !

L'application intègre un **système de reconnaissance vocale** pour une expérience utilisateur révolutionnaire :

**Fonctionnalités vocales :**

- ️ **Accueil personnalisé** : "Bonjour Docteur Christh, comment puis-je vous aider ?"
- **Explications détaillées** : Dites "Explique l'accueil" pour une présentation complète
- **Navigation vocale** : "Va sur le dashboard" ou "Montre-moi les conversions"
- **Interaction continue** : L'assistant écoute et répond en boucle

**Commandes vocales disponibles :**

```
"Explique l'accueil" / "Explique l'application" → Présentation détaillée de la plateforme
"Dashboard" / "Tableau de bord" → Redirection vers le dashboard principal
"Connexion" / "Connecter" → Redirection vers la page de connexion
```

**Compatibilité :** Chrome, Edge, Safari (Web Speech API)

**Essayez maintenant :** Ouvrez http://localhost:8050 et parlez ! ️

## ️ Sécurité - Important pour les Collaborateurs

** [GUIDE COMPLET DE SÉCURITÉ →](SECURITY_GUIDE_COLLABORATORS.md)** (Lecture obligatoire)

### Protections Actives

 **Authentification** : Flask-Login + bcrypt 
 **Anti-DDoS** : Rate limiting 200 req/min (94.4% d'efficacité testée) 
 **En-têtes HTTP** : CSP, X-Frame-Options, X-Content-Type-Options, etc. 
 **Tests automatisés** : 41 types d'attaques (SQL injection, XSS, CSRF...) 
 **Monitoring** : Grafana + 32 alertes en temps réel

### Tests de l'Application

#### Lancer la Suite de Tests Complète

```bash
# Windows
scripts\bin\run_tests.bat

# Linux/Mac
./scripts/bin/run_tests.sh

# Ou directement avec Python
python run_tests.py
```

**Ce qui est testé** :

- Connexion au serveur (port 8050)
- Page d'accueil publique (landing page)
- Page de connexion
- Système d'authentification
- Protection des pages sécurisées
- Services Docker (dash-app, postgres, grafana, prometheus)

** Résultat attendu** :

```
╔════════════════════════════════════════════════════════════╗
║ E-Commerce A/B Test Dashboard - Suite de tests ║
╚════════════════════════════════════════════════════════════╝

 PASS Connexion serveur
 PASS Landing page
 PASS Page de connexion
 PASS Authentification
 PASS Pages protégées
 PASS Services Docker

Résultat: 6/6 tests réussis
 Tous les tests sont passés !
```

**️ Configuration** : Modifiez `run_tests.py` si vous avez changé les identifiants par défaut :

```python
TEST_USER = {
 "username": "admin",
 "password": "admin123" # À modifier selon votre configuration
}
```

** Plus d'informations** : Consultez le [Guide Sécurité Collaborateurs](SECURITY_GUIDE_COLLABORATORS.md) pour :

- Procédures de test complètes
- Bonnes pratiques de développement sécurisé
- Que faire en cas d'incident de sécurité
- Ressources de formation cybersécurité

---

## Démarrage Rapide - Guide Collaborateur

### Installation en 5 Minutes

#### 1️⃣ Prérequis (à installer avant de commencer)

| Logiciel | Version minimum | Lien de téléchargement | Vérification |
| -------------- | --------------- | ------------------------------------------------------------------------------------ | ------------------ |
| Docker Desktop | 24.0+ | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) | `docker --version` |
| Git | 2.40+ | [git-scm.com/downloads](https://git-scm.com/downloads) | `git --version` |
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) | `python --version` |

**Configuration système requise** :

- RAM : Minimum 4 GB disponible (8 GB recommandé)
- Espace disque : 5 GB libre
- Connexion Internet (pour le premier démarrage)

#### 2️⃣ Cloner le Projet

```bash
# Cloner le dépôt
git clone https://github.com/Christh2022/ecommerce-abtest-dashboard.git

# Aller dans le répertoire
cd ecommerce-abtest-dashboard

# Vérifier que vous êtes sur la bonne branche
git branch
```

#### 3️⃣ Installer les Dépendances Python

```bash
# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Windows :
venv\Scripts\activate
# Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

#### 4️⃣ Lancer les Services Docker

```bash
# Démarrer tous les conteneurs
docker compose -f docker-compose.secure.yml up -d --build

# ⏱️ Attendre 2-3 minutes que tous les services démarrent
```

**Ce qui se passe en arrière-plan** :

- Construction des images Docker personnalisées
- ️ Création de la base de données PostgreSQL
- Démarrage de Grafana pour la visualisation
- Lancement de Prometheus pour les métriques
- Initialisation de Loki pour les logs
- Démarrage de l'application Dash

#### 5️⃣ Vérifier que Tout Fonctionne

```bash
# Vérifier l'état des services (tous doivent être "Up" et "healthy")
docker compose -f docker-compose.secure.yml ps

# Vous devriez voir 7-8 conteneurs en cours d'exécution :
# ecommerce-dashboard (healthy)
# ecommerce-postgres (healthy)
# ecommerce-grafana (healthy)
# ecommerce-prometheus (healthy)
# ecommerce-loki
# ecommerce-promtail
# ecommerce-exporter
# ecommerce-postgres-exporter
```

#### 6️⃣ Importer les Données (IMPORTANT !)

Les tables PostgreSQL sont créées automatiquement mais **vides**. Vous devez charger les données.

**️ ATTENTION** : Sur Windows, l'option `-w /` peut causer une erreur. Utilisez la méthode ci-dessous qui fonctionne sur **tous les systèmes** :

```bash
# Étape 1 : Copier les scripts et données nécessaires
docker cp scripts/import_data_to_postgres.py ecommerce-dashboard:/tmp/
docker cp scripts/fix_numeric_overflow.py ecommerce-dashboard:/tmp/
docker cp data/clean ecommerce-dashboard:/tmp/data

# Étape 2 : Corriger le schéma de la base de données (OBLIGATOIRE)
# Cette étape corrige les colonnes NUMERIC(5,4) qui ne peuvent pas stocker les pourcentages (0-100)
docker exec -e DB_HOST=postgres ecommerce-dashboard sh -c "cd /tmp && python fix_numeric_overflow.py"

# Vous devriez voir :
# user_behavior.bounce_rate → NUMERIC(6,2)
# products_summary.conversion_rate → NUMERIC(6,2)
# ab_test_results.conversion_rate → NUMERIC(6,2)
# ab_test_results.statistical_significance → NUMERIC(6,2)
# funnel_stages.conversion_rate → NUMERIC(6,2)

# Étape 3 : Exécuter l'import des données
docker exec -e DB_HOST=postgres ecommerce-dashboard sh -c "
cd /tmp &&
sed 's|Path(__file__).parent.parent / '\''data'\'' / '\''clean'\''|Path('\''/tmp/data'\'')|g' import_data_to_postgres.py > import_fixed.py &&
python import_fixed.py
"

# Étape 4 : Vérifier que l'import a réussi
docker exec -e DB_HOST=postgres ecommerce-dashboard python -c "import psycopg2; conn = psycopg2.connect(host='postgres', database='ecommerce_db', user='dashuser', password='dashpass'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM daily_metrics'); dm = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM products_summary'); ps = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM funnel_stages'); fs = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM ab_test_results'); ab = cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM traffic_sources'); ts = cur.fetchone()[0]; print(f' daily_metrics: {dm} rows'); print(f' products_summary: {ps:,} rows'); print(f' funnel_stages: {fs} rows'); print(f' ab_test_results: {ab} rows'); print(f' traffic_sources: {ts} rows')"
```

** Résultat attendu** :

```
 daily_metrics: 139 rows
 products_summary: 235,061 rows
 funnel_stages: 417 rows
 ab_test_results: 480 rows
 traffic_sources: 139 rows
```

**⏱️ Durée de l'import** : ~2 minutes (correction schéma) + ~2 minutes (import des données)

** Note importante** : La correction du schéma (Étape 2) est **obligatoire** et doit être exécutée **avant** l'import des données. Elle modifie les colonnes de pourcentage de NUMERIC(5,4) à NUMERIC(6,2) pour permettre le stockage de valeurs de 0 à 100.

** Résolution des problèmes courants** :

<details>
<summary> Erreur "numeric field overflow" (si Étape 2 non exécutée)</summary>

Si vous avez oublié l'Étape 2, vous verrez cette erreur :

```
psycopg2.errors.NumericValueOutOfRange: numeric field overflow
DETAIL: A field with precision 5, scale 4 must round to an absolute value less than 10^1.
```

**Solution** : Retournez à l'Étape 2 et exécutez le script de correction du schéma :

```bash
docker exec -e DB_HOST=postgres ecommerce-dashboard sh -c "cd /tmp && python fix_numeric_overflow.py"
```

Puis relancez l'import (Étape 3).

</details>

<details>
<summary> Erreur "CSV not found" lors de l'import</summary>

Vérifiez que les fichiers CSV sont bien copiés :

```bash
# Vérifier que les fichiers sont présents
docker exec ecommerce-dashboard sh -c "ls -la /tmp/data/*.csv | head -10"

# Vous devriez voir : daily_metrics.csv, products_summary.csv, etc.
```

Si les fichiers ne sont pas là, recommencez l'Étape 1 (docker cp).

</details>

** Pourquoi cette méthode ?** : L'import se fait depuis l'intérieur du réseau Docker, ce qui évite les problèmes de connexion localhost sur Windows et les problèmes de chemins relatifs. La correction du schéma est nécessaire car les données de pourcentage sont stockées au format 0-100 et non 0.00-1.00.

#### 7️⃣ Créer les Dashboards Grafana

Les dashboards Grafana doivent être créés après l'import des données (prend ~2 minutes).

** Méthode 1 : Script Automatique (Recommandé)**

```bash
# Windows
scripts\bin\run_all_dashboards.bat

# Linux/Mac
./scripts/bin/run_all_dashboards.sh

# Ou directement avec Python
python run_all_dashboards.py
```

Ce script exécute automatiquement tous les scripts de création de dashboards dans l'ordre avec un résumé détaillé.

** Méthode 2 : Exécution Manuelle**

```bash
# Installer les dépendances si nécessaire
pip install requests python-dotenv

# Exécuter tous les scripts de création de dashboards
python grafana_dashboards_scripts/create_dashboards_1_3.py
python grafana_dashboards_scripts/create_dashboards_4_6.py
python grafana_dashboards_scripts/create_bi_dashboard.py
python grafana_dashboards_scripts/create_full_dashboard.py
python grafana_dashboards_scripts/create_monitoring_dashboard.py
python grafana_dashboards_scripts/create_prometheus_dashboard.py
```

** Messages de confirmation attendus** :

```
 Product Performance Analysis created successfully
 Customer Segmentation Analysis created successfully
 Customer Journey & Funnel Analysis created successfully
 E-Commerce A/B Test Analytics created successfully
 Cohort Analysis & Retention created successfully
 Predictive Analytics & Forecasting created successfully
 Business Intelligence & Decision Support created successfully
 E-Commerce Full Overview Dashboard created successfully
 E-Commerce Monitoring Dashboard created successfully
 E-Commerce Dashboard (Prometheus) created successfully
```

** Dashboards créés (10 au total)** :

1. Product Performance Analysis
2. Customer Segmentation Analysis
3. Customer Journey & Funnel Analysis
4. E-Commerce A/B Test Analytics
5. Cohort Analysis & Retention
6. Predictive Analytics & Forecasting
7. Business Intelligence & Decision Support
8. E-Commerce Full Overview Dashboard
9. E-Commerce Monitoring Dashboard
10. E-Commerce Dashboard (Prometheus)

** En cas d'erreur** :

```bash
# Vérifier que Grafana est accessible
curl http://localhost:3000/api/health

# Vérifier les identifiants Grafana
# Par défaut : admin / admin123
```

** Messages de confirmation attendus** :

```
 Product Performance Analysis created successfully
 Customer Segmentation Analysis created successfully
 Customer Journey & Funnel Analysis created successfully
 E-Commerce A/B Test Analytics created successfully
 Cohort Analysis & Retention created successfully
 Predictive Analytics & Forecasting created successfully
 Business Intelligence & Decision Support created successfully
 E-Commerce Full Overview Dashboard created successfully
 E-Commerce Monitoring Dashboard created successfully
 E-Commerce Dashboard (Prometheus) created successfully
```

** Dashboards créés (10 au total)** :

1. Product Performance Analysis
2. Customer Segmentation Analysis
3. Customer Journey & Funnel Analysis
4. E-Commerce A/B Test Analytics
5. Cohort Analysis & Retention
6. Predictive Analytics & Forecasting
7. Business Intelligence & Decision Support
8. E-Commerce Full Overview Dashboard
9. E-Commerce Monitoring Dashboard
10. E-Commerce Dashboard (Prometheus)

** En cas d'erreur** :

```bash
# Vérifier que Grafana est accessible
curl http://localhost:3000/api/health

# Vérifier les identifiants Grafana
# Par défaut : admin / admin123
```

#### 8️⃣ Accéder aux Applications

| Application | URL | Identifiants | Description |
| --------------------- | ---------------------------------------------- | ------------------- | ------------------------------------------------------ |
| **Dashboard Dash** | [http://localhost:8050](http://localhost:8050) | admin / admin123 | Application principale avec 12 pages + Assistant Vocal |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | admin / admin123 | 10 dashboards de monitoring |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Aucun | Métriques en temps réel |
| ️ **PostgreSQL** | localhost:5432 | dashuser / dashpass | Base de données (connexion via client SQL) |

> ** Astuce :** Une fois sur http://localhost:8050, cliquez sur la page puis dites "Explique l'accueil" pour découvrir toutes les fonctionnalités !

---

### Tester que Tout Fonctionne

**Test 1 : Dashboard Dash**

1. Ouvrir http://localhost:8050
2. Vous devriez voir la page d'accueil avec des KPIs

**Test 2 : Grafana**

1. Ouvrir http://localhost:3000
2. Se connecter avec admin / admin123
3. Aller dans Dashboards → Vous devriez voir 10 dashboards

**Test 3 : Données PostgreSQL**

```bash
# Vérifier le nombre de produits
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -c "SELECT COUNT(*) as nb_produits FROM products_summary;"
# Devrait afficher un nombre > 0
```

---

### � Tests de Sécurité Automatisés

Le projet inclut un système complet de **détection d'attaques en temps réel** avec 41 types d'attaques simulées et monitoring via Grafana.

#### Lancement Rapide des Tests de Sécurité

**Windows** :

```bash
# Double-cliquer sur le fichier ou exécuter dans cmd :
lancer_tests_securite.bat
```

**Linux/Mac** :

```bash
# Rendre le script exécutable et lancer :
chmod +x lancer_tests_securite.sh
./lancer_tests_securite.sh
```

Le script effectue automatiquement :

1. Vérification des services (Dashboard, Prometheus, Pushgateway)
2. Lancement de 41 tests d'attaque sur l'application
3. Envoi des métriques vers Prometheus
4. Affichage du résumé des résultats

#### Visualisation des Alertes dans Grafana

**Accéder au Dashboard de Sécurité** :

1. Ouvrir [http://localhost:3000](http://localhost:3000)
2. Se connecter avec `admin` / `admin123`
3. Aller dans **Dashboards** → **Security Attacks - Real-time Monitoring**

**Dashboard inclut 8 panneaux** :

- Compteur total des attaques détectées
- Attaques critiques (SQL injection, Command injection, etc.)
- Attaques haute sévérité (XSS, CSRF, etc.)
- Attaques moyenne sévérité (Information disclosure, etc.)
- Taux d'attaques par minute
- Distribution par catégorie et sévérité
- Tableau des 20 dernières attaques

#### Règles d'Alerte Configurées

**32+ règles d'alerte actives** incluant :

- **Critical** : SQL Injection, Command Injection, Path Traversal
- **High** : XSS, CSRF, File Upload, Authentication Bypass
- **Medium** : Information Disclosure, Weak Cryptography

Les alertes se déclenchent **30-60 secondes** après détection d'une attaque.

#### Types d'Attaques Testées (41 au total)

| Catégorie | Nombre | Exemples |
| --------------------------- | ------ | -------------------------------------------- |
| ️ Injection SQL | 5 | UNION attacks, Blind SQL, Time-based SQLi |
| Injection de Commandes | 3 | OS command injection, Shell injection |
| Cross-Site Scripting | 4 | Stored XSS, Reflected XSS, DOM XSS |
| Authentification | 6 | Brute force, Session hijacking, Token bypass |
| Manipulation de Fichiers | 5 | Path traversal, File upload, LFI/RFI |
| Sécurité Session | 4 | Session fixation, Cookie hijacking |
| ️ CSRF | 3 | Token bypass, Same-site bypass |
| Information Disclosure | 4 | Error exposure, Directory listing |
| Access Control | 3 | IDOR, Privilege escalation |
| DoS/Resource Abuse | 4 | Rate limit bypass, Resource exhaustion |

#### ️ Test Manuel (avancé)

```bash
# Activer l'environnement virtuel
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/Mac

# Lancer les tests
python test_security_simple.py

# Résultats attendus :
# 41 attaques testées
# Métriques envoyées à Prometheus
# Rapports générés dans security-reports/attack-results/
```

#### Fichiers et Documentation

- `test_security_simple.py` - Script de test principal (41 attaques)
- `GUIDE_COLLABORATEURS.md` - Guide complet pour collaborateurs
- `monitoring/grafana/dashboards/security-attacks-realtime.json` - Dashboard Grafana
- `monitoring/grafana/provisioning/alerting/attack-alerts.yml` - Règles d'alerte (32+)
- `security-reports/attack-results/` - Rapports JSON des tests

#### ️ Notes Importantes

- Les tests sont **non destructifs** et utilisent l'endpoint `/health` de l'application
- Toutes les attaques sont **simulées** et **loggées** uniquement
- Les métriques sont conservées dans Prometheus pendant 15 jours
- Falco n'est pas disponible sur WSL2 (incompatibilité kernel)

---

### �️ Commandes Utiles au Quotidien

#### Redémarrer les Services

```bash
# Redémarrer tous les services
docker compose -f docker-compose.secure.yml restart

# Redémarrer un service spécifique
docker compose -f docker-compose.secure.yml restart grafana
```

#### Voir les Logs

```bash
# Logs de tous les services
docker compose -f docker-compose.secure.yml logs -f

# Logs d'un service spécifique
docker logs ecommerce-dashboard -f
docker logs ecommerce-postgres -f
docker logs ecommerce-grafana -f
```

#### Arrêter les Services

```bash
# Arrêter sans supprimer les données
docker compose -f docker-compose.secure.yml down

# Arrêter ET supprimer toutes les données (️ ATTENTION)
docker compose -f docker-compose.secure.yml down -v
```

#### Reconstruire après Modifications du Code

```bash
# Reconstruire et redémarrer
docker compose -f docker-compose.secure.yml up -d --build

# Forcer la reconstruction complète
docker compose -f docker-compose.secure.yml build --no-cache
docker compose -f docker-compose.secure.yml up -d
```

---

### 🆘 Résolution des Problèmes Courants

#### Problème : "Port already in use"

```bash
# Trouver quel processus utilise le port
# Windows :
netstat -ano | findstr :8050
netstat -ano | findstr :3000

# Linux/Mac :
lsof -i :8050
lsof -i :3000

# Solution : Arrêter le processus ou changer le port dans docker-compose.secure.yml
```

#### Problème : "Container is unhealthy"

```bash
# Voir les détails de santé du conteneur
docker inspect ecommerce-postgres --format='{{.State.Health}}'

# Voir les logs pour comprendre le problème
docker logs ecommerce-postgres --tail 50

# Solution : Redémarrer le conteneur problématique
docker compose -f docker-compose.secure.yml restart postgres
```

#### Problème : "No data in Grafana dashboards"

```bash
# 1. Vérifier que PostgreSQL contient des données
docker exec -e DB_HOST=postgres ecommerce-dashboard python -c "import psycopg2; conn = psycopg2.connect(host='postgres', database='ecommerce_db', user='dashuser', password='dashpass'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM daily_metrics'); print(f'daily_metrics: {cur.fetchone()[0]} rows'); cur.execute('SELECT COUNT(*) FROM products_summary'); print(f'products_summary: {cur.fetchone()[0]} rows')"

# Si le résultat est 0, refaites l'import des données (Étape 6)

# 2. Vérifier que l'exporter Prometheus fonctionne
curl http://localhost:9200/metrics 2>/dev/null | grep ecommerce

# 3. Vérifier que Prometheus scrape l'exporter
# Ouvrir http://localhost:9090/targets et vérifier que "ecommerce-exporter" est UP

# 4. Recréer les dashboards Grafana si nécessaire (Étape 7)
python grafana_dashboards_scripts/create_dashboards_1_3.py
python grafana_dashboards_scripts/create_dashboards_4_6.py
# ... (tous les autres scripts)
```

#### Problème : "Cannot import psycopg2" lors de la création des dashboards

```bash
# Installer les dépendances Python localement
pip install psycopg2-binary requests python-dotenv

# Réessayer la création des dashboards
python grafana_dashboards_scripts/create_dashboards_1_3.py
```

**Note** : Cette erreur apparaît uniquement lors de l'exécution des scripts de création de dashboards Grafana depuis votre machine locale, pas lors de l'import des données qui s'exécute dans le conteneur Docker.

---

### Structure du Projet

```
ecommerce-abtest-dashboard/
├── dashboard/ # Application Dash (Frontend)
│ ├── app.py # Point d'entrée principal
│ ├── pages/ # Pages du dashboard
│ └── components/ # Composants réutilisables
├── data/
│ └── clean/ # Données CSV nettoyées
├── infrastructure/ # 🆕 Infrastructure & Deployment
│ ├── docker/ # Dockerfiles du projet
│ │ ├── Dockerfile # Image principale Dash
│ │ ├── Dockerfile.exporter # Image exporteur Prometheus
│ │ ├── Dockerfile.dashboard-init # Image init dashboards
│ │ └── README.md # Documentation des Dockerfiles
│ ├── k8s/ # Manifests Kubernetes
│ └── config/ # Configuration réseau/firewall
├── monitoring/ # 🆕 Stack Observabilité
│ ├── grafana/ # Dashboards & alertes
│ │ ├── dashboards/ # Fichiers JSON des dashboards
│ │ └── provisioning/ # Configuration Grafana
│ ├── prometheus/ # Métriques time-series
│ ├── loki/ # Agrégation logs
│ ├── promtail/ # Collection logs
│ ├── falco/ # Détection intrusions
│ ├── grafana_dashboards_scripts/ # Scripts création dashboards
│ │ ├── create_dashboards_1_3.py # Dashboards 1-3
│ │ ├── create_dashboards_4_6.py # Dashboards 4-6
│ │ ├── create_bi_dashboard.py # BI Dashboard
│ │ ├── create_full_dashboard.py # Full Dashboard
│ │ ├── create_monitoring_dashboard.py
│ │ ├── create_prometheus_dashboard.py
│ │ └── README.md # Documentation des scripts
│ └── tools/ # Outils monitoring
├── scripts/ # Scripts ETL & Analyse
│ ├── bin/ # 🆕 Scripts exécutables
│ │ ├── run_all_dashboards.bat # Windows - Créer dashboards
│ │ ├── run_all_dashboards.sh # Linux/Mac - Créer dashboards
│ │ ├── run_tests.bat # Windows - Lancer tests
│ │ ├── run_tests.sh # Linux/Mac - Lancer tests
│ │ └── README.md # Documentation des scripts
│ ├── data_prep/ # ETL pipeline
│ ├── kpi_analysis/ # Analyse KPI
│ └── ab_testing/ # Tests A/B
├── docs/ # Documentation
│ └── visualizations/ # Graphiques PNG
├── run_all_dashboards.py # Script Python pour créer tous les dashboards
├── docker-compose.secure.yml # Configuration Docker
└── README.md # Ce fichier
```

**🆕 Nouveautés** :

- Infrastructure consolidée dans `infrastructure/` (docker, k8s, config)
- Stack monitoring complète dans `monitoring/`
- Scripts organisés par fonction dans `scripts/`

---

### Contribution

Pour contribuer au projet :

1. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
2. Faire vos modifications
3. Tester localement : `docker compose -f docker-compose.secure.yml up -d --build`
4. Commit : `git commit -m "feat: description"`
5. Push : `git push origin feature/ma-fonctionnalite`
6. Créer une Pull Request sur GitHub

---

### Support

- Email : [votre-email@example.com]
- Slack : #ecommerce-dashboard
- Documentation complète : [docs/README.md](docs/)

---

---

## Démo en Ligne

**Dashboard accessible à** : http://localhost:8050

**Pages disponibles** :

- Accueil - Vue d'ensemble et KPIs
- Trafic - Analyse des visiteurs
- ️ Comportement - Patterns d'engagement
- Conversions - Funnel analysis
- Produits - Performance et Pareto
- Funnel - Visualisation tunnel
- Simulations A/B - 16 scénarios
- Résultats A/B - Analyse statistique
- Calculateur Z-Test - Outil interactif
- Visualisations - Graphiques avancés
- Méthodologie - Guide complet
- ️ À Propos - Documentation projet

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

## Milestone 1 : Dataset & Préparation des Données 

**Statut** : COMPLÉTÉ (8 issues) 
**Branche** : `feature/data-preprocessing` 
**Période** : Décembre 2025

### Dataset RetailRocket

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

## Issues Complétées

### Issue #1 : Télécharger le dataset RetailRocket 

**Fichiers créés :**

- `scripts/download_data.py` : Script de téléchargement via Kaggle API
- Données brutes (942 MB) → nettoyées (536 MB)

### Issue #2 : Inspecter les fichiers CSV 

**Fichiers créés :**

- `scripts/inspect_csv.py` : Analyse exploratoire des données
- Résultats : 460 doublons détectés dans `events.csv`

### Issue #3 : Nettoyer events.csv 

**Fichiers créés :**

- `scripts/clean_events.py` : Suppression des doublons
- `data/clean/events_cleaned.csv` : 2,755,641 lignes (460 doublons supprimés)

### Issue #4 : Nettoyer item_properties.csv 

**Fichiers créés :**

- `scripts/clean_item_properties.py` : Parsing et structuration
- `data/clean/item_properties_cleaned.csv` : 20,275,902 lignes, 9 colonnes typées

### Issue #5 : Fusionner les données 

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

### Issue #6 : Générer data_clean.csv 

**Fichiers créés :**

- `scripts/generate_data_clean_simple.py` : Consolidation optimisée par chunks
- `data/clean/data_clean.csv` : 2.7M lignes, 13 colonnes (229 MB)
- **Colonnes** : user_id, session_id, timestamp, date, hour, day_of_week, event_type, product_id, transaction_id, amount, segment, product_views, product_purchases

### Issue #7 : Générer daily_metrics.csv 

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

### Issue #8 : Générer products_summary.csv 

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

## KPIs Globaux

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

## Structure des données

```
data/
├── raw/ # Données brutes (942 MB)
│ ├── events.csv
│ ├── item_properties.csv
│ └── category_tree.csv
│
└── clean/ # Données nettoyées et enrichies
 ├── events_cleaned.csv # 2.7M événements nettoyés
 ├── data_clean.csv # 2.7M lignes consolidées (229 MB)
 ├── daily_metrics.csv # 139 jours de métriques (24 KB)
 ├── products_summary.csv # 235K produits analysés (20 MB)
 │
 ├── events_enriched.csv # Événements + segments + produits (242 MB)
 ├── sessions_enriched.csv # Sessions + segments (134 MB)
 ├── transactions_enriched.csv # Transactions enrichies (2 MB)
 │
 ├── daily_funnel.csv # Entonnoir quotidien
 ├── hourly_analysis.csv # Activité horaire
 ├── segment_performance.csv # Performance par segment
 ├── user_journey.csv # Parcours utilisateurs (105 MB)
 └── product_performance.csv # Performance produits (7.5 MB)
```

---

## ️ Scripts développés

```
scripts/
├── download_data.py # Téléchargement Kaggle
├── inspect_csv.py # Exploration données
├── clean_events.py # Nettoyage événements
├── clean_item_properties.py # Nettoyage propriétés
├── merge_data.py # Fusion et enrichissement
├── generate_data_clean_simple.py # Consolidation données
├── generate_daily_metrics.py # Métriques quotidiennes
└── generate_products_summary.py # Analyse produits
```

---

## Utilisation

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

## Insights clés

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

## Milestones du Projet

### Milestone 1 : Dataset & Préparation des Données

**Statut** : COMPLÉTÉ (8/8 issues) 
**Branche** : `feature/data-preprocessing` 
**Date** : Décembre 2025

**Livrables** :

- Téléchargement et nettoyage des données RetailRocket
- 8 tables enrichies (490 MB)
- Scripts de transformation et agrégation
- Métriques quotidiennes et analyse produits

---

### Milestone 2 : KPIs & Métriques Business

**Statut** : COMPLÉTÉ (6/6 issues) 
**Branche** : `feature/kpi-metrics` 
**Date** : Décembre 2025

**Livrables** :

- Calcul des KPIs principaux (conversion, revenu, engagement)
- Segmentation utilisateurs (New, Occasional, Regular, Premium)
- Analyse temporelle (daily, weekly, monthly)
- Moyennes mobiles et tendances
- Métriques par produit et catégorie

---

### Milestone 3 : A/B Testing & Simulations

**Statut** : COMPLÉTÉ (10/10 issues) 
**Branche** : `feature/ab-testing` 
**Date** : Décembre 2025

**Livrables** :

- 16 scénarios de test A/B simulés
- Simulations Monte Carlo (10,000 itérations/scenario)
- Tests statistiques (Chi-Square, Z-Test)
- Calcul puissance statistique (78-81%)
- Données de simulation sur 30 jours (480 lignes)
- Métriques : lift, confidence, p-value, ROI

---

### Milestone 4 : Dashboard Interactif

**Statut** : COMPLÉTÉ (19/19 issues) 
**Branche** : `feature/dashboard-home` 
**Date** : Décembre 2025

**Livrables** :

- Application Dash multi-pages (12 pages)
- Visualisations Plotly interactives (60+ graphiques)
- Filtres dynamiques (date, segment, produit)
- Page Accueil avec KPIs temps réel
- Pages d'analyse : Trafic, Comportement, Conversions
- Pages produits : Performance, Pareto, Funnel
- Pages A/B : Simulations, Résultats, Calculateur
- Page Visualisations avancées
- Page Méthodologie (guide complet)
- Page À Propos (documentation)
- Thème dark moderne avec Bootstrap 5
- Gestion d'erreurs et callbacks optimisés

**Technologies** :

- Python 3.12+
- Dash 2.14.2
- Plotly 5.18.0
- Pandas, NumPy, SciPy
- Bootstrap 5 + Font Awesome

---

### Milestone 5 : Docker & Déploiement

**Statut** : EN COURS (11/14 issues complétées) 
**Branche** : `feature/docker-setup` 
**Date** : Décembre 2025

**Objectif** : Rendre l'application portable et exécutable avec Docker

#### Containerisation Dash App (Issues #28-31)

- [x] **#28** - Créer Dockerfile pour l'application Dash 
- [x] **#29** - Créer docker-compose.yml multi-services 
- [x] **#30** - Tester build de l'image Docker 
- [x] **#31** - Tester run et accès port 8050 

#### PostgreSQL Integration (Issues #41-43)

- [x] **#41** - Créer service Postgres dans docker-compose 
- [x] **#42** - Créer script de migration/init SQL 
- [x] **#43** - Importer les KPIs dans Postgres automatiquement 

#### Grafana Monitoring (Issues #44-48)

- [x] **#44** - Ajouter Grafana dans docker-compose 
- [x] **#45** - Configurer datasource Postgres 
- [x] **#46** - Créer dashboard Grafana (JSON) 
- [ ] **#47** - Panels : sessions, conversion, revenues, erreurs
- [x] **#48** - Test accès http://localhost:3000 

#### Sécurité & Monitoring (Issues #50, #52-53, #55-56)

- [x] **#50** - Optimiser volumes et réseaux 
- [x] **#52** - Configurer Falco pour monitoring sécurité 
- [x] **#53** - Ajouter Loki et Promtail pour collecte logs 
- [x] **#55** - Configurer Grafana pour afficher les logs de sécurité 
- [x] **#56** - Ajouter alertes (connexions suspectes, shell, modifications fichiers) 

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

## Installation & Démarrage

### Prérequis

```bash
# Python 3.12+
pip install -r dashboard/requirements.txt

# Configuration Kaggle API (optionnel pour téléchargement données)
export KAGGLE_USERNAME=<votre_username>
export KAGGLE_KEY=<votre_key>
```

### Lancer le Dashboard

```bash
# Depuis le dossier racine
# Depuis le dossier dashboard
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

````bash
# Build et run tous les services
=======
### Avec Docker (à venir)
```bash
# Build et run
docker-compose up --build

# Services disponibles
# - Dashboard: http://localhost:8050
# - Grafana: http://localhost:3000
# - PostgreSQL: localhost:5432
````

---

## Dépendances

```txt
dash==2.14.2
dash-bootstrap-components==1.5.0
plotly==5.18.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
```

---

## Équipe & Contribution

**Développé par** : Christh Mampassi 
**Email** : cmampassi273@gmail.com 
**Repository** : [Christh2022/ecommerce-abtest-dashboard](https://github.com/Christh2022/ecommerce-abtest-dashboard) 
**Branche main** : `main` 
**Branche dev** : `dev`

---

## License

Ce projet utilise le dataset RetailRocket sous licence publique Kaggle.

---

**Dernière mise à jour** : 17 décembre 2025 
**Version** : 1.1.0 
**Milestones complétés** : 4/5 
**Issues résolues** : 43/57

**Changelog v1.1.0** (17 décembre 2025) :

- **NOUVEAU** : Assistant vocal intelligent avec reconnaissance vocale
- Système de commandes vocales pour navigation mains-libres
- ️ Explications guidées de l'application par la voix
- Interaction continue avec questions/réponses automatiques
- Synthèse vocale multilingue (français)
- Amélioration des icônes Font Awesome (v6.5.1)
- Documentation enrichie avec section assistant vocal

**Changelog v1.0.1** (14 décembre 2025) :

- Correction du problème de numeric overflow lors de l'import des données
- Ajout du script `fix_numeric_overflow.py` pour corriger automatiquement le schéma
- Mise à jour de la documentation avec les étapes correctes d'import
- Amélioration des instructions pour les collaborateurs

---

## Roadmap Future

### Version 1.2.0 (À venir)

- Extension des commandes vocales (20+ commandes)
- Navigation vocale vers toutes les pages du dashboard
- Visualisation réactive aux commandes vocales
- Support multilingue (anglais, espagnol)

### Version 2.0.0 (Q1 2026)

- Intégration d'IA pour analyses prédictives
- Recommandations automatiques basées sur les KPIs
- Alertes vocales en temps réel
- Application mobile avec assistant vocal
