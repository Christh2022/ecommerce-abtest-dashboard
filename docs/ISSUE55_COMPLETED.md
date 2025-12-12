# Issue #55: Configurer Grafana pour afficher les logs de sécurité - COMPLETED ✅

**Status:** Resolved  
**Branch:** `feature/security-intrusion`  
**Completed:** December 12, 2025

---

## 🎯 Objectif

Configurer Grafana pour visualiser et monitorer les logs de sécurité collectés par Loki/Promtail, avec un focus particulier sur les alertes de sécurité générées par Falco.

---

## 📋 Solution Implémentée

### 1. Datasource Loki dans Grafana

**Fichier:** `grafana/provisioning/datasources/loki.yml`

Configuration automatique de la datasource Loki :
- **URL:** http://loki:3100
- **Type:** Loki
- **Access:** Proxy
- **Max Lines:** 1000 par requête
- **Auto-provisioning:** Oui

### 2. Dashboard Security & Application Logs

**Fichier:** `grafana/dashboards/security-logs.json`

Dashboard comprenant **7 panels** :

#### Panel 1: Falco Security Events by Priority
- **Type:** Time series (bars)
- **Query:** `sum by (priority) (count_over_time({compose_service="falco"} |~ "(?i)(error|warning|critical|alert)" [$__interval]))`
- **Description:** Visualisation des événements de sécurité par niveau de priorité

#### Panel 2: Falco Security Alerts
- **Type:** Logs
- **Query:** `{compose_service="falco"} |~ "(?i)(error|warning|critical)"`
- **Description:** Liste des alertes de sécurité en temps réel

#### Panel 3: Dash Application Logs
- **Type:** Logs
- **Query:** `{compose_service="dash-app"}`
- **Description:** Logs de l'application Dash

#### Panel 4: PostgreSQL Errors & Warnings
- **Type:** Logs
- **Query:** `{compose_service="postgres"} |~ "(?i)(error|warning|fatal)"`
- **Description:** Erreurs et avertissements de la base de données

#### Panel 5: Grafana Logs
- **Type:** Logs
- **Query:** `{compose_service="grafana"}`
- **Description:** Logs de Grafana lui-même

#### Panel 6: Log Volume by Service
- **Type:** Pie chart (donut)
- **Query:** `sum by (compose_service) (count_over_time({compose_project="ecommerce-abtest-dashboard"} [$__range]))`
- **Description:** Distribution du volume de logs par service

#### Panel 7: Error Rate by Service
- **Type:** Time series (line)
- **Query:** `sum by (compose_service) (rate({compose_project="ecommerce-abtest-dashboard"} |~ "(?i)error" [$__interval]))`
- **Description:** Taux d'erreur par service en temps réel

---

## 🔧 Configuration

### Auto-refresh
- **Intervalle:** 30 secondes
- **Période par défaut:** 1 heure

### Tags
- `security`
- `logs`
- `monitoring`

### Accès au Dashboard
- **URL:** http://localhost:3000/d/security-logs
- **Titre:** Security & Application Logs

---

## ✅ Tests de Validation

### 1. Datasource Loki

```bash
curl -u admin:admin123 http://localhost:3000/api/datasources | grep -i loki
# ✅ Datasource "Loki" configurée et accessible
```

### 2. Connectivité Loki

```bash
curl http://localhost:3100/ready
# ✅ ready
```

### 3. Dashboard Chargé

```bash
curl -u admin:admin123 http://localhost:3000/api/dashboards/uid/security-logs
# ✅ Dashboard accessible
```

### 4. Logs Collectés

```bash
docker logs ecommerce-promtail --tail 20
# ✅ Promtail collecte les logs de tous les containers
```

---

## 📊 Métriques de Monitoring

### Services Monitorés
1. **Falco** - Intrusion detection logs
2. **Dash App** - Application logs
3. **PostgreSQL** - Database logs
4. **Grafana** - Monitoring platform logs
5. **Prometheus** - Metrics logs
6. **Loki** - Log aggregator logs
7. **Promtail** - Log collector logs

### Types d'Événements Trackés
- ✅ Erreurs (ERROR)
- ✅ Avertissements (WARNING)
- ✅ Événements critiques (CRITICAL)
- ✅ Alertes de sécurité (ALERT)
- ✅ Événements fatals (FATAL)

---

## 🚀 Utilisation

### Accéder au Dashboard

1. Ouvrir Grafana : http://localhost:3000
2. Login : `admin` / `admin123`
3. Naviguer vers **Dashboards** → **Security & Application Logs**

### Rechercher des Logs Spécifiques

**Exemples de requêtes LogQL:**

```logql
# Tous les logs d'un service
{compose_service="dash-app"}

# Logs avec erreurs
{compose_service="dash-app"} |~ "(?i)error"

# Logs de sécurité Falco
{compose_service="falco"} |~ "(?i)(critical|alert)"

# Logs PostgreSQL avec pattern
{compose_service="postgres"} |~ "connection"

# Plusieurs services
{compose_service=~"dash-app|postgres"}

# Recherche case-insensitive
{compose_service="falco"} |~ "(?i)warning"
```

### Filtrer par Période

- **Last 5 minutes** - Monitoring temps réel
- **Last 1 hour** - Vue d'ensemble récente
- **Last 24 hours** - Analyse journalière
- **Custom range** - Investigation spécifique

---

## 📁 Fichiers Créés/Modifiés

### Nouveaux Fichiers

1. **grafana/provisioning/datasources/loki.yml** (13 lignes)
   - Configuration datasource Loki
   - Auto-provisioning activé

2. **grafana/dashboards/security-logs.json** (480 lignes)
   - Dashboard complet avec 7 panels
   - Queries LogQL optimisées
   - Auto-refresh 30s

3. **docs/ISSUE55_COMPLETED.md** (ce fichier)
   - Documentation complète
   - Exemples de requêtes
   - Guide d'utilisation

---

## 🔗 Intégrations

### Avec Issue #53 (Loki/Promtail)
- ✅ Utilise la datasource Loki configurée
- ✅ Affiche les logs collectés par Promtail
- ✅ Visualisation centralisée des logs

### Avec Issue #52 (Falco)
- ✅ Monitoring des alertes de sécurité Falco
- ✅ Dashboard dédié aux événements de sécurité
- ✅ Filtrage par priorité

### Avec Issue #46 (Grafana)
- ✅ S'ajoute aux dashboards existants
- ✅ Réutilise le provisioning automatique
- ✅ Compatible avec les autres datasources

---

## 🎯 Cas d'Usage

### 1. Monitoring Sécurité Temps Réel
- Panel Falco Security Events by Priority
- Auto-refresh 30s
- Alertes visuelles si pics d'événements

### 2. Investigation d'Incidents
- Panel Logs détaillés par service
- Recherche par pattern (regex)
- Timeline des événements

### 3. Analyse de Performance
- Error Rate by Service
- Log Volume by Service
- Identification des services problématiques

### 4. Audit & Compliance
- Logs PostgreSQL (accès données)
- Logs Grafana (accès monitoring)
- Logs Dash (accès application)

---

## 💡 Bonnes Pratiques

### Requêtes LogQL Performantes

```logql
# ✅ BON - Filtre au niveau du label
{compose_service="falco"} |~ "error"

# ❌ MAUVAIS - Trop large, puis filtrage
{compose_project="ecommerce-abtest-dashboard"} |~ "falco.*error"

# ✅ BON - Utilisation de regex case-insensitive
{compose_service="postgres"} |~ "(?i)(error|fatal)"

# ✅ BON - Agrégation avec count_over_time
sum by (priority) (count_over_time({compose_service="falco"}[5m]))
```

### Gestion des Alertes

1. **Définir des seuils** :
   - ERROR rate > 10/min → Warning
   - CRITICAL event → Alert immédiate

2. **Configurer les notifications** :
   - Slack, Email, PagerDuty
   - Via Grafana Alerting

3. **Rotation des logs** :
   - Loki retention: 7 jours (168h)
   - Archivage pour logs critiques

---

## 🔮 Améliorations Futures

### Court Terme
1. Ajouter des alertes Grafana sur les événements critiques
2. Créer des dashboards spécifiques par service
3. Configurer la rotation automatique des logs

### Moyen Terme
1. Intégrer avec un système de notification (Slack, Email)
2. Ajouter des métriques de corrélation (logs + metrics)
3. Créer des rapports automatiques hebdomadaires

### Long Terme
1. Machine Learning pour détection d'anomalies dans les logs
2. Intégration avec SIEM (Security Information and Event Management)
3. Archivage long terme (S3, etc.)

---

## 📚 Ressources

### Documentation
- [Loki LogQL](https://grafana.com/docs/loki/latest/logql/)
- [Grafana Logs Panel](https://grafana.com/docs/grafana/latest/panels/visualizations/logs/)
- [Promtail Configuration](https://grafana.com/docs/loki/latest/clients/promtail/)

### Exemples de Requêtes
- [LogQL Examples](https://grafana.com/docs/loki/latest/logql/log_queries/)
- [Grafana Dashboard Examples](https://grafana.com/grafana/dashboards/)

---

## ✅ Validation Finale

### Checklist
- ✅ Datasource Loki configurée et accessible
- ✅ Dashboard créé avec 7 panels fonctionnels
- ✅ Logs de tous les services visibles
- ✅ Filtrage et recherche opérationnels
- ✅ Auto-refresh activé (30s)
- ✅ Documentation complète

### Tests Effectués
- ✅ Connexion Grafana → Loki
- ✅ Affichage logs en temps réel
- ✅ Requêtes LogQL fonctionnelles
- ✅ Filtrage par service
- ✅ Visualisations correctes

---

## 🎉 Conclusion

Grafana est maintenant configuré pour afficher les logs de sécurité et les logs applicatifs collectés par Loki/Promtail. Le dashboard **Security & Application Logs** offre une vue centralisée et temps réel de tous les événements du système.

**Accès:** http://localhost:3000/d/security-logs

**Issue #55 Status: COMPLETED ✅**

---

## 🔗 Issues Liées

- ✅ Issue #52: Configure Falco (source des alertes de sécurité)
- ✅ Issue #53: Add Loki/Promtail (infrastructure de collecte des logs)
- ✅ Issue #46: Create Grafana Dashboard (infrastructure de visualisation)
- ⏭️ Issue #56: Configurer les alertes automatiques (prochaine étape)

---

**Date de clôture:** 2025-12-12  
**Branche:** feature/security-intrusion  
**Auteur:** E-commerce Dashboard Team
