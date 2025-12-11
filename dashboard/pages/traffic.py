"""
Traffic & Users Page - Traffic Analysis and User Segmentation
Page Traffic & Utilisateurs
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
dash.register_page(__name__, path='/traffic', name='Trafic & Utilisateurs')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

try:
    df_daily = pd.read_csv(DATA_DIR / "traffic_daily.csv")
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_weekly = pd.read_csv(DATA_DIR / "traffic_weekly.csv")
    df_weekday = pd.read_csv(DATA_DIR / "traffic_by_weekday.csv")
    df_segments = pd.read_csv(DATA_DIR / "segment_performance.csv")
    df_segment_behavior = pd.read_csv(DATA_DIR / "segment_behavior_comparison.csv")
except FileNotFoundError:
    df_daily = None
    df_weekly = None
    df_weekday = None
    df_segments = None
    df_segment_behavior = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-users me-3"),
                    "Trafic & Utilisateurs"
                ], className="mb-3"),
                html.P(
                    "Analyse détaillée du trafic quotidien, hebdomadaire et segmentation des utilisateurs "
                    "pour optimiser l'engagement et les conversions.",
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
                        html.I(className="fas fa-user-friends fa-2x text-primary mb-2"),
                        html.H4("1.65M", className="mb-1"),
                        html.P("Utilisateurs Total", className="text-muted mb-0 small"),
                        html.Small("Mai-Sept 2015", className="text-primary"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-success mb-2"),
                        html.H4("11,866", className="mb-1"),
                        html.P("Users/Jour (Moy.)", className="text-muted mb-0 small"),
                        html.Small("139 jours", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-calendar-week fa-2x text-warning mb-2"),
                        html.H4("Mardi", className="mb-1"),
                        html.P("Jour le Plus Fort", className="text-muted mb-0 small"),
                        html.Small("13,226 users/jour", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-crown fa-2x text-danger mb-2"),
                        html.H4("1.78%", className="mb-1"),
                        html.P("Premium Users", className="text-muted mb-0 small"),
                        html.Small("29% du revenue", className="text-danger"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Daily Traffic Evolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-area me-2"),
                        "Évolution du Trafic Quotidien"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='daily-traffic', config={'displayModeBar': True})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Sessions and Events
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-mouse-pointer me-2"),
                        "Sessions & Événements"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sessions-events', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-day me-2"),
                        "Trafic par Jour de la Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekday-traffic', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # User Segmentation
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-user-tag me-2"),
                        "Segmentation des Utilisateurs"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='user-segments', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-euro-sign me-2"),
                        "Revenue par Segment"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='segment-revenue', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Weekly Growth
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-line me-2"),
                        "Croissance Hebdomadaire"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekly-growth', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Engagement Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-heartbeat me-2"),
                        "Engagement: Événements par Utilisateur"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='engagement-metrics', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-user-clock me-2"),
                        "Distribution Segments"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='segment-distribution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=4),
    ]),
    
    # Weekend vs Weekday
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-alt me-2"),
                        "Weekend vs Semaine"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekend-comparison', config={'displayModeBar': False})
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
                    "Insights Clés sur le Trafic"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li([
                        html.Strong("Pic de trafic en milieu de semaine : "),
                        "Mardi (13,226 users) et Mercredi (13,126 users) sont les jours les plus actifs"
                    ]),
                    html.Li([
                        html.Strong("Segmentation efficace : "),
                        "1.78% d'utilisateurs Premium génèrent 29% du revenue (Value Index: 16.38x)"
                    ]),
                    html.Li([
                        html.Strong("Engagement moyen : "),
                        "1.69 événements par utilisateur, stable sur toute la période"
                    ]),
                    html.Li([
                        html.Strong("Weekend effect : "),
                        "Baisse de ~30% du trafic le weekend (8,000-9,000 users/jour)"
                    ]),
                    html.Li([
                        html.Strong("Opportunité Occasional : "),
                        "42.3% des users génèrent 30.8% du revenue - potentiel d'upgrade vers Regular"
                    ]),
                ], className="mb-0")
            ], color="info", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('daily-traffic', 'figure'),
    Input('daily-traffic', 'id')
)
def update_daily_traffic(_):
    """Create daily traffic evolution chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Daily users
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['unique_users'],
        mode='lines',
        name='Users Quotidiens',
        line=dict(color='#3498db', width=1),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)',
    ))
    
    # 7-day moving average
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['ma7_users'],
        mode='lines',
        name='Moyenne Mobile 7j',
        line=dict(color='#e74c3c', width=3),
    ))
    
    # Mark weekends
    weekend_data = df_daily[df_daily['is_weekend'] == True]
    fig.add_trace(go.Scatter(
        x=weekend_data['date'],
        y=weekend_data['unique_users'],
        mode='markers',
        name='Weekend',
        marker=dict(color='#f39c12', size=6, symbol='diamond'),
    ))
    
    fig.update_layout(
        title="Trafic Quotidien avec Moyenne Mobile 7 Jours",
        xaxis_title="Date",
        yaxis_title="Utilisateurs Uniques",
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
    Output('sessions-events', 'figure'),
    Input('sessions-events', 'id')
)
def update_sessions_events(_):
    """Create sessions and events chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Sessions
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['unique_sessions'],
        mode='lines',
        name='Sessions',
        line=dict(color='#2ecc71', width=2),
        yaxis='y'
    ))
    
    # Events
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['total_events'],
        mode='lines',
        name='Événements',
        line=dict(color='#9b59b6', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Sessions et Événements Quotidiens",
        xaxis_title="Date",
        yaxis=dict(title="Sessions", side='left'),
        yaxis2=dict(title="Événements", overlaying='y', side='right'),
        template='plotly_dark',
        height=400,
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
    Output('weekday-traffic', 'figure'),
    Input('weekday-traffic', 'id')
)
def update_weekday_traffic(_):
    """Create weekday traffic chart"""
    if df_weekday is None:
        return go.Figure()
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_sorted = df_weekday.set_index('day_of_week').loc[days_order].reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_sorted['day_of_week'],
        y=df_sorted['unique_users_mean'],
        marker=dict(
            color=df_sorted['unique_users_mean'],
            colorscale='Blues',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        error_y=dict(
            type='data',
            array=df_sorted['unique_users_std'],
            visible=True
        ),
        text=[f"{val:,.0f}" for val in df_sorted['unique_users_mean']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Moyenne: %{y:,.0f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Trafic Moyen par Jour de la Semaine",
        xaxis_title="Jour",
        yaxis_title="Utilisateurs Moyens",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('user-segments', 'figure'),
    Input('user-segments', 'id')
)
def update_user_segments(_):
    """Create user segments comparison"""
    if df_segment_behavior is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Users bars
    fig.add_trace(go.Bar(
        name='Utilisateurs',
        x=df_segment_behavior['segment'],
        y=df_segment_behavior['num_users'],
        marker_color='#3498db',
        yaxis='y',
        text=[f"{val:,}" for val in df_segment_behavior['num_users']],
        textposition='outside',
    ))
    
    # Transactions per user line
    fig.add_trace(go.Scatter(
        name='Transactions/User',
        x=df_segment_behavior['segment'],
        y=df_segment_behavior['transactions_per_user'],
        mode='lines+markers',
        marker=dict(size=12, color='#e74c3c'),
        line=dict(width=3, color='#e74c3c'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Segments: Nombre d'Utilisateurs et Transactions/User",
        xaxis_title="Segment",
        yaxis=dict(title="Nombre d'Utilisateurs", side='left'),
        yaxis2=dict(title="Transactions/User", overlaying='y', side='right'),
        template='plotly_dark',
        height=450,
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
    Output('segment-revenue', 'figure'),
    Input('segment-revenue', 'id')
)
def update_segment_revenue(_):
    """Create segment revenue chart"""
    if df_segment_behavior is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Revenue bars
    fig.add_trace(go.Bar(
        x=df_segment_behavior['segment'],
        y=df_segment_behavior['total_revenue'],
        marker=dict(
            color=df_segment_behavior['value_index'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Value<br>Index"),
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"€{val/1000:.0f}K" for val in df_segment_behavior['total_revenue']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Revenue: €%{y:,.0f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Revenue Total par Segment",
        xaxis_title="Segment",
        yaxis_title="Revenue (€)",
        template='plotly_dark',
        height=450,
        showlegend=False
    )
    
    return fig


@callback(
    Output('weekly-growth', 'figure'),
    Input('weekly-growth', 'id')
)
def update_weekly_growth(_):
    """Create weekly growth chart"""
    if df_weekly is None:
        return go.Figure()
    
    # Skip first week (no growth data)
    df_growth = df_weekly[df_weekly['users_growth_pct'].notna()].copy()
    
    fig = go.Figure()
    
    # Users growth
    fig.add_trace(go.Scatter(
        x=df_growth['week_start'],
        y=df_growth['users_growth_pct'],
        mode='lines+markers',
        name='Croissance Users',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)',
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Croissance Hebdomadaire des Utilisateurs",
        xaxis_title="Semaine",
        yaxis_title="Croissance (%)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('engagement-metrics', 'figure'),
    Input('engagement-metrics', 'id')
)
def update_engagement_metrics(_):
    """Create engagement metrics chart"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Events per user
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['events_per_user'],
        mode='lines',
        name='Events/User',
        line=dict(color='#9b59b6', width=2),
    ))
    
    # Add average line
    avg_engagement = df_daily['events_per_user'].mean()
    fig.add_hline(y=avg_engagement, line_dash="dash", line_color="orange",
                  annotation_text=f"Moyenne: {avg_engagement:.2f}")
    
    fig.update_layout(
        title="Engagement Quotidien (Événements par Utilisateur)",
        xaxis_title="Date",
        yaxis_title="Événements/User",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('segment-distribution', 'figure'),
    Input('segment-distribution', 'id')
)
def update_segment_distribution(_):
    """Create segment distribution pie chart"""
    if df_segment_behavior is None:
        return go.Figure()
    
    colors = {'Premium': '#e74c3c', 'Regular': '#3498db', 'Occasional': '#f39c12', 'New': '#95a5a6'}
    
    fig = go.Figure(data=[go.Pie(
        labels=df_segment_behavior['segment'],
        values=df_segment_behavior['num_users'],
        marker=dict(colors=[colors.get(s, '#95a5a6') for s in df_segment_behavior['segment']]),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>' +
                      'Users: %{value:,}<br>' +
                      'Part: %{percent}<br>' +
                      '<extra></extra>'
    )])
    
    fig.update_layout(
        title="Distribution des Segments",
        template='plotly_dark',
        height=400,
        showlegend=True
    )
    
    return fig


@callback(
    Output('weekend-comparison', 'figure'),
    Input('weekend-comparison', 'id')
)
def update_weekend_comparison(_):
    """Create weekend vs weekday comparison"""
    if df_daily is None:
        return go.Figure()
    
    # Aggregate by weekend flag
    weekend_stats = df_daily.groupby('is_weekend').agg({
        'unique_users': 'mean',
        'unique_sessions': 'mean',
        'total_events': 'mean',
        'transactions': 'mean',
        'conversion_rate': 'mean'
    }).reset_index()
    
    weekend_stats['period'] = weekend_stats['is_weekend'].map({True: 'Weekend', False: 'Semaine'})
    
    fig = go.Figure()
    
    # Users
    fig.add_trace(go.Bar(
        name='Users',
        x=weekend_stats['period'],
        y=weekend_stats['unique_users'],
        marker_color='#3498db',
        text=[f"{val:,.0f}" for val in weekend_stats['unique_users']],
        textposition='outside',
    ))
    
    # Sessions
    fig.add_trace(go.Bar(
        name='Sessions',
        x=weekend_stats['period'],
        y=weekend_stats['unique_sessions'],
        marker_color='#2ecc71',
        text=[f"{val:,.0f}" for val in weekend_stats['unique_sessions']],
        textposition='outside',
    ))
    
    # Events
    fig.add_trace(go.Bar(
        name='Events',
        x=weekend_stats['period'],
        y=weekend_stats['total_events'],
        marker_color='#9b59b6',
        text=[f"{val:,.0f}" for val in weekend_stats['total_events']],
        textposition='outside',
    ))
    
    fig.update_layout(
        title="Comparaison Weekend vs Semaine (Moyennes)",
        xaxis_title="Période",
        yaxis_title="Volume",
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
