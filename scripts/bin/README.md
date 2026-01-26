# Scripts Exécutables du Projet

Ce dossier contient tous les scripts exécutables pour faciliter l'utilisation du projet.

## 📋 Scripts Disponibles

### 🎨 Dashboards Grafana

#### `run_all_dashboards.bat` (Windows)

Script batch pour créer tous les dashboards Grafana en une seule commande.

**Utilisation:**

```cmd
scripts\bin\run_all_dashboards.bat
```

#### `run_all_dashboards.sh` (Linux/Mac)

Script shell pour créer tous les dashboards Grafana en une seule commande.

**Utilisation:**

```bash
./scripts/bin/run_all_dashboards.sh
# ou
bash scripts/bin/run_all_dashboards.sh
```

**Ce que fait ce script:**

- ✅ Vérifie que Python est installé
- ✅ Exécute `run_all_dashboards.py`
- ✅ Crée automatiquement les 10 dashboards Grafana
- ✅ Affiche un rapport de succès/échec

---

### 🧪 Tests

#### `run_tests.bat` (Windows)

Script batch pour exécuter tous les tests du projet.

**Utilisation:**

```cmd
scripts\bin\run_tests.bat
```

#### `run_tests.sh` (Linux/Mac)

Script shell pour exécuter tous les tests du projet.

**Utilisation:**

```bash
./scripts/bin/run_tests.sh
# ou
bash scripts/bin/run_tests.sh
```

**Ce que fait ce script:**

- ✅ Vérifie que Python est installé
- ✅ Exécute `run_tests.py`
- ✅ Lance tous les tests unitaires
- ✅ Affiche les résultats

---

## 🚀 Utilisation Rapide

### Depuis la Racine du Projet

```bash
# Windows
scripts\bin\run_all_dashboards.bat
scripts\bin\run_tests.bat

# Linux/Mac
./scripts/bin/run_all_dashboards.sh
./scripts/bin/run_tests.sh
```

### Depuis le Dossier bin

```bash
# Se déplacer dans le dossier
cd bin

# Windows
run_all_dashboards.bat
run_tests.bat

# Linux/Mac
./run_all_dashboards.sh
./run_tests.sh
```

## ⚙️ Configuration

### Variables d'Environnement (Dashboards)

Les scripts de dashboards utilisent ces variables:

| Variable           | Description         | Défaut                  |
| ------------------ | ------------------- | ----------------------- |
| `GRAFANA_URL`      | URL de Grafana      | `http://localhost:3000` |
| `GRAFANA_USER`     | Utilisateur Grafana | `admin`                 |
| `GRAFANA_PASSWORD` | Mot de passe        | `admin123`              |

**Exemple:**

```bash
# Windows (CMD)
set GRAFANA_URL=http://grafana.example.com:3000
bin\run_all_dashboards.bat

# Windows (PowerShell)
$env:GRAFANA_URL="http://grafana.example.com:3000"
bin\run_all_dashboards.bat

# Linux/Mac
export GRAFANA_URL=http://grafana.example.com:3000
./bin/run_all_dashboards.sh
```

## 🔍 Que Font Ces Scripts ?

### run_all_dashboards.\*

1. Vérifie que Python est installé
2. Exécute le script Python `run_all_dashboards.py`
3. Ce script Python:
   - Crée les dashboards 1-3 (Funnel, Segmentation, Products)
   - Crée les dashboards 4-6 (Cohorts, Real-Time, Predictive)
   - Crée le dashboard Business Intelligence
   - Crée le dashboard E-Commerce complet
   - Crée le dashboard Monitoring
   - Crée le dashboard Prometheus
4. Affiche un résumé avec statistiques

### run_tests.\*

1. Vérifie que Python est installé
2. Exécute le script Python `run_tests.py`
3. Ce script Python:
   - Lance les tests unitaires
   - Vérifie l'intégrité du code
   - Valide les configurations
4. Affiche les résultats des tests

## 🛠️ Dépannage

### Windows: "Python n'est pas reconnu"

```cmd
# Vérifier l'installation de Python
python --version

# Si non installé, téléchargez depuis python.org
# Assurez-vous de cocher "Add Python to PATH" lors de l'installation
```

### Linux/Mac: "Permission denied"

```bash
# Rendre les scripts exécutables
chmod +x bin/run_all_dashboards.sh
chmod +x bin/run_tests.sh

# Puis réessayer
./bin/run_all_dashboards.sh
```

### Erreur "Connection refused" (Dashboards)

```bash
# Vérifier que Grafana est démarré
docker ps | grep grafana

# Vérifier que Grafana répond
curl http://localhost:3000/api/health
```

## 📖 Documentation Associée

- [run_all_dashboards.py](../run_all_dashboards.py) - Script Python principal
- [run_tests.py](../run_tests.py) - Script de tests Python
- [GUIDE_DASHBOARDS.md](../GUIDE_DASHBOARDS.md) - Guide complet des dashboards
- [README.md](../README.md) - Documentation principale

## 💡 Alternative: Exécuter Directement avec Python

Si vous préférez, vous pouvez exécuter les scripts Python directement:

```bash
# Dashboards
python run_all_dashboards.py

# Tests
python run_tests.py
```

Les scripts batch/shell sont juste des wrappers pratiques qui:

- Vérifient les prérequis
- Gèrent les erreurs
- Affichent des messages formatés

## 🎯 Avantages de Ces Scripts

| Avantage              | Description                           |
| --------------------- | ------------------------------------- |
| **Simplicité**        | Une seule commande pour tout exécuter |
| **Multi-plateforme**  | Versions Windows et Unix              |
| **Vérifications**     | Détection automatique des problèmes   |
| **Messages clairs**   | Output formaté et lisible             |
| **Gestion d'erreurs** | Codes de retour appropriés            |

## 📊 Structure

```
bin/
├── run_all_dashboards.bat  # Windows - Création dashboards
├── run_all_dashboards.sh   # Unix - Création dashboards
├── run_tests.bat           # Windows - Exécution tests
├── run_tests.sh            # Unix - Exécution tests
└── README.md               # Ce fichier
```

## 🔗 Liens Utiles

- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Dashboard Dash**: http://localhost:8050

---

**Dernière mise à jour**: 23 Décembre 2025  
**Statut**: ✅ Opérationnel
