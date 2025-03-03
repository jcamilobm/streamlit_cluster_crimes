import streamlit as st
from streamlit import session_state as ss

from src.EDA.data_manager import load_all_data_and_clean

# Importamos el lector de config y la función para cargar datos


st.set_page_config(
    page_title="Inicio: Resultados Clustering",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Main Page")


# Carga de datos y config, todo en una función centralizada
df_crimes , df_pobl , df_geo , config = load_all_data_and_clean()

st.dataframe(df_pobl)


st.dataframe(df_crimes)