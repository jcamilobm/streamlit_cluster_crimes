import streamlit as st
import pandas as pd


def on_change_filter_data():
    """
     # se setean resultados metrica en tabla experimentacion
    """
    pass



def multiselect_filter(label, df, column):
    """Función auxiliar para evitar repetición en filtros multiselect."""
    opciones = df[column].dropna().unique().tolist()
    return st.multiselect(label, options=opciones, default=opciones)

def DatasetFilterSidebar(df):
    """Componente de filtro de datos para múltiples páginas en Streamlit."""
    st.sidebar.header(' 🌪️ Filtrar datos')

    with st.sidebar.form(key='filter_data_form', clear_on_submit=False):
        #  Asegurar que 'fecha_hecho' sea dateti
        
        fecha_min, fecha_max = df['fecha_hecho'].min(), df['fecha_hecho'].max()
        fecha_rango = st.date_input('Selecciona el rango', [fecha_min, fecha_max], min_value=fecha_min, max_value=fecha_max)
        fecha_inicio, fecha_fin = fecha_rango if len(fecha_rango) == 2 else (fecha_min, fecha_max)

        #  Características de la víctima
        with st.expander(' Características de la víctima', expanded=False):
            sexo = multiselect_filter('Sexo', df, 'sexo')
            movil_victima = multiselect_filter('Móvil víctima', df, 'movil_victima')
            curso_vida = multiselect_filter('Curso de vida', df, 'curso_vida')

        # Circunstancias del hecho
        with st.expander(' Circunstancias del hecho', expanded=False):
            momento_del_dia = multiselect_filter('Momento del día', df, 'momento_del_dia')
            tipo_amenaza = multiselect_filter('Tipo de amenaza', df, 'tipo_amenaza')

        #  Aplicar filtros
        filtros_llenos = all([sexo, movil_victima, curso_vida, momento_del_dia, tipo_amenaza])
        submit = st.form_submit_button('✅ Aplicar filtros', on_click = on_change_filter_data)

    #  Mensaje si los filtros están vacíos
    if not filtros_llenos:
        st.sidebar.warning("⚠️ Debes seleccionar al menos un valor en cada filtro.")

    # Filtrar los datos
    filtered_data = filtrar_datos(df, fecha_inicio, fecha_fin,
                                   sexo, movil_victima, curso_vida, 
                                   momento_del_dia, tipo_amenaza)

    return filtered_data




# Función para filtrar los datos
# Se cachea para que se ejecute solo si cambia al menos un filtro 
@st.cache_data(show_spinner="⌛Filtrando datos...")
def filtrar_datos(df, fecha_inicio, fecha_fin, sexo, movil_victima, 
                  curso_vida, momento_del_dia, tipo_amenaza):
    #time.sleep(4)
    return df[
        (df['fecha_hecho'] >= fecha_inicio) &
        (df['fecha_hecho'] <= fecha_fin) &
        (df['sexo'].isin(sexo)) &
        (df['movil_victima'].isin(movil_victima)) &
        (df['curso_vida'].isin(curso_vida)) &
        (df['momento_del_dia'].isin(momento_del_dia)) &
        (df['tipo_amenaza'].isin(tipo_amenaza))
    ]