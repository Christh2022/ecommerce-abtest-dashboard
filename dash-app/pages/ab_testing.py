"""
Page de tests A/B
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/ab-testing', name='Tests A/B')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Tests A/B", className="text-primary mb-4"),
            html.P("Cette page contiendra l'analyse des tests A/B.", 
                   className="text-muted")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🚧 En construction", className="text-center"),
                    html.P("Cette page sera développée dans la branche feature/dashboard-abtest", 
                           className="text-center text-muted")
                ])
            ])
        ])
    ])
], fluid=True)
