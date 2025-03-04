import streamlit as st

from src.EDA.data_manager import load_all_data_and_clean
from src.components.DatasetFilterSidebar import DatasetFilterSidebar

st.set_page_config(
    page_title="Inicio: Resultados Clustering",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Inicio")


# 1. Carga de datos y config, todo en una función centralizada
df_crimes , df_poblacion , df_geo , config = load_all_data_and_clean()

# 2. # Cargar el dataset solo una vez en session state apra otras paginas
if 'df_crimes' not in st.session_state:
    st.session_state.df_crimes = df_crimes

if 'df_poblacion' not in st.session_state:
    st.session_state.df_poblacion = df_poblacion

if 'df_geo' not in st.session_state:
    st.session_state.df_geo = df_geo

# 3. 
df_crimesf = DatasetFilterSidebar(df_crimes)

st.dataframe(df_crimesf)
st.write(df_crimes.shape)
st.write(df_crimesf.shape)