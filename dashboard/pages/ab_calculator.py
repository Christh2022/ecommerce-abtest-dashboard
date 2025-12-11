"""
E-Commerce A/B Test Dashboard - A/B Test Simulator & Calculator
Calculateur interactif pour créer et simuler vos propres tests A/B
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
import os

# Register page
dash.register_page(__name__, path='/ab-testing/calculator', name='Calculateur Simulation')

# Layout
layout = dbc.Container([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-calculator me-3"),
                    "Calculateur de Simulation A/B Test"
                ], className="mb-2"),
                html.P(
                    "Configurez et simulez vos propres tests A/B en temps réel",
                    className="text-muted mb-4"
                ),
            ])
        ])
    ]),
    
    # Instructions Panel
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H5([html.I(className="fas fa-info-circle me-2"), "Comment utiliser ce simulateur"], className="alert-heading"),
                html.Hr(),
                html.Ol([
                    html.Li("Configurez les paramètres de base (taux de conversion actuel, amélioration attendue)"),
                    html.Li("Ajustez la taille de l'échantillon et la durée du test"),
                    html.Li("Définissez les paramètres statistiques (niveau de confiance, puissance)"),
                    html.Li("Cliquez sur 'Lancer la Simulation' pour voir les résultats"),
                    html.Li("Analysez les graphiques de prédiction et les métriques statistiques")
                ], className="mb-0")
            ], color="info", className="mb-4")
        ])
    ]),
    
    # Configuration Panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-cog me-2"),
                    "Configuration du Test"
                ]),
                dbc.CardBody([
                    # Baseline Configuration
                    dbc.Row([
                        dbc.Col([
                            html.Label("Taux de Conversion Actuel (%)", className="fw-bold"),
                            dcc.Input(
                                id='baseline-rate',
                                type='number',
                                value=2.5,
                                min=0.1,
                                max=50,
                                step=0.1,
                                className='form-control mb-3'
                            ),
                            html.Small("Le taux de conversion actuel de votre site", className="text-muted")
                        ], width=6),
                        
                        dbc.Col([
                            html.Label("Amélioration Attendue (%)", className="fw-bold"),
                            dcc.Input(
                                id='expected-improvement',
                                type='number',
                                value=20,
                                min=1,
                                max=200,
                                step=1,
                                className='form-control mb-3'
                            ),
                            html.Small("L'amélioration relative que vous espérez atteindre", className="text-muted")
                        ], width=6),
                    ]),
                    
                    html.Hr(),
                    
                    # Sample Size Configuration
                    dbc.Row([
                        dbc.Col([
                            html.Label("Visiteurs par Jour", className="fw-bold"),
                            dcc.Input(
                                id='daily-visitors',
                                type='number',
                                value=5000,
                                min=100,
                                max=100000,
                                step=100,
                                className='form-control mb-3'
                            ),
                            html.Small("Nombre de visiteurs quotidiens sur votre site", className="text-muted")
                        ], width=4),
                        
                        dbc.Col([
                            html.Label("Durée du Test (jours)", className="fw-bold"),
                            dcc.Input(
                                id='test-duration',
                                type='number',
                                value=14,
                                min=7,
                                max=90,
                                step=1,
                                className='form-control mb-3'
                            ),
                            html.Small("Durée recommandée: 14-30 jours", className="text-muted")
                        ], width=4),
                        
                        dbc.Col([
                            html.Label("Split Test (%)", className="fw-bold"),
                            dcc.Slider(
                                id='test-split',
                                min=10,
                                max=50,
                                step=5,
                                value=50,
                                marks={10: '10%', 25: '25%', 50: '50%'},
                                className='mb-3'
                            ),
                            html.Small("Pourcentage de trafic pour le variant", className="text-muted")
                        ], width=4),
                    ]),
                    
                    html.Hr(),
                    
                    # Statistical Parameters
                    dbc.Row([
                        dbc.Col([
                            html.Label("Niveau de Confiance", className="fw-bold"),
                            dcc.Dropdown(
                                id='confidence-level',
                                options=[
                                    {'label': '90% (Z = 1.645)', 'value': 0.90},
                                    {'label': '95% (Z = 1.96)', 'value': 0.95},
                                    {'label': '99% (Z = 2.576)', 'value': 0.99}
                                ],
                                value=0.95,
                                clearable=False,
                                className='mb-3'
                            ),
                            html.Small("Probabilité que l'effet soit réel", className="text-muted")
                        ], width=6),
                        
                        dbc.Col([
                            html.Label("Puissance Statistique", className="fw-bold"),
                            dcc.Dropdown(
                                id='statistical-power',
                                options=[
                                    {'label': '70%', 'value': 0.70},
                                    {'label': '80% (Recommandé)', 'value': 0.80},
                                    {'label': '90%', 'value': 0.90}
                                ],
                                value=0.80,
                                clearable=False,
                                className='mb-3'
                            ),
                            html.Small("Capacité à détecter un effet réel", className="text-muted")
                        ], width=6),
                    ]),
                    
                    html.Hr(),
                    
                    # Action Button
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-play me-2"),
                                "Lancer la Simulation"
                            ], id='run-simulation-btn', color='primary', size='lg', className='w-100')
                        ])
                    ])
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Results Section (Hidden until simulation runs)
    html.Div(id='simulation-results', children=[
        # Summary Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users fa-2x text-primary mb-2"),
                            html.H3(id='calc-sample-size', className="mb-0"),
                            html.P("Taille Échantillon Totale", className="text-muted mb-0 small")
                        ], className="text-center")
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-percentage fa-2x text-success mb-2"),
                            html.H3(id='calc-variant-rate', className="mb-0"),
                            html.P("Taux Variant Attendu", className="text-muted mb-0 small")
                        ], className="text-center")
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-bolt fa-2x text-warning mb-2"),
                            html.H3(id='calc-power', className="mb-0"),
                            html.P("Puissance Statistique", className="text-muted mb-0 small")
                        ], className="text-center")
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-check-circle fa-2x text-info mb-2"),
                            html.H3(id='calc-significance', className="mb-0"),
                            html.P("Significativité Attendue", className="text-muted mb-0 small")
                        ], className="text-center")
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=3),
        ]),
        
        # Simulation Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-line me-2"),
                        "Évolution Prédictive des Conversions"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='calc-conversion-prediction', config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-area me-2"),
                        "Confidence Intervals"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='calc-confidence-intervals', config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-signal me-2"),
                        "Évolution de la Puissance Statistique"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='calc-power-evolution', config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Distribution des Résultats"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='calc-results-distribution', config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=6),
        ]),
        
        # Recommendations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-lightbulb me-2"),
                        "Recommandations"
                    ]),
                    dbc.CardBody([
                        html.Div(id='calc-recommendations')
                    ])
                ], className="shadow-sm border-0 mb-4")
            ])
        ]),
    ], style={'display': 'none'}),  # Hidden by default
    
], fluid=True)


# Callbacks
@callback(
    [Output('simulation-results', 'style'),
     Output('calc-sample-size', 'children'),
     Output('calc-variant-rate', 'children'),
     Output('calc-power', 'children'),
     Output('calc-significance', 'children'),
     Output('calc-conversion-prediction', 'figure'),
     Output('calc-confidence-intervals', 'figure'),
     Output('calc-power-evolution', 'figure'),
     Output('calc-results-distribution', 'figure'),
     Output('calc-recommendations', 'children')],
    Input('run-simulation-btn', 'n_clicks'),
    [State('baseline-rate', 'value'),
     State('expected-improvement', 'value'),
     State('daily-visitors', 'value'),
     State('test-duration', 'value'),
     State('test-split', 'value'),
     State('confidence-level', 'value'),
     State('statistical-power', 'value')]
)
def run_simulation(n_clicks, baseline_rate, improvement, daily_visitors, duration, split, confidence, power):
    """Run the A/B test simulation"""
    if not n_clicks:
        return ({'display': 'none'}, "", "", "", "", go.Figure(), go.Figure(), go.Figure(), go.Figure(), "")
    
    # Convert inputs
    baseline_rate = baseline_rate / 100
    improvement_pct = improvement / 100
    variant_rate = baseline_rate * (1 + improvement_pct)
    split = split / 100
    
    # Calculate sample sizes
    total_visitors = daily_visitors * duration
    variant_visitors = int(total_visitors * split)
    control_visitors = int(total_visitors * (1 - split))
    
    # Calculate Z-scores
    z_alpha = stats.norm.ppf(1 - (1 - confidence) / 2)
    z_beta = stats.norm.ppf(power)
    
    # Simulate daily results
    days = np.arange(1, duration + 1)
    daily_control_visitors = control_visitors / duration
    daily_variant_visitors = variant_visitors / duration
    
    # Control group simulation
    control_conversions = np.random.binomial(int(daily_control_visitors), baseline_rate, duration)
    control_rates = control_conversions / daily_control_visitors
    
    # Variant group simulation
    variant_conversions = np.random.binomial(int(daily_variant_visitors), variant_rate, duration)
    variant_rates = variant_conversions / daily_variant_visitors
    
    # Cumulative rates
    cumulative_control_conversions = np.cumsum(control_conversions)
    cumulative_variant_conversions = np.cumsum(variant_conversions)
    cumulative_control_visitors = np.cumsum([daily_control_visitors] * duration)
    cumulative_variant_visitors = np.cumsum([daily_variant_visitors] * duration)
    
    cumulative_control_rates = cumulative_control_conversions / cumulative_control_visitors
    cumulative_variant_rates = cumulative_variant_conversions / cumulative_variant_visitors
    
    # Calculate confidence intervals
    control_se = np.sqrt(cumulative_control_rates * (1 - cumulative_control_rates) / cumulative_control_visitors)
    variant_se = np.sqrt(cumulative_variant_rates * (1 - cumulative_variant_rates) / cumulative_variant_visitors)
    
    control_ci_lower = cumulative_control_rates - z_alpha * control_se
    control_ci_upper = cumulative_control_rates + z_alpha * control_se
    variant_ci_lower = cumulative_variant_rates - z_alpha * variant_se
    variant_ci_upper = cumulative_variant_rates + z_alpha * variant_se
    
    # Calculate statistical power over time
    pooled_se = np.sqrt(cumulative_control_rates * (1 - cumulative_control_rates) / cumulative_control_visitors + 
                        cumulative_variant_rates * (1 - cumulative_variant_rates) / cumulative_variant_visitors)
    z_scores = (cumulative_variant_rates - cumulative_control_rates) / pooled_se
    power_over_time = stats.norm.cdf(z_scores - z_alpha) + stats.norm.cdf(-z_scores - z_alpha)
    power_over_time = power_over_time * 100
    
    # KPIs
    final_sample = f"{total_visitors:,.0f}"
    final_variant_rate = f"{variant_rate * 100:.2f}%"
    final_power = f"{power * 100:.0f}%"
    
    # Calculate expected significance
    final_z = z_scores[-1]
    expected_pvalue = 2 * (1 - stats.norm.cdf(abs(final_z)))
    is_significant = expected_pvalue < (1 - confidence)
    significance_text = "OUI" if is_significant else "NON"
    
    # Chart 1: Conversion Prediction
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=days, y=cumulative_control_rates * 100,
        mode='lines', name='Control',
        line=dict(color='#e74c3c', width=3)
    ))
    fig1.add_trace(go.Scatter(
        x=days, y=cumulative_variant_rates * 100,
        mode='lines', name='Variant',
        line=dict(color='#2ecc71', width=3)
    ))
    fig1.update_layout(
        title="Taux de Conversion Cumulés",
        xaxis_title="Jour",
        yaxis_title="Taux de Conversion (%)",
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )
    
    # Chart 2: Confidence Intervals
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=days, y=control_ci_upper * 100,
        mode='lines', line=dict(width=0),
        showlegend=False, hoverinfo='skip'
    ))
    fig2.add_trace(go.Scatter(
        x=days, y=control_ci_lower * 100,
        mode='lines', line=dict(width=0),
        fillcolor='rgba(231, 76, 60, 0.2)',
        fill='tonexty', name='Control CI',
        hoverinfo='skip'
    ))
    fig2.add_trace(go.Scatter(
        x=days, y=variant_ci_upper * 100,
        mode='lines', line=dict(width=0),
        showlegend=False, hoverinfo='skip'
    ))
    fig2.add_trace(go.Scatter(
        x=days, y=variant_ci_lower * 100,
        mode='lines', line=dict(width=0),
        fillcolor='rgba(46, 204, 113, 0.2)',
        fill='tonexty', name='Variant CI',
        hoverinfo='skip'
    ))
    fig2.add_trace(go.Scatter(
        x=days, y=cumulative_control_rates * 100,
        mode='lines', name='Control',
        line=dict(color='#e74c3c', width=2)
    ))
    fig2.add_trace(go.Scatter(
        x=days, y=cumulative_variant_rates * 100,
        mode='lines', name='Variant',
        line=dict(color='#2ecc71', width=2)
    ))
    fig2.update_layout(
        title=f"Intervalles de Confiance ({int(confidence*100)}%)",
        xaxis_title="Jour",
        yaxis_title="Taux de Conversion (%)",
        template='plotly_dark',
        height=400
    )
    
    # Chart 3: Power Evolution
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=days, y=power_over_time,
        mode='lines', fill='tozeroy',
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    fig3.add_hline(y=power*100, line_dash="dash", line_color="yellow",
                   annotation_text=f"Cible: {int(power*100)}%")
    fig3.update_layout(
        title="Puissance Statistique au Fil du Temps",
        xaxis_title="Jour",
        yaxis_title="Puissance (%)",
        template='plotly_dark',
        height=400
    )
    
    # Chart 4: Results Distribution
    fig4 = go.Figure()
    x_range = np.linspace(0, max(variant_rate, baseline_rate) * 2, 100)
    control_dist = stats.norm.pdf(x_range, baseline_rate, control_se[-1])
    variant_dist = stats.norm.pdf(x_range, variant_rate, variant_se[-1])
    
    fig4.add_trace(go.Scatter(
        x=x_range * 100, y=control_dist,
        mode='lines', fill='tozeroy',
        name='Control',
        line=dict(color='#e74c3c', width=2),
        fillcolor='rgba(231, 76, 60, 0.3)'
    ))
    fig4.add_trace(go.Scatter(
        x=x_range * 100, y=variant_dist,
        mode='lines', fill='tozeroy',
        name='Variant',
        line=dict(color='#2ecc71', width=2),
        fillcolor='rgba(46, 204, 113, 0.3)'
    ))
    fig4.update_layout(
        title="Distribution Probabiliste des Taux",
        xaxis_title="Taux de Conversion (%)",
        yaxis_title="Densité de Probabilité",
        template='plotly_dark',
        height=400
    )
    
    # Recommendations
    recommendations = []
    
    if is_significant:
        recommendations.append(dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            f"Test statistiquement significatif! Le variant montre une amélioration de {improvement}% avec {int(confidence*100)}% de confiance."
        ], color="success"))
    else:
        recommendations.append(dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Test non significatif. Considérez d'augmenter la durée ou la taille de l'échantillon."
        ], color="warning"))
    
    if power_over_time[-1] < 80:
        recommendations.append(dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            f"Puissance actuelle: {power_over_time[-1]:.1f}%. Recommandé: ≥80%. Augmentez la taille de l'échantillon."
        ], color="info"))
    
    if duration < 14:
        recommendations.append(dbc.Alert([
            html.I(className="fas fa-clock me-2"),
            "Durée de test courte. Recommandation: minimum 14 jours pour capturer les variations hebdomadaires."
        ], color="warning"))
    
    recommendations.append(dbc.Alert([
        html.H6("Métriques Finales:", className="alert-heading"),
        html.Ul([
            html.Li(f"Échantillon total: {total_visitors:,} visiteurs"),
            html.Li(f"Control: {control_visitors:,} | Variant: {variant_visitors:,}"),
            html.Li(f"Taux Control: {baseline_rate*100:.2f}% | Variant: {cumulative_variant_rates[-1]*100:.2f}%"),
            html.Li(f"Z-Score: {final_z:.2f} | P-Value: {expected_pvalue:.4f}"),
            html.Li(f"Lift observé: {((cumulative_variant_rates[-1]/baseline_rate - 1)*100):.2f}%")
        ])
    ], color="light"))
    
    return (
        {'display': 'block'},
        final_sample,
        final_variant_rate,
        final_power,
        significance_text,
        fig1, fig2, fig3, fig4,
        recommendations
    )
