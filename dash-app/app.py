"""
Application Dash principale - E-commerce Dashboard & A/B Testing
Point d'entrée de l'application
"""

import os
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'application Dash avec support multi-pages
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="E-commerce Dashboard & A/B Testing"
)

server = app.server

# Layout principal avec navigation
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-shopping-cart me-2"),
                    "E-commerce Dashboard & A/B Testing"
                ], className="text-primary"),
                html.P("Analyse avancée et tests A/B pour optimiser vos performances", 
                       className="text-muted")
            ], className="my-4")
        ])
    ]),
    
    # Navigation
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavLink([
                    html.I(className="fas fa-home me-2"),
                    "Accueil"
                ], href="/", active="exact"),
                dbc.NavLink([
                    html.I(className="fas fa-chart-line me-2"),
                    "Comportement"
                ], href="/behavior", active="exact"),
                dbc.NavLink([
                    html.I(className="fas fa-box me-2"),
                    "Produits"
                ], href="/products", active="exact"),
                dbc.NavLink([
                    html.I(className="fas fa-flask me-2"),
                    "Tests A/B"
                ], href="/ab-testing", active="exact"),
                dbc.NavLink([
                    html.I(className="fas fa-users me-2"),
                    "Cohortes"
                ], href="/cohorts", active="exact"),
            ], pills=True, className="mb-4")
        ])
    ]),
    
    # Container pour les pages
    dbc.Row([
        dbc.Col([
            page_container
        ])
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.Footer([
                html.P([
                    "E-commerce Dashboard & A/B Testing © 2025 | ",
                    html.A("Documentation", href="/docs", className="text-decoration-none"),
                    " | ",
                    html.A("GitHub", href="https://github.com/Christh2022/ecommerce-abtest-dashboard", 
                           target="_blank", className="text-decoration-none")
                ], className="text-center text-muted small")
            ], className="my-4")
        ])
    ])
], fluid=True)


if __name__ == '__main__':
    debug_mode = os.getenv('DASH_DEBUG', 'False').lower() == 'true'
    host = os.getenv('DASH_HOST', '0.0.0.0')
    port = int(os.getenv('DASH_PORT', 8050))
    
    print("=" * 60)
    print("🚀 Démarrage de l'application E-commerce Dashboard")
    print("=" * 60)
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Mode debug: {debug_mode}")
    print("=" * 60)
    
    app.run_server(debug=debug_mode, host=host, port=port)
