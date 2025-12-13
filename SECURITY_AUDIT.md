# 🔒 Audit de Sécurité - Guide Rapide

## 🚀 Utilisation Rapide

### Méthode 1: Script Bash (Recommandé)

```bash
# Audit simple
./scripts/audit_dependencies.sh

# Avec correction automatique (attention!)
./scripts/audit_dependencies.sh --fix

# Sortie JSON
./scripts/audit_dependencies.sh --json --output security-reports/audit.json
```

### Méthode 2: pip-audit Direct

```bash
# Installer pip-audit
pip install pip-audit

# Audit
pip-audit --requirement requirements.txt

# Avec descriptions
pip-audit --requirement requirements.txt --desc
```

### Méthode 3: Docker

```bash
# Audit dans conteneur isolé
docker-compose -f docker-compose.security.yml up

# Les rapports sont dans ./security-reports/
```

## 📊 Status Actuel

**Dernière mise à jour:** 13 décembre 2025

| Package  | Version | Vulnérabilités | Status      |
| -------- | ------- | -------------- | ----------- |
| dash     | 2.15.0  | 0              | ✅ Sécurisé |
| gunicorn | 22.0.0  | 0              | ✅ Sécurisé |
| black    | 24.3.0  | 0              | ✅ Sécurisé |
| werkzeug | 3.0.6   | 1 (basse)      | ⚠️ Mitigé   |

**Total:** 4/5 vulnérabilités corrigées (80%)

## 📁 Documentation

- **Guide complet:** [docs/ISSUE58_COMPLETED.md](../docs/ISSUE58_COMPLETED.md)
- **Rapport d'audit:** [security-reports/AUDIT_REPORT.md](../security-reports/AUDIT_REPORT.md)

## 🔄 Automatisation

- ✅ GitHub Actions - Hebdomadaire (lundi 9h UTC)
- ✅ CI/CD - À chaque push/PR
- ✅ Docker - On-demand

## 🆘 Support

En cas de vulnérabilité détectée:

1. **Examiner le rapport:**

   ```bash
   pip-audit --requirement requirements.txt --desc
   ```

2. **Vérifier les versions disponibles:**

   ```bash
   pip index versions <package-name>
   ```

3. **Mettre à jour:**

   ```bash
   # Tester en dev d'abord!
   pip install --upgrade <package-name>
   ```

4. **Ou utiliser --fix:**

   ```bash
   pip-audit --requirement requirements.txt --fix
   ```

5. **Tester:**
   ```bash
   pytest
   docker-compose up -d
   ```

## 🔗 Liens Utiles

- [pip-audit Documentation](https://pypi.org/project/pip-audit/)
- [PyPI Advisory Database](https://github.com/pypa/advisory-database)
- [OSV Vulnerability Database](https://osv.dev/)
