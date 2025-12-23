"""
Landing Page Moderne - Site Vitrine
Design moderne responsive avec animations et glassmorphism
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_login import current_user

# Page accessible sans authentification
dash.register_page(__name__, path='/', title='E-Commerce A/B Testing Dashboard - Plateforme d\'Optimisation')


def layout():
    """Modern landing page layout"""
    
    # Si l'utilisateur est déjà connecté, rediriger vers le dashboard
    if current_user.is_authenticated:
        return dcc.Location(pathname='/dashboard', id='redirect-dashboard')
    
    return html.Div([
        # Header Navigation Accessible et Moderne
        html.Header([
            html.Nav([
                dbc.Container([
                    dbc.Row([
                        # Logo et Brand
                        dbc.Col([
                            html.A([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-chart-line fa-2x text-primary")
                                    ], className="logo-icon-circle"),
                                    html.Div([
                                        html.Span("E-Commerce", className="brand-title"),
                                        html.Span("Analytics Platform", className="brand-subtitle")
                                    ], className="brand-text ms-3")
                                ], className="d-flex align-items-center")
                            ], href="/", className="navbar-brand-custom", 
                               title="E-Commerce Analytics - Retour à l'accueil")
                        ], width="auto", className="d-flex align-items-center"),
                        
                        # Navigation Links (Desktop)
                        dbc.Col([
                            html.Ul([
                                html.Li([
                                    html.A("Fonctionnalités", href="#features", 
                                          className="nav-link-custom",
                                          title="Voir les fonctionnalités")
                                ]),
                                html.Li([
                                    html.A("Technologies", href="#technologies", 
                                          className="nav-link-custom",
                                          title="Découvrir les technologies")
                                ]),
                                html.Li([
                                    html.A("Démo", href="#demo", 
                                          className="nav-link-custom",
                                          title="Voir la démo")
                                ]),
                                html.Li([
                                    html.A("Témoignages", href="#testimonials", 
                                          className="nav-link-custom",
                                          title="Lire les témoignages")
                                ]),
                            ], className="nav-menu d-none d-lg-flex", role="menubar")
                        ], className="d-flex justify-content-center flex-grow-1"),
                        
                        # CTA Buttons
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.I(className="fas fa-sign-in-alt me-2", **{"aria-hidden": "true"}),
                                    html.Span("Connexion")
                                ], href="/login", color="primary", size="md", 
                                   className="header-btn-login px-4",
                                   title="Se connecter au dashboard"),
                                dbc.Button([
                                    html.I(className="fas fa-rocket me-2", **{"aria-hidden": "true"}),
                                    html.Span("Démarrer")
                                ], href="/login", outline=True, color="light", size="md", 
                                   className="header-btn-start px-4 ms-2 d-none d-md-inline-block",
                                   title="Démarrer gratuitement")
                            ], className="d-flex align-items-center")
                        ], width="auto", className="d-flex justify-content-end"),
                        
                        # Mobile Menu Toggle
                        dbc.Col([
                            html.Button([
                                html.Span(className="navbar-toggler-icon")
                            ], className="navbar-toggler d-lg-none", 
                               title="Menu de navigation mobile",
                               **{"type": "button", 
                                  "data-bs-toggle": "collapse", 
                                  "data-bs-target": "#mobileMenu",
                                  "aria-controls": "mobileMenu",
                                  "aria-expanded": "false"})
                        ], width="auto", className="d-lg-none")
                    ], className="align-items-center"),
                    
                    # Mobile Menu Collapse
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Ul([
                                    html.Li([
                                        html.A("Fonctionnalités", href="#features", 
                                              className="mobile-nav-link")
                                    ]),
                                    html.Li([
                                        html.A("Technologies", href="#technologies", 
                                              className="mobile-nav-link")
                                    ]),
                                    html.Li([
                                        html.A("Démo", href="#demo", 
                                              className="mobile-nav-link")
                                    ]),
                                    html.Li([
                                        html.A("Témoignages", href="#testimonials", 
                                              className="mobile-nav-link")
                                    ]),
                                ], className="mobile-menu-list")
                            ], className="collapse", id="mobileMenu")
                        ])
                    ], className="d-lg-none")
                ], fluid=True, className="px-4")
            ], **{"role": "navigation"})
        ], className="header-modern position-sticky top-0", style={"zIndex": "1000"}),
        
        # Hero Section avec particules animées
        html.Div([
            # Particles background
            html.Div(className="particles-bg"),
            
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            # Badge animé
                            html.Div([
                                html.Span([
                                    html.I(className="fas fa-bolt me-2"),
                                    "Powered by Python, Dash & PostgreSQL"
                                ], className="badge bg-gradient-badge fs-6 px-4 py-2 pulse-animation")
                            ], className="mb-4 fade-in"),
                            
                            # Main Title avec animation
                            html.H1([
                                "Transformez Vos Données en ",
                                html.Br(),
                                html.Span("Décisions Gagnantes", className="text-gradient animate-gradient")
                            ], className="display-1 fw-bold text-white mb-4 fade-in-up", 
                               style={"lineHeight": "1.1", "letterSpacing": "-2px"}),
                            
                            # Subtitle
                            html.P([
                                "Plateforme complète d'analyse A/B Testing avec ",
                                html.Span("2.7M+ événements", className="text-primary fw-bold"),
                                " analysés, ",
                                html.Span("visualisations en temps réel", className="text-success fw-bold"),
                                " et ",
                                html.Span("sécurité militaire", className="text-warning fw-bold")
                            ], className="lead text-white-50 mb-5 fade-in-up", 
                               style={"fontSize": "1.4rem", "animationDelay": "0.2s", "maxWidth": "800px"}),
                            
                            # CTA Buttons modernes
                            html.Div([
                                dbc.Button([
                                    html.I(className="fas fa-rocket me-2"),
                                    "Démarrer Gratuitement"
                                ], href="/login", size="lg", 
                                   className="btn-gradient me-3 px-5 py-3 shadow-lg hover-lift"),
                                dbc.Button([
                                    html.I(className="fas fa-play-circle me-2"),
                                    "Voir une Démo Live"
                                ], href="#demo", color="outline-light", size="lg", 
                                   className="px-5 py-3 hover-lift")
                            ], className="d-flex gap-3 mb-5 flex-wrap fade-in-up", 
                               style={"animationDelay": "0.4s"}),
                            
                            # Social Proof
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-star text-warning me-1"),
                                    html.I(className="fas fa-star text-warning me-1"),
                                    html.I(className="fas fa-star text-warning me-1"),
                                    html.I(className="fas fa-star text-warning me-1"),
                                    html.I(className="fas fa-star text-warning me-2"),
                                    html.Span("4.9/5", className="text-white fw-bold me-3"),
                                    html.Span("basé sur 127 avis", className="text-white-50 small")
                                ], className="mb-3")
                            ], className="fade-in-up", style={"animationDelay": "0.6s"}),
                            
                            # Stats Row avec glassmorphism
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-users fa-2x text-primary mb-2"),
                                        html.H3("1.65M+", className="text-white fw-bold mb-1 counter"),
                                        html.P("Utilisateurs", className="text-white-50 small mb-0")
                                    ], className="text-center stat-card p-3")
                                ], className="col"),
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-box fa-2x text-success mb-2"),
                                        html.H3("235K+", className="text-white fw-bold mb-1 counter"),
                                        html.P("Produits", className="text-white-50 small mb-0")
                                    ], className="text-center stat-card p-3")
                                ], className="col"),
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-shield-alt fa-2x text-warning mb-2"),
                                        html.H3("41", className="text-white fw-bold mb-1 counter"),
                                        html.P("Tests Sécurité", className="text-white-50 small mb-0")
                                    ], className="text-center stat-card p-3")
                                ], className="col"),
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-lock fa-2x text-danger mb-2"),
                                        html.H3("94.4%", className="text-white fw-bold mb-1 counter"),
                                        html.P("DDoS Block", className="text-white-50 small mb-0")
                                    ], className="text-center stat-card p-3")
                                ], className="col"),
                            ], className="row g-3 glass-card p-4 rounded-4 fade-in-up", 
                               style={"animationDelay": "0.8s"})
                            
                        ], className="py-5")
                    ], lg=12)
                ])
            ], fluid=True, className="py-5 position-relative", style={"zIndex": "1"})
        ], className="hero-section position-relative overflow-hidden"),
        
        # Features Section moderne
        html.Div([
            dbc.Container([
                # Section Title
                html.Div([
                    html.Span("FONCTIONNALITÉS", className="text-primary small fw-bold mb-2 d-block letter-spacing"),
                    html.H2("Tout ce Dont Vous Avez Besoin", 
                           className="text-center text-white display-4 fw-bold mb-3"),
                    html.P("Des outils puissants pour transformer vos données en insights actionnables", 
                           className="text-center text-white-50 lead mb-5 mx-auto", 
                           style={"maxWidth": "700px"})
                ], className="mb-5 section-title"),
                
                # Features Grid moderne
                dbc.Row([
                    # Feature 1
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-chart-line fa-3x mb-3 icon-gradient-1")
                                        ], className="icon-container mb-3"),
                                        html.H4("Analyses Temps Réel", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Visualisez vos KPIs instantanément avec ",
                                            html.Span("12+ dashboards", className="text-primary fw-bold"),
                                            " interactifs. Suivez le trafic et les conversions en direct."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Graphiques Plotly interactifs", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Métriques & tendances quotidiennes", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Segmentation client avancée", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                    
                    # Feature 2
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-vials fa-3x mb-3 icon-gradient-2")
                                        ], className="icon-container mb-3"),
                                        html.H4("Tests A/B Intelligents", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Lancez des expérimentations avec ",
                                            html.Span("16 scénarios", className="text-success fw-bold"),
                                            " pré-configurés. Significativité statistique automatique."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Calculateur taille échantillon", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Tests statistiques (t-test, chi²)", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Visualisations des résultats", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                    
                    # Feature 3
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-funnel-dollar fa-3x mb-3 icon-gradient-3")
                                        ], className="icon-container mb-3"),
                                        html.H4("Analyse de Funnel", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Optimisez chaque étape avec ",
                                            html.Span("417 parcours", className="text-warning fw-bold"),
                                            " analysés. Identifiez les frictions et boostez vos conversions."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Diagramme Sankey interactif", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Taux conversion par étape", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Analyse cohortes & rétention", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                    
                    # Feature 4
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-shield-alt fa-3x mb-3 icon-gradient-4")
                                        ], className="icon-container mb-3"),
                                        html.H4("Sécurité Militaire", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Protection multicouche avec ",
                                            html.Span("41 tests automatisés", className="text-danger fw-bold"),
                                            " et rate limiting anti-DDoS. Monitoring 24/7."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Tests vulnérabilités auto", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Protection DDoS (200 req/min)", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Monitoring Grafana 24/7", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                    
                    # Feature 5
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-brain fa-3x mb-3 icon-gradient-5")
                                        ], className="icon-container mb-3"),
                                        html.H4("IA & Prédictions", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Décisions data-driven avec ",
                                            html.Span("analyses prédictives", className="text-info fw-bold"),
                                            " et recommandations IA basées sur l'historique."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Prévisions de tendances", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Recommandations automatiques", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Tableaux de bord BI", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                    
                    # Feature 6
                    dbc.Col([
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-database fa-3x mb-3 icon-gradient-6")
                                        ], className="icon-container mb-3"),
                                        html.H4("Big Data Réel", className="text-white mb-3 fw-bold"),
                                        html.P([
                                            "Dataset ",
                                            html.Span("RetailRocket", className="text-purple fw-bold"),
                                            " avec 2.7M événements e-commerce sur 139 jours. PostgreSQL optimisé."
                                        ], className="text-white-50 mb-4"),
                                        html.Div([
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("PostgreSQL haute performance", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Queries ultra-rapides (<50ms)", className="text-white-50 small")
                                            ], className="mb-2"),
                                            html.Div([
                                                html.I(className="fas fa-check-circle text-success me-2"),
                                                html.Span("Backup automatique quotidien", className="text-white-50 small")
                                            ])
                                        ])
                                    ])
                                ], className="p-4")
                            ], className="h-100 feature-card bg-card-dark border-0 shadow-xl")
                        ], className="hover-scale")
                    ], md=6, lg=4, className="mb-4"),
                ], className="g-4")
            ], fluid=True, className="py-5")
        ], className="features-section"),
        
        # Technology Stack Section
        html.Div([
            dbc.Container([
                html.Div([
                    html.Span("TECHNOLOGIES", className="text-primary small fw-bold mb-2 d-block letter-spacing"),
                    html.H2("Stack Technologique Moderne", 
                           className="text-center text-white display-4 fw-bold mb-3"),
                    html.P("Technologies éprouvées pour des performances optimales", 
                           className="text-center text-white-50 lead mb-5")
                ], className="mb-5"),
                
                dbc.Row([
                    # Python
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("Python 3.12", className="text-white fw-bold"),
                            html.P("Backend & Analytics", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                    
                    # Dash & Plotly
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://images.plot.ly/logo/new-branding/plotly-logomark.png",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("Dash & Plotly", className="text-white fw-bold"),
                            html.P("Visualizations", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                    
                    # PostgreSQL
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("PostgreSQL 16", className="text-white fw-bold"),
                            html.P("Database", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                    
                    # Docker
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("Docker", className="text-white fw-bold"),
                            html.P("Containers", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                    
                    # Grafana
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/grafana/grafana-original.svg",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("Grafana", className="text-white fw-bold"),
                            html.P("Monitoring", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                    
                    # Prometheus
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Img(src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/prometheus/prometheus-original.svg",
                                        className="tech-logo icon-float",
                                        style={"width": "70px", "height": "70px", "objectFit": "contain"})
                            ], className="icon-circle-large mb-3"),
                            html.H5("Prometheus", className="text-white fw-bold"),
                            html.P("Metrics", className="text-white-50 small")
                        ], className="text-center p-4 tech-card rounded-4 h-100 hover-lift")
                    ], md=6, lg=2, className="mb-3"),
                ])
            ], fluid=True, className="py-5")
        ], className="tech-section"),
        
        # Demo Section avec mockup
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span("DÉMO", className="text-primary small fw-bold mb-2 d-block letter-spacing"),
                            html.H2("Interface Intuitive & Moderne", className="text-white display-5 fw-bold mb-4"),
                            html.P([
                                "Notre dashboard responsive vous permet de naviguer facilement entre ",
                                html.Span("12+ pages d'analyses", className="text-primary fw-bold"),
                                " avec une interface élégante."
                            ], className="text-white-50 lead mb-4"),
                            html.Ul([
                                html.Li([
                                    html.I(className="fas fa-chart-bar text-primary me-2"),
                                    html.Strong("Trafic & Utilisateurs", className="text-white me-2"),
                                    html.Span("Sources et comportements", className="text-white-50")
                                ], className="mb-3"),
                                html.Li([
                                    html.I(className="fas fa-funnel-dollar text-success me-2"),
                                    html.Strong("Conversions & Funnel", className="text-white me-2"),
                                    html.Span("Optimisation du parcours", className="text-white-50")
                                ], className="mb-3"),
                                html.Li([
                                    html.I(className="fas fa-box-open text-warning me-2"),
                                    html.Strong("Catalogue Produits", className="text-white me-2"),
                                    html.Span("Analytics détaillées", className="text-white-50")
                                ], className="mb-3"),
                                html.Li([
                                    html.I(className="fas fa-flask text-info me-2"),
                                    html.Strong("Tests A/B", className="text-white me-2"),
                                    html.Span("Expérimentation complète", className="text-white-50")
                                ], className="mb-3"),
                            ], className="list-unstyled mb-4"),
                            dbc.Button([
                                html.I(className="fas fa-rocket me-2"),
                                "Commencer Maintenant"
                            ], href="/login", size="lg", className="btn-gradient px-5 py-3 shadow-lg hover-lift")
                        ])
                    ], md=6),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-chart-pie fa-5x text-primary mb-4 icon-float"),
                                    html.H4("Dashboard Interactif", className="text-white mb-3 fw-bold"),
                                    html.P("Graphiques dynamiques et filtres temps réel", 
                                           className="text-white-50 mb-4"),
                                    html.Div([
                                        html.Span([
                                            html.I(className="fas fa-play-circle text-primary me-2"),
                                            "Voir la démo vidéo"
                                        ], className="text-white-50 small")
                                    ])
                                ], className="text-center py-5")
                            ], className="mockup-container rounded-4 p-5 shadow-xl h-100 d-flex align-items-center justify-content-center")
                        ])
                    ], md=6)
                ], className="align-items-center")
            ], fluid=True, className="py-5")
        ], className="demo-section", id="demo"),
        
        # Metrics Section avec compteurs animés
        html.Div([
            dbc.Container([
                html.Div([
                    html.H2("Performance & Fiabilité Garanties", 
                           className="text-center text-white display-5 fw-bold mb-5")
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H2("139", className="display-2 text-primary fw-bold mb-0 counter"),
                            html.P("Jours de données", className="text-white-50 fs-5")
                        ], className="text-center metric-box p-4 rounded-4 hover-lift")
                    ], md=6, lg=3, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.H2("2.7M", className="display-2 text-success fw-bold mb-0 counter"),
                            html.P("Événements analysés", className="text-white-50 fs-5")
                        ], className="text-center metric-box p-4 rounded-4 hover-lift")
                    ], md=6, lg=3, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.H2("<50ms", className="display-2 text-warning fw-bold mb-0"),
                            html.P("Temps de réponse", className="text-white-50 fs-5")
                        ], className="text-center metric-box p-4 rounded-4 hover-lift")
                    ], md=6, lg=3, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.H2("99.9%", className="display-2 text-info fw-bold mb-0"),
                            html.P("Uptime garanti", className="text-white-50 fs-5")
                        ], className="text-center metric-box p-4 rounded-4 hover-lift")
                    ], md=6, lg=3, className="mb-4"),
                ])
            ], fluid=True, className="py-5")
        ], className="metrics-section"),
        
        # Testimonials Section
        html.Div([
            dbc.Container([
                html.Div([
                    html.Span("TÉMOIGNAGES", className="text-primary small fw-bold mb-2 d-block letter-spacing"),
                    html.H2("Ce Que Disent Nos Utilisateurs", 
                           className="text-center text-white display-5 fw-bold mb-5")
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                    ], className="mb-3"),
                                    html.P([
                                        "\"La plateforme la plus complète que j'ai utilisée pour l'analyse A/B. ",
                                        "Les visualisations sont superbes et l'interface est très intuitive.\""
                                    ], className="text-white-50 mb-4 fst-italic"),
                                    html.Div([
                                        html.Strong("Sarah M.", className="text-white"),
                                        html.Br(),
                                        html.Small("Head of Growth - TechCorp", className="text-white-50")
                                    ])
                                ])
                            ], className="p-4")
                        ], className="testimonial-card bg-card-dark border-0 shadow-lg h-100 hover-lift")
                    ], md=6, lg=4, className="mb-4"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                    ], className="mb-3"),
                                    html.P([
                                        "\"Les métriques de sécurité et la protection DDoS nous ont permis ",
                                        "de dormir tranquilles. Un outil professionnel de bout en bout.\""
                                    ], className="text-white-50 mb-4 fst-italic"),
                                    html.Div([
                                        html.Strong("Marc D.", className="text-white"),
                                        html.Br(),
                                        html.Small("CTO - E-Commerce Pro", className="text-white-50")
                                    ])
                                ])
                            ], className="p-4")
                        ], className="testimonial-card bg-card-dark border-0 shadow-lg h-100 hover-lift")
                    ], md=6, lg=4, className="mb-4"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                        html.I(className="fas fa-star text-warning"),
                                    ], className="mb-3"),
                                    html.P([
                                        "\"Nous avons augmenté nos conversions de 34% grâce aux insights ",
                                        "fournis par cette plateforme. ROI impressionnant!\""
                                    ], className="text-white-50 mb-4 fst-italic"),
                                    html.Div([
                                        html.Strong("Julie K.", className="text-white"),
                                        html.Br(),
                                        html.Small("Marketing Director - ShopNow", className="text-white-50")
                                    ])
                                ])
                            ], className="p-4")
                        ], className="testimonial-card bg-card-dark border-0 shadow-lg h-100 hover-lift")
                    ], md=6, lg=4, className="mb-4"),
                ])
            ], fluid=True, className="py-5")
        ], className="testimonials-section"),
        
        # CTA Section finale avec gradient
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H2("Prêt à Booster Vos Conversions ?", 
                                   className="text-white display-3 fw-bold mb-4"),
                            html.P("Rejoignez des centaines d'équipes e-commerce qui optimisent leurs tests A/B avec notre plateforme", 
                                   className="text-white-50 lead mb-5", style={"maxWidth": "700px", "margin": "0 auto"}),
                            html.Div([
                                dbc.Button([
                                    html.I(className="fas fa-rocket me-2"),
                                    "Démarrer Gratuitement"
                                ], href="/login", size="lg", 
                                   className="btn-white me-3 px-5 py-3 shadow-lg hover-lift"),
                                dbc.Button([
                                    html.I(className="fab fa-github me-2"),
                                    "Code Source"
                                ], href="https://github.com/Christh2022/ecommerce-abtest-dashboard", 
                                   target="_blank", color="outline-light", size="lg", 
                                   className="px-5 py-3 hover-lift")
                            ], className="d-flex gap-3 justify-content-center flex-wrap"),
                            
                            # Trust badges
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-shield-check text-success me-2 fa-2x"),
                                    html.Span("Sécurisé", className="text-white small")
                                ], className="d-flex align-items-center me-4"),
                                html.Div([
                                    html.I(className="fas fa-clock text-info me-2 fa-2x"),
                                    html.Span("Support 24/7", className="text-white small")
                                ], className="d-flex align-items-center me-4"),
                                html.Div([
                                    html.I(className="fas fa-users text-warning me-2 fa-2x"),
                                    html.Span("127+ Utilisateurs", className="text-white small")
                                ], className="d-flex align-items-center"),
                            ], className="d-flex justify-content-center gap-4 mt-5 flex-wrap")
                        ], className="text-center py-5")
                    ])
                ])
            ], fluid=True)
        ], className="cta-section py-5"),
        
        # Footer moderne
        html.Footer([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H5([
                                html.I(className="fas fa-chart-line me-2 text-primary"),
                                "E-Commerce Analytics"
                            ], className="text-white mb-3 fw-bold"),
                            html.P("Plateforme d'analyse et d'optimisation des tests A/B pour e-commerce", 
                                   className="text-white-50 small mb-3"),
                            html.Div([
                                html.A([html.I(className="fab fa-github fa-lg")], 
                                      href="https://github.com", target="_blank", 
                                      className="text-white-50 me-3 hover-text-primary"),
                                html.A([html.I(className="fab fa-linkedin fa-lg")], 
                                      href="#", className="text-white-50 me-3 hover-text-primary"),
                                html.A([html.I(className="fab fa-twitter fa-lg")], 
                                      href="#", className="text-white-50 hover-text-primary"),
                            ])
                        ])
                    ], md=4),
                    
                    dbc.Col([
                        html.Div([
                            html.H6("Navigation", className="text-white mb-3 fw-bold"),
                            html.Ul([
                                html.Li(html.A("Se Connecter", href="/login", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                                html.Li(html.A("Documentation", href="/methodology", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                                html.Li(html.A("À Propos", href="/about", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                            ], className="list-unstyled")
                        ])
                    ], md=2),
                    
                    dbc.Col([
                        html.Div([
                            html.H6("Fonctionnalités", className="text-white mb-3 fw-bold"),
                            html.Ul([
                                html.Li(html.A("Analytics", href="#features", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                                html.Li(html.A("Tests A/B", href="#features", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                                html.Li(html.A("Sécurité", href="#features", 
                                              className="text-white-50 text-decoration-none hover-text-primary")),
                            ], className="list-unstyled")
                        ])
                    ], md=2),
                    
                    dbc.Col([
                        html.Div([
                            html.H6("Sécurité", className="text-white mb-3 fw-bold"),
                            html.P([
                                html.I(className="fas fa-shield-alt me-2 text-success"),
                                "41 tests automatisés"
                            ], className="text-white-50 small mb-2"),
                            html.P([
                                html.I(className="fas fa-lock me-2 text-success"),
                                "Protection DDoS (94.4%)"
                            ], className="text-white-50 small mb-2"),
                            html.P([
                                html.I(className="fas fa-chart-line me-2 text-success"),
                                "Monitoring 24/7"
                            ], className="text-white-50 small mb-2"),
                        ])
                    ], md=4),
                ]),
                html.Hr(className="border-secondary my-4"),
                dbc.Row([
                    dbc.Col([
                        html.P([
                            "© 2025 E-Commerce Analytics. Powered by ",
                            html.Span("Python", className="text-primary"),
                            ", ",
                            html.Span("Dash", className="text-success"),
                            " & ",
                            html.Span("PostgreSQL", className="text-info")
                        ], className="text-white-50 small mb-0 text-center")
                    ])
                ])
            ], fluid=True, className="py-5")
        ], className="footer-section"),
        
        # Bouton Retour en haut
        html.A([
            html.I(className="fas fa-arrow-up fa-lg")
        ], href="#", className="scroll-to-top", id="scroll-top-btn",
           style={"position": "fixed", "bottom": "30px", "right": "30px", 
                  "width": "50px", "height": "50px", "borderRadius": "50%",
                  "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  "display": "flex", "alignItems": "center", "justifyContent": "center",
                  "color": "white", "fontSize": "20px", "textDecoration": "none",
                  "boxShadow": "0 4px 15px rgba(102, 126, 234, 0.5)",
                  "transition": "all 0.3s ease", "zIndex": "9999",
                  "opacity": "0", "pointerEvents": "none"}),
        
    ], className="landing-modern", style={"backgroundColor": "#0d1117", "overflow": "hidden"})
