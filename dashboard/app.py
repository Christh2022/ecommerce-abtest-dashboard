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
app.layout = html.Div([
    # Fixed Header
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1([
                            html.I(className="fas fa-chart-line me-3"),
                            "E-Commerce A/B Test Dashboard"
                        ], className="text-white mb-1", style={"fontSize": "1.8rem", "fontWeight": "600"}),
                        html.P([
                            "Analyse complète des tests A/B et optimisations e-commerce",
                            html.Span(" | ", className="mx-2"),
                            html.I(className="fas fa-calendar-alt me-2"),
                            "Mai - Septembre 2015"
                        ], className="text-white-50 mb-0", style={"fontSize": "0.95rem"}),
                    ], className="d-flex flex-column justify-content-center", style={"height": "100%"})
                ], width=9),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-users fa-2x mb-2"),
                            html.H4("1.65M", className="mb-0 fw-bold"),
                            html.Small("Utilisateurs", className="text-white-50")
                        ], className="text-center text-white p-2"),
                    ], className="d-flex align-items-center justify-content-center h-100")
                ], width=3),
            ], className="align-items-center")
        ], fluid=True)
    ], className="shadow-lg", style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "right": "0",
        "zIndex": "1000",
        "backgroundColor": "#161b22",
        "borderBottom": "1px solid #30363d"
    }),
    
    # Main content area with fixed sidebar
    html.Div([
        # Fixed Sidebar navigation
        html.Div([
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
                
                dbc.NavLink([
                    html.I(className="fas fa-layer-group me-2"),
                    "Cohorts & Rétention"
                ], href="/cohorts", active="exact", className="mb-2"),
                
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
                
            ], vertical=True, pills=True, className="bg-dark p-3"),
            
            # Footer info in sidebar
            html.Div([
                html.Hr(className="border-secondary"),
                html.Div([
                    html.Div([
                        html.I(className="fas fa-database fa-lg mb-2 text-primary"),
                        html.P("139 jours", className="mb-0 fw-bold"),
                        html.Small("de données", className="text-muted")
                    ], className="text-center mb-3"),
                    html.Div([
                        html.I(className="fas fa-shopping-basket fa-lg mb-2 text-success"),
                        html.P("22.5K", className="mb-0 fw-bold"),
                        html.Small("transactions", className="text-muted")
                    ], className="text-center mb-3"),
                    html.Div([
                        html.I(className="fas fa-box fa-lg mb-2 text-warning"),
                        html.P("235K", className="mb-0 fw-bold"),
                        html.Small("produits", className="text-muted")
                    ], className="text-center"),
                ], className="p-3 bg-dark rounded-3 border border-secondary")
            ], className="px-3 py-2 mt-3"),
            
        ], style={
            "position": "fixed",
            "top": "100px",
            "left": "0",
            "width": "280px",
            "height": "calc(100vh - 100px)",
            "overflowY": "auto",
            "overflowX": "hidden",
            "backgroundColor": "#161b22",
            "padding": "1rem",
            "borderRight": "1px solid #30363d",
            "zIndex": "999"
        }),
        
        # Page content with left margin for fixed sidebar
        html.Div([
            dbc.Container([
                dash.page_container
            ], fluid=True, className="p-4")
        ], style={
            "marginLeft": "280px",
            "marginTop": "100px",
            "backgroundColor": "#0d1117",
            "minHeight": "calc(100vh - 100px)"
        }),
    ]),
    
], style={"backgroundColor": "#0d1117"})


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
