"""
Change Password Page for E-Commerce Dashboard
Forces users to change their password on first login
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import current_user, logout_user
from flask import session
import logging
import re

dash.register_page(__name__, path='/change-password', title='Changer le mot de passe')

logger = logging.getLogger(__name__)


def layout():
    """Change password page layout"""
    
    # If user is not logged in, redirect to login
    if not current_user.is_authenticated:
        return dcc.Location(pathname='/login', id='redirect-login')
    
    # Check if password change is forced
    is_forced = getattr(current_user, 'force_password_change', False)
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            # Header
                            html.Div([
                                html.I(className="fas fa-key fa-3x text-warning mb-3"),
                                html.H2("Changement de mot de passe", className="text-white mb-2"),
                                html.P(
                                    "Pour des raisons de sécurité, vous devez changer votre mot de passe" if is_forced 
                                    else "Modifiez votre mot de passe", 
                                    className="text-muted mb-4"
                                ),
                            ], className="text-center mb-4"),
                            
                            # Alert for forced password change
                            dbc.Alert([
                                html.I(className="fas fa-exclamation-triangle me-2"),
                                html.Strong("Changement obligatoire : "),
                                "Vous utilisez un mot de passe par défaut. Veuillez le changer avant de continuer."
                            ], color="warning", className="mb-4") if is_forced else None,
                            
                            # Change password form
                            html.Div([
                                dbc.Alert(
                                    id="change-password-alert",
                                    is_open=False,
                                    dismissable=True,
                                    duration=4000,
                                ),
                                
                                # Current user info
                                html.Div([
                                    html.I(className="fas fa-user me-2"),
                                    html.Strong("Utilisateur : ", className="text-muted"),
                                    html.Span(current_user.username, className="text-white"),
                                ], className="mb-3 p-3 bg-dark rounded"),
                                
                                dbc.Label("Nouveau mot de passe", html_for="new-password-input"),
                                dbc.Input(
                                    id="new-password-input",
                                    type="password",
                                    placeholder="Entrez votre nouveau mot de passe",
                                    className="mb-2",
                                    autoComplete="new-password",
                                ),
                                
                                # Password strength indicator
                                html.Div([
                                    html.Small(id="password-strength", className="text-muted"),
                                ], className="mb-3"),
                                
                                dbc.Label("Confirmer le mot de passe", html_for="confirm-password-input"),
                                dbc.Input(
                                    id="confirm-password-input",
                                    type="password",
                                    placeholder="Confirmez votre nouveau mot de passe",
                                    className="mb-3",
                                    autoComplete="new-password",
                                ),
                                
                                # Password requirements
                                html.Div([
                                    html.H6("Exigences du mot de passe:", className="text-muted mb-2"),
                                    html.Ul([
                                        html.Li([
                                            html.I(id="check-length", className="fas fa-circle text-muted me-2"),
                                            "Au moins 8 caractères"
                                        ], className="text-muted mb-1"),
                                        html.Li([
                                            html.I(id="check-uppercase", className="fas fa-circle text-muted me-2"),
                                            "Au moins une majuscule"
                                        ], className="text-muted mb-1"),
                                        html.Li([
                                            html.I(id="check-lowercase", className="fas fa-circle text-muted me-2"),
                                            "Au moins une minuscule"
                                        ], className="text-muted mb-1"),
                                        html.Li([
                                            html.I(id="check-number", className="fas fa-circle text-muted me-2"),
                                            "Au moins un chiffre"
                                        ], className="text-muted"),
                                    ], className="list-unstyled"),
                                ], className="p-3 bg-dark rounded mb-4"),
                                
                                dbc.Button(
                                    [
                                        html.I(className="fas fa-check me-2"),
                                        "Changer le mot de passe"
                                    ],
                                    id="change-password-button",
                                    color="success",
                                    className="w-100 mb-3",
                                    size="lg",
                                ),
                                
                                # Cancel button (only if not forced)
                                dbc.Button(
                                    [
                                        html.I(className="fas fa-times me-2"),
                                        "Annuler"
                                    ],
                                    id="cancel-button",
                                    color="secondary",
                                    className="w-100",
                                    href="/",
                                    outline=True,
                                ) if not is_forced else None,
                                
                                dbc.Spinner(
                                    html.Div(id="change-password-output"),
                                    color="success",
                                    type="border",
                                    size="sm",
                                ),
                            ]),
                        ]),
                    ], className="p-5"),
                ], className="shadow-lg border-0", style={"backgroundColor": "#161b22"}),
            ], width={"size": 6, "offset": 3}, lg={"size": 5, "offset": 3.5}),
        ], className="min-vh-100 align-items-center"),
        
        # Store for password change state
        dcc.Store(id='password-change-state'),
        dcc.Location(id='password-change-redirect', refresh=True),
        
    ], fluid=True, className="bg-dark py-5")


@callback(
    [Output('password-strength', 'children'),
     Output('password-strength', 'className'),
     Output('check-length', 'className'),
     Output('check-uppercase', 'className'),
     Output('check-lowercase', 'className'),
     Output('check-number', 'className')],
    Input('new-password-input', 'value'),
    prevent_initial_call=True
)
def check_password_strength(password):
    """Check password strength and requirements"""
    if not password:
        return "", "text-muted", "fas fa-circle text-muted me-2", "fas fa-circle text-muted me-2", "fas fa-circle text-muted me-2", "fas fa-circle text-muted me-2"
    
    # Check requirements
    length_ok = len(password) >= 8
    uppercase_ok = re.search(r'[A-Z]', password) is not None
    lowercase_ok = re.search(r'[a-z]', password) is not None
    number_ok = re.search(r'[0-9]', password) is not None
    
    # Calculate strength
    strength_score = sum([length_ok, uppercase_ok, lowercase_ok, number_ok])
    
    if strength_score == 4:
        strength_text = "✓ Mot de passe fort"
        strength_class = "text-success fw-bold"
    elif strength_score >= 3:
        strength_text = "⚠ Mot de passe moyen"
        strength_class = "text-warning fw-bold"
    else:
        strength_text = "✗ Mot de passe faible"
        strength_class = "text-danger fw-bold"
    
    # Icons for requirements
    check_icon = "fas fa-check-circle text-success me-2"
    circle_icon = "fas fa-circle text-muted me-2"
    
    return (
        strength_text,
        strength_class,
        check_icon if length_ok else circle_icon,
        check_icon if uppercase_ok else circle_icon,
        check_icon if lowercase_ok else circle_icon,
        check_icon if number_ok else circle_icon
    )


@callback(
    [Output('change-password-alert', 'children'),
     Output('change-password-alert', 'is_open'),
     Output('change-password-alert', 'color'),
     Output('password-change-redirect', 'pathname')],
    Input('change-password-button', 'n_clicks'),
    [State('new-password-input', 'value'),
     State('confirm-password-input', 'value')],
    prevent_initial_call=True
)
def change_password_callback(n_clicks, new_password, confirm_password):
    """Handle password change"""
    
    if not n_clicks:
        return "", False, "danger", dash.no_update
    
    # Validate inputs
    if not new_password or not confirm_password:
        return "Veuillez remplir tous les champs", True, "warning", dash.no_update
    
    # Check if passwords match
    if new_password != confirm_password:
        return "Les mots de passe ne correspondent pas", True, "danger", dash.no_update
    
    # Validate password strength
    if len(new_password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères", True, "danger", dash.no_update
    
    if not re.search(r'[A-Z]', new_password):
        return "Le mot de passe doit contenir au moins une majuscule", True, "danger", dash.no_update
    
    if not re.search(r'[a-z]', new_password):
        return "Le mot de passe doit contenir au moins une minuscule", True, "danger", dash.no_update
    
    if not re.search(r'[0-9]', new_password):
        return "Le mot de passe doit contenir au moins un chiffre", True, "danger", dash.no_update
    
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return "Session expirée. Veuillez vous reconnecter.", True, "danger", '/login'
    
    # Get auth_manager from Flask app context
    try:
        from flask import current_app
        auth_manager = current_app.auth_manager
        
        # Change password
        success = auth_manager.change_password(current_user.username, new_password)
        
        if success:
            logger.info(f"Password changed successfully for user: {current_user.username}")
            return "Mot de passe changé avec succès! Redirection...", True, "success", '/'
        else:
            logger.error(f"Failed to change password for user: {current_user.username}")
            return "Erreur lors du changement de mot de passe", True, "danger", dash.no_update
            
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        return "Erreur lors du changement de mot de passe. Veuillez réessayer.", True, "danger", dash.no_update
