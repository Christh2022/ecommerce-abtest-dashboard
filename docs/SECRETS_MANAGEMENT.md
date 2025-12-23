# 🔐 Guide de Gestion des Secrets

## ⚠️ Problème Détecté

GitGuardian a détecté des secrets hardcodés dans le code. Cette documentation explique comment gérer correctement les secrets.

---

## 🚨 Secrets Détectés (Historique Git)

Les fichiers suivants contenaient des secrets hardcodés dans l'historique Git:

| Fichier                              | Type de Secret       | Status      | Commit  |
| ------------------------------------ | -------------------- | ----------- | ------- |
| `test_auth.py`                       | Username/Password    | ✅ Supprimé | cfc1b8d |
| `import_security_dashboard.py`       | Authentication Tuple | ✅ Supprimé | cfc1b8d |
| `scripts/init_grafana_dashboards.sh` | Generic Password     | ✅ Corrigé  | 3656fb6 |
| `security_attack_suite.py`           | Generic Password     | ✅ Supprimé | 3656fb6 |

---

## ✅ Actions Correctives Appliquées

### 1. Nettoyage des Secrets Hardcodés

**Avant** (scripts/init_grafana_dashboards.sh):

```bash
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin123}"  # ❌ Hardcodé
```

**Après**:

```bash
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-changeme}"  # ✅ Placeholder générique
```

### 2. Configuration via Variables d'Environnement

Tous les secrets sont maintenant dans `.env` (non versionné):

```env
# .env (à créer depuis .env.example)
GRAFANA_PASSWORD=VotreMotDePasseSecurisé123!
POSTGRES_PASSWORD=MotDePasseBDDSecurisé456!
GF_SECURITY_ADMIN_PASSWORD=AdminGrafanaSecurisé789!
```

### 3. Fichiers Supprimés

Les fichiers de test contenant des credentials ont été supprimés:

- ✅ `test_auth.py` - Contenait username/password de test
- ✅ `import_security_dashboard.py` - Contenait tuple d'authentification
- ✅ `security_attack_suite.py` - Contenait passwords de test

---

## 🛡️ Bonnes Pratiques

### 1. Utiliser des Variables d'Environnement

#### ✅ BON

```python
import os

# Lire depuis l'environnement
grafana_password = os.getenv('GRAFANA_PASSWORD')
db_password = os.getenv('POSTGRES_PASSWORD')

if not grafana_password:
    raise ValueError("GRAFANA_PASSWORD environment variable required")
```

#### ❌ MAUVAIS

```python
# NE JAMAIS faire ça!
grafana_password = "admin123"  # ❌ Hardcodé
db_password = "password123"     # ❌ Hardcodé
```

### 2. Fichier .env pour le Développement Local

```bash
# 1. Copier l'exemple
cp .env.example .env

# 2. Éditer avec vos vrais secrets
nano .env

# 3. Ne JAMAIS commiter .env
git add .env  # ❌ NE JAMAIS FAIRE
```

**Vérifier .gitignore**:

```gitignore
# Secrets
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

### 3. Docker Compose avec Secrets

#### Option 1: Fichier .env (développement)

```yaml
# docker-compose.yml
services:
  grafana:
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
```

#### Option 2: Docker Secrets (production)

```yaml
# docker-compose.yml
services:
  grafana:
    secrets:
      - grafana_admin_password
    environment:
      - GF_SECURITY_ADMIN_PASSWORD_FILE=/run/secrets/grafana_admin_password

secrets:
  grafana_admin_password:
    external: true
```

### 4. Kubernetes Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: grafana-secrets
type: Opaque
data:
  admin-password: <base64-encoded-password>
```

```bash
# Créer le secret depuis la ligne de commande
kubectl create secret generic grafana-secrets \
  --from-literal=admin-password='VotreMotDePasse' \
  -n ecommerce-monitoring
```

### 5. GitHub Actions Secrets

Pour les workflows CI/CD:

1. Aller dans **Settings** → **Secrets and variables** → **Actions**
2. Ajouter les secrets:
   - `GRAFANA_PASSWORD`
   - `POSTGRES_PASSWORD`
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - etc.

Usage dans workflow:

```yaml
- name: Deploy
  env:
    GRAFANA_PASSWORD: ${{ secrets.GRAFANA_PASSWORD }}
  run: ./deploy.sh
```

---

## 🔍 Détection Automatique des Secrets

### 1. Pre-commit Hook

Installation:

```bash
# Installer pre-commit
pip install pre-commit

# Installer les hooks
pre-commit install

# Tester
pre-commit run --all-files
```

Le hook vérifie automatiquement:

- ✅ Secrets avec detect-secrets
- ✅ Clés privées
- ✅ Patterns de credentials
- ✅ Tokens API

### 2. GitGuardian (Déjà Configuré)

GitGuardian scanne automatiquement les commits et PRs pour détecter:

- Passwords
- API keys
- Tokens
- Private keys
- Certificates

### 3. Scan Manuel

```bash
# Avec detect-secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline

# Avec gitleaks
docker run -v $(pwd):/path zricethezav/gitleaks:latest detect --source /path

# Avec truffleHog
docker run --rm -v $(pwd):/repo trufflesecurity/trufflehog:latest git file:///repo
```

---

## 🔧 Configuration Recommandée

### pyproject.toml (Bandit)

```toml
[tool.bandit]
exclude_dirs = ["/tests", "/build", "/dist"]
tests = ["B201", "B301", "B302", "B303", "B304", "B305", "B306", "B307"]
skips = ["B101", "B601"]
```

### .secrets.baseline

```bash
# Générer le baseline (ignore les faux positifs connus)
detect-secrets scan --baseline .secrets.baseline

# Audit du baseline
detect-secrets audit .secrets.baseline
```

---

## 📋 Checklist de Sécurité

### Avant Chaque Commit

- [ ] Pas de passwords hardcodés
- [ ] Pas de clés API dans le code
- [ ] Pas de tokens exposés
- [ ] `.env` non commité
- [ ] Pre-commit hooks passent
- [ ] Variables d'environnement documentées dans `.env.example`

### Configuration Production

- [ ] Secrets dans HashiCorp Vault / AWS Secrets Manager
- [ ] Rotation automatique des secrets
- [ ] Secrets chiffrés au repos
- [ ] Logs ne contiennent pas de secrets
- [ ] HTTPS/TLS pour toutes les communications
- [ ] Principes du moindre privilège

### Revue de Code

- [ ] Vérifier les nouveaux fichiers
- [ ] Scanner avec detect-secrets
- [ ] Vérifier .env.example (pas de vrais secrets)
- [ ] GitGuardian ne détecte rien

---

## 🚀 Migration des Secrets Existants

### 1. Identifier les Secrets

```bash
# Rechercher dans le code
grep -r "password\|secret\|token\|api_key" . --include="*.py" --include="*.sh"

# Avec detect-secrets
detect-secrets scan
```

### 2. Extraire vers .env

```bash
# Créer .env depuis .env.example
cp .env.example .env

# Ajouter vos secrets réels
echo "GRAFANA_PASSWORD=$(openssl rand -base64 32)" >> .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env
```

### 3. Mettre à Jour le Code

```python
# Avant
GRAFANA_PASSWORD = "admin123"

# Après
import os
GRAFANA_PASSWORD = os.getenv("GRAFANA_PASSWORD")
```

### 4. Nettoyer l'Historique Git (Optionnel mais Recommandé)

⚠️ **ATTENTION**: Récrire l'historique Git est une opération sensible!

```bash
# Avec git-filter-repo (recommandé)
pip install git-filter-repo
git filter-repo --invert-paths --path test_auth.py

# Ou avec BFG Repo-Cleaner
java -jar bfg.jar --delete-files 'test_auth.py' .

# Force push (coordonner avec l'équipe!)
git push --force --all
```

---

## 📞 Ressources

### Outils de Détection

- [detect-secrets](https://github.com/Yelp/detect-secrets) - Yelp
- [gitleaks](https://github.com/gitleaks/gitleaks) - Scan de repos
- [truffleHog](https://github.com/trufflesecurity/trufflehog) - Détection avancée
- [GitGuardian](https://www.gitguardian.com/) - Service cloud

### Gestionnaires de Secrets

- [HashiCorp Vault](https://www.vaultproject.io/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)
- [Google Secret Manager](https://cloud.google.com/secret-manager)

### Documentation

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secrets Best Practices](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)

---

## 🆘 En Cas de Fuite de Secret

### Actions Immédiates

1. **Révoquer** le secret immédiatement
2. **Générer** un nouveau secret
3. **Mettre à jour** tous les services qui l'utilisent
4. **Notifier** l'équipe de sécurité
5. **Auditer** les accès récents
6. **Documenter** l'incident

### Contacts

- **Équipe Sécurité**: security@example.com
- **GitGuardian Support**: https://www.gitguardian.com/support
- **Incident Response**: [SECURITY.md](../SECURITY.md)

---

## ✅ Status Actuel

- ✅ Secrets hardcodés supprimés du code actif
- ✅ `.env.example` avec placeholders sécurisés
- ✅ Pre-commit hooks configurés
- ✅ GitGuardian activé sur le repo
- ✅ CI/CD utilise GitHub Secrets
- ✅ Documentation complète

**Dernière mise à jour**: 23 décembre 2025
**Statut**: ✅ Sécurisé
