"""
E-Commerce A/B Test Dashboard - A/B Test Simulations Page
Simulation et prédiction des tests A/B
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

# Register page
dash.register_page(__name__, path='/ab-testing/simulations', name='Simulations A/B')

# Load data
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(os.path.dirname(base_path), 'data', 'clean')

try:
    df_simulation = pd.read_csv(os.path.join(data_path, 'ab_test_simulation.csv'))
    df_simulation['date'] = pd.to_datetime(df_simulation['date'])
    
    df_results = pd.read_csv(os.path.join(data_path, 'ab_test_simulation_results.csv'))
    
    print(f"[OK] Simulations chargees: {len(df_simulation)} lignes, {df_simulation['scenario_id'].nunique()} scenarios")
except Exception as e:
    print(f"[ERREUR] Chargement simulations: {e}")
    df_simulation = None
    df_results = None

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-flask me-3"),
                    "Simulations de Tests A/B"
                ], className="mb-2"),
                html.P(
                    "Simulation et prédiction des performances des tests A/B sur 30 jours",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # Scenario Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Sélectionner un scénario:", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='scenario-selector',
                        options=[],
                        value=None,
                        clearable=False,
                        className='mb-2',
                        maxHeight=400,
                        style={'zIndex': 9999}
                    ),
                    dcc.Store(id='scenario-store', data=None)
                ], style={'overflow': 'visible'})
            ], className="shadow-sm border-0 mb-4", style={'overflow': 'visible'})
        ])
    ], style={'zIndex': 1000, 'position': 'relative'}),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-success mb-2"),
                        html.H3(id='sim-expected-lift', className="mb-0"),
                        html.P("Lift Attendu", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-bolt fa-2x text-warning mb-2"),
                        html.H3(id='sim-statistical-power', className="mb-0"),
                        html.P("Puissance Statistique", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x text-info mb-2"),
                        html.H3(id='sim-sample-size', className="mb-0"),
                        html.P("Taille Échantillon", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-dollar-sign fa-2x text-danger mb-2"),
                        html.H3(id='sim-implementation-cost', className="mb-0"),
                        html.P("Coût d'Implémentation", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
    ]),
    
    # Simulation Evolution Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-area me-2"),
                    "Évolution des Conversions (30 jours)"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-conversion-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-money-bill-wave me-2"),
                    "Évolution du Revenue (30 jours)"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-revenue-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Lift Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-percentage me-2"),
                    "Lift par Métrique"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-lift-metrics', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-line me-2"),
                    "Revenue Lift Cumulatif"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-cumulative-revenue', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Statistical Significance
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-check-circle me-2"),
                    "Évolution de la Significativité Statistique"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-significance-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-calculator me-2"),
                    "Évolution du Z-Score"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-zscore-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Sample Size Growth
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-users-cog me-2"),
                    "Croissance de la Taille d'Échantillon"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-sample-size-growth', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-balance-scale me-2"),
                    "Comparaison Control vs Variant"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-control-variant-compare', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # All Scenarios Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-layer-group me-2"),
                    "Comparaison de Tous les Scénarios"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sim-all-scenarios', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Scenario Details Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-table me-2"),
                    "Résumé des Scénarios"
                ]),
                dbc.CardBody([
                    html.Div(id='sim-scenarios-table')
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    [Output('scenario-selector', 'options'),
     Output('scenario-selector', 'value')],
    Input('scenario-store', 'data')
)
def populate_scenario_dropdown(_):
    """Populate scenario dropdown with current data - reload from file"""
    try:
        # Reload data from file to get latest scenarios
        df_results_fresh = pd.read_csv(os.path.join(data_path, 'ab_test_simulation_results.csv'))
        
        if df_results_fresh is None or len(df_results_fresh) == 0:
            return [], None
        
        options = [
            {'label': f"{row['scenario_name']} (Priority: {row['priority']})", 
             'value': row['scenario_id']}
            for _, row in df_results_fresh.iterrows()
        ]
        
        default_value = df_results_fresh.iloc[0]['scenario_id']
        
        return options, default_value
    except Exception as e:
        print(f"[ERROR] Loading scenarios: {e}")
        return [], None


@callback(
    [Output('sim-expected-lift', 'children'),
     Output('sim-statistical-power', 'children'),
     Output('sim-sample-size', 'children'),
     Output('sim-implementation-cost', 'children')],
    Input('scenario-selector', 'value')
)
def update_kpis(scenario_id):
    """Update KPI cards"""
    if df_results is None or scenario_id is None:
        return "N/A", "N/A", "N/A", "N/A"
    
    try:
        scenario = df_results[df_results['scenario_id'] == scenario_id].iloc[0]
        
        return (
            f"+{scenario['expected_lift_pct']:.1f}%",
            f"{scenario['statistical_power'] * 100:.1f}%",
            f"{scenario['sample_size_per_group']:,.0f}",
            f"${scenario['implementation_cost']:,.0f}"
        )
    except Exception as e:
        return "Erreur", "Erreur", "Erreur", "Erreur"


@callback(
    Output('sim-conversion-evolution', 'figure'),
    Input('scenario-selector', 'value')
)
def update_conversion_evolution(scenario_id):
    """Conversion evolution over 30 days"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['control_view_to_purchase_pct'],
        mode='lines+markers',
        name='Control',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['variant_view_to_purchase_pct'],
        mode='lines+markers',
        name='Variant',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Taux de Conversion View → Purchase",
        xaxis_title="Jour",
        yaxis_title="Taux de Conversion (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-revenue-evolution', 'figure'),
    Input('scenario-selector', 'value')
)
def update_revenue_evolution(scenario_id):
    """Revenue evolution over time"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['control_revenue'],
        mode='lines',
        name='Control',
        fill='tozeroy',
        line=dict(color='#e74c3c', width=2),
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['variant_revenue'],
        mode='lines',
        name='Variant',
        fill='tozeroy',
        line=dict(color='#2ecc71', width=2),
        fillcolor='rgba(46, 204, 113, 0.1)'
    ))
    
    fig.update_layout(
        title="Revenue Control vs Variant",
        xaxis_title="Jour",
        yaxis_title="Revenue ($)",
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-lift-metrics', 'figure'),
    Input('scenario-selector', 'value')
)
def update_lift_metrics(scenario_id):
    """Lift by metric"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    try:
        scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
        if len(scenario_data) == 0:
            return go.Figure().add_annotation(
                text="Aucune donnée pour ce scénario",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        last_day = scenario_data[scenario_data['day_number'] == scenario_data['day_number'].max()].iloc[0]
        
        metrics = ['View → Cart', 'Cart → Purchase', 'View → Purchase']
        values = [
            last_day['lift_view_to_cart_pct'],
            last_day['lift_cart_to_purchase_pct'],
            last_day['lift_view_to_purchase_pct']
        ]
    except Exception as e:
        return go.Figure().add_annotation(
            text=f"Erreur: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    colors = ['#3498db', '#f39c12', '#2ecc71']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=metrics,
        y=values,
        marker_color=colors,
        text=[f"{v:.2f}%" for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Lift par Métrique (Jour 30)",
        yaxis_title="Lift (%)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('sim-cumulative-revenue', 'figure'),
    Input('scenario-selector', 'value')
)
def update_cumulative_revenue(scenario_id):
    """Cumulative revenue lift"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['cumulative_revenue_lift'],
        mode='lines',
        name='Revenue Lift Cumulatif',
        fill='tozeroy',
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        title="Revenue Lift Cumulatif",
        xaxis_title="Jour",
        yaxis_title="Revenue Lift Cumulatif ($)",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-significance-evolution', 'figure'),
    Input('scenario-selector', 'value')
)
def update_significance_evolution(scenario_id):
    """Statistical significance evolution"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    # P-value evolution
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['p_value'],
        mode='lines+markers',
        name='P-value',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=6)
    ))
    
    # Significance threshold
    fig.add_hline(y=0.05, line_dash="dash", line_color="yellow", 
                  annotation_text="Seuil α = 0.05")
    
    fig.update_layout(
        title="Évolution de la P-Value",
        xaxis_title="Jour",
        yaxis_title="P-Value",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-zscore-evolution', 'figure'),
    Input('scenario-selector', 'value')
)
def update_zscore_evolution(scenario_id):
    """Z-score evolution"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['z_score'],
        mode='lines+markers',
        name='Z-Score',
        line=dict(color='#3498db', width=2),
        marker=dict(size=6)
    ))
    
    # Critical value for 95% confidence
    fig.add_hline(y=1.96, line_dash="dash", line_color="green", 
                  annotation_text="Z = 1.96 (95% confiance)")
    fig.add_hline(y=-1.96, line_dash="dash", line_color="green")
    
    fig.update_layout(
        title="Évolution du Z-Score",
        xaxis_title="Jour",
        yaxis_title="Z-Score",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-sample-size-growth', 'figure'),
    Input('scenario-selector', 'value')
)
def update_sample_size_growth(scenario_id):
    """Sample size growth"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['sample_size_control'],
        mode='lines',
        name='Control',
        stackgroup='one',
        line=dict(color='#e74c3c', width=0),
        fillcolor='rgba(231, 76, 60, 0.5)'
    ))
    
    fig.add_trace(go.Scatter(
        x=scenario_data['day_number'],
        y=scenario_data['sample_size_variant'],
        mode='lines',
        name='Variant',
        stackgroup='one',
        line=dict(color='#2ecc71', width=0),
        fillcolor='rgba(46, 204, 113, 0.5)'
    ))
    
    fig.update_layout(
        title="Croissance de la Taille d'Échantillon",
        xaxis_title="Jour",
        yaxis_title="Nombre d'Utilisateurs",
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('sim-control-variant-compare', 'figure'),
    Input('scenario-selector', 'value')
)
def update_control_variant_compare(scenario_id):
    """Control vs variant comparison"""
    if df_simulation is None or scenario_id is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    try:
        scenario_data = df_simulation[df_simulation['scenario_id'] == scenario_id]
        if len(scenario_data) == 0:
            return go.Figure().add_annotation(
                text="Aucune donnée pour ce scénario",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        last_day = scenario_data[scenario_data['day_number'] == scenario_data['day_number'].max()].iloc[0]
        
        categories = ['Views', 'Carts', 'Purchases', 'Revenue']
        control_values = [
            last_day['control_views'],
            last_day['control_carts'],
            last_day['control_purchases'],
            last_day['control_revenue'] / 100  # Scale down for visibility
        ]
        variant_values = [
            last_day['variant_views'],
            last_day['variant_carts'],
            last_day['variant_purchases'],
            last_day['variant_revenue'] / 100
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Control',
            x=categories,
            y=control_values,
            marker_color='#e74c3c'
        ))
        
        fig.add_trace(go.Bar(
            name='Variant',
            x=categories,
            y=variant_values,
            marker_color='#2ecc71'
        ))
        
        fig.update_layout(
            title="Control vs Variant (Jour 30)",
            yaxis_title="Valeur",
            barmode='group',
            template='plotly_dark',
            height=400
        )
        
        return fig
        
    except Exception as e:
        return go.Figure().add_annotation(
            text=f"Erreur: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )


@callback(
    Output('sim-all-scenarios', 'figure'),
    Input('scenario-selector', 'value')
)
def update_all_scenarios(_):
    """Compare all scenarios"""
    if df_results is None:
        return go.Figure().add_annotation(
            text="Données non disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_results['expected_lift_pct'],
        y=df_results['statistical_power'],
        mode='markers+text',
        marker=dict(
            size=df_results['implementation_cost'] / 1000,
            color=df_results['sample_size_per_group'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sample Size")
        ),
        text=df_results['scenario_name'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Lift: %{x:.1f}%<br>Power: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Comparaison: Lift vs Puissance Statistique (Taille = Coût)",
        xaxis_title="Expected Lift (%)",
        yaxis_title="Statistical Power (%)",
        template='plotly_dark',
        height=500
    )
    
    return fig


@callback(
    Output('sim-scenarios-table', 'children'),
    Input('scenario-selector', 'value')
)
def update_scenarios_table(_):
    """Display scenarios summary table"""
    if df_results is None:
        return html.P("Données non disponibles", className="text-muted")
    
    table_header = [
        html.Thead(html.Tr([
            html.Th("Scénario"),
            html.Th("Priorité"),
            html.Th("Métrique Cible"),
            html.Th("Lift Attendu"),
            html.Th("Puissance"),
            html.Th("Échantillon"),
            html.Th("Coût"),
            html.Th("Durée")
        ]))
    ]
    
    rows = []
    for _, row in df_results.iterrows():
        rows.append(html.Tr([
            html.Td(row['scenario_name']),
            html.Td(html.Span(row['priority'], className=f"badge bg-{'success' if row['priority']=='HIGH' else 'warning'}")),
            html.Td(row['target_metric']),
            html.Td(f"{row['expected_lift_pct']:.1f}%"),
            html.Td(f"{row['statistical_power']:.1f}%"),
            html.Td(f"{row['sample_size_per_group']:,.0f}"),
            html.Td(f"${row['implementation_cost']:,.0f}"),
            html.Td(f"{row['test_duration_weeks']} sem")
        ]))
    
    table_body = [html.Tbody(rows)]
    
    return dbc.Table(table_header + table_body, bordered=True, dark=True, hover=True, responsive=True, striped=True)
