# 🧹 Issue #3 - Nettoyage de events.csv

**Date:** 2025-12-08  
**Branche:** feature/data-preprocessing  
**Statut:** ✅ Terminé

## 📋 Objectif

Nettoyer le fichier `events.csv` en supprimant les doublons identifiés lors de l'inspection (Issue #2) et en validant l'intégrité des données.

---

## 🔍 Problèmes Identifiés (Issue #2)

Lors de l'inspection, nous avons détecté :
- **460 doublons** (0.02% des données) - lignes complètement identiques
- **471 doublons partiels** - même timestamp + visitorid + itemid

---

## 🛠️ Opérations de Nettoyage Réalisées

### 1. Suppression des Doublons

**Méthode :** Suppression des lignes complètement identiques (toutes colonnes)

**Résultats :**
- Lignes avant : 2,756,101
- Doublons supprimés : 460
- Lignes après : 2,755,641
- Taux de doublons : **0.0167%**

**Impact :**
- ✅ 0 doublon restant
- ✅ Intégrité temporelle préservée (ordre chronologique maintenu)

### 2. Validation des Données

**Vérifications effectuées :**

✅ **Timestamps**
- Aucun timestamp invalide (<= 0)
- Période : 2015-05-03 → 2015-09-18 (137 jours)
- Format : UNIX timestamp en millisecondes

✅ **IDs (visitorid, itemid)**
- Aucun ID négatif ou nul
- visitorid : 1,407,580 utilisateurs uniques
- itemid : 235,061 produits uniques

✅ **Types d'événements**
- Uniquement 3 types valides : `view`, `addtocart`, `transaction`
- Aucun type d'événement invalide détecté

✅ **Transactions**
- 22,457 transactions
- Toutes les transactions ont un `transactionid` valide
- Aucune transaction sans ID

✅ **Valeurs manquantes**
- Aucune valeur manquante dans les colonnes critiques :
  - timestamp ✅
  - visitorid ✅
  - event ✅
  - itemid ✅
- transactionid : 99.19% manquantes (normal, seules les transactions ont un ID)

### 3. Tri des Données

Les données ont été triées par **timestamp** (ordre chronologique) pour faciliter :
- L'analyse temporelle
- Le traçage des sessions utilisateurs
- Le calcul des séquences d'événements

---

## 📊 Distribution des Événements Nettoyés

### Avant Nettoyage
| Événement    | Nombre     | Pourcentage |
|--------------|------------|-------------|
| view         | 2,664,312  | 96.67%      |
| addtocart    | 69,332     | 2.52%       |
| transaction  | 22,457     | 0.81%       |
| **TOTAL**    | **2,756,101** | **100%** |

### Après Nettoyage
| Événement    | Nombre     | Pourcentage | Changement |
|--------------|------------|-------------|------------|
| view         | 2,664,218  | 96.68%      | -94 lignes |
| addtocart    | 68,966     | 2.50%       | -366 lignes |
| transaction  | 22,457     | 0.81%       | ✅ Aucun changement |
| **TOTAL**    | **2,755,641** | **100%** | **-460 lignes** |

**Observations :**
- Les transactions sont intactes ✅ (aucune transaction n'était dupliquée)
- La plupart des doublons concernaient des `view` et `addtocart`
- Distribution globale inchangée (< 0.02% d'impact)

---

## 📁 Fichiers Générés

### 1. events_cleaned.csv

**Chemin :** `data/clean/events_cleaned.csv`

**Caractéristiques :**
- 2,755,641 lignes × 5 colonnes
- Taille : 92.53 MB (vs 223.90 MB en mémoire)
- Trié par ordre chronologique
- 0 doublon
- 0 valeur manquante critique

**Colonnes :**
- `timestamp` (int64) : UNIX timestamp en millisecondes
- `visitorid` (int64) : ID utilisateur unique
- `event` (object) : Type d'événement (view/addtocart/transaction)
- `itemid` (int64) : ID produit
- `transactionid` (float64) : ID transaction (vide sauf pour events = transaction)

### 2. CLEANING_REPORT.txt

**Chemin :** `data/clean/CLEANING_REPORT.txt`

**Contenu :**
- Résumé des opérations
- Nombre de lignes supprimées
- Validation finale
- Distribution des événements

---

## 🔧 Script de Nettoyage

### clean_events.py

**Chemin :** `scripts/clean_events.py`

**Fonctionnalités :**

1. **Chargement sécurisé**
   - Vérification de l'existence du fichier
   - Gestion des erreurs de lecture
   - Affichage des métadonnées

2. **Analyse pré-nettoyage**
   - Détection des doublons
   - Détection des valeurs manquantes
   - Validation des types de données
   - Distribution des événements

3. **Nettoyage automatisé**
   - Suppression des doublons exacts
   - Suppression des données invalides (timestamps négatifs, IDs invalides)
   - Validation des transactions
   - Tri chronologique

4. **Analyse post-nettoyage**
   - Validation finale (0 doublon, 0 valeur manquante critique)
   - Comparaison avant/après
   - Statistiques descriptives

5. **Sauvegarde et rapport**
   - Export CSV nettoyé
   - Génération de rapport texte
   - Recommandations pour la suite

**Usage :**
```bash
python scripts/clean_events.py
```

**Sorties :**
- `data/clean/events_cleaned.csv` : Données nettoyées
- `data/clean/CLEANING_REPORT.txt` : Rapport détaillé

---

## 📈 Statistiques Comparatives

### Avant vs Après Nettoyage

| Métrique                          | Avant        | Après        | Changement |
|-----------------------------------|--------------|--------------|------------|
| **Lignes totales**                | 2,756,101    | 2,755,641    | -460 (-0.0167%) |
| **Doublons**                      | 460          | 0            | ✅ -100% |
| **Valeurs manquantes critiques**  | 0            | 0            | ✅ OK |
| **Timestamps invalides**          | 0            | 0            | ✅ OK |
| **IDs invalides**                 | 0            | 0            | ✅ OK |
| **Types événements invalides**    | 0            | 0            | ✅ OK |
| **Transactions sans ID**          | 0            | 0            | ✅ OK |
| **Taille fichier**                | ~224 MB      | 92.53 MB     | -58.7% (compression) |

### Intégrité des Données

✅ **100% des transactions préservées** (22,457 → 22,457)  
✅ **0 doublon restant**  
✅ **0 donnée invalide**  
✅ **Ordre chronologique garanti**  
✅ **Tous les utilisateurs préservés** (1,407,580)  
✅ **Tous les produits préservés** (235,061)

---

## 🔍 Analyse des Doublons Supprimés

### Répartition par Type d'Événement

| Type        | Doublons Supprimés | % du Type |
|-------------|-------------------|-----------|
| view        | 94                | 0.0035%   |
| addtocart   | 366               | 0.528%    |
| transaction | 0                 | 0%        |
| **TOTAL**   | **460**           | **0.0167%** |

**Insights :**
- Les doublons affectaient principalement les `addtocart` (79.6% des doublons)
- Aucune transaction n'était dupliquée ✅
- Impact négligeable sur les vues (0.0035%)

### Hypothèses sur la Cause des Doublons

1. **Double-clic utilisateur** : Clics répétés rapides sur "Ajouter au panier"
2. **Problèmes réseau** : Retry automatique côté client
3. **Bug de tracking** : Événements envoyés deux fois par le SDK analytics
4. **Latence API** : Événements enregistrés en doublon côté serveur

---

## ✅ Validation de la Qualité

### Tests Effectués

1. ✅ **Absence de doublons**
   ```python
   assert df_cleaned.duplicated().sum() == 0
   ```

2. ✅ **Absence de valeurs manquantes critiques**
   ```python
   critical_cols = ['timestamp', 'visitorid', 'event', 'itemid']
   assert df_cleaned[critical_cols].isnull().sum().sum() == 0
   ```

3. ✅ **Timestamps valides**
   ```python
   assert (df_cleaned['timestamp'] > 0).all()
   ```

4. ✅ **IDs valides**
   ```python
   assert (df_cleaned['visitorid'] >= 0).all()
   assert (df_cleaned['itemid'] >= 0).all()
   ```

5. ✅ **Types d'événements valides**
   ```python
   valid_events = ['view', 'addtocart', 'transaction']
   assert df_cleaned['event'].isin(valid_events).all()
   ```

6. ✅ **Transactions avec ID**
   ```python
   transactions = df_cleaned[df_cleaned['event'] == 'transaction']
   assert transactions['transactionid'].notna().all()
   ```

7. ✅ **Ordre chronologique**
   ```python
   assert df_cleaned['timestamp'].is_monotonic_increasing
   ```

---

## 🔄 Impact sur les Scripts Existants

### Scripts à Mettre à Jour

Les scripts suivants peuvent maintenant utiliser `events_cleaned.csv` au lieu de `events.csv` :

1. ~~`preprocess_retailrocket.py`~~ *(optionnel, déjà exécuté)*
   - Peut être réexécuté avec le fichier nettoyé pour régénérer :
     - `users.csv`
     - `products.csv`
     - `sessions.csv`
     - `transactions.csv`

2. `load_retailrocket_to_db.py`
   - Charger `events_cleaned.csv` dans PostgreSQL au lieu de `events.csv`

3. Futurs scripts d'analyse
   - Utiliser systématiquement `events_cleaned.csv` comme source

### Commande de Régénération (Optionnel)

```bash
# Si vous souhaitez régénérer les fichiers prétraités avec les données nettoyées
python scripts/preprocess_retailrocket.py --input data/clean/events_cleaned.csv
```

---

## 📊 Métriques de Performance

### Temps d'Exécution

- **Chargement** : ~5 secondes (2.7M lignes)
- **Détection des doublons** : ~2 secondes
- **Suppression** : ~1 seconde
- **Validation** : ~3 secondes
- **Tri** : ~4 secondes
- **Sauvegarde** : ~6 secondes
- **Total** : ~21 secondes ⚡

### Consommation Mémoire

- **Données brutes** : ~224 MB en RAM
- **Données nettoyées** : ~92.53 MB sur disque
- **Pic mémoire** : ~250 MB (pandas overhead)

---

## 🎯 Recommandations pour la Suite

### Court Terme

1. ✅ **Utiliser events_cleaned.csv** pour toutes les analyses futures
2. ✅ **Archiver events.csv** (garder en backup, ne plus utiliser directement)
3. ⏳ **Mettre à jour load_retailrocket_to_db.py** pour charger les données nettoyées
4. ⏳ **Commiter les changements** sur la branche feature/data-preprocessing

### Moyen Terme

1. 📊 **Créer un dashboard de qualité des données**
   - Suivi des doublons au fil du temps
   - Alertes sur anomalies
   - Métriques de fraîcheur des données

2. 🔄 **Automatiser le nettoyage**
   - Pipeline ETL pour nettoyer les nouvelles données
   - Scheduler quotidien/hebdomadaire
   - Validation automatique des règles qualité

3. 📈 **Tracer l'origine des doublons**
   - Analyser les patterns temporels
   - Identifier les utilisateurs/produits récurrents
   - Corriger la source (tracking, API)

---

## 🐛 Problèmes Résolus

| Problème | Statut | Solution |
|----------|--------|----------|
| 460 doublons dans events.csv | ✅ Résolu | Suppression avec `drop_duplicates()` |
| Ordre non chronologique | ✅ Résolu | Tri par timestamp |
| Validation des transactions | ✅ Vérifié | Toutes ont un transactionid |
| Types d'événements invalides | ✅ Aucun | Validation passed |
| IDs négatifs | ✅ Aucun | Validation passed |

---

## 📝 Notes Techniques

### Algorithme de Déduplication

```python
# Suppression des doublons exacts (toutes colonnes identiques)
df_cleaned = df.drop_duplicates()

# Alternative : Suppression par clés primaires
# df_cleaned = df.drop_duplicates(subset=['timestamp', 'visitorid', 'itemid'], keep='first')
```

**Choix retenu :** Suppression des doublons exacts (toutes colonnes)

**Raison :** Conserver les événements avec des `transactionid` différents même si timestamp/user/item sont identiques (cas rares mais légitimes).

### Gestion des Valeurs Manquantes

- **transactionid** : 99.19% manquantes (normal, comportement attendu)
- **Autres colonnes** : 0% manquantes ✅

Pas de remplissage (imputation) nécessaire.

---

## 🎯 Conclusion

Le nettoyage de `events.csv` est **terminé avec succès**. Les données sont maintenant :

✅ **Sans doublon** (460 lignes supprimées)  
✅ **Valides** (timestamps, IDs, types d'événements)  
✅ **Triées** chronologiquement  
✅ **Prêtes** pour l'analyse et le chargement en base de données  

**Impact :** Minime (-0.0167%) mais crucial pour la qualité des analyses.

**Qualité des données :** ⭐⭐⭐⭐⭐ (5/5)

---

## 📂 Fichiers du Projet

```
data/
├── raw/
│   └── events.csv (2,756,101 lignes - NE PLUS UTILISER)
└── clean/
    ├── events_cleaned.csv (2,755,641 lignes - À UTILISER)
    ├── CLEANING_REPORT.txt (rapport de nettoyage)
    ├── users.csv
    ├── products.csv
    ├── sessions.csv
    └── transactions.csv

scripts/
├── clean_events.py (script de nettoyage)
├── inspect_csv.py
├── download_dataset.py
├── preprocess_retailrocket.py
└── load_retailrocket_to_db.py

docs/
├── ISSUE1_COMPLETED.md
├── ISSUE2_COMPLETED.md
└── ISSUE3_COMPLETED.md (ce fichier)
```

---

**Date de clôture :** 2025-12-08  
**Branche :** feature/data-preprocessing  
**Issue :** #3 ✅ CLOSED
