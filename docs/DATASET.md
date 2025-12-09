# Dataset RetailRocket - E-commerce

## 📊 Vue d'ensemble

**Source**: [Kaggle - RetailRocket E-commerce Dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)

**Description**: Dataset de comportement utilisateur réel sur un site e-commerce, collecté par le système de recommandation RetailRocket.

**Période couverte**: 4.5 mois

**Taille**: ~2.7 millions d'événements

## 📁 Fichiers du dataset

### 1. events.csv

Événements utilisateur sur le site e-commerce.

**Colonnes**:

- `timestamp` : Horodatage de l'événement (en millisecondes)
- `visitorid` : ID unique du visiteur
- `event` : Type d'événement (`view`, `addtocart`, `transaction`)
- `itemid` : ID du produit concerné
- `transactionid` : ID de transaction (uniquement pour les événements `transaction`)

**Statistiques**:

- ~2.7M événements
- ~1.4M visiteurs uniques
- ~400K produits uniques

**Types d'événements**:

- `view` : Consultation d'un produit (~98%)
- `addtocart` : Ajout au panier (~1.5%)
- `transaction` : Achat effectué (~0.5%)

### 2. item_properties_part1.csv & item_properties_part2.csv

Propriétés des produits (divisé en 2 parties pour la taille).

**Colonnes**:

- `timestamp` : Horodatage de la propriété
- `itemid` : ID du produit
- `property` : Nom de la propriété (ex: categoryid, available)
- `value` : Valeur de la propriété

**Propriétés disponibles**:

- `categoryid` : ID de catégorie du produit
- `available` : Disponibilité (0 ou 1)
- Autres propriétés spécifiques au catalogue

### 3. category_tree.csv

Arborescence des catégories de produits.

**Colonnes**:

- `categoryid` : ID de la catégorie
- `parentid` : ID de la catégorie parente

## 🔄 Pipeline de traitement

### Étape 1: Téléchargement

```bash
python scripts/download_dataset.py
```

**Actions**:

- Télécharge le dataset depuis Kaggle
- Extrait les fichiers CSV dans `data/raw/`
- Vérifie l'intégrité des fichiers

**Prérequis**:

- Compte Kaggle
- API Token Kaggle configuré

### Étape 2: Preprocessing

```bash
python scripts/preprocess_retailrocket.py
```

**Actions**:

- Charge et analyse les données brutes
- Nettoie et transforme les données
- Crée les tables structurées :
  - `users.csv` : Profils utilisateurs
  - `products.csv` : Catalogue produits
  - `sessions.csv` : Sessions de navigation
  - `transactions.csv` : Transactions
- Génère des statistiques descriptives

**Transformations**:

- Conversion des timestamps
- Agrégation des événements par utilisateur/produit
- Création de sessions (groupement par utilisateur et jour)
- Segmentation des utilisateurs (New, Occasional, Regular, Premium)
- Génération de montants fictifs pour les transactions (le dataset original n'a pas de prix)

### Étape 3: Chargement en base de données

```bash
python scripts/load_retailrocket_to_db.py
```

**Actions**:

- Lit les fichiers nettoyés depuis `data/clean/`
- Charge les données dans PostgreSQL
- Crée les index pour optimiser les performances
- Vérifie l'intégrité des données

## 📈 Statistiques du dataset

### Événements

- **Total**: ~2,756,101 événements
- **Views**: ~2,664,312 (96.7%)
- **Add to cart**: ~69,332 (2.5%)
- **Transactions**: ~22,457 (0.8%)

### Utilisateurs

- **Visiteurs uniques**: ~1,407,580
- **Moyenne événements/utilisateur**: ~2 événements
- **Utilisateurs actifs**: ~30% font plus de 3 actions

### Produits

- **Produits uniques**: ~417,053
- **Produits avec transactions**: ~22,457 (5.4%)
- **Top produit**: ~13,000 vues

### Période

- **Début**: Mai 2015
- **Fin**: Septembre 2015
- **Durée**: 135 jours
- **Événements/jour**: ~20,000

## 🎯 Cas d'usage pour le dashboard

### 1. KPIs E-commerce

- Taux de conversion (transaction / view)
- Taux d'ajout au panier (addtocart / view)
- Panier moyen (simulé)
- Produits les plus consultés
- Utilisateurs actifs

### 2. Analyse comportementale

- Funnel de conversion (view → addtocart → transaction)
- Durée des sessions
- Nombre de produits consultés par session
- Distribution des événements dans le temps
- Patterns de navigation

### 3. Tests A/B

- Segmentation utilisateurs (New, Occasional, Regular, Premium)
- Comparaison de conversion par segment
- Tests sur différentes périodes
- Impact de la catégorie sur la conversion

### 4. Analyse de cohortes

- Rétention utilisateur sur la période
- Comportement par cohorte d'inscription
- Évolution de l'engagement dans le temps

## ⚠️ Limitations et notes

### Limitations du dataset

1. **Pas de prix réels**: Les montants sont générés aléatoirement pour la démo
2. **Pas d'informations démographiques**: Pas de données sur l'âge, le genre, la localisation
3. **Propriétés limitées**: Peu d'informations sur les caractéristiques des produits
4. **Dataset anonymisé**: IDs génériques pour préserver la confidentialité

### Améliorations possibles

1. Enrichir avec des prix réalistes basés sur les catégories
2. Simuler des données démographiques cohérentes
3. Ajouter des descriptions de produits pour améliorer l'analyse
4. Créer des segments plus sophistiqués

## 📚 Références

- **Dataset source**: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset
- **RetailRocket**: https://retailrocket.io/
- **Paper**: "Context-Aware Recommender Systems for E-commerce"

## 🔗 Liens utiles

- [Kaggle Dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)
- [Documentation Kaggle API](https://github.com/Kaggle/kaggle-api)
- [Notebooks d'analyse](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset/code)
