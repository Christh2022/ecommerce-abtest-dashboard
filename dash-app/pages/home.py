"""
Page d'accueil - Dashboard principal avec KPIs
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Accueil')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Vue d'ensemble - KPIs E-commerce", className="text-primary mb-4")
        ])
    ]),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Chiffre d'affaires", className="card-title"),
                    html.H2("€ 125,430", className="text-success"),
                    html.P("+12.5% vs mois dernier", className="text-muted small")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Taux de conversion", className="card-title"),
                    html.H2("3.2%", className="text-primary"),
                    html.P("+0.5% vs mois dernier", className="text-muted small")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Panier moyen", className="card-title"),
                    html.H2("€ 85.50", className="text-info"),
                    html.P("-2.3% vs mois dernier", className="text-muted small")
                ])
            ], className="shadow-sm")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Utilisateurs actifs", className="card-title"),
                    html.H2("1,248", className="text-warning"),
                    html.P("+8.7% vs mois dernier", className="text-muted small")
                ])
            ], className="shadow-sm")
        ], width=3),
    ], className="mb-4"),
    
    # Graphiques
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Évolution du chiffre d'affaires"),
                dbc.CardBody([
                    dcc.Graph(id='revenue-chart')
                ])
            ], className="shadow-sm")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Répartition par canal"),
                dbc.CardBody([
                    dcc.Graph(id='channel-chart')
                ])
            ], className="shadow-sm")
        ], width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 5 produits"),
                dbc.CardBody([
                    dcc.Graph(id='top-products-chart')
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Conversion par segment"),
                dbc.CardBody([
                    dcc.Graph(id='segment-conversion-chart')
                ])
            ], className="shadow-sm")
        ], width=6),
    ])
], fluid=True)


# Callbacks pour les graphiques (données mockées pour l'instant)
@callback(
    Output('revenue-chart', 'figure'),
    Input('revenue-chart', 'id')
)
def update_revenue_chart(_):
    # Données de démonstration
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    revenue = [95000, 98000, 102000, 105000, 110000, 115000, 120000, 125000, 130000, 128000, 132000, 135000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=revenue, mode='lines+markers', name='CA mensuel'))
    fig.update_layout(template='plotly_white', hovermode='x unified')
    return fig


@callback(
    Output('channel-chart', 'figure'),
    Input('channel-chart', 'id')
)
def update_channel_chart(_):
    fig = go.Figure(data=[go.Pie(
        labels=['Organique', 'Publicité', 'Email', 'Social', 'Direct'],
        values=[35, 25, 15, 15, 10],
        hole=.3
    )])
    fig.update_layout(template='plotly_white')
    return fig


@callback(
    Output('top-products-chart', 'figure'),
    Input('top-products-chart', 'id')
)
def update_top_products(_):
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    sales = [1200, 980, 850, 720, 650]
    
    fig = go.Figure(data=[go.Bar(x=sales, y=products, orientation='h')])
    fig.update_layout(template='plotly_white', xaxis_title="Ventes")
    return fig


@callback(
    Output('segment-conversion-chart', 'figure'),
    Input('segment-conversion-chart', 'id')
)
def update_segment_conversion(_):
    segments = ['Premium', 'Regular', 'Occasional', 'New']
    conversion = [5.2, 3.8, 2.1, 1.5]
    
    fig = go.Figure(data=[go.Bar(x=segments, y=conversion)])
    fig.update_layout(template='plotly_white', yaxis_title="Taux de conversion (%)")
    return fig
