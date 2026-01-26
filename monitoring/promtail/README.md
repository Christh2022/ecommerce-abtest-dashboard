# Promtail Configuration

Ce dossier contient la configuration pour **Promtail**, l'agent de collecte de logs pour Loki.

---

## 📋 Vue d'ensemble

Promtail est un agent qui :

- **Découvre** automatiquement les conteneurs Docker
- **Collecte** leurs logs (stdout/stderr)
- **Tag** avec des labels (container, stream, etc.)
- **Envoie** vers Loki pour agrégation

---

## 📁 Fichiers

### promtail-config.yml

Configuration de Promtail pour collecter les logs de 5 services du projet e-commerce dashboard.

**Port:**

- `9080` : API HTTP (metrics, health)

**Cible:**

- Loki : `http://loki:3100/loki/api/v1/push`

---

## 🎯 Services Monitorés

Promtail collecte les logs des conteneurs suivants :

| Job Name     | Container Name       | Description                 |
| ------------ | -------------------- | --------------------------- |
| `dash`       | ecommerce-dashboard  | Application Dash principale |
| `postgres`   | ecommerce-postgres   | Base de données PostgreSQL  |
| `grafana`    | ecommerce-grafana    | Interface de visualisation  |
| `prometheus` | ecommerce-prometheus | Collecte des métriques      |
| `falco`      | ecommerce-falco      | Monitoring de sécurité      |

---

## 🔧 Configuration Détaillée

### Client Loki

```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
```

**Paramètres implicites:**

- Timeout : 10s
- Batch size : 1 MB
- Batch wait : 1s

### Auto-Discovery Docker

**Pour chaque job:**

```yaml
scrape_configs:
  - job_name: dash
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
        filters:
          - name: name
            values: ["ecommerce-dashboard"]
```

**Fonctionnement:**

1. Promtail se connecte au Docker socket
2. Découvre les conteneurs matchant le filtre
3. Lit leurs logs depuis `/var/lib/docker/containers/`
4. Rafraîchit la liste toutes les 5 secondes

### Labels Automatiques

```yaml
relabel_configs:
  - source_labels: ["__meta_docker_container_name"]
    regex: "/(.*)"
    target_label: "container"
  - source_labels: ["__meta_docker_container_log_stream"]
    target_label: "stream"
```

**Labels ajoutés:**

- `container` : Nom du conteneur (ex: `ecommerce-dashboard`)
- `stream` : `stdout` ou `stderr`
- `job` : Nom du job Promtail (ex: `dash`)

**Labels Loki résultants:**

```
{container="ecommerce-dashboard", stream="stdout", job="dash"}
```

### Pipeline Stages

```yaml
pipeline_stages:
  - docker: {}
```

**Rôle du stage `docker`:**

- Parse les logs formatés par Docker
- Extrait timestamp, stream (stdout/stderr)
- Supprime le wrapper JSON Docker

---

## 🚀 Utilisation

### Démarrer Promtail

```bash
# Via Docker Compose
docker-compose up -d promtail

# Vérifier statut
docker logs ecommerce-promtail

# Test health
curl http://localhost:9080/ready
```

### Vérifier Positions

```bash
# Afficher le fichier positions
docker exec ecommerce-promtail cat /tmp/positions.yaml
```

**Contenu exemple:**

```yaml
positions:
  /var/lib/docker/containers/abc123.../abc123...-json.log: 12345
  /var/lib/docker/containers/def456.../def456...-json.log: 67890
```

**Signification:**

- Promtail track la position de lecture dans chaque fichier
- En cas de restart, reprend où il s'était arrêté
- Pas de perte ni duplication de logs

---

## 📊 Métriques

### API Metrics

```bash
# Toutes les métriques Prometheus
curl http://localhost:9080/metrics
```

### Métriques Importantes

```promql
# Taux d'envoi vers Loki (lignes/sec)
rate(promtail_sent_entries_total[5m])

# Taux d'erreurs
rate(promtail_dropped_entries_total[5m])

# Bytes envoyés
rate(promtail_sent_bytes_total[5m])

# Durée du dernier envoi
promtail_request_duration_seconds
```

### Monitoring dans Grafana

**Panel 1: Lignes Collectées par Service**

```promql
sum(rate(promtail_read_lines_total[5m])) by (path)
```

**Panel 2: Erreurs de Collecte**

```promql
sum(rate(promtail_dropped_entries_total[5m])) by (reason)
```

**Panel 3: Latence vers Loki**

```promql
histogram_quantile(0.99, rate(promtail_request_duration_seconds_bucket[5m]))
```

---

## ⚙️ Personnalisation

### Ajouter un Nouveau Service

**Exemple: Ajouter Redis**

```yaml
scrape_configs:
  # ... jobs existants ...

  - job_name: redis
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
        filters:
          - name: name
            values: ["ecommerce-redis"]
    relabel_configs:
      - source_labels: ["__meta_docker_container_name"]
        regex: "/(.*)"
        target_label: "container"
      - source_labels: ["__meta_docker_container_log_stream"]
        target_label: "stream"
    pipeline_stages:
      - docker: {}
```

**Puis redémarrer:**

```bash
docker-compose restart promtail
```

### Filtrer les Logs

**Exclure les healthchecks:**

```yaml
pipeline_stages:
  - docker: {}
  - match:
      selector: '{job="dash"}'
      stages:
        - drop:
            expression: ".*GET /health.*"
```

### Parser les Logs JSON

**Si logs en JSON:**

```yaml
pipeline_stages:
  - docker: {}
  - json:
      expressions:
        level: level
        timestamp: timestamp
        message: message
  - labels:
      level:
```

**Résultat:**

- Label `level` ajouté (info, warning, error)
- Filtrage possible : `{container="...", level="error"}`

### Enrichir avec Metadata

**Ajouter labels custom:**

```yaml
relabel_configs:
  - source_labels: ["__meta_docker_container_name"]
    regex: "/(.*)"
    target_label: "container"
  - target_label: "environment"
    replacement: "production"
  - target_label: "project"
    replacement: "ecommerce-dashboard"
```

---

## 🔍 Debugging

### Vérifier Configuration

```bash
# Afficher config chargée
docker exec ecommerce-promtail cat /etc/promtail/config.yml

# Logs Promtail (erreurs)
docker logs ecommerce-promtail | grep -i error
```

### Problèmes Courants

**1. "Permission denied" sur Docker socket**

**Solution:**

```yaml
# Dans docker-compose.yml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro # Ajouter :ro
```

**2. "Failed to push to Loki"**

**Causes:**

- Loki pas démarré : `docker ps | grep loki`
- URL incorrecte : Vérifier `clients[0].url`
- Network : Vérifier que Promtail et Loki sur même network

**Solution:**

```bash
# Vérifier connectivité
docker exec ecommerce-promtail wget -O- http://loki:3100/ready
```

**3. "No targets discovered"**

**Causes:**

- Filtre container name incorrect
- Conteneur pas démarré
- Docker socket non monté

**Solution:**

```bash
# Lister conteneurs visibles
docker exec ecommerce-promtail ls -la /var/run/docker.sock

# Vérifier filtre
docker ps --filter "name=ecommerce-"
```

**4. Logs dupliqués**

**Cause:** Fichier positions corrompu

**Solution:**

```bash
# Supprimer positions et restart
docker exec ecommerce-promtail rm /tmp/positions.yaml
docker-compose restart promtail
```

### Mode Debug

**Activer logs verbeux:**

```yaml
server:
  log_level: debug # au lieu de info
```

**Puis:**

```bash
docker-compose restart promtail
docker logs -f ecommerce-promtail
```

---

## 📈 Performance & Optimisation

### Tuning Batching

**Pour réduire requêtes HTTP:**

```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
    batchwait: 5s # Attendre 5s avant envoi (défaut: 1s)
    batchsize: 2097152 # 2 MB par batch (défaut: 1 MB)
```

**Impact:**

- Moins de requêtes HTTP
- Latence plus élevée (logs arrivent avec 5s de retard)
- Meilleure compression

### Limiter la Mémoire

**Dans docker-compose.yml:**

```yaml
promtail:
  deploy:
    resources:
      limits:
        memory: 256M # Limite stricte
```

**Si OOM (Out Of Memory):**

- Réduire `batchsize`
- Réduire nombre de positions trackées
- Augmenter mémoire allouée

### Filtrer en Amont

**Éviter d'envoyer logs verbeux:**

```yaml
pipeline_stages:
  - docker: {}
  - match:
      selector: '{job="postgres"}'
      stages:
        - drop:
            expression: ".*STATEMENT:.*" # Drop statements SQL
```

---

## 🧪 Tests

### Test Local (Sans Docker)

**Installer Promtail:**

```bash
# Linux
wget https://github.com/grafana/loki/releases/download/v2.9.0/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
chmod +x promtail-linux-amd64

# Lancer
./promtail-linux-amd64 -config.file=promtail-config.yml
```

### Test Envoi Manuel

**Simuler envoi vers Loki:**

```bash
curl -X POST http://localhost:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [
      {
        "stream": {
          "job": "test",
          "container": "manual"
        },
        "values": [
          ["'$(date +%s%N)'", "Test log from curl"]
        ]
      }
    ]
  }'
```

### Vérifier Réception Loki

```bash
# Query logs de test
curl -G "http://localhost:3100/loki/api/v1/query" \
  --data-urlencode 'query={job="test"}' \
  --data-urlencode 'limit=10'
```

---

## 📚 Ressources

### Documentation Officielle

- [Promtail Documentation](https://grafana.com/docs/loki/latest/send-data/promtail/)
- [Configuration Reference](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/)
- [Pipeline Stages](https://grafana.com/docs/loki/latest/send-data/promtail/stages/)
- [Scraping](https://grafana.com/docs/loki/latest/send-data/promtail/scraping/)

### Guides

- [Docker Integration](https://grafana.com/docs/loki/latest/send-data/promtail/cloud/docker/)
- [Service Discovery](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#docker_sd_config)
- [Best Practices](https://grafana.com/docs/loki/latest/best-practices/)

### Exemples

- [Official Examples](https://github.com/grafana/loki/tree/main/clients/cmd/promtail)
- [Community Configs](https://github.com/grafana/loki/discussions)

---

## 🔗 Fichiers Liés

- [../loki/loki-config.yml](../loki/loki-config.yml) - Config serveur Loki
- [../docker-compose.yml](../docker-compose.yml) - Service Docker
- [../grafana/README.md](../grafana/README.md) - Integration Grafana
- [../docs/ISSUE53_COMPLETED.md](../docs/ISSUE53_COMPLETED.md) - Documentation complète

---

**Dernière mise à jour:** 2025-12-12  
**Version Promtail:** latest (via Docker image)  
**Jobs Configurés:** 5 (dash, postgres, grafana, prometheus, falco)
