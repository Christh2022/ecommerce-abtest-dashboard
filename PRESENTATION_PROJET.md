---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: ' Analyse E-Commerce - RetailRocket Dataset'
footer: 'Projet #1 - L\'École Multimédia - Décembre 2025'
---
<style>
section {
 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
 color: #1e88e5;
 border-bottom: 3px solid #1e88e5;
 padding-bottom: 10px;
}
h2 {
 color: #43a047;
}
.columns {
 display: grid;
 grid-template-columns: repeat(2, minmax(0, 1fr));
 gap: 1rem;
}
.highlight {
 background-color: #fff3cd;
 border-left: 5px solid #ffc107;
 padding: 10px;
 margin: 10px 0;
}
.success {
 background-color: #d4edda;
 border-left: 5px solid #28a745;
 padding: 10px;
 margin: 10px 0;
}
.warning {
 background-color: #f8d7da;
 border-left: 5px solid #dc3545;
 padding: 10px;
 margin: 10px 0;
}
</style>

<!-- _class: lead -->

# ANALYSE DE PERFORMANCES

# ET OPTIMISATION

# D'UN SITE E-COMMERCE

**Projet #1 - Programmation Data avec Python**

---

## Programme & Contexte 

**École** : L'École Multimédia
**Formation** : Directeur de projet en intelligence artificielle - Année 1
**Étudiant** : [Votre Nom]
**Date** : Décembre 2025

**Objectif du projet** :
Analyser les données d'une plateforme e-commerce et proposer des optimisations basées sur des A/B tests simulés.

---

<!-- _class: lead -->

# SOMMAIRE

1. **Dataset & Méthodologie**
2. **Résultats Clés**
3. **Analyse des Performances**
4. **Tests A/B - Top 5 Optimisations**
5. **Recommandations Stratégiques**
6. **Impact Financier**
7. **Conclusion**

---

# DATASET RETAILROCKET

<div class="columns">
<div>

## Source des Données

- **Origine** : Kaggle
- **Dataset** : RetailRocket E-commerce
- **Période** : Mai - Sept 2015
- **Durée** : **139 jours**

</div>
<div>



## Volume de Données

- **Événements** : 2,76M
- **Utilisateurs** : 1,4M
- **Produits** : 235K
- **Qualité** : **99.98%** 

</div>
</div>


---

# MÉTHODOLOGIE

## Pipeline ETL

```
Données Brutes (RetailRocket)
 ↓ Nettoyage (460 doublons supprimés)
 ↓ Validation (0 erreur)
 ↓ Transformation (Feature Engineering)
 ↓ Agrégations (Daily, Weekly, Monthly)
 ↓ Segmentation (4 profils utilisateurs)
 ↓
PostgreSQL → Dashboard Dash (12 pages)
```

**Taux de qualité final** : 99.98% 

---

# TESTS A/B - MÉTHODOLOGIE

<div class="columns">
<div>

## Approche

- **16 scénarios** testés
- **Monte Carlo** : 10,000 simulations
- **Confiance** : 95%
- **Puissance** : 80%

</div>
<div>


## Tests Statistiques

- Z-test (proportions)
- Chi² (indépendance)
- Bayésien (P(B>A) > 95%)
- ROI 30j + annuel

</div>
</div>


---

<!-- _class: lead -->

# RÉSULTATS CLÉS

---

# MÉTRIQUES GLOBALES

| KPI | Valeur | Évaluation |
| :----------------------------- | :---------------- | :------------------------ |
| **Revenu Total** | **5,73M$** | Performance solide |
| ️**Transactions** | **22,457** | Base d'analyse robuste |
| **Panier Moyen (AOV)** | **255,36$** | +27% vs retail |
| **Utilisateurs** | **11,719** | 4 segments identifiés |
| **Taux Conversion** | **0.84%** | ️ À optimiser (-58%) |
| **Abandon Panier** | **67.43%** | ️ Point critique |

---

# ENTONNOIR DE CONVERSION

```
┌────────────────────────────────────────────────┐
│ ️ VUES 2,664,218 (100%) │
│ ████████████████████████████████████████ │
└──────────────────┬─────────────────────────────┘
 │ -97.41%
 ▼
┌────────────────────────────────────────────────┐
│ PANIERS 68,966 (2.59%) │
│ ██ │
└──────────────────┬─────────────────────────────┘
 │ -67.43% ABANDON
 ▼
┌────────────────────────────────────────────────┐
│ ACHATS 22,457 (0.84%) │
│ █ │
└────────────────────────────────────────────────┘
```

---

# SEGMENTATION UTILISATEURS

| Segment | Users | Rev/User | % Revenu | Stratégie |
| :---------------------- | :---------- | :--------------- | :---------- | :------------------ |
| ** Premium** | 209 (1.8%) | **7,999$** | 29.1% | Rétention VIP |
| ** Regular** | 1,316 (11%) | 691$ | 15.9% | ️ Upsell Premium |
| ** Occasional** | 4,957 (42%) | 356$ | 30.8% | Fréquence achat |
| **🆕 New** | 5,237 (45%) | 265$ | 24.2% | Conversion |

<div class="highlight">

** Insight** : Les Premium (1.8%) génèrent 29% du revenu → **Focus rétention critique**

</div>

---

<!-- _class: lead -->

# TOP 5 OPTIMISATIONS A/B

---

# #1 - OPTIONS PAIEMENT MULTIPLES

<div class="success">

## Ajouter PayPal, Apple Pay, Google Pay

</div>

| Métrique | Impact |
| :--------------------------- | :-------------------- |
| **Lift Conversion** | **+15.3%** |
| **ROI 30 jours** | **+12,333%** |
| **ROI Annuel** | **+151,215%** |
| **Coût** | 10,000$ |
| **Revenu add. annuel** | **15,1M$** |

<div class="highlight">

** PRIORITÉ CRITIQUE** - Déploiement immédiat recommandé

</div>

---

# #2 - CHECKOUT SIMPLIFIÉ

<div class="success">

## Réduire de 5 à 2 étapes le checkout

</div>

| Métrique | Impact |
| :--------------------------- | :----------------- |
| **Lift Conversion** | **+24.6%** |
| **ROI 30 jours** | **+7,485%** |
| **ROI Annuel** | **+92,212%** |
| **Coût** | 25,000$ |
| **Revenu add. annuel** | **23,1M$** |

<div class="warning">

** PRIORITÉ HAUTE** - Combat l'abandon panier (67%)

</div>

---

# #3 - PROGRAMME FIDÉLITÉ

<div class="success">

## Points + Cashback + Avantages VIP

</div>

| Métrique | Impact |
| :--------------------------- | :----------------- |
| **Lift Conversion** | **+21.4%** |
| **ROI 30 jours** | **+6,665%** |
| **ROI Annuel** | **+82,230%** |
| **Coût** | 25,000$ |
| **Revenu add. annuel** | **20,6M$** |

<div class="highlight">

** QUICK WIN** - Rétention Premium (29% du revenu)

</div>

---

# #4 - NETTOYAGE CATALOGUE

<div class="success">

## Supprimer produits sous-performants

</div>

| Métrique | Impact |
| :--------------------------- | :------------------------------ |
| **Lift Conversion** | **+34.1%** |
| **ROI 30 jours** | **+4,231%** |
| **Coût** | **5,000$** (très faible) |
| **Revenu add. annuel** | **2,6M$** |

<div class="highlight">

** QUICK WIN** - 30% des produits = 0 vente → simplicité ++

</div>

---

# ️ #5 - SYSTÈME DE REVIEWS

<div class="success">

## Avis clients + Notes + Proof sociale

</div>

| Métrique | Impact |
| :--------------------------- | :----------------- |
| **Lift Conversion** | **+42.6%** |
| **ROI 30 jours** | **+1,698%** |
| **ROI Annuel** | **+21,778%** |
| **Coût** | 15,000$ |
| **Revenu add. annuel** | **3,3M$** |

<div class="warning">

** INSIGHT** - 88% des clients lisent les avis avant achat

</div>

---

<!-- _class: lead -->

# IMPACT FINANCIER GLOBAL

---

# PROJECTION FINANCIÈRE

<div class="columns">
<div>

## Actuel

- **Revenu annuel** : 15M$
- **Conversion** : 0.84%
- **AOV** : 255$
- **Rev/User** : 489$

</div>
<div>


## Avec Optimisations

- **Revenu annuel** : **80M$**
- **Conversion** : **1.52%** (+81%)
- **AOV** : **285$** (+12%)
- **Rev/User** : **865$** (+77%)

</div>
</div>


<div class="success">

## GAIN ANNUEL : +65M$ DE REVENU SUPPLÉMENTAIRE

</div>

---

# ROI GLOBAL

| Phase | Scénarios | Investissement | Revenu Annuel | ROI |
| :---------------------------- | :------------------------------ | :----------------------- | :------------ | :-- |
| **Phase 1** (0-3 mois) | Paiements + Catalogue + Reviews | 30K$ | +20M$ | 66,567% | |
| **Phase 2** (3-6 mois) | Checkout + Fidélité + Photos | 80K$ | +38M$ | 47,400% | |
| **Phase 3** (6-12 mois) | Pricing + Weekend + Perso | 78K$ | +7M$ | 8,874% | |

<div class="highlight">

### TOTAL : 188K$ investis → 65M$ revenu = **34,500% ROI**

</div>

---

# FEUILLE DE ROUTE

## Phase 1 : Quick Wins (0-3 mois) 

- Nettoyage catalogue (2 semaines, 5K$)
- Options paiement (1 mois, 10K$)
- Système reviews (6 semaines, 15K$)

## Phase 2 : Optimisations Majeures (3-6 mois) 

- Checkout simplifié (2 mois, 25K$)
- Programme fidélité (3 mois, 25K$)
- Amélioration photos (2 mois, 30K$)

## Phase 3 : Long Terme (6-12 mois) 

- Pricing dynamique, Opti weekend, Personnalisation

---

# RECOMMANDATIONS PAR SEGMENT

<div class="columns">
<div>

## Premium (1.8%)

- Programme VIP exclusif
- Personal shopper
- Cashback 5-10%
- **Impact** : +5M$/an

</div>
<div>


## Regular (11%)

- Conversion vers Premium
- Paliers fidélité
- Recommandations IA
- **Impact** : +3M$/an

</div>
</div>


<div class="highlight">

## 🆕 Occasional + New (87%)

Checkout simplifié + Paiements + Reviews → **+18M$/an**

</div>

---

<!-- _class: lead -->

# STACK TECHNIQUE

---

# TECHNOLOGIES UTILISÉES

<div class="columns">
<div>

## Backend

- **Python 3.12**
- Pandas, NumPy
- SciPy, Statsmodels
- PostgreSQL 15

</div>
<div>


## Frontend

- **Dash/Plotly** (12 pages)
- Bootstrap (Dark theme)
- Charts interactifs
- Authentication

</div>
</div>


<div class="columns">
<div>

## Infrastructure

- Docker Compose
- Grafana + Prometheus
- Monitoring temps réel

</div>
<div>


## Sécurité

- Flask-Login + bcrypt
- Rate limiting (anti-DDoS)
- 41 tests automatisés

</div>
</div>


---

# STRUCTURE DU PROJET

```
ecommerce-abtest-dashboard/
├── dashboard/ # Application Dash (12 pages)
│ ├── app.py # Point d'entrée
│ ├── auth.py # Authentification
│ └── pages/ # Pages interactives
├── data/
│ ├── raw/ # RetailRocket brut
│ └── clean/ # 28 CSV nettoyés
├── scripts/
│ ├── ab_testing/ # 5 scripts simulation
│ ├── data_prep/ # ETL pipeline
│ └── kpi_analysis/ # Analyses
├── infrastructure/ # Docker, K8s
└── monitoring/ # Grafana dashboards
```

---

# DASHBOARD INTERACTIF

## 12 Pages de Visualisation

1. **Home** - KPIs globaux
2. **Traffic** - Analyse temporelle
3. **Conversions** - Funnel & taux
4. **Cohortes** - Segmentation RFM
5. **Produits** - Performance catalogue
6. **Comportements** - Parcours clients
7. **A/B Tests** - Résultats simulations
8. **Visualisations A/B** - Charts
9. **Méthodologie** - Guide statistique
10. **Calculateur A/B** - Outil interactif
11. **About** - Documentation
12. **Login/Logout** - Authentification

---

# COMPÉTENCES DÉVELOPPÉES

<div class="success">

## B-2 : Architecture de Données

- 15 tables PostgreSQL normalisées
- Pipeline ETL automatisé
- Documentation complète

</div>

<div class="success">

## C-3 : Automatisation des Flux

- 24 scripts Python
- Pipeline Docker orchestré
- Optimisation performances

</div>

<div class="success">

## C-5 : Contrôle Qualité

- 99.98% qualité données
- Tests unitaires & intégration
- Monitoring Grafana

</div>

---

<!-- _class: lead -->

# CONCLUSION

---

# LIVRABLES RÉALISÉS

## Analyse Complète

- 2,76M événements analysés
- 16 scénarios A/B testés avec 95% confiance
- 4 segments utilisateurs identifiés
- 139 jours de données nettoyées (99.98%)

## Dashboard Production

- 12 pages interactives Dash/Plotly
- Authentification sécurisée
- Infrastructure Docker
- Monitoring temps réel

## Documentation

- Rapport d'analyse 44 pages
- GitHub avec historique complet
- Code commenté (PEP 8)

---

# APPRENTISSAGES CLÉS

## Techniques

- Maîtrise pipeline ETL complet
- Tests statistiques rigoureux (Z-test, Chi², Bayésien)
- Dashboard production-ready
- Infrastructure Docker multi-services

## Business

- Importance segmentation pour stratégies ciblées
- Impact majeur des "Quick Wins" (faible coût, ROI élevé)
- Approche data-driven pour décisions produit
- Valeur Premium : 1.8% users = 29% revenu

---

# PERSPECTIVES D'AMÉLIORATION

<div class="columns">
<div>

## Machine Learning

- Modèle prédiction churn
- Système recommandation
- Personnalisation contenu
- Attribution multi-touch

</div>
<div>


## Optimisations

- Alertes temps réel
- A/B tests en production
- Analyse saisonnalité
- Segmentation avancée

</div>
</div>


<div class="highlight">

** Validation en production nécessaire** - Données simulées à confirmer avec tests réels

</div>

---

# IMPACT ATTENDU

<div class="success">

## Objectifs 12 Mois

| KPI | Baseline | Objectif | Gain |
| :------------------- | :---------------- | :-------------- | :------------- |
| **Conversion** | 0.84% | 1.52% | **+81%** |
| **Revenu** | 15M$ | 80M$ | **+65M$** | |
| **AOV** | 255$ | 285$ | **+12%** | |
| **Rev/User** | 489$ | 865$ | **+77%** | |

</div>

---

<!-- _class: lead -->

# MERCI !

## Questions ?

---

** Contact** : [Votre Email]
** GitHub** : https://github.com/Christh2022/ecommerce-abtest-dashboard
** Dashboard Live** : http://localhost:8050

---

** L'École Multimédia - Projet #1**
**Directeur de projet en intelligence artificielle - Année 1**
**Décembre 2025**
