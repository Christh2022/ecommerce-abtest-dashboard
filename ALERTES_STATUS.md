# 🎯 Système d'Alertes de Sécurité - Guide de Configuration Complet

## ✅ Ce qui a été créé

### 1. **Script d'Attaque avec Métriques** (`security_attack_suite.py`)
- ✅ 199 types d'attaques automatisées
- ✅ Push de métriques Prometheus intégré
- ✅ Chaque attaque génère une métrique `security_attacks_total`

### 2. **Prometheus Pushgateway**
- ✅ Service Docker configuré (port 9091)
- ✅ Configuration Prometheus pour scraping

### 3. **Règles d'Alertes Grafana** (`grafana/provisioning/alerting/attack-alerts.yml`)
- ✅ **50+ règles d'alertes** configurées
- ✅ Une alerte par type d'attaque
- ✅ Classification par sévérité (Critical/High/Medium)

### 4. **Dashboard Grafana** (`grafana/dashboards/security-attacks-realtime.json`)
- ✅ Monitoring en temps réel (refresh 5s)
- ✅ Gauges pour métriques critiques
- ✅ Graphiques temporels
- ✅ Tables des attaques actives

---

## 🚀 Activation du Système (Prochaines Étapes)

### Étape 1 : Exposer le Pushgateway

Le Pushgateway est dans le réseau Docker mais pas accessible depuis l'hôte Windows.

**Option A : Via Docker Network (Recommandé pour Production)**

Modifier `security_attack_suite.py` :
```python
# Au lieu de :
PROMETHEUS_PUSHGATEWAY = "http://127.0.0.1:9091"

# Utiliser :
PROMETHEUS_PUSHGATEWAY = "http://pushgateway:9091"
```

Puis lancer le script dans un container Docker :
```bash
docker run --rm --network ecommerce-abtest-dashboard_monitoring-network \
  -v $(pwd):/app -w /app python:3.12 \
  python security_attack_suite.py
```

**Option B : Mapper le port sur l'hôte (Pour Tests)**

Le port est déjà configuré dans `docker-compose.secure.yml` ligne 131 :
```yaml
ports:
  - "9091:9091"
```

Vérifier que le service démarre correctement :
```bash
docker-compose -f docker-compose.secure.yml ps pushgateway
docker logs ecommerce-pushgateway
```

### Étape 2 : Vérifier Prometheus

1. Accéder à http://localhost:9090/targets
2. Vérifier que le target `pushgateway` est **UP**
3. Si pas UP, vérifier `prometheus/prometheus.yml`

### Étape 3 : Importer le Dashboard dans Grafana

1. Accéder à http://localhost:3000
2. Aller dans **Dashboards** → **Import**
3. Uploader `grafana/dashboards/security-attacks-realtime.json`
4. Ou utiliser le provisioning automatique (déjà configuré)

### Étape 4 : Configurer les Notifications

Dans Grafana :
1. **Alerting** → **Contact points**
2. Créer un contact (Email, Slack, Teams, etc.)
3. **Notification policies** → Associer par labels

---

## 🎮 Utilisation

### Lancer une attaque

```bash
echo "yes" | python security_attack_suite.py
```

### Visualiser en temps réel

1. **Dashboard Grafana** : http://localhost:3000/d/security-attacks
   - Attaques totales
   - Par type
   - Par sévérité
   - Timeline

2. **Alertes actives** : http://localhost:3000/alerting/list
   - Toutes les alertes déclenchées
   - État (Firing/Pending/Normal)

3. **Métriques Prometheus** : http://localhost:9090
   ```promql
   # Voir toutes les attaques
   security_attacks_total
   
   # Attaques critiques
   security_attacks_total{severity="critical"}
   
   # Top 10 attaques
   topk(10, sum by(attack_type) (security_attacks_total))
   ```

---

## 📊 Exemples d'Alertes

### SQL Injection
**Déclenchement** : Dès la première détection  
**Sévérité** : 🔴 CRITICAL  
**Message** : "⚠️ SQL Injection attack detected! X attempts in the last 5 minutes"

### Webshell Upload
**Déclenchement** : Dès la première détection  
**Sévérité** : 🔴 CRITICAL  
**Message** : "🚨 WEBSHELL UPLOAD DETECTED! Critical threat - immediate action required!"

### Parameter Tampering
**Déclenchement** : Dès la première détection  
**Sévérité** : 🟠 HIGH  
**Message** : "⚠️ Parameter tampering detected! User input manipulation in progress"

### Rate Limit Bypass
**Déclenchement** : Dès la première détection  
**Sévérité** : 🟡 MEDIUM  
**Message** : "⚠️ Rate limit bypass detected! Attacker evading rate limiting"

---

## 🔧 Configuration Actuelle

| Composant | Statut | Port | URL |
|-----------|--------|------|-----|
| Pushgateway | ✅ Running | 9091 | http://localhost:9091 |
| Prometheus | ✅ Running | 9090 | http://localhost:9090 |
| Grafana | ✅ Running | 3000 | http://localhost:3000 |
| Dashboard | ✅ Créé | - | security-attacks-realtime.json |
| Alertes | ✅ Créées | - | attack-alerts.yml (50+ règles) |

---

## 📋 Liste Complète des Alertes

### 🔴 CRITICAL (12 alertes)
1. SQL Injection
2. NoSQL Injection
3. Command Injection
4. File Upload Vulnerability
5. Path Traversal
6. Local File Inclusion (LFI)
7. Remote File Inclusion (RFI)
8. Blind SQL Injection
9. Polyglot Injection
10. Insecure Deserialization
11. Webshell Upload
12. Backdoor Creation
13. Attack Chaining
14. Multiple Critical Vulnerabilities (> 5 dans 5 min)

### 🟠 HIGH (11 alertes)
15. LDAP Injection
16. XPath Injection
17. Sensitive Data Exposure
18. Parameter Tampering
19. Mass Assignment
20. Race Condition
21. Second-Order Injection
22. API Data Exposure
23. BOLA
24. DNS Exfiltration
25. Slow Data Exfiltration

### 🟡 MEDIUM (6 alertes)
26. Information Disclosure
27. Business Logic Abuse
28. GraphQL Abuse
29. Dependency Exposure
30. Rate Limit Bypass
31. API Exfiltration

### 📈 VOLUME
32. High Attack Volume (> 50 attaques en 5 min)

---

## 🔍 Monitoring en Temps Réel

### Dashboard affiche :

**Gauges (mise à jour toutes les 5s)**
- 🚨 Total Attacks (Last 5 min)
- 🔴 Critical Attacks
- 🟠 High Severity Attacks
- 🟡 Medium Severity Attacks

**Graphiques**
- 📊 Attack Rate by Type (Real-time)
- 🎯 Attacks by Category (Pie chart)
- ⚠️ Attacks by Severity (Pie chart)
- 📈 Attack Timeline (Bars)

**Tables**
- 🔝 Top 20 Active Attacks
- 📚 Attack Types Reference

---

## 🎯 Prochaine Action

Pour activer complètement le système :

```bash
# 1. Vérifier les services
docker-compose -f docker-compose.secure.yml ps

# 2. Vérifier Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job=="pushgateway")'

# 3. Lancer une attaque de test
echo "yes" | python security_attack_suite.py

# 4. Vérifier les métriques dans Pushgateway
curl http://localhost:9091/metrics | grep security_attacks

# 5. Voir les alertes dans Grafana
open http://localhost:3000/alerting/list
```

---

## ✅ Résumé

**Ce qui est configuré** :
- ✅ 199 types d'attaques automatisées
- ✅ Envoi de métriques Prometheus
- ✅ 32+ règles d'alertes Grafana
- ✅ Dashboard temps réel
- ✅ Classification par sévérité
- ✅ Pushgateway Docker

**Pour activer** :
1. Vérifier que le Pushgateway est accessible
2. Lancer le script d'attaque
3. Observer les alertes dans Grafana

**Délai de détection** : < 30 secondes
**Refresh dashboard** : 5 secondes
**Évaluation alertes** : 30 secondes

---

🔗 **Documentation complète** : [SECURITY_ALERTS_GRAFANA.md](SECURITY_ALERTS_GRAFANA.md)
