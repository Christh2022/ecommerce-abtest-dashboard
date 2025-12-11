"""
E-Commerce A/B Test Dashboard - A/B Test Visualizations
Visualisations avancées et analyses détaillées des tests A/B
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
import os

# Register page
dash.register_page(__name__, path='/ab-testing/visualizations', name='Visualisations A/B')

# Load data
base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(base_path)), 'data', 'clean')

# Load A/B test data
ab_summary = pd.read_csv(os.path.join(data_path, 'ab_test_conversion_tests_summary.csv'))
ab_daily = pd.read_csv(os.path.join(data_path, 'ab_test_daily_aggregate.csv'))

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-chart-pie me-3"),
                    "Visualisations Avancées des Tests A/B"
                ], className="mb-2"),
                html.P(
                    "Analyses détaillées et visualisations interactives des performances des tests A/B",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # Summary Statistics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-vial fa-2x text-primary mb-2"),
                        html.H3(id='viz-total-tests', className="mb-0"),
                        html.P("Tests A/B Réalisés", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-trophy fa-2x text-success mb-2"),
                        html.H3(id='viz-winning-tests', className="mb-0"),
                        html.P("Tests Gagnants", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-warning mb-2"),
                        html.H3(id='viz-avg-lift', className="mb-0"),
                        html.P("Lift Moyen", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x text-info mb-2"),
                        html.H3(id='viz-total-users', className="mb-0"),
                        html.P("Sample Size Total", className="text-muted mb-0 small")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=3),
    ]),
    
    # Test Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-filter me-2"),
                    "Sélection du Test"
                ]),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='viz-test-selector',
                        options=[{'label': name, 'value': name} for name in sorted(ab_summary['scenario_name'].unique())],
                        value=ab_summary['scenario_name'].iloc[0],
                        clearable=False,
                        className='mb-0'
                    )
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Performance Overview & Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-tachometer-alt me-2"),
                    "Métriques Clés"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-performance-overview', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Comparaison Control vs Variant"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-control-variant-compare', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Daily Evolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-calendar-alt me-2"),
                    "Évolution Quotidienne des Métriques"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-daily-evolution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Revenue Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-dollar-sign me-2"),
                    "Revenue Quotidien"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-revenue-analysis', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-area me-2"),
                    "Revenue Cumulatif"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-cumulative-revenue', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Statistical Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-calculator me-2"),
                    "Analyse Statistique Détaillée"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-statistical-analysis', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-bell-curve me-2"),
                    "Distribution des Conversions"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-conversion-distribution', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Test Comparison Matrix & Lift Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-th me-2"),
                    "Matrice de Comparaison"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-test-matrix', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-rocket me-2"),
                    "Analyse des Lifts"
                ]),
                dbc.CardBody([
                    dcc.Graph(id='viz-lift-analysis', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
], fluid=True)


# Callbacks
@callback(
    [Output('viz-total-tests', 'children'),
     Output('viz-winning-tests', 'children'),
     Output('viz-avg-lift', 'children'),
     Output('viz-total-users', 'children')],
    Input('viz-test-selector', 'value')
)
def update_summary_stats(selected_test):
    """Update summary statistics"""
    total_tests = len(ab_summary)
    winning_tests = len(ab_summary[ab_summary['decision'] == 'WINNER_VARIANT'])
    avg_lift = ab_summary['lift_pct'].mean()
    total_users = ab_daily['sample_size_total'].sum()
    
    return (
        f"{total_tests}",
        f"{winning_tests}",
        f"+{avg_lift:.1f}%",
        f"{total_users:,.0f}"
    )


@callback(
    Output('viz-performance-overview', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_performance_overview(selected_test):
    """Performance overview"""
    test_data = ab_summary[ab_summary['scenario_name'] == selected_test].iloc[0]
    
    metrics = ['Control Rate', 'Variant Rate', 'Lift %', 'Power', 'Confidence']
    values = [
        test_data['control_rate'] * 100,
        test_data['variant_rate'] * 100,
        test_data['lift_pct'],
        test_data['statistical_power'] * 100,
        test_data['prob_b_beats_a'] * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=metrics,
        y=values,
        marker_color=['#e74c3c', '#2ecc71', '#3498db', '#9b59b6', '#f39c12'],
        text=[f'{v:.2f}' if i < 3 else f'{v:.1f}%' for i, v in enumerate(values)],
        textposition='outside'
    ))
    
    fig.update_layout(
        xaxis_title="Métrique",
        yaxis_title="Valeur",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    
    return fig


@callback(
    Output('viz-control-variant-compare', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_control_variant_compare(selected_test):
    """Control vs Variant comparison"""
    test_data = ab_summary[ab_summary['scenario_name'] == selected_test].iloc[0]
    
    metrics = ['Taux de Conversion']
    control = [test_data['control_rate'] * 100]
    variant = [test_data['variant_rate'] * 100]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Control',
        x=metrics,
        y=control,
        marker_color='#e74c3c',
        text=[f'{v:.2f}%' for v in control],
        textposition='outside',
        width=0.3
    ))
    
    fig.add_trace(go.Bar(
        name='Variant',
        x=metrics,
        y=variant,
        marker_color='#2ecc71',
        text=[f'{v:.2f}%' for v in variant],
        textposition='outside',
        width=0.3
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="",
        yaxis_title="Taux (%)",
        template='plotly_dark',
        height=400,
        showlegend=True
    )
    
    return fig


@callback(
    Output('viz-daily-evolution', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_daily_evolution(selected_test):
    """Daily evolution of metrics"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ab_daily['day_number'],
        y=ab_daily['control_purchases'],
        mode='lines+markers',
        name='Control Purchases',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=ab_daily['day_number'],
        y=ab_daily['variant_purchases'],
        mode='lines+markers',
        name='Variant Purchases',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        xaxis_title="Jour",
        yaxis_title="Purchases",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig


@callback(
    Output('viz-revenue-analysis', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_revenue_analysis(selected_test):
    """Revenue analysis"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Control',
        x=ab_daily['day_number'],
        y=ab_daily['control_revenue'],
        marker_color='#e74c3c',
        opacity=0.7
    ))
    
    fig.add_trace(go.Bar(
        name='Variant',
        x=ab_daily['day_number'],
        y=ab_daily['variant_revenue'],
        marker_color='#2ecc71',
        opacity=0.7
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Jour",
        yaxis_title="Revenue ($)",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('viz-cumulative-revenue', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_cumulative_revenue(selected_test):
    """Cumulative revenue"""
    control_cumulative = ab_daily['control_revenue'].cumsum()
    variant_cumulative = ab_daily['variant_revenue'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ab_daily['day_number'],
        y=control_cumulative,
        mode='lines',
        fill='tozeroy',
        name='Control',
        line=dict(color='#e74c3c', width=3),
        fillcolor='rgba(231, 76, 60, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=ab_daily['day_number'],
        y=variant_cumulative,
        mode='lines',
        fill='tozeroy',
        name='Variant',
        line=dict(color='#2ecc71', width=3),
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))
    
    fig.update_layout(
        xaxis_title="Jour",
        yaxis_title="Revenue Cumulatif ($)",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig


@callback(
    Output('viz-statistical-analysis', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_statistical_analysis(selected_test):
    """Statistical analysis visualization"""
    test_data = ab_summary[ab_summary['scenario_name'] == selected_test].iloc[0]
    
    metrics = ['P-Value Chi2', 'Prob B>A', 'Stat Power', 'Lift %']
    values = [
        min(test_data['p_value_chi2'] * 100, 5) if test_data['p_value_chi2'] > 0 else 0.01,
        test_data['prob_b_beats_a'] * 100,
        test_data['statistical_power'] * 100,
        test_data['lift_pct']
    ]
    
    colors = [
        '#2ecc71' if test_data['p_value_chi2'] < 0.05 else '#e74c3c',
        '#2ecc71' if test_data['prob_b_beats_a'] >= 0.95 else '#f39c12',
        '#2ecc71' if test_data['statistical_power'] >= 0.8 else '#f39c12',
        '#2ecc71' if test_data['lift_pct'] > 0 else '#e74c3c'
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=metrics,
        y=values,
        marker_color=colors,
        text=[f'{v:.2f}' for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        xaxis_title="Métrique Statistique",
        yaxis_title="Valeur",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('viz-conversion-distribution', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_conversion_distribution(selected_test):
    """Conversion distribution"""
    test_data = ab_summary[ab_summary['scenario_name'] == selected_test].iloc[0]
    
    # Generate distribution curves
    x = np.linspace(0, 0.1, 100)
    
    control_mean = test_data['control_rate']
    control_std = 0.0015
    control_dist = stats.norm.pdf(x, control_mean, control_std)
    
    variant_mean = test_data['variant_rate']
    variant_std = 0.0015
    variant_dist = stats.norm.pdf(x, variant_mean, variant_std)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x * 100,
        y=control_dist,
        mode='lines',
        fill='tozeroy',
        name='Control',
        line=dict(color='#e74c3c', width=2),
        fillcolor='rgba(231, 76, 60, 0.3)'
    ))
    
    fig.add_trace(go.Scatter(
        x=x * 100,
        y=variant_dist,
        mode='lines',
        fill='tozeroy',
        name='Variant',
        line=dict(color='#2ecc71', width=2),
        fillcolor='rgba(46, 204, 113, 0.3)'
    ))
    
    fig.update_layout(
        xaxis_title="Taux de Conversion (%)",
        yaxis_title="Densité de Probabilité",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('viz-test-matrix', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_test_matrix(selected_test):
    """Test comparison matrix heatmap"""
    metrics = ['Control %', 'Variant %', 'Lift %', 'Power %', 'Confidence %']
    tests = ab_summary['scenario_name'].tolist()
    
    matrix_data = []
    for _, test_data in ab_summary.iterrows():
        row = [
            test_data['control_rate'] * 100,
            test_data['variant_rate'] * 100,
            test_data['lift_pct'],
            test_data['statistical_power'] * 100,
            test_data['prob_b_beats_a'] * 100
        ]
        matrix_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=metrics,
        y=[t[:30] + '...' if len(t) > 30 else t for t in tests],
        colorscale='RdYlGn',
        text=[[f'{val:.1f}' for val in row] for row in matrix_data],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Valeur")
    ))
    
    fig.update_layout(
        xaxis_title="Métrique",
        yaxis_title="Test",
        template='plotly_dark',
        height=400
    )
    
    return fig


@callback(
    Output('viz-lift-analysis', 'figure'),
    Input('viz-test-selector', 'value')
)
def update_lift_analysis(selected_test):
    """Lift analysis for all tests"""
    fig = go.Figure()
    
    sorted_tests = ab_summary.sort_values('lift_pct', ascending=True)
    
    colors = ['#2ecc71' if lift > 0 else '#e74c3c' for lift in sorted_tests['lift_pct']]
    
    fig.add_trace(go.Bar(
        y=[name[:30] + '...' if len(name) > 30 else name for name in sorted_tests['scenario_name']],
        x=sorted_tests['lift_pct'],
        orientation='h',
        marker_color=colors,
        text=[f'{v:+.1f}%' for v in sorted_tests['lift_pct']],
        textposition='outside'
    ))
    
    fig.add_vline(x=0, line_dash="dash", line_color="white")
    
    fig.update_layout(
        xaxis_title="Lift (%)",
        yaxis_title="Test",
        template='plotly_dark',
        height=400
    )
    
    return fig
