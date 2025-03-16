from src.LLM.helper import * 


def llm_build_model_info(tipo_modelo, numero_clusters, metodo_distancia, tipo_frecuencia, escala_crimen, escala_no_crimen):
    """
    Construye un diccionario con la información global del modelo.

    Parámetros:
      tipo_modelo (str): Tipo de modelo utilizado, por ejemplo, "kmeans" o "Clustering Jerárquico".
      numero_clusters (int): Número total de clusters identificados.
      tipo_frecuencia (str): Tipo de frecuencia aplicada a las variables de crimen, por ejemplo, "RME".
      escala_crimen (str): Escala aplicada a las variables de crimen, por ejemplo, "RME".
      escala_no_crimen (str): Escala aplicada a las demás variables, por ejemplo, "min_max".

    Retorna:
      dict: Diccionario con la información del modelo.
    """

    if "RME" not in escala_crimen:
        escala_crimen  =  escala_no_crimen


    return {
        "tipo_modelo": tipo_modelo,
        "numero_clusters": numero_clusters,
        "metodo_distancia":metodo_distancia,
        "tipo_frecuencia": tipo_frecuencia,
        "escala_crimen": escala_crimen,
        "escala_no_crimen": escala_no_crimen,
        "escala_no_crimen_descripcion": "Método de normalización aplicado a las variables no relacionadas con la criminalidad (por ejemplo, población, área,manzanas, etc.)."
    }



# resultados_modelo
def llm_build_results_sklearn(dict_results, df_model_scaled, model):
    """
    Construye un diccionario con los resultados del modelo a partir de dict_results,
    el DataFrame escalado y el modelo entrenado.
    
    Parámetros:
      dict_results: dict
          Diccionario con los resultados del experimento (obtenido de st.session_state.results).
      df_model_scaled: pd.DataFrame
          DataFrame escalado con los datos del modelo.
      model: objeto
          El modelo entrenado (por ejemplo, una instancia de KMeans).
    
    Retorna:
      dict: Diccionario con los resultados agrupados, incluyendo:
            - proporciones_clusters_
            - metricas_
            - labels_
            - clusters_centers_ (si Modelo es "K-means")
            - linkage_summary_ (si Modelo es "Clustering Jerárquico")
    """
    # Crear el diccionario base con proporciones, métricas y etiquetas.
    dict_sklearn_model = {
        "proporciones_clusters_": labels_frequency_dict(dict_results["Labels"]),
        "metricas_": agrupar_metricas(dict_results),
        "labels_": dict_results["Labels"].tolist()
    }

    # Agregar condicionalmente según el modelo
    if dict_results["Modelo"] == "K-means":
        dict_sklearn_model["clusters_centers_"] = cluster_centers_kmeans(df_model_scaled, model)
    
    elif dict_results["Modelo"] == "Clustering Jerárquico":
        dict_sklearn_model["linkage_summary_"] = compute_linkage_summary_jerarquico(df_model_scaled, method='ward')
    
    return dict_sklearn_model