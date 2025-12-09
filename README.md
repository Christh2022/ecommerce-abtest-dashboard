"# E-commerce Dashboard & A/B Testing

Plateforme d'analyse e-commerce avec dashboard interactif et outils d'A/B testing utilisant Python, Dash, PostgreSQL, Docker et Grafana.

## 📊 Vue d'ensemble

Ce projet analyse les données du dataset **RetailRocket** (2.7M événements, 1.4M utilisateurs, 235K produits) pour créer un dashboard de visualisation et des outils d'analyse de performance e-commerce.

### Objectifs
- 📈 **Dashboard interactif** : Visualisation en temps réel des KPIs e-commerce
- 🧪 **A/B Testing** : Comparaison de segments utilisateurs et analyse de conversion
- 📉 **Analyse de tendances** : Métriques quotidiennes, entonnoirs de conversion, performance produits
- 🎯 **Recommandations** : Identification des produits top performers et opportunités d'optimisation

---

## 🎯 Milestone 1 : Dataset & Préparation des Données ✅

**Statut** : COMPLÉTÉ (8 issues)  
**Branche** : `feature/data-preprocessing`  
**Période** : Décembre 2025

### 📦 Dataset RetailRocket

Source : [Kaggle - RetailRocket E-commerce Dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)

**Caractéristiques :**
- **Période couverte** : 2015-05-03 → 2015-09-18 (137 jours / 19.6 semaines)
- **Événements totaux** : 2,755,641 (après nettoyage)
  - Views : 2,664,218 (96.7%)
  - Add-to-carts : 68,966 (2.5%)
  - Transactions : 22,457 (0.8%)
- **Utilisateurs uniques** : 1,407,580
- **Sessions uniques** : 1,649,534
- **Produits uniques** : 235,061
- **Revenu total** : 5,732,867.82 €
- **Taux de conversion global** : 0.84%

---

## 🔧 Issues Complétées

### Issue #1 : Télécharger le dataset RetailRocket ✅
**Fichiers créés :**
- `scripts/download_data.py` : Script de téléchargement via Kaggle API
- Données brutes (942 MB) → nettoyées (536 MB)

### Issue #2 : Inspecter les fichiers CSV ✅
**Fichiers créés :**
- `scripts/inspect_csv.py` : Analyse exploratoire des données
- Résultats : 460 doublons détectés dans `events.csv`

### Issue #3 : Nettoyer events.csv ✅
**Fichiers créés :**
- `scripts/clean_events.py` : Suppression des doublons
- `data/clean/events_cleaned.csv` : 2,755,641 lignes (460 doublons supprimés)

### Issue #4 : Nettoyer item_properties.csv ✅
**Fichiers créés :**
- `scripts/clean_item_properties.py` : Parsing et structuration
- `data/clean/item_properties_cleaned.csv` : 20,275,902 lignes, 9 colonnes typées

### Issue #5 : Fusionner les données ✅
**Fichiers créés :**
- `scripts/merge_data.py` : Fusion et enrichissement (515 lignes)
- **8 tables enrichies** (490 MB total) :
  - `events_enriched.csv` : 2.7M lignes, 12 colonnes (242 MB)
  - `sessions_enriched.csv` : 1.6M lignes, 10 colonnes (134 MB)
  - `transactions_enriched.csv` : 22K lignes, 13 colonnes (2 MB)
  - `daily_funnel.csv` : 139 jours, entonnoir de conversion
  - `hourly_analysis.csv` : 24 heures, activité horaire
  - `segment_performance.csv` : 4 segments utilisateurs
  - `user_journey.csv` : 1.4M parcours (105 MB)
  - `product_performance.csv` : 235K produits (7.5 MB)

### Issue #6 : Générer data_clean.csv ✅
**Fichiers créés :**
- `scripts/generate_data_clean_simple.py` : Consolidation optimisée par chunks
- `data/clean/data_clean.csv` : 2.7M lignes, 13 colonnes (229 MB)
- **Colonnes** : user_id, session_id, timestamp, date, hour, day_of_week, event_type, product_id, transaction_id, amount, segment, product_views, product_purchases

### Issue #7 : Générer daily_metrics.csv ✅
**Fichiers créés :**
- `scripts/generate_daily_metrics.py` : Métriques quotidiennes (224 lignes)
- `data/clean/daily_metrics.csv` : 139 jours, 29 colonnes (24 KB)
- **Métriques incluses** :
  - Base : users, sessions, produits, événements
  - Conversion : view→cart, view→purchase, cart→purchase
  - Revenus : daily_revenue, avg_order_value, min/max_order
  - Par utilisateur : events_per_user, sessions_per_user, revenue_per_user
  - Moyennes mobiles (MA7) : revenue, users, conversion
  - Segmentation : users_new, users_occasional, users_regular, users_premium
  - Temporel : day_of_week, week_number, month, is_weekend

### Issue #8 : Générer products_summary.csv ✅
**Fichiers créés :**
- `scripts/generate_products_summary.py` : Analyse produits (268 lignes)
- `data/clean/products_summary.csv` : 235K produits, 21 colonnes (20 MB)
- **Métriques incluses** :
  - Rang et catégorisation (Top Performer, High Revenue)
  - Engagement : views, add_to_carts, purchases, unique_users
  - Conversion : view→cart, view→purchase, cart→purchase
  - Revenus : total_revenue, avg_price, min/max_price
  - Performance : events_per_user, revenue_per_user, revenue_per_view

---

## 📊 KPIs Globaux

### Utilisateurs
- **Total** : 1,407,580 utilisateurs uniques
- **Sessions** : 1,649,534 (1.17 sessions/user en moyenne)
- **Segmentation** :
  - New : 70% (983K users)
  - Occasional : 17% (239K users)
  - Regular : 7% (99K users)
  - Premium : 6% (89K users)

### Événements
- **Total** : 2,755,641 événements
- **Par type** :
  - Views : 2,664,218 (96.7%)
  - Add-to-carts : 68,966 (2.5%)
  - Transactions : 22,457 (0.8%)
- **Moyenne** : 1.96 événements/utilisateur

### Conversion
- **View → Add-to-cart** : 2.59%
- **View → Purchase** : 0.84%
- **Cart → Purchase** : 32.56%

### Revenus
- **Total** : 5,732,867.82 €
- **Par jour** : 41,243.65 € (moyenne)
- **Panier moyen** : 255.28 €
- **Par utilisateur** : 4.07 €

### Produits
- **Catalogués** : 235,061 produits
- **Avec ventes** : 12,025 (5.1%)
- **Sans ventes** : 223,036 (94.9%)
- **Revenu moyen** : 24.39 €/produit
- **Top produit #461686** : 34,781.58 € (133 achats, 5.24% conversion)

### Meilleurs jours
- **Revenue max** : 2015-07-28
- **Utilisateurs max** : 2015-07-26
- **Conversion max** : 2015-07-28

---

## 📁 Structure des données

```
data/
├── raw/                          # Données brutes (942 MB)
│   ├── events.csv
│   ├── item_properties.csv
│   └── category_tree.csv
│
└── clean/                        # Données nettoyées et enrichies
    ├── events_cleaned.csv        # 2.7M événements nettoyés
    ├── data_clean.csv            # 2.7M lignes consolidées (229 MB)
    ├── daily_metrics.csv         # 139 jours de métriques (24 KB)
    ├── products_summary.csv      # 235K produits analysés (20 MB)
    │
    ├── events_enriched.csv       # Événements + segments + produits (242 MB)
    ├── sessions_enriched.csv     # Sessions + segments (134 MB)
    ├── transactions_enriched.csv # Transactions enrichies (2 MB)
    │
    ├── daily_funnel.csv          # Entonnoir quotidien
    ├── hourly_analysis.csv       # Activité horaire
    ├── segment_performance.csv   # Performance par segment
    ├── user_journey.csv          # Parcours utilisateurs (105 MB)
    └── product_performance.csv   # Performance produits (7.5 MB)
```

---

## 🛠️ Scripts développés

```
scripts/
├── download_data.py                    # Téléchargement Kaggle
├── inspect_csv.py                      # Exploration données
├── clean_events.py                     # Nettoyage événements
├── clean_item_properties.py            # Nettoyage propriétés
├── merge_data.py                       # Fusion et enrichissement
├── generate_data_clean_simple.py       # Consolidation données
├── generate_daily_metrics.py           # Métriques quotidiennes
└── generate_products_summary.py        # Analyse produits
```

---

## 🚀 Utilisation

### Prérequis
```bash
# Python 3.12+
pip install pandas numpy kaggle

# Configuration Kaggle API
export KAGGLE_USERNAME=<votre_username>
export KAGGLE_KEY=<votre_key>
```

### Télécharger et préparer les données
```bash
# 1. Télécharger le dataset
python scripts/download_data.py

# 2. Nettoyer les données
python scripts/clean_events.py
python scripts/clean_item_properties.py

# 3. Fusionner et enrichir
python scripts/merge_data.py

# 4. Générer les fichiers d'analyse
python scripts/generate_data_clean_simple.py
python scripts/generate_daily_metrics.py
python scripts/generate_products_summary.py
```

---

## 📈 Insights clés

### 1. Conversion en entonnoir classique
- **96.7%** des interactions sont des vues
- Seulement **2.5%** ajoutent au panier
- **32.6%** des paniers se convertissent en achat
- **Opportunité** : Optimiser la transition view → cart (+2.59% actuellement)

### 2. Segmentation utilisateurs
- **70% sont "New"** : Opportunité de rétention
- **Premium (6%)** représentent probablement une part disproportionnée du revenu
- **Stratégie** : Programmes de fidélisation pour convertir New → Occasional → Regular

### 3. Catalogue produits
- **94.9% des produits n'ont jamais été vendus** : Problème de merchandising
- **5.1% des produits génèrent 100% du revenu** : Concentration extrême
- **Top 4.7% ("Top Performers")** : Focus sur ces produits pour maximiser ROI

### 4. Saisonnalité
- **Pic d'activité** : Fin juillet 2015 (été)
- **Variation hebdomadaire** : Analyse des weekends vs semaine disponible
- **Tendances** : Moyennes mobiles (MA7) pour lisser les variations

---

## 🎯 Prochaines étapes : Milestone 2

### Dashboard & Visualisation
- [ ] **Issue #9** : Créer le dashboard Dash avec visualisations interactives
- [ ] **Issue #10** : Implémenter les filtres (segment, période, produit)
- [ ] **Issue #11** : Configurer Docker + PostgreSQL
- [ ] **Issue #12** : Intégrer Grafana pour monitoring avancé
- [ ] **Issue #13** : Déployer l'application complète

---

## 👥 Équipe & Contribution

**Auteur** : E-commerce Dashboard Team  
**Repository** : [Christh2022/ecommerce-abtest-dashboard](https://github.com/Christh2022/ecommerce-abtest-dashboard)  
**Branche active** : `feature/data-preprocessing`

---

## 📝 License

Ce projet utilise le dataset RetailRocket sous licence publique Kaggle.

---

**Dernière mise à jour** : 9 décembre 2025  
**Milestone 1** : ✅ COMPLÉTÉ (8/8 issues)" 
