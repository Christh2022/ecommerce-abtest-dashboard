# Grafana Configuration - E-commerce A/B Test Dashboard

Configuration complète de Grafana pour le monitoring et la visualisation des KPIs e-commerce.

##  Vue d'ensemble

Grafana est intégré dans le stack Docker Compose pour:

-  Visualisation en temps réel des KPIs
-  Monitoring des métriques quotidiennes
-  Analyse des tests A/B
-  Suivi des performances produits
-  Agrégation des logs avec Loki

## ️ Architecture

```
┌─────────────────┐
│  Dash Dashboard │
│   (Port 8050)   │
└────────┬────────┘
         │
┌────────▼────────┐      ┌──────────────┐
│   PostgreSQL    │◄─────┤   Grafana    │
│   (Port 5432)   │      │  (Port 3000) │
└────────┬────────┘      └──────┬───────┘
         │                      │
         │                      │
    ┌────▼────┐            ┌────▼────┐
    │  Data   │            │  Loki   │
    │ Import  │            │(Port 3100)
    └─────────┘            └────┬────┘
                                │
                           ┌────▼────┐
                           │ Promtail│
                           └─────────┘
```

##  Services Docker

### Grafana

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
    - GF_SERVER_ROOT_URL=http://localhost:3000
  volumes:
    - grafana-data:/var/lib/grafana
    - ./grafana/provisioning:/etc/grafana/provisioning
    - ./grafana/dashboards:/var/lib/grafana/dashboards
  depends_on:
    - postgres
    - loki
  networks:
    - dashboard-network
  restart: unless-stopped
```

### Loki (Log Aggregation)

```yaml
loki:
  image: grafana/loki:latest
  container_name: ecommerce-loki
  ports:
    - "3100:3100"
  volumes:
    - loki-data:/loki
  networks:
    - dashboard-network
  restart: unless-stopped
```

### Promtail (Log Collection)

```yaml
promtail:
  image: grafana/promtail:latest
  container_name: ecommerce-promtail
  volumes:
    - dash-logs:/var/log/dashboard:ro
  depends_on:
    - loki
  networks:
    - dashboard-network
  restart: unless-stopped
```

##  Configuration

### Datasources

**PostgreSQL Datasource** (`grafana/provisioning/datasources/postgres.yml`):

```yaml
apiVersion: 1

datasources:
  - name: PostgreSQL-Ecommerce
    type: postgres
    access: proxy
    url: postgres:5432
    database: ecommerce_db
    user: dashuser
    secureJsonData:
      password: "dashpass"
    jsonData:
      sslmode: "disable"
      maxOpenConns: 10
      maxIdleConns: 10
      connMaxLifetime: 14400
      postgresVersion: 1600
    editable: true
    isDefault: true
```

**Loki Datasource** (à ajouter):

```yaml
- name: Loki
  type: loki
  access: proxy
  url: http://loki:3100
  jsonData:
    maxLines: 1000
  editable: true
```

### Dashboard Provisioning

**Configuration** (`grafana/provisioning/dashboards/dashboards.yml`):

```yaml
apiVersion: 1

providers:
  - name: "E-commerce Dashboards"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

##  Dashboards Disponibles

### 1. E-commerce KPIs (`ecommerce-kpis.json`)

**Panels inclus:**

-  Total Users
-  Total Revenue
-  Conversion Rate
-  Daily Metrics Timeline
-  Top Products
-  A/B Test Results

**Requêtes SQL:**

```sql
-- Total Users
SELECT SUM(total_users) as "Total Users"
FROM daily_metrics;

-- Total Revenue
SELECT SUM(total_revenue) as "Total Revenue"
FROM daily_metrics;

-- Conversion Rate (Average)
SELECT AVG(conversion_rate) as "Avg Conversion Rate"
FROM daily_metrics;

-- Daily Timeline
SELECT
  date as time,
  total_users,
  total_revenue,
  conversion_rate
FROM daily_metrics
ORDER BY date;

-- Top Products
SELECT
  product_name,
  total_revenue,
  total_purchases
FROM products_summary
ORDER BY total_revenue DESC
LIMIT 10;
```

##  Utilisation

### Démarrage

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier que Grafana est démarré
docker logs ecommerce-grafana

# Vérifier l'état de santé
docker ps
```

### Accès

**Grafana Web UI:**

- URL: http://localhost:3000
- Username: `admin`
- Password: `admin123`

**Loki (API):**

- URL: http://localhost:3100

### Navigation

1. **Connexion** → http://localhost:3000
2. **Dashboards** → Browse → E-commerce Dashboards
3. **Explore** → PostgreSQL-Ecommerce datasource
4. **Configuration** → Data Sources

##  Créer des Dashboards Personnalisés

### Via l'interface Web

1. Click **+** → **Create Dashboard**
2. **Add Panel**
3. Sélectionner datasource: **PostgreSQL-Ecommerce**
4. Écrire la requête SQL
5. Configurer la visualisation
6. **Save Dashboard**

### Exemple de Panel: Revenue par Jour

```sql
SELECT
  date as time,
  total_revenue as "Revenue €",
  total_conversions as "Conversions"
FROM daily_metrics
WHERE date >= NOW() - INTERVAL '30 days'
ORDER BY date;
```

**Visualization:** Time series graph

### Exemple de Panel: A/B Test Comparison

```sql
SELECT
  scenario_name,
  AVG(CASE WHEN variant = 'A' THEN conversion_rate END) as "Control (A)",
  AVG(CASE WHEN variant = 'B' THEN conversion_rate END) as "Variant (B)"
FROM ab_test_results r
JOIN ab_test_scenarios s ON r.scenario_id = s.scenario_id
GROUP BY scenario_name;
```

**Visualization:** Bar chart

##  Requêtes Utiles

### KPIs Quotidiens

```sql
-- Métriques du jour
SELECT
  date,
  total_users,
  total_revenue,
  conversion_rate,
  avg_order_value
FROM v_daily_kpis
WHERE date = CURRENT_DATE;
```

### Performance Produits

```sql
-- Top 20 produits par revenue
SELECT
  product_name,
  category,
  total_revenue,
  total_purchases,
  conversion_rate
FROM v_top_products
LIMIT 20;
```

### Analyse Funnel

```sql
-- Funnel de conversion
SELECT
  stage_name,
  AVG(visitors) as avg_visitors,
  AVG(conversion_rate) as avg_conversion_rate
FROM funnel_stages
GROUP BY stage_name, stage_order
ORDER BY stage_order;
```

### A/B Test Summary

```sql
-- Résumé des tests A/B actifs
SELECT * FROM v_ab_test_summary
WHERE status = 'active';
```

##  Variables de Dashboard

Ajouter des variables pour des dashboards dynamiques:

### Date Range Variable

- **Name:** `date_from`
- **Type:** Text box
- **Default:** `NOW() - INTERVAL '30 days'`

### Scenario Variable

- **Name:** `scenario`
- **Type:** Query
- **Query:** `SELECT DISTINCT scenario_id FROM ab_test_scenarios`

##  Sécurité

### Changement du mot de passe admin

```bash
# Méthode 1: Via l'interface web après première connexion
# Settings → Profile → Change Password

# Méthode 2: Via environment variable
# Dans docker-compose.yml:
GF_SECURITY_ADMIN_PASSWORD=VotreNouveauMotDePasse
```

### Ajout d'utilisateurs

1. **Configuration** → **Users**
2. **Invite** → Ajouter email
3. Définir rôle: Viewer, Editor, ou Admin

##  Plugins Installés

```yaml
GF_INSTALL_PLUGINS: grafana-clock-panel,grafana-simple-json-datasource
```

### Plugins additionnels recommandés

```bash
# Installer manuellement dans le container
docker exec ecommerce-grafana grafana-cli plugins install grafana-piechart-panel
docker exec ecommerce-grafana grafana-cli plugins install grafana-worldmap-panel
docker restart ecommerce-grafana
```

##  Backup & Restore

### Backup des dashboards

```bash
# Export des dashboards via API
curl -u admin:admin123 \
  http://localhost:3000/api/search \
  | jq '.[] | select(.type == "dash-db") | .uid' \
  | xargs -I {} curl -u admin:admin123 \
    http://localhost:3000/api/dashboards/uid/{} \
    > backup_{}.json
```

### Backup de la base de données Grafana

```bash
docker exec ecommerce-grafana \
  sqlite3 /var/lib/grafana/grafana.db \
  .dump > grafana_backup.sql
```

##  Dépannage

### Grafana ne démarre pas

```bash
# Vérifier les logs
docker logs ecommerce-grafana

# Vérifier les permissions
docker exec ecommerce-grafana ls -la /var/lib/grafana

# Recréer le volume
docker-compose down -v
docker-compose up -d
```

### Datasource PostgreSQL non accessible

```bash
# Tester la connexion depuis Grafana
docker exec ecommerce-grafana \
  psql -h postgres -U dashuser -d ecommerce_db -c "SELECT 1;"

# Vérifier le réseau
docker network inspect ecommerce-network
```

### Dashboards non chargés

```bash
# Vérifier le provisioning
docker exec ecommerce-grafana \
  ls -la /etc/grafana/provisioning/dashboards/

# Vérifier les dashboards
docker exec ecommerce-grafana \
  ls -la /var/lib/grafana/dashboards/
```

##  Ressources

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [PostgreSQL Data Source](https://grafana.com/docs/grafana/latest/datasources/postgres/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)

##  Checklist d'Intégration

- [x] Grafana service dans docker-compose.yml
- [x] PostgreSQL datasource configuré
- [x] Loki service pour les logs
- [x] Promtail pour la collection de logs
- [x] Dashboard KPIs e-commerce
- [x] Volumes persistants pour les données
- [x] Health checks configurés
- [x] Documentation complète

---

**Status:**  Grafana intégré et opérationnel
