"""
Page d'analyse des produits
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/products', name='Produits')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Analyse des produits", className="text-primary mb-4"),
            html.P("Cette page contiendra l'analyse des performances des produits.", 
                   className="text-muted")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🚧 En construction", className="text-center"),
                    html.P("Cette page sera développée dans la branche feature/dashboard-products", 
                           className="text-center text-muted")
                ])
            ])
        ])
    ])
], fluid=True)
