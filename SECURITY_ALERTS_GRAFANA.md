# 🚨 Système d'Alertes de Sécurité Automatisé - Grafana

Ce système détecte et alerte automatiquement sur **TOUTES les attaques** effectuées contre l'application en temps réel.

## 📋 Table des matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Types d'attaques détectées](#types-dattaques-détectées)
- [Visualisation dans Grafana](#visualisation-dans-grafana)
- [Configuration des alertes](#configuration-des-alertes)
- [Utilisation](#utilisation)

---

## 🏗️ Architecture

```
┌─────────────────────┐
│ Script d'Attaque    │
│ security_attack_    │
│ suite.py            │
└──────────┬──────────┘
           │ Métriques Prometheus
           ▼
┌─────────────────────┐
│ Prometheus         │
│ Pushgateway        │
│ :9091              │
└──────────┬──────────┘
           │ Scraping
           ▼
┌─────────────────────┐
│ Prometheus         │
│ :9090              │
└──────────┬──────────┘
           │ Queries
           ▼
┌─────────────────────┐
│ Grafana            │
│ :3000              │
│ • Dashboards       │
│ • Alertes          │
└────────────────────┘
```

## 🚀 Installation

### 1. Installer les dépendances Python

```bash
pip install prometheus_client requests
```

### 2. Démarrer les services Docker

```bash
docker-compose -f docker-compose.secure.yml up -d
```

### 3. Vérifier que tous les services sont actifs

```bash
docker-compose -f docker-compose.secure.yml ps
```

Vous devriez voir :
- ✅ ecommerce-prometheus (9090)
- ✅ ecommerce-pushgateway (9091)
- ✅ ecommerce-grafana (3000)

### 4. Accéder à Grafana

1. Ouvrez http://localhost:3000
2. Connectez-vous avec les identifiants par défaut :
   - **Username**: admin
   - **Password**: admin

### 5. Vérifier le Dashboard

Le dashboard **"🚨 Security Attacks Dashboard - Real-Time Monitoring"** devrait être automatiquement disponible dans Grafana.

---

## 🎯 Types d'attaques détectées

### 🔴 CRITICAL (Critiques)

| Attaque | Alert | Description |
|---------|-------|-------------|
| **SQL Injection** | `sql_injection_alert` | Manipulation de requêtes SQL |
| **NoSQL Injection** | `nosql_injection_alert` | MongoDB, CouchDB injection |
| **Command Injection** | `command_injection_alert` | Injection de commandes système |
| **File Upload** | `file_upload_vulnerability_alert` | Upload de webshells/malware |
| **Path Traversal** | `path_traversal_alert` | Accès fichiers système |
| **LFI/RFI** | `lfi_alert`, `rfi_alert` | Inclusion de fichiers |
| **Blind SQL Injection** | `blind_sql_injection_alert` | SQLi aveugle time/boolean |
| **Polyglot Injection** | `polyglot_injection_alert` | Payload multi-contextes |
| **Deserialization** | `deserialization_alert` | RCE via désérialisation |
| **Webshell Upload** | `webshell_upload_alert` | Upload de shell web |
| **Backdoor** | `backdoor_alert` | Création de porte dérobée |
| **Attack Chaining** | `attack_chain_alert` | Chaînage de vulnérabilités |

### 🟠 HIGH (Hautes)

| Attaque | Alert | Description |
|---------|-------|-------------|
| **LDAP Injection** | `ldap_injection_alert` | Injection LDAP |
| **XPath Injection** | `xpath_injection_alert` | Injection XPath |
| **Sensitive Data Exposure** | `sensitive_data_exposure_alert` | Exposition données sensibles |
| **Parameter Tampering** | `parameter_tampering_alert` | Manipulation paramètres |
| **Mass Assignment** | `mass_assignment_alert` | Affectation massive |
| **Race Condition** | `race_condition_alert` | Condition de course |
| **Second-Order Injection** | `second_order_injection_alert` | Injection stockée |
| **API Data Exposure** | `api_data_exposure_alert` | Données API exposées |
| **BOLA** | `bola_alert` | Broken Object Authorization |
| **DNS Exfiltration** | `dns_exfiltration_alert` | Exfiltration via DNS |
| **Slow Exfiltration** | `slow_exfiltration_alert` | Exfiltration lente |

### 🟡 MEDIUM (Moyennes)

| Attaque | Alert | Description |
|---------|-------|-------------|
| **Information Disclosure** | `information_disclosure_alert` | Fuite d'informations |
| **Business Logic Abuse** | `business_logic_abuse_alert` | Abus logique métier |
| **GraphQL Abuse** | `graphql_abuse_alert` | Abus GraphQL |
| **Dependency Exposure** | `dependency_exposure_alert` | Dépendances vulnérables |
| **Rate Limit Bypass** | `rate_limit_bypass_alert` | Contournement rate limit |
| **API Exfiltration** | `api_exfiltration_alert` | Exfiltration via API |

---

## 📊 Visualisation dans Grafana

### Dashboard Principal

Le dashboard **"Security Attacks Dashboard"** affiche :

#### 🎛️ Gauges en temps réel
- 🚨 **Total Attacks** : Nombre total d'attaques (5 min)
- 🔴 **Critical Attacks** : Attaques critiques
- 🟠 **High Severity** : Attaques haute sévérité
- 🟡 **Medium Severity** : Attaques moyenne sévérité

#### 📈 Graphiques
- **Attack Rate by Type** : Taux d'attaque par type (temps réel)
- **Attacks by Category** : Distribution par catégorie (donut)
- **Attacks by Severity** : Distribution par sévérité (donut)
- **Attack Timeline** : Timeline des attaques (barres)

#### 📋 Tables
- **Top 20 Active Attacks** : Top 20 attaques actives
- **Attack Types Reference** : Guide de référence

### Refresh automatique

Le dashboard se rafraîchit **toutes les 5 secondes** pour un monitoring en temps réel.

---

## 🔔 Configuration des Alertes

### Règles d'alertes

Toutes les règles sont configurées dans :
- **Fichier** : `grafana/provisioning/alerting/attack-alerts.yml`
- **Dossier Grafana** : Alerting → Rules

### Paramètres des alertes

- **Évaluation** : Toutes les 30 secondes
- **Déclenchement** : Dès la première détection (10s)
- **État NoData** : NoData (pas d'alerte si pas de données)
- **État Error** : Alerting (alerte en cas d'erreur)

### Notifications

Pour configurer les notifications (Email, Slack, Teams, etc.) :

1. Aller dans **Grafana** → **Alerting** → **Contact points**
2. Créer un nouveau contact point
3. Choisir le type (Email, Slack, etc.)
4. Dans **Notification policies**, associer les labels :
   - `severity=critical` → Notification immédiate
   - `severity=high` → Notification rapide
   - `severity=medium` → Notification normale

### Exemple de notification Slack

```yaml
- name: slack-security
  type: slack
  settings:
    url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    text: |
      🚨 **SECURITY ALERT**
      
      **Alert**: {{ .CommonLabels.alertname }}
      **Severity**: {{ .CommonLabels.severity }}
      **Attack Type**: {{ .CommonLabels.attack_type }}
      **Category**: {{ .CommonLabels.category }}
      
      **Description**: {{ .Annotations.description }}
```

---

## 🎮 Utilisation

### 1. Lancer une attaque de test

```bash
# Répondre "yes" quand demandé
echo "yes" | python security_attack_suite.py
```

### 2. Surveiller dans Grafana

1. Ouvrez http://localhost:3000
2. Allez dans **Dashboards** → **Security Attacks Dashboard**
3. Observez les métriques en temps réel

### 3. Voir les alertes

1. Dans Grafana, allez dans **Alerting** → **Alert rules**
2. Vous verrez les alertes actives en rouge/orange
3. Cliquez sur une alerte pour voir les détails

### 4. Vérifier les métriques dans Prometheus

```bash
# Ouvrir Prometheus
open http://localhost:9090

# Exemples de requêtes :
# - sum(security_attacks_total)
# - sum by(attack_type) (rate(security_attacks_total[5m]))
# - sum by(severity) (security_attacks_total)
```

---

## 🔍 Requêtes Prometheus utiles

### Voir toutes les attaques
```promql
security_attacks_total
```

### Compter les attaques par type
```promql
sum by(attack_type) (security_attacks_total)
```

### Taux d'attaque par minute
```promql
sum by(attack_type) (rate(security_attacks_total[1m])) * 60
```

### Attaques critiques seulement
```promql
sum(security_attacks_total{severity="critical"})
```

### Top 10 types d'attaques
```promql
topk(10, sum by(attack_type) (increase(security_attacks_total[5m])))
```

### Attaques des 5 dernières minutes
```promql
sum(increase(security_attacks_total[5m]))
```

---

## 🛠️ Dépannage

### Les alertes ne se déclenchent pas

1. **Vérifier Pushgateway** :
   ```bash
   curl http://localhost:9091/metrics
   ```
   Vous devriez voir les métriques `security_attacks_total`

2. **Vérifier Prometheus** :
   - Aller sur http://localhost:9090/targets
   - Vérifier que `pushgateway` est **UP**

3. **Vérifier les règles d'alertes** :
   - Grafana → Alerting → Alert rules
   - Vérifier que les règles sont **Provisioned**

### Le dashboard est vide

1. **Vérifier que le script a bien tourné** :
   ```bash
   ls security-reports/attack-results/
   ```

2. **Vérifier que des métriques existent** :
   ```bash
   curl http://localhost:9091/metrics | grep security_attacks
   ```

3. **Relancer le script** :
   ```bash
   echo "yes" | python security_attack_suite.py
   ```

### Prometheus ne scrape pas le Pushgateway

1. **Vérifier la config Prometheus** :
   ```bash
   cat prometheus/prometheus.yml
   ```
   Doit contenir le job `pushgateway`

2. **Recharger la config** :
   ```bash
   curl -X POST http://localhost:9090/-/reload
   ```

---

## 📁 Fichiers importants

| Fichier | Description |
|---------|-------------|
| `security_attack_suite.py` | Script d'attaque principal |
| `attack_metrics_exporter.py` | Définition des métriques |
| `grafana/provisioning/alerting/attack-alerts.yml` | Règles d'alertes |
| `grafana/dashboards/security-attacks-realtime.json` | Dashboard Grafana |
| `prometheus/prometheus.yml` | Configuration Prometheus |
| `docker-compose.secure.yml` | Services Docker |

---

## 🎯 Résumé

✅ **199 types d'attaques** détectés automatiquement  
✅ **Alertes en temps réel** dans Grafana (< 30 secondes)  
✅ **Dashboard interactif** avec refresh 5 secondes  
✅ **Classification automatique** (Critical/High/Medium/Low)  
✅ **Métriques Prometheus** pour analyse historique  
✅ **Notifications configurables** (Slack, Email, Teams, etc.)

---

## 🔗 Liens utiles

- **Grafana** : http://localhost:3000
- **Prometheus** : http://localhost:9090
- **Pushgateway** : http://localhost:9091
- **Dashboard** : http://localhost:3000/d/security-attacks
- **Alertes** : http://localhost:3000/alerting/list

---

## 📞 Support

En cas de problème :
1. Vérifier les logs Docker : `docker-compose -f docker-compose.secure.yml logs`
2. Vérifier les services : `docker-compose -f docker-compose.secure.yml ps`
3. Vérifier Prometheus targets : http://localhost:9090/targets
4. Vérifier Pushgateway metrics : http://localhost:9091/metrics

---

**🚨 IMPORTANT** : Ce système est conçu pour les tests de sécurité sur vos propres applications uniquement. L'utilisation sur des systèmes non autorisés est illégale.
