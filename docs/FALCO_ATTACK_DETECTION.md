# 🛡️ FALCO SECURITY ATTACK DETECTION

## 📋 Vue d'ensemble

Falco est maintenant configuré pour **détecter automatiquement toutes les attaques** exécutées par le script `security_attack_suite.py`.

### Architecture de détection

```
Attack Script → Docker Containers → Falco → Promtail → Loki → Grafana Alerts
                                      ↓
                                   Logs JSON
```

## 🚀 Activation de Falco

### 1. Démarrage des services

```bash
# Arrêter les services existants
docker-compose -f docker-compose.secure.yml down

# Recréer les services avec Falco activé
docker-compose -f docker-compose.secure.yml up -d

# Vérifier que Falco est en cours d'exécution
docker ps | grep falco
docker logs ecommerce-falco
```

### 2. Vérification des règles

```bash
# Lister les règles chargées
docker exec ecommerce-falco falco -L

# Vérifier les règles personnalisées
docker exec ecommerce-falco cat /etc/falco/security_attack_rules.yaml
```

## 🎯 Types d'attaques détectées

### 1. **Injection Attacks** (Détection en temps réel)

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| SQL Injection | `SQL Injection Attack Detected` | CRITICAL | ✅ |
| NoSQL Injection | `NoSQL Injection Attack` | CRITICAL | ✅ |
| Command Injection | `Command Injection Attack` | CRITICAL | ✅ |
| LDAP Injection | `LDAP Injection Attempt` | HIGH | ✅ |
| XPath Injection | `XPath Injection Attempt` | HIGH | ✅ |

**Détection :**
- Analyse des arguments de commandes
- Détection de mots-clés SQL : `SELECT`, `UNION`, `DROP TABLE`, `' OR '1'='1'`
- Détection de caractères d'injection : `;`, `|`, `&&`, `||`, `$(`

### 2. **File Attacks**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Path Traversal | `Path Traversal Attack` | CRITICAL | ✅ |
| Sensitive File Access | `Sensitive File Access` | HIGH | ✅ |
| Webshell Upload | `Webshell Upload Detected` | CRITICAL | ✅ |
| Suspicious File Upload | `Suspicious File Upload` | HIGH | ✅ |

**Détection :**
- Accès à des chemins avec `../`, `..%2F`
- Lecture de fichiers sensibles : `/etc/passwd`, `/etc/shadow`, `.env`, `users.json`
- Upload de fichiers exécutables : `.php`, `.jsp`, `.aspx`, `.exe`, `.sh`
- Détection de code malveillant : `eval`, `system`, `exec`, `shell_exec`

### 3. **Shell & Process Attacks**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Shell Spawned | `Shell Spawned in Container` | HIGH | ✅ |
| Reverse Shell | `Reverse Shell Detected` | CRITICAL | ✅ |
| Suspicious Network Tool | `Suspicious Network Tool` | HIGH | ✅ |

**Détection :**
- Shells interactifs : `bash`, `sh`, `zsh` avec TTY
- Reverse shells : `nc -e`, `bash -i`, `/dev/tcp/`, `python -c socket`
- Outils de reconnaissance : `nmap`, `masscan`, `nikto`, `sqlmap`

### 4. **Data Exfiltration**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| DNS Exfiltration | `Data Exfiltration via DNS` | HIGH | ✅ |
| Suspicious Connection | `Suspicious Network Connection` | MEDIUM | ✅ |
| Large Data Transfer | `Large Data Transfer` | MEDIUM | ✅ |

**Détection :**
- Requêtes DNS avec `base64`
- Connexions sortantes vers des IPs externes
- Transferts de données > 1MB

### 5. **Credential Access**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Password File Access | `Password File Access` | HIGH | ✅ |
| SSH Key Access | `SSH Key Access` | CRITICAL | ✅ |

**Détection :**
- Accès à `/etc/passwd`, `/etc/shadow`
- Lecture de clés SSH : `id_rsa`, `authorized_keys`
- Accès à fichiers secrets : `.env`, `credentials.json`, `passwords.txt`

### 6. **Persistence Mechanisms**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Cron Job Modification | `Cron Job Modification` | HIGH | ✅ |
| Startup Script Modification | `Startup Script Modification` | HIGH | ✅ |

**Détection :**
- Modifications dans `/etc/cron`, `crontab`
- Modifications de scripts : `.bashrc`, `.bash_profile`, `/etc/profile`

### 7. **Privilege Escalation**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Privilege Escalation | `Privilege Escalation Attempt` | CRITICAL | ✅ |
| Docker Socket Access | `Docker Socket Access` | CRITICAL | ✅ |

**Détection :**
- Commandes `sudo`, `su`, `pkexec`
- Modifications de permissions : `chmod +s`, `chmod 4755`
- Accès à `/var/run/docker.sock` (container escape)

### 8. **Advanced Attacks**

| Type d'attaque | Règle Falco | Priorité | Alerte Grafana |
|---------------|-------------|----------|----------------|
| Container Escape | `Container Escape Attempt` | CRITICAL | ✅ |
| Attack Chain | `Attack Chain Detected` | CRITICAL | ✅ |
| Crypto Mining | `Crypto Mining Activity` | HIGH | ✅ |
| Insecure Deserialization | `Insecure Deserialization` | CRITICAL | ✅ |

**Détection :**
- Utilisation de `nsenter`, `unshare`, `chroot /host`
- Chaînage d'attaques avec `curl`, `wget`, `python -c`
- Processus de mining : `xmrig`, `cpuminer`, `stratum+`
- Désérialisation dangereuse : `pickle`, `yaml.load`, `unserialize`

## 📊 Alertes Grafana

### Configuration des alertes

**Fichiers :**
- `grafana/provisioning/alerting/falco-alerts.yml` - 25+ règles d'alerte

**Caractéristiques :**
- ✅ Détection en temps réel (évaluation toutes les 10s)
- ✅ Seuil : 1 événement en 1 minute
- ✅ Délai de confirmation : 10-30 secondes
- ✅ Labels par sévérité : `critical`, `high`, `medium`
- ✅ Labels par type d'attaque
- ✅ Source identifiée : `source=falco`

### Accès aux alertes

1. **Grafana UI** : http://localhost:3000/alerting/list
2. **Filtrer par** :
   - `severity=critical` - Alertes critiques
   - `source=falco` - Alertes Falco uniquement
   - `attack_type=sql_injection` - Type spécifique

## 🔍 Monitoring en temps réel

### Logs Falco

```bash
# Afficher les logs Falco en temps réel
docker logs -f ecommerce-falco

# Filtrer par type d'attaque
docker logs ecommerce-falco | grep "SQL INJECTION"
docker logs ecommerce-falco | grep "WEBSHELL UPLOAD"
docker logs ecommerce-falco | grep "REVERSE SHELL"
```

### Logs JSON structurés

Falco génère des logs JSON avec :
```json
{
  "output": "🚨 SQL INJECTION DETECTED",
  "priority": "Critical",
  "rule": "SQL Injection Attack Detected",
  "time": "2024-01-15T10:30:45.123Z",
  "output_fields": {
    "container.name": "ecommerce-dashboard",
    "proc.name": "python3",
    "proc.cmdline": "SELECT * FROM users WHERE id='1' OR '1'='1'",
    "user.name": "root",
    "fd.name": "/app/data.db"
  },
  "tags": ["injection", "sql", "attack", "security"]
}
```

### Loki queries

Dans Grafana Explore (http://localhost:3000/explore) :

```logql
# Toutes les attaques détectées par Falco
{container="ecommerce-falco"} |= "DETECTED"

# Attaques SQL
{container="ecommerce-falco"} |= "SQL INJECTION DETECTED"

# Attaques critiques
{container="ecommerce-falco", priority="Critical"}

# Comptage des attaques par type
sum(count_over_time({container="ecommerce-falco"} |= "DETECTED" [5m])) by (rule)

# Top 10 des règles déclenchées
topk(10, sum(count_over_time({container="ecommerce-falco"}[1h])) by (rule))
```

## 🧪 Test de détection

### 1. Exécuter le script d'attaque

```bash
python security_attack_suite.py --target http://localhost:8050 --timeout 5
```

### 2. Vérifier les détections Falco

```bash
# Compter les alertes générées
docker logs ecommerce-falco | grep "DETECTED" | wc -l

# Voir les types d'attaques détectées
docker logs ecommerce-falco | grep "DETECTED" | grep -oP '\w+ DETECTED' | sort | uniq -c
```

### 3. Vérifier les alertes Grafana

1. Aller sur : http://localhost:3000/alerting/list
2. Filtrer par `source=falco`
3. Voir les alertes actives en **Firing**

### 4. Vérifier les logs dans Loki

1. Aller sur : http://localhost:3000/explore
2. Sélectionner datasource **Loki**
3. Query : `{container="ecommerce-falco"} |= "DETECTED"`
4. Voir les résultats en temps réel

## 📈 Dashboard Falco

### Création d'un dashboard personnalisé

Créer un nouveau dashboard dans Grafana avec ces panels :

#### Panel 1 : Total attaques détectées
```logql
sum(count_over_time({container="ecommerce-falco"} |= "DETECTED" [5m]))
```

#### Panel 2 : Attaques par priorité
```logql
sum(count_over_time({container="ecommerce-falco", priority=~"Critical|Error|Warning"} [5m])) by (priority)
```

#### Panel 3 : Top 10 règles déclenchées
```logql
topk(10, sum(count_over_time({container="ecommerce-falco"}[1h])) by (rule))
```

#### Panel 4 : Attaques par conteneur cible
```logql
sum(count_over_time({container="ecommerce-falco"} [5m])) by (container)
```

#### Panel 5 : Timeline des attaques
```logql
{container="ecommerce-falco"} |= "DETECTED"
```

## 🛠️ Configuration avancée

### Ajuster la sensibilité

**Fichier :** `falco/falco.yaml`

```yaml
# Priorité minimale pour logger
priority: debug  # debug, info, warning, error, critical

# Buffer pour les sorties
buffered_outputs: true
```

### Ajouter des règles personnalisées

**Fichier :** `falco/security_attack_rules.yaml`

```yaml
- rule: Ma Nouvelle Règle
  desc: Description de la détection
  condition: >
    spawned_process and
    proc.name = "mon_process"
  output: >
    🚨 MA NOUVELLE ATTAQUE (container=%container.name process=%proc.name)
  priority: CRITICAL
  tags: [custom, attack]
  source: syscall
```

### Désactiver certaines règles

```yaml
# Dans falco_rules.local.yaml
- rule: Ma Règle à Désactiver
  enabled: false
```

## 🔧 Troubleshooting

### Falco ne démarre pas

```bash
# Vérifier les logs
docker logs ecommerce-falco

# Vérifier la configuration
docker exec ecommerce-falco falco --validate /etc/falco/falco.yaml

# Vérifier les règles
docker exec ecommerce-falco falco --validate /etc/falco/security_attack_rules.yaml
```

### Pas d'alertes générées

```bash
# 1. Vérifier que Falco détecte bien
docker logs ecommerce-falco | tail -50

# 2. Vérifier que Promtail envoie les logs
docker logs ecommerce-promtail | grep falco

# 3. Vérifier que Loki reçoit les logs
curl -s "http://localhost:3100/loki/api/v1/query?query={container=\"ecommerce-falco\"}" | jq

# 4. Vérifier les règles d'alerte Grafana
curl -s http://admin:admin@localhost:3000/api/v1/provisioning/alert-rules | jq
```

### Performances

Si Falco consomme trop de ressources :

```yaml
# Dans docker-compose.secure.yml
deploy:
  resources:
    limits:
      cpus: "0.5"      # Réduire à 0.5 CPU
      memory: 256M     # Réduire à 256MB
```

## 📚 Référence des règles

### Syntaxe des conditions Falco

```yaml
# Événements système
evt.type = execve                    # Exécution de processus
evt.type in (open, openat, openat2)  # Ouverture de fichiers
evt.dir = "<"                        # Lecture
evt.dir = ">"                        # Écriture

# Processus
spawned_process                      # Nouveau processus créé
proc.name = "bash"                   # Nom du processus
proc.cmdline contains "curl"         # Arguments contiennent "curl"
proc.pname = "python"                # Processus parent

# Fichiers
fd.name = "/etc/passwd"              # Nom de fichier exact
fd.name startswith "/etc/"           # Commence par
fd.name glob "*.php"                 # Pattern glob
fd.size > 1000000                    # Taille > 1MB

# Réseau
evt.type = connect                   # Connexion réseau
fd.sip = "192.168.1.1"              # IP source
fd.sport = 5432                      # Port source

# Conteneurs
container                            # Dans un conteneur
container.name = "ecommerce-dashboard"
```

## 🎓 Ressources

- **Documentation Falco** : https://falco.org/docs/
- **Règles par défaut** : https://github.com/falcosecurity/rules
- **Exemples de règles** : https://falco.org/docs/rules/
- **Loki queries** : https://grafana.com/docs/loki/latest/logql/

## ✅ Checklist de déploiement

- [ ] Falco activé dans `docker-compose.secure.yml`
- [ ] Services démarrés : `docker-compose up -d`
- [ ] Falco logs visibles : `docker logs ecommerce-falco`
- [ ] Règles chargées : 13 groupes de règles
- [ ] Promtail envoie vers Loki
- [ ] Alertes Grafana configurées (25+ règles)
- [ ] Test d'attaque exécuté
- [ ] Détections visibles dans Grafana
- [ ] Dashboard Falco créé

## 🚀 Prochaines étapes

1. **Personnaliser les règles** pour votre application
2. **Configurer les notifications** (email, Slack, PagerDuty)
3. **Créer des playbooks de réponse** aux incidents
4. **Intégrer avec un SIEM** pour corrélation avancée
5. **Automatiser les réponses** aux attaques détectées

---

**Falco est maintenant prêt à détecter toutes les attaques ! 🛡️**
