"""
E-Commerce A/B Test Dashboard - Cohorts & Retention Page
Issue #24: Cohort Analysis and Retention Metrics
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Register page
dash.register_page(__name__, path='/cohorts', name='Cohorts & Rétention')

# Load data
import os

# Get the correct path relative to the dashboard directory
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(os.path.dirname(base_path), 'data', 'clean')

try:
    df_daily = pd.read_csv(os.path.join(data_path, 'daily_metrics.csv'))
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    
    df_traffic = pd.read_csv(os.path.join(data_path, 'traffic_daily.csv'))
    df_traffic['date'] = pd.to_datetime(df_traffic['date'])
    
    df_conversion = pd.read_csv(os.path.join(data_path, 'conversion_daily.csv'))
    df_conversion['date'] = pd.to_datetime(df_conversion['date'])
    
    print(f"✓ Données chargées: {len(df_daily)} jours, {df_daily['unique_users'].sum():,} utilisateurs")
except FileNotFoundError as e:
    print(f"✗ Erreur chargement données: {e}")
    df_daily = None
    df_traffic = None
    df_conversion = None
except Exception as e:
    print(f"✗ Erreur: {e}")
    df_daily = None
    df_traffic = None
    df_conversion = None

# Create cohort analysis data
def create_cohort_data(df):
    """Create cohort analysis from daily data"""
    if df is None or len(df) == 0:
        return None
    
    # Group by week for cohort analysis
    df = df.copy()
    df['week'] = df['date'].dt.to_period('W').apply(lambda x: x.start_time)
    
    weekly_data = df.groupby('week').agg({
        'unique_users': 'sum',
        'unique_sessions': 'sum',
        'transactions': 'sum'
    }).reset_index()
    
    # Calculate retention rates (simplified version)
    cohorts = []
    for i, row in weekly_data.iterrows():
        cohort_week = row['week']
        cohort_size = row['unique_users']
        
        for j in range(len(weekly_data) - i):
            week_offset = j
            if i + j < len(weekly_data):
                retained_users = weekly_data.iloc[i + j]['unique_users']
                retention_rate = (retained_users / cohort_size * 100) if cohort_size > 0 else 0
                
                cohorts.append({
                    'cohort_week': cohort_week,
                    'week_number': week_offset,
                    'retention_rate': retention_rate,
                    'cohort_size': cohort_size,
                    'retained_users': retained_users
                })
    
    return pd.DataFrame(cohorts)

cohort_df = create_cohort_data(df_daily) if df_daily is not None else None

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-layer-group me-3"),
                    "Analyse de Cohortes & Rétention"
                ], className="mb-2"),
                html.P(
                    "Analyse de la rétention des utilisateurs par cohortes et périodes",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x text-primary mb-2"),
                        html.H3(id='cohort-total-users', className="mb-0"),
                        html.P("Utilisateurs Total", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-redo fa-2x text-success mb-2"),
                        html.H3(id='cohort-avg-retention', className="mb-0"),
                        html.P("Rétention Moyenne", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-calendar-week fa-2x text-info mb-2"),
                        html.H3(id='cohort-total-weeks', className="mb-0"),
                        html.P("Semaines Analysées", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-warning mb-2"),
                        html.H3(id='cohort-retention-week1', className="mb-0"),
                        html.P("Rétention Semaine 1", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
    ]),
    
    # Cohort Heatmap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-th me-2"),
                    "Heatmap de Rétention par Cohorte"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='cohort-heatmap', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Retention Curves
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-area me-2"),
                    "Courbes de Rétention par Cohorte"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='retention-curves', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-percentage me-2"),
                    "Taux de Rétention Moyen par Semaine"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='avg-retention-week', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Cohort Size Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-users-cog me-2"),
                    "Taille des Cohortes"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='cohort-size-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-funnel-dollar me-2"),
                    "Rétention vs Conversion"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='retention-conversion-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Weekly Retention Trends
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-calendar-alt me-2"),
                    "Tendances de Rétention Hebdomadaire"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='weekly-retention-trend', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Retention Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Distribution de Rétention"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='retention-distribution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-layer-group me-2"),
                    "Comparaison Cohortes Précoces vs Tardives"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='early-late-cohorts', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
], fluid=True)


# Callbacks
@callback(
    [Output('cohort-total-users', 'children'),
     Output('cohort-avg-retention', 'children'),
     Output('cohort-total-weeks', 'children'),
     Output('cohort-retention-week1', 'children')],
    Input('cohort-heatmap', 'id')
)
def update_kpis(_):
    """Update KPI cards"""
    if cohort_df is None or df_daily is None:
        return "N/A", "N/A", "N/A", "N/A"
    
    total_users = df_daily['unique_users'].sum()
    avg_retention = cohort_df[cohort_df['week_number'] > 0]['retention_rate'].mean()
    total_weeks = cohort_df['cohort_week'].nunique()
    week1_retention = cohort_df[cohort_df['week_number'] == 1]['retention_rate'].mean()
    
    return (
        f"{total_users:,.0f}",
        f"{avg_retention:.1f}%",
        f"{total_weeks}",
        f"{week1_retention:.1f}%"
    )


@callback(
    Output('cohort-heatmap', 'figure'),
    Input('cohort-heatmap', 'id')
)
def update_cohort_heatmap(_):
    """Create cohort retention heatmap"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Pivot data for heatmap
    pivot_data = cohort_df.pivot(
        index='cohort_week',
        columns='week_number',
        values='retention_rate'
    )
    
    # Format dates for display
    pivot_data.index = pivot_data.index.strftime('%Y-%m-%d')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=[f"Semaine {i}" for i in pivot_data.columns],
        y=pivot_data.index,
        colorscale='RdYlGn',
        text=np.round(pivot_data.values, 1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Rétention (%)")
    ))
    
    fig.update_layout(
        title="Taux de Rétention par Cohorte (%)",
        xaxis_title="Semaines depuis la création de la cohorte",
        yaxis_title="Date de Cohorte",
        template='plotly_dark',
        height=500
    )
    
    return fig


@callback(
    Output('retention-curves', 'figure'),
    Input('retention-curves', 'id')
)
def update_retention_curves(_):
    """Create retention curves by cohort"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # Plot each cohort
    for cohort in cohort_df['cohort_week'].unique()[:10]:  # Limit to 10 cohorts for readability
        cohort_data = cohort_df[cohort_df['cohort_week'] == cohort]
        
        fig.add_trace(go.Scatter(
            x=cohort_data['week_number'],
            y=cohort_data['retention_rate'],
            mode='lines+markers',
            name=cohort.strftime('%Y-%m-%d'),
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Courbes de Rétention par Cohorte",
        xaxis_title="Semaines",
        yaxis_title="Taux de Rétention (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15
        )
    )
    
    return fig


@callback(
    Output('avg-retention-week', 'figure'),
    Input('avg-retention-week', 'id')
)
def update_avg_retention(_):
    """Average retention by week number"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    avg_by_week = cohort_df.groupby('week_number')['retention_rate'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=avg_by_week['week_number'],
        y=avg_by_week['retention_rate'],
        marker_color='rgba(102, 126, 234, 0.7)',
        text=avg_by_week['retention_rate'].round(1),
        texttemplate='%{text}%',
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Rétention Moyenne par Semaine",
        xaxis_title="Semaine",
        yaxis_title="Rétention Moyenne (%)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('cohort-size-chart', 'figure'),
    Input('cohort-size-chart', 'id')
)
def update_cohort_size(_):
    """Cohort size evolution"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Get unique cohort sizes
    cohort_sizes = cohort_df[cohort_df['week_number'] == 0][['cohort_week', 'cohort_size']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cohort_sizes['cohort_week'].dt.strftime('%Y-%m-%d'),
        y=cohort_sizes['cohort_size'],
        marker_color='rgba(46, 204, 113, 0.7)',
        text=cohort_sizes['cohort_size'],
        texttemplate='%{text:,.0f}',
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Taille de Chaque Cohorte",
        xaxis_title="Date de Cohorte",
        yaxis_title="Nombre d'Utilisateurs",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('retention-conversion-chart', 'figure'),
    Input('retention-conversion-chart', 'id')
)
def update_retention_conversion(_):
    """Retention vs conversion analysis"""
    if cohort_df is None or df_daily is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Calculate weekly conversion rates
    df_weekly = df_daily.copy()
    df_weekly['week'] = df_weekly['date'].dt.to_period('W').apply(lambda x: x.start_time)
    weekly_conv = df_weekly.groupby('week').agg({
        'view_to_purchase_rate': 'mean',
        'unique_users': 'sum'
    }).reset_index()
    
    # Get week 1 retention for each cohort
    week1_retention = cohort_df[cohort_df['week_number'] == 1].groupby('cohort_week')['retention_rate'].mean().reset_index()
    week1_retention.columns = ['week', 'retention_rate']
    
    # Merge
    merged = pd.merge(weekly_conv, week1_retention, on='week', how='inner')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=merged['retention_rate'],
        y=merged['view_to_purchase_rate'],
        mode='markers',
        marker=dict(
            size=merged['unique_users'] / 100,
            color=merged['unique_users'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Utilisateurs")
        ),
        text=merged['week'].dt.strftime('%Y-%m-%d'),
        hovertemplate='<b>%{text}</b><br>Rétention: %{x:.1f}%<br>Conversion: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Corrélation Rétention vs Conversion",
        xaxis_title="Taux de Rétention Semaine 1 (%)",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('weekly-retention-trend', 'figure'),
    Input('weekly-retention-trend', 'id')
)
def update_weekly_trend(_):
    """Weekly retention trends"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    # Week 1, 2, 3, 4 retention trends
    for week_num in [1, 2, 3, 4]:
        week_data = cohort_df[cohort_df['week_number'] == week_num]
        
        fig.add_trace(go.Scatter(
            x=week_data['cohort_week'].dt.strftime('%Y-%m-%d'),
            y=week_data['retention_rate'],
            mode='lines+markers',
            name=f'Semaine {week_num}',
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Évolution de la Rétention par Semaine",
        xaxis_title="Date de Cohorte",
        yaxis_title="Taux de Rétention (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        showlegend=True
    )
    
    return fig


@callback(
    Output('retention-distribution', 'figure'),
    Input('retention-distribution', 'id')
)
def update_retention_distribution(_):
    """Distribution of retention rates"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Filter out week 0 (100% retention)
    data = cohort_df[cohort_df['week_number'] > 0]['retention_rate']
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=30,
        marker_color='rgba(102, 126, 234, 0.7)',
        name='Distribution'
    ))
    
    fig.update_layout(
        title="Distribution des Taux de Rétention",
        xaxis_title="Taux de Rétention (%)",
        yaxis_title="Fréquence",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('early-late-cohorts', 'figure'),
    Input('early-late-cohorts', 'id')
)
def update_early_late_comparison(_):
    """Compare early vs late cohorts"""
    if cohort_df is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Split cohorts into early and late
    unique_cohorts = sorted(cohort_df['cohort_week'].unique())
    mid_point = len(unique_cohorts) // 2
    
    early_cohorts = unique_cohorts[:mid_point]
    late_cohorts = unique_cohorts[mid_point:]
    
    early_data = cohort_df[cohort_df['cohort_week'].isin(early_cohorts)].groupby('week_number')['retention_rate'].mean()
    late_data = cohort_df[cohort_df['cohort_week'].isin(late_cohorts)].groupby('week_number')['retention_rate'].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=early_data.index,
        y=early_data.values,
        mode='lines+markers',
        name='Cohortes Précoces',
        line=dict(width=3, color='#667eea'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=late_data.index,
        y=late_data.values,
        mode='lines+markers',
        name='Cohortes Tardives',
        line=dict(width=3, color='#2ecc71'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Comparaison Cohortes Précoces vs Tardives",
        xaxis_title="Semaines",
        yaxis_title="Rétention Moyenne (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        showlegend=True
    )
    
    return fig
