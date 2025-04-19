import pandas as pd
import json
import warnings
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import linkage
import numpy as np

def labels_frequency_dict(labels):
    # Convertir a Series y ordenar por el índice (si los clusters son numéricos)
    cluster_sizes = pd.Series(labels).value_counts().sort_index()
    cluster_percentages = pd.Series(labels).value_counts(normalize=True).sort_index() * 100
    
    # Crear un DataFrame resumen
    df_resumen = pd.DataFrame({
        'Cluster': cluster_sizes.index,
        'Tamaño del Clúster': cluster_sizes.values,
        'Peso (%)': cluster_percentages.values.round(2)
    })
    
    # Convertir a lista de diccionarios para una salida JSON amigable
    return df_resumen.to_dict(orient='records')



def agrupar_metricas(dict_results: dict) -> dict:
    """
    Extrae las métricas definidas en 'metric_keys' del diccionario 'dict_results',
    las agrupa en un subdiccionario bajo la clave 'metricas', y elimina las claves originales.
    
    Parámetros:
        dict_results (dict): Diccionario con los resultados, incluyendo las métricas.
    
    Retorna:
        dit.
    """
    metric_keys = [
        "Silhouette Score",
        "Davies-Bouldin",
        "Calinski-Harabasz",
        "Inercia"
    ]
    # Extraer y eliminar las métricas del diccionario original
    metrics = {key: dict_results.pop(key) for key in metric_keys if key in dict_results}
    # Insertar el subdiccionario de métricas
    # dict_results["metricas"] = metrics
    return metrics



def cluster_centers_kmeans(df_model, model):
    """
    Extrae los centros de clúster del modelo KMeans y los convierte en una lista de diccionarios.
    
    Parámetros:
      df_model: pd.DataFrame
          DataFrame original utilizado para entrenar el modelo. Se usan sus columnas como claves.
      model: objeto entrenado de KMeans.
      
    Retorna:
      list: Lista de diccionarios, cada uno representando un centro de clúster.
            Si el modelo no es de tipo KMeans, se emite una advertencia y se retorna una lista vacía.
    """
    # Verificar si el modelo es una instancia de KMeans
    if not isinstance(model, KMeans):
        warnings.warn("El modelo proporcionado no es una instancia de KMeans. No se pueden extraer los centros.")
        return [] 

    # Obtener los nombres de las columnas del DataFrame
    columnas = df_model.columns.tolist()
    
    # Obtener los centros de clúster del modelo
    centers = model.cluster_centers_
    
    # Convertir cada centro en un diccionario usando las columnas como claves
    centers_list = []
    for center in centers:
        center_dict = {col: float(val) for col, val in zip(columnas, center)}
        centers_list.append(center_dict)
    
    return centers_list



def compute_linkage_summary_jerarquico(X_scaled, method='ward'):
    """
    Calcula la matriz de enlace para datos escalados usando el método especificado.
     permite realizar un análisis más profundo y ofrecer interpretaciones y recomendaciones 
     basadas en la estructura jerárquica del clustering.
    
    Parámetros:
      X_scaled: np.ndarray
          Matriz de datos escalados.
      method: str (opcional)
          Método de enlace a utilizar (por ejemplo, 'ward', 'average', 'complete').
          
    Retorna:
      List[Dict]: Una lista de diccionarios, cada uno representando una fusión, con las claves:
          - cluster1: ID del primer cluster fusionado.
          - cluster2: ID del segundo cluster fusionado.
          - distance: Distancia entre los clusters fusionados.
          - sample_count: Número de observaciones en el nuevo cluster.
    """
    # Calcular la matriz de enlace
    Z = linkage(X_scaled, method=method)
    
    # Convertir la matriz de enlace a una lista de diccionarios para facilitar la serialización en JSON
    merge_list = []
    for row in Z:
        merge_dict = {
            "cluster1": int(row[0]),
            "cluster2": int(row[1]),
            "distance": float(row[2]),
            "sample_count": int(row[3])
        }
        merge_list.append(merge_dict)
    
    return merge_list


def llm_build_zonas_list(df_identifiers, df_model_scaled, df_descripcion_comunas):
    """
    Construye la lista de zonas a partir de los DataFrames:
      - df_identifiers: Información identificadora de las zonas.
      - df_model_scaled: Datos del modelo escalados.
      - df_descripcion_comunas: Descripciones de las comunas.
      
    El proceso realiza:
      1. Concatenación de df_identifiers y df_model_scaled.
      2. Merge con df_descripcion_comunas usando "num_com" e "id" como llave.
      3. Eliminación de las columnas 'id' y 'comuna'.
      4. Conversión del DataFrame resultante a una lista de diccionarios.
    
    Retorna:
      list: Una lista de diccionarios, cada uno representando una zona.
    """
    # Concatenar los DataFrames identificadores y los datos escalados
    df = pd.concat([df_identifiers, df_model_scaled], axis=1)
    
    # Hacer merge con las descripciones, usando "num_com" (en df) y "id" (en df_descripcion_comunas)
    df = pd.merge(df, df_descripcion_comunas, how="inner", left_on="num_com", right_on="id")
    
    # Eliminar las columnas que no se desean en el resultado final
    df.drop(["id", "comuna"], axis=1, inplace=True)
    
    # Convertir el DataFrame a lista de diccionarios
    zonas_list = df.to_dict(orient="records")
    
    return zonas_list

def llm_assign_clusters_to_zonas_list(zonas_list, labels):
    """
    Asigna a cada elemento de zonas_list el cluster correspondiente de labels.
    
    Parámetros:
      zonas_list (list): Lista de diccionarios, cada uno representando una zona.
      labels (np.ndarray): Array de NumPy con la asignación de clusters.
      
    Retorna:
      list: La misma lista, con cada diccionario enriquecido con la clave "cluster_asignado".
    """
    # Verificar si el número de zonas coincide con el número de labels
    if len(zonas_list) != len(labels):
        raise ValueError("La cantidad de zonas no coincide con la cantidad de labels.")
    
    for i, zona in enumerate(zonas_list):
        zona["cluster_asignado"] = int(labels[i])
    
    return zonas_list




def llm_calcular_proporciones_por_dimension(
    df: pd.DataFrame,
    cluster_col: str = "cluster",
    dimensiones: list = None
) -> dict:
    """
    Calcula las proporciones normalizadas (0–1) de cada categoría
    para cada dimensión, por cluster.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame que debe incluir una columna con el identificador de cluster
        y una columna por cada dimensión de la que se quieran proporciones.
    cluster_col : str
        Nombre de la columna con las etiquetas de cluster.
    dimensiones : list de str
        Lista de nombres de columna correspondientes a las dimensiones:
        p.ej. ["tipo_delito","arma","momento","edad","movilidad","ubicacion"].
        Si es None, tomará todas las columnas distintas a `cluster_col`.

    Retorna
    -------
    dict
        Estructura:
        {
          "0": { "tipo_delito": {"violencia_intrafamiliar":0.32, ...}, 
                 "arma": {...}, ... },
          "1": { ... },
           …
        }
    """
    if dimensiones is None:
        dimensiones = [c for c in df.columns if c != cluster_col]

    proporciones = {}
    # Agrupamos por cada cluster
    for clust, subdf in df.groupby(cluster_col):
        proporciones[str(clust)] = {}
        # Para cada dimensión calculamos value_counts(normalize=True)
        for dim in dimensiones:
            vc = subdf[dim].value_counts(normalize=True).round(2)
            proporciones[str(clust)][dim] = vc.to_dict()

    return proporciones

# Ejemplo de uso:
# df_crimenes = pd.read_csv("datos_crimenes.csv")
# cols = ["tipo_delito","arma","momento","edad","movilidad","ubicacion"]
# proporciones = calcular_proporciones_por_dimension(df_crimenes, "cluster", cols)
# dict_api_prompt_llm["proporciones_por_dimension"] = proporciones
