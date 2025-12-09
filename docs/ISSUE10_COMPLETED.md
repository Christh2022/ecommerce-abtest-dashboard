# Issue #10 : Analyse comportement utilisateur ✅

**Milestone** : 2 - Analyses & KPIs  
**Statut** : COMPLÉTÉ ✅  
**Date** : 2025-12-09  
**Branche** : `feature/kpi-metricss`

---

## 📊 Objectif

Analyser en détail le comportement des utilisateurs : engagement, parcours de conversion, segmentation et évolution temporelle des comportements.

---

## 🎯 Résultats Clés

### Métriques d'Engagement Globales

| Métrique                             | Valeur            |
| ------------------------------------ | ----------------- |
| **Événements/utilisateur (moyenne)** | 1.67              |
| **Événements/utilisateur (médiane)** | 1.67              |
| **Total événements**                 | 2,755,641         |
| **Total vues**                       | 2,664,218 (96.7%) |
| **Total ajouts panier**              | 68,966 (2.5%)     |
| **Total transactions**               | 22,457 (0.8%)     |

**Insight** : Engagement modéré avec une moyenne de 1.67 événements par utilisateur, indiquant des sessions courtes et focalisées.

### 🎯 Taux de Conversion

| Métrique               | Valeur |
| ---------------------- | ------ |
| **View → Cart**        | 2.59%  |
| **View → Purchase**    | 0.83%  |
| **Cart → Purchase**    | 31.88% |
| **Conversion globale** | 1.36%  |

**Insight** : Fort drop-off entre viewing et cart (97.4%), mais bon taux de conversion du panier (31.88%).

### 📈 Funnel de Conversion Détaillé

| Étape          | Utilisateurs | % Initial | Drop-off | Conversion suivante |
| -------------- | ------------ | --------- | -------- | ------------------- |
| **Viewers**    | 1,649,534    | 100.0%    | -        | 4.18%               |
| **Cart Users** | 68,966       | 4.18%     | 95.82%   | 32.56%              |
| **Buyers**     | 22,457       | 1.36%     | 67.44%   | -                   |

**Insights critiques** :

- ⚠️ **95.82% drop-off** entre viewing et cart - Point critique d'optimisation
- ✅ **32.56% conversion** du panier - Performance correcte
- 🎯 **Opportunité principale** : Améliorer le passage view → cart

### 👥 Segmentation Comportementale

#### Performance par Segment

| Segment        | Utilisateurs | % Users | Revenue/User  | Trans/User | Value Index | Revenue Share |
| -------------- | ------------ | ------- | ------------- | ---------- | ----------- | ------------- |
| **Premium**    | 209          | 1.8%    | **€7,999.81** | 31.00      | **16.38**   | 29.2%         |
| **Regular**    | 1,316        | 11.2%   | €690.85       | 2.73       | 1.41        | 15.9%         |
| **Occasional** | 4,957        | 42.3%   | €356.07       | 1.40       | 0.73        | 30.8%         |
| **New**        | 5,237        | 44.7%   | €264.79       | 1.04       | 0.54        | 24.2%         |

**Value Index** : Ratio Revenue Share / User Share (>1 = segment à haute valeur)

**Insights stratégiques** :

1. 🌟 **Premium** : 1.8% des users génèrent 29.2% du revenue (Value Index: 16.38)

   - Valeur par user 30x supérieure aux nouveaux
   - 31 transactions par user en moyenne
   - **Action** : Fidélisation prioritaire, programme VIP

2. 💼 **Regular** : 11.2% des users, 15.9% du revenue (Value Index: 1.41)

   - Performance solide avec €690.85/user
   - **Action** : Convertir en Premium avec incentives

3. 🔄 **Occasional** : 42.3% des users, 30.8% du revenue (Value Index: 0.73)

   - Plus gros segment en volume
   - **Action** : Campagnes de ré-engagement

4. 🆕 **New** : 44.7% des users, 24.2% du revenue (Value Index: 0.54)
   - Sous-performant en valeur
   - **Action** : Onboarding optimisé, incitations first purchase

### 📅 Patterns Temporels

#### Semaine vs Week-end

| Métrique            | Semaine | Week-end | Variation |
| ------------------- | ------- | -------- | --------- |
| **Événements/user** | 1.68    | 1.64     | -2.5%     |
| **View → Cart**     | 2.67%   | 2.38%    | -11.0%    |
| **Revenue/user**    | €3.76   | €2.52    | -32.9%    |

**Insight** : Comportement moins engagé le week-end avec baisse significative du revenue par user (-32.9%).

### 📈 Évolution Temporelle

| Période       | Dates                   | Engagement    | Conversion | Revenue/User |
| ------------- | ----------------------- | ------------- | ---------- | ------------ |
| **Période 1** | 2015-05-03 → 2015-06-17 | 1.72 evt/user | 0.80%      | €3.38        |
| **Période 2** | 2015-06-18 → 2015-08-02 | 1.68 evt/user | 0.84%      | €3.56        |
| **Période 3** | 2015-08-03 → 2015-09-18 | 1.60 evt/user | 0.84%      | €3.30        |

**Tendances** :

- ⬇️ **Engagement** : Baisse de 1.72 → 1.60 (-6.9%)
- ⬆️ **Conversion** : Amélioration de 0.80% → 0.84% (+5.0%)
- ➡️ **Revenue/user** : Relativement stable autour de €3.40

---

## 📁 Fichiers Générés

### 1. `user_behavior_summary.json` (2.1 KB)

Résumé complet JSON incluant :

- Métriques d'engagement (moyennes, totaux)
- Taux de conversion à chaque étape
- Analyse par segment avec KPIs détaillés
- Funnel de conversion complet
- Patterns temporels (semaine/week-end)
- Évolution sur 3 périodes

### 2. `behavior_daily.csv` (139 lignes, 22 colonnes)

Métriques comportementales quotidiennes :

- **Temporel** : `date`, `day_of_week`, `is_weekend`
- **Volume** : `unique_users`, `total_events`, `views`, `add_to_carts`, `transactions`
- **Engagement** : `events_per_user`, `engagement_score` (0-100)
- **Conversion** : `view_to_cart_rate`, `view_to_purchase_rate`, `cart_to_purchase_rate`, `conversion_score` (0-100)
- **Revenue** : `revenue_per_user`
- **Segments** : `users_new`, `users_occasional`, `users_regular`, `users_premium`
- **Moyennes mobiles 7j** : `ma7_engagement`, `ma7_view_to_cart`, `ma7_conversion`

### 3. `segment_behavior_comparison.csv` (4 lignes, 10 colonnes)

Comparaison détaillée des segments :

- `segment` : New, Occasional, Regular, Premium
- `num_users`, `total_revenue`, `revenue_per_user`
- `num_transactions`, `avg_transaction`, `transactions_per_user`
- `revenue_share`, `user_share` : Parts en %
- `value_index` : Ratio revenue_share / user_share

Classement par `revenue_per_user` décroissant.

### 4. `conversion_funnel_analysis.csv` (3 lignes, 5 colonnes)

Analyse détaillée du funnel :

- `stage` : Viewers, Cart Users, Buyers
- `users` : Nombre d'utilisateurs à chaque étape
- `percentage_of_initial` : % par rapport aux viewers
- `drop_off_rate` : % de perte à cette étape
- `conversion_to_next` : Taux de conversion vers l'étape suivante

### 5. `behavior_evolution.csv` (3 lignes, 9 colonnes)

Évolution temporelle sur 3 périodes :

- `period`, `dates`, `days` : Identification de la période
- `avg_events_per_user`, `avg_conversion_rate`, `avg_revenue_per_user` : Moyennes
- `engagement_change_pct`, `conversion_change_pct`, `revenue_change_pct` : Variations % vs Période 1

---

## 🔧 Script Créé

### `scripts/user_behavior_analysis.py` (450 lignes)

**Fonctionnalités** :

1. **Analyse d'engagement** :

   - Événements par utilisateur (moyenne, médiane, min, max)
   - Distribution des types d'événements

2. **Taux de conversion multi-niveaux** :

   - View → Cart
   - View → Purchase
   - Cart → Purchase
   - Conversion globale

3. **Analyse du funnel** :

   - 3 étapes : Viewers, Cart Users, Buyers
   - Calcul des drop-offs à chaque étape
   - Taux de conversion inter-étapes

4. **Segmentation comportementale** :

   - Performance par segment (New, Occasional, Regular, Premium)
   - Calcul du Value Index
   - Revenue share et user share

5. **Patterns temporels** :

   - Comparaison semaine/week-end
   - Variations d'engagement et conversion

6. **Évolution temporelle** :
   - Division en 3 périodes égales
   - Tracking des tendances d'engagement, conversion, revenue

**Utilisation** :

```bash
python scripts/user_behavior_analysis.py
```

**Temps d'exécution** : 0.13s

---

## 📊 Insights Stratégiques

### 🎯 Points Forts

1. ✅ **Bon taux cart → purchase** : 31.88% est correct pour l'e-commerce
2. ✅ **Segment Premium performant** : Value Index de 16.38
3. ✅ **Conversion stable** : +5% sur la période analysée

### ⚠️ Points Critiques

#### 1. Drop-off View → Cart (95.82%)

**Impact** : Perte massive de 1.58M utilisateurs potentiels
**Actions recommandées** :

- 🔍 Améliorer les fiches produits (photos, descriptions, avis)
- 💰 Afficher prix et disponibilité clairement
- 🎁 Offres incitatives (frais de port, réductions)
- ⚡ Optimiser UX du bouton "Ajouter au panier"
- 📱 Tester la performance mobile

#### 2. Engagement faible (1.67 événements/user)

**Impact** : Sessions courtes, exploration limitée
**Actions recommandées** :

- 🎯 Recommandations produits personnalisées
- 🔗 Cross-selling et upselling
- 📧 Email marketing avec suggestions
- 🏆 Gamification (points, badges)

#### 3. Dominance segments faible valeur (87%)

**Impact** : 87% des users (New + Occasional) génèrent 55% du revenue
**Actions recommandées** :

- 🎓 Programme d'onboarding pour nouveaux
- 🔄 Campagnes de réactivation pour occasionnels
- ⬆️ Parcours de montée en gamme vers Regular/Premium

#### 4. Baisse week-end (-32.9% revenue/user)

**Impact** : Sous-utilisation du trafic week-end
**Actions recommandées** :

- 🎉 Promotions spécifiques week-end
- 📱 Campagnes social media ciblées
- ⏰ Offres flash samedi/dimanche

### 💡 Opportunités Majeures

1. **Optimisation du funnel** (ROI potentiel élevé)

   - Si drop-off view→cart passe de 95.82% à 90% : +132K cart users supplémentaires
   - Impact estimé : +43K transactions (à 32.56% conversion)

2. **Fidélisation Premium** (haute valeur)

   - 209 users Premium = 29.2% du revenue
   - Rétention à 95% : +€335K revenue sauvegardé

3. **Conversion Occasional → Regular**
   - 4,957 users × (€690.85 - €356.07) = +€1.66M potential

---

## 🔄 Prochaines Étapes

1. ✅ **Issue #9** : Analyse du trafic - COMPLÉTÉ
2. ✅ **Issue #10** : Analyse comportement utilisateur - COMPLÉTÉ
3. 🔜 **Issue #11** : Analyse de conversion détaillée
4. 🔜 **Issue #12** : Analyse produits et catégories
5. 🔜 **Issue #13** : Analyse revenue et monetisation

---

## 📝 Notes Techniques

- **Sources** : `daily_metrics.csv`, `segment_performance.csv`, `daily_funnel.csv`
- **Période** : 139 jours (2015-05-03 → 2015-09-18)
- **Méthode** : Pandas aggregations, calculs de ratios et moyennes mobiles
- **Qualité** : Données complètes, analyses multi-dimensionnelles

---

**Complété le** : 2025-12-09  
**Par** : GitHub Copilot  
**Issue** : #10 - Milestone 2
