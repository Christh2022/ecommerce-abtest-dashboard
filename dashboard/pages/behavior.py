"""
Behavior Page - User Behavior Analysis with Funnel and Heatmap
Issue #21 - Funnel + Heatmap
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
dash.register_page(__name__, path='/behavior', name='Comportement')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

# Load funnel data
try:
    df_funnel_daily = pd.read_csv(DATA_DIR / "funnel_daily_detailed.csv")
    df_funnel_daily['date'] = pd.to_datetime(df_funnel_daily['date'])
except FileNotFoundError:
    df_funnel_daily = None

try:
    df_funnel_segment = pd.read_csv(DATA_DIR / "funnel_by_segment.csv")
except FileNotFoundError:
    df_funnel_segment = None

try:
    df_funnel_weekday = pd.read_csv(DATA_DIR / "funnel_by_weekday.csv")
except FileNotFoundError:
    df_funnel_weekday = None

try:
    df_daily = pd.read_csv(DATA_DIR / "daily_metrics.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
except FileNotFoundError:
    df_daily = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-mouse-pointer me-3"),
                    "Analyse du Comportement Utilisateur"
                ], className="mb-3"),
                html.P(
                    "Explorez le funnel de conversion et les patterns de comportement des utilisateurs "
                    "pour identifier les points de friction et opportunités d'optimisation.",
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
                        html.I(className="fas fa-eye fa-2x text-primary mb-2"),
                        html.H4("2.59%", className="mb-1"),
                        html.P("View → Cart", className="text-muted mb-0 small"),
                        html.Small("97.41% d'abandon", className="text-danger"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-shopping-cart fa-2x text-success mb-2"),
                        html.H4("32.56%", className="mb-1"),
                        html.P("Cart → Purchase", className="text-muted mb-0 small"),
                        html.Small("Bon taux", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-percent fa-2x text-info mb-2"),
                        html.H4("0.84%", className="mb-1"),
                        html.P("View → Purchase", className="text-muted mb-0 small"),
                        html.Small("Global conversion", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x text-warning mb-2"),
                        html.H4("30x", className="mb-1"),
                        html.P("Premium vs New", className="text-muted mb-0 small"),
                        html.Small("Conversion rate", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Main Funnel Visualization
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-filter me-2"),
                        "Funnel de Conversion Global"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='main-funnel-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Funnel by Segment and Weekday
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-user-tag me-2"),
                        "Funnel par Segment Utilisateur"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='segment-funnel-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-week me-2"),
                        "Funnel par Jour de la Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekday-funnel-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Heatmap Section
    dbc.Row([
        dbc.Col([
            html.H4([
                html.I(className="fas fa-fire me-2"),
                "Heatmaps Comportementales"
            ], className="mb-3 mt-2"),
        ])
    ]),
    
    # Conversion Heatmap and Traffic Heatmap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-th me-2"),
                        "Heatmap Taux de Conversion (Jour × Semaine)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='conversion-heatmap', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-area me-2"),
                        "Heatmap Trafic (Jour × Semaine)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='traffic-heatmap', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Drop-off Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Analyse des Abandons"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='dropoff-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Insights Section
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H6([
                    html.I(className="fas fa-lightbulb me-2"),
                    "Insights Clés"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li("97.41% des utilisateurs abandonnent avant d'ajouter au panier - problème majeur d'engagement produit"),
                    html.Li("Les utilisateurs Premium ont un taux de conversion 30x supérieur aux nouveaux utilisateurs"),
                    html.Li("Le samedi affiche le pire taux de conversion (-39% vs mercredi), suggérant un manque d'optimisation weekend"),
                    html.Li("Le funnel cart→purchase est performant (32.56%), l'optimisation doit se concentrer sur view→cart"),
                ], className="mb-0")
            ], color="info", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('main-funnel-chart', 'figure'),
    Input('main-funnel-chart', 'id')
)
def update_main_funnel(_):
    """Create main funnel visualization"""
    if df_funnel_daily is None:
        return go.Figure()
    
    # Calculate totals
    total_views = df_funnel_daily['view'].sum()
    total_carts = df_funnel_daily['addtocart'].sum()
    total_purchases = df_funnel_daily['transaction'].sum()
    
    fig = go.Figure()
    
    # Funnel chart
    fig.add_trace(go.Funnel(
        name='Funnel Global',
        y=['Views', 'Add to Cart', 'Transactions'],
        x=[total_views, total_carts, total_purchases],
        textposition="inside",
        textinfo="value+percent initial+percent previous",
        marker=dict(
            color=['#667eea', '#e74c3c', '#2ecc71'],
        ),
        connector=dict(
            line=dict(
                color='rgba(0,0,0,0.2)',
                width=2
            )
        )
    ))
    
    fig.update_layout(
        title=f"Funnel de Conversion (Total: {total_views:,} views → {total_purchases:,} transactions)",
        height=450,
        template='plotly_dark',
        showlegend=False
    )
    
    return fig


@callback(
    Output('segment-funnel-chart', 'figure'),
    Input('segment-funnel-chart', 'id')
)
def update_segment_funnel(_):
    """Create segment funnel comparison"""
    if df_funnel_segment is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Sort by conversion rate
    df_sorted = df_funnel_segment.sort_values('conversion_rate', ascending=False)
    
    colors = {
        'Premium': '#2ecc71',
        'Regular': '#3498db',
        'Occasional': '#f39c12',
        'New': '#e74c3c'
    }
    
    for idx, row in df_sorted.iterrows():
        fig.add_trace(go.Bar(
            name=row['segment'],
            x=[row['segment']],
            y=[row['conversion_rate']],
            marker_color=colors.get(row['segment'], '#95a5a6'),
            text=f"{row['conversion_rate']:.2f}%",
            textposition='outside',
            hovertemplate=f"<b>{row['segment']}</b><br>" +
                         f"Conversion: {row['conversion_rate']:.2f}%<br>" +
                         f"Utilisateurs: {row['num_users']:,}<br>" +
                         f"Transactions: {row['num_transactions']:,}<br>" +
                         f"Revenue/User: €{row['revenue_per_user']:.2f}<br>" +
                         "<extra></extra>"
        ))
    
    fig.update_layout(
        title="Taux de Conversion par Segment (View → Purchase)",
        xaxis_title="Segment",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=400,
        showlegend=False,
        yaxis=dict(range=[0, max(df_sorted['conversion_rate']) * 1.2])
    )
    
    return fig


@callback(
    Output('weekday-funnel-chart', 'figure'),
    Input('weekday-funnel-chart', 'id')
)
def update_weekday_funnel(_):
    """Create weekday funnel comparison"""
    if df_funnel_weekday is None:
        return go.Figure()
    
    # Order days
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_weekday = df_funnel_weekday.copy()
    df_weekday['weekday'] = pd.Categorical(df_weekday['weekday'], categories=days_order, ordered=True)
    df_weekday = df_weekday.sort_values('weekday')
    
    # French day names
    french_days = {
        'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mer',
        'Thursday': 'Jeu', 'Friday': 'Ven', 'Saturday': 'Sam', 'Sunday': 'Dim'
    }
    df_weekday['day_fr'] = df_weekday['weekday'].map(french_days)
    
    fig = go.Figure()
    
    # View to Cart
    fig.add_trace(go.Bar(
        name='View → Cart',
        x=df_weekday['day_fr'],
        y=df_weekday['view_to_cart_pct'],
        marker_color='#3498db',
        text=[f"{val:.2f}%" for val in df_weekday['view_to_cart_pct']],
        textposition='outside'
    ))
    
    # Cart to Purchase
    fig.add_trace(go.Bar(
        name='Cart → Purchase',
        x=df_weekday['day_fr'],
        y=df_weekday['cart_to_purchase_pct'],
        marker_color='#2ecc71',
        text=[f"{val:.2f}%" for val in df_weekday['cart_to_purchase_pct']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Conversion par Jour de la Semaine",
        xaxis_title="Jour",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=400,
        barmode='group',
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
    Output('conversion-heatmap', 'figure'),
    Input('conversion-heatmap', 'id')
)
def update_conversion_heatmap(_):
    """Create conversion rate heatmap"""
    if df_daily is None:
        return go.Figure()
    
    # Create pivot table for heatmap
    df_daily['week'] = df_daily['date'].dt.isocalendar().week
    df_daily['weekday_num'] = df_daily['date'].dt.dayofweek
    
    pivot = df_daily.pivot_table(
        values='view_to_purchase_rate',
        index='weekday_num',
        columns='week',
        aggfunc='mean'
    )
    
    # Day names
    day_labels = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[f"S{w}" for w in pivot.columns],
        y=day_labels,
        colorscale='RdYlGn',
        text=np.round(pivot.values, 2),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Conv. %")
    ))
    
    fig.update_layout(
        title="Heatmap: Taux de Conversion par Jour et Semaine",
        xaxis_title="Semaine de l'année",
        yaxis_title="Jour de la semaine",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('traffic-heatmap', 'figure'),
    Input('traffic-heatmap', 'id')
)
def update_traffic_heatmap(_):
    """Create traffic heatmap"""
    if df_daily is None:
        return go.Figure()
    
    # Create pivot table for heatmap
    df_daily['week'] = df_daily['date'].dt.isocalendar().week
    df_daily['weekday_num'] = df_daily['date'].dt.dayofweek
    
    pivot = df_daily.pivot_table(
        values='unique_users',
        index='weekday_num',
        columns='week',
        aggfunc='mean'
    )
    
    # Day names
    day_labels = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[f"S{w}" for w in pivot.columns],
        y=day_labels,
        colorscale='Blues',
        text=np.round(pivot.values, 0),
        texttemplate='%{text:,.0f}',
        textfont={"size": 10},
        colorbar=dict(title="Users")
    ))
    
    fig.update_layout(
        title="Heatmap: Trafic Utilisateurs par Jour et Semaine",
        xaxis_title="Semaine de l'année",
        yaxis_title="Jour de la semaine",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('dropoff-chart', 'figure'),
    Input('dropoff-chart', 'id')
)
def update_dropoff_chart(_):
    """Create drop-off analysis chart"""
    if df_funnel_daily is None:
        return go.Figure()
    
    # Calculate average drop-off rates
    avg_view_to_cart = df_funnel_daily['view_to_cart_pct'].mean()
    avg_cart_to_purchase = df_funnel_daily['cart_to_purchase_pct'].mean()
    
    # Drop-off percentages
    dropoff_view_to_cart = 100 - avg_view_to_cart
    dropoff_cart_to_purchase = 100 - avg_cart_to_purchase
    
    fig = go.Figure()
    
    # Waterfall chart
    fig.add_trace(go.Waterfall(
        name="Drop-off",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Views (100%)", f"Abandon View→Cart<br>(-{dropoff_view_to_cart:.1f}%)", 
           f"Abandon Cart→Purchase<br>(-{dropoff_cart_to_purchase * avg_view_to_cart / 100:.1f}%)", 
           "Transactions Finales"],
        textposition="outside",
        text=[
            "100%",
            f"-{dropoff_view_to_cart:.1f}%",
            f"-{dropoff_cart_to_purchase * avg_view_to_cart / 100:.1f}%",
            f"{avg_view_to_cart * avg_cart_to_purchase / 100:.2f}%"
        ],
        y=[100, -dropoff_view_to_cart, -dropoff_cart_to_purchase * avg_view_to_cart / 100, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        increasing={"marker": {"color": "#2ecc71"}},
        totals={"marker": {"color": "#3498db"}}
    ))
    
    fig.update_layout(
        title="Analyse des Abandons dans le Funnel (Waterfall)",
        yaxis_title="Pourcentage",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig
