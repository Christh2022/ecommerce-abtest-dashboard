"""
A/B Testing Results Page - Test Results and Statistical Analysis
Issue #23 - A/B Test Results + Stats
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
dash.register_page(__name__, path='/ab-testing/results', name='Résultats A/B Tests')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

try:
    df_summary = pd.read_csv(DATA_DIR / "ab_test_summary_by_scenario.csv")
    df_simulation = pd.read_csv(DATA_DIR / "ab_test_simulation_results.csv")
    df_conversion = pd.read_csv(DATA_DIR / "ab_test_conversion_tests_summary.csv")
    df_business = pd.read_csv(DATA_DIR / "ab_test_business_impact.csv")
    df_daily = pd.read_csv(DATA_DIR / "ab_test_daily_aggregate.csv")
except FileNotFoundError:
    df_summary = None
    df_simulation = None
    df_conversion = None
    df_business = None
    df_daily = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-flask me-3"),
                    "Résultats des Tests A/B"
                ], className="mb-3"),
                html.P(
                    "Analyse statistique complète des 8 scénarios de tests A/B avec métriques de conversion, "
                    "significance testing, et impact business.",
                    className="lead text-muted"
                ),
            ], className="mb-4")
        ])
    ]),
    
    # Summary Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-check-circle fa-2x text-success mb-2"),
                        html.H4("8/8", className="mb-1"),
                        html.P("Tests Réussis", className="text-muted mb-0 small"),
                        html.Small("100% gagnants", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-primary mb-2"),
                        html.H4("+35.7%", className="mb-1"),
                        html.P("Lift Moyen", className="text-muted mb-0 small"),
                        html.Small("Conversion globale", className="text-primary"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-percentage fa-2x text-info mb-2"),
                        html.H4("95%", className="mb-1"),
                        html.P("Confiance Stats", className="text-muted mb-0 small"),
                        html.Small("Tous tests", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-euro-sign fa-2x text-warning mb-2"),
                        html.H4("€2.24M", className="mb-1"),
                        html.P("Revenue Lift Total", className="text-muted mb-0 small"),
                        html.Small("30 jours", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Test Results Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-trophy me-2"),
                        "Classement des Scénarios par Performance"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='scenarios-ranking', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Statistical Power and Confidence
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Puissance Statistique par Scénario"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='statistical-power', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-percentage me-2"),
                        "Distribution des P-Values"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='pvalue-distribution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Conversion Rates Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-exchange-alt me-2"),
                        "Control vs Variant: Taux de Conversion"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='control-vs-variant', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Daily Performance Evolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-calendar-alt me-2"),
                        "Évolution Quotidienne du Revenue Lift"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='daily-revenue-lift', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-bullseye me-2"),
                        "Significance Timeline"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='significance-timeline', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=4),
    ]),
    
    # ROI Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-money-bill-wave me-2"),
                        "ROI et Impact Business (30 jours)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='roi-analysis', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Detailed Results Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-table me-2"),
                        "Résultats Détaillés par Scénario"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='results-table')
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Key Insights
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H6([
                    html.I(className="fas fa-lightbulb me-2"),
                    "Insights Clés des Tests A/B"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li([
                        html.Strong("100% de réussite : "),
                        "Les 8 scénarios ont produit des variants gagnants avec 95% de confiance statistique"
                    ]),
                    html.Li([
                        html.Strong("Meilleur performer : "),
                        "Système Reviews Clients (S2) avec +42.6% de lift et ROI de 1,697%"
                    ]),
                    html.Li([
                        html.Strong("Puissance statistique élevée : "),
                        "Moyenne de 78% de statistical power sur 10,000 simulations"
                    ]),
                    html.Li([
                        html.Strong("Impact revenue annuel projeté : "),
                        "€22.4M avec implémentation séquentielle des 8 scénarios"
                    ]),
                    html.Li([
                        html.Strong("Quick wins : "),
                        "4 scénarios HIGH priority avec ROI >500% et coût <€30K"
                    ]),
                ], className="mb-0")
            ], color="success", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('scenarios-ranking', 'figure'),
    Input('scenarios-ranking', 'id')
)
def update_scenarios_ranking(_):
    """Create scenarios ranking chart"""
    if df_summary is None:
        return go.Figure()
    
    # Sort by ROI
    df_sorted = df_summary.sort_values('roi_30d_pct', ascending=True)
    
    # Color by priority
    colors = {'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#3498db'}
    bar_colors = [colors.get(p, '#95a5a6') for p in df_sorted['priority']]
    
    fig = go.Figure()
    
    # ROI bars
    fig.add_trace(go.Bar(
        y=df_sorted['scenario_name'],
        x=df_sorted['roi_30d_pct'],
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"{val:.0f}%" for val in df_sorted['roi_30d_pct']],
        textposition='outside',
        name='ROI 30j',
        hovertemplate='<b>%{y}</b><br>' +
                      'ROI: %{x:.1f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="ROI 30 Jours par Scénario",
        xaxis_title="ROI (%)",
        yaxis_title="",
        template='plotly_dark',
        height=500,
        showlegend=False
    )
    
    return fig


@callback(
    Output('statistical-power', 'figure'),
    Input('statistical-power', 'id')
)
def update_statistical_power(_):
    """Create statistical power chart"""
    if df_simulation is None:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_simulation['scenario_name'],
        y=df_simulation['statistical_power'] * 100,
        marker=dict(
            color=df_simulation['statistical_power'] * 100,
            colorscale='Greens',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"{val*100:.1f}%" for val in df_simulation['statistical_power']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Power: %{y:.1f}%<br>' +
                      '<extra></extra>'
    ))
    
    # Add 80% threshold line
    fig.add_hline(y=80, line_dash="dash", line_color="orange", 
                  annotation_text="Seuil recommandé 80%")
    
    fig.update_layout(
        title="Puissance Statistique (10,000 simulations)",
        xaxis_title="Scénario",
        yaxis_title="Statistical Power (%)",
        template='plotly_dark',
        height=400,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


@callback(
    Output('pvalue-distribution', 'figure'),
    Input('pvalue-distribution', 'id')
)
def update_pvalue_distribution(_):
    """Create p-value distribution chart"""
    if df_conversion is None:
        return go.Figure()
    
    # Use log scale for p-values (they're very small)
    df_conversion['log_pvalue'] = -np.log10(df_conversion['p_value_chi2'].clip(lower=1e-300))
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_conversion['scenario_name'],
        y=df_conversion['log_pvalue'],
        marker=dict(
            color='#2ecc71',
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"p<{val:.2e}" for val in df_conversion['p_value_chi2']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'P-value: %{text}<br>' +
                      '<extra></extra>'
    ))
    
    # Add significance threshold (p=0.05 -> -log10(0.05) = 1.3)
    fig.add_hline(y=1.3, line_dash="dash", line_color="red", 
                  annotation_text="Seuil α=0.05")
    
    fig.update_layout(
        title="Significance Testing (Chi-Square)",
        xaxis_title="Scénario",
        yaxis_title="-log10(p-value)",
        template='plotly_dark',
        height=400,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


@callback(
    Output('control-vs-variant', 'figure'),
    Input('control-vs-variant', 'id')
)
def update_control_vs_variant(_):
    """Create control vs variant comparison"""
    if df_conversion is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Control rates
    fig.add_trace(go.Bar(
        name='Control',
        x=df_conversion['scenario_name'],
        y=df_conversion['control_rate'] * 100,
        marker_color='#95a5a6',
        text=[f"{val*100:.2f}%" for val in df_conversion['control_rate']],
        textposition='inside',
    ))
    
    # Variant rates
    fig.add_trace(go.Bar(
        name='Variant',
        x=df_conversion['scenario_name'],
        y=df_conversion['variant_rate'] * 100,
        marker_color='#3498db',
        text=[f"{val*100:.2f}%" for val in df_conversion['variant_rate']],
        textposition='inside',
    ))
    
    fig.update_layout(
        title="Control vs Variant: Taux de Conversion View→Cart",
        xaxis_title="Scénario",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        barmode='group',
        height=450,
        xaxis=dict(tickangle=-45),
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
    Output('daily-revenue-lift', 'figure'),
    Input('daily-revenue-lift', 'id')
)
def update_daily_revenue_lift(_):
    """Create daily revenue lift evolution"""
    if df_daily is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Revenue lift bars
    fig.add_trace(go.Bar(
        x=df_daily['day_number'],
        y=df_daily['revenue_lift'],
        marker=dict(
            color=df_daily['revenue_lift'],
            colorscale='Blues',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        name='Revenue Lift',
        hovertemplate='<b>Jour %{x}</b><br>' +
                      'Lift: €%{y:,.0f}<br>' +
                      '<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(df_daily['day_number'], df_daily['revenue_lift'], 2)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=df_daily['day_number'],
        y=p(df_daily['day_number']),
        mode='lines',
        name='Tendance',
        line=dict(color='#e74c3c', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title="Évolution du Revenue Lift Quotidien (Tous Scénarios)",
        xaxis_title="Jour",
        yaxis_title="Revenue Lift (€)",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig


@callback(
    Output('significance-timeline', 'figure'),
    Input('significance-timeline', 'id')
)
def update_significance_timeline(_):
    """Create significance achievement timeline"""
    if df_daily is None:
        return go.Figure()
    
    # Count significant tests per day
    sig_by_day = df_daily.groupby('day_number')['is_significant'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sig_by_day['day_number'],
        y=sig_by_day['is_significant'],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8, color='#2ecc71'),
        hovertemplate='<b>Jour %{x}</b><br>' +
                      'Tests significatifs: %{y}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Tests Significatifs par Jour",
        xaxis_title="Jour",
        yaxis_title="Nombre de Tests",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('roi-analysis', 'figure'),
    Input('roi-analysis', 'id')
)
def update_roi_analysis(_):
    """Create ROI analysis chart"""
    if df_business is None:
        return go.Figure()
    
    fig = go.Figure()
    
    # Annual ROI
    fig.add_trace(go.Scatter(
        x=df_business['implementation_cost'],
        y=df_business['annual_roi'],
        mode='markers+text',
        marker=dict(
            size=df_business['annual_additional_revenue'] / 50000,  # Size by revenue
            color=df_business['confidence_level'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Statistical<br>Power"),
            line=dict(color='white', width=1)
        ),
        text=df_business['scenario_id'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>' +
                      'Coût: €%{x:,.0f}<br>' +
                      'ROI Annuel: %{y:.0f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Matrice ROI Annuel vs Coût d'Implémentation",
        xaxis_title="Coût d'Implémentation (€)",
        yaxis_title="ROI Annuel (%)",
        template='plotly_dark',
        height=450
    )
    
    return fig


@callback(
    Output('results-table', 'children'),
    Input('results-table', 'id')
)
def update_results_table(_):
    """Create detailed results table"""
    if df_summary is None or df_conversion is None:
        return html.P("Données non disponibles")
    
    # Merge data
    df_merged = df_summary.merge(
        df_conversion[['scenario_id', 'control_rate', 'variant_rate', 'p_value_chi2', 'statistical_power']],
        on='scenario_id',
        how='left'
    )
    
    # Create table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Scénario"),
            html.Th("Priority"),
            html.Th("Control"),
            html.Th("Variant"),
            html.Th("Lift %"),
            html.Th("P-Value"),
            html.Th("Power"),
            html.Th("Revenue 30j"),
            html.Th("ROI 30j"),
        ]))
    ]
    
    table_body = [html.Tbody([
        html.Tr([
            html.Td([
                html.Strong(row['scenario_id']),
                html.Br(),
                html.Small(row['scenario_name'], className="text-muted")
            ]),
            html.Td(html.Span(row['priority'], 
                   className=f"badge bg-{'danger' if row['priority']=='HIGH' else 'warning' if row['priority']=='MEDIUM' else 'info'}")),
            html.Td(f"{row['control_rate']*100:.2f}%"),
            html.Td(f"{row['variant_rate']*100:.2f}%"),
            html.Td(html.Span(f"+{row['avg_lift_view_to_cart_pct']:.1f}%", className="text-success")),
            html.Td(f"{row['p_value_chi2']:.2e}"),
            html.Td(f"{row['statistical_power']*100:.1f}%"),
            html.Td(f"€{row['total_revenue_lift_30d']:,.0f}"),
            html.Td(html.Strong(f"{row['roi_30d_pct']:.0f}%", className="text-warning")),
        ]) for idx, row in df_merged.iterrows()
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
