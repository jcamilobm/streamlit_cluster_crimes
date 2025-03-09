import streamlit as st
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# Función para calcular las métricas de clustering
def calculate_clustering_metrics(df_model, labels, model=None):
    silhouette = silhouette_score(df_model, labels)
    calinski_harabasz = calinski_harabasz_score(df_model, labels)
    davies_bouldin = davies_bouldin_score(df_model, labels)
    inertia = model.inertia_ if model and hasattr(model, 'inertia_') else 'N/A'

    return {
        'Inercia': inertia,
        'Silhouette Score': silhouette,
        'Calinski-Harabasz': calinski_harabasz,
        'Davies-Bouldin': davies_bouldin
    }





def calculate_score_normalizado(df):
    """
    Normaliza las métricas y calcula un score global ponderado,
    omitiendo la métrica de Inercia (aplicable solo a KMeans).

    Se consideran:
    - Métricas donde mayor es mejor: 'Silhouette Score' y 'Calinski-Harabasz'
    - Métricas donde menor es mejor: 'Davies-Bouldin'

    Si alguna métrica es None o NaN, se rellena con la mediana o 0.5 si no hay datos.
    """
    df_norm = df.copy()
    
    # Actualizamos el diccionario de pesos sin incluir Inercia
    pesos = {
        'Silhouette Score': 0.5,
        'Calinski-Harabasz': 0.3,
        'Davies-Bouldin': 0.2
    }
    
    # Listas de métricas según su criterio
    metrics_positive = ['Silhouette Score', 'Calinski-Harabasz']
    metrics_negative = ['Davies-Bouldin']
    
    # Función auxiliar para rellenar valores faltantes
    def fill_missing(col):
        if col.isna().all():
            return col.fillna(0.5)
        else:
            return col.fillna(col.median())
    
    # Normalización para métricas donde mayor es mejor
    for metrica in metrics_positive:
        df_norm[metrica] = pd.to_numeric(df_norm[metrica], errors='coerce')
        df_norm[metrica] = fill_missing(df_norm[metrica])
        min_val = df_norm[metrica].min()
        max_val = df_norm[metrica].max()
        if max_val != min_val:
            df_norm[metrica + '_norm'] = (df_norm[metrica] - min_val) / (max_val - min_val)
        else:
            df_norm[metrica + '_norm'] = 0.5

    # Normalización para métricas donde menor es mejor
    for metrica in metrics_negative:
        df_norm[metrica] = pd.to_numeric(df_norm[metrica], errors='coerce')
        df_norm[metrica] = fill_missing(df_norm[metrica])
        min_val = df_norm[metrica].min()
        max_val = df_norm[metrica].max()
        if max_val != min_val:
            # Invertir la escala: menor valor -> mayor score normalizado
            df_norm[metrica + '_norm'] = 1 - ((df_norm[metrica] - min_val) / (max_val - min_val))
        else:
            df_norm[metrica + '_norm'] = 0.5

    # Calcular el score global combinando las métricas normalizadas
    df_norm['score_global'] = (
        pesos['Silhouette Score'] * df_norm['Silhouette Score_norm'] +
        pesos['Calinski-Harabasz'] * df_norm['Calinski-Harabasz_norm'] +
        pesos['Davies-Bouldin'] * df_norm['Davies-Bouldin_norm']
    )
    return df_norm
