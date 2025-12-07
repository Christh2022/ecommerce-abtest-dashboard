"""
Page d'analyse comportementale
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/behavior', name='Comportement')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Analyse du comportement utilisateur", className="text-primary mb-4"),
            html.P("Cette page contiendra l'analyse du comportement des utilisateurs.", 
                   className="text-muted")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🚧 En construction", className="text-center"),
                    html.P("Cette page sera développée dans la branche feature/dashboard-behavior", 
                           className="text-center text-muted")
                ])
            ])
        ])
    ])
], fluid=True)
