# 🚀 CI/CD Pipeline - Documentation

## 📋 Vue d'Ensemble

Le projet utilise **GitHub Actions** pour automatiser les builds, tests, déploiements et maintenance.

## 🔄 Workflows Disponibles

### 1. **CI - Build and Test** ([ci.yml](.github/workflows/ci.yml))

**Déclenchement**:

- Push sur `main`, `develop`, ou `feature/*`
- Pull requests vers `main` ou `develop`

**Jobs**:

1. **validate** - Validation de la structure du projet
   - ✅ Validation avec `validate_dashboard_organization.py`
   - ✅ Vérification de la syntaxe Python
2. **test** - Exécution des tests
   - ✅ Tests unitaires et d'intégration
   - ✅ Base de données PostgreSQL de test
   - ✅ Upload des résultats
3. **build-docker** - Build des images Docker
   - ✅ Build de `dashboard`
   - ✅ Build de `exporter`
   - ✅ Build de `dashboard-init`
   - ✅ Cache optimisé
4. **security-scan** - Scan de sécurité
   - ✅ Trivy vulnerability scanner
   - ✅ Upload vers GitHub Security
5. **lint** - Qualité du code
   - ✅ Flake8 (erreurs syntaxe)
   - ✅ Black (formatage)
   - ✅ Isort (imports)

---

### 2. **CD - Deploy** (DÉSACTIVÉ)

**Status**: ⚠️ **Workflow désactivé** - Renommé en `cd.yml.disabled`

**Raison**: Déploiement en production géré manuellement pour l'instant.

**Pour réactiver**: 
```bash
git mv .github/workflows/cd.yml.disabled .github/workflows/cd.yml
```

---

### 3. **Create Grafana Dashboards** ([dashboards.yml](.github/workflows/dashboards.yml))

**Déclenchement**:

- Manuel via `workflow_dispatch` uniquement

**Jobs**:

- 📊 Création automatique des 10 dashboards Grafana
- ✅ Vérification des dashboards créés
- ⚠️ Nécessite secrets GRAFANA_URL, GRAFANA_USER, GRAFANA_PASSWORD

---

### 4. **Dependency Review** ([dependency-review.yml](.github/workflows/dependency-review.yml))

**Déclenchement**:

- Pull requests vers `main` ou `develop`

**Jobs**:

- 🔍 Revue des dépendances
- 🛡️ Check de sécurité avec `safety`
- ⚠️ Fail si vulnérabilités modérées ou critiques

---

### 5. **Cleanup** ([cleanup.yml](.github/workflows/cleanup.yml))

**Déclenchement**:

- Hebdomadaire (Dimanche à 2h)
- Manuel via `workflow_dispatch`

**Jobs**:

- 🧹 Suppression des artifacts > 30 jours
- 🧹 Suppression des images Docker > 30 jours
- 💾 Conservation des 5 plus récents

---

## 🔐 Secrets Requis

### GitHub Secrets à Configurer

| Secret             | Description                | Requis Pour           |
| ------------------ | -------------------------- | --------------------- |
| `GITHUB_TOKEN`     | Token GitHub (auto)        | CD, Cleanup           |
| `KUBECONFIG`       | Config Kubernetes (base64) | Deploy K8s            |
| `DEPLOY_HOST`      | Serveur de déploiement     | Deploy Docker Compose |
| `DEPLOY_USER`      | User SSH                   | Deploy Docker Compose |
| `DEPLOY_SSH_KEY`   | Clé SSH privée             | Deploy Docker Compose |
| `GRAFANA_URL`      | URL Grafana                | Dashboards            |
| `GRAFANA_USER`     | Username Grafana           | Dashboards            |
| `GRAFANA_PASSWORD` | Password Grafana           | Dashboards            |

### Configuration des Secrets

```bash
# Via GitHub CLI
gh secret set KUBECONFIG < ~/.kube/config | base64
gh secret set DEPLOY_HOST --body "your-server.com"
gh secret set DEPLOY_USER --body "deploy"
gh secret set DEPLOY_SSH_KEY < ~/.ssh/id_rsa
gh secret set GRAFANA_URL --body "http://grafana.example.com"
gh secret set GRAFANA_USER --body "admin"
gh secret set GRAFANA_PASSWORD --body "your-password"
```

---

## 🎯 Stratégie de Branches

### Branch Protection Rules

**`main`**:

- ✅ Require PR reviews (1 approbation)
- ✅ Require status checks (CI doit passer)
- ✅ Require up-to-date branches
- ✅ Include administrators
- ❌ Allow force pushes
- ❌ Allow deletions

**`develop`**:

- ✅ Require status checks (CI doit passer)
- ✅ Require up-to-date branches
- ✅ Allow force pushes (pour rebase)

### Workflow Branches

```
main (production)
  ↑
  PR + CI/CD
  ↑
develop (staging)
  ↑
  PR + CI
  ↑
feature/* (développement)
```

---

## 📦 Container Registry

### Images Publiées

Les images sont publiées sur **GitHub Container Registry**:

```
ghcr.io/christh2022/ecommerce-dashboard:latest
ghcr.io/christh2022/ecommerce-exporter:latest
ghcr.io/christh2022/ecommerce-dashboard-init:latest
```

### Tags

- `latest` - Dernière version de `main`
- `develop` - Dernière version de `develop`
- `v1.0.0` - Version semver
- `sha-abc123` - SHA du commit

### Pull des Images

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull
docker pull ghcr.io/christh2022/ecommerce-dashboard:latest
docker pull ghcr.io/christh2022/ecommerce-exporter:latest
docker pull ghcr.io/christh2022/ecommerce-dashboard-init:latest
```

---

## 🚀 Déploiements

### Déploiement Automatique

**Staging** (develop):

- ✅ CI automatique sur chaque push
- ✅ Déploiement Docker Compose automatique

**Production** (main):

- ✅ CI automatique sur chaque push
- ✅ Build et push des images
- ✅ Déploiement Kubernetes automatique
- ✅ Création de release pour les tags

### Déploiement Manuel

```bash
# Via GitHub Actions UI
# Actions → CD - Deploy → Run workflow
# Sélectionner l'environnement: staging ou production
```

---

## 🧪 Tests Locaux

### Tester le CI Localement

Utiliser [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
choco install act  # Windows

# Run CI workflow
act -j validate
act -j test
act -j build-docker

# Run all CI
act push
```

### Tester les Builds Docker

```bash
# Build toutes les images
docker-compose -f docker-compose.secure.yml build

# Test individual builds
docker build -f docker/Dockerfile -t test-dashboard .
docker build -f docker/Dockerfile.exporter -t test-exporter .
docker build -f docker/Dockerfile.dashboard-init -t test-init .
```

---

## 📊 Monitoring des Workflows

### Status Badges

Ajouter à votre README:

```markdown
![CI](https://github.com/Christh2022/ecommerce-abtest-dashboard/workflows/CI%20-%20Build%20and%20Test/badge.svg)
![CD](https://github.com/Christh2022/ecommerce-abtest-dashboard/workflows/CD%20-%20Deploy/badge.svg)
```

### Viewing Workflow Runs

```bash
# Via GitHub CLI
gh run list
gh run view <run-id>
gh run watch <run-id>

# Voir les logs
gh run view <run-id> --log
```

---

## 🔧 Maintenance

### Dependabot

Configuration dans [.github/dependabot.yml](.github/dependabot.yml):

- ✅ Updates Python packages hebdomadaires
- ✅ Updates Docker images hebdomadaires
- ✅ Updates GitHub Actions hebdomadaires
- ✅ Auto-assignment aux reviewers
- ✅ Labels automatiques

### Code Owners

Configuration dans [.github/CODEOWNERS](.github/CODEOWNERS):

- ✅ Review automatique sur les PRs
- ✅ Protection par composant

---

## 🐛 Troubleshooting

### Workflow Fails

```bash
# Check logs
gh run view <run-id> --log

# Re-run failed jobs
gh run rerun <run-id>

# Re-run specific job
gh run rerun <run-id> --job <job-id>
```

### Build Failures

1. Vérifier la syntaxe:

   ```bash
   python -m py_compile dashboard/app.py
   ```

2. Tester localement:

   ```bash
   python run_tests.py
   python tools/validate_dashboard_organization.py
   ```

3. Vérifier les dépendances:
   ```bash
   pip install -r requirements.txt
   safety check
   ```

### Deploy Failures

1. Vérifier les secrets:

   ```bash
   gh secret list
   ```

2. Tester la connexion SSH:

   ```bash
   ssh $DEPLOY_USER@$DEPLOY_HOST
   ```

3. Vérifier Kubernetes:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

---

## 📚 Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [kubectl Setup](https://github.com/azure/setup-kubectl)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)

---

## ✅ Checklist de Configuration

- [ ] Configurer les secrets GitHub
- [ ] Configurer les branch protection rules
- [ ] Tester le workflow CI localement
- [ ] Vérifier le déploiement staging
- [ ] Configurer Dependabot
- [ ] Ajouter les status badges au README
- [ ] Documenter le processus de release
- [ ] Former l'équipe aux workflows

---

**Dernière mise à jour**: 23 Décembre 2025  
**Version**: 1.0  
**Statut**: ✅ Production Ready
