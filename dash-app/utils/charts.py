"""
Générateurs de graphiques pour le dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_metric_card(title, value, delta=None, prefix="", suffix=""):
    """
    Créer une carte de métrique
    
    Args:
        title (str): Titre de la métrique
        value (float): Valeur de la métrique
        delta (float): Variation (optionnel)
        prefix (str): Préfixe (ex: "$", "€")
        suffix (str): Suffixe (ex: "%", "k")
    """
    fig = go.Figure(go.Indicator(
        mode="number+delta" if delta else "number",
        value=value,
        delta={'reference': delta} if delta else None,
        title={'text': title},
        number={'prefix': prefix, 'suffix': suffix}
    ))
    
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_time_series(df, x, y, title, color=None):
    """
    Créer un graphique de série temporelle
    
    Args:
        df (pandas.DataFrame): Données
        x (str): Colonne pour l'axe X
        y (str): Colonne pour l'axe Y
        title (str): Titre du graphique
        color (str): Colonne pour la couleur
    """
    fig = px.line(df, x=x, y=y, color=color, title=title)
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white'
    )
    return fig


def create_bar_chart(df, x, y, title, orientation='v', color=None):
    """
    Créer un graphique à barres
    
    Args:
        df (pandas.DataFrame): Données
        x (str): Colonne pour l'axe X
        y (str): Colonne pour l'axe Y
        title (str): Titre du graphique
        orientation (str): 'v' pour vertical, 'h' pour horizontal
        color (str): Colonne pour la couleur
    """
    fig = px.bar(df, x=x, y=y, title=title, orientation=orientation, color=color)
    fig.update_layout(template='plotly_white')
    return fig


def create_pie_chart(df, names, values, title):
    """
    Créer un graphique en camembert
    
    Args:
        df (pandas.DataFrame): Données
        names (str): Colonne pour les noms
        values (str): Colonne pour les valeurs
        title (str): Titre du graphique
    """
    fig = px.pie(df, names=names, values=values, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_funnel_chart(stages, values, title):
    """
    Créer un graphique en entonnoir
    
    Args:
        stages (list): Liste des étapes
        values (list): Liste des valeurs
        title (str): Titre du graphique
    """
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(title=title, template='plotly_white')
    return fig


def create_heatmap(df, x, y, z, title):
    """
    Créer une heatmap
    
    Args:
        df (pandas.DataFrame): Données
        x (str): Colonne pour l'axe X
        y (str): Colonne pour l'axe Y
        z (str): Colonne pour les valeurs
        title (str): Titre du graphique
    """
    fig = px.density_heatmap(df, x=x, y=y, z=z, title=title)
    fig.update_layout(template='plotly_white')
    return fig


def create_ab_test_comparison(variant_a_data, variant_b_data, metric_name):
    """
    Créer un graphique de comparaison pour tests A/B
    
    Args:
        variant_a_data (dict): Données pour la variante A
        variant_b_data (dict): Données pour la variante B
        metric_name (str): Nom de la métrique
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Variante A',
        x=[metric_name],
        y=[variant_a_data['value']],
        error_y=dict(type='data', array=[variant_a_data.get('std', 0)])
    ))
    
    fig.add_trace(go.Bar(
        name='Variante B',
        x=[metric_name],
        y=[variant_b_data['value']],
        error_y=dict(type='data', array=[variant_b_data.get('std', 0)])
    ))
    
    fig.update_layout(
        title=f'Comparaison A/B: {metric_name}',
        barmode='group',
        template='plotly_white'
    )
    
    return fig
