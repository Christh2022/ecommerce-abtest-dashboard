"""
E-Commerce A/B Test Dashboard - Main Application
Multi-page Dash application with Bootstrap styling
Issue #19 - Dashboard Structure
"""

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap theme and multi-page support
app = Dash(
    __name__,
    use_pages=True,  # Enable multi-page functionality
    external_stylesheets=[
        dbc.themes.DARKLY,  # Dark theme
        dbc.icons.FONT_AWESOME,  # For icons
    ],
    suppress_callback_exceptions=True,
    title="E-Commerce A/B Test Dashboard",
    update_title=None,  # Prevent "Updating..." in title
)

# Server object for deployment
server = app.server

# Main layout with sidebar navigation
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-chart-line me-3"),
                    "E-Commerce A/B Test Dashboard"
                ], className="text-white mb-0"),
                html.P(
                    "Analyse complète des tests A/B et optimisations e-commerce",
                    className="text-white-50 mb-0"
                ),
            ], className="p-4 bg-primary rounded-3 mb-4 shadow")
        ])
    ]),
    
    # Main content area with sidebar and page content
    dbc.Row([
        # Sidebar navigation (3 columns width)
        dbc.Col([
            dbc.Nav([
                dbc.NavLink([
                    html.I(className="fas fa-home me-2"),
                    "Accueil"
                ], href="/", active="exact", className="mb-2"),
                
                html.Hr(className="my-3"),
                
                html.H6("KPI Analysis", className="text-muted px-3 mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-users me-2"),
                    "Trafic & Utilisateurs"
                ], href="/traffic", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-mouse-pointer me-2"),
                    "Comportement"
                ], href="/behavior", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-shopping-cart me-2"),
                    "Conversions"
                ], href="/conversions", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-box me-2"),
                    "Produits"
                ], href="/products", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-filter me-2"),
                    "Funnel"
                ], href="/funnel", active="exact", className="mb-2"),
                
                html.Hr(className="my-3"),
                
                html.H6("A/B Testing", className="text-muted px-3 mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-flask me-2"),
                    "Simulations"
                ], href="/ab-testing/simulations", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Résultats Tests"
                ], href="/ab-testing/results", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-calculator me-2"),
                    "Calculateur Z-Test"
                ], href="/ab-testing/calculator", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-chart-area me-2"),
                    "Visualisations"
                ], href="/ab-testing/visualizations", active="exact", className="mb-2"),
                
                html.Hr(className="my-3"),
                
                html.H6("Documentation", className="text-muted px-3 mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-book me-2"),
                    "Guide Méthodologie"
                ], href="/methodology", active="exact", className="mb-2"),
                
                dbc.NavLink([
                    html.I(className="fas fa-info-circle me-2"),
                    "À Propos"
                ], href="/about", active="exact", className="mb-2"),
                
            ], vertical=True, pills=True, className="bg-dark p-3 rounded-3 shadow-sm"),
            
            # Footer info in sidebar
            html.Div([
                html.Hr(),
                html.P([
                    html.I(className="fas fa-database me-2"),
                    "Période: Mai-Sept 2015"
                ], className="text-muted small mb-1"),
                html.P([
                    html.I(className="fas fa-chart-line me-2"),
                    "1.65M utilisateurs"
                ], className="text-muted small mb-1"),
                html.P([
                    html.I(className="fas fa-shopping-basket me-2"),
                    "22.5K transactions"
                ], className="text-muted small mb-0"),
            ], className="px-3 py-2 bg-dark rounded-3 mt-3"),
            
        ], width=3, className="pe-3"),
        
        # Page content (9 columns width)
        dbc.Col([
            # Page content will be inserted here by dash.page_container
            dash.page_container
        ], width=9),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(className="my-4"),
            html.Div([
                html.P([
                    "Dashboard créé avec ",
                    html.I(className="fas fa-heart text-danger"),
                    " | ",
                    html.A("GitHub", href="https://github.com/Christh2022/ecommerce-abtest-dashboard", 
                           target="_blank", className="text-decoration-none"),
                    " | Milestone 4: Multi-page Dashboard"
                ], className="text-center text-muted small mb-0")
            ])
        ])
    ])
    
], fluid=True, className="p-4", style={"backgroundColor": "#0d1117"})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 E-Commerce A/B Test Dashboard")
    print("="*60)
    print("📊 Dashboard URL: http://127.0.0.1:8050")
    print("📁 Pages disponibles:")
    print("   - Home: /")
    print("   - Traffic: /traffic")
    print("   - Behavior: /behavior")
    print("   - Conversions: /conversions")
    print("   - Products: /products")
    print("   - Funnel: /funnel")
    print("   - A/B Simulations: /ab-testing/simulations")
    print("   - A/B Results: /ab-testing/results")
    print("   - Z-Test Calculator: /ab-testing/calculator")
    print("   - Visualizations: /ab-testing/visualizations")
    print("   - Methodology: /methodology")
    print("   - About: /about")
    print("="*60)
    print("\n🔄 Le dashboard se recharge automatiquement à chaque modification")
    print("🛑 Appuyez sur Ctrl+C pour arrêter\n")
    
    app.run_server(
        debug=True,
        host='127.0.0.1',
        port=8050,
        dev_tools_hot_reload=True,
        dev_tools_ui=True,
    )
