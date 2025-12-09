# Guide de déploiement

## Déploiement local avec Docker

### Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/Christh2022/ecommerce-abtest-dashboard.git
cd ecommerce-abtest-dashboard

# 2. Configurer l'environnement
cp .env.example .env

# 3. Lancer les services
docker-compose up -d

# 4. Vérifier le statut
docker-compose ps

# 5. Initialiser la base de données
docker-compose exec dash-app python scripts/setup_db.py
docker-compose exec dash-app python scripts/load_data.py
```

### Accès aux services

- Dashboard: http://localhost:8050
- Grafana: http://localhost:3000
- PostgreSQL: localhost:5432

## Déploiement en production

### Configuration recommandée

- 2 CPU cores
- 8GB RAM
- 50GB stockage
- Réseau privé

### Sécurité

1. Changer tous les mots de passe par défaut
2. Configurer SSL/TLS
3. Restreindre les ports exposés
4. Activer les sauvegardes automatiques
5. Configurer les alertes Grafana

### Sauvegarde

```bash
# Sauvegarder la base de données
docker-compose exec postgres pg_dump -U admin ecommerce_db > backup.sql

# Restaurer
docker-compose exec -T postgres psql -U admin ecommerce_db < backup.sql
```

## Scaling

Pour scaler l'application :

```bash
docker-compose up -d --scale dash-app=3
```

Plus de détails à venir...
