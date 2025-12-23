# Outils et Scripts Utilitaires

Ce dossier contient les scripts utilitaires et outils du projet.

## 📋 Scripts Disponibles

### 🔍 `ecommerce_exporter.py`

**Exporteur de métriques Prometheus pour e-commerce**

Script qui exporte les métriques de la base de données PostgreSQL vers Prometheus.

**Utilisation:**

```bash
python tools/ecommerce_exporter.py
```

**Variables d'environnement:**

- `DB_HOST` - Hôte PostgreSQL (défaut: localhost)
- `DB_PORT` - Port PostgreSQL (défaut: 5432)
- `DB_NAME` - Nom de la base de données (défaut: ecommerce_db)
- `DB_USER` - Utilisateur (défaut: dashuser)
- `DB_PASSWORD` - Mot de passe

**Port:** 9200 (métriques Prometheus)

---

### 📊 `import_dashboard.py`

**Import de dashboards dans Grafana**

Script pour importer des dashboards Grafana depuis des fichiers JSON.

**Utilisation:**

```bash
python tools/import_dashboard.py
```

---

### 📊 `import_dashboard_to_grafana.py`

**Import avancé de dashboards**

Version améliorée pour l'import de dashboards dans Grafana avec plus d'options.

**Utilisation:**

```bash
python tools/import_dashboard_to_grafana.py
```

**Variables d'environnement:**

- `GRAFANA_URL` - URL de Grafana
- `GRAFANA_USER` - Utilisateur Grafana
- `GRAFANA_PASSWORD` - Mot de passe

---

### ✅ `validate_dashboard_organization.py`

**Validation de l'organisation du projet**

Script de validation pour vérifier que tous les fichiers de dashboards sont correctement organisés.

**Utilisation:**

```bash
python tools/validate_dashboard_organization.py
```

**Ce qu'il vérifie:**

- ✅ Existence du dossier `grafana_dashboards_scripts/`
- ✅ Présence de tous les scripts de dashboards
- ✅ Syntaxe Python valide
- ✅ Fichiers de configuration (Dockerfiles, scripts)
- ✅ Structure des dashboards

---

## 🚀 Utilisation Générale

### Depuis la Racine du Projet

```bash
# Exporter les métriques
python tools/ecommerce_exporter.py

# Importer un dashboard
python tools/import_dashboard.py

# Valider l'organisation
python tools/validate_dashboard_organization.py
```

### Avec Docker

L'exporteur est exécuté automatiquement dans le container `ecommerce-exporter`:

```bash
docker-compose -f docker-compose.secure.yml up -d ecommerce-exporter
```

---

## 📖 Documentation Associée

- [docker/README.md](../docker/README.md) - Documentation des Dockerfiles
- [grafana_dashboards_scripts/README.md](../grafana_dashboards_scripts/README.md) - Scripts de dashboards
- [README.md](../README.md) - Documentation principale

---

## 🔧 Dépendances

Ces scripts nécessitent:

- Python 3.11+
- `requests` - Pour les appels API
- `psycopg2-binary` - Pour PostgreSQL (exporter)
- `prometheus_client` - Pour l'exporteur

Installation:

```bash
pip install -r requirements.txt
```

---

## 🎯 Structure

```
tools/
├── ecommerce_exporter.py           # Exporteur Prometheus
├── import_dashboard.py             # Import dashboards
├── import_dashboard_to_grafana.py  # Import dashboards avancé
├── validate_dashboard_organization.py  # Validation
└── README.md                       # Ce fichier
```

---

## 💡 Bonnes Pratiques

1. **Exporter des métriques** : Utilisez `ecommerce_exporter.py` avec Docker pour un monitoring continu
2. **Valider régulièrement** : Exécutez `validate_dashboard_organization.py` après des modifications
3. **Variables d'environnement** : Utilisez un fichier `.env` pour la configuration
4. **Logs** : Consultez les logs pour le débogage

---

**Dernière mise à jour** : 23 Décembre 2025  
**Statut** : ✅ Opérationnel
