import streamlit as st
from src.utils.config_loader import load_config, update_config
import pandas as pd
from src.LLM.prompt_editor import prompt_editor

# ============================================================
# 🟢 1️⃣ Configuración de página
# ============================================================
st.set_page_config(
    page_title="Ajustes LLM",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# ⚙️ 2️⃣ Función principal de configuración
# ============================================================
def configuracion_llm(models_llm, modelo_actual):
    st.title("⚙️ Ajustes del Modelo LLM")

    # Indicador visual del modelo actual
    st.info(f"**Modelo actual:** `{modelo_actual}`", icon="🤖")

    # Selectbox que guarda automáticamente el cambio
    modelo_llm_new = st.selectbox(
        "Selecciona el modelo de LLM:",
        models_llm,
        index=models_llm.index(modelo_actual) if modelo_actual in models_llm else 0
    )

    # Guardar automáticamente si cambia
    if modelo_llm_new != modelo_actual:
        update_config("llm.model", modelo_llm_new)
        st.session_state.config = load_config()
        st.toast(f"✅ Modelo actualizado automáticamente a: {modelo_llm_new}")
        st.rerun()

    # ============================================================
    # 🧩 Sección del editor de prompt
    # ============================================================
    st.markdown("---")
    st.subheader("Editor del Prompt")
    st.caption("Puedes ajustar libremente el contenido del prompt en las pestañas siguientes.")

    # Editor visual del prompt
    prompt_editor(session_key_prefix="llm_prompt")


# ============================================================
# 🔄 3️⃣ Cargar configuración desde YAML (solo una vez)
# ============================================================
if "config" not in st.session_state:
    st.session_state.config = load_config()

config = st.session_state.config
models_llm = config["llm"]["models"]
modelo_actual = config["llm"]["model"]

# Ejecutar la función de configuración
configuracion_llm(models_llm, modelo_actual)

# ============================================================
# 📊 4️⃣ Editor de descripciones por comuna
# ============================================================
st.markdown("---")
st.subheader("Descripciones por comuna")

if "df_descripcion_comunas" not in st.session_state:
    descripcion_comunas_path = "data/raw/comunas_descripcion.xlsx"
    st.session_state.df_descripcion_comunas = pd.read_excel(
        descripcion_comunas_path, sheet_name="descripciones_comunas"
    )

df = st.session_state.df_descripcion_comunas

# Selección de comuna
comuna = st.selectbox("Selecciona la comuna:", df["comuna"])

# Mostrar y editar descripción
descripcion_actual = df.loc[df["comuna"] == comuna, "descripcion"].values[0]
descripcion_editada = st.text_area("Editar descripción:", descripcion_actual, height=150)

# Aplicar cambio solo en memoria
if st.button("💾 Aplicar cambio en esta sesión", type="primary"):
    df.loc[df["comuna"] == comuna, "descripcion"] = descripcion_editada
    st.success(f"✅ Descripción actualizada temporalmente para la comuna: {comuna}")

# Vista previa general
st.subheader("📋 Vista previa general:")
st.dataframe(df, use_container_width=True)
