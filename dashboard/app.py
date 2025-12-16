"""
E-Commerce A/B Test Dashboard - Main Application
Multi-page Dash application with Bootstrap styling
Issue #19 - Dashboard Structure
"""

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import logging
from flask import request, redirect, session
from flask_login import current_user
from auth import AuthManager

# Configure logging for application monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Initialize authentication
auth_manager = AuthManager(server)

# Store auth_manager in Flask's app context for global access
server.auth_manager = auth_manager

# SECURITY: Setup DDoS protection with rate limiting
from ddos_protection import setup_ddos_protection
setup_ddos_protection(server)

# SECURITY: Add security headers to all responses
@server.after_request
def add_security_headers(response):
    """Add security headers to protect against common web vulnerabilities"""
    # Prevent clickjacking attacks
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection in older browsers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy - restrict resource loading
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdn.plot.ly; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self'"
    )
    
    # Control referrer information
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions policy (formerly Feature-Policy)
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=(), '
        'payment=(), usb=(), magnetometer=(), gyroscope=()'
    )
    
    # HSTS for HTTPS enforcement (commented out for dev, enable in production with HTTPS)
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

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
                
                html.Hr(className="my-3"),
                
                # User info and logout
                html.Div([
                    html.Div([
                        html.I(className="fas fa-user-circle fa-lg me-2 text-info"),
                        html.Span(id="current-username", className="text-white fw-bold"),
                    ], className="px-3 mb-2"),
                    dbc.NavLink([
                        html.I(className="fas fa-sign-out-alt me-2"),
                        "Déconnexion"
                    ], href="/logout", className="text-danger"),
                ], id="user-info-section"),
                
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
    
    # Hidden components for callbacks
    dcc.Location(id='url', refresh=False),
    
], style={"backgroundColor": "#0d1117"})


# Authentication middleware
@server.before_request
def check_authentication():
    """Check if user is authenticated before allowing access"""
    # Allow access to login page and static assets
    if request.path.startswith('/login') or \
       request.path.startswith('/assets') or \
       request.path.startswith('/_dash') or \
       request.path.startswith('/logout'):
        return None
    
    # Check if user is authenticated
    if not current_user.is_authenticated:
        logger.warning(f"Unauthorized access attempt to {request.path} from {request.remote_addr}")
        return redirect('/login')
    
    # Check if user needs to change password (but not if already on change-password page)
    if current_user.is_authenticated and \
       hasattr(current_user, 'force_password_change') and \
       current_user.force_password_change and \
       not request.path.startswith('/change-password'):
        logger.info(f"Redirecting {current_user.username} to change password")
        return redirect('/change-password')
    
    return None


# Add request logging middleware
@server.before_request
def log_request():
    """Log each incoming HTTP request"""
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr} - User: {current_user.username if current_user.is_authenticated else 'Anonymous'}")


@server.after_request
def log_response(response):
    """Log each HTTP response"""
    logger.info(f"Response: {request.method} {request.path} - Status {response.status_code}")
    return response


# Callback to display current username
@app.callback(
    dash.dependencies.Output('current-username', 'children'),
    dash.dependencies.Input('url', 'pathname')
)
def display_username(pathname):
    """Display current username in sidebar"""
    if current_user.is_authenticated:
        return current_user.username
    return "Invité"


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
    import os
    
    # SECURITY: Use environment variable to control debug mode
    # NEVER set debug=True in production!
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    if debug_mode:
        print("\n⚠️  WARNING: Debug mode is ENABLED - for development only!")
        print("🔄 Le dashboard se recharge automatiquement à chaque modification")
        print("🛑 Appuyez sur Ctrl+C pour arrêter\n")
    else:
        print("\n✅ Running in PRODUCTION mode (debug disabled)")
    
    logger.info("🚀 Starting E-Commerce A/B Test Dashboard...")
    
    app.run_server(
        debug=debug_mode,
        host='0.0.0.0',
        port=8050,
        dev_tools_hot_reload=debug_mode,
        dev_tools_ui=debug_mode,
    )
