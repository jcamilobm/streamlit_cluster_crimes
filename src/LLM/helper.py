import pandas as pd
import json

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







def unir_json(json_str_1, json_str_2):
    # 1. Cargar cada JSON como diccionario
    data1 = json.loads(json_str_1)
    data2 = json.loads(json_str_2)

    # 2. Insertar el contenido del segundo JSON dentro del primero
    #    Aquí decides en qué clave quieres guardarlo.
    #    Por ejemplo, podrías llamarlo "DistribucionClusters".
    data1["DistribucionClusters"] = data2

    # 3. Convertir el resultado a una cadena JSON
    return data1