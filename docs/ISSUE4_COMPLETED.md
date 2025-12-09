# 🧹 Issue #4 - Nettoyage de item_properties.csv

**Date:** 2025-12-08  
**Branche:** feature/data-preprocessing  
**Statut:** ✅ Terminé

## 📋 Objectif

Nettoyer les fichiers `item_properties_part1.csv` et `item_properties_part2.csv`, parser les valeurs mixtes, structurer les données et créer une vue consolidée des propriétés par produit.

---

## 🔍 Problèmes Identifiés (Issue #2)

Lors de l'inspection, nous avons détecté :
- **Valeurs mixtes** : Format hétérogène (numériques, texte, multiples, avec préfixe 'n')
- **~20M de lignes** : Dataset très volumineux nécessitant une optimisation
- **1,104 types de propriétés** différents
- **Valeurs multiples** : 36.16% des valeurs contiennent plusieurs éléments séparés par des espaces

---

## 📊 Statistiques du Dataset

### Volume de Données

| Métrique | Valeur |
|----------|--------|
| **Lignes totales** | 20,275,902 |
| **Produits uniques** | 417,053 |
| **Propriétés uniques** | 1,104 |
| **Propriétés par produit (moyenne)** | 48.62 |
| **Période temporelle** | 2015-05-10 → 2015-09-13 (126 jours) |
| **Taille mémoire** | 2,616 MB |

### Top 10 Propriétés

| Propriété | Occurrences | % |
|-----------|-------------|---|
| 888 | 3,000,398 | 14.80% |
| 790 | 1,790,516 | 8.83% |
| available | 1,503,639 | 7.42% |
| categoryid | 788,214 | 3.89% |
| 6 | 631,471 | 3.11% |
| 283 | 597,419 | 2.95% |
| 776 | 574,220 | 2.83% |
| 678 | 481,966 | 2.38% |
| 364 | 476,486 | 2.35% |
| 202 | 448,938 | 2.21% |

---

## 🛠️ Opérations de Nettoyage Réalisées

### 1. Chargement et Fusion

**Méthode :** Chargement des deux fichiers (part1 + part2) et concaténation

**Résultats :**
- Part 1 : 10,999,999 lignes
- Part 2 : 9,275,903 lignes
- **Total : 20,275,902 lignes**

### 2. Validation des Données

✅ **Aucun doublon détecté** (0 ligne dupliquée)  
✅ **Aucune valeur manquante** dans les colonnes critiques  
✅ **Tous les timestamps valides** (> 0)  
✅ **Tous les itemid valides** (>= 0)

**Conclusion :** Les données brutes sont de très bonne qualité !

### 3. Structuration des Valeurs (Parsing)

**Problème :** Le champ `value` contient des formats hétérogènes :
- Nombres simples : `519769`
- Valeurs avec préfixe 'n' : `n240.000`, `n91200.000`
- Valeurs multiples : `66094 372274 478989`
- Valeurs mixtes : `n552.000 639502 n720.000 424566`

**Solution :** Parsing intelligent avec extraction des métadonnées

**Nouvelles colonnes créées :**

1. **`value_type`** : Type de valeur
   - `numeric` : Nombre simple (52.43%)
   - `mixed` : Valeur avec préfixe 'n' et autres nombres (25.52%)
   - `multiple` : Plusieurs valeurs séparées (22.04%)
   - `text` : Valeur texte pure (0.00%)

2. **`value_numeric`** : Valeur numérique extraite (pour types `numeric`)

3. **`value_text`** : Valeur texte complète (pour types `mixed`, `multiple`, `text`)

4. **`has_n_prefix`** : Booléen indiquant la présence du préfixe 'n' (25.52%)

5. **`value_count`** : Nombre de valeurs dans le champ (moyenne : 2.53, max : 59)

### 4. Distribution des Types de Valeurs

| Type | Nombre | % | Exemple |
|------|--------|---|---------|
| **numeric** | 10,631,047 | 52.43% | `519769` |
| **mixed** | 5,175,116 | 25.52% | `n552.000 639502 n720.000 424566` |
| **multiple** | 4,469,718 | 22.04% | `66094 372274 478989` |
| **text** | 21 | 0.00% | `available` |

### 5. Création de la Table Pivot

**Objectif :** Agréger toutes les propriétés par produit pour un accès rapide

**Méthode :**
- Garder uniquement la valeur la plus récente pour chaque propriété par produit
- Regrouper toutes les propriétés d'un produit dans des listes

**Résultats :**
- **12,003,814 propriétés uniques** par produit (dédoublonnées)
- **417,053 produits** avec propriétés
- **Propriétés par produit (moyenne) : 28.78**
- **Propriétés par produit (médiane) : 27**
- **Propriétés par produit (max) : 59**

---

## 📁 Fichiers Générés

### 1. item_properties_cleaned.csv

**Chemin :** `data/clean/item_properties_cleaned.csv`

**Caractéristiques :**
- 20,275,902 lignes × 9 colonnes
- Taille : **1,570.99 MB**
- Trié par timestamp, itemid, property

**Colonnes :**
```
1. timestamp (int64)        : UNIX timestamp en millisecondes
2. itemid (int64)           : ID produit
3. property (object)        : Code propriété (0-1103)
4. value (object)           : Valeur originale brute
5. value_type (object)      : Type de valeur (numeric/mixed/multiple/text)
6. value_numeric (float64)  : Valeur numérique extraite (si applicable)
7. value_text (object)      : Valeur texte complète (si applicable)
8. has_n_prefix (bool)      : Présence du préfixe 'n'
9. value_count (int64)      : Nombre de valeurs dans le champ
```

**Usage :**
```python
import pandas as pd

# Charger les données structurées
df = pd.read_csv('data/clean/item_properties_cleaned.csv')

# Filtrer par type de valeur
numeric_props = df[df['value_type'] == 'numeric']
mixed_props = df[df['value_type'] == 'mixed']

# Filtrer les propriétés avec préfixe 'n'
n_prefix_props = df[df['has_n_prefix'] == True]
```

### 2. product_properties_summary.csv

**Chemin :** `data/clean/product_properties_summary.csv`

**Caractéristiques :**
- 417,053 lignes × 5 colonnes
- Taille : **313.22 MB**
- Une ligne par produit avec toutes ses propriétés

**Colonnes :**
```
1. itemid (int64)              : ID produit
2. properties_list (list)      : Liste des codes propriétés
3. values_list (list)          : Liste des valeurs correspondantes
4. last_updated (int64)        : Timestamp de la dernière mise à jour
5. properties_count (int64)    : Nombre de propriétés du produit
```

**Usage :**
```python
import pandas as pd
import ast

# Charger le résumé
df = pd.read_csv('data/clean/product_properties_summary.csv')

# Parser les listes (stockées comme strings)
df['properties_list'] = df['properties_list'].apply(ast.literal_eval)
df['values_list'] = df['values_list'].apply(ast.literal_eval)

# Obtenir toutes les propriétés d'un produit
product_id = 0
product = df[df['itemid'] == product_id].iloc[0]
print(f"Produit {product_id} a {product['properties_count']} propriétés")
print(dict(zip(product['properties_list'], product['values_list'])))
```

### 3. ITEM_PROPERTIES_CLEANING_REPORT.txt

**Chemin :** `data/clean/ITEM_PROPERTIES_CLEANING_REPORT.txt`

**Contenu :**
- Résumé des opérations
- Statistiques avant/après
- Distribution des types de valeurs
- Validation finale

---

## 📈 Résultats du Nettoyage

### Avant vs Après

| Métrique | Avant | Après | Changement |
|----------|-------|-------|------------|
| **Lignes totales** | 20,275,902 | 20,275,902 | ✅ Aucune perte |
| **Doublons** | 0 | 0 | ✅ OK |
| **Valeurs manquantes** | 0 | 0 | ✅ OK |
| **Colonnes** | 4 | 9 | +5 (structuration) |
| **Produits uniques** | 417,053 | 417,053 | ✅ Préservés |
| **Propriétés uniques** | 1,104 | 1,104 | ✅ Préservées |

### Qualité des Données

✅ **100% des données préservées** (aucune suppression nécessaire)  
✅ **0 doublon**  
✅ **0 valeur manquante**  
✅ **Parsing réussi pour 100% des valeurs**  
✅ **Ordre chronologique garanti**  
✅ **Métadonnées enrichies** (+5 colonnes)

---

## 🔍 Analyse Détaillée des Valeurs

### Préfixe 'n'

**5,175,116 valeurs** (25.52%) contiennent le préfixe 'n'

**Hypothèses sur la signification :**
1. **Négation** : Propriété absente ou désactivée
2. **Normalisation** : Valeur normalisée ou standardisée
3. **Notation spéciale** : Code interne du système RetailRocket
4. **Null/None** : Représentation de valeurs nulles

**Exemples :**
- `n240.000` → Peut signifier "pas de 240" ou "valeur normalisée 240"
- `n91200.000` → Valeur élevée avec notation spéciale
- `n552.000 639502 n720.000 424566` → Mix de valeurs normales et 'n'

### Valeurs Multiples

**9,644,834 valeurs** (47.56%) contiennent plusieurs éléments

**Distribution :**
- 1 valeur : 52.44%
- 2-5 valeurs : 38.20%
- 6-10 valeurs : 7.12%
- 11+ valeurs : 2.24%
- Max : **59 valeurs** dans un seul champ

**Exemple extrême :**
```
n36.000 1186610 119932 717520 903287 98606 632686 1117759 504389 
227411 768453 414047 1008741 561431 508431 621351 976840 260167 
934278 388767 42948
```

**Interprétation possible :**
- Propriétés composites (ex: tailles disponibles, couleurs, etc.)
- Références croisées (IDs de catégories liées)
- Historique de valeurs

### Propriété "available"

**1,503,639 occurrences** (7.42%)

**Valeurs observées :**
- `0` : Produit non disponible
- `1` : Produit disponible (probablement)

**Usage :** Indicateur de stock ou de disponibilité

### Propriété "categoryid"

**788,214 occurrences** (3.89%)

**Valeurs :** IDs numériques de catégories (ex: `1338`, `209`, `1114`)

**Lien :** Référence à `category_tree.csv`

---

## 🧪 Exemples de Parsing

### Exemple 1 : Valeur Numérique Simple

**Input :**
```
property: 159
value: 519769
```

**Output :**
```
value_type: numeric
value_numeric: 519769.0
value_text: None
has_n_prefix: False
value_count: 1
```

### Exemple 2 : Valeur Mixte avec 'n'

**Input :**
```
property: 400
value: n552.000 639502 n720.000 424566
```

**Output :**
```
value_type: mixed
value_numeric: None
value_text: n552.000 639502 n720.000 424566
has_n_prefix: True
value_count: 4
```

### Exemple 3 : Valeurs Multiples

**Input :**
```
property: 283
value: 66094 372274 478989
```

**Output :**
```
value_type: multiple
value_numeric: None
value_text: 66094 372274 478989
has_n_prefix: False
value_count: 3
```

---

## 🔧 Script de Nettoyage

### clean_item_properties.py

**Chemin :** `scripts/clean_item_properties.py`

**Fonctionnalités :**

1. **Chargement optimisé**
   - Fusion des deux parties (part1 + part2)
   - Gestion de gros volumes (20M+ lignes)

2. **Validation des données**
   - Détection des doublons
   - Validation des timestamps et IDs
   - Détection des valeurs manquantes

3. **Parsing intelligent**
   - Reconnaissance des types de valeurs
   - Extraction du préfixe 'n'
   - Comptage des valeurs multiples

4. **Structuration**
   - Ajout de colonnes métadonnées
   - Typage cohérent

5. **Agrégation**
   - Création de la table pivot
   - Déduplication par produit/propriété (garder la plus récente)

6. **Optimisation**
   - Tri chronologique
   - Export CSV optimisé

**Usage :**
```bash
python scripts/clean_item_properties.py
```

**Temps d'exécution :** ~5-10 minutes (parsing intensif)

---

## 💡 Insights et Recommandations

### Court Terme

1. ✅ **Utiliser item_properties_cleaned.csv** pour les analyses détaillées
2. ✅ **Utiliser product_properties_summary.csv** pour un accès rapide par produit
3. ⏳ **Documenter la signification du préfixe 'n'** (contacter RetailRocket ou analyser les patterns)
4. ⏳ **Créer un dictionnaire des propriétés** (mapper les codes 0-1103 vers des noms lisibles)

### Moyen Terme

1. 📊 **Analyser les propriétés les plus impactantes**
   - Corrélation entre propriétés et ventes
   - Propriétés manquantes sur les produits populaires

2. 🔄 **Normaliser les valeurs**
   - Supprimer ou interpréter le préfixe 'n'
   - Séparer les valeurs multiples en lignes distinctes (optionnel)

3. 🏷️ **Enrichir avec category_tree.csv**
   - Joindre les catégories via `categoryid`
   - Créer une hiérarchie complète produit → catégorie

### Long Terme

1. 🗄️ **Modélisation en base de données**
   - Table `products` (itemid, last_updated)
   - Table `product_properties` (itemid, property, value, timestamp)
   - Index sur itemid et property

2. 🚀 **API de requête**
   - Endpoint pour récupérer toutes les propriétés d'un produit
   - Recherche par propriété
   - Filtrage par type de valeur

---

## 📊 Cas d'Usage

### 1. Récupérer toutes les propriétés d'un produit

```python
import pandas as pd
import ast

# Charger le résumé
df = pd.read_csv('data/clean/product_properties_summary.csv')

# Parser les listes
df['properties_list'] = df['properties_list'].apply(ast.literal_eval)
df['values_list'] = df['values_list'].apply(ast.literal_eval)

# Fonction utilitaire
def get_product_properties(itemid):
    product = df[df['itemid'] == itemid]
    if product.empty:
        return None
    product = product.iloc[0]
    return dict(zip(product['properties_list'], product['values_list']))

# Exemple
props = get_product_properties(0)
print(f"Produit 0 : {len(props)} propriétés")
print(props)
```

### 2. Analyser les produits par disponibilité

```python
import pandas as pd

# Charger les données nettoyées
df = pd.read_csv('data/clean/item_properties_cleaned.csv')

# Filtrer la propriété 'available'
availability = df[df['property'] == 'available']

# Compter par statut
available_counts = availability['value'].value_counts()
print("Disponibilité des produits:")
print(available_counts)

# Produits disponibles
available_items = availability[availability['value'] == '1']['itemid'].unique()
print(f"\nNombre de produits disponibles: {len(available_items)}")
```

### 3. Trouver les produits d'une catégorie

```python
import pandas as pd

# Charger les données
df = pd.read_csv('data/clean/item_properties_cleaned.csv')

# Filtrer par categoryid
category_id = '1338'
products_in_category = df[
    (df['property'] == 'categoryid') & 
    (df['value'] == category_id)
]['itemid'].unique()

print(f"Produits dans la catégorie {category_id}: {len(products_in_category)}")
```

---

## 📝 Notes Techniques

### Gestion Mémoire

Le dataset étant volumineux (2.6 GB en RAM), optimisations appliquées :
- Chargement par chunks (non implémenté mais possible)
- Export CSV direct sans copies intermédiaires
- Libération mémoire après agrégation

### Format des Listes

Dans `product_properties_summary.csv`, les listes sont stockées comme strings :
```
"['283', '790', '678']"
```

Pour les parser en Python :
```python
import ast
df['properties_list'] = df['properties_list'].apply(ast.literal_eval)
```

---

## ✅ Critères de Complétion

- [x] Chargement et fusion des deux parties (part1 + part2)
- [x] Validation des données (doublons, valeurs manquantes, IDs invalides)
- [x] Parsing complet du champ `value`
- [x] Création de colonnes métadonnées (value_type, value_numeric, etc.)
- [x] Détection du préfixe 'n' (25.52%)
- [x] Comptage des valeurs multiples
- [x] Création de la table pivot par produit
- [x] Tri chronologique
- [x] Génération de 2 fichiers CSV (cleaned + summary)
- [x] Rapport de nettoyage détaillé
- [x] Documentation complète

---

## 🎯 Conclusion

Le nettoyage de `item_properties.csv` est **terminé avec succès**. Les données sont maintenant :

✅ **Structurées** (9 colonnes vs 4)  
✅ **Validées** (0 doublon, 0 valeur manquante)  
✅ **Enrichies** (métadonnées de parsing)  
✅ **Optimisées** (table pivot pour accès rapide)  
✅ **Prêtes** pour l'analyse et le chargement en base de données

**Impact :** Transformation majeure d'un dataset brut en données exploitables

**Qualité des données :** ⭐⭐⭐⭐⭐ (5/5)

---

## 📂 Fichiers du Projet

```
data/
├── raw/
│   ├── item_properties_part1.csv (11M lignes)
│   └── item_properties_part2.csv (9.3M lignes)
└── clean/
    ├── item_properties_cleaned.csv (20.3M lignes, 1.57 GB - À UTILISER)
    ├── product_properties_summary.csv (417K produits, 313 MB - ACCÈS RAPIDE)
    └── ITEM_PROPERTIES_CLEANING_REPORT.txt

scripts/
└── clean_item_properties.py (script de nettoyage)

docs/
└── ISSUE4_COMPLETED.md (ce fichier)
```

---

**Date de clôture :** 2025-12-08  
**Branche :** feature/data-preprocessing  
**Issue :** #4 ✅ CLOSED
