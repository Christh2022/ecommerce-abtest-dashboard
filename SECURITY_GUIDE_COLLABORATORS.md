# 🛡️ Guide de Sécurité pour les Collaborateurs

**Version:** 1.0  
**Date:** 16 Décembre 2025  
**Auteur:** Équipe Sécurité E-Commerce Dashboard

---

## 📋 Table des Matières

1. [Vue d'ensemble de la sécurité](#-vue-densemble-de-la-sécurité)
2. [Tests de sécurité automatisés](#-tests-de-sécurité-automatisés)
3. [Tests de résistance DDoS](#-tests-de-résistance-ddos)
4. [Monitoring et alertes Grafana](#-monitoring-et-alertes-grafana)
5. [Recommandations de sécurité](#-recommandations-de-sécurité)
6. [Que faire en cas d'incident](#-que-faire-en-cas-dincident-de-sécurité)
7. [Ressources et formation](#-ressources-et-formation)

---

## 🔒 Vue d'Ensemble de la Sécurité

### Protections Implémentées

Cette application e-commerce intègre **plusieurs couches de sécurité** contre les vulnérabilités web les plus courantes :

| Protection                    | Status | Description                                           |
| ----------------------------- | ------ | ----------------------------------------------------- |
| 🔐 Authentification           | ✅     | Flask-Login + bcrypt hash (12 rounds)                 |
| 🛡️ En-têtes HTTP sécurisés    | ✅     | CSP, X-Frame-Options, X-Content-Type-Options, etc.    |
| ⚡ Protection anti-DDoS        | ✅     | Rate limiting par IP (200 req/min)                    |
| 🔑 SECRET_KEY cryptographique | ✅     | 64 caractères aléatoires (SHA-256)                    |
| 🐛 Debug mode désactivé       | ✅     | Contrôlé par variable d'environnement                 |
| 📊 Tests automatisés          | ✅     | 41 types d'attaques simulées                          |
| 🚨 Monitoring temps réel      | ✅     | Grafana + Prometheus avec 32+ alertes                 |
| 💾 Backup automatique         | ⏳     | À configurer en production                            |

### Architecture de Sécurité

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Browser)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS (Production)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Reverse Proxy (Nginx)                       │
│  • SSL/TLS Termination                                          │
│  • Rate Limiting Layer 1 (10 req/s général)                     │
│  • Header Injection (HSTS, CORS)                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               Flask Application (Port 8050)                     │
│  • DDoS Protection Layer 2 (200 req/min par IP)                 │
│  • Security Headers Middleware                                  │
│  • Authentication (Flask-Login)                                 │
│  • Session Management (Secure cookies)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
    ┌────────────────────┐   ┌────────────────────┐
    │   PostgreSQL DB    │   │  Prometheus/Grafana│
    │  • Encrypted conn  │   │  • Attack monitoring│
    │  • Read-only user  │   │  • Real-time alerts │
    └────────────────────┘   └────────────────────┘
```

---

## 🚀 Tests de Sécurité Automatisés

### ⚡ Lancement Rapide (Méthode Recommandée)

#### Windows
```bash
# Double-cliquer sur le fichier ou exécuter dans cmd :
lancer_tests_securite.bat
```

#### Linux/Mac
```bash
# Rendre le script exécutable et lancer :
chmod +x lancer_tests_securite.sh
./lancer_tests_securite.sh
```

### 🎯 Ce que fait le script automatiquement

1. **Vérification des prérequis** (30 secondes)
   - ✅ Dashboard accessible sur http://localhost:8050
   - ✅ Prometheus actif sur http://localhost:9090
   - ✅ Pushgateway opérationnel sur http://localhost:9091

2. **Exécution des tests** (1-2 minutes)
   - 🎯 41 attaques simulées
   - 📊 Envoi des métriques vers Prometheus en temps réel
   - 📝 Génération de rapport JSON

3. **Affichage des résultats** (instantané)
   ```
   ╔═══════════════════════════════════════════════════════════╗
   ║           RÉSULTATS DES TESTS DE SÉCURITÉ                ║
   ╠═══════════════════════════════════════════════════════════╣
   ║  ✅ Attaques testées : 41                                 ║
   ║  ✅ Succès           : 41                                 ║
   ║  ❌ Échecs           : 0                                  ║
   ║  📊 Taux de réussite : 100%                               ║
   ╚═══════════════════════════════════════════════════════════╝
   ```

### 🧪 Test Manuel (Pour Développeurs Avancés)

```bash
# 1. Activer l'environnement virtuel
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 2. Installer les dépendances si nécessaire
pip install requests prometheus-client

# 3. Lancer les tests avec options
python test_security_simple.py

# Options disponibles :
python test_security_simple.py --verbose          # Mode verbeux
python test_security_simple.py --category sql     # Tester uniquement SQL injection
python test_security_simple.py --delay 2          # Délai de 2s entre attaques
```

### 📊 Résultats et Rapports

#### Rapport JSON
Chaque exécution génère un rapport dans `security-reports/attack-results/` :

```json
{
  "timestamp": "2025-12-16T16:47:03.123456",
  "total_attacks": 41,
  "success": 41,
  "failed": 0,
  "duration_seconds": 87.5,
  "attacks": [
    {
      "name": "SQL Injection - OR 1=1",
      "category": "sql_injection",
      "severity": "critical",
      "status": "detected",
      "response_code": 200,
      "blocked": false
    }
  ]
}
```

#### Métriques Prometheus
Les métriques sont automatiquement envoyées à Prometheus :

```prometheus
# Compteur d'attaques par type
security_attack_detected{attack_type="sql_injection", severity="critical"} 5

# Compteur d'attaques bloquées
security_attack_blocked{attack_type="xss", severity="high"} 3

# Durée des tests
security_test_duration_seconds 87.5
```

---

## ⚡ Tests de Résistance DDoS

### 🛡️ Protection Implémentée

L'application dispose d'un **système de rate limiting par IP** avec les limites suivantes :

| Endpoint Type     | Limite          | Action si dépassement        |
| ----------------- | --------------- | ---------------------------- |
| Général (/, /dashboard) | 200 req/min | Blocage IP pendant 5 minutes |
| Sensible (/login, /admin) | 20 req/min | Blocage IP immédiat |
| Exclus (/health, /assets) | Illimité | Aucune limite |

### 🧪 Test Rapide (30 secondes)

```bash
# Test de validation du rate limiting
python test_rate_limit.py
```

**Résultat attendu** :
```
🛡️  TEST DE RATE LIMITING
==================================================
Target: http://localhost:8050/
Requêtes: 250
Limite attendue: 200 req/min → blocage après ~200 req

🚫 RATE LIMIT ACTIVÉ après 7 requêtes!
   Temps écoulé: 34.2s

==================================================
📊 RÉSULTATS DU TEST
==================================================
✅ Succès:        14 (5.6%)
🚫 Bloquées:     236 (94.4%)
❌ Erreurs:        0 (0.0%)
⏱️  Temps total:  576.9s
📈 Taux moyen:   26 req/min

✅ PROTECTION DDOS FONCTIONNELLE!
   Le rate limiting a bloqué 236 requêtes
==================================================
```

### 🔥 Tests Avancés (2-5 minutes)

**⚠️ ATTENTION** : Ces tests génèrent beaucoup de traffic. **Utilisez UNIQUEMENT en local/dev**, jamais en production !

#### Test HTTP Flood (200 threads asynchrones)
```bash
python test_ddos_advanced.py http_flood
```

#### Test POST Flood (attaques sur formulaires)
```bash
python test_ddos_advanced.py post_flood
```

#### Test Slowloris (connexions lentes qui épuisent les ressources)
```bash
python test_ddos_advanced.py slowloris
```

#### Test Simple (Bash - aucune dépendance Python)
```bash
bash test_ddos_simple.sh
```

### 📈 Monitoring pendant les Tests

**Terminal 1 - Lancer le test** :
```bash
python test_ddos_advanced.py http_flood
```

**Terminal 2 - Surveiller les logs** :
```bash
docker logs ecommerce-dashboard -f | grep -E "rate_limit|blocked|429"
```

**Terminal 3 - Surveiller les ressources** :
```bash
docker stats ecommerce-dashboard
```

---

## 📊 Monitoring et Alertes Grafana

### 🎯 Accéder au Dashboard de Sécurité

1. Ouvrir [http://localhost:3000](http://localhost:3000)
2. Se connecter : `admin` / `admin123`
3. Aller dans **Dashboards** → **Security Attacks - Real-time Monitoring**

### 📈 Panneaux Disponibles (8 au total)

#### 1. Compteur Total des Attaques
```
╔═════════════════════════════════╗
║   ATTAQUES DÉTECTÉES            ║
║                                 ║
║          2,847                  ║
║                                 ║
║   ↑ +156 (dernière heure)       ║
╚═════════════════════════════════╝
```

#### 2. Attaques Critiques (Temps Réel)
- SQL Injection (OR 1=1, UNION, Blind, Time-based)
- Command Injection (OS, Shell, Reverse shell)
- Path Traversal / Directory Traversal
- Authentication Bypass

#### 3. Attaques Haute Sévérité
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- File Upload Malicious
- Brute Force Login

#### 4. Attaques Moyenne Sévérité
- Information Disclosure
- Weak Cryptography
- Rate Limit Abuse
- Directory Listing

#### 5. Graphique Temporel (Taux d'Attaques)
```
Attaques/min
   ↑
 50│     ╭─╮
   │    ╭╯ ╰╮      ╭─╮
 25│  ╭─╯   ╰─╮  ╭─╯ ╰╮
   │╭─╯       ╰──╯    ╰─
  0└──────────────────────→ Temps
   10h  11h  12h  13h  14h
```

#### 6. Distribution par Catégorie (Pie Chart)
```
   SQL Injection: 35%
   XSS: 25%
   Auth Bypass: 20%
   CSRF: 10%
   File Upload: 10%
```

#### 7. Distribution par Sévérité
```
■ Critical (25%)  ■ High (40%)  ■ Medium (30%)  ■ Low (5%)
```

#### 8. Tableau des Dernières Attaques
| Timestamp           | Type          | Sévérité | IP Source   | Status  |
| ------------------- | ------------- | -------- | ----------- | ------- |
| 2025-12-16 16:47:03 | SQL Injection | Critical | 172.20.0.1  | Détecté |
| 2025-12-16 16:47:05 | XSS Reflected | High     | 172.20.0.1  | Bloqué  |
| 2025-12-16 16:47:08 | CSRF Token    | High     | 192.168.1.5 | Détecté |

### 🚨 Règles d'Alerte (32+ configurées)

#### Alertes Critiques (déclenchement immédiat)
```yaml
# Exemple: SQL Injection détectée
- alert: SQLInjectionCritical
  expr: rate(security_attack_detected{attack_type="sql_injection"}[1m]) > 0
  for: 30s
  annotations:
    summary: "🔴 SQL Injection détectée"
    description: "Une tentative d'injection SQL a été détectée depuis {{ $labels.ip }}"
```

**Liste des alertes critiques** :
- SQL Injection (OR 1=1, UNION, Blind, Time-based)
- OS Command Injection
- Path Traversal
- Authentication Bypass

#### Alertes Haute Sévérité (déclenchement après 2-3 occurrences)
- Cross-Site Scripting (XSS)
- CSRF Token Bypass
- File Upload Malicious
- Brute Force Login (5+ tentatives)

#### Alertes Moyenne Sévérité (déclenchement après 5 occurrences)
- Information Disclosure
- Weak Cryptography
- Rate Limit Exceeded
- Directory Listing

### ⏱️ Délais de Notification
- **Critical** : 30 secondes après détection
- **High** : 1 minute
- **Medium** : 5 minutes
- **Low** : 15 minutes

---

## 🔐 Recommandations de Sécurité

### ✅ Checklist pour les Collaborateurs

#### Avant Chaque Commit

- [ ] **Aucun secret dans le code**
  ```bash
  # Vérifier qu'aucun secret n'est committé
  git diff --cached | grep -iE "password|secret|token|api_key|private_key"
  ```

- [ ] **Tests de sécurité passent**
  ```bash
  lancer_tests_securite.bat  # Windows
  ./lancer_tests_securite.sh # Linux/Mac
  ```

- [ ] **Rate limiting toujours actif**
  ```bash
  python test_rate_limit.py
  ```

- [ ] **Debug mode désactivé**
  ```bash
  docker exec ecommerce-dashboard python -c "from dashboard.app import app; print('Debug:', app.debug)"
  # Doit afficher: Debug: False
  ```

- [ ] **En-têtes de sécurité présents**
  ```bash
  curl -I http://localhost:8050/ | grep -E "X-Frame-Options|Content-Security-Policy"
  ```

#### Avant Chaque Pull Request

- [ ] **Documentation à jour** (README, SECURITY.md)
- [ ] **Tests unitaires passent** (pytest)
- [ ] **Pas de régression de sécurité**
- [ ] **Code review par un autre développeur**
- [ ] **Branch à jour avec main** (`git rebase main`)

#### Avant Chaque Déploiement

- [ ] **Backup de la base de données**
  ```bash
  docker exec ecommerce-postgres pg_dump -U dashuser ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql
  ```

- [ ] **Variables d'environnement configurées**
  ```bash
  # Vérifier que SECRET_KEY est défini
  docker exec ecommerce-dashboard printenv | grep SECRET_KEY
  ```

- [ ] **HTTPS activé** (en production uniquement)
- [ ] **Monitoring Grafana opérationnel**
- [ ] **Plan de rollback préparé**

### 🚫 Pratiques Interdites

#### ❌ Ne JAMAIS commiter ces fichiers

```gitignore
# Secrets et configuration sensible
.env
.env.local
.env.production
*.secret
*.key
*.pem

# Données utilisateurs
users.json
dashboard/users.json

# Credentials
config/database.yml
config/secrets.yml

# Backups de base de données
*.sql
*.dump
backup_*

# Logs contenant des données sensibles
*.log
security-reports/
```

#### ❌ Ne JAMAIS exposer ces informations

```python
# ❌ MAUVAIS - Secrets en dur dans le code
SECRET_KEY = "ma-cle-super-secrete-123"
DATABASE_URL = "postgresql://user:password@localhost/db"
API_KEY = "sk_live_123456789abcdef"

# ✅ BON - Variables d'environnement
import os
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')
```

#### ❌ Ne JAMAIS désactiver les protections de sécurité

```python
# ❌ MAUVAIS
app.debug = True  # En production !
rate_limit_enabled = False
csrf_protection_enabled = False

# ✅ BON - Contrôlé par environnement
app.debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
rate_limit_enabled = True  # Toujours actif
csrf_protection_enabled = True  # Toujours actif
```

### 🔒 Bonnes Pratiques de Développement

#### 1. Gestion des Secrets

```bash
# Créer un fichier .env (ne pas commiter !)
cat > .env << EOF
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_PASSWORD=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
EOF

# Charger les variables d'environnement
source .env  # Linux/Mac
# ou utiliser python-dotenv dans le code
from dotenv import load_dotenv
load_dotenv()
```

#### 2. Validation des Entrées Utilisateur

```python
# ❌ MAUVAIS - Aucune validation
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection !

# ✅ BON - Validation + Parameterized query
from flask import request, abort

user_id = request.args.get('id', type=int)
if not user_id or user_id <= 0:
    abort(400, "Invalid user ID")

# Utiliser des requêtes paramétrées
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

#### 3. Gestion des Sessions

```python
# ✅ Configuration sécurisée des sessions Flask
app.config.update(
    SESSION_COOKIE_SECURE=True,      # HTTPS uniquement
    SESSION_COOKIE_HTTPONLY=True,    # Pas d'accès JavaScript
    SESSION_COOKIE_SAMESITE='Lax',   # Protection CSRF
    PERMANENT_SESSION_LIFETIME=3600  # 1 heure
)
```

#### 4. Logging Sécurisé

```python
import logging

# ❌ MAUVAIS - Logger des données sensibles
logger.info(f"User {username} logged in with password {password}")

# ✅ BON - Ne jamais logger de secrets
logger.info(f"User {username} logged in successfully")
logger.info(f"Failed login attempt for user {username} from IP {ip}")
```

#### 5. Mise à Jour des Dépendances

```bash
# Vérifier les vulnérabilités connues
pip install safety
safety check

# Afficher les packages obsolètes
pip list --outdated

# Mettre à jour un package spécifique
pip install --upgrade requests flask werkzeug

# Régénérer requirements.txt
pip freeze > requirements.txt
```

---

## 🚨 Que Faire en Cas d'Incident de Sécurité

### Phase 1 : Réponse Immédiate (0-15 minutes)

#### Étape 1 : Isoler l'Application
```bash
# Arrêter immédiatement tous les services
docker compose -f docker-compose.secure.yml down

# Vérifier que tous les conteneurs sont arrêtés
docker ps -a | grep ecommerce
```

#### Étape 2 : Sauvegarder les Preuves
```bash
# Extraire les logs des dernières 24h
docker logs ecommerce-dashboard --since 24h > incident_logs_$(date +%Y%m%d_%H%M%S).log
docker logs ecommerce-postgres --since 24h > incident_db_logs_$(date +%Y%m%d_%H%M%S).log
docker logs ecommerce-grafana --since 24h > incident_grafana_logs_$(date +%Y%m%d_%H%M%S).log

# Backup immédiat de la base de données
docker exec ecommerce-postgres pg_dump -U dashuser ecommerce_db > incident_backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Étape 3 : Analyser l'Attaque
```bash
# Identifier les IP suspectes
grep -E "attack|injection|unauthorized" incident_logs_*.log | awk '{print $1}' | sort | uniq -c | sort -rn

# Rechercher des patterns d'attaque
grep -iE "union select|<script|cmd=|../../../|' or '1'='1" incident_logs_*.log

# Analyser les requêtes bloquées (code 429)
grep "429" incident_logs_*.log | wc -l
```

### Phase 2 : Notification (15-30 minutes)

#### Qui Notifier

1. **Responsable Sécurité** (immédiat)
   - Email : security@example.com
   - Téléphone : +33 X XX XX XX XX

2. **Équipe DevOps** (si infrastructure compromise)
   - Slack : `#devops-urgent`

3. **Management** (si données exposées)
   - CTO / RSSI

#### Que Documenter

Créer une issue GitHub avec le tag `security-incident` :

```markdown
## 🚨 Incident de Sécurité

**Date de détection** : 2025-12-16 16:47:03
**Détecté par** : [Votre nom]
**Gravité** : [Critical / High / Medium / Low]

### Description de l'incident
[Description détaillée de ce qui s'est passé]

### Type d'attaque
- [ ] SQL Injection
- [ ] XSS
- [ ] DDoS
- [ ] Brute Force
- [ ] Autre : ___________

### IP sources suspectes
- 203.0.113.45 (156 requêtes suspectes)
- 198.51.100.22 (89 tentatives de brute force)

### Impact estimé
- [ ] Aucun accès non autorisé
- [ ] Données exposées
- [ ] Service indisponible
- [ ] Perte de données

### Actions prises
1. [x] Application isolée (docker down)
2. [x] Logs sauvegardés
3. [x] Base de données backupée
4. [x] Équipe notifiée

### Prochaines étapes
- [ ] Analyse forensique complète
- [ ] Patch de sécurité
- [ ] Test de non-régression
- [ ] Redéploiement
```

### Phase 3 : Analyse et Remédiation (1-4 heures)

#### Analyse Forensique

```bash
# Analyser les temps d'accès suspects
cat incident_logs_*.log | grep -E "2025-12-16 (14|15|16):" | sort | less

# Vérifier l'intégrité des fichiers
docker exec ecommerce-dashboard sh -c "find /app -type f -name '*.py' -exec md5sum {} \;"

# Comparer avec la version Git
git status
git diff

# Chercher des backdoors
grep -r "eval\|exec\|system\|shell_exec" dashboard/
```

#### Corriger la Vulnérabilité

```bash
# 1. Créer une branche de fix
git checkout -b fix/security-incident-$(date +%Y%m%d)

# 2. Corriger le code
# [Effectuer les corrections nécessaires]

# 3. Tester localement
lancer_tests_securite.bat
python test_rate_limit.py

# 4. Commit et push
git add .
git commit -m "fix(security): [DESCRIPTION DÉTAILLÉE]"
git push origin fix/security-incident-$(date +%Y%m%d)

# 5. Créer une Pull Request URGENTE
# Tag : 🚨 SECURITY FIX
```

### Phase 4 : Redéploiement (4-6 heures)

```bash
# 1. Rebuild avec le fix
docker compose -f docker-compose.secure.yml build --no-cache

# 2. Redéployer
docker compose -f docker-compose.secure.yml up -d

# 3. Vérifier que tout fonctionne
docker compose -f docker-compose.secure.yml ps

# 4. Re-tester la sécurité
lancer_tests_securite.bat
python test_rate_limit.py

# 5. Vérifier les logs
docker logs ecommerce-dashboard --since 10m -f
```

### Phase 5 : Post-Mortem (J+1 à J+3)

#### Document à Créer : `docs/POST_MORTEM_YYYYMMDD.md`

```markdown
# Post-Mortem : Incident de Sécurité du [DATE]

## Résumé Exécutif
[Résumé en 2-3 phrases de ce qui s'est passé]

## Timeline
- **14:00** : Première attaque détectée
- **14:15** : Alerte Grafana déclenchée
- **14:20** : Application isolée
- **15:30** : Vulnérabilité identifiée
- **17:00** : Fix déployé
- **17:30** : Service restauré

## Cause Racine
[Explication détaillée de la vulnérabilité exploitée]

## Impact
- Durée de l'incident : 3h30
- Utilisateurs affectés : 0 (isolé avant exploitation)
- Données exposées : Aucune
- Perte financière : Estimée à 0€

## Actions Correctives
1. [x] Patch de sécurité appliqué
2. [ ] Tests de sécurité élargis
3. [ ] Formation équipe sur la vulnérabilité
4. [ ] Amélioration du monitoring

## Leçons Apprises
- Ce qui a bien fonctionné :
  * Détection rapide via Grafana
  * Procédure d'isolation efficace
  
- Ce qui doit être amélioré :
  * Délai de notification trop long
  * Manque d'automatisation du rollback

## Recommandations
1. Mettre en place un WAF (Web Application Firewall)
2. Augmenter la couverture des tests de sécurité
3. Formation mensuelle de l'équipe sur OWASP Top 10
```

---

## 🎓 Ressources et Formation

### 📚 Documentation Officielle

#### Sécurité Web Générale
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Les 10 vulnérabilités les plus critiques
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - Guides de sécurité par sujet
- [CWE/SANS Top 25](https://www.sans.org/top25-software-errors/) - Erreurs logicielles les plus dangereuses

#### Technologies Utilisées
- [Flask Security](https://flask.palletsprojects.com/en/3.0.x/security/) - Best practices Flask
- [Docker Security](https://docs.docker.com/engine/security/) - Sécuriser les conteneurs
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html) - Sécurité base de données
- [Nginx Security](https://nginx.org/en/docs/http/ngx_http_ssl_module.html) - Configuration SSL/TLS

### 🎮 Plateformes d'Apprentissage Pratique

| Plateforme                                                  | Type           | Niveau      | Coût   |
| ----------------------------------------------------------- | -------------- | ----------- | ------ |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | Labs guidés    | Débutant+   | Gratuit|
| [HackTheBox](https://www.hackthebox.com/)                   | CTF / Labs     | Intermédiaire+ | Freemium |
| [TryHackMe](https://tryhackme.com/)                         | Parcours guidés | Débutant+ | Freemium |
| [PentesterLab](https://pentesterlab.com/)                   | Exercices web  | Tous niveaux | Payant |
| [OWASP WebGoat](https://owasp.org/www-project-webgoat/)    | Application vulnérable | Débutant | Gratuit |

### 🛠️ Outils de Test Recommandés

#### Scanners de Vulnérabilités
```bash
# OWASP ZAP (gratuit, open-source)
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:8050

# Nikto (scanner de serveur web)
nikto -h http://localhost:8050

# SQLMap (test d'injection SQL)
sqlmap -u "http://localhost:8050/search?q=test" --batch --level=5 --risk=3
```

#### Proxy d'Interception
- **Burp Suite Community** : [portswigger.net/burp/communitydownload](https://portswigger.net/burp/communitydownload)
- **OWASP ZAP** : [zaproxy.org](https://www.zaproxy.org/)

#### Analyse de Code
```bash
# Bandit (Python security linter)
pip install bandit
bandit -r dashboard/ -f json -o security_report.json

# Safety (vérification des dépendances)
pip install safety
safety check --json
```

### 📖 Livres Recommandés

1. **"The Web Application Hacker's Handbook"** - Dafydd Stuttard, Marcus Pinto
   - La bible de la sécurité web
   - 736 pages, niveau intermédiaire/avancé

2. **"OWASP Testing Guide v4"** - OWASP Foundation
   - Guide complet de test de pénétration
   - Gratuit, disponible en ligne

3. **"Practical API Security"** - Prabath Siriwardena
   - Spécialisé sur la sécurité des APIs
   - Niveau intermédiaire

### 🎓 Certifications Cybersécurité

| Certification                      | Niveau        | Durée Préparation | Coût     |
| ---------------------------------- | ------------- | ----------------- | -------- |
| **CEH** (Certified Ethical Hacker) | Intermédiaire | 3-6 mois          | ~1000€   |
| **OSCP** (Offensive Security)      | Avancé        | 6-12 mois         | ~1500€   |
| **CISSP** (Security Professional)  | Avancé        | 6-12 mois         | ~700€    |
| **Security+** (CompTIA)            | Débutant      | 2-3 mois          | ~350€    |

---

## 📞 Support et Contact

### 🚨 Signalement de Vulnérabilité

**Email de sécurité** : security@example.com

**Politique de divulgation responsable** :
1. **Ne pas** publier la vulnérabilité avant correction
2. Envoyer un rapport détaillé à l'équipe sécurité
3. Attendre notre accusé de réception (< 48h)
4. Collaborer avec nous pour la correction
5. Divulgation publique après patch déployé

**Modèle de rapport** :
```
Sujet : [SECURITY] Vulnérabilité [TYPE] dans [COMPOSANT]

1. Description de la vulnérabilité
2. Étapes pour reproduire
3. Impact potentiel (CVSS si possible)
4. Preuve de concept (PoC)
5. Suggestions de correction
```

### 💬 Questions et Aide

- **Issues GitHub** : https://github.com/Christh2022/ecommerce-abtest-dashboard/issues (tag `security`)
- **Slack** : `#security` (pour l'équipe interne)
- **Email** : support@example.com

### 📚 Documentation Complémentaire

- `README.md` - Guide de démarrage général
- `SECURITY.md` - Politique de sécurité du projet
- `GUIDE_COLLABORATEURS.md` - Guide pour nouveaux collaborateurs
- `docs/DDOS_PROTECTION_REPORT.md` - Rapport sur la protection DDoS
- `docs/AUTHENTICATION_ARCHITECTURE.md` - Architecture d'authentification

---

## ✅ Checklist Finale

### Pour les Nouveaux Collaborateurs

- [ ] J'ai lu ce guide en entier
- [ ] J'ai compris l'architecture de sécurité
- [ ] J'ai lancé les tests de sécurité avec succès
- [ ] J'ai accès au dashboard Grafana
- [ ] Je connais la procédure en cas d'incident
- [ ] J'ai configuré mon environnement de dev sécurisé
- [ ] Je sais qui contacter en cas de problème

### Pour les Contributeurs Réguliers

- [ ] Je lance les tests de sécurité avant chaque PR
- [ ] Je vérifie qu'aucun secret n'est committé
- [ ] Je documente les changements liés à la sécurité
- [ ] Je reste à jour sur OWASP Top 10
- [ ] Je participe aux revues de code sécurité
- [ ] Je contribue à améliorer les tests

---

**Dernière mise à jour** : 16 Décembre 2025  
**Version** : 1.0  
**Mainteneur** : Équipe Sécurité E-Commerce Dashboard

**Questions ?** Contactez-nous sur `#security` ou par email à security@example.com
