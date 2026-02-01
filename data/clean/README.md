# Données nettoyées - RetailRocket Dataset

## ️ Fichiers non inclus dans Git

Les fichiers CSV nettoyés ne sont pas inclus dans le repository Git car ils sont trop volumineux (536+ MB au total).

##  Fichiers disponibles après preprocessing

| Fichier | Lignes | Taille | Description |
|---------|--------|--------|-------------|
| `users.csv` | 1,407,580 | 83.9 MB | Profils utilisateurs avec segments |
| `products.csv` | 235,061 | 327.3 MB | Catalogue produits avec statistiques |
| `sessions.csv` | 1,649,534 | 123.6 MB | Sessions de navigation |
| `transactions.csv` | 22,457 | 1.8 MB | Transactions avec montants |

**Total**: ~536 MB

##  Comment regénérer les données

### Option 1: Télécharger et préprocesser (recommandé)

```bash
# 1. Télécharger le dataset depuis Kaggle
python scripts/download_dataset.py

# 2. Préprocesser les données
python scripts/preprocess_retailrocket.py

# 3. Les fichiers seront créés dans data/clean/
```

**Durée estimée**: 5-10 minutes

### Option 2: Charger directement en base de données

Si vous voulez simplement utiliser les données dans PostgreSQL:

```bash
# 1. Démarrer PostgreSQL
docker-compose up -d postgres

# 2. Télécharger et préprocesser
python scripts/download_dataset.py
python scripts/preprocess_retailrocket.py

# 3. Initialiser et charger en base
python scripts/setup_db.py
python scripts/load_retailrocket_to_db.py
```

##  Prérequis

### Pour télécharger depuis Kaggle

1. **Compte Kaggle** avec API Token configuré
   ```bash
   # Télécharger kaggle.json depuis kaggle.com
   # Placer dans ~/.kaggle/ (Linux/Mac) ou C:\Users\<username>\.kaggle\ (Windows)
   ```

2. **Dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

##  Alternative: Archive compressée

Si vous avez déjà les fichiers CSV, vous pouvez créer une archive compressée:

```bash
# Compresser
python scripts/compress_data.py

# Extraire plus tard
python scripts/compress_data.py extract
```

**Note**: L'archive ZIP résultante fait ~82 MB.

##  Source des données

Dataset RetailRocket original disponible sur Kaggle:
- https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

##  Remarques

- Les fichiers bruts (`data/raw/*.csv`) sont également exclus de Git (taille totale: ~942 MB)
- Assurez-vous d'avoir au moins 2 GB d'espace disque libre
- Le preprocessing utilise environ 4 GB de RAM pendant l'exécution

##  Documentation

Pour plus de détails, consultez:
- [DATASET.md](../../docs/DATASET.md) - Documentation complète du dataset
- [QUICKSTART_ISSUE1.md](../../docs/QUICKSTART_ISSUE1.md) - Guide de démarrage
