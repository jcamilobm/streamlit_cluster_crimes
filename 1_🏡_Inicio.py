import streamlit as st
from streamlit import session_state as ss

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
df_crimes , df_pobl , df_geo , config = load_all_data_and_clean()

# 2. 


# 3. 
df_crimesf = DatasetFilterSidebar(df_crimes)


st.write(df_crimes.shape)
st.write(df_crimesf.shape)