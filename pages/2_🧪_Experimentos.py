import streamlit as st
import pandas as pd
from src.EDA.data_manager import load_all_data_and_clean
from src.components.DatasetFilterSidebar import DatasetFilterSidebar
from src.models.model_data_preparation import get_model_data, scale_data
from src.models.helper import calculate_clustering_metrics, calculate_score_normalizado
#from src.models.plots import show_model_metrics_table,show_teory_metrics_clustering, show_labels_frequency_table
from src.models.plots import *
from sklearn.cluster import KMeans, AgglomerativeClustering

st.set_page_config(
    page_title="Experimentos modelos",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'results' not in st.session_state:
    st.session_state.results = []

if "deshabilitar_botones" not in st.session_state:
    st.session_state.deshabilitar_botones = False

def deshabilitar_filtros():
    st.session_state.deshabilitar_botones = True

def habilitar_filtros():
    st.session_state.deshabilitar_botones = False

#1. Titulo
st.markdown("""
# ⚔️ **K-means vs. Jerárquico**  
""")



# 2. # Cargar el dataset solo una vez en session state para otras paginas
if 'df_crimes' not in st.session_state:
    df_crimes , df_poblacion , df_geo , config = load_all_data_and_clean()
    
else:
    df_crimes = st.session_state.df_crimes
    df_poblacion = st.session_state.df_poblacion
    df_geo = st.session_state.df_geo

# 3. Dibujar side y filtrar datos
df_crimesf = DatasetFilterSidebar(df_crimes, st.session_state.deshabilitar_botones)


# Obtener tabla para los modelos de machine learning

df_model , df_identifiers = get_model_data(df_crimesf, df_poblacion , df_geo)

with st.expander("Ver Datos completos pivoteados"):
    df_concatenado = pd.concat([ df_identifiers, df_model], axis=1)
    st.dataframe(df_concatenado)


# Variables del modelo
st.subheader('Elige las variables del modelo')
# Opciones para la tasa de crímenes
opciones_tasa_crimenes = [
    "Sin tasa",
    "Crimenes por 1000hab",
    "Crimenes por 1000hab log"
]

# Creamos dos columnas
col1, col2 = st.columns(2)

with col1:
    seleccion_tasa = st.radio("Tasa de crimen:", opciones_tasa_crimenes, disabled=st.session_state.deshabilitar_botones)
    # Definición de columnas según la opción elegida
    if seleccion_tasa == "Sin tasa":
        opciones_crimenes_seleccionada = [
            'Crimen Organizado', 'Delitos Sexuales', 
            'Delitos Violentos', 'Robos y Hurtos', 
            'Violencia Familiar'
        ]
    elif seleccion_tasa  == "Crimenes por 1000hab":
        opciones_crimenes_seleccionada = [col for col in df_model.columns if 'hab' in col and 'log' not in col]
    elif seleccion_tasa == "Crimenes por 1000hab log":
        opciones_crimenes_seleccionada = [col for col in df_model.columns if 'log' in col]

with col2:
    opciones_restantes = ["personas", "area", "manzanas", "poblacional_km2"]
    opciones_restantes_selecionadas = st.multiselect(
        'Selecciona otras variables a considerar', 
        options=opciones_restantes,  
        default=opciones_restantes[-2:],
        disabled=st.session_state.deshabilitar_botones
    )
   # st.write("Columnas restantes seleccionadas:", opciones_restantes_selecionadas)

lista_concatenada = opciones_crimenes_seleccionada + opciones_restantes_selecionadas


# filtrar el modelo
df_model  = df_model[lista_concatenada]

st.markdown("---")
# Filtros principales (fuera del sidebar)
st.subheader('🔧 Configuración del Modelo')

# Disposición en columnas para mejor organización visual
col1, col2, col3 = st.columns(3)

with col1:
    model_type = st.selectbox('Seleccionar modelo:', ['K-means', 'Clustering Jerárquico'],
                              help="Modelo para agrupar comunas similares.")

with col2:
    #n_clusters = st.slider('Número de Clusters:', 2, 10, 3)
    # Selección del número de clusters con un widget interactivo (+ y -)
    n_clusters = st.number_input('Número de Clusters:', min_value=2, max_value=6, value=3, step=1,help="Número de grupos de comunas")


with col3:
    scaling_method = st.selectbox('Método de escalado:', 
                                  ['StandardScaler (Z-score)', 'MinMaxScaler (0-1)', 'RobustScaler'],
                                  help="StandardScaler: media 0, varianza 1. MinMaxScaler: 0 a 1, afectado por outliers. RobustScaler: usa mediana, resistente a outliers.")
     
# Aplicar el escalado seleccionado
df_model_scaled = scale_data(df_model, scaling_method)
with st.expander("Ver tabla para el modelo escalada"):
    st.dataframe(df_model_scaled)

col_run, col_reset = st.columns(2)
run_model = col_run.button('🚀 Ejecutar Modelo', type="primary", on_click=deshabilitar_filtros)
reset_results = col_reset.button('🗑️ Borrar Resultados', type="secondary", on_click=habilitar_filtros)
st.markdown("---")

if run_model:
    if model_type == 'K-means':
        model = KMeans(n_clusters = n_clusters, random_state=42)
    else:
        model = AgglomerativeClustering(n_clusters = n_clusters)

    labels = model.fit_predict(df_model_scaled)
    metrics = calculate_clustering_metrics(df_model_scaled, labels, model if model_type == 'K-means' else None)

        # Guardar resultados dinámicamente
    st.session_state.results.append({
        'Modelo': model_type,
        'Clusters': n_clusters,
        'Escalado': scaling_method,
        'Modelo Entrenado': model,  # Aquí guardamos el modelo completo
        'Labels':labels ,
        **metrics
    })

# Borrar resultados
if reset_results:
    st.session_state.results = []


posFilaSeleccionada = "Sin seleccion de fila"
if st.session_state.results:
    st.subheader('📊 Resultados Comparativos')

    results_df = pd.DataFrame(st.session_state.results)
    results_df['Inercia'] = pd.to_numeric(results_df['Inercia'], errors='coerce')
    results_df.drop(columns=["Modelo Entrenado", "Labels"],inplace=True)

    # Calcular el score global con normalización ponderada
    df_norm = calculate_score_normalizado(results_df)
 
    response = show_model_metrics_table(df_norm)
    #response = show_table_with_preselected_row(df_norm, preselect_index=0)
    selected_rows = response.selected_rows

   # validar si devuelve un dataframe para evitar error
    if isinstance(selected_rows, pd.DataFrame):
        posFilaSeleccionada = int(selected_rows.index[0])
        st.write(posFilaSeleccionada)
# Mostrar informacion teorica de como interpretar las emtricas encontradas
show_teory_metrics_clustering()


# Input numérico básico
if posFilaSeleccionada != "Sin seleccion de fila" :
       
    modelo = st.session_state.results[posFilaSeleccionada]['Modelo']
    model = st.session_state.results[posFilaSeleccionada]['Modelo Entrenado']
    n_clusters = st.session_state.results[posFilaSeleccionada]['Clusters']
    labels = st.session_state.results[posFilaSeleccionada]['Labels']
    st.markdown(f"""
    ### Modelo Seleccionado
    - **Modelo:** {modelo}  
    - **Número de Clusters:** {n_clusters}
    """)

    show_labels_frequency_table(labels)

    if modelo == "K-means":
        plot_heatmap_clusters_kmeans(df_model,model)
    else:
        plot_dendrogram_jerarquico(df_model, n_clusters)
