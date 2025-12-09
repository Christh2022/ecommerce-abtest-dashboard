# 🚀 Guide de démarrage rapide - Issue #1

## Téléchargement et intégration du dataset RetailRocket

Ce guide vous accompagne pour l'Issue #1 du Milestone 1 : Télécharger et intégrer le dataset RetailRocket.

---

## 📋 Prérequis

1. **Compte Kaggle**

   - Créer un compte sur [kaggle.com](https://www.kaggle.com)
   - Aller dans `Account` > `API` > `Create New API Token`
   - Télécharger le fichier `kaggle.json`

2. **Configuration Kaggle API**

   ```bash
   # Windows
   mkdir %USERPROFILE%\.kaggle
   copy kaggle.json %USERPROFILE%\.kaggle\

   # Linux/Mac
   mkdir -p ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

3. **Environnement Python**
   ```bash
   # Installer les dépendances
   pip install -r requirements.txt
   ```

---

## 🎯 Étapes d'exécution

### Étape 1: Télécharger le dataset

```bash
python scripts/download_dataset.py
```

**Ce script va**:

- ✓ Vérifier que Kaggle API est installé
- ✓ Vérifier les credentials Kaggle
- ✓ Télécharger le dataset RetailRocket (~170 MB)
- ✓ Extraire les fichiers dans `data/raw/`
- ✓ Vérifier l'intégrité des fichiers

**Fichiers téléchargés**:

- `events.csv` - Événements utilisateur (~2.7M lignes)
- `item_properties_part1.csv` - Propriétés produits (partie 1)
- `item_properties_part2.csv` - Propriétés produits (partie 2)
- `category_tree.csv` - Arborescence catégories

**Durée estimée**: 2-5 minutes (selon votre connexion)

---

### Étape 2: Préprocesser les données

```bash
python scripts/preprocess_retailrocket.py
```

**Ce script va**:

- ✓ Charger les données brutes
- ✓ Analyser les événements (views, addtocart, transactions)
- ✓ Créer des tables structurées:
  - `users.csv` - Profils utilisateurs avec segments
  - `products.csv` - Catalogue produits avec stats
  - `sessions.csv` - Sessions de navigation
  - `transactions.csv` - Transactions avec montants simulés
- ✓ Générer des statistiques descriptives
- ✓ Sauvegarder dans `data/clean/`

**Durée estimée**: 3-8 minutes (selon votre machine)

---

### Étape 3: Charger en base de données

```bash
# Démarrer PostgreSQL
docker-compose up -d postgres

# Attendre que PostgreSQL soit prêt (10-20 secondes)
docker-compose ps

# Initialiser les tables
python scripts/setup_db.py

# Charger les données RetailRocket
python scripts/load_retailrocket_to_db.py
```

**Ce script va**:

- ✓ Se connecter à PostgreSQL
- ✓ Vider les tables existantes
- ✓ Charger les utilisateurs (~1.4M)
- ✓ Charger les produits (~100K premiers)
- ✓ Charger les sessions
- ✓ Charger les transactions (~22K)
- ✓ Créer les index pour optimiser les performances

**Durée estimée**: 5-15 minutes

---

## ✅ Vérification

### Vérifier les fichiers téléchargés

```bash
# Windows PowerShell
Get-ChildItem data\raw\

# Bash
ls -lh data/raw/
```

**Vous devriez voir**:

```
events.csv                    (~340 MB)
item_properties_part1.csv     (~70 MB)
item_properties_part2.csv     (~65 MB)
category_tree.csv             (~1 MB)
```

### Vérifier les données nettoyées

```bash
# Windows PowerShell
Get-ChildItem data\clean\

# Bash
ls -lh data/clean/
```

**Vous devriez voir**:

```
users.csv
products.csv
sessions.csv
transactions.csv
```

### Vérifier la base de données

```bash
# Se connecter à PostgreSQL
docker-compose exec postgres psql -U admin -d ecommerce_db

# Compter les enregistrements
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sessions', COUNT(*) FROM sessions
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions;

# Quitter
\q
```

---

## 📊 Statistiques attendues

Après le chargement complet, vous devriez avoir:

| Table                 | Enregistrements attendus |
| --------------------- | ------------------------ |
| **users**             | ~1,407,000               |
| **products**          | ~100,000 (limité)        |
| **sessions**          | ~800,000                 |
| **transactions**      | ~22,000                  |
| **transaction_items** | ~22,000                  |

**KPIs du dataset**:

- Taux de conversion global: ~0.8%
- CA total (simulé): ~500,000€
- Utilisateurs avec achats: ~1.5%
- Produits avec ventes: ~5%

---

## 🐛 Dépannage

### Problème: Kaggle API non configurée

**Erreur**: `OSError: Could not find kaggle.json`

**Solution**:

1. Télécharger `kaggle.json` depuis votre compte Kaggle
2. Le placer dans `~/.kaggle/` (Linux/Mac) ou `C:\Users\<username>\.kaggle\` (Windows)
3. Sur Linux/Mac: `chmod 600 ~/.kaggle/kaggle.json`

---

### Problème: Mémoire insuffisante

**Erreur**: `MemoryError` pendant le preprocessing

**Solution**:

```python
# Modifier preprocess_retailrocket.py
# Charger les données par chunks
df = pd.read_csv('events.csv', chunksize=100000)
```

---

### Problème: PostgreSQL non accessible

**Erreur**: `could not connect to server`

**Solution**:

```bash
# Vérifier que PostgreSQL tourne
docker-compose ps

# Redémarrer si nécessaire
docker-compose restart postgres

# Attendre 20 secondes
sleep 20

# Réessayer
python scripts/load_retailrocket_to_db.py
```

---

## 📚 Documentation supplémentaire

- [Dataset RetailRocket - Documentation complète](../docs/DATASET.md)
- [Kaggle Dataset Page](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)
- [API Kaggle Documentation](https://github.com/Kaggle/kaggle-api)

---

## 🎉 Prochaines étapes

Une fois le dataset chargé avec succès:

1. **✓ Issue #1 terminée**: Dataset téléchargé et chargé
2. **→ Issue #2**: Nettoyer et valider les données (`feature/data-cleaning`)
3. **→ Issue #3**: Analyse exploratoire (`feature/data-exploration`)

---

## 💡 Commandes utiles

```bash
# Voir les logs PostgreSQL
docker-compose logs -f postgres

# Voir l'espace disque utilisé
docker-compose exec postgres du -sh /var/lib/postgresql/data

# Sauvegarder la base
docker-compose exec postgres pg_dump -U admin ecommerce_db > backup.sql

# Restaurer la base
docker-compose exec -T postgres psql -U admin ecommerce_db < backup.sql
```

---

**Besoin d'aide?** Consultez les [Issues GitHub](https://github.com/Christh2022/ecommerce-abtest-dashboard/issues) ou la documentation.
