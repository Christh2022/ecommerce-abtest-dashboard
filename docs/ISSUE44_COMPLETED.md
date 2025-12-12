# Issue #44: Grafana dans Docker Compose - COMPLÉTÉ ✅

**Date**: 2025-12-12  
**Status**: ✅ Complété et opérationnel

## 📋 Objectif

Intégrer Grafana dans le stack Docker Compose pour la visualisation en temps réel des KPIs e-commerce et le monitoring des tests A/B.

## 🎯 Réalisations

### 1. ✅ Services Docker Configurés

#### Grafana

```yaml
grafana:
  image: grafana/grafana:latest
  container_name: ecommerce-grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_USER=admin
    - GF_SECURITY_ADMIN_PASSWORD=admin123
    - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
  volumes:
    - grafana-data:/var/lib/grafana
    - ./grafana/provisioning:/etc/grafana/provisioning
    - ./grafana/dashboards:/var/lib/grafana/dashboards
```

**Fonctionnalités**:

- ✅ Port 3000 exposé
- ✅ Volumes persistants pour les données
- ✅ Provisioning automatique des datasources
- ✅ Provisioning automatique des dashboards
- ✅ Health check configuré
- ✅ Plugins pré-installés

#### Loki (Log Aggregation)

```yaml
loki:
  image: grafana/loki:latest
  container_name: ecommerce-loki
  ports:
    - "3100:3100"
  volumes:
    - loki-data:/loki
```

**Fonctionnalités**:

- ✅ Agrégation des logs
- ✅ API disponible sur port 3100
- ✅ Volume persistant
- ✅ Health check

#### Promtail (Log Collection)

```yaml
promtail:
  image: grafana/promtail:latest
  container_name: ecommerce-promtail
  volumes:
    - dash-logs:/var/log/dashboard:ro
```

**Fonctionnalités**:

- ✅ Collection automatique des logs dashboard
- ✅ Envoi vers Loki
- ✅ Mode lecture seule

### 2. ✅ Datasources Configurées

#### PostgreSQL Datasource

**Fichier**: `grafana/provisioning/datasources/postgres.yml`

```yaml
- name: PostgreSQL-Ecommerce
  type: postgres
  url: postgres:5432
  database: ecommerce_db
  user: dashuser
  password: dashpass
  isDefault: true
```

**Configuration avancée**:

- ✅ Max connections: 10
- ✅ SSL désactivé (environnement Docker)
- ✅ PostgreSQL 16
- ✅ Éditable depuis l'UI

#### Loki Datasource

**Ajouté dans le même fichier**:

```yaml
- name: Loki
  type: loki
  url: http://loki:3100
  maxLines: 1000
```

**Fonctionnalités**:

- ✅ Accès aux logs agrégés
- ✅ Liens vers PostgreSQL (derived fields)
- ✅ Limite de 1000 lignes par requête

### 3. ✅ Dashboards Créés

#### Dashboard 1: E-commerce KPIs

**Fichier**: `grafana/dashboards/ecommerce-kpis.json`

**Panels**:

1. **Total Users** (Stat)

   - Somme des utilisateurs uniques
   - Requête: `SELECT SUM(total_users) FROM daily_metrics`

2. **Total Revenue** (Stat)

   - Revenue total cumulé
   - Requête: `SELECT SUM(total_revenue) FROM daily_metrics`

3. **Conversion Rate** (Gauge)

   - Taux de conversion moyen
   - Requête: `SELECT AVG(conversion_rate) FROM daily_metrics`

4. **Daily Metrics Timeline** (Time Series)

   - Évolution des métriques quotidiennes
   - Users, Revenue, Conversions

5. **Top Products** (Table)

   - Top 10 produits par revenue
   - Requête: `SELECT * FROM v_top_products LIMIT 10`

6. **Funnel Visualization** (Bar Chart)
   - Conversion funnel view → cart → purchase

#### Dashboard 2: A/B Testing Analysis (Nouveau)

**Fichier**: `grafana/dashboards/ab-testing-analysis.json`

**Panels**:

1. **Conversion Rates Over Time** (Time Series)

   - Évolution des taux par variant (A vs B)
   - Multi-séries pour chaque scénario

2. **Visitors Distribution** (Pie Chart)

   - Répartition des visiteurs par scénario
   - Somme des visitors par test

3. **A/B Test Summary** (Table)

   - Tableau récapitulatif des tests
   - Control vs Variant avec lift %
   - Statistical significance
   - Status et durée

4. **Revenue Comparison** (Bar Chart)
   - Comparaison revenue par variant
   - Visualisation du gain/perte

**Fonctionnalités avancées**:

- ✅ Auto-refresh toutes les 30s
- ✅ Time range: Last 30 days
- ✅ Colored cells pour les lifts
- ✅ Tags: ecommerce, ab-testing, experiments

### 4. ✅ Provisioning Automatique

**Configuration**: `grafana/provisioning/dashboards/dashboards.yml`

```yaml
providers:
  - name: "E-commerce Dashboards"
    folder: ""
    type: file
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
```

**Avantages**:

- ✅ Chargement automatique des dashboards au démarrage
- ✅ Mise à jour toutes les 10 secondes
- ✅ Éditable depuis l'UI
- ✅ Support de l'arborescence

### 5. ✅ Documentation Complète

**Fichier**: `grafana/README.md`

**Contenu**:

- Architecture du stack de monitoring
- Configuration détaillée de chaque service
- Guide d'utilisation (démarrage, accès, navigation)
- Exemples de requêtes SQL pour panels
- Variables de dashboard
- Sécurité et gestion des utilisateurs
- Plugins recommandés
- Backup & restore
- Troubleshooting complet

## 📊 Tests et Validation

### Services Démarrés ✅

```bash
$ docker ps --filter "name=grafana"
NAMES               STATUS                    PORTS
ecommerce-grafana   Up 39 minutes (healthy)   0.0.0.0:3000->3000/tcp
ecommerce-loki      Up 39 minutes (healthy)   0.0.0.0:3100->3100/tcp
ecommerce-promtail  Up 39 minutes             N/A
```

### Health Check ✅

```bash
$ curl http://localhost:3000/api/health
{
    "database": "ok",
    "version": "12.3.0",
    "commit": "20051fb1fc604fc54aae76356da1c14612af41d0"
}
```

### Datasources ✅

Vérification via API:

```bash
$ curl -s -u admin:admin123 http://localhost:3000/api/datasources
[
  {
    "id": 1,
    "name": "PostgreSQL-Ecommerce",
    "type": "postgres",
    "isDefault": true
  },
  {
    "id": 2,
    "name": "Loki",
    "type": "loki"
  }
]
```

### Dashboards ✅

- ✅ E-commerce KPIs: Chargé et fonctionnel
- ✅ A/B Testing Analysis: Créé et provisionné
- ✅ Accès via: http://localhost:3000/dashboards

## 🎨 Requêtes SQL Utiles

### KPIs Quotidiens

```sql
SELECT
  date,
  total_users,
  total_revenue,
  conversion_rate,
  avg_order_value
FROM v_daily_kpis
ORDER BY date DESC
LIMIT 30;
```

### Top Products

```sql
SELECT
  product_name,
  category,
  total_revenue,
  total_purchases,
  conversion_rate
FROM v_top_products
WHERE total_purchases > 0
LIMIT 20;
```

### A/B Test Performance

```sql
SELECT
  scenario_name,
  variant,
  AVG(conversion_rate) as avg_conv_rate,
  SUM(revenue) as total_revenue,
  SUM(visitors) as total_visitors
FROM ab_test_results r
JOIN ab_test_scenarios s ON r.scenario_id = s.scenario_id
GROUP BY scenario_name, variant
ORDER BY scenario_name, variant;
```

### Funnel Analysis

```sql
SELECT
  stage_name,
  AVG(visitors) as avg_visitors,
  AVG(drop_off) as avg_drop_off,
  AVG(conversion_rate) as avg_conversion_rate
FROM funnel_stages
GROUP BY stage_name, stage_order
ORDER BY stage_order;
```

### Revenue Trend

```sql
SELECT
  date,
  total_revenue,
  total_conversions,
  ROUND(total_revenue / NULLIF(total_conversions, 0), 2) as avg_order_value
FROM daily_metrics
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY date;
```

## 🚀 Utilisation

### Accès à Grafana

```
URL: http://localhost:3000
Username: admin
Password: admin123
```

### Navigation Rapide

1. **Home** → Dashboards
2. **Browse** → E-commerce Dashboards folder
3. **E-commerce KPIs** → Vue d'ensemble
4. **A/B Testing Analysis** → Résultats des tests

### Créer un Panel

1. Click **+ Create** → **Dashboard**
2. **Add Panel**
3. Select **PostgreSQL-Ecommerce** datasource
4. Write SQL query
5. Configure visualization
6. **Save**

## 📈 Architecture de Monitoring

```
┌─────────────────────┐
│  Users / Browsers   │
└──────────┬──────────┘
           │
    ┌──────▼───────┐
    │   Grafana    │  ← Visualisation UI
    │  Port 3000   │
    └──────┬───────┘
           │
    ┌──────▼──────────────────┐
    │   Datasources           │
    ├─────────────────────────┤
    │  PostgreSQL  │  Loki    │
    │  (Port 5432) │(Port 3100)
    └──────┬───────┴────┬─────┘
           │            │
    ┌──────▼──────┐ ┌──▼──────┐
    │ Data Import │ │ Promtail│
    │   Script    │ │  Logs   │
    └─────────────┘ └─────────┘
```

## 📁 Structure des Fichiers

```
grafana/
├── README.md                          ✅ (Nouveau)
├── provisioning/
│   ├── datasources/
│   │   └── postgres.yml               ✅ (Mis à jour - Loki ajouté)
│   └── dashboards/
│       └── dashboards.yml             ✅ (Existant)
└── dashboards/
    ├── ecommerce-kpis.json           ✅ (Existant)
    └── ab-testing-analysis.json      ✅ (Nouveau)

docker-compose.yml                     ✅ (Déjà configuré)
```

## ✅ Validation

- [x] Grafana service opérationnel (healthy)
- [x] Port 3000 accessible
- [x] PostgreSQL datasource configuré et connecté
- [x] Loki datasource configuré
- [x] Dashboard E-commerce KPIs fonctionnel
- [x] Dashboard A/B Testing Analysis créé
- [x] Provisioning automatique des dashboards
- [x] Volumes persistants créés
- [x] Health checks configurés
- [x] Loki service démarré
- [x] Promtail collecte les logs
- [x] Documentation complète créée

## 🔧 Commandes Utiles

```bash
# Démarrer le stack complet
docker-compose up -d

# Vérifier l'état de Grafana
docker logs ecommerce-grafana

# Vérifier l'état de Loki
docker logs ecommerce-loki

# Tester l'API Grafana
curl http://localhost:3000/api/health

# Lister les datasources
curl -u admin:admin123 http://localhost:3000/api/datasources

# Lister les dashboards
curl -u admin:admin123 http://localhost:3000/api/search

# Redémarrer Grafana
docker restart ecommerce-grafana

# Voir les logs en temps réel
docker logs -f ecommerce-grafana
```

## 🎯 Prochaines Étapes

Issue #44 est **complétée**. Améliorations possibles:

- Issue #45: Alerting Grafana (notifications)
- Issue #46: Dashboards additionnels (cohorts, segments)
- Issue #47: Intégration Prometheus pour métriques système
- Issue #48: Annotations automatiques des A/B tests
- Issue #49: Export automatique de rapports

## 🔐 Sécurité

**Recommandations**:

- ✅ Changer le mot de passe admin par défaut
- ⚠️ Utiliser HTTPS en production
- ⚠️ Configurer OAuth/LDAP pour authentification
- ⚠️ Limiter les accès réseau (firewall)

## 📚 Ressources

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [PostgreSQL Datasource](https://grafana.com/docs/grafana/latest/datasources/postgres/)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)

---

**Status Final**: ✅ **GRAFANA INTÉGRÉ ET OPÉRATIONNEL**

**Accès**: http://localhost:3000 (admin/admin123)  
**Dashboards**: 2 dashboards provisionés automatiquement  
**Datasources**: PostgreSQL + Loki configurés  
**Logs**: Collecte via Promtail → Loki
