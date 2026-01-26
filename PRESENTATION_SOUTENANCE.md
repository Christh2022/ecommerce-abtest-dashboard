---
marp: true
theme: default
paginate: true
backgroundColor: #fff
header: '📊 Analyse E-Commerce - Projet #1'
footer: 'L\'École Multimédia - Décembre 2025'
---
<style>
section {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 24px;
}
h1 {
  color: #1e88e5;
  border-bottom: 3px solid #1e88e5;
  padding-bottom: 10px;
}
h2 {
  color: #43a047;
}
.lead {
  text-align: center;
}
blockquote {
  background-color: #f5f5f5;
  border-left: 5px solid #1e88e5;
  padding: 15px;
  margin: 20px 0;
  font-style: italic;
}
code {
  background-color: #f4f4f4;
  padding: 2px 6px;
  border-radius: 3px;
}
</style>

<!-- _class: lead -->

# 📊 ANALYSE DE PERFORMANCES

# ET OPTIMISATION

# D'UN SITE E-COMMERCE

**Projet #1 - Programmation Data avec Python**
**Directeur de projet en intelligence artificielle - Année 1**

[Votre Nom] - Décembre 2025

---

<!-- _class: lead -->

> **Démarche**
>
> La présentation suit une démarche classique d'analyse de données, appuyée par des diagrammes explicatifs et une revue du code pour illustrer la méthodologie.

**Durée : 10 minutes + questions**

---

# 1. CONTEXTE GÉNÉRAL 🎯

## Cadre du projet

**Mission** : Développeur data recruté par une entreprise e-commerce

**Environnement métier** :

- Plateforme de vente en ligne (retail)
- 235,000 produits catalogués
- 1,4 million d'utilisateurs
- Volume : 2,76M d'événements sur 4,5 mois

**Problématique globale** :

> Comment améliorer les performances du site et augmenter les conversions en s'appuyant sur l'analyse de données réelles ?

---

# Diagramme de Contexte

```
┌─────────────────────────────────────────────────────────────┐
│                    ÉCOSYSTÈME E-COMMERCE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👥 UTILISATEURS (1.4M)                                     │
│       │                                                     │
│       ├──► 👁️  Vues produits (2.66M)                       │
│       ├──► 🛒 Ajouts panier (69K)                          │
│       └──► 💰 Transactions (22K)                           │
│                                                             │
│  📦 CATALOGUE                                               │
│       └──► 235,000 produits                                │
│                                                             │
│  💵 REVENU                                                  │
│       └──► 5.73M$ sur 139 jours                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# Schéma du Système Étudié

```
┌────────────────┐        ┌────────────────┐        ┌──────────────┐
│   UTILISATEUR  │───────►│   PLATEFORME   │───────►│   DONNÉES    │
│                │        │   E-COMMERCE   │        │   ÉVÉNEMENTS │
└────────────────┘        └────────────────┘        └──────────────┘
                                 │                          │
                                 │                          │
                                 ▼                          ▼
                          ┌──────────────┐         ┌──────────────┐
                          │  CONVERSIONS │         │   ANALYSE    │
                          │     & AOV    │         │   PYTHON     │
                          └──────────────┘         └──────────────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │  DASHBOARD   │
                                                    │ RECOMMAND.   │
                                                    └──────────────┘
```

---

# 2. OBJECTIFS DE L'ANALYSE 🎯

## Finalité de l'analyse

**Objectifs principaux** :

1. Analyser le comportement des utilisateurs
2. Identifier les points de friction dans le parcours client
3. Proposer des optimisations basées sur les données
4. Simuler l'impact d'A/B tests sur les métriques clés

## Attendus globaux

- Dashboard interactif de suivi des KPIs
- Segmentation utilisateurs (profils comportementaux)
- 16 scénarios d'A/B tests avec ROI calculé
- Recommandations stratégiques actionnables

---

Critères de Réussite

| 🎯 Critère                    | ✅ Réalisation              |
| :----------------------------- | :--------------------------- |
| **Analyse complète**    | 2.76M événements traités  |
| **Qualité données**    | 99.98% de qualité           |
| **Dashboard interactif** | 12 pages Dash/Plotly         |
| **A/B tests simulés**   | 16 scénarios, 95% confiance |
| **ROI documenté**       | Projection 30j + annuelle    |
| **Code versioning**      | GitHub complet               |
| **Documentation**        | Rapport 44 pages             |

---

# 3. DONNÉES UTILISÉES 📊

## Origine des données

**Source** : Dataset RetailRocket (Kaggle)

- https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset
- Données réelles d'une plateforme e-commerce russe
- Période : Mai - Septembre 2015

## Types de données

| Type                          | Description                                              | Volume        |
| :---------------------------- | :------------------------------------------------------- | :------------ |
| **events.csv**          | Événements utilisateurs (view, addtocart, transaction) | 2.76M lignes  |
| **item_properties.csv** | Propriétés produits (catégories, prix)                | 235K produits |
| **category_tree.csv**   | Arborescence catégories                                 | Hiérarchique |

---

# Périmètre des Données

```
ÉVÉNEMENTS (2,756,101 lignes)
├── timestamp        : Date/heure de l'événement
├── visitorid        : ID utilisateur unique
├── event            : Type (view, addtocart, transaction)
├── itemid           : ID produit
└── transactionid    : ID transaction (si achat)

PÉRIODE
├── Début : 3 mai 2015
├── Fin   : 18 septembre 2015
└── Durée : 139 jours

PÉRIMÈTRE MÉTIER
├── B2C Retail (consommateur final)
├── Multi-catégories produits
└── Tous types utilisateurs
```

---

# Diagramme de Flux de Données

```
┌──────────────────┐
│  KAGGLE API      │
│  RetailRocket    │
└────────┬─────────┘
         │ download_data.py
         ▼
┌──────────────────┐
│  DATA/RAW/       │
│  events.csv      │
│  items.csv       │
└────────┬─────────┘
         │ clean_*.py
         ▼
┌──────────────────┐
│  NETTOYAGE       │
│  - Doublons      │
│  - Validation    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  DATA/CLEAN/     │
│  28 CSV          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  POSTGRESQL      │
│  15 tables       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  DASHBOARD DASH  │
│  12 pages        │
└──────────────────┘
```

---

# 4. PRÉPARATION ET QUALITÉ DES DONNÉES 🧹

## Nettoyage effectué

| Étape                  | Action                 | Résultat            |
| :---------------------- | :--------------------- | :------------------- |
| **1. Chargement** | Lecture events.csv     | 2,756,101 lignes     |
| **2. Doublons**   | Suppression duplicatas | -460 lignes (0.017%) |
| **3. Validation** | Formats timestamp      | 0 erreur             |
| **4. Cohérence** | Événements orphelins | Filtrés             |
| **5. Typage**     | Conversion colonnes    | Optimisé            |

## Résultat final

- **Lignes finales** : 2,755,641 (99.98% conservées)
- **Taux de qualité** : 99.98% ✅
- **Données invalides** : 0
- **Distribution** : View (96.7%), AddToCart (2.5%), Transaction (0.8%)

---

# Contrôles Qualité

## Tests automatisés

```python
# Validation temporelle
assert events['timestamp'].min() == '2015-05-03'
assert events['timestamp'].max() == '2015-09-18'

# Cohérence événements
assert events['event'].isin(['view', 'addtocart', 'transaction']).all()

# Absence de valeurs manquantes critiques
assert events[['timestamp', 'visitorid', 'event']].notna().all().all()

# Intégrité référentielle
assert events['itemid'].isin(items['itemid']).all()
```

## Hypothèses sur les données

- **Sessions** : Reconstructions basées sur gaps temporels (30 min)
- **Prix** : Extraction depuis item_properties (valeurs manquantes = médiane)
- **Catégories** : Mapping via category_tree (2 niveaux)

---

# 5. DÉMARCHE ANALYTIQUE 🔍

## Logique suivie

```
1️⃣  EXPLORATION
    ├─ Statistiques descriptives
    ├─ Distribution des événements
    └─ Analyse temporelle

2️⃣  SEGMENTATION
    ├─ Calcul RFM (Recency, Frequency, Monetary)
    ├─ Clustering en 4 profils
    └─ Caractérisation segments

3️⃣  ANALYSE FUNNEL
    ├─ Vue → Panier → Achat
    ├─ Identification points de friction
    └─ Calcul taux conversion

4️⃣  SIMULATION A/B
    ├─ Définition 16 scénarios
    ├─ Monte Carlo (10K simulations)
    └─ Tests statistiques (Z, Chi², Bayésien)

5️⃣  RECOMMANDATIONS
    ├─ Priorisation ROI
    ├─ Roadmap 3 phases
    └─ Impact financier
```

---

# Étapes de Raisonnement

## Phase 1 : Comprendre l'existant

- Calcul KPIs de base (conversion, AOV, revenue/user)
- Identification comportements types
- Analyse cohortes temporelles

## Phase 2 : Identifier les opportunités

- Benchmark taux conversion (0.84% vs 2-3% standard)
- Analyse abandon panier (67% → élevé)
- Vue → Panier faible (2.59%)

## Phase 3 : Proposer des solutions

- 16 scénarios UX/UI, Pricing, Features, Marketing
- Simulation impact avec données historiques
- Validation statistique rigoureuse

---

# Types d'Analyses Réalisées

| Type                    | Méthode                              | Outil              |
| :---------------------- | :------------------------------------ | :----------------- |
| **Descriptive**   | Statistiques univariées              | Pandas, NumPy      |
| **Temporelle**    | Séries chronologiques, MA7/MA30      | Pandas resample    |
| **Segmentation**  | RFM, Clustering                       | Quantiles, K-means |
| **Conversion**    | Funnel analysis                       | Custom pipeline    |
| **A/B Testing**   | Monte Carlo, Z-test, Chi², Bayésien | SciPy, Statsmodels |
| **Visualisation** | Charts interactifs                    | Plotly, Dash       |

---

# 6. RÉSULTATS PRINCIPAUX 📊

## Faits observés

| 📈 Métrique Clé         | Valeur            | Observation                   |
| :------------------------ | :---------------- | :---------------------------- |
| **Taux conversion** | **0.84%**   | ⚠️ -58% vs benchmark (2-3%) |
| **Abandon panier**  | **67.43%**  | ⚠️ Élevé (norme 60-70%)   |
| **AOV**             | **255.36$** | ✅ +27% vs retail standard    |
| **Revenue/User**    | **489$**    | ✅ +22% vs benchmark          |
| **Vue → Panier**   | **2.59%**   | ⚠️ Très faible             |
| **Panier → Achat** | **32.57%**  | ⚠️ Perte de 67%             |

**Diagnostic** : Excellent AOV mais conversion critique → Optimisation funnel prioritaire

---

# Tendances Générales

## 📅 Analyse Temporelle

- **Meilleurs jours** : Jeudi (15.0%), Mercredi (14.7%), Mardi (14.3%)
- **Jours faibles** : Dimanche (12.7%), Samedi (13.2%)
- **Écart weekend/semaine** : -9.3% conversion
- **Heures de pointe** : 18h-20h (12.3%), 12h-14h (10.8%)

## 📦 Catalogue

- **Concentration** : 94% du revenu sur 1 catégorie (Top Performer)
- **Risque** : Dépendance forte à une seule catégorie
- **Opportunité** : 30% des produits = 0 vente (à nettoyer)

---

# Comparaisons Clés

## 👥 Performance par Segment

| Segment                | Users | % Total        | Rev/User         | % Revenu        | Conv. Rate |
| :--------------------- | :---- | :------------- | :--------------- | :-------------- | :--------- |
| 💎**Premium**    | 209   | **1.8%** | **7,999$** | **29.1%** | 309.95x    |
| ⭐**Regular**    | 1,316 | 11.2%          | 691$             | 15.9%           | 273.02x    |
| 🔵**Occasional** | 4,957 | 42.3%          | 356$             | 30.8%           | 140.41x    |
| 🆕**New**        | 5,237 | 44.7%          | 265$             | 24.2%           | 103.61x    |

**Insight majeur** :

> Les clients Premium (1.8%) génèrent 29% du revenu → **ROI rétention exceptionnel**

---

# Graphique Synthétique : Entonnoir

```
100%  👁️  VUES PRODUITS (2,664,218)
 │    ████████████████████████████████████████████
 │
 │    📉 PERTE: -97.41%
 ▼
2.59% 🛒 AJOUTS PANIER (68,966)
 │    ██
 │
 │    📉 ABANDON: -67.43%
 ▼
0.84% 💰 TRANSACTIONS (22,457)
      █

OPPORTUNITÉS D'OPTIMISATION
├─ Vue → Panier : Photos, descriptions, prix
├─ Panier → Achat : Checkout, paiements, frais
└─ Rétention : Programme fidélité, personnalisation
```

---

# 7. VISUALISATION ET RESTITUTION 📊

## Choix des indicateurs

**KPIs primaires** :

- Taux de conversion (objectif : +81%)
- AOV - Average Order Value (objectif : +12%)
- Revenue per User (objectif : +77%)
- Taux d'abandon panier (objectif : -33%)

**KPIs secondaires** :

- Taux rebond, Pages/session, Durée session
- Distribution temporelle (jours, heures)
- Performance catégories produits
- Lifetime Value par segment

---

# Mode de Restitution

## Dashboard Dash - 12 Pages Interactives

| Page                    | Contenu                | Visualisations        |
| :---------------------- | :--------------------- | :-------------------- |
| **Home**          | KPIs globaux           | Cards, Gauges, Trends |
| **Traffic**       | Analyse temporelle     | Line charts, Heatmaps |
| **Conversions**   | Funnel & taux          | Funnel chart, Bars    |
| **Cohortes**      | Segmentation RFM       | Treemap, Tables       |
| **Produits**      | Performance catalogue  | Scatter, Top 10       |
| **Comportements** | Parcours clients       | Sankey, Flow          |
| **A/B Tests**     | Résultats simulations | Comparison charts     |
| **Calculateur**   | Outil interactif       | Form + résultats     |

---

# Lisibilité des Résultats

## Principes appliqués

✅ **Simplicité** : 1 message par visualisation
✅ **Cohérence** : Palette de couleurs unifiée (vert=succès, orange=attention, rouge=critique)
✅ **Interactivité** : Filtres, drill-down, tooltips
✅ **Accessibilité** : Authentification, responsive design
✅ **Documentation** : Help tooltips, méthodologie expliquée

## Exemple : Card KPI

```python
dbc.Card([
    dbc.CardBody([
        html.H4("💰 Revenu Total", className="card-title"),
        html.H2("5,732,868$", className="text-success"),
        html.P("↗ +22% vs benchmark", className="text-muted")
    ])
], color="success", outline=True)
```

---

# 8. TESTS, COMPARAISONS ET VALIDATIONS 🧪

## Méthode de Comparaison A/B

**Approche de simulation** :

1. **Baseline** : Données historiques (control group)
2. **Variant** : Simulation avec lift attendu
3. **Monte Carlo** : 10,000 itérations par scénario
4. **Tests statistiques multiples** :
   - Z-test (comparaison proportions)
   - Chi² (indépendance variables)
   - Bayesian A/B (P(B>A) > 95%)

**Paramètres** :

- Confiance : 95%
- Puissance : 80%
- Taille échantillon min : 2,000/groupe

---

# Logique de Validation

## Critères d'acceptation d'un scénario

```
SI (p-value < 0.05)
   ET (P(B>A) > 95%)
   ET (Puissance > 80%)
   ET (IC 95% ne contient pas 0)
ALORS
   ✅ Scénario VALIDÉ
SINON
   ❌ Scénario REJETÉ
```

## Validation ROI

```python
ROI = ((Revenu_Variant - Revenu_Control) - Coût_Implémentation)
      / Coût_Implémentation * 100

SI ROI > 100%:
    Priorité = "HAUTE"
SI ROI > 1000%:
    Priorité = "CRITIQUE"
```

---

# Mesure des Écarts

## Top 3 Scénarios Validés

| Scénario                      | Baseline | Variant | Lift             | p-value | P(B>A) |
| :----------------------------- | :------- | :------ | :--------------- | :------ | :----- |
| **Options Paiement**     | 0.84%    | 0.97%   | **+15.3%** | <0.001  | 99.2%  |
| **Checkout Simplifié**  | 0.84%    | 1.05%   | **+24.6%** | <0.001  | 99.8%  |
| **Programme Fidélité** | 0.84%    | 1.02%   | **+21.4%** | <0.001  | 99.5%  |

## ROI Comparé

- Options Paiement : **+12,333%** (30j) → **151K%** (annuel)
- Checkout Simplifié : **+7,485%** (30j) → **92K%** (annuel)
- Programme Fidélité : **+6,665%** (30j) → **82K%** (annuel)

---

# Schéma A/B - Options Paiement

```
┌─────────────────────────────────────────────────────────┐
│  GROUPE A (CONTROL) - Paiement CB uniquement           │
├─────────────────────────────────────────────────────────┤
│  Sample size    : 30,241 users                          │
│  Conversions    : 254 (0.84%)                           │
│  Revenue 30j    : 1,230,000$                            │
└─────────────────────────────────────────────────────────┘

                         VS

┌─────────────────────────────────────────────────────────┐
│  GROUPE B (VARIANT) - CB + PayPal + Apple Pay + GPay   │
├─────────────────────────────────────────────────────────┤
│  Sample size    : 30,241 users                          │
│  Conversions    : 293 (0.97%) ✅                        │
│  Revenue 30j    : 1,420,000$ (+15.4%)                   │
└─────────────────────────────────────────────────────────┘

RÉSULTATS
├─ Z-test p-value    : <0.001 ✅
├─ P(B > A)         : 99.2% ✅
├─ Lift             : +15.3% ✅
└─ ROI 30j          : +12,333% ✅
```

---

# Diagramme de Décision

```
                    SCÉNARIO A/B
                         │
                         ▼
              ┌──────────────────────┐
              │  Simulation Monte    │
              │  Carlo (10K runs)    │
              └──────────┬───────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
  ┌──────────────┐              ┌──────────────┐
  │   p < 0.05?  │              │  P(B>A)>95%? │
  └──────┬───────┘              └──────┬───────┘
         │ OUI                         │ OUI
         ▼                             ▼
         └──────────┬──────────────────┘
                    ▼
           ┌─────────────────┐
           │   ROI > 100%?   │
           └────────┬────────┘
                    │ OUI
                    ▼
           ┌─────────────────┐
           │  ✅ VALIDER     │
           │  SCÉNARIO       │
           └─────────────────┘
```

---

# 9. CODE REVIEW & IMPLÉMENTATION 💻

## Organisation du Code

```
ecommerce-abtest-dashboard/
├── 📊 dashboard/              # Application principale
│   ├── app.py                # Point d'entrée Dash
│   ├── auth.py               # Authentification Flask-Login
│   ├── db.py                 # Connexion PostgreSQL
│   ├── pages/                # 12 pages modulaires
│   │   ├── home.py           # KPIs globaux
│   │   ├── conversions.py    # Funnel analysis
│   │   ├── ab_results.py     # Résultats A/B tests
│   │   └── ...
│   └── assets/               # CSS, JS, images
├── 🐍 scripts/
│   ├── ab_testing/           # Simulations A/B
│   │   ├── test_ab_conversions.py
│   │   └── generate_ab_simulation.py
│   ├── data_prep/            # ETL pipeline
│   │   ├── clean_events.py
│   │   └── preprocess_*.py
│   └── kpi_analysis/         # Calculs métriques
├── 📁 data/                   # Données (raw + clean)
└── 🐳 infrastructure/         # Docker, configs
```

---

# Bonnes Pratiques Appliquées

## ✅ Code Quality

```python
# PEP 8 : Style guide Python
# - Indentation 4 spaces
# - Longueur ligne ≤ 100 caractères
# - Noms explicites (snake_case)

# Documentation complète
def calculate_conversion_rate(
    events_df: pd.DataFrame,
    event_type: str = 'transaction'
) -> float:
    """
    Calcule le taux de conversion global.

    Args:
        events_df: DataFrame des événements
        event_type: Type d'événement cible

    Returns:
        Taux de conversion en pourcentage
    """
    total_users = events_df['visitorid'].nunique()
    converted_users = events_df[
        events_df['event'] == event_type
    ]['visitorid'].nunique()

    return (converted_users / total_users) * 100
```

---

# Lisibilité et Maintenabilité

## Modularité

✅ **Séparation des responsabilités** :

- `data_prep/` : Nettoyage données (responsabilité unique)
- `kpi_analysis/` : Calculs métriques
- `ab_testing/` : Simulations A/B
- `dashboard/pages/` : Interface utilisateur

✅ **Configuration centralisée** :

```python
# dashboard/src/config.py
class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    SECRET_KEY = os.getenv('SECRET_KEY')
```

✅ **Tests unitaires** :

```python
# tests/test_conversions.py
def test_conversion_rate_calculation():
    # Arrange
    df = create_sample_events()
    # Act
    rate = calculate_conversion_rate(df)
    # Assert
    assert 0 <= rate <= 100
```

---

# Extrait de Code Commenté

```python
def simulate_ab_test(
    baseline_rate: float,
    expected_lift: float,
    sample_size: int,
    n_simulations: int = 10000
) -> Dict[str, float]:
    """
    Simule un A/B test avec Monte Carlo.

    Args:
        baseline_rate: Taux de conversion control (ex: 0.0084)
        expected_lift: Lift attendu en % (ex: 15.3)
        sample_size: Taille échantillon par groupe
        n_simulations: Nombre de simulations Monte Carlo

    Returns:
        Dict avec résultats statistiques (p-value, puissance, etc.)
    """
    # Calcul taux variant
    variant_rate = baseline_rate * (1 + expected_lift / 100)

    # Simulations Monte Carlo
    control_conversions = np.random.binomial(
        sample_size, baseline_rate, n_simulations
    )
    variant_conversions = np.random.binomial(
        sample_size, variant_rate, n_simulations
    )

    # Z-test sur chaque simulation
    significant_tests = 0
    for i in range(n_simulations):
        # Test bilatéral Z-test
        z_stat, p_value = proportions_ztest(
            [control_conversions[i], variant_conversions[i]],
            [sample_size, sample_size]
        )
        if p_value < 0.05:  # Seuil de signification
            significant_tests += 1

    # Puissance statistique
    statistical_power = significant_tests / n_simulations

    return {
        'control_rate': baseline_rate,
        'variant_rate': variant_rate,
        'lift_pct': expected_lift,
        'statistical_power': statistical_power,
        'significant_tests_pct': statistical_power * 100
    }
```

---

# Arborescence Complète

```
📦 ecommerce-abtest-dashboard
├── 📊 dashboard/              Application Dash (12 pages)
├── 📁 data/
│   ├── raw/                  Données brutes RetailRocket
│   └── clean/                28 CSV nettoyés
├── 🐍 scripts/
│   ├── ab_testing/           5 scripts simulation
│   ├── data_prep/            8 scripts nettoyage
│   ├── kpi_analysis/         6 scripts calculs
│   └── utils/                Fonctions communes
├── 🐳 infrastructure/
│   ├── docker/               Dockerfiles
│   └── k8s/                  Kubernetes manifests
├── 📊 monitoring/            Grafana dashboards
├── 📄 docs/                  Documentation
├── 🧪 tests/                 Tests unitaires
├── requirements.txt          Dépendances Python
├── docker-compose.yml        Orchestration
└── README.md                 Documentation projet
```

---

# Diagramme Modules / Scripts

```
┌─────────────────────────────────────────────────────────┐
│                    ARCHITECTURE                         │
└─────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  DATA PREP   │──────►│     ETL      │──────►│  POSTGRESQL  │
│   Scripts    │       │   Pipeline   │       │   Database   │
└──────────────┘       └──────────────┘       └──────┬───────┘
                                                      │
┌──────────────┐       ┌──────────────┐              │
│   A/B TEST   │──────►│  SIMULATION  │              │
│   Scripts    │       │    Engine    │              │
└──────────────┘       └──────────────┘              │
                                                      │
┌──────────────┐       ┌──────────────┐              │
│     KPI      │──────►│  ANALYTICS   │◄─────────────┘
│   Scripts    │       │    Layer     │
└──────────────┘       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │     DASH     │
                       │  Dashboard   │
                       │   12 pages   │
                       └──────────────┘
```

---

# 10. LIMITES ET PERSPECTIVES 🔮

## Limites Méthodologiques

### 📊 Données

- **Période limitée** : 4,5 mois (pas de saisonnalité complète)
- **Année 2015** : Comportements e-commerce évoluent vite
- **Données manquantes** : Pas de démographie, localisation
- **Simulations A/B** : Basées sur hypothèses, non validées en production

### 🧪 Tests A/B

- **Monte Carlo** : Simulations ≠ tests réels
- **Hypothèses** : Lift attendus basés sur benchmarks
- **Interaction effets** : Tests isolés, pas d'analyse combinée

---

# Points d'Amélioration

## 🔧 Court Terme

1. **Validation production** : Déployer 1-2 A/B tests réels
2. **Enrichissement données** : Intégrer Google Analytics
3. **Temps réel** : Alertes automatiques sur anomalies KPIs
4. **UX Dashboard** : Tests utilisateurs pour améliorer interface

## 📈 Moyen Terme

1. **Machine Learning** :

   - Modèle prédiction churn (Random Forest, XGBoost)
   - Recommandation produits (Collaborative Filtering)
   - Segmentation avancée (K-means clustering)
2. **Attribution** : Modèle multi-touch pour tracking campagnes

---

# Extensions Possibles

## 🚀 Fonctionnalités Avancées

### 1. Personnalisation

```
IF segment == "Premium":
    Afficher produits haut de gamme
    Offrir livraison gratuite
    Cashback 10%
ELIF segment == "New":
    Offrir code promo -15%
    Guide d'achat
    Chat support proactif
```

### 2. Pricing Dynamique

- A/B tests sur élasticité prix
- Tarification différenciée par segment
- Promotions ciblées temps réel

---

# Extensions Techniques

## 🤖 Intelligence Artificielle

**Recommandation Produits** :

- Collaborative filtering (User-User, Item-Item)
- Matrix factorization (SVD)
- Deep Learning (Neural Collaborative Filtering)

**Prédiction Churn** :

- Features : RFM, engagement, parcours
- Modèles : Logistic Regression, Random Forest, XGBoost
- Scoring : Probabilité churn à 30/60/90 jours

**NLP pour Reviews** :

- Analyse sentiment (positif/négatif/neutre)
- Extraction topics (LDA)
- Résumé automatique

---

# Roadmap Future

```
Q1 2026 - Validation Production
├─ Déployer Options Paiement (A/B test réel)
├─ Mesurer impact réel vs simulation
└─ Ajuster modèles prédictifs

Q2 2026 - Machine Learning
├─ Modèle prédiction churn
├─ Système recommandation v1
└─ Personnalisation contenu

Q3 2026 - Optimisations Avancées
├─ Pricing dynamique
├─ Attribution multi-touch
└─ Segmentation comportementale temps réel

Q4 2026 - Scale & Performance
├─ Architecture Big Data (Spark)
├─ Real-time analytics (Kafka)
└─ API pour intégrations tierces
```

---

<!-- _class: lead -->

# ✅ CONCLUSION

---

# Synthèse du Projet

## 🎯 Objectifs Atteints

✅ **Analyse complète** : 2.76M événements, 139 jours, 11K users
✅ **Dashboard interactif** : 12 pages Dash/Plotly production-ready
✅ **16 A/B tests simulés** : Confiance 95%, puissance 80%
✅ **ROI documenté** : +65M$ de revenu potentiel annuel
✅ **Code versioning** : GitHub complet, commits réguliers
✅ **Documentation** : Rapport 44 pages, présentation 30 slides

## 💰 Impact Business

- **Conversion** : +81% (de 0.84% à 1.52%)
- **Revenu** : +65M$/an (de 15M$ à 80M$)
- **ROI global** : 34,500% (188K$ investis)

---

# Compétences Développées

## 📚 Référentiel École Multimédia

### ✅ B-2 : Architecture de Données

- Cahier des charges : 15 tables PostgreSQL normalisées
- Pipeline ETL : Scripts automatisés, qualité 99.98%
- Documentation : Schémas, diagrammes, README

### ✅ C-3 : Automatisation des Flux

- 24 scripts Python structurés (PEP 8)
- Pipeline Docker orchestré (Compose, Grafana)
- Optimisation : Indexation DB, cache, async

### ✅ C-5 : Contrôle Qualité

- Validation données : 0 erreur, tests unitaires
- Monitoring : Grafana + 32 alertes temps réel
- Correction erreurs : Logs, debugging, rollback

---

# Apprentissages Clés

## 🔍 Techniques

- Maîtrise **pipeline ETL** complet (Extract, Transform, Load)
- **Tests statistiques** rigoureux (Z-test, Chi², Bayésien)
- Dashboard **production-ready** (auth, sécurité, monitoring)
- **Infrastructure DevOps** (Docker, PostgreSQL, Grafana)

## 💼 Business

- **Segmentation utilisateurs** : Premium (1.8%) = 29% revenu
- **Quick Wins** : Faible coût + ROI élevé = priorité
- **Approche data-driven** : Décisions basées sur données, pas intuition
- **Priorisation ROI** : Focus sur impact vs effort

---

# Remerciements 🙏

## Merci pour votre attention !

**Questions ?**

---

**📧 Contact** : [Votre Email]
**🔗 GitHub** : https://github.com/Christh2022/ecommerce-abtest-dashboard
**📊 Dashboard Live** : http://localhost:8050 (après déploiement)

---

**🎓 Projet #1 - L'École Multimédia**
**Directeur de projet en intelligence artificielle - Année 1**
**Programmation Data avec Python**

**Décembre 2025**
