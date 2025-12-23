"""
Login Page for E-Commerce Dashboard
Provides user authentication interface
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import login_user, current_user
from flask import session, redirect, current_app
import logging

# This page does not require registration as it's the login page
dash.register_page(__name__, path='/login', title='Login - E-Commerce Dashboard')

logger = logging.getLogger(__name__)


def layout():
    """Login page layout"""
    
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return dcc.Location(pathname='/', id='redirect-home')
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            # Logo and title
                            html.Div([
                                html.I(className="fas fa-chart-line fa-3x text-primary mb-3"),
                                html.H2("E-Commerce Dashboard", className="text-white mb-2"),
                                html.P("Connexion requise pour accéder au tableau de bord", 
                                      className="text-muted mb-4"),
                            ], className="text-center mb-4"),
                            
                            # Login form
                            html.Div([
                                dbc.Alert(
                                    id="login-alert",
                                    is_open=False,
                                    dismissable=True,
                                    duration=4000,
                                ),
                                
                                dbc.Label("Nom d'utilisateur", html_for="username-input"),
                                dbc.Input(
                                    id="username-input",
                                    type="text",
                                    placeholder="Entrez votre nom d'utilisateur",
                                    className="mb-3",
                                    autoComplete="username",
                                ),
                                
                                dbc.Label("Mot de passe", html_for="password-input"),
                                dbc.Input(
                                    id="password-input",
                                    type="password",
                                    placeholder="Entrez votre mot de passe",
                                    className="mb-3",
                                    autoComplete="current-password",
                                ),
                                
                                dbc.Checkbox(
                                    id="remember-me",
                                    label="Se souvenir de moi",
                                    value=False,
                                    className="mb-3",
                                ),
                                
                                dbc.Button(
                                    [
                                        html.I(className="fas fa-sign-in-alt me-2"),
                                        "Se connecter"
                                    ],
                                    id="login-button",
                                    color="primary",
                                    className="w-100 mb-3",
                                    size="lg",
                                ),
                                
                                dbc.Spinner(
                                    html.Div(id="login-output"),
                                    color="primary",
                                    type="border",
                                    size="sm",
                                ),
                            ]),
                            
                            # Info section
                            html.Hr(className="my-4"),
                            html.Div([
                                html.H6("Comptes de démonstration:", className="text-muted mb-3"),
                                dbc.Alert([
                                    html.I(className="fas fa-info-circle me-2"),
                                    html.Strong("Première connexion : "),
                                    "Vous devrez changer votre mot de passe après la première connexion."
                                ], color="info", className="mb-3", style={"fontSize": "0.85rem"}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.I(className="fas fa-user-shield text-danger me-2"),
                                            html.Strong("Admin", className="text-white"),
                                            html.Br(),
                                            html.Small("admin / admin123", className="text-muted font-monospace"),
                                        ], className="p-3 bg-dark rounded")
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.I(className="fas fa-user text-primary me-2"),
                                            html.Strong("Utilisateur", className="text-white"),
                                            html.Br(),
                                            html.Small("user / user123", className="text-muted font-monospace"),
                                        ], className="p-3 bg-dark rounded")
                                    ], width=6),
                                ]),
                            ]),
                        ]),
                    ], className="p-5"),
                ], className="shadow-lg border-0", style={"backgroundColor": "#161b22"}),
            ], width={"size": 6, "offset": 3}, lg={"size": 4, "offset": 4}),
        ], className="min-vh-100 align-items-center"),
        
        # Store for login state
        dcc.Store(id='login-state'),
        dcc.Location(id='login-redirect', refresh=True),
        
    ], fluid=True, className="bg-dark py-5")


@callback(
    [Output('login-alert', 'children'),
     Output('login-alert', 'is_open'),
     Output('login-alert', 'color'),
     Output('login-redirect', 'pathname')],
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'),
     State('password-input', 'value'),
     State('remember-me', 'value')],
    prevent_initial_call=True
)
def login_user_callback(n_clicks, username, password, remember):
    """Handle login button click"""
    
    logger.info(f"Login callback triggered! n_clicks={n_clicks}, username={username}")
    
    if not n_clicks:
        logger.warning("No clicks registered")
        return "", False, "danger", dash.no_update
    
    # Validate inputs
    if not username or not password:
        logger.warning(f"Empty fields - username: {bool(username)}, password: {bool(password)}")
        return "Veuillez remplir tous les champs", True, "warning", dash.no_update
    
    # Get auth_manager from Flask app context
    try:
        auth_manager = current_app.auth_manager
        
        logger.info(f"Attempting to authenticate user: {username}")
        
        # Attempt authentication
        user = auth_manager.authenticate_user(username, password, remember=remember)
        
        if user:
            logger.info(f"✓ Successful login: {username}")
            session.permanent = remember
            return "Connexion réussie! Redirection...", True, "success", '/'
        else:
            logger.warning(f"✗ Failed login attempt for user: {username}")
            return "Nom d'utilisateur ou mot de passe incorrect", True, "danger", dash.no_update
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return "Erreur de connexion. Veuillez réessayer.", True, "danger", dash.no_update


# Add keyboard support for Enter key
dash.clientside_callback(
    """
    function(username, password) {
        document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                document.getElementById('login-button').click();
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output('login-output', 'children'),
    [Input('username-input', 'value'),
     Input('password-input', 'value')]
)
