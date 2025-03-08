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

def DatasetFilterSidebar(df, filtro_habilitado=True):
    """Componente de filtro de datos para múltiples páginas en Streamlit."""
    st.sidebar.header(' 🌪️ Filtrar datos')

    with st.sidebar.form(key='filter_data_form', clear_on_submit=False):
        
        # Obtener el rango de años disponibles
        year_min, year_max = df['year'].min(), df['year'].max()

        # Selección del rango de años
        year_rango = st.slider('Selecciona el rango de años', year_min, year_max, (year_min, year_max))

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
        submit = st.form_submit_button('✅ Aplicar filtros', on_click = on_change_filter_data,
                                       disabled = filtro_habilitado)

    #  Mensaje si los filtros están vacíos
    if not filtros_llenos:
        st.sidebar.warning("⚠️ Debes seleccionar al menos un valor en cada filtro.")

    # Filtrar los datos
    filtered_data = filtrar_datos(df, year_rango[0] , year_rango[1],
                                   sexo, movil_victima, curso_vida, 
                                   momento_del_dia, tipo_amenaza)

    return filtered_data



@st.cache_data(show_spinner="⌛ Filtrando datos...")
def filtrar_datos(df, year_inicio, year_fin, sexo, movil_victima, 
                  curso_vida, momento_del_dia, tipo_amenaza):
    return df[
        (df['year'].between(year_inicio, year_fin)) &
        (df['sexo'].isin(sexo)) &
        (df['movil_victima'].isin(movil_victima)) &
        (df['curso_vida'].isin(curso_vida)) &
        (df['momento_del_dia'].isin(momento_del_dia)) &
        (df['tipo_amenaza'].isin(tipo_amenaza))
    ]
