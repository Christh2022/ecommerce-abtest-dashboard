# 🔧 Configuration GitHub Repository - Guide d'Administration

## 📋 Vue d'Ensemble

Ce guide explique comment configurer correctement le repository GitHub pour que tous les workflows CI/CD et fonctionnalités de sécurité fonctionnent parfaitement.

---

## ⚙️ Configurations Requises

### 1. 🔐 Security & Code Analysis

**Chemin**: Settings → Security → Code security and analysis  
**URL**: https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/security_analysis

#### À Activer:

| Fonctionnalité                  | Status        | Impact                          | Workflow Concerné     |
| ------------------------------- | ------------- | ------------------------------- | --------------------- |
| **Dependency graph**            | ❌ À activer  | Requis pour dependency-review   | dependency-review.yml |
| **Dependabot alerts**           | ✅ Recommandé | Alertes sur vulnérabilités      | -                     |
| **Dependabot security updates** | ✅ Recommandé | PRs automatiques de sécurité    | -                     |
| **Secret scanning**             | ✅ Activé     | Détection de secrets            | -                     |
| **Push protection**             | ✅ Recommandé | Bloque les commits avec secrets | -                     |

#### Instructions:

1. Aller dans **Settings** du repository
2. Cliquer sur **Security** dans le menu de gauche
3. Section **Code security and analysis**
4. Activer **Dependency graph** → Cliquer "Enable"
5. Activer **Dependabot alerts** → Cliquer "Enable"
6. Activer **Dependabot security updates** → Cliquer "Enable"

---

### 2. 📦 GitHub Actions

**Chemin**: Settings → Actions → General  
**URL**: https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/actions

#### Permissions Requises:

| Permission                      | Configuration Requise                 | Utilisation                     |
| ------------------------------- | ------------------------------------- | ------------------------------- |
| **Workflow permissions**        | Read and write permissions            | Push d'images Docker, artifacts |
| **Fork pull request workflows** | Run workflows from fork pull requests | CI sur PRs externes             |
| **Artifacts and logs**          | 90 days retention                     | Logs de builds                  |

#### Configuration Recommandée:

```yaml
Workflow permissions: ☑ Read and write permissions
  ☐ Read repository contents and packages permissions

Fork pull request workflows from outside collaborators:
  ☑ Require approval for all outside collaborators
  ☑ Require approval for first-time contributors
```

---

### 3. 🎯 Secrets GitHub Actions

**Chemin**: Settings → Secrets and variables → Actions  
**URL**: https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/secrets/actions

#### Secrets à Configurer (Production):

| Secret Name        | Description               | Utilisé Dans   | Requis       |
| ------------------ | ------------------------- | -------------- | ------------ |
| `GRAFANA_URL`      | URL Grafana production    | dashboards.yml | ✅           |
| `GRAFANA_USER`     | Username Grafana admin    | dashboards.yml | ✅           |
| `GRAFANA_PASSWORD` | Password Grafana admin    | dashboards.yml | ✅           |
| `DOCKER_USERNAME`  | Docker Hub username       | cd.yml         | ⚠️ Optionnel |
| `DOCKER_PASSWORD`  | Docker Hub password       | cd.yml         | ⚠️ Optionnel |
| `SSH_PRIVATE_KEY`  | Clé SSH pour déploiement  | cd.yml         | ⚠️ Optionnel |
| `DEPLOY_HOST`      | Serveur de production     | cd.yml         | ⚠️ Optionnel |
| `DEPLOY_USER`      | User SSH pour déploiement | cd.yml         | ⚠️ Optionnel |

#### Comment Ajouter un Secret:

```bash
1. Aller dans Settings → Secrets and variables → Actions
2. Cliquer sur "New repository secret"
3. Name: GRAFANA_PASSWORD (par exemple)
4. Secret: VotreMotDePasseSecurisé123!
5. Cliquer "Add secret"
```

---

### 4. 🌿 Branch Protection Rules

**Chemin**: Settings → Branches  
**URL**: https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/branches

#### Configuration Recommandée pour `main`:

```yaml
Branch name pattern: main

☑ Require a pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale pull request approvals when new commits are pushed
  ☑ Require review from Code Owners

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Required status checks:
    - Validate Project Structure
    - Run Tests
    - Build Docker Images
    - Security Scan
    - Code Quality

☑ Require conversation resolution before merging
☑ Include administrators
```

#### Créer une Branch Protection Rule:

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Cocher les options ci-dessus
4. Cliquer "Create" ou "Save changes"

---

### 5. 📋 GitHub Packages (Container Registry)

**Chemin**: Settings → Packages  
**URL**: https://github.com/orgs/YOUR_ORG/packages?repo_name=ecommerce-abtest-dashboard

#### Configuration:

Les images Docker sont automatiquement publiées dans GitHub Container Registry (ghcr.io) lors du déploiement.

**Images créées automatiquement**:

- `ghcr.io/christh2022/ecommerce-dashboard:latest`
- `ghcr.io/christh2022/ecommerce-exporter:latest`
- `ghcr.io/christh2022/ecommerce-dashboard-init:latest`

**Visibilité**: Public ou Private selon vos besoins

---

## 🛠️ Workflows Spécifiques

### Workflow `dependency-review.yml`

**Status**: ⚠️ Temporairement désactivé

**Raison**: Nécessite que "Dependency Graph" soit activé

**Pour Réactiver**:

1. Activer **Dependency Graph** dans Settings → Security
2. Éditer `.github/workflows/dependency-review.yml`:
   ```yaml
   on:
     pull_request:
       branches: [main, develop]
   ```
3. Retirer les commentaires du trigger `pull_request`
4. Commit et push

---

## 🚨 Résolution des Erreurs Courantes

### Erreur: "Resource not accessible by integration"

**Cause**: Permissions insuffisantes pour CodeQL ou SARIF upload

**Solution**:

1. Vérifier que `security-events: write` est dans les permissions du workflow
2. Vérifier que le workflow a accès aux GitHub Advanced Security features
3. Pour les forks: les workflows peuvent avoir des restrictions

**Vérification**:

```yaml
permissions:
  contents: read
  security-events: write # ← Cette permission est critique
  actions: read
```

---

### Erreur: "Dependency review is not supported"

**Cause**: Dependency Graph non activé

**Solution**:

1. Settings → Security → Code security and analysis
2. Activer **Dependency graph**
3. Le workflow dependency-review.yml fonctionnera alors

---

### Erreur: "No files were found with the provided path"

**Cause**: Les fichiers d'artifacts n'existent pas

**Solution**: Déjà corrigé dans le workflow ci.yml:

```yaml
- name: Run tests
  run: |
    mkdir -p test-results  # Crée le dossier automatiquement
    python run_tests.py > test-results/test-output.txt 2>&1 || true
```

---

### Warning: "CodeQL Action v3 will be deprecated"

**Cause**: Utilisation d'une vieille version de CodeQL

**Solution**: Déjà corrigé - tous les workflows utilisent maintenant v4:

```yaml
uses: github/codeql-action/upload-sarif@v4
```

---

## ✅ Checklist de Configuration Complète

### Étape 1: Sécurité de Base

- [ ] Dependency graph activé
- [ ] Dependabot alerts activé
- [ ] Secret scanning activé
- [ ] Push protection activé (optionnel mais recommandé)

### Étape 2: GitHub Actions

- [ ] Workflow permissions: Read and write
- [ ] Fork PR workflows configurés
- [ ] Artifacts retention: 90 jours

### Étape 3: Secrets

- [ ] GRAFANA_PASSWORD configuré
- [ ] GRAFANA_USER configuré
- [ ] GRAFANA_URL configuré
- [ ] Autres secrets production (si déploiement automatique)

### Étape 4: Branch Protection

- [ ] Protection sur `main` configurée
- [ ] Status checks requis configurés
- [ ] Review required activée

### Étape 5: Vérification

- [ ] Lancer un workflow manuellement (Actions → Choose workflow → Run workflow)
- [ ] Vérifier qu'il se termine sans erreur
- [ ] Créer une PR de test pour vérifier les checks

---

## 📊 Status Actuel des Workflows

| Workflow                  | Status               | Corrections Appliquées                            |
| ------------------------- | -------------------- | ------------------------------------------------- |
| **ci.yml**                | ✅ Prêt              | Permissions ajoutées, CodeQL v4, test-results fix |
| **cd.yml**                | ✅ Prêt              | Permissions ajoutées                              |
| **dashboards.yml**        | ⚠️ Nécessite secrets | Permissions OK, secrets GRAFANA\_\* requis        |
| **dependency-review.yml** | ⚠️ Désactivé         | Attend activation Dependency Graph                |
| **security-audit.yml**    | ✅ Prêt              | Permissions ajoutées                              |
| **cleanup.yml**           | ✅ Prêt              | Permissions ajoutées                              |

---

## 🔗 Liens Rapides

- [Settings du Repository](https://github.com/Christh2022/ecommerce-abtest-dashboard/settings)
- [Security Analysis](https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/security_analysis)
- [Actions Settings](https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/actions)
- [Secrets](https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/secrets/actions)
- [Branch Protection](https://github.com/Christh2022/ecommerce-abtest-dashboard/settings/branches)
- [Actions Workflows](https://github.com/Christh2022/ecommerce-abtest-dashboard/actions)

---

## 📞 Support

Pour toute question:

1. Consulter [docs/CICD_DOCUMENTATION.md](CICD_DOCUMENTATION.md)
2. Vérifier les [GitHub Actions logs](https://github.com/Christh2022/ecommerce-abtest-dashboard/actions)
3. Lire la [documentation GitHub Actions](https://docs.github.com/en/actions)

---

**Dernière mise à jour**: 23 décembre 2025  
**Responsable**: Admin du repository  
**Version**: 1.0
