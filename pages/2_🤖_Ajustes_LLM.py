import streamlit as st
from src.utils.config_loader import load_config, update_config
import pandas as pd

st.set_page_config(
    page_title="Ajustes LLM",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

def configuracion_llm(models_llm, system_prompt, modelo_actual):
    st.title("Ajustes LLM")
    st.info('Elige un modelo de lenguaje y modifica el prompt para utilizar en la página de Inicio.', icon="ℹ️")

    # Indicador visual del modelo actual
    st.info(f"**Modelo actual:** `{modelo_actual}`", icon="🤖")

    modelo_llm_new = st.selectbox("Selecciona el modelo de LLM", models_llm)
    system_prompt_new = st.text_area("Prompt del usuario", system_prompt, height=420)

    return modelo_llm_new, system_prompt_new

# Inicializa o recarga configuración desde YAML dinámicamente
if "config" not in st.session_state:
    st.session_state.config = load_config()

config = st.session_state.config
models_llm = config["llm"]["models"]
system_prompt = config["llm"]["system_prompt"]
modelo_actual = config["llm"]["model"]  # Modelo actualmente cargado

modelo_llm_new, system_prompt_new = configuracion_llm(models_llm, system_prompt, modelo_actual)

# Botones para guardar configuración
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Guardar Configuración", type="primary"):
        update_config("llm.model", modelo_llm_new)
        update_config("llm.system_prompt", system_prompt_new)

        st.session_state.config = load_config()

        st.success("Configuración guardada exitosamente.")
        st.rerun()

with col2:
    if st.button("♻️ Restablecer valores por defecto"):
        models_llm_default = config["llm"]["model_default"]
        system_prompt_default = config["llm"]["user_prompt_default"]

        update_config("llm.model", models_llm_default)
        update_config("llm.system_prompt", system_prompt_default)

        st.session_state.config = load_config()

        st.success("Restablecimiento exitoso.")
        st.rerun()




####################


# App Streamlit
st.markdown("---")
# Verifica si ya está en session_state; si no, lo carga
if 'df_descripcion_comunas' not in st.session_state:
    descripcion_comunas_path = "data/raw/comunas_descripcion.xlsx"
    st.session_state.df_descripcion_comunas =  pd.read_excel(descripcion_comunas_path, sheet_name="descripciones_comunas")



st.subheader("Editor de descripciones por comuna ")
# Obtener la copia editable desde session_state
df = st.session_state.df_descripcion_comunas
# Selección de comuna
comuna = st.selectbox("Selecciona la comuna", df['comuna'])

# Mostrar y editar descripción
descripcion_actual = df.loc[df['comuna'] == comuna, 'descripcion'].values[0]
descripcion_editada = st.text_area("Editar descripción", descripcion_actual, height=150)

# Aplicar cambio solo en memoria (session_state)
if st.button("Aplicar cambio",type="primary"):
    df.loc[df['comuna'] == comuna, 'descripcion'] = descripcion_editada
    st.success(f"Descripción actualizada en esta sesión para la comuna: {comuna}")

# Mostrar tabla completa actualizada (solo para el usuario)
st.subheader("Vista previa descripciones comunas:")
st.dataframe(df, use_container_width=True)
