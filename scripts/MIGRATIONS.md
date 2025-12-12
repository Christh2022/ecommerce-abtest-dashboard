# Database Migrations

Scripts de migration et d'initialisation de la base de données PostgreSQL.

## 📁 Structure

```
scripts/
├── migrations/              # Migration files versionnées
│   ├── 001_initial_schema.sql
│   ├── 002_indexes_and_views.sql
│   ├── 003_functions_and_triggers.sql
│   └── 004_seed_data.sql
├── run_migrations.py        # Script Python pour exécuter les migrations
├── init_db.sql             # Script d'initialisation complet (Docker)
└── import_data_to_postgres.py
```

## 🚀 Utilisation

### Option 1: Docker Compose (Initialisation automatique)

Le script `init_db.sql` est automatiquement exécuté lors du premier démarrage du conteneur PostgreSQL:

```bash
docker-compose up -d postgres
```

### Option 2: Migration manuelle avec Python

```bash
# Voir les migrations en attente
python scripts/run_migrations.py --dry-run

# Appliquer toutes les migrations
python scripts/run_migrations.py

# Voir le statut des migrations
python scripts/run_migrations.py --status
```

### Option 3: Exécution manuelle SQL

```bash
# Se connecter à PostgreSQL
docker exec -it ecommerce-postgres psql -U dashuser -d ecommerce_db

# Exécuter les migrations dans l'ordre
\i /scripts/migrations/001_initial_schema.sql
\i /scripts/migrations/002_indexes_and_views.sql
\i /scripts/migrations/003_functions_and_triggers.sql
\i /scripts/migrations/004_seed_data.sql
```

## 📋 Détail des Migrations

### Migration 001: Initial Schema

- Création de toutes les tables principales
- Tables d'analytics (daily_metrics, user_behavior, products_summary)
- Tables A/B testing (ab_test_scenarios, ab_test_results)
- Tables de monitoring (dashboard_logs, query_performance)
- Table de tracking des migrations (schema_migrations)

### Migration 002: Indexes and Views

- **15+ indexes** pour optimiser les performances
- **3 vues** SQL pour requêtes courantes:
  - `v_daily_kpis`: KPIs quotidiens agrégés
  - `v_top_products`: Produits les plus performants
  - `v_ab_test_summary`: Résumé des tests A/B

### Migration 003: Functions and Triggers

- **Fonctions utilitaires**:
  - `update_updated_at_column()`: MAJ automatique des timestamps
  - `calculate_conversion_rate()`: Calcul du taux de conversion
  - `calculate_aov()`: Calcul de l'AOV (Average Order Value)
- **Triggers** sur daily_metrics, products_summary, ab_test_scenarios

### Migration 004: Seed Data

- Données de test pour ab_test_scenarios (5 scénarios)
- Permissions pour l'utilisateur dashuser

## 🔧 Configuration

Variables d'environnement pour `run_migrations.py`:

```bash
POSTGRES_DB=ecommerce_db
POSTGRES_USER=dashuser
POSTGRES_PASSWORD=dashpass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## 📊 Tables Créées

| Table             | Description                        | Lignes estimées |
| ----------------- | ---------------------------------- | --------------- |
| daily_metrics     | Métriques quotidiennes agrégées    | ~365/an         |
| user_behavior     | Comportement utilisateur détaillé  | ~10K+/jour      |
| products_summary  | Performance des produits           | ~500-1000       |
| traffic_sources   | Analyse des sources de trafic      | ~50/jour        |
| ab_test_scenarios | Scénarios de test A/B              | ~20-50          |
| ab_test_results   | Résultats quotidiens des tests A/B | ~1000+          |
| funnel_stages     | Étapes du funnel de conversion     | ~100/jour       |
| dashboard_logs    | Logs de l'application              | ~1000+/jour     |
| query_performance | Performance des requêtes           | ~500+/jour      |
| schema_migrations | Historique des migrations          | Variable        |

## 🛠️ Maintenance

### Ajouter une nouvelle migration

1. Créer un nouveau fichier: `005_description.sql`
2. Commencer par un commentaire descriptif
3. Terminer par l'enregistrement de la migration:

```sql
INSERT INTO schema_migrations (version, description)
VALUES ('005', 'Description de la migration')
ON CONFLICT (version) DO NOTHING;
```

### Vérifier l'état de la base

```bash
# Via Python
python scripts/run_migrations.py --status

# Via SQL
docker exec -it ecommerce-postgres psql -U dashuser -d ecommerce_db \
  -c "SELECT * FROM schema_migrations ORDER BY version;"
```

### Backup avant migration

```bash
docker exec ecommerce-postgres pg_dump -U dashuser ecommerce_db > backup_$(date +%Y%m%d).sql
```

## ⚠️ Notes Importantes

- Les migrations sont **idempotentes** (peuvent être réexécutées sans erreur)
- L'ordre d'exécution est important (001 → 002 → 003 → 004)
- Le script `run_migrations.py` gère automatiquement l'ordre
- Les migrations ne sont pas réversibles automatiquement (créer une migration inverse si nécessaire)

## 🔍 Dépannage

### Problème de connexion

```bash
# Vérifier que PostgreSQL est démarré
docker ps | grep postgres

# Vérifier les logs
docker logs ecommerce-postgres
```

### Migration échouée

```bash
# Voir la dernière migration appliquée
python scripts/run_migrations.py --status

# Se connecter manuellement pour corriger
docker exec -it ecommerce-postgres psql -U dashuser -d ecommerce_db
```

### Réinitialiser complètement

```bash
# Arrêter et supprimer les volumes
docker-compose down -v

# Redémarrer (réinitialisation complète)
docker-compose up -d
```

## 📚 Ressources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Docker Compose avec PostgreSQL](https://docs.docker.com/samples/postgres/)
