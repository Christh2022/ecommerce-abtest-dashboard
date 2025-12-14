# 🧪 GUIDE POUR LES COLLABORATEURS - TESTS DE SÉCURITÉ

## 📋 Vue d'ensemble

Ce guide explique comment **tester le système de détection d'attaques** et **vérifier que tout fonctionne correctement**.

---

## 🚀 Méthode 1 : Utiliser le script automatique (RECOMMANDÉ)

### Windows

Double-cliquez sur le fichier :
```
lancer_tests_securite.bat
```

### Linux / Mac

```bash
chmod +x lancer_tests_securite.sh
./lancer_tests_securite.sh
```

### Ce que fait le script :
1. ✅ Vérifie que Docker est lancé
2. ✅ Vérifie que Pushgateway fonctionne
3. ✅ Lance 41 tests d'attaques
4. ✅ Envoie les métriques vers Prometheus
5. ✅ Génère un rapport JSON

---

## 🔍 Méthode 2 : Vérifier que le système fonctionne

### Étape 1 : Vérifier les services

**Windows :**
```cmd
verifier_systeme.bat
```

**Linux/Mac :**
```bash
docker ps
```

**Services requis :**
- ✅ ecommerce-pushgateway (port 9091)
- ✅ ecommerce-prometheus (port 9090)
- ✅ ecommerce-grafana (port 3000)
- ✅ ecommerce-dashboard (port 8050)

### Étape 2 : Lancer un test manuel

```bash
python test_security_simple.py --target http://localhost:8050
```

**Résultat attendu :**
```
============================================================
SECURITY TESTING COMPLETED
Total vulnerabilities: 41
Critical: 20
High: 15
Medium: 6
============================================================
```

### Étape 3 : Vérifier les métriques dans Pushgateway

**Navigateur :** http://localhost:9091

**Terminal :**
```bash
curl http://localhost:9091/metrics | grep security_attacks_total
```

**Ce que vous devez voir :**
```
security_attacks_total{attack_type="sql_injection",...} 5
security_attacks_total{attack_type="command_injection",...} 4
security_attacks_total{attack_type="path_traversal",...} 4
...
```

### Étape 4 : Vérifier le Dashboard Grafana

1. **Ouvrir Grafana :** http://localhost:3000
2. **Login :** admin / admin (changez le mot de passe si demandé)
3. **Aller dans :** Dashboards → "Security Attacks Dashboard - Real-Time Monitoring"

**Ce que vous devez voir :**
- 🔴 Total Attacks : **41**
- 🔴 Critical Attacks : **20**
- 🟠 High Severity : **15**
- 🟡 Medium Severity : **6**
- 📊 Graphiques avec les attaques par type

### Étape 5 : Vérifier les alertes

1. **Aller sur :** http://localhost:3000/alerting/list
2. **Attendre 30-60 secondes** après les tests
3. **Voir les alertes en état "Firing"** (rouge)

**Alertes attendues :**
- 🚨 SQL Injection Detected
- 🚨 Command Injection Detected
- 🚨 Path Traversal Attack
- 🚨 File Upload Vulnerability
- Et plus...

### Étape 6 : Consulter les rapports

**Emplacement :**
```
security-reports/attack-results/security_test_YYYYMMDD_HHMMSS.json
```

**Ouvrir le dernier rapport :**
```json
{
  "timestamp": "2025-12-15T00:46:25.123456",
  "target": "http://localhost:8050",
  "total_tests": 41,
  "vulnerabilities": [
    {
      "category": "SQL Injection",
      "severity": "CRITICAL",
      "description": "SQL payload tested: ' OR '1'='1",
      "timestamp": "2025-12-15T00:46:25.234567"
    },
    ...
  ]
}
```

---

## ❌ Résolution de problèmes

### Problème 1 : "No data" dans le dashboard

**Cause :** Les tests n'ont pas été lancés ou Prometheus n'a pas encore scrapé les données.

**Solution :**
1. Lancer les tests : `lancer_tests_securite.bat`
2. Attendre 10-15 secondes
3. Rafraîchir le dashboard Grafana (F5)

### Problème 2 : Pushgateway inaccessible

**Erreur :**
```
Could not push to Prometheus: [WinError 10061]
```

**Solution :**
```bash
# Vérifier que Pushgateway est lancé
docker ps | grep pushgateway

# Recréer le service si nécessaire
docker-compose -f docker-compose.secure.yml up -d --force-recreate pushgateway

# Tester la connexion
curl http://localhost:9091/metrics
```

### Problème 3 : Dashboard Grafana vide après les tests

**Vérifications :**
1. **Pushgateway a les métriques ?**
   ```bash
   curl http://localhost:9091/metrics | grep security_attacks
   ```

2. **Prometheus scrape Pushgateway ?**
   ```bash
   docker logs ecommerce-prometheus | grep pushgateway
   ```

3. **Datasource Grafana configurée ?**
   - Aller sur http://localhost:3000/datasources
   - Vérifier que "Prometheus" existe
   - Tester la connexion

### Problème 4 : Alertes ne se déclenchent pas

**Causes possibles :**
- ⏱️ **Délai normal :** Les alertes ont un délai de 30s-1min
- 🔧 **Règles non chargées :** Vérifier les logs Grafana

**Solution :**
```bash
# Vérifier les logs Grafana
docker logs ecommerce-grafana | grep alert

# Vérifier les règles d'alerte
curl -s http://admin:admin@localhost:3000/api/v1/provisioning/alert-rules
```

---

## 📊 Interpréter les résultats

### Types d'attaques par sévérité

| Sévérité | Count | Description |
|----------|-------|-------------|
| 🔴 **CRITICAL** | 20 | Nécessite une action immédiate |
| 🟠 **HIGH** | 15 | Risque élevé, correction rapide |
| 🟡 **MEDIUM** | 6 | Risque modéré, planifier correction |

### Top 5 des attaques les plus fréquentes

1. **SQL Injection** : 5 tests (CRITICAL)
2. **Command Injection** : 4 tests (CRITICAL)
3. **Path Traversal** : 4 tests (CRITICAL)
4. **File Upload** : 4 tests (HIGH)
5. **NoSQL Injection** : 4 tests (CRITICAL)

### Que faire si une vraie attaque est détectée ?

1. **Consulter le dashboard** pour identifier le type d'attaque
2. **Vérifier les logs applicatifs** dans `dashboard/logs/`
3. **Consulter le rapport JSON** pour les détails
4. **Bloquer l'IP source** si nécessaire
5. **Corriger la vulnérabilité** dans le code
6. **Re-tester** avec le script

---

## 🔄 Automatisation des tests

### Tester toutes les heures (Windows Task Scheduler)

1. Ouvrir **Task Scheduler**
2. Créer une nouvelle tâche
3. **Déclencheur :** Toutes les heures
4. **Action :** Lancer `lancer_tests_securite.bat`

### Tester toutes les heures (Linux Cron)

```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne
0 * * * * cd /path/to/ecommerce-abtest-dashboard && ./lancer_tests_securite.sh
```

### Intégration CI/CD (GitHub Actions)

```yaml
name: Security Tests

on:
  schedule:
    - cron: '0 */6 * * *'  # Toutes les 6 heures
  workflow_dispatch:

jobs:
  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run security tests
        run: python test_security_simple.py --target ${{ secrets.TARGET_URL }}
```

---

## 📞 Support

### Commandes utiles

```bash
# Voir tous les services
docker ps

# Voir les logs d'un service
docker logs ecommerce-pushgateway
docker logs ecommerce-prometheus
docker logs ecommerce-grafana

# Redémarrer un service
docker restart ecommerce-pushgateway

# Redémarrer tout
docker-compose -f docker-compose.secure.yml restart

# Arrêter tout
docker-compose -f docker-compose.secure.yml down

# Démarrer tout
docker-compose -f docker-compose.secure.yml up -d
```

### URLs importantes

- 📊 **Grafana Dashboard :** http://localhost:3000
- 🔔 **Alertes Grafana :** http://localhost:3000/alerting/list
- 📈 **Pushgateway :** http://localhost:9091
- 🎯 **Application cible :** http://localhost:8050

---

## ✅ Checklist de validation

Avant de dire que le système fonctionne, vérifier :

- [ ] Tous les services Docker sont "Up" et "healthy"
- [ ] Pushgateway accessible sur http://localhost:9091
- [ ] Script de test s'exécute sans erreur
- [ ] Message "Metric pushed to Prometheus" apparaît
- [ ] Métriques visibles dans Pushgateway
- [ ] Dashboard Grafana affiche des données
- [ ] Au moins une alerte en état "Firing"
- [ ] Rapport JSON généré dans `security-reports/`

---

**Système opérationnel ✅**
**Date de dernière mise à jour : 2025-12-15**
