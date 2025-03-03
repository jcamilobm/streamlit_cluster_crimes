import streamlit as st
import pandas as pd
import geopandas as gpd
import warnings

from pathlib import Path

from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)


import pandas as pd
import geopandas as gpd
import requests
import io

import pandas as pd
import geopandas as gpd

def load_data(file_path, dtypes=None):
    """
    Carga archivos CSV o GeoJSON desde rutas locales o URLs sin redundancias.
    """
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path, dtype=dtypes)
    elif file_path.endswith(".geojson"):
        return gpd.read_file(file_path)
    else:
        raise ValueError("Formato no soportado. Usa un archivo CSV o GeoJSON.")

