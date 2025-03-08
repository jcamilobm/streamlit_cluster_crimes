import streamlit as st
import pandas as pd
from src.EDA.data_manager import load_all_data_and_clean
from src.components.DatasetFilterSidebar import DatasetFilterSidebar
from src.models.model_data_preparation import get_model_data, scale_data
from src.models.helper import calculate_clustering_metrics

from sklearn.cluster import KMeans, AgglomerativeClustering

st.set_page_config(
    page_title="Experimentos modelos",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
df_crimesf = DatasetFilterSidebar(df_crimes)


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
    seleccion = st.radio("Tasa de crimen:", opciones_tasa_crimenes)
    # Definición de columnas según la opción elegida
    if seleccion == "Sin tasa":
        opciones_crimenes_seleccionada = [
            'Crimen Organizado', 'Delitos Sexuales', 
            'Delitos Violentos', 'Robos y Hurtos', 
            'Violencia Familiar'
        ]
    elif seleccion == "Crimenes por 1000hab":
        opciones_crimenes_seleccionada = [col for col in df_model.columns if 'hab' in col and 'log' not in col]
    elif seleccion == "Crimenes por 1000hab log":
        opciones_crimenes_seleccionada = [col for col in df_model.columns if 'log' in col]

    # st.write("Columnas de crímenes seleccionadas:", opciones_crimenes_seleccionada)

with col2:
    opciones_restantes = ["personas", "area", "manzanas", "poblacional_km2"]
    opciones_restantes_selecionadas = st.multiselect(
        'Selecciona otras variables a considerar', 
        options=opciones_restantes,  
        default=opciones_restantes[-2:]
    )
   # st.write("Columnas restantes seleccionadas:", opciones_restantes_selecionadas)

lista_concatenada = opciones_crimenes_seleccionada + opciones_restantes_selecionadas


# filtrar el modelo
df_model  = df_model[lista_concatenada]
with st.expander("Ver tabla para el modelo"):
    st.dataframe(df_model)


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
     

# Botones para ejecutar el modelo y borrar resultados
col_run, col_reset = st.columns(2)
run_model = col_run.button('🚀 Ejecutar Modelo', type="primary")
reset_results = col_reset.button('🗑️ Borrar Resultados', type="secondary")

st.markdown("---")



# Aplicar el escalado seleccionado
df_model_scaled = scale_data(df_model, scaling_method)

if run_model:
    if model_type == 'K-means':
        model = KMeans(n_clusters=n_clusters, random_state=42)
    else:
        model = AgglomerativeClustering(n_clusters=n_clusters)

    labels = model.fit_predict(df_model_scaled)
    metrics = calculate_clustering_metrics(df_model_scaled, labels, model if model_type == 'K-means' else None)