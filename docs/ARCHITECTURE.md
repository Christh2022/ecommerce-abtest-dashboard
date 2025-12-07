# Architecture du Projet E-commerce Dashboard

## Vue d'ensemble

Ce document décrit l'architecture technique du projet E-commerce Dashboard & A/B Testing.

## Architecture en couches

### 1. Couche Présentation

- **Dash Application** : Interface utilisateur interactive
- **Grafana** : Monitoring et visualisation système

### 2. Couche Application

- **Backend Python** : Logique métier
- **API REST** : Communication avec le frontend (futur)

### 3. Couche Données

- **PostgreSQL** : Base de données relationnelle
- **Pandas/NumPy** : Traitement des données

### 4. Couche Infrastructure

- **Docker** : Conteneurisation
- **Loki/Promtail** : Agrégation de logs
- **Falco** : Détection d'intrusions

## Diagramme de composants

```
[Frontend Dash] ←→ [Backend Python] ←→ [PostgreSQL]
       ↓                    ↓
  [Grafana] ←─────────→ [Loki]
                          ↑
                     [Promtail]
                          ↑
                      [Falco]
```

## Flux de données

1. **Ingestion** : Données brutes → PostgreSQL
2. **Transformation** : Scripts Python → Nettoyage
3. **Analyse** : KPIs, A/B tests → Métriques
4. **Visualisation** : Dash/Grafana → Utilisateurs

## Technologies

- Python 3.11
- PostgreSQL 15
- Docker & Docker Compose
- Grafana, Loki, Promtail, Falco

Pour plus de détails, voir le README principal.
