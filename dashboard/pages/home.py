"""
Home Page - Dashboard Overview with Interactive Charts
Issue #20 - KPIs + Traffic + Revenue
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from datetime import datetime

# Register this page with dash.page_registry
dash.register_page(__name__, path='/', name='Accueil')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

# Load daily metrics
try:
    df_daily = pd.read_csv(DATA_DIR / "daily_metrics.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
except FileNotFoundError:
    df_daily = None

# Load AB test summary
try:
    df_ab = pd.read_csv(DATA_DIR / "ab_test_summary_by_scenario.csv")
except FileNotFoundError:
    df_ab = None

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
    
    # Interactive Charts Section
    dbc.Row([
        dbc.Col([
            html.H4([
                html.I(className="fas fa-chart-line me-2"),
                "Évolution des KPIs"
            ], className="mb-3 mt-4"),
        ])
    ]),
    
    # Traffic and Revenue Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-users me-2"),
                        "Trafic Quotidien"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='traffic-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-euro-sign me-2"),
                        "Revenue Quotidien"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='revenue-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Conversion Funnel and Weekend Effect
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-percentage me-2"),
                        "Taux de Conversion"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-week me-2"),
                        "Effet Jour de la Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekday-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # A/B Test ROI Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Comparaison ROI des Scénarios A/B"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='ab-roi-chart', config={'displayModeBar': False})
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


# Callbacks for interactive charts
@callback(
    Output('traffic-chart', 'figure'),
    Input('traffic-chart', 'id')
)
def update_traffic_chart(_):
    """Create traffic evolution chart"""
    if df_daily is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # Daily traffic
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['unique_users'],
        mode='lines',
        name='Utilisateurs Quotidiens',
        line=dict(color='#667eea', width=2),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # 7-day moving average
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['ma7_users'],
        mode='lines',
        name='Moyenne Mobile 7j',
        line=dict(color='#764ba2', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Évolution du Trafic (Mai - Sept 2015)",
        xaxis_title="Date",
        yaxis_title="Utilisateurs Uniques",
        hovermode='x unified',
        template='plotly_dark',
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@callback(
    Output('revenue-chart', 'figure'),
    Input('revenue-chart', 'id')
)
def update_revenue_chart(_):
    """Create revenue evolution chart"""
    if df_daily is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # Daily revenue
    fig.add_trace(go.Bar(
        x=df_daily['date'],
        y=df_daily['daily_revenue'],
        name='Revenue Quotidien',
        marker_color='#2ecc71',
        opacity=0.7
    ))
    
    # 7-day moving average
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['ma7_revenue'],
        mode='lines',
        name='Moyenne Mobile 7j',
        line=dict(color='#e74c3c', width=3)
    ))
    
    fig.update_layout(
        title="Évolution du Revenue (Mai - Sept 2015)",
        xaxis_title="Date",
        yaxis_title="Revenue (€)",
        hovermode='x unified',
        template='plotly_dark',
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@callback(
    Output('conversion-chart', 'figure'),
    Input('conversion-chart', 'id')
)
def update_conversion_chart(_):
    """Create conversion rates evolution chart"""
    if df_daily is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # View to Cart
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['view_to_cart_rate'],
        mode='lines+markers',
        name='View → Cart',
        line=dict(color='#3498db', width=2),
        marker=dict(size=4)
    ))
    
    # Cart to Purchase
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['cart_to_purchase_rate'],
        mode='lines+markers',
        name='Cart → Purchase',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=4)
    ))
    
    # View to Purchase
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['view_to_purchase_rate'],
        mode='lines+markers',
        name='View → Purchase',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Taux de Conversion par Étape du Funnel",
        xaxis_title="Date",
        yaxis_title="Taux de Conversion (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@callback(
    Output('weekday-chart', 'figure'),
    Input('weekday-chart', 'id')
)
def update_weekday_chart(_):
    """Create weekday effect chart"""
    if df_daily is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Aggregate by day of week
    weekday_stats = df_daily.groupby('day_of_week').agg({
        'unique_users': 'mean',
        'daily_revenue': 'mean',
        'view_to_purchase_rate': 'mean'
    }).reset_index()
    
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_stats['day_of_week'] = pd.Categorical(weekday_stats['day_of_week'], categories=days_order, ordered=True)
    weekday_stats = weekday_stats.sort_values('day_of_week')
    
    # French day names
    french_days = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }
    weekday_stats['day_fr'] = weekday_stats['day_of_week'].map(french_days)
    
    fig = go.Figure()
    
    # Users bar
    fig.add_trace(go.Bar(
        x=weekday_stats['day_fr'],
        y=weekday_stats['unique_users'],
        name='Utilisateurs Moy.',
        marker_color='#667eea',
        yaxis='y',
        opacity=0.7
    ))
    
    # Conversion rate line
    fig.add_trace(go.Scatter(
        x=weekday_stats['day_fr'],
        y=weekday_stats['view_to_purchase_rate'],
        name='Taux Conversion (%)',
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Performance par Jour de la Semaine",
        xaxis_title="Jour",
        yaxis_title="Utilisateurs Moyens",
        yaxis2=dict(
            title="Taux de Conversion (%)",
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        template='plotly_dark',
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@callback(
    Output('ab-roi-chart', 'figure'),
    Input('ab-roi-chart', 'id')
)
def update_ab_roi_chart(_):
    """Create A/B test ROI comparison chart"""
    if df_ab is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Sort by annual ROI
    df_sorted = df_ab.sort_values('annual_roi_pct', ascending=True)
    
    fig = go.Figure()
    
    # ROI bars
    colors = ['#2ecc71' if roi > 30000 else '#3498db' if roi > 20000 else '#f39c12' 
              for roi in df_sorted['annual_roi_pct']]
    
    fig.add_trace(go.Bar(
        x=df_sorted['annual_roi_pct'],
        y=df_sorted['scenario_name'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0.2)', width=1)
        ),
        text=[f"+{roi:,.0f}%" for roi in df_sorted['annual_roi_pct']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      'ROI Annuel: +%{x:,.0f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="ROI Annuel par Scénario A/B (Top 8)",
        xaxis_title="ROI Annuel (%)",
        yaxis_title="",
        template='plotly_dark',
        height=400,
        showlegend=False,
        xaxis=dict(
            tickformat=',.0f',
            ticksuffix='%'
        )
    )
    
    return fig
