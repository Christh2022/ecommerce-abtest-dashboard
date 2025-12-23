# 🚀 Guide de Démarrage Rapide

## ⚡ Commandes Essentielles

### 1️⃣ Créer Tous les Dashboards Grafana

**Windows** :

```bash
bin\run_all_dashboards.bat
```

**Unix/Mac/Linux** :

```bash
./bin/run_all_dashboards.sh
```

**Direct Python** :

```bash
python run_all_dashboards.py
```

---

### 2️⃣ Lancer l'Application Complète

```bash
docker-compose -f docker-compose.secure.yml up -d
```

---

### 3️⃣ Valider l'Organisation

```bash
python tools/validate_dashboard_organization.py
```

---

### 4️⃣ Exécuter les Tests

**Windows** :

```bash
bin\run_tests.bat
```

**Unix/Mac/Linux** :

```bash
./bin/run_tests.sh
```

**Direct Python** :

```bash
python run_tests.py
```

---

## 📂 Structure du Projet en 1 Minute

```
ecommerce-abtest-dashboard/
│
├── 📊 grafana_dashboards_scripts/    # Scripts de création de dashboards
│   └── 6 scripts Python + README
│
├── 🐳 docker/                        # Tous les Dockerfiles
│   └── 3 Dockerfiles + README
│
├── 🔧 bin/                           # Scripts exécutables (.bat/.sh)
│   └── 4 scripts wrapper + README
│
├── 🛠️ tools/                         # Utilitaires Python
│   └── 4 scripts utilitaires + README
│
└── 📁 dashboard/                     # Application Dash principale
    └── Interface web + auth + pages
```

---

## 🎯 Accès Rapide aux Services

### Après `docker-compose up -d` :

| Service            | URL                           | Identifiants                |
| ------------------ | ----------------------------- | --------------------------- |
| **Dashboard Dash** | http://localhost:8050         | Voir `dashboard/users.json` |
| **Grafana**        | http://localhost:3000         | admin / admin               |
| **Prometheus**     | http://localhost:9090         | -                           |
| **Métriques**      | http://localhost:9200/metrics | -                           |

---

## 📚 Documentation Complète

### Par Dossier

- [grafana_dashboards_scripts/README.md](grafana_dashboards_scripts/README.md) - Dashboards
- [docker/README.md](docker/README.md) - Docker
- [bin/README.md](bin/README.md) - Scripts
- [tools/README.md](tools/README.md) - Utilitaires

### Générale

- [ORGANISATION_PROJET.md](ORGANISATION_PROJET.md) - Structure complète
- [RECAPITULATIF_REORGANISATION.md](RECAPITULATIF_REORGANISATION.md) - Réorganisation
- [README.md](README.md) - Documentation principale

---

## 🔥 Workflow Typique

### Développement Local

1. **Démarrer les services** :

   ```bash
   docker-compose -f docker-compose.secure.yml up -d
   ```

2. **Créer les dashboards** :

   ```bash
   bin\run_all_dashboards.bat   # Windows
   ./bin/run_all_dashboards.sh  # Unix
   ```

3. **Accéder à l'application** :

   - Dashboard : http://localhost:8050
   - Grafana : http://localhost:3000

4. **Valider** :
   ```bash
   python tools/validate_dashboard_organization.py
   ```

---

### Déploiement Kubernetes

1. **Build les images** :

   ```bash
   docker build -t ecommerce-dashboard:latest -f docker/Dockerfile .
   docker build -t ecommerce-exporter:latest -f docker/Dockerfile.exporter .
   ```

2. **Déployer** :

   ```bash
   # Windows
   .\k8s\deploy.ps1

   # Unix
   ./k8s/deploy.sh
   ```

3. **Vérifier** :
   ```bash
   kubectl get pods -n ecommerce-monitoring
   ```

---

## 🛠️ Commandes Docker Utiles

### Logs

```bash
# Tous les services
docker-compose -f docker-compose.secure.yml logs -f

# Service spécifique
docker-compose -f docker-compose.secure.yml logs -f dashboard
```

### Rebuild

```bash
# Rebuild complet
docker-compose -f docker-compose.secure.yml up -d --build

# Rebuild un service
docker-compose -f docker-compose.secure.yml build dashboard
docker-compose -f docker-compose.secure.yml up -d dashboard
```

### Arrêt/Nettoyage

```bash
# Arrêter
docker-compose -f docker-compose.secure.yml down

# Arrêter et supprimer volumes
docker-compose -f docker-compose.secure.yml down -v
```

---

## 📊 Les 10 Dashboards Grafana

| #   | Nom                       | Description                  |
| --- | ------------------------- | ---------------------------- |
| 1   | Performance Générale      | Vue d'ensemble des KPIs      |
| 2   | Analyse des Conversions   | Taux de conversion et tunnel |
| 3   | Comportement Utilisateurs | Navigation et engagement     |
| 4   | Revenue Analysis          | Revenus et panier moyen      |
| 5   | Traffic Sources           | Sources de trafic            |
| 6   | Device Analytics          | Analyse par appareil         |
| 7   | Full E-commerce           | Dashboard complet            |
| 8   | BI Dashboard              | Business Intelligence        |
| 9   | Monitoring                | Monitoring système           |
| 10  | Prometheus Metrics        | Métriques techniques         |

**Créer tous les dashboards** :

```bash
python run_all_dashboards.py
```

---

## 🆘 Résolution Rapide

### Dashboard ne se lance pas

```bash
# Vérifier les logs
docker-compose -f docker-compose.secure.yml logs dashboard

# Rebuild
docker-compose -f docker-compose.secure.yml build dashboard
docker-compose -f docker-compose.secure.yml up -d dashboard
```

### Grafana ne crée pas les dashboards

```bash
# Vérifier les logs d'initialisation
docker-compose -f docker-compose.secure.yml logs dashboard-init

# Recréer manuellement
bin\run_all_dashboards.bat   # Windows
./bin/run_all_dashboards.sh  # Unix
```

### Base de données problématique

```bash
# Réinitialiser
docker-compose -f docker-compose.secure.yml down -v
docker-compose -f docker-compose.secure.yml up -d
```

---

## ✅ Checklist Avant Commit

```bash
# 1. Valider l'organisation
python tools/validate_dashboard_organization.py

# 2. Exécuter les tests
python run_tests.py

# 3. Vérifier qu'il n'y a pas d'erreurs
# (Visual inspection dans VS Code)

# 4. Commit
git add .
git commit -m "description du changement"
git push
```

---

## 🎓 Bonnes Pratiques

### 1. Toujours Documenter

- Créer un README.md dans chaque nouveau dossier
- Mettre à jour la documentation existante
- Commenter le code complexe

### 2. Valider Régulièrement

```bash
python tools/validate_dashboard_organization.py
```

### 3. Tester Avant de Commit

```bash
python run_tests.py
```

### 4. Suivre les Conventions

- **Scripts Python** : `snake_case.py`
- **Scripts Shell** : `kebab-case.sh`
- **Documentation** : `UPPERCASE.md`
- **Dossiers** : `lowercase_underscores/`

---

## 📞 Aide

### Documentation Détaillée

- [ORGANISATION_PROJET.md](ORGANISATION_PROJET.md) - Structure complète
- [README.md](README.md) - Vue d'ensemble

### Documentation Sécurité

- [SECURITY.md](SECURITY.md) - Politique de sécurité
- [docs/AUTHENTICATION_ARCHITECTURE.md](docs/AUTHENTICATION_ARCHITECTURE.md)
- [docs/DDOS_PROTECTION_REPORT.md](docs/DDOS_PROTECTION_REPORT.md)

---

**Dernière mise à jour** : Réorganisation 2.0  
**Statut** : ✅ Production Ready
