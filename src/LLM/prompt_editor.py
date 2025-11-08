# ============================================================
# 🧩 Componente: Editor de Prompt (único, sin roles)
# ============================================================
import streamlit as st
from src.LLM.init_prompt import init_prompt_defaults


def prompt_editor(session_key_prefix: str = "prompt"):
    """
    🧠 Editor visual del prompt dividido por pestañas.
    -------------------------------------------------
    - Todos los campos son editables.
    - Los cambios se guardan automáticamente o con un botón.
    - Asegura que la vista previa siempre esté actualizada.
    """

    # Inicializar valores base si aún no existen
    init_prompt_defaults(session_key_prefix)

    # --- Claves en session_state ---
    role_key = f"{session_key_prefix}_role"
    rules_key = f"{session_key_prefix}_rules"
    json_key = f"{session_key_prefix}_json"
    output_key = f"{session_key_prefix}_output"
    combined_key = f"{session_key_prefix}_combined"

    # --- Pestañas del editor ---
    tabs = st.tabs([
        "🧠 Rol y propósito",
        "⚙️ Reglas",
        "📦 Estructura JSON",
        "🧾 Formato de salida",
        "🔍 Vista previa"
    ])

    # ============================================================
    # 🧠 Rol y propósito
    # ============================================================
    with tabs[0]:
        st.markdown("### Descripción del rol y propósito del modelo")
        st.session_state[role_key] = st.text_area(
            "Rol y propósito del modelo:",
            value=st.session_state.get(role_key, ""),
            height=160,
            key=f"{role_key}_input"
        )

    # ============================================================
    # ⚙️ Reglas
    # ============================================================
    with tabs[1]:
        st.markdown("### Reglas de razonamiento y formato")
        st.session_state[rules_key] = st.text_area(
            "Reglas de razonamiento y formato:",
            value=st.session_state.get(rules_key, ""),
            height=220,
            key=f"{rules_key}_input"
        )

    # ============================================================
    # 📦 Estructura JSON
    # ============================================================
    with tabs[2]:
        st.markdown("### Estructura del JSON de entrada")
        st.session_state[json_key] = st.text_area(
            "Estructura del JSON de entrada:",
            value=st.session_state.get(json_key, ""),
            height=220,
            key=f"{json_key}_input"
        )

    # ============================================================
    # 🧾 Formato de salida
    # ============================================================
    with tabs[3]:
        st.markdown("###  Formato esperado de salida")
        st.session_state[output_key] = st.text_area(
            "Formato esperado de salida:",
            value=st.session_state.get(output_key, ""),
            height=220,
            key=f"{output_key}_input"
        )

    # ============================================================
    # 🔍 Vista previa
    # ============================================================
    with tabs[4]:
        st.markdown("### Vista previa del prompt completo")

        # 🔘 Botón para forzar actualización
        if st.button("🔄 Actualizar vista previa"):
            st.session_state[combined_key] = (
                f"{st.session_state[role_key]}\n\n"
                f"{st.session_state[rules_key]}\n\n"
                f"{st.session_state[json_key]}\n\n"
                f"{st.session_state[output_key]}"
            )
            st.success("✅ Vista previa actualizada con éxito.")

        combined_prompt = st.session_state.get(combined_key, "")
        st.text_area(
            "📝 Prompt combinado (solo sesión actual):",
            value=combined_prompt,
            height=420
        )

    return st.session_state[combined_key]
