# ISSUES.md - Liste des issues pour le projet

## Milestone 1 : Dataset & Préparation

### Issue #1: Collecter les données e-commerce brutes

**Branche**: `feature/data-preprocessing`
**Description**: Collecter et importer les données brutes (transactions, users, products, sessions)
**Tâches**:

- [ ] Définir le schéma des données
- [ ] Créer des datasets de test
- [ ] Documenter les sources de données

### Issue #2: Nettoyer les données

**Branche**: `feature/data-cleaning`
**Description**: Implémenter les scripts de nettoyage des données
**Tâches**:

- [ ] Gérer les valeurs manquantes
- [ ] Détecter et traiter les outliers
- [ ] Normaliser les formats de dates
- [ ] Valider les types de données

### Issue #3: Explorer les données

**Branche**: `feature/data-exploration`
**Description**: Analyse exploratoire des données (EDA)
**Tâches**:

- [ ] Statistiques descriptives
- [ ] Visualisations des distributions
- [ ] Corrélations entre variables
- [ ] Rapport d'exploration

---

## Milestone 2 : KPIs & Exploration

### Issue #4: Calculer les KPIs principaux

**Branche**: `feature/kpi-metrics`
**Description**: Implémenter le calcul des KPIs e-commerce
**Tâches**:

- [ ] Taux de conversion
- [ ] Panier moyen (AOV)
- [ ] Customer Lifetime Value (CLV)
- [ ] Taux de rétention
- [ ] Revenue par utilisateur

---

## Milestone 3 : A/B Testing

### Issue #5: Framework de tests A/B

**Branche**: `feature/ab-testing`
**Description**: Créer le framework pour les tests A/B
**Tâches**:

- [ ] Tests statistiques (Student, Chi-2)
- [ ] Calcul de la taille d'échantillon
- [ ] Calcul de la significativité
- [ ] Intervalles de confiance
- [ ] Documentation des méthodes

---

## Milestone 4 : Dashboard Multi-Pages

### Issue #6: Page d'accueil du dashboard

**Branche**: `feature/dashboard-home`
**Description**: Créer la page d'accueil avec KPIs principaux
**Tâches**:

- [x] Layout de base
- [ ] Cartes KPIs dynamiques
- [ ] Graphiques de tendances
- [ ] Filtres de dates

### Issue #7: Page comportement utilisateur

**Branche**: `feature/dashboard-behavior`
**Description**: Page d'analyse du comportement utilisateur
**Tâches**:

- [ ] Analyse des sessions
- [ ] Funnels de conversion
- [ ] Heatmaps d'activité
- [ ] Segments utilisateurs

### Issue #8: Page analyse produits

**Branche**: `feature/dashboard-products`
**Description**: Page d'analyse des produits
**Tâches**:

- [ ] Top produits
- [ ] Analyse par catégorie
- [ ] Cross-selling
- [ ] Tendances de ventes

### Issue #9: Page tests A/B

**Branche**: `feature/dashboard-abtest`
**Description**: Page de visualisation des tests A/B
**Tâches**:

- [ ] Liste des tests actifs
- [ ] Résultats des tests
- [ ] Comparaisons visuelles
- [ ] Recommandations

### Issue #10: Page analyse de cohortes

**Branche**: `feature/dashboard-cohorts`
**Description**: Page d'analyse de cohortes
**Tâches**:

- [ ] Matrice de rétention
- [ ] Analyse de cohortes temporelles
- [ ] Graphiques de survie
- [ ] Métriques par cohorte

---

## Milestone 5 : Dockerisation

### Issue #11: Configuration Docker complète

**Branche**: `feature/docker-setup`
**Description**: Finaliser la configuration Docker
**Tâches**:

- [x] Docker Compose
- [ ] Optimisation des images
- [ ] Healthchecks
- [ ] Volume persistence
- [ ] Network configuration

---

## Milestone 6 : Documentation & Livraison

### Issue #12: Documentation complète

**Branche**: `feature/docs-writing`
**Description**: Rédiger la documentation technique et utilisateur
**Tâches**:

- [x] README principal
- [ ] Guide d'installation détaillé
- [ ] Documentation API
- [ ] Guide utilisateur
- [ ] Rapport PDF final

---

## Milestone 7 : Sécurité & Intrusion

### Issue #13: Monitoring de sécurité

**Branche**: `feature/security-intrusion`
**Description**: Mettre en place le système de détection d'intrusions
**Tâches**:

- [x] Configuration Falco
- [x] Configuration Loki/Promtail
- [x] Dashboard Grafana sécurité
- [ ] Règles d'alerting personnalisées
- [ ] Tests de sécurité

---

## Issues transversales

### Issue #14: Refactoring du code

**Branche**: `feature/refactor`
**Description**: Améliorer la qualité et la structure du code
**Tâches**:

- [ ] Respect PEP 8
- [ ] Optimisation des performances
- [ ] Réduction de la dette technique
- [ ] Documentation inline

### Issue #15: Tests unitaires

**Branche**: `feature/tests`
**Description**: Créer une suite de tests complète
**Tâches**:

- [ ] Tests des KPIs
- [ ] Tests des A/B tests
- [ ] Tests du preprocessing
- [ ] Tests du dashboard
- [ ] Coverage > 80%

---

## Comment contribuer

1. Choisir une issue
2. Créer/checkout la branche correspondante
3. Implémenter les changements
4. Tester localement
5. Commit et push
6. Créer une Pull Request vers `develop`
