import streamlit as st

st.set_page_config(
    page_title="Ayuda",
    page_icon="❓",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.info('Revisa el alcance de la App', icon="ℹ️")


import streamlit as st

st.write("Contenido de st.secrets:", dict(st.secrets))


