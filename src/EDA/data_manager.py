import streamlit as st

from pathlib import Path
from src.utils.config_loader import load_config
from src.EDA.load_data import load_data
from src.EDA.data_processing_gdf import eda_gdf
from src.EDA.data_processing_crimes import eda_crimes
from src.EDA.data_processing_poblacion import eda_pobl

# Definir los tipos de datos para las columnas
dtype_crimes = {
    'descripcion_conducta': 'object',
    'armas_medios': 'object',
    'barrios_hecho': 'object',
    'fecha_hecho': 'object',
    'hora_hecho': 'object',
    'edad': 'int64' ,
    'sexo': 'object',
    'movil_victima': 'object',
    'movil_agresor': 'object',
    'clase_sitio': 'object',
    'articulo': 'object',
    'delito_solo': 'object',
    'curso_vida': 'object',
    'curso_vida_orden': 'int64',
    'year_num': 'int64',
    'mes_num': 'int64',
    'dia_num': 'int64',
    'rango_horario': 'object',
    'tipologia': 'object',
    'rango_horario_orden': 'int64',
    'dia_nombre': 'object',
    'dia_nombre_orden': 'int64',
    'localidad': 'object',
    'num_com': 'int64',
    'nom_com': 'object',
    'cantidad_unica': 'int64'
}

@st.cache_data(show_spinner="⌛Cargando tablas...")  
def load_all_data_and_clean(config_path: str = "config/config.yaml"):
    """
    Carga la configuración desde config_path y carga los DataFrames.
    """
    config = load_config(config_path)

    # Cargar rutas sin modificar nada
    crimes_path = config["paths"]["raw_data"]["crimes"]
    population_path = config["paths"]["raw_data"]["population"]
    geolocation_path = config["paths"]["raw_data"]["geolocation"]

    # Cargar los datos directamente
    df_crimes = load_data(crimes_path, dtype_crimes)
    df_crimes = eda_crimes(df_crimes)

    df_geolocation = load_data(geolocation_path)
    df_geolocation = eda_gdf(df_geolocation)

    df_poblacion = load_data(population_path)
    df_poblacion = eda_pobl(df_poblacion)

    return df_crimes, df_poblacion, df_geolocation, config





