import streamlit as st

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# Objetivo:

#  Transformar los datos en un 
#  formatoo adecuado para alimentar los modelos de machine learningg no supervisados.


# 1) Row Preparation (Granularity)
def prepare_rows(df_crimesf, df_poblacion , df_geo):

    num_years = df_crimesf['year'].nunique()

    df_pivot_sin_datos_demograficos = (df_crimesf.pivot_table(index='num_com',
                                            columns='categoria_delito',
                                            aggfunc='size', fill_value=0)
                                            / num_years).reset_index()
   
    df_pivot_con_datos_demograficos = df_pivot_sin_datos_demograficos.merge(
                                                    df_poblacion ,
                                                    how = 'left',
                                                    left_on ='num_com' ,
                                                    right_on = 'cod_comuna' )

    df_pivot_con_datos_demograficos = df_pivot_con_datos_demograficos.merge(
                                                    df_geo[['cod_comuna','nombre_com', 'area']],
                                                    how='left',
                                                    left_on ='num_com' ,
                                                    right_on = 'cod_comuna' )

    df_pivot  = df_pivot_con_datos_demograficos.drop(columns = ['cod_comuna_x','cod_comuna_y'])

    return df_pivot 


# 2) Column Preparation (No null values)
def clean_columns(df_pivot):
    df_pivot = df_pivot.dropna() # aunque esto ya se garantizo con filll_value = 0 en prepare_rows
    return df_pivot


# 3) Feature Engineering (New columns) y/o transformar variables crudas para que representen patrones más útiles para el modelo.
def feature_engineering(df_pivot):
    df_pivot['poblacional_km2'] = df_pivot['personas'] / df_pivot['area']
    df_pivot["manzanas_km2"] = df_pivot["manzanas"] / df_pivot["area"]
    df_pivot = calcular_tasas_por_habitantes(df_pivot)

    

    return df_pivot

def calcular_tasas_por_habitantes(df_pivot):
    crimenes = ['Crimen Organizado', 'Delitos Sexuales',
                'Delitos Violentos', 'Robos y Hurtos', 'Violencia Familiar']
    
    cada_X_habitantes = 1000

    for crimen in crimenes:
        nombre_tasa = crimen.lower().replace(' ', '_') + f'_por_{cada_X_habitantes}hab'
        df_pivot[nombre_tasa] = ((df_pivot[crimen] / df_pivot['personas']) * cada_X_habitantes).round(2)

        nombre_log = nombre_tasa + '_log'
        df_pivot[nombre_log] = np.log1p(df_pivot[nombre_tasa])

    return df_pivot


# 4) Separar identificadores de variables del modelo
# Es decir, el nombre d eal comuna y su id no van en modelo
def split_identifiers(df_pivot):
    columns_to_remove = ['num_com', 'nombre_com']
    df_identifiers = df_pivot[columns_to_remove]
    df_model  = df_pivot.drop(columns=columns_to_remove)
    return df_model , df_identifiers

# Función para aplicar el escalado seleccionado
def scale_data(df, method):
    if method == 'StandardScaler (Z-score)':
        scaler = StandardScaler()
    elif method == 'MinMaxScaler (0-1)':
        scaler = MinMaxScaler()
    
    scaled_data = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return scaled_data

#5) Feature Selection: se hara desde app interactiva

# Funcion osquestadora:
def get_model_data(df_crimesf, df_poblacion , df_geo):

    df_pivot = prepare_rows(df_crimesf, df_poblacion , df_geo)

    df_pivot = clean_columns(df_pivot)

    df_pivot = feature_engineering(df_pivot)

    df_model , df_identifiers =  split_identifiers(df_pivot)

    return df_model , df_identifiers