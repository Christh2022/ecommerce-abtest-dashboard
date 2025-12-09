"""
Home Page - Dashboard Overview
Issue #19 - Multi-page Structure
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime

# Register this page with dash.page_registry
dash.register_page(__name__, path='/', name='Accueil')

# Layout for the home page
layout = dbc.Container([
    # Welcome Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-home me-3"),
                    "Bienvenue sur le Dashboard A/B Testing"
                ], className="mb-3"),
                html.P(
                    "Explorez les analyses complètes des tests A/B et les opportunités d'optimisation "
                    "pour votre plateforme e-commerce.",
                    className="lead text-muted"
                ),
                html.Hr(),
                html.P([
                    html.Strong("Période d'analyse: "),
                    "Mai - Septembre 2015 (139 jours)"
                ], className="mb-2"),
                html.P([
                    html.Strong("Dataset: "),
                    "RetailRocket E-commerce Dataset"
                ], className="mb-2"),
            ], className="mb-4")
        ])
    ]),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-3x text-primary mb-3"),
                        html.H3("1,649,534", className="mb-1"),
                        html.P("Utilisateurs Uniques", className="text-muted mb-0"),
                        html.Small("11,869 par jour", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-shopping-cart fa-3x text-success mb-3"),
                        html.H3("22,457", className="mb-1"),
                        html.P("Transactions", className="text-muted mb-0"),
                        html.Small("Taux conversion: 0.84%", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-euro-sign fa-3x text-info mb-3"),
                        html.H3("€5.73M", className="mb-1"),
                        html.P("Revenue Total", className="text-muted mb-0"),
                        html.Small("AOV: €255.36", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-flask fa-3x text-danger mb-3"),
                        html.H3("8", className="mb-1"),
                        html.P("Scénarios A/B", className="text-muted mb-0"),
                        html.Small("5 Winners validés", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Business Impact Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-rocket me-2"),
                        "Impact Business Potentiel"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2("€38.4M", className="text-success mb-1"),
                                html.P("Revenue Annuel Potentiel", className="text-muted mb-2"),
                                html.P([
                                    html.I(className="fas fa-arrow-up me-2"),
                                    "+670% vs baseline"
                                ], className="text-success mb-0"),
                            ])
                        ], width=4),
                        
                        dbc.Col([
                            html.Div([
                                html.H2("+25,845%", className="text-primary mb-1"),
                                html.P("ROI Portfolio", className="text-muted mb-2"),
                                html.P([
                                    html.I(className="fas fa-coins me-2"),
                                    "€259 retour par €1 investi"
                                ], className="text-primary mb-0"),
                            ])
                        ], width=4),
                        
                        dbc.Col([
                            html.Div([
                                html.H2("€148K", className="text-info mb-1"),
                                html.P("Investissement Total", className="text-muted mb-2"),
                                html.P([
                                    html.I(className="fas fa-calendar-alt me-2"),
                                    "Programme 6 mois"
                                ], className="text-info mb-0"),
                            ])
                        ], width=4),
                    ]),
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Top 3 Scenarios
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-trophy me-2"),
                        "Top 3 Scénarios d'Optimisation"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            dbc.Row([
                                dbc.Col([
                                    html.Span("🥇 S8", className="badge bg-warning text-dark me-2"),
                                    html.Strong("Nettoyage Catalogue"),
                                ], width=6),
                                dbc.Col([
                                    html.Span("ROI: +105,309%", className="badge bg-success"),
                                ], width=3, className="text-end"),
                                dbc.Col([
                                    html.Span("€5.27M/an", className="text-success"),
                                ], width=3, className="text-end"),
                            ])
                        ], className="border-0 border-bottom"),
                        
                        dbc.ListGroupItem([
                            dbc.Row([
                                dbc.Col([
                                    html.Span("🥈 S2", className="badge bg-secondary me-2"),
                                    html.Strong("Système Reviews"),
                                ], width=6),
                                dbc.Col([
                                    html.Span("ROI: +40,056%", className="badge bg-success"),
                                ], width=3, className="text-end"),
                                dbc.Col([
                                    html.Span("€6.02M/an", className="text-success"),
                                ], width=3, className="text-end"),
                            ])
                        ], className="border-0 border-bottom"),
                        
                        dbc.ListGroupItem([
                            dbc.Row([
                                dbc.Col([
                                    html.Span("🥉 S4", className="badge bg-warning text-dark me-2"),
                                    html.Strong("Prix Compétitifs"),
                                ], width=6),
                                dbc.Col([
                                    html.Span("ROI: +37,546%", className="badge bg-success"),
                                ], width=3, className="text-end"),
                                dbc.Col([
                                    html.Span("€7.53M/an", className="text-success"),
                                ], width=3, className="text-end"),
                            ])
                        ], className="border-0"),
                    ], flush=True),
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        # Quick Navigation
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-compass me-2"),
                        "Navigation Rapide"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-chart-line me-2"),
                                "Analyses KPI"
                            ], color="primary", outline=True, href="/traffic", 
                            className="w-100 mb-3"),
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-flask me-2"),
                                "Tests A/B"
                            ], color="success", outline=True, href="/ab-testing/simulations", 
                            className="w-100 mb-3"),
                        ], width=6),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-chart-area me-2"),
                                "Visualisations"
                            ], color="info", outline=True, href="/ab-testing/visualizations", 
                            className="w-100 mb-3"),
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-calculator me-2"),
                                "Calculateur"
                            ], color="warning", outline=True, href="/ab-testing/calculator", 
                            className="w-100 mb-3"),
                        ], width=6),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-book me-2"),
                                "Méthodologie"
                            ], color="secondary", outline=True, href="/methodology", 
                            className="w-100"),
                        ], width=12),
                    ]),
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Key Findings Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-lightbulb me-2"),
                        "Insights Clés"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Alert([
                                html.H6([
                                    html.I(className="fas fa-exclamation-triangle me-2"),
                                    "Problème Majeur"
                                ], className="alert-heading"),
                                html.P("97.41% des utilisateurs abandonnent avant l'ajout au panier", className="mb-2"),
                                html.Hr(),
                                html.P("Baseline view→cart: 2.59% (très faible)", className="mb-0 small"),
                            ], color="danger", className="mb-3"),
                            
                            dbc.Alert([
                                html.H6([
                                    html.I(className="fas fa-box me-2"),
                                    "Dead Stock"
                                ], className="alert-heading"),
                                html.P("94.9% des produits (211K) n'ont généré aucune vente", className="mb-2"),
                                html.Hr(),
                                html.P("Opportunité: Nettoyage catalogue → ROI +105K%", className="mb-0 small"),
                            ], color="warning", className="mb-3"),
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Alert([
                                html.H6([
                                    html.I(className="fas fa-calendar-week me-2"),
                                    "Effet Weekend"
                                ], className="alert-heading"),
                                html.P("Samedi: -39% de conversion vs Mercredi", className="mb-2"),
                                html.Hr(),
                                html.P("Solution: Optimisation weekend dédiée", className="mb-0 small"),
                            ], color="info", className="mb-3"),
                            
                            dbc.Alert([
                                html.H6([
                                    html.I(className="fas fa-check-circle me-2"),
                                    "Point Fort"
                                ], className="alert-heading"),
                                html.P("Cart→Purchase: 32.56% (très bon taux)", className="mb-2"),
                                html.Hr(),
                                html.P("Focus: Améliorer le funnel amont (view→cart)", className="mb-0 small"),
                            ], color="success", className="mb-3"),
                        ], width=6),
                    ]),
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Footer Note
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "Utilisez la navigation de gauche pour explorer les différentes analyses et résultats des tests A/B. ",
                "Toutes les visualisations sont interactives et peuvent être exportées."
            ], color="light", className="border")
        ])
    ]),
    
], fluid=True)
