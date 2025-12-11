"""
Funnel Page - Detailed Funnel Analysis and Optimization
Page Funnel
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
dash.register_page(__name__, path='/funnel', name='Funnel')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

try:
    df_daily = pd.read_csv(DATA_DIR / "funnel_daily_detailed.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_segment = pd.read_csv(DATA_DIR / "funnel_by_segment.csv")
    df_weekday = pd.read_csv(DATA_DIR / "funnel_by_weekday.csv")
    df_weekly = pd.read_csv(DATA_DIR / "funnel_weekly.csv")
    df_monthly = pd.read_csv(DATA_DIR / "funnel_monthly.csv")
    df_top = pd.read_csv(DATA_DIR / "funnel_top_performers.csv")
    df_blocked = pd.read_csv(DATA_DIR / "funnel_blocked_products.csv")
    df_friction = pd.read_csv(DATA_DIR / "funnel_high_friction_days.csv")
except FileNotFoundError:
    df_daily = None
    df_segment = None
    df_weekday = None
    df_weekly = None
    df_monthly = None
    df_top = None
    df_blocked = None
    df_friction = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-filter me-3"),
                    "Analyse du Funnel"
                ], className="mb-3"),
                html.P(
                    "Analyse détaillée du parcours utilisateur à travers le funnel de conversion "
                    "(Views → Cart → Purchase) avec identification des points de friction.",
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
                        html.H4("1.65M", className="mb-1"),
                        html.P("Views Total", className="text-muted mb-0 small"),
                        html.Small("100% funnel", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-shopping-cart fa-2x text-warning mb-2"),
                        html.H4("68,966", className="mb-1"),
                        html.P("Add to Cart", className="text-muted mb-0 small"),
                        html.Small("4.18% → -95.82%", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-credit-card fa-2x text-success mb-2"),
                        html.H4("22,457", className="mb-1"),
                        html.P("Purchases", className="text-muted mb-0 small"),
                        html.Small("32.56% → -67.44%", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-exclamation-triangle fa-2x text-danger mb-2"),
                        html.H4("97.18%", className="mb-1"),
                        html.P("Drop-off Total", className="text-muted mb-0 small"),
                        html.Small("View → Purchase", className="text-danger"),
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
                        html.I(className="fas fa-funnel-dollar me-2"),
                        "Funnel Principal de Conversion"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='main-funnel', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-pie me-2"),
                        "Distribution Funnel"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='funnel-distribution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=4),
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
                    dcc.Graph(id='funnel-segment', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-day me-2"),
                        "Funnel par Jour de la Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='funnel-weekday', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Daily Funnel Evolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-area me-2"),
                        "Évolution Quotidienne du Funnel"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='funnel-daily-evolution', config={'displayModeBar': True})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Waterfall Drop-off Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-waterfall me-2"),
                        "Analyse des Abandons (Waterfall)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='funnel-waterfall', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=7),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-star me-2"),
                        "Top 10 Performers"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='top-performers', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=5),
    ]),
    
    # Monthly Trends
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-alt me-2"),
                        "Tendances Mensuelles"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='funnel-monthly', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # High Friction Days
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-fire me-2"),
                        "Jours à Forte Friction (Bottom 10)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='friction-table')
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
                    "Insights Clés du Funnel"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li([
                        html.Strong("Friction majeure View → Cart : "),
                        "95.82% des viewers ne mettent pas au panier - optimisation UX critique"
                    ]),
                    html.Li([
                        html.Strong("Cart abandonment : "),
                        "67.44% des paniers abandonnés - opportunité de remarketing et email recovery"
                    ]),
                    html.Li([
                        html.Strong("Premium excellence : "),
                        "31.0% cart→purchase vs 15.9% pour New users (95% supérieur)"
                    ]),
                    html.Li([
                        html.Strong("Dimanche optimal : "),
                        "Meilleure conversion end-to-end - focus marketing weekend"
                    ]),
                    html.Li([
                        html.Strong("223K produits bloqués : "),
                        "Aucune vente sur 94.9% du catalogue - nettoyage et focus sur winners"
                    ]),
                ], className="mb-0")
            ], color="danger", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('main-funnel', 'figure'),
    Input('main-funnel', 'id')
)
def update_main_funnel(_):
    """Create main funnel chart"""
    if df_daily is None:
        return go.Figure()
    
    # Aggregate totals
    total_views = df_daily['view'].sum()
    total_carts = df_daily['addtocart'].sum()
    total_purchases = df_daily['transaction'].sum()
    
    fig = go.Figure(go.Funnel(
        y=['Views', 'Add to Cart', 'Purchases'],
        x=[total_views, total_carts, total_purchases],
        textposition='inside',
        textinfo='value+percent initial+percent previous',
        marker=dict(
            color=['#3498db', '#f39c12', '#2ecc71'],
            line=dict(width=2, color='rgba(0,0,0,0.3)')
        ),
        connector=dict(line=dict(color='rgba(255,255,255,0.3)', width=3))
    ))
    
    fig.update_layout(
        title="Funnel Global de Conversion",
        template='plotly_dark',
        height=500,
        showlegend=False
    )
    
    return fig


@callback(
    Output('funnel-distribution', 'figure'),
    Input('funnel-distribution', 'id')
)
def update_funnel_distribution(_):
    """Create funnel distribution pie"""
    if df_daily is None:
        return go.Figure()
    
    total_views = df_daily['view'].sum()
    total_carts = df_daily['addtocart'].sum()
    total_purchases = df_daily['transaction'].sum()
    
    drop_view_cart = total_views - total_carts
    drop_cart_purchase = total_carts - total_purchases
    
    fig = go.Figure(data=[go.Pie(
        labels=['Purchases', 'Cart Drop-off', 'View Drop-off'],
        values=[total_purchases, drop_cart_purchase, drop_view_cart],
        marker=dict(colors=['#2ecc71', '#f39c12', '#e74c3c']),
        textinfo='label+percent',
        hole=0.4
    )])
    
    fig.update_layout(
        title="Distribution",
        template='plotly_dark',
        height=500,
        showlegend=True
    )
    
    return fig


@callback(
    Output('funnel-segment', 'figure'),
    Input('funnel-segment', 'id')
)
def update_funnel_segment(_):
    """Create funnel by segment"""
    if df_segment is None:
        return go.Figure()
    
    fig = go.Figure()
    
    segments = df_segment['segment'].tolist()
    
    # Conversion rate by segment
    fig.add_trace(go.Bar(
        name='Taux de Conversion',
        x=segments,
        y=df_segment['conversion_rate'],
        marker=dict(
            color=df_segment['conversion_rate'],
            colorscale='Greens',
            showscale=False
        ),
        text=[f"{val:.1f}%" for val in df_segment['conversion_rate']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Taux de Conversion par Segment",
        xaxis_title="Segment",
        yaxis_title="Taux (%)",
        template='plotly_dark',
        height=400,
        barmode='group'
    )
    
    return fig


@callback(
    Output('funnel-weekday', 'figure'),
    Input('funnel-weekday', 'id')
)
def update_funnel_weekday(_):
    """Create funnel by weekday"""
    if df_weekday is None:
        return go.Figure()
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_sorted = df_weekday.set_index('weekday').loc[days_order].reset_index()
    
    fig = go.Figure()
    
    # View to cart
    fig.add_trace(go.Bar(
        name='View → Cart %',
        x=df_sorted['weekday'],
        y=df_sorted['view_to_cart_pct'],
        marker_color='#3498db'
    ))
    
    # View to purchase
    fig.add_trace(go.Bar(
        name='View → Purchase %',
        x=df_sorted['weekday'],
        y=df_sorted['view_to_purchase_pct'],
        marker_color='#2ecc71'
    ))
    
    fig.update_layout(
        title="Taux de Conversion par Jour",
        xaxis_title="Jour",
        yaxis_title="Taux (%)",
        template='plotly_dark',
        height=400,
        barmode='group'
    )
    
    return fig


@callback(
    Output('funnel-daily-evolution', 'figure'),
    Input('funnel-daily-evolution', 'id')
)
def update_funnel_daily_evolution(_):
    """Create daily funnel evolution"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Views
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['view'],
        mode='lines',
        name='Views',
        line=dict(color='#3498db', width=1),
        stackgroup='one',
        fillcolor='rgba(52, 152, 219, 0.5)'
    ))
    
    # Add to cart
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['addtocart'],
        mode='lines',
        name='Add to Cart',
        line=dict(color='#f39c12', width=1),
        yaxis='y'
    ))
    
    # Purchases
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['transaction'],
        mode='lines',
        name='Purchases',
        line=dict(color='#2ecc71', width=2),
        yaxis='y'
    ))
    
    fig.update_layout(
        title="Évolution Quotidienne des Étapes du Funnel",
        xaxis_title="Date",
        yaxis_title="Nombre",
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
    Output('funnel-waterfall', 'figure'),
    Input('funnel-waterfall', 'id')
)
def update_funnel_waterfall(_):
    """Create waterfall drop-off chart"""
    if df_daily is None:
        return go.Figure()
    
    total_views = df_daily['view'].sum()
    total_carts = df_daily['addtocart'].sum()
    total_purchases = df_daily['transaction'].sum()
    
    drop_view_cart = -(total_views - total_carts)
    drop_cart_purchase = -(total_carts - total_purchases)
    
    fig = go.Figure(go.Waterfall(
        x=['Views', 'Drop View→Cart', 'Cart', 'Drop Cart→Purchase', 'Purchases'],
        y=[total_views, drop_view_cart, 0, drop_cart_purchase, 0],
        measure=['absolute', 'relative', 'total', 'relative', 'total'],
        text=[f"{total_views:,}", f"{drop_view_cart:,}", f"{total_carts:,}", 
              f"{drop_cart_purchase:,}", f"{total_purchases:,}"],
        textposition='outside',
        connector=dict(line=dict(color='rgba(255,255,255,0.3)')),
        decreasing=dict(marker=dict(color='#e74c3c')),
        increasing=dict(marker=dict(color='#2ecc71')),
        totals=dict(marker=dict(color='#3498db'))
    ))
    
    fig.update_layout(
        title="Analyse des Abandons (Waterfall)",
        yaxis_title="Utilisateurs",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('top-performers', 'figure'),
    Input('top-performers', 'id')
)
def update_top_performers(_):
    """Create top performers chart"""
    if df_top is None:
        return go.Figure()
    
    top10 = df_top.head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top10['view_to_purchase_rate'],
        y=[f"P{pid}" for pid in top10['product_id']],
        orientation='h',
        marker=dict(
            color=top10['view_to_purchase_rate'],
            colorscale='Greens',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"{val:.1f}%" for val in top10['view_to_purchase_rate']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Top 10 Produits (View→Purchase)",
        xaxis_title="Conversion %",
        yaxis_title="",
        template='plotly_dark',
        height=400,
        showlegend=False,
        yaxis=dict(autorange='reversed')
    )
    
    return fig


@callback(
    Output('funnel-monthly', 'figure'),
    Input('funnel-monthly', 'id')
)
def update_funnel_monthly(_):
    """Create monthly trends"""
    if df_monthly is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # View to cart
    fig.add_trace(go.Scatter(
        x=df_monthly['month'],
        y=df_monthly['view_to_cart_pct'],
        mode='lines+markers',
        name='View → Cart %',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10)
    ))
    
    # View to purchase
    fig.add_trace(go.Scatter(
        x=df_monthly['month'],
        y=df_monthly['view_to_purchase_pct'],
        mode='lines+markers',
        name='View → Purchase %',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Évolution Mensuelle des Taux de Conversion",
        xaxis_title="Mois",
        yaxis_title="Taux (%)",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig


@callback(
    Output('friction-table', 'children'),
    Input('friction-table', 'id')
)
def update_friction_table(_):
    """Create high friction days table"""
    if df_friction is None:
        return html.P("Données non disponibles")
    
    # Create table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Date"),
            html.Th("Jour"),
            html.Th("Views"),
            html.Th("Carts"),
            html.Th("Purchases"),
            html.Th("View→Cart %"),
            html.Th("Cart→Purchase %"),
            html.Th("Drop-off Total"),
        ]))
    ]
    
    table_body = [html.Tbody([
        html.Tr([
            html.Td(row['date']),
            html.Td(row['weekday']),
            html.Td(f"{row['view']:,}"),
            html.Td(f"{row['addtocart']:,}"),
            html.Td(f"{row['transaction']:,}"),
            html.Td(html.Span(f"{row['view_to_cart_pct']:.2f}%", className="text-warning")),
            html.Td(html.Span(f"{row['cart_to_purchase_pct']:.2f}%", className="text-warning")),
            html.Td(html.Span(f"{100-row['view_to_purchase_pct']:.2f}%", className="text-danger")),
        ]) for idx, row in df_friction.iterrows()
    ])]
    
    return dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size='sm',
        className='table-sm'
    )
