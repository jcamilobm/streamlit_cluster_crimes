import streamlit as st
import pandas as pd
import geopandas as gpd


import itertools
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

from sklearn.cluster import KMeans, AgglomerativeClustering

def get_clustering_model(model_type, n_clusters, distance_metric):
    """
    Devuelve una instancia del modelo de clustering según la selección del usuario.

    Parámetros:
    - model_type (str): 'K-means' o 'Clustering Jerárquico'.
    - n_clusters (int): Número de clusters.
    - distance_metric (str): Métrica de distancia seleccionada por el usuario.

    Retorna:
    - Instancia del modelo seleccionado (KMeans o AgglomerativeClustering).
    """
    if model_type == 'K-means':
        return KMeans(n_clusters=n_clusters, random_state=42)

    else:  # Clustering Jerárquico
        metric_method = distance_metric.lower()

        # Configurar el linkage adecuado
        if metric_method == "euclidean":
            linkage_method = "ward"  # Ward solo funciona con Euclidean
        else:
            linkage_method = "average"  # Permite Manhattan, Cosine, Correlation

        # Retornar el modelo
        return AgglomerativeClustering(n_clusters=n_clusters, 
                                       metric=metric_method, 
                                       linkage=linkage_method)


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
    El score global se redondea a 3 decimales.
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



def scale_data(df, method):
    """
    Escala las columnas numéricas de un DataFrame según el método especificado,
    EXCLUYENDO aquellas columnas que contengan "RME" en su nombre.
    Se excluye RME ya que esas columnas ya se escalaron con una normalziacion especal en abse a la poblacion.
    
    Parámetros:
    - df (pd.DataFrame): Datos a escalar.
    - method (str): Método de escalado ('StandardScaler (Z-score)', 'MinMaxScaler (0-1)', 'RobustScaler').
    
    Retorna:
    - pd.DataFrame: DataFrame con las mismas columnas e índice original, donde solo se han escalado 
      las columnas que no contienen "RME".
    """
    
    scalers = {
        'StandardScaler (Z-score)': StandardScaler(),
        'MinMaxScaler (0-1)': MinMaxScaler(),
        'RobustScaler': RobustScaler()
    }

    if method not in scalers:
        raise ValueError(f"❌ Método de escalado '{method}' no reconocido. Usa: {list(scalers.keys())}")

    scaler = scalers[method]
    
    # Determinar las columnas a escalar: aquellas que no contengan "RME"
    columns_to_scale = [col for col in df.columns if "RME" not in col]
    
    # Si no hay columnas para escalar, se retorna el DataFrame original
    if not columns_to_scale:
        return df.copy()
    
    # Escalar únicamente las columnas seleccionadas, manteniendo el índice
    scaled_subset = pd.DataFrame(scaler.fit_transform(df[columns_to_scale]),
                                 columns=columns_to_scale,
                                 index=df.index)
    
    # Crear una copia del DataFrame original
    df_scaled = df.copy()
    # Reemplazar las columnas escaladas en la copia
    for col in columns_to_scale:
        df_scaled[col] = scaled_subset[col]
    
    return df_scaled


def run_manual_experiment(df_model, model_type, n_clusters, distance_metric, scaling_method):
    """
    Ejecuta un experimento manual de clustering y guarda los resultados en `st.session_state.results`.
    
    Parámetros:
    - df_model (pd.DataFrame): Datos a clusterizar.
    - model_type (str): Tipo de modelo ('K-means' o 'Clustering Jerárquico').
    - n_clusters (int): Número de clusters.
    - distance_metric (str): Métrica de distancia.
    - scaling_method (str): Método de escalado ('StandardScaler', 'MinMaxScaler', 'RobustScaler').
    """
    
    # Obtener el modelo según el tipo seleccionado
    model = get_clustering_model(model_type, n_clusters, distance_metric)
    
    # Escalar los datos
    df_model_scaled =  scale_data(df_model, scaling_method)

    # Ejecutar clustering
    labels = model.fit_predict(df_model_scaled)

    # Calcular métricas (si es K-means, se pasa el modelo para calcular inercia)
    metrics = calculate_clustering_metrics(df_model_scaled, labels, model if model_type == 'K-means' else None)

    # Guardar resultados en `st.session_state`
    st.session_state.results.append({
        'Modelo': model_type,
        'Clusters': n_clusters,
        'Escalado': scaling_method,
        'distance_metric': distance_metric,
        'Modelo Entrenado': model,  # Guarda el modelo completo
        'Labels': labels,  # Etiquetas de clusterización
        **metrics  # Agregar métricas de evaluación dinámicamente
    })
    
    st.success("✅ Se ejecutó el clustering manual y se guardó en `st.session_state.results`")



def run_all_experiments(X_df):
    """Ejecuta todas las combinaciones de clustering y almacena los resultados en st.session_state['results'].

    Parámetros:
    - X_df: pd.DataFrame -> Datos reales del usuario en formato DataFrame (sin escalar).
    """

    # Convertir DataFrame a array de numpy
    X = X_df.to_numpy()

    # Definir los valores posibles de cada parámetro
    model_types = ["K-means", "Clustering Jerárquico"]
    n_clusters_options = list(range(3, 6))  # De 2 a 6 clusters
    scaling_methods = ["StandardScaler", "MinMaxScaler", "RobustScaler"]
    distance_metrics = ["Euclidean", "Manhattan", "Cosine", "Correlation"]

    # Inicializar `st.session_state.results` si no existe
    if "results" not in st.session_state:
        st.session_state.results = []

    # Recorrer primero un modelo y luego el otro
    for model_type in model_types:
        # Ajustar métricas de distancia según el modelo seleccionado
        metrics_to_use = ["Euclidean"] if model_type == "K-means" else distance_metrics

        # Generar todas las combinaciones de parámetros
        for n_clusters, scaling_method, distance_metric in itertools.product(n_clusters_options, scaling_methods, metrics_to_use):
            # Aplicar escalado
            scaler = {
                "StandardScaler": StandardScaler(),
                "MinMaxScaler": MinMaxScaler(),
                "RobustScaler": RobustScaler()
            }[scaling_method]
            
            X_scaled = scaler.fit_transform(X)  # Escalar los datos reales

            # Configurar y ejecutar el modelo
            if model_type == "K-means":
                model = KMeans(n_clusters=n_clusters, random_state=42)
                model.fit(X_scaled)  # Ajustar modelo para obtener `inertia_`
                inertia = model.inertia_
                labels = model.predict(X_scaled)
            else:
                linkage_method = "ward" if distance_metric == "Euclidean" else "average"
                model = AgglomerativeClustering(n_clusters=n_clusters, metric=distance_metric.lower(), linkage=linkage_method)
                labels = model.fit_predict(X_scaled)
                inertia = None  # AgglomerativeClustering no tiene `inertia_`

            # Calcular métricas de evaluación
            metrics = {
                "Silhouette Score": silhouette_score(X_scaled, labels),
                "Davies-Bouldin": davies_bouldin_score(X_scaled, labels),
                "Calinski-Harabasz": calinski_harabasz_score(X_scaled, labels)
            }

            # Agregar Inercia solo si el modelo es K-Means
            if inertia is not None:
                metrics["Inercia"] = inertia

            # Guardar resultados en el formato correcto
            st.session_state.results.append({
                "Modelo": model_type,
                "Clusters": n_clusters,
                "Escalado": scaling_method,
                "distance_metric": distance_metric,
                "Modelo Entrenado": model,  # Guardamos el modelo completo
                "Labels": labels,  # Etiquetas del clustering
                **metrics  # Se expanden las métricas dentro del diccionario
            })

    st.success("✅ Se ejecutaron todas las combinaciones y los resultados están guardados en session_state['results']")





import pandas as pd

def calcular_RME(df, 
                 columnas_eventos=['Crimen Organizado', 'Delitos Sexuales', 'Delitos Violentos', 'Robos y Hurtos', 'Violencia Familiar'], 
                 columna_poblacion='personas', 
                 solo_rme=True):
    """
    Calcula la Razón de Morbilidad Estandarizada (RME) para cada columna de eventos.

    Parámetros:
      - df: DataFrame que contiene los datos.
      - columnas_eventos: Lista de nombres de columnas que representan los eventos. 
                          Por defecto: ['Crimen Organizado', 'Delitos Sexuales', 'Delitos Violentos', 'Robos y Hurtos', 'Violencia Familiar'].
      - columna_poblacion: Nombre de la columna que contiene la población. Por defecto: 'personas'.
      - solo_rme: Booleano que, si es True (por defecto), retorna únicamente las columnas que comienzan con "RME_". 
                  Si es False, retorna el DataFrame completo con las columnas adicionales.
    
    Proceso:
      1. Calcula la tasa global para cada evento (total del evento en todas las comunas / población total).
      2. Calcula los casos esperados en cada comuna (población de la comuna * tasa global).
      3. Calcula la RME: Observados / Esperados.
    """
    # Calcular la población total (una sola vez)
    total_population = df[columna_poblacion].sum()
    
    # Iterar sobre cada columna de evento para calcular la RME
    for col in columnas_eventos:
        # a) Calcular la tasa global para el evento
        total_event = df[col].sum()  # Total del evento en todas las comunas
        global_rate = total_event / total_population  # Casos por persona en el conjunto
        
        # b) Calcular los casos esperados en cada comuna para el evento
        df[f'expected_{col}'] = df[columna_poblacion] * global_rate
        
        # c) Calcular la RME: Observados / Esperados
        df[f'RME_{col}'] = df[col] / df[f'expected_{col}']
    
    # Retornar solo las columnas RME si solo_rme es True
    if solo_rme:
        rme_cols = [col for col in df.columns if col.startswith('RME_')]
        return df[rme_cols]
    
    # Si solo_rme es False, retornar el DataFrame completo
    return df
