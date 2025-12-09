"""
Conversions Page - Conversion Rate Analysis and Optimization
Page Conversions
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

# Register this page
dash.register_page(__name__, path='/conversions', name='Conversions')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

try:
    df_daily = pd.read_csv(DATA_DIR / "conversion_daily.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_segment = pd.read_csv(DATA_DIR / "conversion_by_segment.csv")
    df_weekday = pd.read_csv(DATA_DIR / "conversion_by_weekday.csv")
    df_funnel_analysis = pd.read_csv(DATA_DIR / "conversion_funnel_analysis.csv")
    df_evolution = pd.read_csv(DATA_DIR / "conversion_evolution.csv")
except FileNotFoundError:
    df_daily = None
    df_segment = None
    df_weekday = None
    df_funnel_analysis = None
    df_evolution = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-shopping-cart me-3"),
                    "Analyse des Conversions"
                ], className="mb-3"),
                html.P(
                    "Analyse complète des taux de conversion à travers le funnel (View → Cart → Purchase) "
                    "avec segmentation et opportunités d'optimisation.",
                    className="lead text-muted"
                ),
            ], className="mb-4")
        ])
    ]),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-eye fa-2x text-info mb-2"),
                        html.H4("2.59%", className="mb-1"),
                        html.P("View → Cart", className="text-muted mb-0 small"),
                        html.Small("Taux moyen", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-shopping-basket fa-2x text-warning mb-2"),
                        html.H4("32.56%", className="mb-1"),
                        html.P("Cart → Purchase", className="text-muted mb-0 small"),
                        html.Small("Taux moyen", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-check-circle fa-2x text-success mb-2"),
                        html.H4("0.84%", className="mb-1"),
                        html.P("View → Purchase", className="text-muted mb-0 small"),
                        html.Small("Global", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-euro-sign fa-2x text-primary mb-2"),
                        html.H4("€255.36", className="mb-1"),
                        html.P("AOV Moyen", className="text-muted mb-0 small"),
                        html.Small("Panier moyen", className="text-primary"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Conversion Rates Evolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-line me-2"),
                        "Évolution des Taux de Conversion"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-evolution', config={'displayModeBar': True})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Conversion by Weekday and Segment
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-week me-2"),
                        "Conversion par Jour de la Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-weekday', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-user-tag me-2"),
                        "Conversion par Segment"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-segment', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # AOV Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-money-bill-wave me-2"),
                        "Évolution du Panier Moyen (AOV)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='aov-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-pie me-2"),
                        "AOV par Segment"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='aov-segment', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=4),
    ]),
    
    # Conversion Efficiency
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-tachometer-alt me-2"),
                        "Efficacité de Conversion"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-efficiency', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Revenue par Utilisateur"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='revenue-per-user', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Heatmap: Conversion by Day x Week
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-th me-2"),
                        "Heatmap: Conversion Rate (Jour × Semaine)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-rate-heatmap', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Insights
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H6([
                    html.I(className="fas fa-lightbulb me-2"),
                    "Insights Clés sur les Conversions"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li([
                        html.Strong("Cart abandonment élevé : "),
                        "67.44% des utilisateurs qui ajoutent au panier n'achètent pas - friction majeure"
                    ]),
                    html.Li([
                        html.Strong("Premium champions : "),
                        "31.0 transactions/user vs 0.45 pour New users (69x supérieur)"
                    ]),
                    html.Li([
                        html.Strong("Meilleur jour : "),
                        "Dimanche avec 0.92% view→purchase (9% supérieur à la moyenne)"
                    ]),
                    html.Li([
                        html.Strong("AOV stable : "),
                        "€255.36 moyen avec faible variance (€250-€260) - pricing cohérent"
                    ]),
                    html.Li([
                        html.Strong("Opportunité Regular : "),
                        "273% conversion rate mais seulement 2.73 transactions/user - potentiel d'augmentation fréquence"
                    ]),
                ], className="mb-0")
            ], color="warning", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('conversion-evolution', 'figure'),
    Input('conversion-evolution', 'id')
)
def update_conversion_evolution(_):
    """Create conversion rates evolution chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # View to cart
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['view_to_cart_rate'],
        mode='lines',
        name='View → Cart',
        line=dict(color='#3498db', width=2),
    ))
    
    # Cart to purchase
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['cart_to_purchase_rate'],
        mode='lines',
        name='Cart → Purchase',
        line=dict(color='#e74c3c', width=2),
    ))
    
    # View to purchase
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['view_to_purchase_rate'],
        mode='lines',
        name='View → Purchase',
        line=dict(color='#2ecc71', width=2),
    ))
    
    # Moving averages
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['ma7_conversion'],
        mode='lines',
        name='MA7 (View→Purchase)',
        line=dict(color='#f39c12', width=2, dash='dash'),
    ))
    
    fig.update_layout(
        title="Taux de Conversion Quotidiens avec Moyenne Mobile 7 Jours",
        xaxis_title="Date",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=450,
        hovermode='x unified',
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
    Output('conversion-weekday', 'figure'),
    Input('conversion-weekday', 'id')
)
def update_conversion_weekday(_):
    """Create conversion by weekday chart"""
    if df_weekday is None:
        return go.Figure()
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_sorted = df_weekday.set_index('day_of_week').loc[days_order].reset_index()
    
    fig = go.Figure()
    
    # View to cart
    fig.add_trace(go.Bar(
        name='View → Cart',
        x=df_sorted['day_of_week'],
        y=df_sorted['view_to_cart'],
        marker_color='#3498db',
        text=[f"{val:.2f}%" for val in df_sorted['view_to_cart']],
        textposition='outside',
    ))
    
    # Cart to purchase
    fig.add_trace(go.Bar(
        name='Cart → Purchase',
        x=df_sorted['day_of_week'],
        y=df_sorted['cart_to_purchase'],
        marker_color='#2ecc71',
        text=[f"{val:.1f}%" for val in df_sorted['cart_to_purchase']],
        textposition='outside',
    ))
    
    fig.update_layout(
        title="Taux de Conversion par Jour de la Semaine",
        xaxis_title="Jour",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=400,
        barmode='group'
    )
    
    return fig


@callback(
    Output('conversion-segment', 'figure'),
    Input('conversion-segment', 'id')
)
def update_conversion_segment(_):
    """Create conversion by segment chart"""
    if df_segment is None:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_segment['segment'],
        y=df_segment['conversion_rate'],
        marker=dict(
            color=df_segment['conversion_rate'],
            colorscale='Greens',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"{val:.1f}%" for val in df_segment['conversion_rate']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Conversion: %{y:.2f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Taux de Conversion par Segment",
        xaxis_title="Segment",
        yaxis_title="Conversion Rate (%)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('aov-evolution', 'figure'),
    Input('aov-evolution', 'id')
)
def update_aov_evolution(_):
    """Create AOV evolution chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Daily AOV
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['avg_order_value'],
        mode='lines',
        name='AOV Quotidien',
        line=dict(color='#9b59b6', width=1),
        fill='tozeroy',
        fillcolor='rgba(155, 89, 182, 0.2)',
    ))
    
    # 7-day MA
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['ma7_aov'],
        mode='lines',
        name='MA7 AOV',
        line=dict(color='#e74c3c', width=3),
    ))
    
    # Average line
    avg_aov = df_daily['avg_order_value'].mean()
    fig.add_hline(y=avg_aov, line_dash="dash", line_color="orange",
                  annotation_text=f"Moyenne: €{avg_aov:.2f}")
    
    fig.update_layout(
        title="Évolution du Panier Moyen (AOV)",
        xaxis_title="Date",
        yaxis_title="AOV (€)",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig


@callback(
    Output('aov-segment', 'figure'),
    Input('aov-segment', 'id')
)
def update_aov_segment(_):
    """Create AOV by segment pie chart"""
    if df_segment is None:
        return go.Figure()
    
    colors = {'Premium': '#e74c3c', 'Regular': '#3498db', 'Occasional': '#f39c12', 'New': '#95a5a6'}
    
    fig = go.Figure(data=[go.Pie(
        labels=df_segment['segment'],
        values=df_segment['avg_transaction'],
        marker=dict(colors=[colors.get(s, '#95a5a6') for s in df_segment['segment']]),
        textinfo='label+value',
        hovertemplate='<b>%{label}</b><br>' +
                      'AOV: €%{value:.2f}<br>' +
                      '<extra></extra>'
    )])
    
    fig.update_layout(
        title="AOV Moyen par Segment",
        template='plotly_dark',
        height=400,
        showlegend=True
    )
    
    return fig


@callback(
    Output('conversion-efficiency', 'figure'),
    Input('conversion-efficiency', 'id')
)
def update_conversion_efficiency(_):
    """Create conversion efficiency chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['conversion_efficiency'],
        mode='lines+markers',
        line=dict(color='#3498db', width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)',
        hovertemplate='<b>%{x}</b><br>' +
                      'Efficiency: %{y:.2f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Efficacité de Conversion Quotidienne",
        xaxis_title="Date",
        yaxis_title="Efficiency Index",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('revenue-per-user', 'figure'),
    Input('revenue-per-user', 'id')
)
def update_revenue_per_user(_):
    """Create revenue per user chart"""
    if df_segment is None:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_segment['segment'],
        y=df_segment['revenue_per_user'],
        marker=dict(
            color=df_segment['revenue_per_user'],
            colorscale='Reds',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"€{val:.2f}" for val in df_segment['revenue_per_user']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Revenue/User: €%{y:.2f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Revenue Moyen par Utilisateur (Segment)",
        xaxis_title="Segment",
        yaxis_title="Revenue/User (€)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('conversion-rate-heatmap', 'figure'),
    Input('conversion-rate-heatmap', 'id')
)
def update_conversion_rate_heatmap(_):
    """Create conversion heatmap"""
    if df_daily is None:
        return go.Figure()
    
    # Create pivot table
    df_daily['week'] = df_daily['date'].dt.isocalendar().week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_daily['day_of_week'] = pd.Categorical(df_daily['day_of_week'], categories=days_order, ordered=True)
    
    pivot = df_daily.pivot_table(
        values='view_to_purchase_rate',
        index='day_of_week',
        columns='week',
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        hovertemplate='Semaine %{x}<br>%{y}<br>Conversion: %{z:.2f}%<br><extra></extra>'
    ))
    
    fig.update_layout(
        title="Heatmap des Taux de Conversion (View→Purchase)",
        xaxis_title="Semaine",
        yaxis_title="Jour",
        template='plotly_dark',
        height=400
    )
    
    return fig
