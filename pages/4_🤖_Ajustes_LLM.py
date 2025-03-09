import streamlit as st

st.set_page_config(
    page_title="Ajustes LLM",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Ajustes LLM")
st.info('Elije un modelo de lenguaje y modifica el prompt para utilziar en la página de Inicio.', icon="ℹ️")