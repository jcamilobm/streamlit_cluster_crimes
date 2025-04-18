import streamlit as st
import pandas as pd
from src.EDA.data_manager import load_all_data_and_clean
from src.components.DatasetFilterSidebar import DatasetFilterSidebar
from src.models.model_data_preparation import get_model_data, scale_data
from src.models.helper import *
from src.models.plots import *
from src.components.HelpUser import *

from src.LLM.data_manager_llm import *
from src.LLM.api_configuracion import send_llm_request

from src.utils.config_loader import load_config

st.set_page_config(
    page_title="Experimentos modelos",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'results' not in st.session_state:
    st.session_state.results = []

if "deshabilitar_botones_filtros_datos" not in st.session_state:
    st.session_state.deshabilitar_botones_filtros_datos = False

if "deshabilitar_boton_ejecutar_modelo" not in st.session_state:
    st.session_state.deshabilitar_boton_ejecutar_modelo = False

if "deshabilitar_boton_run_many_experiments" not in st.session_state:
    st.session_state.deshabilitar_boton_run_many_experiments = False

#def deshabilitar_filtros():
#    st.session_state.deshabilitar_botones_filtros_datos = True

def deshabilitar_filtros_ejecutar_un_modelo():
    st.session_state.deshabilitar_botones_filtros_datos = True
    st.session_state.deshabilitar_boton_run_many_experiments = True

def deshabilitar_filtros_run_many_experiments():
    st.session_state.deshabilitar_botones_filtros_datos= True 
    st.session_state.deshabilitar_boton_ejecutar_modelo = True
    st.session_state.deshabilitar_boton_run_many_experiments = True

def habilitar_filtros():
    st.session_state.deshabilitar_botones_filtros_datos = False
    st.session_state.deshabilitar_boton_ejecutar_modelo = False
    st.session_state.deshabilitar_boton_run_many_experiments = False
    st.session_state.results = []

config = load_config() 
system_prompt = config["llm"]["system_prompt"]
model_llm = config["llm"]["model"]    


#1. Titulo
st.markdown("""
# ⚔️ **K-means vs. Jerárquico**  
""")



# 2. # Cargar el dataset solo una vez en session state para otras paginas
if 'df_crimes' not in st.session_state:
    df_crimes, df_poblacion, df_geo, df_descripcion_comunas, config = load_all_data_and_clean()

    st.session_state.df_crimes = df_crimes
    st.session_state.df_poblacion = df_poblacion
    st.session_state.df_geo = df_geo
    st.session_state.df_descripcion_comunas = df_descripcion_comunas
    st.session_state.config = config
else:
    df_crimes = st.session_state.df_crimes
    df_poblacion = st.session_state.df_poblacion
    df_geo = st.session_state.df_geo
    df_descripcion_comunas = st.session_state.df_descripcion_comunas
    config = st.session_state.config

 

# 3. Dibujar side y filtrar datos
df_crimesf = DatasetFilterSidebar(df_crimes, st.session_state.deshabilitar_botones_filtros_datos)


# 4) Obtener tabla para los modelos de machine learning

df_model , df_identifiers = get_model_data(df_crimesf, df_poblacion , df_geo)
df_model  = calcular_RME(df_model , solo_rme=False)


show_guia_experimentacion(expandir=True)

with st.expander("Ver Datos completos pivoteados"):
    df_concatenado = pd.concat([ df_identifiers, df_model], axis=1)
    st.dataframe(df_concatenado)


# Variables del modelo
col1, col2 = st.columns([4, 1])

with col1:
    st.subheader('Elige las variables del modelo')

with col2:
  st.button('🔄 Reiniciar', key='reset_test', type="secondary", on_click=habilitar_filtros)
 



# Opciones para la tasa de crímenes
opciones_tasa_crimenes = [
    "Sin tasa",
    "Estandarización indirecta RME",
    "Crimenes por 1000hab",
    "Crimenes por 1000hab log"
]

# Creamos dos columnas
col1, col2 = st.columns(2)

with col1:
    seleccion_tasa = st.radio("Tasa de crimen:", opciones_tasa_crimenes, disabled = st.session_state.deshabilitar_botones_filtros_datos)
    # Definición de columnas según la opción elegida
    if seleccion_tasa == "Sin tasa":
        opciones_crimenes_seleccionada = [
            'Crimen Organizado', 'Delitos Sexuales', 
            'Delitos Violentos', 'Robos y Hurtos', 
            'Violencia Familiar'
        ]
    elif seleccion_tasa == "Estandarización indirecta RME":
       # df_model = calcular_RME(df_model)
       opciones_crimenes_seleccionada = [col for col in df_model.columns if 'RME' in col]
       pass

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
        disabled=st.session_state.deshabilitar_botones_filtros_datos
    )
   # st.write("Columnas restantes seleccionadas:", opciones_restantes_selecionadas)

lista_concatenada = opciones_crimenes_seleccionada + opciones_restantes_selecionadas

# filtrar el modelo
df_model  = df_model[lista_concatenada]

#df_model_scaled = scale_data(df_model, 'RobustScaler')
with st.expander("Ver tabla inicial para el modelo"):
    df_concatenado = pd.concat([ df_identifiers, df_model], axis=1)
    st.dataframe(df_concatenado)

plot_heatmap(df_model)


st.markdown("---")
# Filtros principales (fuera del sidebar)
st.subheader('🔧 Configuración del Modelo')

# Disposición en columnas para mejor organización visual
col1, col2, col3, col4 = st.columns([2, 1.5, 2, 1.5])  # Ajuste del ancho de las columnas

with col1:
    model_type = st.selectbox('Seleccionar modelo:', 
                              ['K-means', 'Clustering Jerárquico'],
                              help="Modelo para agrupar comunas similares.")

with col2:
    n_clusters = st.number_input('Clusters:', 
                                 min_value=2, max_value=6, 
                                 value=3, step=1,
                                 help="Número de grupos de comunas.")

with col3:
    scaling_method = st.selectbox('Método de escalado:', 
                                  ['StandardScaler (Z-score)', 
                                   'MinMaxScaler (0-1)', 
                                   'RobustScaler'],
                                  help="StandardScaler: media 0, varianza 1. MinMaxScaler: 0 a 1, afectado por outliers. RobustScaler: usa mediana, resistente a outliers.")

with col4:
    # Opciones de distancia según el modelo seleccionado
    distance_options = ['Euclidean']  # K-Means solo usa Euclidean
    if model_type == 'Clustering Jerárquico':
        distance_options.extend(['Manhattan', 'Cosine', 'Correlation'])  # Opciones adicionales para clustering jerárquico

    distance_metric = st.selectbox('Métrica de distancia:', 
                                   distance_options,
                                   help="Euclidean: estándar en clustering. Manhattan: robusto ante outliers. Cosine: para direccionalidad. Correlation: útil si hay relaciones entre crímenes.")



# Aplicar el escalado seleccionado
df_model_scaled = scale_data(df_model, scaling_method)

with st.expander("Ver tabla para el modelo escalada"):
    st.dataframe(df_model_scaled)

#col_run, col_reset = st.columns(2)
#run_model = col_run.button('🚀 Ejecutar Modelo', type="primary", on_click=deshabilitar_filtros_ejecutar_un_modelo, disabled = st.session_state.deshabilitar_boton_ejecutar_modelo)
#run_many_experiments = col_run.button('🚀 Ejecutar varias pruebas', type="primary", on_click=deshabilitar_filtros_run_many_experiments, disabled = st.session_state.deshabilitar_boton_run_many_experiments)
#reset_results = col_reset.button('🗑️ Borrar Resultados', type="secondary", on_click=habilitar_filtros)

col_run, col_run_many, col_reset = st.columns(3)
with col_run:
    run_model = st.button('🚀 Ejecutar Modelo', type="primary", on_click=deshabilitar_filtros_ejecutar_un_modelo, disabled=st.session_state.deshabilitar_boton_ejecutar_modelo)
with col_run_many:
    run_many_experiments = st.button('🔁 Ejecutar varias pruebas', type="primary", on_click=deshabilitar_filtros_run_many_experiments, disabled=st.session_state.deshabilitar_boton_run_many_experiments)

with col_reset:
    reset_results = st.button('🗑️ Borrar Resultados', type="secondary", on_click=habilitar_filtros)


st.markdown("---")

if run_model:
    run_manual_experiment(df_model, model_type, n_clusters, distance_metric, scaling_method)

if run_many_experiments:
    run_all_experiments(df_model)  # Pasa el DataFrame aquí sin escalar.

# Borrar resultados
if reset_results:
    st.session_state.results = []


posFilaSeleccionada = "Sin seleccion de fila"

if st.session_state.results:
    #st.subheader('📊 Resultados Comparativos')

    results_df = pd.DataFrame(st.session_state.results).copy()
    results_df['Inercia'] = pd.to_numeric(results_df['Inercia'], errors='coerce')
    results_df.drop(columns=["Modelo Entrenado", "Labels"],inplace=True)

    # Calcular el score global con normalización ponderada
    df_norm = calculate_score_normalizado(results_df)
   
    # Convertir el dataframe a CSV
    csv_norm = df_norm.to_csv(index=False).encode('utf-8')

    # Crear dos columnas con proporciones 3:1
    col1, col2 = st.columns([3, 1])

    # En la primera columna se muestra el subheader
    col1.subheader('📊 Resultados Comparativos')

    # En la segunda columna se coloca el botón de descarga
    col2.download_button(
        label="Descargar Exp. 📥",
        data=csv_norm,
        file_name='df_norm.csv',
        mime='text/csv'
    )

    ####


    response = show_model_metrics_table(df_norm)
    #response = show_table_with_preselected_row(df_norm, preselect_index=0)
    selected_rows = response.selected_rows
    
  
   # validar si devuelve un dataframe para evitar error
    if isinstance(selected_rows, pd.DataFrame):
       posFilaSeleccionada = int(selected_rows.index[0])
       st.write(selected_rows)
   
   
# Mostrar informacion teorica de como interpretar las metricas encontradas
show_teory_metrics_clustering()


# Input numérico básico
if posFilaSeleccionada != "Sin seleccion de fila" :
    
    
    modelo = st.session_state.results[posFilaSeleccionada]['Modelo']
    model = st.session_state.results[posFilaSeleccionada]['Modelo Entrenado']
    escala = st.session_state.results[posFilaSeleccionada]['Escalado']
    distancia = st.session_state.results[posFilaSeleccionada]['distance_metric']

    n_clusters = st.session_state.results[posFilaSeleccionada]['Clusters']
    labels = st.session_state.results[posFilaSeleccionada]['Labels']
     
    metric_silueta = st.session_state.results[posFilaSeleccionada]['Silhouette Score']


    df_pivot_with_labels = pd.concat([ df_identifiers , pd.Series(labels,name="cluster")],axis=1)
    #st.dataframe(df_pivot_with_labels)
    df_crimes_cluster = df_pivot_with_labels.merge(df_crimesf, on="num_com", how="inner")
    #st.dataframe(df_crimes_cluster

    # end 06/04/2025

    st.markdown("---")
    st.markdown(f"""
    ### Modelo Seleccionado
    - **Modelo:** {modelo}  
    - **Número de Clusters:** {n_clusters}
    - **Escala:** {escala}.  Si escogió RME, la ya no aplica a las categorias de crimenes.
    - **Metodo de Distancia:** {distancia}
    - **Metrica Silueta:** {metric_silueta}
    """)
    col1, col2 = st.columns([1.7, 2])  # Ajuste del ancho de las columnas
    with col1:
        show_labels_frequency_table(labels)
    with col2:
    # preparar datos para mapa
        df_pivot_with_clusters, geojson_data = prepare_geojson_with_clusters(df_identifiers, df_model, labels, df_geo)
        plot_clusters_map(df_pivot_with_clusters , geojson_data)

    if modelo == "K-means":
            plot_heatmap_clusters_kmeans(df_model,model)
    else:
            plot_dendrogram_jerarquico(df_model, n_clusters)
    


    #display_all_grouped_bar_charts(df_crimes_cluster)
  

    #--------------------------------------------------------------------------------
    #  LLM

    # 1)  Organizar JSON para enviar a la API
    dict_results = st.session_state.results[posFilaSeleccionada].copy()
    
    #st.json(dict_results)
    dict_model_info = llm_build_model_info(dict_results["Modelo"], dict_results['Clusters'],  dict_results['distance_metric'] , seleccion_tasa , seleccion_tasa, dict_results['Escalado'])
                                          
    dict_sklearn_model = llm_build_results_sklearn(dict_results, df_model_scaled, model)

    zonas_list = llm_build_zonas_list(df_identifiers, df_model_scaled, df_descripcion_comunas)
    zonas_list_with_clusters = llm_assign_clusters_to_zonas_list(zonas_list, dict_results['Labels'])


    dict_api_prompt_llm =  {
       "informacion_modelo": dict_model_info  ,
       "resultados_modelo": dict_sklearn_model ,
       "comunas": zonas_list_with_clusters
    }

    json_string_prompt_llm   = json.dumps( dict_api_prompt_llm  , indent=4)


    st.markdown("---")

    # Mensaje dinámico indicando el modelo cargado actualmente
    
    help_text = f"Modelo actual cargado: {model_llm}"

    with st.expander("Despliega para ver detalles del prompt"):
            st.write(f"**Modelo lenguaje:** {model_llm}")
            st.write(f"**Prompt del sistema:** {system_prompt}")
            st.json(json_string_prompt_llm)

    if st.button("🤖 Interpretar resultados con IA", type="primary", help=help_text):
        with st.spinner("Cargando respuesta del modelo de lenguaje..."):
            response_text = send_llm_request(json_string_prompt_llm)
            st.write(response_text)
