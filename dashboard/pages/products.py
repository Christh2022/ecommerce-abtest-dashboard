"""
Products Page - Top Products and Conversion Analysis
Issue #22 - Top Products + Conversion
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

# Register this page
dash.register_page(__name__, path='/products', name='Produits')

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "clean"

# Load products data
try:
    df_products = pd.read_csv(DATA_DIR / "products_summary.csv")
except FileNotFoundError:
    df_products = None


# Layout
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-box me-3"),
                    "Analyse des Produits"
                ], className="mb-3"),
                html.P(
                    "Découvrez les produits les plus performants et les opportunités d'optimisation "
                    "du catalogue pour maximiser les conversions et le revenue.",
                    className="lead text-muted"
                ),
            ], className="mb-4")
        ])
    ]),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-boxes fa-2x text-primary mb-2"),
                        html.H4("235,061", className="mb-1"),
                        html.P("Produits Total", className="text-muted mb-0 small"),
                        html.Small("94.9% dead stock", className="text-danger"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-star fa-2x text-warning mb-2"),
                        html.H4("11,854", className="mb-1"),
                        html.P("Avec Ventes", className="text-muted mb-0 small"),
                        html.Small("5.1% du catalogue", className="text-warning"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-trophy fa-2x text-success mb-2"),
                        html.H4("2.55%", className="mb-1"),
                        html.P("Top Performers", className="text-muted mb-0 small"),
                        html.Small("Génèrent 80% revenue", className="text-success"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-euro-sign fa-2x text-info mb-2"),
                        html.H4("€255.36", className="mb-1"),
                        html.P("AOV Moyen", className="text-muted mb-0 small"),
                        html.Small("Panier moyen", className="text-info"),
                    ], className="text-center")
                ])
            ], className="shadow-sm h-100 border-0")
        ], width=3),
    ], className="mb-4"),
    
    # Top 20 Products by Revenue
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-medal me-2"),
                        "Top 20 Produits par Revenue"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='top-products-revenue', config={'displayModeBar': True})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Conversion Rates and AOV
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-percentage me-2"),
                        "Taux de Conversion par Produit (Top 30)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='products-conversion', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-shopping-bag me-2"),
                        "Valeur Moyenne Panier (Top 30)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='products-aov', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Pareto Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-line me-2"),
                        "Analyse Pareto: Distribution du Revenue"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='pareto-chart', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Scatter Plot: Conversion vs Traffic
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-scatter me-2"),
                        "Matrice: Trafic vs Conversion (Top 100)"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='scatter-traffic-conversion', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-funnel-dollar me-2"),
                        "Distribution Funnel par Catégorie"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='category-funnel', config={'displayModeBar': False})
                ])
            ], className="shadow-sm border-0 mb-4")
        ], width=6),
    ]),
    
    # Products Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-table me-2"),
                        "Top 50 Produits Détaillés"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='products-table')
                ])
            ], className="shadow-sm border-0 mb-4")
        ])
    ]),
    
    # Insights Section
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H6([
                    html.I(className="fas fa-lightbulb me-2"),
                    "Recommandations Stratégiques"
                ], className="alert-heading mb-3"),
                html.Ul([
                    html.Li("Principe de Pareto vérifié : 2.55% des produits (Top Performers) génèrent 80% du revenue"),
                    html.Li("94.9% du catalogue (223K produits) n'a généré aucune vente - opportunité de nettoyage majeure"),
                    html.Li("Les produits avec taux de conversion élevé manquent souvent de trafic - potentiel marketing"),
                    html.Li("Focus sur les Top 100 produits pour maximiser ROI marketing et optimiser stocks"),
                ], className="mb-0")
            ], color="success", className="border-0")
        ])
    ]),
    
], fluid=True)


# Callbacks
@callback(
    Output('top-products-revenue', 'figure'),
    Input('top-products-revenue', 'id')
)
def update_top_products_revenue(_):
    """Create top products by revenue chart"""
    if df_products is None:
        return go.Figure()
    
    # Top 20 by revenue
    top20 = df_products.nlargest(20, 'total_revenue')
    
    fig = go.Figure()
    
    # Color by category
    colors = {'Top Performer': '#2ecc71', 
              'High Performer': '#3498db',
              'Dead Stock': '#e74c3c'}
    
    bar_colors = [colors.get(cat, '#95a5a6') for cat in top20['category']]
    
    fig.add_trace(go.Bar(
        x=top20['total_revenue'],
        y=[f"Produit {pid}" for pid in top20['product_id']],
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(0,0,0,0.2)', width=1)
        ),
        text=[f"€{val:,.0f}" for val in top20['total_revenue']],
        textposition='outside',
        hovertemplate='<b>Produit %{y}</b><br>' +
                      'Revenue: €%{x:,.2f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Top 20 Produits par Revenue Total",
        xaxis_title="Revenue Total (€)",
        yaxis_title="",
        template='plotly_dark',
        height=600,
        showlegend=False,
        yaxis=dict(autorange="reversed")
    )
    
    return fig


@callback(
    Output('products-conversion', 'figure'),
    Input('products-conversion', 'id')
)
def update_products_conversion(_):
    """Create products conversion rate chart"""
    if df_products is None or len(df_products) == 0:
        return go.Figure().update_layout(
            title="Aucune donnée disponible",
            template='plotly_dark',
            height=500
        )
    
    try:
        # Filter products with purchases and reasonable conversion rates
        df_with_sales = df_products[(df_products['purchases'] > 0) & 
                                    (df_products['view_to_purchase_rate'] < 100) &
                                    (df_products['view_to_purchase_rate'] > 0)].copy()
        
        if len(df_with_sales) == 0:
            return go.Figure().update_layout(
                title="Aucun produit avec conversions",
                template='plotly_dark',
                height=500
            )
        
        # Drop any NaN/inf values
        df_with_sales = df_with_sales.replace([np.inf, -np.inf], np.nan)
        df_with_sales = df_with_sales.dropna(subset=['view_to_purchase_rate', 'total_revenue'])
        
        if len(df_with_sales) == 0:
            return go.Figure().update_layout(
                title="Données invalides",
                template='plotly_dark',
                height=500
            )
        
        # Top 30 by conversion
        top30 = df_with_sales.nlargest(30, 'view_to_purchase_rate')
        
        fig = go.Figure()
        
        # Calculate marker sizes (clip between 10 and 30)
        marker_sizes = (top30['total_revenue'] / 500).clip(10, 30)
        
        fig.add_trace(go.Scatter(
            x=top30['view_to_purchase_rate'],
            y=list(range(len(top30))),
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=top30['view_to_purchase_rate'],
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="Conv. %"),
                line=dict(color='white', width=1)
            ),
            text=[f"Produit {pid}" for pid in top30['product_id']],
            hovertemplate='<b>%{text}</b><br>' +
                          'Conversion: %{x:.2f}%<br>' +
                          '<extra></extra>'
        ))
        
        fig.update_layout(
            title="Taux de Conversion View → Purchase (Top 30)",
            xaxis_title="Taux de Conversion (%)",
            yaxis_title="Rank",
            template='plotly_dark',
            height=500,
            showlegend=False,
            yaxis=dict(showticklabels=False)
        )
        
        return fig
        
    except Exception as e:
        return go.Figure().update_layout(
            title=f"Erreur: {str(e)}",
            template='plotly_dark',
            height=500
        )


@callback(
    Output('products-aov', 'figure'),
    Input('products-aov', 'id')
)
def update_products_aov(_):
    """Create products AOV chart"""
    if df_products is None:
        return go.Figure()
    
    # Top 30 by AOV
    top30 = df_products.nlargest(30, 'avg_price')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f"P{pid}" for pid in top30['product_id']],
        y=top30['avg_price'],
        marker=dict(
            color=top30['avg_price'],
            colorscale='Blues',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.2)', width=1)
        ),
        text=[f"€{val:.0f}" for val in top30['avg_price']],
        textposition='outside',
        hovertemplate='<b>Produit %{x}</b><br>' +
                      'AOV: €%{y:.2f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Valeur Moyenne Panier par Produit (Top 30)",
        xaxis_title="Produit",
        yaxis_title="AOV (€)",
        template='plotly_dark',
        height=500,
        showlegend=False,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


@callback(
    Output('pareto-chart', 'figure'),
    Input('pareto-chart', 'id')
)
def update_pareto_chart(_):
    """Create Pareto analysis chart"""
    if df_products is None or len(df_products) == 0:
        return go.Figure().update_layout(
            title="Aucune donnée disponible",
            template='plotly_dark',
            height=500
        )
    
    try:
        # Filter products with revenue > 0
        df_with_revenue = df_products[df_products['total_revenue'] > 0].copy()
        
        if len(df_with_revenue) == 0:
            return go.Figure().update_layout(
                title="Aucun produit avec revenue",
                template='plotly_dark',
                height=500
            )
        
        # Drop any NaN/inf values
        df_with_revenue = df_with_revenue.replace([np.inf, -np.inf], np.nan)
        df_with_revenue = df_with_revenue.dropna(subset=['total_revenue'])
        
        if len(df_with_revenue) == 0:
            return go.Figure().update_layout(
                title="Données invalides",
                template='plotly_dark',
                height=500
            )
        
        # Sort by revenue and calculate cumulative
        df_sorted = df_with_revenue.sort_values('total_revenue', ascending=False).reset_index(drop=True)
        df_sorted['cumulative_revenue_pct'] = (df_sorted['total_revenue'].cumsum() / df_sorted['total_revenue'].sum()) * 100
        df_sorted['product_pct'] = ((df_sorted.index + 1) / len(df_with_revenue)) * 100
        
        fig = go.Figure()
        
        # Revenue bars
        fig.add_trace(go.Bar(
            x=df_sorted['product_pct'][:100],
            y=df_sorted['total_revenue'][:100],
            name='Revenue',
            marker_color='#3498db',
            yaxis='y',
            opacity=0.6
        ))
        
        # Cumulative line
        fig.add_trace(go.Scatter(
            x=df_sorted['product_pct'],
            y=df_sorted['cumulative_revenue_pct'],
            name='Revenue Cumulé (%)',
            mode='lines',
            line=dict(color='#e74c3c', width=3),
            yaxis='y2'
        ))
        
        # 80% line - add as a shape on y2 axis
        fig.add_shape(
            type="line",
            x0=0, x1=100,
            y0=80, y1=80,
            yref='y2',
            line=dict(color="green", width=2, dash="dash")
        )
        fig.add_annotation(
            x=50, y=80,
            yref='y2',
            text="80% du revenue",
            showarrow=False,
            yshift=10,
            font=dict(color="green")
        )
        
        fig.update_layout(
            title="Analyse Pareto: 2.55% des produits = 80% du revenue",
            xaxis_title="% des Produits",
            yaxis_title="Revenue (€)",
            yaxis2=dict(
                title="Revenue Cumulé (%)",
                overlaying='y',
                side='right',
                range=[0, 100]
            ),
            template='plotly_dark',
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
        
    except Exception as e:
        return go.Figure().update_layout(
            title=f"Erreur: {str(e)}",
            template='plotly_dark',
            height=500
        )


@callback(
    Output('scatter-traffic-conversion', 'figure'),
    Input('scatter-traffic-conversion', 'id')
)
def update_scatter_traffic_conversion(_):
    """Create traffic vs conversion scatter plot"""
    if df_products is None:
        return go.Figure()
    
    # Top 100 products
    top100 = df_products.nlargest(100, 'total_revenue')
    
    fig = px.scatter(
        top100,
        x='unique_users',
        y='view_to_purchase_rate',
        size='total_revenue',
        color='category',
        hover_data={'product_id': True},
        labels={
            'unique_users': 'Utilisateurs Uniques',
            'view_to_purchase_rate': 'Taux de Conversion (%)',
            'category': 'Catégorie'
        },
        color_discrete_map={
            'Top Performer': '#2ecc71',
            'High Performer': '#3498db',
            'Dead Stock': '#e74c3c'
        }
    )
    
    # Add quadrant lines
    median_users = top100['unique_users'].median()
    median_conv = top100['view_to_purchase_rate'].median()
    
    fig.add_vline(x=median_users, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=median_conv, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Matrice Performance: Trafic vs Conversion (Top 100)",
        template='plotly_dark',
        height=500
    )
    
    return fig


@callback(
    Output('category-funnel', 'figure'),
    Input('category-funnel', 'id')
)
def update_category_funnel(_):
    """Create funnel by category"""
    if df_products is None:
        return go.Figure()
    
    # Aggregate by category
    category_stats = df_products.groupby('category').agg({
        'views': 'sum',
        'add_to_carts': 'sum',
        'purchases': 'sum',
        'total_revenue': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    categories = category_stats['category'].tolist()
    colors = {'Top Performer': '#2ecc71', 
              'High Performer': '#3498db',
              'Dead Stock': '#e74c3c'}
    
    for idx, row in category_stats.iterrows():
        fig.add_trace(go.Bar(
            name=row['category'],
            x=['Views', 'Add to Cart', 'Purchases'],
            y=[row['views'], row['add_to_carts'], row['purchases']],
            marker_color=colors.get(row['category'], '#95a5a6'),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         '%{x}: %{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
    
    fig.update_layout(
        title="Distribution du Funnel par Catégorie",
        xaxis_title="Étape du Funnel",
        yaxis_title="Nombre",
        template='plotly_dark',
        height=500,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


@callback(
    Output('products-table', 'children'),
    Input('products-table', 'id')
)
def update_products_table(_):
    """Create products data table"""
    if df_products is None:
        return html.P("Données non disponibles")
    
    # Top 50 products
    top50 = df_products.nlargest(50, 'total_revenue')
    
    # Create table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Rank"),
            html.Th("Produit ID"),
            html.Th("Catégorie"),
            html.Th("Users"),
            html.Th("Views"),
            html.Th("Carts"),
            html.Th("Achats"),
            html.Th("Conv. %"),
            html.Th("Revenue"),
            html.Th("AOV"),
        ]))
    ]
    
    table_body = [html.Tbody([
        html.Tr([
            html.Td(row['rank']),
            html.Td(row['product_id']),
            html.Td(html.Span(row['category'], 
                   className=f"badge bg-{'success' if row['category']=='Top Performer' else 'primary' if row['category']=='High Performer' else 'danger'}")),
            html.Td(f"{row['unique_users']:,.0f}"),
            html.Td(f"{row['views']:,.0f}"),
            html.Td(f"{row['add_to_carts']:,.0f}"),
            html.Td(f"{row['purchases']:,.0f}"),
            html.Td(f"{row['view_to_purchase_rate']:.2f}%"),
            html.Td(f"€{row['total_revenue']:,.2f}"),
            html.Td(f"€{row['avg_price']:.2f}"),
        ]) for idx, row in top50.iterrows()
    ])]
    
    return dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size='sm',
        className='table-sm'
    )
