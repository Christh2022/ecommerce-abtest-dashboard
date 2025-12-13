"""
Logout Page for E-Commerce Dashboard
Handles user logout
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user
import logging

dash.register_page(__name__, path='/logout', title='Logout - E-Commerce Dashboard')

logger = logging.getLogger(__name__)


def layout():
    """Logout page layout"""
    
    # Logout the user
    if current_user.is_authenticated:
        username = current_user.username
        logout_user()
        logger.info(f"User logged out: {username}")
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-sign-out-alt fa-3x text-success mb-3"),
                            html.H2("Déconnexion réussie", className="text-white mb-3"),
                            html.P("Vous avez été déconnecté avec succès.", 
                                  className="text-muted mb-4"),
                            dbc.Button(
                                [
                                    html.I(className="fas fa-sign-in-alt me-2"),
                                    "Se reconnecter"
                                ],
                                href="/login",
                                color="primary",
                                size="lg",
                            ),
                        ], className="text-center p-5"),
                    ]),
                ], className="shadow-lg border-0", style={"backgroundColor": "#161b22"}),
            ], width={"size": 6, "offset": 3}, lg={"size": 4, "offset": 4}),
        ], className="min-vh-100 align-items-center"),
        
        # Redirect to login after 2 seconds
        dcc.Interval(id='logout-redirect-timer', interval=2000, n_intervals=0, max_intervals=1),
        dcc.Location(id='logout-redirect', refresh=True),
        
    ], fluid=True, className="bg-dark py-5")


@callback(
    Output('logout-redirect', 'pathname'),
    Input('logout-redirect-timer', 'n_intervals'),
    prevent_initial_call=True
)
def redirect_to_login(n):
    """Redirect to login page after logout"""
    if n is not None and n > 0:
        return '/login'
    return dash.no_update
