import streamlit as st
import pandas as pd
import geopandas as gpd
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
    El score global se redondea a 4 decimales.
    """
    df_norm = df.copy()
    
    # Diccionario de pesos (sin incluir Inercia)
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
    df_norm['score'] = (
        pesos['Silhouette Score'] * df_norm['Silhouette Score_norm'] +
        pesos['Calinski-Harabasz'] * df_norm['Calinski-Harabasz_norm'] +
        pesos['Davies-Bouldin'] * df_norm['Davies-Bouldin_norm']
    )
    # Redondear el score a 4 decimales
    df_norm['score'] = df_norm['score'].round(3)
    
    return df_norm



def prepare_geojson_with_clusters(df_identifiers, df_model, labels, gdf):
    """
    Prepara los datos para visualización en mapa combinando la información de identificadores,
    modelo, y asignación de clusters, y los integra con datos geográficos.

    Parámetros:
      - df_identifiers (pd.DataFrame): DataFrame con identificadores (e.g., num_com).
      - df_model (pd.DataFrame): DataFrame con los datos del modelo.
      - labels (array-like): Etiquetas de cluster asignadas a cada registro.
      - gdf (GeoDataFrame): GeoDataFrame con la columna 'cod_comuna' y la geometría.

    Retorna:
      - df_pivot_with_clusters (pd.DataFrame): DataFrame resultante de unir los identificadores,
          los datos del modelo y los clusters.
      - geojson_data (str): Cadena con el GeoJSON generado a partir de la unión con el GeoDataFrame.
    """
    # Crear una Serie a partir de los labels
    cluster_series = pd.Series(labels, name='cluster')
    
    # Unir los DataFrames de identificadores, modelo y la Serie de clusters
    df_pivot_with_clusters = pd.concat([df_identifiers, df_model, cluster_series], axis=1)
    
    # Unir con el GeoDataFrame utilizando "num_com" y "cod_comuna" (left join)
    df_pivot_clusters_and_geo = df_pivot_with_clusters.merge(
        gdf[['cod_comuna', 'geometry']],
        how="left",
        left_on="num_com",
        right_on="cod_comuna"
    )
    
    # Eliminar columnas duplicadas (si existieran)
    df_pivot_clusters_and_geo.drop(columns=['cod_comuna'], inplace=True)
    
    # Convertir a GeoDataFrame asegurando que la columna 'geometry' es la geometría
    gdf_final = gpd.GeoDataFrame(df_pivot_clusters_and_geo, geometry="geometry")
    
    # Convertir el GeoDataFrame a GeoJSON
    geojson_data = gdf_final.to_json()
    
    return df_pivot_with_clusters, geojson_data

