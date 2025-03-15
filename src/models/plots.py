import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from st_aggrid import AgGrid, GridOptionsBuilder

import folium
from folium import Figure
from folium.plugins import Fullscreen
from streamlit_folium import st_folium

def show_model_metrics_table(df, title='📊 Comparación de métricas'):
    """
    Renderiza una tabla interactiva con selección de fila única usando AgGrid,
    considerando las columnas ['Modelo', 'Clusters', 'Inercia', 'Silhouette Score',
    'Calinski-Harabasz', 'Davies-Bouldin', 'score_global'] y eliminando duplicados.
    
    Se renombra la columna 'score_global' a 'Score' para mostrarla en la tabla.
    
    Parámetros:
      - df (pd.DataFrame): DataFrame con las métricas de los modelos, que debe incluir la columna 'score_global'.
      - title (str): Título de la tabla.
    
    Retorna:
      - dict: Datos de la fila seleccionada (si existe).
    """
    # Seleccionar las columnas de interés, incluyendo 'score_global'
    columnas = ['score','Modelo', 'Clusters', 'Inercia', 'Silhouette Score', 'Calinski-Harabasz', 'Davies-Bouldin']
    df_subset = df[columnas].copy()
    
    # Eliminar duplicados basados en las columnas seleccionadas
    df_clean = df_subset.drop_duplicates()
    
    # Configurar AgGrid
    gb = GridOptionsBuilder.from_dataframe(df_clean)
    gb.configure_default_column(
        editable=False,
        filter=True,
        sortable=True,
        resizable=True,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )
    
    # Renombrar la columna 'score_global' a 'Score' en la vista
   # gb.configure_column('score_global', headerName='Score')
    
    # Centrar columnas numéricas, exceptuando la columna 'Modelo'
    for col in columnas:
        if col != 'Modelo' and col in df_clean.columns:
            gb.configure_column(col, cellStyle={'textAlign': 'center'})
    
    # Habilitar selección única de fila con checkbox
    gb.configure_selection('single', use_checkbox=True)
    
    # Construir opciones de la grilla
    grid_options = gb.build()
    
    # Calcular altura dinámica de la tabla
    row_count = max(1, df_clean.shape[0])
    row_height = 60
    min_height = 140
    max_height = 300  # Altura máxima para evitar espacio en blanco excesivo
    calculated_height = min(max_height, max(min_height, row_count * row_height))
    
    # Renderizar la tabla
    response = AgGrid(
        df_clean,
        gridOptions=grid_options,
        theme='streamlit',
        height=calculated_height,
        fit_columns_on_grid_load=True,
        domLayout='autoHeight'
    )
    
    return response






# Función que calcula y dibuja la tabla de frecuencias en Streamlit
def show_labels_frequency_table(labels):
    # Calcular tamaños y porcentajes de cada cluster
    cluster_sizes = pd.Series(labels).value_counts()
    cluster_percentages = pd.Series(labels).value_counts(normalize=True) * 100

    # Crear un DataFrame resumen
    cluster_summary = pd.DataFrame({
        'Cluster': cluster_sizes.index,
        'Tamaño del Clúster': cluster_sizes.values,
        'Peso (%)': cluster_percentages.values.round(2)
    }).sort_values(by='Cluster').reset_index(drop=True)

    # Visualización en Streamlit
    # st.subheader('Tabla de Frecuencias de Clusters')
    st.markdown("""
    Esta tabla muestra el tamaño de cada clúster y su peso porcentual dentro del total.
    """)

    # Mostrar la tabla con formato bonito
    st.dataframe(cluster_summary.style.format({
        'Tamaño del Clúster': '{:,}',
        'Peso (%)': '{:.2f}%'
    }))

    st.markdown("""
     La proporción de los clusters indica si la segmentación es equilibrada y su impacto en el análisis. 
    """)

   



def plot_heatmap_clusters_kmeans(  data , model_kmeans):
  # Graficar un mapa de calor para interpretar los centros de los clusters del algortimo KMEANS
  centroids_df = pd.DataFrame(model_kmeans.cluster_centers_, columns = data.columns)
  plt.figure(figsize=(10, 2))
  sns.heatmap(centroids_df , cmap='RdBu', annot=True , fmt=".2f", linewidths=.5)
      # Mostrar el gráfico en Streamlit
  st.pyplot(plt)

    # Cerrar la figura para evitar que se acumulen
  plt.clf()





from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import numpy as np

def plot_dendrogram_jerarquico(data, num_clusters, method='ward', metric='euclidean', title='Dendrograma'):
    """
    Genera y muestra un dendrograma coloreado para datos utilizando agrupamiento jerárquico.
    Se dibuja una línea horizontal que indica el corte que produce el número deseado de clusters.
    Las ramas se colorean de acuerdo al umbral (cutoff) y, por tanto, al número de clusters.
    
    Parámetros:
      - data (array-like o DataFrame): Datos para el clustering.
      - num_clusters (int): Número deseado de clusters.
      - method (str): Método de enlace ('ward', 'single', 'complete', 'average', etc.).
      - metric (str): Métrica de distancia ('euclidean', 'manhattan', etc.).
      - title (str): Título del gráfico.
      
    Retorna:
      - clusters: Arreglo con la asignación de clusters para cada muestra.
    """
    # Calcular la matriz de enlace
    Z = linkage(data, method=method, metric=metric)
    
    # Obtener la asignación de clusters usando fcluster (criterio 'maxclust')
    clusters = fcluster(Z, num_clusters, criterion='maxclust')
    
    # Para determinar el umbral de corte:
    # Una estrategia simple es ordenar las distancias de fusión y tomar el valor que separa los últimos (num_clusters-1) enlaces.
    distances = Z[:, 2]
    if num_clusters > 1:
        threshold = np.sort(distances)[- (num_clusters - 1)]
    else:
        threshold = 0

    # Crear la figura del dendrograma
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generar el dendrograma utilizando color_threshold para que las ramas cambien de color
    dendrogram(Z, ax=ax, color_threshold=threshold)
    
    # Dibujar una línea horizontal que indica el corte
    ax.axhline(y=threshold, c='red', lw=2, linestyle='dashed', label=f'Corte para {num_clusters} clusters')
    ax.set_title(title)
    ax.set_xlabel('Índice de muestra')
    ax.set_ylabel('Distancia')
    ax.legend()
    
    st.pyplot(fig)
    return clusters




def plot_heatmap(df, title='Heatmap de Correlación'):
    """
    Calcula la matriz de correlación de un DataFrame y muestra un heatmap en Streamlit.
    
    Parámetros:
      - df (pd.DataFrame): DataFrame de entrada.
      - title (str): Título del gráfico.
      
    Retorna:
      - None. Muestra el heatmap en la aplicación Streamlit.
    """
    # Calcular la matriz de correlación
    corr_matrix = df.corr()
    
    # Crear la figura y el eje para el heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Graficar el heatmap con anotaciones y un mapa de colores adecuado
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    
    # Asignar título y mostrar el gráfico
    ax.set_title(title)
    st.pyplot(fig)

    
def show_teory_metrics_clustering():
    col1, col2 = st.columns(2)
    with col1:
      with st.expander('🟢 **Inercia (Suma de distancias)**'):
        st.markdown("""
        - **¿Qué es?**  
          La inercia mide la suma de las distancias al cuadrado desde cada punto a su centroide más cercano.  
        - **¿Cómo interpretarla?**  
          Valores más bajos indican que los puntos están más cerca de sus centroides, lo que sugiere clusters compactos.  
        - **¿Buenos valores?**  
          La inercia **siempre disminuye** al aumentar el número de clusters, así que no tiene un "buen valor absoluto".  
          Se suele usar junto con la **curva del codo** para elegir el número óptimo de clusters.
        """)

      with st.expander('🟠 **Silhouette Score**'):
        st.markdown("""
        - **¿Qué es?**  
          Evalúa cuán similares son los puntos dentro de un cluster comparados con otros clusters.  
          Los valores van de **-1 a 1**:  
          - **1**: Los clusters están bien separados.  
          - **0**: Los clusters se superponen.  
          - **-1**: Los puntos están mal asignados (están más cerca de otro cluster).  
        - **¿Cómo interpretarla?**  
          Un **Silhouette Score cercano a 1** indica que los clusters están bien definidos.  
        - **¿Buenos valores?**  
          Depende del contexto, pero generalmente:  
          - **0.5 a 1**: Buena separación de clusters.  
          - **0 a 0.5**: Clusters algo superpuestos.  
          - **Negativo**: Asignación incorrecta de puntos.
        """)
    with col2 :
      with st.expander('🔵 **Calinski-Harabasz Index**'):
        st.markdown("""
        - **¿Qué es?**  
          Calcula la relación entre la dispersión interna (dentro de los clusters) y la dispersión externa (entre clusters).  
        - **¿Cómo interpretarla?**  
          Valores más altos indican clusters bien definidos y separados entre sí.  
        - **¿Buenos valores?**  
          **Valores más altos son mejores**, pero no hay un umbral absoluto. Se usa para comparar modelos.
        """)

      with st.expander('🔴 **Davies-Bouldin Index**'):
        st.markdown("""
        - **¿Qué es?**  
          Mide la similitud promedio entre cada cluster y el más cercano a él.  
        - **¿Cómo interpretarla?**  
          Valores más bajos indican clusters más distintos entre sí.  
        - **¿Buenos valores?**  
          **0 es el valor óptimo** (clusters completamente separados).  
          **Valores más altos** sugieren que los clusters están solapados.
        """)



def plot_clusters_map(df_pivot_clusters_and_geo, geojson_data):
    # Crear el mapa centrado en Bucaramanga
    fig = Figure(width=150, height=150)
    mapa = folium.Map(location=[7.1254, -73.1198],
                      zoom_start=12,
                      tiles="CartoDB positron",
                      attr="Map tiles by CartoDB")
    fig.add_child(mapa)

    # Paleta de colores para clusters
    palette = {
        0: "#1f77b4", 1: "#ff7f0e", 2: "#2ca02c", 3: "#d62728", 4: "#9467bd",
        5: "#8c564b", 6: "#e377c2", 7: "#7f7f7f", 8: "#bcbd22", 9: "#17becf"
    }

    # Función para colorear las comunas según su cluster
    def style_function(feature):
        cluster = feature["properties"].get("cluster")
        return {"fillColor": palette.get(cluster, "gray"), "color": "black", "weight": 1, "fillOpacity": 0.6}

    # Añadir tooltip con info de cada comuna
    tooltip = folium.GeoJsonTooltip(fields=["nombre_com", "cluster"], aliases=["Comuna:", "Cluster:"])

    # Añadir las comunas al mapa
    folium.GeoJson(
        geojson_data,
        name="Comunas de Bucaramanga",
        style_function=style_function,
        tooltip=tooltip
    ).add_to(mapa)

    # Añadir botón de pantalla completa
    Fullscreen(position="topright").add_to(mapa)

    # Dividir en dos columnas (70% mapa, 30% leyenda)
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st_folium(mapa, width=300, height=330)

    with col2:
        # Obtener clusters únicos para la leyenda
        clusters = sorted(df_pivot_clusters_and_geo["cluster"].unique())

        # Crear tarjetas alineadas con el mapa
        for cluster in clusters:
            color = palette.get(cluster, "gray")
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                    <div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div>
                    <span>Cluster {cluster}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
