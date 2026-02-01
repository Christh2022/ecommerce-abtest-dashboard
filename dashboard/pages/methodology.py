"""
E-Commerce A/B Test Dashboard - Methodology Page
Guide méthodologique pour l'analyse A/B testing
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register page
dash.register_page(__name__, path='/methodology', name='Méthodologie')

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-book me-3"),
                    "Guide Méthodologique A/B Testing"
                ], className="mb-2"),
                html.P(
                    "Comprendre les concepts, métriques et bonnes pratiques de l'A/B testing",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # Table of Contents
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-list me-2"),
                        "Table des Matières"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.Ul([
                        html.Li(html.A("1. Introduction à l'A/B Testing", href="#intro")),
                        html.Li(html.A("2. Métriques Clés", href="#metrics")),
                        html.Li(html.A("3. Puissance Statistique", href="#power")),
                        html.Li(html.A("4. Taille d'Échantillon", href="#sample-size")),
                        html.Li(html.A("5. Tests Statistiques", href="#tests")),
                        html.Li(html.A("6. Interprétation des Résultats", href="#interpretation")),
                        html.Li(html.A("7. Pièges Communs", href="#pitfalls")),
                        html.Li(html.A("8. Bonnes Pratiques", href="#best-practices")),
                    ], className="list-unstyled")
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 1: Introduction
    dbc.Row([
        dbc.Col([
            html.Div(id="intro"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-play-circle me-2"),
                        "1. Introduction à l'A/B Testing"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P([
                        "L'A/B testing est une méthode d'expérimentation qui permet de comparer deux versions ",
                        "(A et B) d'un élément pour déterminer laquelle performe le mieux. C'est une approche ",
                        "scientifique pour optimiser les conversions et l'expérience utilisateur."
                    ], className="lead"),
                    
                    html.H5("Principes Fondamentaux", className="mt-4 mb-3"),
                    html.Ul([
                        html.Li([html.Strong("Randomisation: "), "Les utilisateurs sont assignés aléatoirement à un groupe (Control ou Variant)"]),
                        html.Li([html.Strong("Contrôle: "), "Le groupe A (Control) représente l'expérience actuelle"]),
                        html.Li([html.Strong("Traitement: "), "Le groupe B (Variant) reçoit la nouvelle expérience à tester"]),
                        html.Li([html.Strong("Mesure: "), "Une métrique clé est définie pour évaluer le succès"]),
                    ]),
                    
                    html.H5("Types de Tests A/B", className="mt-4 mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Design/UI", className="text-primary"),
                                    html.P("Modifications visuelles, couleurs, mise en page", className="small mb-0")
                                ])
                            ], className="h-100")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Contenu", className="text-success"),
                                    html.P("Textes, titres, descriptions, call-to-action", className="small mb-0")
                                ])
                            ], className="h-100")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("️ Fonctionnalités", className="text-warning"),
                                    html.P("Nouvelles features, processus checkout, filtres", className="small mb-0")
                                ])
                            ], className="h-100")
                        ], md=4),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 2: Métriques Clés
    dbc.Row([
        dbc.Col([
            html.Div(id="metrics"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-line me-2"),
                        "2. Métriques Clés"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Métriques de Conversion", className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("View → Cart", className="text-info mb-2"),
                                    html.P("Taux de conversion des visiteurs qui ajoutent un produit au panier", className="small"),
                                    dbc.Badge("Formule: (Ajouts Panier / Vues) × 100", color="light", text_color="dark")
                                ])
                            ], className="border-info mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Cart → Purchase", className="text-success mb-2"),
                                    html.P("Taux de conversion des utilisateurs qui finalisent leur achat", className="small"),
                                    dbc.Badge("Formule: (Achats / Paniers) × 100", color="light", text_color="dark")
                                ])
                            ], className="border-success mb-3")
                        ], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("View → Purchase", className="text-primary mb-2"),
                                    html.P("Taux de conversion global du funnel complet", className="small"),
                                    dbc.Badge("Formule: (Achats / Vues) × 100", color="light", text_color="dark")
                                ])
                            ], className="border-primary mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Revenue per User", className="text-warning mb-2"),
                                    html.P("Revenu moyen généré par utilisateur", className="small"),
                                    dbc.Badge("Formule: Revenue Total / Utilisateurs", color="light", text_color="dark")
                                ])
                            ], className="border-warning mb-3")
                        ], md=6),
                    ]),
                    
                    html.H5("Lift (Amélioration)", className="mt-4 mb-3"),
                    html.P([
                        "Le ", html.Strong("lift"), " mesure l'amélioration relative entre le variant et le control:"
                    ]),
                    dbc.Alert([
                        html.Pre("Lift (%) = ((Variant Rate - Control Rate) / Control Rate) × 100", 
                                className="mb-0 text-center", style={'fontSize': '1.1em'})
                    ], color="info"),
                    html.P([
                        html.Strong("Exemple: "), "Si le taux de conversion control est 2.5% et variant 3.3%, ",
                        "le lift est: ((3.3 - 2.5) / 2.5) × 100 = ", html.Strong("+32%")
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 3: Puissance Statistique
    dbc.Row([
        dbc.Col([
            html.Div(id="power"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-bolt me-2"),
                        "3. Puissance Statistique"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P([
                        "La puissance statistique (1 - β) représente la probabilité de détecter un effet réel ",
                        "quand il existe. Une puissance de 80% signifie 80% de chances de détecter une différence ",
                        "significative si elle existe vraiment."
                    ], className="lead"),
                    
                    html.H5("Niveaux de Puissance Recommandés", className="mt-4 mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("80%", className="text-warning mb-0"),
                                    html.P("Standard", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-warning")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("90%", className="text-success mb-0"),
                                    html.P("Élevé", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-success")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("95%", className="text-primary mb-0"),
                                    html.P("Très Élevé", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-primary")
                        ], md=4),
                    ]),
                    
                    html.H5("Facteurs Influençant la Puissance", className="mt-4 mb-3"),
                    html.Ul([
                        html.Li([html.Strong("Taille d'échantillon: "), "Plus l'échantillon est grand, plus la puissance augmente"]),
                        html.Li([html.Strong("Taille de l'effet: "), "Les grands effets sont plus faciles à détecter"]),
                        html.Li([html.Strong("Niveau de signification (α): "), "Généralement fixé à 5%"]),
                        html.Li([html.Strong("Variabilité: "), "Moins de variabilité = plus de puissance"]),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 4: Taille d'Échantillon
    dbc.Row([
        dbc.Col([
            html.Div(id="sample-size"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-users me-2"),
                        "4. Taille d'Échantillon"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P([
                        "La taille d'échantillon nécessaire dépend de plusieurs paramètres. ",
                        "Un échantillon trop petit manquera de puissance, tandis qu'un échantillon ",
                        "trop grand gaspillera des ressources."
                    ], className="lead"),
                    
                    html.H5("Formule Simplifiée (Test Proportions)", className="mt-4 mb-3"),
                    dbc.Alert([
                        html.P("Pour chaque groupe (Control et Variant):", className="mb-2"),
                        html.Pre("n = (Z_α/2 + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₁ - p₂)²", 
                                className="text-center", style={'fontSize': '1.1em'}),
                        html.Ul([
                            html.Li("Z_α/2 : Score Z pour le niveau de confiance (1.96 pour 95%)"),
                            html.Li("Z_β : Score Z pour la puissance (0.84 pour 80%)"),
                            html.Li("p₁ : Taux de conversion control"),
                            html.Li("p₂ : Taux de conversion variant"),
                        ], className="small mt-3")
                    ], color="light"),
                    
                    html.H5("Règles Pratiques", className="mt-4 mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Minimum Viable", className="text-info mb-2"),
                                    html.P("≥ 100 conversions par groupe", className="mb-1"),
                                    html.Small("Pour détecter des effets moyens", className="text-muted")
                                ])
                            ], className="mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Recommandé", className="text-success mb-2"),
                                    html.P("≥ 350-400 conversions par groupe", className="mb-1"),
                                    html.Small("Pour détecter de petits effets", className="text-muted")
                                ])
                            ], className="mb-3")
                        ], md=6),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 5: Tests Statistiques
    dbc.Row([
        dbc.Col([
            html.Div(id="tests"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-calculator me-2"),
                        "5. Tests Statistiques"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Chi-Square Test (χ²)", className="mb-3"),
                    html.P([
                        "Test d'indépendance utilisé pour comparer des proportions entre deux groupes. ",
                        "Idéal pour les taux de conversion."
                    ]),
                    dbc.Alert([
                        html.Strong("Hypothèse nulle (H₀): "), 
                        "Les taux de conversion des deux groupes sont identiques",
                        html.Br(),
                        html.Strong("Hypothèse alternative (H₁): "), 
                        "Les taux de conversion sont différents"
                    ], color="info"),
                    
                    html.H5("Z-Test", className="mt-4 mb-3"),
                    html.P([
                        "Test de comparaison de deux proportions. Équivalent au Chi-Square test pour ",
                        "comparer deux groupes, mais donne un résultat directionnel."
                    ]),
                    
                    html.H5("P-Value (Valeur p)", className="mt-4 mb-3"),
                    html.P([
                        "La p-value mesure la probabilité d'observer des résultats au moins aussi extrêmes ",
                        "que ceux observés, en supposant que l'hypothèse nulle est vraie."
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("p < 0.05", className="text-success"),
                                    html.P("Résultat statistiquement significatif", className="small mb-0")
                                ], className="text-center")
                            ], className="border-success")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("p ≥ 0.05", className="text-danger"),
                                    html.P("Pas de différence significative", className="small mb-0")
                                ], className="text-center")
                            ], className="border-danger")
                        ], md=6),
                    ]),
                    
                    html.H5("Intervalle de Confiance", className="mt-4 mb-3"),
                    html.P([
                        "L'intervalle de confiance à 95% indique que nous sommes 95% certains que ",
                        "la vraie valeur du paramètre se trouve dans cet intervalle."
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 6: Interprétation des Résultats
    dbc.Row([
        dbc.Col([
            html.Div(id="interpretation"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-check-circle me-2"),
                        "6. Interprétation des Résultats"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Critères de Décision", className="mb-3"),
                    
                    dbc.Alert([
                        html.H6(" Test Concluant (Variant Gagnant)", className="text-success"),
                        html.Ul([
                            html.Li("p-value < 0.05 (significatif)"),
                            html.Li("Puissance statistique ≥ 80%"),
                            html.Li("Lift positif et substantiel (≥ 5%)"),
                            html.Li("Intervalle de confiance ne contient pas 0"),
                        ])
                    ], color="success"),
                    
                    dbc.Alert([
                        html.H6(" Test Non Concluant", className="text-warning"),
                        html.Ul([
                            html.Li("p-value ≥ 0.05 (non significatif)"),
                            html.Li("ou Puissance statistique < 80%"),
                            html.Li("ou Intervalle de confiance trop large"),
                        ])
                    ], color="warning"),
                    
                    dbc.Alert([
                        html.H6(" Continuer le Test", className="text-info"),
                        html.Ul([
                            html.Li("Tendance positive mais pas encore significative"),
                            html.Li("Taille d'échantillon insuffisante"),
                            html.Li("Variance élevée nécessitant plus de données"),
                        ])
                    ], color="info"),
                    
                    html.H5("Significativité vs Pertinence Pratique", className="mt-4 mb-3"),
                    html.P([
                        "Un résultat peut être ", html.Strong("statistiquement significatif"), 
                        " sans être ", html.Strong("pratiquement pertinent"), ". Par exemple:",
                    ]),
                    html.Ul([
                        html.Li("Un lift de +0.5% peut être significatif avec 100K utilisateurs"),
                        html.Li("Mais l'impact business peut être négligeable"),
                        html.Li("Considérez toujours le coût d'implémentation vs le bénéfice"),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 7: Pièges Communs
    dbc.Row([
        dbc.Col([
            html.Div(id="pitfalls"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "7. Pièges Communs à Éviter"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Peeking", className="text-danger mb-3"),
                                    html.P([
                                        "Arrêter le test prématurément en voyant des résultats prometteurs. ",
                                        "Cela augmente le taux de faux positifs."
                                    ], className="small"),
                                    dbc.Badge("Solution: Définir la durée à l'avance", color="danger")
                                ])
                            ], className="border-danger h-100 mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Multiple Testing", className="text-danger mb-3"),
                                    html.P([
                                        "Tester plusieurs variantes simultanément sans ajuster le niveau ",
                                        "de signification augmente le risque d'erreur de Type I."
                                    ], className="small"),
                                    dbc.Badge("Solution: Correction de Bonferroni", color="danger")
                                ])
                            ], className="border-danger h-100 mb-3")
                        ], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Seasonality Bias", className="text-warning mb-3"),
                                    html.P([
                                        "Lancer un test pendant une période atypique (promo, vacances) ",
                                        "peut fausser les résultats."
                                    ], className="small"),
                                    dbc.Badge("Solution: Tester sur cycles complets", color="warning")
                                ])
                            ], className="border-warning h-100 mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Selection Bias", className="text-warning mb-3"),
                                    html.P([
                                        "Mauvaise randomisation créant des groupes non comparables ",
                                        "(ex: desktop vs mobile)."
                                    ], className="small"),
                                    dbc.Badge("Solution: Randomisation stratifiée", color="warning")
                                ])
                            ], className="border-warning h-100 mb-3")
                        ], md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Novelty Effect", className="text-info mb-3"),
                                    html.P([
                                        "Les utilisateurs réagissent positivement au changement par curiosité, ",
                                        "mais l'effet s'estompe avec le temps."
                                    ], className="small"),
                                    dbc.Badge("Solution: Tests de longue durée", color="info")
                                ])
                            ], className="border-info h-100 mb-3")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Sample Ratio Mismatch", className="text-info mb-3"),
                                    html.P([
                                        "Les groupes ont des tailles très différentes de ce qui était prévu, ",
                                        "indiquant un problème d'implémentation."
                                    ], className="small"),
                                    dbc.Badge("Solution: Vérifier le ratio dès le début", color="info")
                                ])
                            ], className="border-info h-100 mb-3")
                        ], md=6),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Section 8: Bonnes Pratiques
    dbc.Row([
        dbc.Col([
            html.Div(id="best-practices"),
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-star me-2"),
                        "8. Bonnes Pratiques"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Avant le Test", className="mb-3"),
                    dbc.Checklist([
                        {'label': 'Définir une hypothèse claire et mesurable', 'value': 1},
                        {'label': 'Choisir une métrique primaire (et des métriques secondaires)', 'value': 2},
                        {'label': 'Calculer la taille d\'échantillon nécessaire', 'value': 3},
                        {'label': 'Déterminer la durée du test (minimum 1-2 semaines)', 'value': 4},
                        {'label': 'Documenter le plan d\'expérimentation', 'value': 5},
                        {'label': 'Vérifier l\'implémentation technique (QA)', 'value': 6},
                    ], className="mb-4", value=[1,2,3,4,5,6], inline=False),
                    
                    html.H5("Pendant le Test", className="mb-3 mt-4"),
                    dbc.Checklist([
                        {'label': 'Monitorer le Sample Ratio Mismatch (SRM)', 'value': 1},
                        {'label': 'Ne pas modifier les critères en cours de route', 'value': 2},
                        {'label': 'Éviter de regarder les résultats trop souvent (peeking)', 'value': 3},
                        {'label': 'Surveiller les métriques de santé (erreurs, temps de chargement)', 'value': 4},
                        {'label': 'Documenter tout événement inhabituel', 'value': 5},
                    ], className="mb-4", value=[1,2,3,4,5], inline=False),
                    
                    html.H5("Après le Test", className="mb-3 mt-4"),
                    dbc.Checklist([
                        {'label': 'Analyser les résultats avec les tests statistiques appropriés', 'value': 1},
                        {'label': 'Examiner les segments (desktop/mobile, nouveaux/anciens)', 'value': 2},
                        {'label': 'Vérifier les métriques secondaires et guardrail metrics', 'value': 3},
                        {'label': 'Calculer le ROI et l\'impact business', 'value': 4},
                        {'label': 'Documenter les learnings (succès ou échec)', 'value': 5},
                        {'label': 'Partager les résultats avec l\'équipe', 'value': 6},
                    ], className="mb-4", value=[1,2,3,4,5,6], inline=False),
                    
                    html.H5("Règles d'Or", className="mb-3 mt-4"),
                    dbc.Alert([
                        html.Ul([
                            html.Li([html.Strong("Un test, une hypothèse: "), "Ne testez qu'un seul changement à la fois"]),
                            html.Li([html.Strong("Patience: "), "Attendez d'avoir la taille d'échantillon nécessaire"]),
                            html.Li([html.Strong("Itération: "), "Apprenez de chaque test pour améliorer le suivant"]),
                            html.Li([html.Strong("Documentation: "), "Gardez un historique de tous vos tests"]),
                            html.Li([html.Strong("Business First: "), "La significativité statistique n'est pas tout"]),
                        ], className="mb-0")
                    ], color="primary")
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Resources Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-graduation-cap me-2"),
                        "Ressources Complémentaires"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H6("Lectures Recommandées", className="mb-3"),
                    html.Ul([
                        html.Li("\"Trustworthy Online Controlled Experiments\" - Kohavi, Tang & Xu"),
                        html.Li("\"Testing Business Ideas\" - David Bland & Alexander Osterwalder"),
                        html.Li("Evan Miller's A/B Testing Tools and Articles"),
                        html.Li("Google's Experiment Design Guide"),
                    ]),
                    
                    html.H6("Outils en Ligne", className="mb-3 mt-4"),
                    html.Ul([
                        html.Li("Sample Size Calculator: Evan Miller, Optimizely"),
                        html.Li("Statistical Significance Calculator"),
                        html.Li("Cette dashboard pour simuler et analyser vos tests! "),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
], fluid=True, className="py-4")
