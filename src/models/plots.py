from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show_model_metrics_table(df, title='📊 Comparación de métricas'):
    """
    Renderiza una tabla interactiva con selección de fila única usando AgGrid,
    considerando solo las columnas ['Modelo', 'Clusters', 'Inercia', 'Silhouette Score', 
    'Calinski-Harabasz', 'Davies-Bouldin'] y eliminando duplicados.

    Parámetros:
    - df (pd.DataFrame): DataFrame con las métricas de los modelos.
    - title (str): Título de la tabla.

    Retorna:
    - list: Datos de la fila seleccionada (si existe).
    """
    # Seleccionar solo las columnas de interés
    columnas = ['Modelo', 'Clusters', 'Inercia', 'Silhouette Score', 'Calinski-Harabasz', 'Davies-Bouldin']
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
    max_height = 300 # Altura máxima para evitar espacio en blanco excesivo
    
    # Calcula la altura según el número de filas, pero sin exceder el máximo
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