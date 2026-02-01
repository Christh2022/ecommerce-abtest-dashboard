"""
E-Commerce A/B Test Dashboard - About Page
Informations sur le projet et les données
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register page
dash.register_page(__name__, path='/about', name='À Propos')

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-info-circle me-3"),
                    "À Propos du Dashboard"
                ], className="mb-2"),
                html.P(
                    "Tout ce qu'il faut savoir sur ce projet d'analyse A/B testing",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # Project Overview
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-project-diagram me-2"),
                        "Le Projet"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P([
                        "Ce dashboard interactif a été développé pour faciliter l'analyse des tests A/B ",
                        "dans un contexte e-commerce. Il permet de visualiser les performances, simuler ",
                        "de nouveaux tests, et comprendre l'impact des optimisations sur les conversions ",
                        "et le revenu."
                    ], className="lead"),
                    
                    html.H5("Objectifs", className="mt-4 mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-chart-line fa-3x text-primary mb-3"),
                                        html.H6("Visualisation", className="text-primary"),
                                        html.P("Explorer les métriques clés et les tendances", className="small mb-0")
                                    ], className="text-center")
                                ])
                            ], className="h-100 border-primary")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-flask fa-3x text-success mb-3"),
                                        html.H6("Simulation", className="text-success"),
                                        html.P("Prédire l'impact de nouveaux tests A/B", className="small mb-0")
                                    ], className="text-center")
                                ])
                            ], className="h-100 border-success")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-lightbulb fa-3x text-warning mb-3"),
                                        html.H6("Décisions", className="text-warning"),
                                        html.P("Prendre des décisions basées sur les données", className="small mb-0")
                                    ], className="text-center")
                                ])
                            ], className="h-100 border-warning")
                        ], md=4),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Data Overview
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-database me-2"),
                        "Les Données"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Dataset E-Commerce", className="mb-3"),
                    html.P([
                        "Ce dashboard utilise un dataset d'événements e-commerce couvrant la période ",
                        html.Strong("Mai - Septembre 2015"), ". Les données incluent le comportement ",
                        "de plus de ", html.Strong("1,6 million d'utilisateurs"), " sur une plateforme ",
                        "de vente en ligne."
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("1.65M+", className="text-primary mb-0"),
                                    html.P("Utilisateurs", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-primary")
                        ], md=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("139", className="text-success mb-0"),
                                    html.P("Jours d'Analyse", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-success")
                        ], md=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("3.9M+", className="text-info mb-0"),
                                    html.P("Événements", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-info")
                        ], md=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3("15K+", className="text-warning mb-0"),
                                    html.P("Transactions", className="small text-muted mb-0")
                                ], className="text-center")
                            ], className="border-warning")
                        ], md=3),
                    ], className="mt-4"),
                    
                    html.H5("Types d'Événements", className="mt-4 mb-3"),
                    html.Ul([
                        html.Li([html.Strong("View: "), "Consultation d'une page produit"]),
                        html.Li([html.Strong("Add to Cart: "), "Ajout d'un produit au panier"]),
                        html.Li([html.Strong("Transaction: "), "Achat confirmé avec montant"]),
                    ]),
                    
                    html.H5("Métriques Calculées", className="mt-4 mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge("Taux de Conversion", color="primary", className="me-2 mb-2"),
                            dbc.Badge("Revenue par Utilisateur", color="success", className="me-2 mb-2"),
                            dbc.Badge("Funnel Analysis", color="info", className="me-2 mb-2"),
                        ], md=6),
                        dbc.Col([
                            dbc.Badge("Segments Utilisateurs", color="warning", className="me-2 mb-2"),
                            dbc.Badge("Cohortes", color="danger", className="me-2 mb-2"),
                            dbc.Badge("Pareto Products", color="secondary", className="me-2 mb-2"),
                        ], md=6),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Features
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-star me-2"),
                        "Fonctionnalités"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6([html.I(className="fas fa-home me-2 text-primary"), "Accueil"], className="mb-2"),
                            html.P("Vue d'ensemble des KPIs, trafic, revenue et conversions avec filtres interactifs", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-users me-2 text-success"), "Trafic"], className="mb-2"),
                            html.P("Analyse détaillée du trafic: utilisateurs, sessions, sources et tendances temporelles", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-mouse-pointer me-2 text-info"), "Comportement"], className="mb-2"),
                            html.P("Patterns de navigation, engagement utilisateur, et analyse des événements", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-shopping-cart me-2 text-warning"), "Conversions"], className="mb-2"),
                            html.P("Taux de conversion par étape, analyse temporelle et segmentation", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-box me-2 text-danger"), "Produits"], className="mb-2"),
                            html.P("Performance par produit, analyse Pareto, et optimisation du catalogue", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-filter me-2 text-primary"), "Funnel"], className="mb-2"),
                            html.P("Visualisation du tunnel de conversion et identification des points de friction", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-flask me-2 text-success"), "Simulations A/B"], className="mb-2"),
                            html.P("16 scénarios de test A/B simulés avec métriques et évolution sur 30 jours", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-chart-bar me-2 text-info"), "Résultats A/B"], className="mb-2"),
                            html.P("Synthèse des résultats de tests avec significativité statistique", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-calculator me-2 text-warning"), "Calculateur Z-Test"], className="mb-2"),
                            html.P("Outil interactif pour planifier et simuler vos propres tests A/B", className="small text-muted")
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-chart-line me-2 text-danger"), "Visualisations"], className="mb-2"),
                            html.P("Graphiques avancés pour analyser les tests A/B en profondeur", className="small text-muted")
                        ], md=6, className="mb-3"),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Technology Stack
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-code me-2"),
                        "Technologies Utilisées"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5([html.I(className="fab fa-python me-2 text-primary"), "Python"], className="mb-3"),
                            html.Ul([
                                html.Li([html.Strong("Dash 2.14.2: "), "Framework web pour analytics"]),
                                html.Li([html.Strong("Plotly 5.18.0: "), "Visualisations interactives"]),
                                html.Li([html.Strong("Pandas: "), "Manipulation et analyse de données"]),
                                html.Li([html.Strong("NumPy: "), "Calculs numériques"]),
                                html.Li([html.Strong("SciPy: "), "Tests statistiques"]),
                            ])
                        ], md=6),
                        dbc.Col([
                            html.H5([html.I(className="fab fa-css3-alt me-2 text-info"), "Frontend"], className="mb-3"),
                            html.Ul([
                                html.Li([html.Strong("Bootstrap 5: "), "Design responsive"]),
                                html.Li([html.Strong("Font Awesome: "), "Icons"]),
                                html.Li([html.Strong("Dash Bootstrap Components: "), "UI components"]),
                                html.Li([html.Strong("Plotly Dark Theme: "), "Thème moderne"]),
                            ])
                        ], md=6),
                    ]),
                    
                    html.H5("Architecture", className="mt-4 mb-3"),
                    html.P([
                        "Dashboard multi-pages avec routing automatique, callbacks interactifs pour les filtres ",
                        "et graphiques, et rechargement à chaud en développement."
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Methodology
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-book me-2"),
                        "Méthodologie A/B Testing"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P([
                        "Les tests A/B présentés dans ce dashboard suivent des principes statistiques rigoureux:"
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Puissance Statistique", className="text-primary mb-2"),
                                    html.P("Minimum 78% pour tous les scénarios", className="small mb-0")
                                ])
                            ], className="border-primary mb-3")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Niveau de Confiance", className="text-success mb-2"),
                                    html.P("95% (α = 0.05) pour tous les tests", className="small mb-0")
                                ])
                            ], className="border-success mb-3")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(" Simulations", className="text-info mb-2"),
                                    html.P("10,000 itérations Monte Carlo par scénario", className="small mb-0")
                                ])
                            ], className="border-info mb-3")
                        ], md=4),
                    ]),
                    
                    html.P([
                        "Consultez la page ", 
                        dcc.Link("Méthodologie", href="/methodology", className="fw-bold"),
                        " pour plus de détails sur les concepts statistiques, les formules utilisées, ",
                        "et les bonnes pratiques."
                    ], className="mt-3 mb-0")
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Use Cases
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-lightbulb me-2"),
                        "Cas d'Usage"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H5("Ce dashboard est idéal pour:", className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.I(className="fas fa-user-tie fa-2x text-primary mb-2"),
                                html.H6("Product Managers", className="text-primary"),
                                html.Ul([
                                    html.Li("Prioriser les tests à lancer"),
                                    html.Li("Estimer l'impact business"),
                                    html.Li("Suivre les performances"),
                                ], className="small")
                            ])
                        ], md=4),
                        dbc.Col([
                            html.Div([
                                html.I(className="fas fa-chart-line fa-2x text-success mb-2"),
                                html.H6("Data Analysts", className="text-success"),
                                html.Ul([
                                    html.Li("Analyser les tendances"),
                                    html.Li("Calculer la significativité"),
                                    html.Li("Segmenter les utilisateurs"),
                                ], className="small")
                            ])
                        ], md=4),
                        dbc.Col([
                            html.Div([
                                html.I(className="fas fa-users fa-2x text-info mb-2"),
                                html.H6("Growth Teams", className="text-info"),
                                html.Ul([
                                    html.Li("Optimiser les conversions"),
                                    html.Li("Identifier les opportunités"),
                                    html.Li("Mesurer le ROI"),
                                ], className="small")
                            ])
                        ], md=4),
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Contact & Links
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-link me-2"),
                        "Liens & Ressources"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6([html.I(className="fab fa-github me-2"), "Code Source"], className="mb-2"),
                            html.P([
                                "Ce projet est disponible sur ",
                                html.A("GitHub", href="https://github.com/Christh2022/ecommerce-abtest-dashboard", 
                                      target="_blank", className="fw-bold"),
                            ], className="small text-muted")
                        ], md=6),
                        dbc.Col([
                            html.H6([html.I(className="fas fa-envelope me-2"), "Contact"], className="mb-2"),
                            html.P([
                                "Développé par ", html.Strong("Christh Mampassi"), html.Br(),
                                html.A("cmampassi273@gmail.com", href="mailto:cmampassi273@gmail.com", className="text-decoration-none")
                            ], className="small text-muted")
                        ], md=6),
                    ]),
                    
                    html.Hr(className="my-3"),
                    
                    html.Div([
                        html.P([
                            html.I(className="fas fa-calendar-alt me-2"),
                            "Dernière mise à jour: Décembre 2025"
                        ], className="small text-muted mb-2"),
                        html.P([
                            html.I(className="fas fa-code-branch me-2"),
                            "Version: 1.0.0"
                        ], className="small text-muted mb-0")
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Hr(),
                html.P([
                    "Développé avec ",
                    html.I(className="fas fa-heart text-danger"),
                    " par Christh Mampassi | ",
                    html.A("cmampassi273@gmail.com", href="mailto:cmampassi273@gmail.com", className="text-decoration-none text-muted")
                ], className="text-center text-muted mb-0")
            ])
        ])
    ]),
    
], fluid=True, className="py-4")
