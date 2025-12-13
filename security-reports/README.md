# Security Reports Directory

Ce dossier contient les rapports d'audit de sécurité générés par pip-audit.

## Fichiers

- `AUDIT_REPORT.md` - Rapport détaillé des vulnérabilités et corrections
- `audit-YYYYMMDD.json` - Rapports JSON horodatés (générés automatiquement)

## Génération des Rapports

### Manuellement

```bash
# Audit avec rapport JSON
pip-audit --requirement ../requirements.txt --format json --output audit-$(date +%Y%m%d).json
```

### Via Script

```bash
# Depuis la racine du projet
./scripts/audit_dependencies.sh --json --output security-reports/audit.json
```

### Via Docker

```bash
# Les rapports sont automatiquement générés dans ce dossier
docker-compose -f docker-compose.security.yml up
```

## Rétention

- Les rapports JSON sont conservés localement
- Les rapports GitHub Actions sont conservés 30 jours
- Nettoyer les anciens rapports manuellement si nécessaire

## .gitignore

Les rapports JSON peuvent être ajoutés à .gitignore s'ils contiennent des informations sensibles:

```
# .gitignore
security-reports/*.json
!security-reports/AUDIT_REPORT.md
```
