import streamlit as st
from src.EDA.data_manager import load_all_data_and_clean
from src.components.DatasetFilterSidebar import DatasetFilterSidebar
from src.models.model_data_preparation import get_model_data

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

st.dataframe(df_model)
st.dataframe(df_identifiers)



# Filtro para seleccionar columnas
columnas_seleccionadas = st.multiselect(
    'Selecciona las columnas a mostrar', 
    options=df_model.columns,  # Las opciones son las columnas del DataFrame
    default=df_model.columns.tolist()  # Predeterminado: mostrar todas las columnas
)

df_model  = df_model[columnas_seleccionadas]
st.dataframe(df_model)


st.markdown("---")
# Filtros principales (fuera del sidebar)
st.header('🔧 Configuración del Modelo')

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
#df_model_scaled = scale_data(df_model, scaling_method)