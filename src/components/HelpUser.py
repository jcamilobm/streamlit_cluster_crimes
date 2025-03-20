import streamlit as st

import streamlit as st

def show_guia_experimentacion(expandir=False):
    """Muestra la descripción de la página de experimentación en Streamlit.
    
    Args:
        expandir (bool): Si es True, el contenido se mostrará dentro de un st.expander.
    """
    contenido = """

    ### ¿Cómo funciona esta sección?
    1️⃣ **Define la tasa de criminalidad** 
       Elige el criterio de análisis ajustado a la población.  

    2️⃣ **Selecciona variables clave**   
       Incluye factores como el número de manzanas, el área o la densidad poblacional.  

    3️⃣ **Ejecuta pruebas con diferentes modelos**  
       Compara algoritmos como K-Means y clustering jerárquico.  

    4️⃣ **Analiza y elige el mejor modelo** 
       Explora la tabla comparativa y selecciona el más adecuado según métricas clave.  

    5️⃣ **Interpreta patrones y tendencias** 
       Observa cómo se agrupan las zonas de criminalidad y sugiere estrategias basadas en datos.  

    6️⃣ **Obtén insights estratégicos con IA** 🤖  
       Usa la IA para generar recomendaciones basadas en los resultados obtenidos.  
    """

    if expandir:
        with st.expander("ℹ️ Más información sobre la experimentación"):
            st.markdown(contenido, unsafe_allow_html=True)
    else:
        st.markdown(contenido, unsafe_allow_html=True)
