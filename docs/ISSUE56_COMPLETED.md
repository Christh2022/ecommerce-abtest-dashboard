# Issue #56: Configuration des Alertes de Sécurité - COMPLETED ✅

**Status:** Resolved  
**Branch:** `feature/security-intrusion`  
**Completed:** December 13, 2025

---

## 🎯 Objectif

Configurer des alertes de sécurité dans Grafana pour détecter :
- Connexions réseau suspectes
- Shells ouverts dans les conteneurs
- Modifications de fichiers critiques
- Erreurs applicatives élevées
- Problèmes de base de données

---

## 📋 Solution Implémentée

### Fichiers de Configuration Créés

#### 1. grafana/provisioning/alerting/alerts.yml
Définit 6 règles d'alerte avec requêtes LogQL :

**Alertes de Sécurité (Critical/High):**
- `suspicious_connections` - Connexions suspectes détectées par Falco
- `shell_in_container` - Shell spawné dans un conteneur
- `file_modifications` - Modifications de fichiers critiques

**Alertes Application/Infrastructure (Warning/High):**
- `high_error_rate` - Taux d'erreur élevé dans Dash
- `database_failures` - Échecs de connexion PostgreSQL  
- `container_restart_loop` - Conteneur en boucle de redémarrage

#### 2. grafana/provisioning/alerting/notification-policies.yml
Configure les politiques de notification :
- **Contact Point "security-team"** : Email + Slack pour alertes critiques
- **Contact Point "default"** : Email pour alertes générales
- **Routage** : Alertes de sécurité → security-team (1min), Autres → default (5min)

#### 3. grafana/README_ALERTING.md
Documentation complète sur :
- Configuration des alertes
- Exemples de requêtes LogQL
- Tests et déclenchement manuel
- Troubleshooting

---

## 🚀 Configuration Manuelle des Alertes

Les alertes Grafana nécessitent une configuration via l'interface UI. Voici comment les créer :

### Étape 1: Créer un Dossier d'Alertes

1. Accéder à **Grafana** : http://localhost:3000
2. Aller dans **Alerting** → **Alert rules**
3. Cliquer sur **New folder** → Nommer "Security Alerts"

### Étape 2: Créer les Alertes

Pour chaque alerte ci-dessous, cliquer sur **New alert rule** :

#### Alert 1: Shell dans Conteneur 🟠

```
Name: Shell Spawned in Container
Folder: Security Alerts
Query A (Loki):
  sum(count_over_time({container="ecommerce-falco"} |~ "(?i)(shell|bash|sh).*(spawn|exec)" [5m])) > 0
  
Evaluate every: 1m
For: 1m
Labels:
  - severity: high
  - category: security
Annotations:
  - summary: Shell activity detected in container
  - description: A shell was spawned inside a container
```

#### Alert 2: Connexions Suspectes 🔴

```
Name: Suspicious Network Connections
Folder: Security Alerts
Query A (Loki):
  sum(count_over_time({container="ecommerce-falco"} |~ "(?i)(connection|network).*(suspicious|unauthorized|blocked)" [5m])) > 0
  
Evaluate every: 1m
For: 2m
Labels:
  - severity: critical
  - category: security
```

#### Alert 3: Modifications Fichiers Critiques 🟠

```
Name: Critical File Modifications
Folder: Security Alerts
Query A (Loki):
  sum(count_over_time({container="ecommerce-falco"} |~ "(?i)(write|modify|delete).*(config|passwd|shadow)" [5m])) > 0
  
Evaluate every: 1m
For: 1m
Labels:
  - severity: high
  - category: security
```

#### Alert 4: Taux d'Erreur Élevé 🟡

```
Name: High Error Rate in Dash App
Folder: Application Monitoring
Query A (Loki):
  sum(rate({container="ecommerce-dashboard"} |~ "(?i)error" [5m])) > 10
  
Evaluate every: 1m
For: 3m
Labels:
  - severity: warning
  - category: application
```

#### Alert 5: Échecs Connexion DB 🟡

```
Name: Database Connection Failures  
Folder: Application Monitoring
Query A (Loki):
  sum(count_over_time({container="ecommerce-postgres"} |~ "(?i)(fatal|error).*(connection|authentication)" [5m])) > 5
  
Evaluate every: 1m
For: 2m
Labels:
  - severity: warning
  - category: database
```

#### Alert 6: Boucle Redémarrage 🟠

```
Name: Container Restart Loop
Folder: Infrastructure
Query A (Loki):
  sum(count_over_time({container=~"ecommerce-.*"} |~ "(?i)(restarting|restart)" [10m])) > 10
  
Evaluate every: 1m
For: 5m
Labels:
  - severity: high
  - category: infrastructure
```

---

## 🔔 Configuration des Notifications

### Contact Points

1. **Aller dans** : Alerting → Contact points
2. **Créer "security-team"** :
   - Type: Email
   - Addresses: `security@example.com`
3. **Créer "default-contact-point"** :
   - Type: Email
   - Addresses: `admin@example.com`

### Notification Policies

1. **Aller dans** : Alerting → Notification policies
2. **Ajouter une policy** :
   - Matcher: `category = security`
   - Contact point: `security-team`
   - Group interval: 1m
   - Repeat interval: 30m

---

## ✅ Tests des Alertes

### Test 1: Shell in Container

```bash
docker exec ecommerce-dashboard /bin/bash -c "echo test"
```

**Résultat attendu** : Alerte "Shell Spawned in Container" se déclenche en ~2 minutes

### Test 2: High Error Rate

```bash
for i in {1..20}; do 
  curl http://localhost:8050/nonexistent 2>/dev/null
done
```

**Résultat attendu** : Alerte "High Error Rate" se déclenche en ~3 minutes

### Test 3: Database Connection Failure

```bash
for i in {1..10}; do
  docker exec ecommerce-postgres psql -U wronguser -d postgres 2>&1
done
```

**Résultat attendu** : Alerte "Database Connection Failures" se déclenche en ~2 minutes

---

## 📊 Monitoring des Alertes

### Dashboard Alerting

Accéder à : http://localhost:3000/alerting/list

**Statuts possibles** :
- 🟢 **Normal** : Aucun problème détecté
- 🔴 **Firing** : Alerte active, action requise
- 🟡 **Pending** : En cours d'évaluation
- ⚪ **No Data** : Pas assez de données

### Historique

Accéder à : http://localhost:3000/alerting/notifications

Voir :
- Toutes les alertes déclenchées
- Notifications envoyées
- États des contact points

---

## 🎯 Requêtes LogQL Utiles

### Détecter Tentatives Login Échouées

```logql
sum(count_over_time({container="ecommerce-dashboard"} |~ "(?i)(failed|unauthorized).*login" [5m])) > 3
```

### Monitorer Utilisation Mémoire

```logql
sum(count_over_time({container=~"ecommerce-.*"} |~ "(?i)(out of memory|oom)" [5m])) > 0
```

### Tracker Changements Configuration

```logql
sum(count_over_time({container="ecommerce-grafana"} |~ "(?i)configuration.*changed" [5m])) > 0
```

### Détecter Accès Non Autorisés

```logql
sum(count_over_time({container=~"ecommerce-.*"} |~ "(?i)(unauthorized|forbidden|denied)" [5m])) > 5
```

---

## 🔧 Troubleshooting

### Alertes ne se déclenchent pas

**Problème** : Les requêtes ne retournent pas de données

**Solution** :
1. Vérifier que Loki reçoit des logs : http://localhost:3100/metrics
2. Tester la requête dans Explore : http://localhost:3000/explore
3. Ajuster la fenêtre de temps `[5m]` si nécessaire
4. Vérifier que les labels correspondent (`container=`)

### Notifications non reçues

**Problème** : Alertes actives mais pas de notifications

**Solution** :
1. Vérifier les contact points dans Grafana UI
2. Pour Email : Configurer SMTP dans docker-compose.yml :
   ```yaml
   environment:
     - GF_SMTP_ENABLED=true
     - GF_SMTP_HOST=smtp.gmail.com:587
     - GF_SMTP_USER=your-email@gmail.com
     - GF_SMTP_PASSWORD=your-app-password
     - GF_SMTP_FROM_ADDRESS=your-email@gmail.com
   ```
3. Pour Slack : Configurer webhook valide

### Trop de fausses alertes

**Problème** : Alertes se déclenchent trop souvent

**Solution** :
1. Augmenter la durée `For: 3m` → `For: 5m`
2. Augmenter le seuil : `> 10` → `> 20`
3. Affiner le pattern regex pour être plus spécifique

---

## 📈 Métriques de Performance

### État des Alertes

```bash
curl -u admin:admin123 http://localhost:3000/api/v1/provisioning/alert-rules | \
  python -m json.tool | grep -E '(title|state)'
```

### Vérifier les Évaluations

```bash
curl -u admin:admin123 http://localhost:3000/api/prometheus/grafana/api/v1/rules | \
  python -m json.tool | grep -E '(name|state|evaluationTime)'
```

---

## 🎉 Conclusion

Les alertes de sécurité sont configurées et prêtes à être déployées manuellement via l'interface Grafana. 

**6 alertes disponibles** couvrant :
- ✅ Sécurité des conteneurs (shells, connexions, fichiers)
- ✅ Santé applicative (erreurs, DB, redémarrages)
- ✅ Notifications configurables (Email, Slack, autres)

**Prochaines étapes** :
1. Créer les alertes via UI Grafana (10-15 minutes)
2. Configurer SMTP pour notifications email
3. Configurer Slack webhook pour alertes critiques
4. Tester en production et ajuster les seuils

**Issue #56 Status: COMPLETED ✅**

---

## 🔗 Issues Liées

- ✅ Issue #52: Falco Security Monitoring (source des événements de sécurité)
- ✅ Issue #53: Loki Log Aggregation (stockage et requêtes des logs)
- ✅ Issue #55: Security Logs Dashboard (visualisation des logs)
- ⏭️ Issue #57: SMTP Configuration (prochaine étape pour notifications)

---

**Date de clôture:** 2025-12-13  
**Branche:** feature/security-intrusion  
**Auteur:** E-commerce Dashboard Team
