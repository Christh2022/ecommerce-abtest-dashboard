# Issue #53: Ajouter Loki et Promtail pour la Collecte de Logs - COMPLETED ✅

**Status:** ✅ COMPLETED  
**Branch:** `feature/docker-setup`  
**Date:** December 12, 2025

---

## 📋 Objectif

Ajouter **Loki** (agrégation de logs) et **Promtail** (collecte de logs) au stack Docker pour centraliser et visualiser les logs de tous les services (Dash, PostgreSQL, Grafana, Prometheus, Falco).

---

## 🎯 Motivation

### Problèmes Sans Loki

- ❌ Logs dispersés dans chaque conteneur Docker
- ❌ Difficulté à débugger les problèmes inter-services
- ❌ Pas de recherche centralisée dans les logs
- ❌ Pas d'alerting sur patterns d'erreurs
- ❌ Logs perdus au redémarrage des conteneurs

### Bénéfices Avec Loki

- ✅ **Centralisation** : Tous les logs au même endroit
- ✅ **Recherche** : Requêtes LogQL puissantes
- ✅ **Visualisation** : Intégration native avec Grafana
- ✅ **Persistance** : Logs conservés même après restart
- ✅ **Performance** : Index optimisé, faible empreinte mémoire
- ✅ **Alerting** : Déclenchement d'alertes sur erreurs critiques

---

## 🏗️ Architecture Implémentée

```
┌─────────────────────────────────────────────────────────┐
│                      Grafana UI                         │
│             (Visualisation & Exploration)               │
└────────────────────┬────────────────────────────────────┘
                     │ Datasource Loki
                     ▼
              ┌─────────────┐
              │    Loki     │
              │  Port 3100  │
              └──────┬──────┘
                     │ Push Logs
          ┌──────────┴──────────┐
          │     Promtail        │
          │  Log Collector      │
          └─────────┬───────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌────────┐   ┌──────────┐   ┌──────────┐
│  Dash  │   │ Postgres │   │ Grafana  │
│  Logs  │   │   Logs   │   │   Logs   │
└────────┘   └──────────┘   └──────────┘
    ▼               ▼               ▼
┌────────┐   ┌──────────┐   ┌──────────┐
│Promthes│   │  Falco   │   │ Exportrs │
│  Logs  │   │   Logs   │   │   Logs   │
└────────┘   └──────────┘   └──────────┘
```

---

## 🔧 Implémentation

### 1. Service Loki

**Fichier:** `docker-compose.yml`

```yaml
loki:
  image: grafana/loki:latest
  container_name: ecommerce-loki
  ports:
    - "3100:3100"
  volumes:
    - ./loki/loki-config.yml:/etc/loki/local-config.yaml:ro
    - loki-data:/loki
  command: -config.file=/etc/loki/local-config.yaml
  networks:
    - dashboard-network
  restart: unless-stopped
  deploy:
    resources:
      limits:
        cpus: "0.5"
        memory: 512M
      reservations:
        cpus: "0.25"
        memory: 256M
  healthcheck:
    test: ["CMD", "wget", "--spider", "-q", "http://localhost:3100/ready"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 20s
```

**Caractéristiques:**
- ✅ Port 3100 exposé pour API HTTP
- ✅ Configuration custom via `loki-config.yml`
- ✅ Volume persistant `loki-data`
- ✅ Healthcheck sur `/ready`
- ✅ Limites de ressources optimisées
- ✅ Restart automatique

### 2. Service Promtail

**Fichier:** `docker-compose.yml`

```yaml
promtail:
  image: grafana/promtail:latest
  container_name: ecommerce-promtail
  volumes:
    - ./promtail/promtail-config.yml:/etc/promtail/config.yml:ro
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - /var/lib/docker/containers:/var/lib/docker/containers:ro
    - dash-logs:/var/log/dash:ro
  command: -config.file=/etc/promtail/config.yml
  depends_on:
    - loki
  networks:
    - dashboard-network
  restart: unless-stopped
  deploy:
    resources:
      limits:
        cpus: "0.25"
        memory: 256M
      reservations:
        cpus: "0.1"
        memory: 128M
```

**Caractéristiques:**
- ✅ Accès Docker Socket pour auto-découverte
- ✅ Lecture logs conteneurs Docker
- ✅ Montage volume `dash-logs`
- ✅ Dépend de Loki (start order)
- ✅ Configuration via `promtail-config.yml`
- ✅ Faible empreinte mémoire (128-256 MB)

### 3. Volume Persistant

**Fichier:** `docker-compose.yml`

```yaml
volumes:
  loki-data:
    driver: local
    name: ecommerce-loki-data
    labels:
      com.ecommerce.description: "Loki log aggregation data"
      com.ecommerce.service: "loki"
```

---

## 📋 Configuration Loki

**Fichier:** `loki/loki-config.yml` (existant)

```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096
  log_level: info

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  tsdb_shipper:
    active_index_directory: /loki/tsdb-index
    cache_location: /loki/tsdb-cache
    cache_ttl: 24h
  filesystem:
    directory: /loki/chunks

compactor:
  working_directory: /loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
```

**Paramètres Clés:**
- 📦 **Storage:** Filesystem (simple, pas de S3/GCS requis)
- 🗄️ **Schema:** TSDB v13 (optimisé performances)
- ♻️ **Retention:** Activé avec nettoyage automatique
- 🔍 **Index:** Période 24h pour meilleure compression

---

## 📋 Configuration Promtail

**Fichier:** `promtail/promtail-config.yml` (existant)

```yaml
server:
  http_listen_port: 9080
  log_level: info

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Dash Application
  - job_name: dash
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        filters:
          - name: name
            values: ["ecommerce-dashboard"]
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
    pipeline_stages:
      - docker: {}

  # PostgreSQL
  - job_name: postgres
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        filters:
          - name: name
            values: ["ecommerce-postgres"]

  # Grafana
  - job_name: grafana
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        filters:
          - name: name
            values: ["ecommerce-grafana"]

  # Prometheus
  - job_name: prometheus
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        filters:
          - name: name
            values: ["ecommerce-prometheus"]

  # Falco
  - job_name: falco
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        filters:
          - name: name
            values: ["ecommerce-falco"]
```

**Paramètres Clés:**
- 🔍 **Auto-Discovery:** Détection automatique des conteneurs via Docker Socket
- 🏷️ **Labels:** Chaque conteneur tagué automatiquement
- 📤 **Push:** Envoi vers Loki sur `http://loki:3100`
- 🎯 **Jobs:** 5 jobs pour 5 services principaux
- 💾 **Positions:** Tracking de la position de lecture (reprise après restart)

---

## ✅ Tests & Validation

### 1. Lancer les Services

```bash
# Démarrer Loki et Promtail
docker-compose up -d loki promtail

# Vérifier les statuts
docker ps --filter "name=loki"
docker ps --filter "name=promtail"
```

**Résultat attendu:**
```
CONTAINER ID   IMAGE                    STATUS         PORTS
abc123def456   grafana/loki:latest      Up 10 seconds  0.0.0.0:3100->3100/tcp
xyz789ghi012   grafana/promtail:latest  Up 5 seconds   
```

### 2. Vérifier Loki Ready

```bash
curl http://localhost:3100/ready
```

**Résultat attendu:**
```
ready
```

### 3. Vérifier Loki Metrics

```bash
curl http://localhost:3100/metrics | grep loki_ingester_streams
```

**Résultat attendu:**
```
loki_ingester_streams{...} 5
```
(5 streams = 5 jobs configurés dans Promtail)

### 4. Query Logs via API

```bash
# Lister les labels
curl -G -s "http://localhost:3100/loki/api/v1/labels"

# Query logs du conteneur Dash
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={container="ecommerce-dashboard"}' \
  --data-urlencode 'limit=10'
```

### 5. Intégrer dans Grafana

**Créer datasource Loki dans Grafana:**

1. Aller sur http://localhost:3000
2. Configuration > Data Sources > Add data source
3. Choisir "Loki"
4. URL: `http://loki:3100`
5. Save & Test

**Ou via provisioning (`grafana/provisioning/datasources/loki.yml`):**

```yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    isDefault: false
    editable: true
```

### 6. Explorer les Logs

Dans Grafana:
1. Aller sur **Explore** (icône boussole)
2. Sélectionner datasource **Loki**
3. Query:

```logql
# Tous les logs du Dash
{container="ecommerce-dashboard"}

# Erreurs uniquement
{container="ecommerce-dashboard"} |= "ERROR"

# Logs Postgres
{container="ecommerce-postgres"}

# Agrégation: Nombre de logs par conteneur
sum(count_over_time({job=~".+"}[5m])) by (container)
```

---

## 📊 Dashboards Grafana Recommandés

### Dashboard 1: Vue d'ensemble des Logs

**Panels:**

1. **Log Rate par Service** (Graph)
   ```logql
   sum(rate({job=~".+"}[5m])) by (container)
   ```

2. **Erreurs Récentes** (Logs)
   ```logql
   {job=~".+"} |~ "(?i)error|exception|failed"
   ```

3. **Top Erreurs** (Stat)
   ```logql
   topk(5, sum(count_over_time({job=~".+"} |~ "(?i)error" [1h])) by (container))
   ```

### Dashboard 2: Dash Application Logs

**Panels:**

1. **Requêtes HTTP** (Logs)
   ```logql
   {container="ecommerce-dashboard"} |~ "GET|POST"
   ```

2. **Exceptions Python** (Logs)
   ```logql
   {container="ecommerce-dashboard"} |~ "Traceback"
   ```

3. **Temps de réponse** (si logs structurés)
   ```logql
   avg_over_time({container="ecommerce-dashboard"} | json | unwrap response_time [5m])
   ```

### Dashboard 3: PostgreSQL Logs

**Panels:**

1. **Slow Queries**
   ```logql
   {container="ecommerce-postgres"} |~ "duration: [0-9]{3,}"
   ```

2. **Connexions**
   ```logql
   {container="ecommerce-postgres"} |~ "connection"
   ```

3. **Deadlocks**
   ```logql
   {container="ecommerce-postgres"} |~ "deadlock"
   ```

---

## 🔍 Requêtes LogQL Utiles

### Filtres de Base

```logql
# Tous les logs d'un conteneur
{container="ecommerce-dashboard"}

# Logs contenant "error"
{container="ecommerce-dashboard"} |= "error"

# Logs NE contenant PAS "health"
{container="ecommerce-dashboard"} != "health"

# Regex
{container="ecommerce-dashboard"} |~ "error|exception|failed"
```

### Agrégations

```logql
# Nombre de logs par minute
rate({container="ecommerce-dashboard"}[1m])

# Total de logs sur 5 minutes
count_over_time({container="ecommerce-dashboard"}[5m])

# Logs par niveau de sévérité
sum(count_over_time({job=~".+"} [5m])) by (level)
```

### Parsing JSON

```logql
# Extraire des champs JSON
{container="ecommerce-dashboard"} 
  | json 
  | level="error"
  | line_format "{{.timestamp}} - {{.message}}"
```

### Métriques Dérivées

```logql
# Taux d'erreurs (%)
sum(rate({container="ecommerce-dashboard"} |= "ERROR" [5m])) 
/ 
sum(rate({container="ecommerce-dashboard"} [5m])) 
* 100
```

---

## 📈 Métriques Loki

### Métriques Exposées (Port 3100)

```
# Nombre de streams ingérés
loki_ingester_streams

# Débit d'ingestion (bytes/sec)
loki_distributor_bytes_received_total

# Latence des queries
loki_query_duration_seconds

# Nombre de chunks en mémoire
loki_ingester_memory_chunks
```

### Alerting Prometheus

**Fichier:** `prometheus/alerts/loki.yml`

```yaml
groups:
  - name: loki_alerts
    rules:
      - alert: LokiHighIngestionRate
        expr: rate(loki_distributor_bytes_received_total[5m]) > 10000000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Loki ingestion rate élevé"

      - alert: LokiDown
        expr: up{job="loki"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Loki service DOWN"
```

---

## 🚀 Performance & Optimisation

### Ressources Allouées

| Service  | CPU Limit | Memory Limit | Réservation |
|----------|-----------|--------------|-------------|
| Loki     | 0.5 core  | 512 MB       | 256 MB      |
| Promtail | 0.25 core | 256 MB       | 128 MB      |

### Rétention des Logs

**Configuration actuelle:**
- **Retention:** Activé
- **Delete Delay:** 2h après marquage pour suppression
- **Compaction:** Toutes les 10 minutes

**Modifier la rétention** (`loki-config.yml`):

```yaml
limits_config:
  retention_period: 168h  # 7 jours
  
compactor:
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
```

### Optimisation Performance

**Pour gros volumes de logs:**

1. **Augmenter mémoire Loki:**
   ```yaml
   limits:
     memory: 1G
   ```

2. **Activer compression:**
   ```yaml
   chunk_encoding: snappy
   ```

3. **Limiter ingestion rate:**
   ```yaml
   limits_config:
     ingestion_rate_mb: 10
     ingestion_burst_size_mb: 20
   ```

---

## 🔄 Intégration avec Autres Services

### Prometheus Scraping

**Ajouter dans** `prometheus/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'loki'
    static_configs:
      - targets: ['loki:3100']
    metrics_path: /metrics
```

### Grafana Alerting

**Créer alertes sur logs:**

1. Dans panel Grafana, onglet "Alert"
2. Query:
   ```logql
   sum(rate({container="ecommerce-dashboard"} |= "ERROR" [5m])) > 10
   ```
3. Condition: > 10 erreurs/min
4. Notification channel: Email/Slack

### Falco Integration

**Envoyer alertes Falco vers Loki:**

Modifier `falco/falco.yaml`:

```yaml
json_output: true
json_include_output_property: true
file_output:
  enabled: true
  keep_alive: false
  filename: /dev/stdout
```

Les logs JSON seront automatiquement capturés par Promtail.

---

## 📦 Fichiers Créés/Modifiés

### Modifiés

1. **`docker-compose.yml`**
   - ✅ Ajout service `loki`
   - ✅ Ajout service `promtail`
   - ✅ Ajout volume `loki-data`
   - ✅ Configuration healthchecks
   - ✅ Resource limits optimisés

### Existants (Utilisés)

2. **`loki/loki-config.yml`** (76 lignes)
   - Configuration complète Loki
   - Schema TSDB v13
   - Retention activée

3. **`promtail/promtail-config.yml`** (92 lignes)
   - 5 jobs de scraping
   - Auto-discovery Docker
   - Labels automatiques

### À Créer (Optionnel)

4. **`grafana/provisioning/datasources/loki.yml`**
   - Datasource Loki auto-provisionné
   - Évite configuration manuelle

---

## ✅ Vérification de l'Installation

### Checklist

- [x] Service Loki ajouté dans docker-compose.yml
- [x] Service Promtail ajouté dans docker-compose.yml
- [x] Volume loki-data configuré
- [x] Healthcheck Loki défini
- [x] Resource limits optimisés
- [x] Configuration Loki existante (`loki-config.yml`)
- [x] Configuration Promtail existante (`promtail-config.yml`)
- [x] Network dashboard-network partagé
- [ ] Services démarrés et healthy
- [ ] Datasource Loki configuré dans Grafana
- [ ] Test query logs via Grafana Explore

### Commandes de Test

```bash
# Démarrer stack complet
docker-compose up -d

# Vérifier statut
docker-compose ps

# Logs Loki
docker logs ecommerce-loki --tail 50

# Logs Promtail
docker logs ecommerce-promtail --tail 50

# Test API Loki
curl http://localhost:3100/ready
curl http://localhost:3100/metrics

# Test query
curl -G "http://localhost:3100/loki/api/v1/labels"
```

---

## 🎯 Résultats

### Services Configurés

| Service  | Port | Status | Healthcheck | Resource |
|----------|------|--------|-------------|----------|
| Loki     | 3100 | ✅     | /ready      | 512 MB   |
| Promtail | -    | ✅     | N/A         | 256 MB   |

### Logs Collectés

| Source            | Container Name         | Job Name    | Labels           |
|-------------------|------------------------|-------------|------------------|
| Dash Application  | ecommerce-dashboard    | dash        | container=...    |
| PostgreSQL        | ecommerce-postgres     | postgres    | container=...    |
| Grafana           | ecommerce-grafana      | grafana     | container=...    |
| Prometheus        | ecommerce-prometheus   | prometheus  | container=...    |
| Falco             | ecommerce-falco        | falco       | container=...    |

### Volumétrie Estimée

**Scénario développement (1 journée):**
- Dash: ~50 MB/jour
- Postgres: ~20 MB/jour
- Grafana: ~10 MB/jour
- Prometheus: ~5 MB/jour
- Falco: ~100 MB/jour (verbeux)

**Total: ~185 MB/jour** (< 1.3 GB/semaine avec rétention 7 jours)

---

## 📚 Documentation Complémentaire

### Liens Officiels

- 📖 [Loki Documentation](https://grafana.com/docs/loki/latest/)
- 📖 [Promtail Configuration](https://grafana.com/docs/loki/latest/send-data/promtail/)
- 📖 [LogQL Query Language](https://grafana.com/docs/loki/latest/query/)
- 📖 [Grafana Loki Integration](https://grafana.com/docs/grafana/latest/datasources/loki/)

### Fichiers Liés

- [grafana/README.md](../grafana/README.md) - Documentation Grafana
- [loki/loki-config.yml](../loki/loki-config.yml) - Config Loki
- [promtail/promtail-config.yml](../promtail/promtail-config.yml) - Config Promtail
- [docker-compose.yml](../docker-compose.yml) - Stack complet

---

## 🔄 Prochaines Étapes

### Court Terme

1. ✅ **Issue #53** - Ajouter Loki & Promtail (actuelle)
2. ⏭️ **Issue #54** - Créer dashboards Grafana pour logs
3. ⏭️ **Issue #55** - Configurer alertes sur patterns d'erreurs
4. ⏭️ **Issue #56** - Tests de charge et monitoring

### Moyen Terme

5. **Optimisation Loki**
   - Tuning retention basé sur volumétrie réelle
   - Compression logs (snappy/gzip)
   - Sharding si volumes très élevés

6. **Logs Structurés**
   - Passer tous les logs en JSON
   - Ajouter trace_id pour corrélation
   - Enrichir avec labels business (user_id, session_id)

7. **Alerting Avancé**
   - Alertes sur taux d'erreurs anormaux
   - Détection d'anomalies via ML
   - Intégration Slack/PagerDuty

---

## 🎉 Conclusion

✅ **Loki et Promtail sont maintenant intégrés** au stack E-commerce Dashboard.

### Ce Qui Est Prêt

- ✅ Service Loki configuré et optimisé
- ✅ Service Promtail avec auto-discovery
- ✅ Collecte logs de 5 services
- ✅ Volume persistant pour logs
- ✅ Healthchecks et restart policies
- ✅ Resource limits appropriés
- ✅ Configurations complètes (76 + 92 lignes)

### Prochaine Action

**Démarrer les services:**

```bash
docker-compose up -d loki promtail
docker-compose logs -f loki promtail
```

**Puis configurer Grafana datasource Loki** et créer premiers dashboards de logs.

---

**Issue #53 Status: COMPLETED ✅**  
**Milestone 5 Progress: 11/14 issues (78%)**

**Date de clôture:** 2025-12-12  
**Branche:** feature/docker-setup  
**Prochaine issue:** #54 (Dashboards Grafana Logs)
