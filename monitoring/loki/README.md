# Loki Configuration

Ce dossier contient la configuration pour **Loki**, le système d'agrégation de logs de Grafana.

---

##  Vue d'ensemble

Loki est un système de stockage et d'interrogation de logs hautement scalable, conçu pour être :

- **Léger** : Index uniquement les métadonnées, pas le contenu des logs
- **Performant** : Compression efficace et recherche rapide
- **Compatible** : Intégration native avec Grafana

---

##  Fichiers

### loki-config.yml

Configuration principale de Loki pour le projet e-commerce dashboard.

**Ports:**

- `3100` : API HTTP (queries, ingestion)
- `9096` : API gRPC

**Stockage:**

- Type : Filesystem (local)
- Chunks : `/loki/chunks`
- Index : `/loki/tsdb-index`
- Cache : `/loki/tsdb-cache`

**Rétention:**

- Activée : Oui
- Compaction : Toutes les 10 minutes
- Delete delay : 2h après marquage

---

##  Paramètres Clés

### Schema

```yaml
schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb # Time-series database
      object_store: filesystem
      schema: v13 # Version optimisée
      index:
        period: 24h # Rotation quotidienne
```

**Pourquoi TSDB?**

- Meilleure compression
- Queries plus rapides
- Index plus petits

### Storage

```yaml
storage_config:
  tsdb_shipper:
    active_index_directory: /loki/tsdb-index
    cache_location: /loki/tsdb-cache
    cache_ttl: 24h
  filesystem:
    directory: /loki/chunks
```

**Organisation:**

```
/loki/
├── chunks/          # Logs compressés
├── tsdb-index/      # Index actifs
├── tsdb-cache/      # Cache des queries
└── compactor/       # Travail de compaction
```

### Compactor

```yaml
compactor:
  working_directory: /loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
```

**Rôle:**

- Fusionne les petits chunks en gros chunks
- Supprime les logs expirés (selon rétention)
- Optimise l'espace disque

---

##  Utilisation

### Démarrer Loki

```bash
# Via Docker Compose
docker-compose up -d loki

# Vérifier statut
docker logs ecommerce-loki

# Test ready
curl http://localhost:3100/ready
```

### API Endpoints

**Health & Status:**

```bash
# Ready check
curl http://localhost:3100/ready

# Metrics
curl http://localhost:3100/metrics

# Build info
curl http://localhost:3100/loki/api/v1/status/buildinfo
```

**Labels:**

```bash
# Lister tous les labels
curl http://localhost:3100/loki/api/v1/labels

# Valeurs d'un label
curl http://localhost:3100/loki/api/v1/label/container/values
```

**Query Logs:**

```bash
# Query range (dernières 1h)
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={container="ecommerce-dashboard"}' \
  --data-urlencode 'limit=100'

# Query instant
curl -G -s "http://localhost:3100/loki/api/v1/query" \
  --data-urlencode 'query={container="ecommerce-dashboard"}' \
  --data-urlencode 'limit=10'
```

**Tail (streaming):**

```bash
# Tail logs en temps réel
curl -G -s "http://localhost:3100/loki/api/v1/tail" \
  --data-urlencode 'query={container="ecommerce-dashboard"}' \
  --data-urlencode 'follow=true'
```

---

##  Métriques Importantes

### Ingestion

```promql
# Taux d'ingestion (bytes/sec)
rate(loki_distributor_bytes_received_total[5m])

# Nombre de lignes ingérées
rate(loki_distributor_lines_received_total[5m])

# Nombre de streams actifs
loki_ingester_streams
```

### Performance

```promql
# Latence des queries (p99)
histogram_quantile(0.99, rate(loki_query_duration_seconds_bucket[5m]))

# Chunks en mémoire
loki_ingester_memory_chunks

# Taille du cache
loki_chunk_store_index_lookups_per_query
```

### Storage

```promql
# Chunks stockés
loki_ingester_chunks_stored_total

# Espace disque utilisé (approximatif)
sum(loki_chunk_store_index_entries_per_chunk)
```

---

## ️ Personnalisation

### Modifier la Rétention

**Dans loki-config.yml, ajouter:**

```yaml
limits_config:
  retention_period: 168h  # 7 jours (défaut)
  # ou
  retention_period: 720h  # 30 jours
```

**Redémarrer:**

```bash
docker-compose restart loki
```

### Limiter le Taux d'Ingestion

**Pour éviter surcharge:**

```yaml
limits_config:
  ingestion_rate_mb: 10 # 10 MB/sec max par tenant
  ingestion_burst_size_mb: 20 # Burst de 20 MB
  max_streams_per_user: 10000 # Max 10K streams
```

### Activer Compression Avancée

```yaml
chunk_encoding: snappy # ou gzip, lz4, zstd
```

**Comparaison:**

- `gzip` : Meilleure compression, plus lent
- `snappy` : Équilibré (recommandé)
- `lz4` : Rapide, compression moyenne
- `zstd` : Bon compromis vitesse/compression

---

##  Debugging

### Vérifier Configuration

```bash
# Afficher config chargée
docker exec ecommerce-loki cat /etc/loki/local-config.yaml

# Logs Loki (erreurs config)
docker logs ecommerce-loki | grep -i error
```

### Problèmes Courants

**1. "No data sources found"**

- Vérifier que Promtail est démarré
- Vérifier connexion Promtail → Loki sur port 3100

**2. "Too many outstanding requests"**

- Augmenter `max_outstanding_requests_per_tenant`
- Augmenter ressources CPU/RAM

**3. "Context deadline exceeded"**

- Query trop lourde, réduire time range
- Augmenter timeout dans config

**4. Espace disque plein**

- Vérifier rétention activée
- Réduire `retention_period`
- Nettoyer manuellement `/loki/chunks`

### Mode Debug

**Activer logs verbeux:**

```yaml
server:
  log_level: debug # au lieu de info
```

---

##  Ressources

### Documentation Officielle

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Configuration Reference](https://grafana.com/docs/loki/latest/configure/)
- [LogQL Query Language](https://grafana.com/docs/loki/latest/query/)
- [API Reference](https://grafana.com/docs/loki/latest/reference/api/)

### Guides

- [Best Practices](https://grafana.com/docs/loki/latest/best-practices/)
- [Performance Tuning](https://grafana.com/docs/loki/latest/operations/storage/retention/)
- [Troubleshooting](https://grafana.com/docs/loki/latest/operations/troubleshooting/)

### Outils

- [LogCLI](https://grafana.com/docs/loki/latest/tools/logcli/) - CLI pour requêter Loki
- [Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/) - Agent de collecte
- [Grafana Explore](https://grafana.com/docs/grafana/latest/explore/) - Interface de query

---

##  Fichiers Liés

- [../promtail/promtail-config.yml](../promtail/promtail-config.yml) - Config agent de collecte
- [../docker-compose.yml](../docker-compose.yml) - Service Docker
- [../grafana/README.md](../grafana/README.md) - Integration Grafana
- [../docs/ISSUE53_COMPLETED.md](../docs/ISSUE53_COMPLETED.md) - Documentation complète

---

**Dernière mise à jour:** 2025-12-12  
**Version Loki:** latest (via Docker image)  
**Schema Version:** v13 (TSDB)
