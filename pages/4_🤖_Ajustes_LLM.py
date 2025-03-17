import streamlit as st
from src.utils.config_loader import load_config, update_config

st.set_page_config(
    page_title="Ajustes LLM",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


import streamlit as st

def configuracion_llm(models_llm,system_prompt):
    st.title("Ajustes LLM")
    st.info('Elije un modelo de lenguaje y modifica el prompt para utilziar en la página de Inicio.', icon="ℹ️")
    
    # Selección del modelo de LLM
   # modelo_llm = st.selectbox("Selecciona el modelo de LLM", ["gpt-4", "gpt-3.5-turbo", "gpt-neo", "otros"])

    modelo_llm_new = st.selectbox("Selecciona el modelo de LLM", models_llm )

    # Definir el prompt base del usuario
    system_prompt_new = st.text_area("Prompt del usuario", system_prompt)
    
    # Sección para gestionar descripciones de comunas
   # st.subheader("Descripciones de las 17 comunas")
   
   # comunas = {}
   # for i in range(1, 18):
   #     comunas[f"Comuna {i}"] = st.text_area(f"Descripción Comuna {i}", "Añade información sobre la comuna...")
    
    # Botón para guardar configuración
    return modelo_llm_new, system_prompt_new
        

if __name__ == "__main__":
  
    config = load_config()
    models_llm = config["llm"]["models"]
    system_prompt = config["llm"]["system_prompt"] 
    modelo_llm_new , system_prompt_new = configuracion_llm(models_llm, system_prompt)

    if st.button("Guardar Configuración"):
      update_config("llm.model", modelo_llm_new )
      update_config("llm.system_prompt", system_prompt_new )
    
      st.success("Configuración guardada exitosamente")

    models_llm_default = config["llm"]["model_default"]
    system_prompt_default = config["llm"]["user_prompt_default"] 
    if st.button("Restablecer valores por defecto"):
      update_config("llm.model", models_llm_default)
      update_config("llm.system_prompt", system_prompt_default  )

      st.rerun()
    
      st.success("Restablecimiento exitoso.")

