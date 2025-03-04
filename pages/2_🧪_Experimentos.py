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

df_model = get_model_data(df_crimesf, df_poblacion , df_geo)

st.dataframe(df_model)