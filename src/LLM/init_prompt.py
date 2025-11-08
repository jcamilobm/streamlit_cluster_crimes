import streamlit as st

def init_prompt_defaults(session_key_prefix: str = "prompt"):
    """
    🧠 Inicializador de valores por defecto del prompt.
    ---------------------------------------------------
    - Carga los textos base en st.session_state si no existen.
    - No muestra interfaz (solo prepara el estado para otras páginas).
    - Conserva los cambios del usuario durante la sesión.
    """

    # --- Claves del session_state ---
    role_key = f"{session_key_prefix}_role"
    rules_key = f"{session_key_prefix}_rules"
    json_key = f"{session_key_prefix}_json"
    output_key = f"{session_key_prefix}_output"
    combined_key = f"{session_key_prefix}_combined"

    # =====================================================
    # 🧠 Texto base del rol / propósito del modelo
    # =====================================================
    role_text = (
        "Eres un **analista especializado en seguridad pública y operaciones criminales**. "
        "Tu misión es interpretar los resultados de segmentación criminal (clusters) "
        "y traducirlos en **planes tácticos claros y priorizados** para orientar "
        "la toma de decisiones, la planeación operativa y la prevención del delito."
    )

    # =====================================================
    # ⚙️ Reglas y lineamientos de razonamiento
    # =====================================================
    rules_text = (
        "Reglas de análisis y formato:\n"
        "1. Usa únicamente los porcentajes incluidos en `proporciones_por_dimension`.\n"
        "2. No inventes ni estimes valores que no estén explícitamente en el JSON.\n"
        "3. Para cada `cluster_n`, infiere un nombre breve y representativo según sus proporciones internas.\n"
        "4. Cita siempre los porcentajes exactos para cada categoría y dimensión.\n"
        "5. Estructura la respuesta en: Resumen General, Análisis por Cluster, "
        "Recomendaciones Estratégicas, Acciones Prioritarias y Plan Táctico."
    )

    # =====================================================
    # 📦 Descripción de la estructura del JSON
    # =====================================================
    json_text = (
        "El modelo recibe un objeto JSON con las siguientes secciones:\n\n"
        "• **schema**: descripción de las claves "
        "(informacion_modelo, resultados_modelo, comunas, proporciones_por_dimension)\n"
        "• **informacion_modelo**: metadatos del entrenamiento y configuración\n"
        "• **resultados_modelo**: labels_, proporciones_clusters_, métricas_ y linkage_summary_ de sklearn\n"
        "• **comunas**: lista de comunas con su RME, descripción y cluster asignado\n"
        "• **proporciones_por_dimension**: proporciones normalizadas (0–1) para cada cluster_n "
        "en las dimensiones: tipo_delito, arma, momento, edad, movilidad y ubicación."
    )

    # =====================================================
    # 🧾 Formato esperado de salida
    # =====================================================
    output_text = (
        "La respuesta generada debe incluir las siguientes secciones:\n\n"
        "1. **Resumen General:** Panorama general de la criminalidad en la ciudad, "
        "resaltando patrones, tendencias y anomalías según las proporciones por cluster.\n"
        "2. **Análisis por Cluster:** Descripción detallada de cada cluster, su nombre representativo, "
        "comunas asignadas, tipo de delito predominante y factores clave (arma, edad, momento, ubicación, movilidad).\n"
        "3. **Recomendaciones Estratégicas:** Propuestas concretas de intervención, "
        "ya sean operativas o preventivas, alineadas con los resultados observados.\n"
        "4. **Acciones Prioritarias:** Ordenadas según impacto, riesgo y factibilidad en terreno.\n"
        "5. **Plan Táctico por Cluster:** Objetivos operativos, recursos mínimos requeridos, "
        "acciones concretas, tiempo estimado e indicadores esperados."
    )

    # =====================================================
    # 💾 Guardar en session_state si no existen
    # =====================================================
    st.session_state.setdefault(role_key, role_text)
    st.session_state.setdefault(rules_key, rules_text)
    st.session_state.setdefault(json_key, json_text)
    st.session_state.setdefault(output_key, output_text)

    # =====================================================
    # 🔗 Crear prompt combinado completo
    # =====================================================
    combined_text = (
        f"{st.session_state[role_key]}\n\n"
        f"{st.session_state[rules_key]}\n\n"
        f"{st.session_state[json_key]}\n\n"
        f"{st.session_state[output_key]}"
    )
    st.session_state[combined_key] = combined_text

    return st.session_state[combined_key]
