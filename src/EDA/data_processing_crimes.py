import numpy as np
import pandas as pd

from src.EDA.category_papping import (
                                    CRIME_CATEGORY_DICT,
                                    TRANSPORT_MODE_DICT,
                                    WEAPON_THREAT_DICT , 
                                    AGE_GROUP_DICT
)


### Limpieza y transformacion

def assign_time_of_day(hora):
    # Extraemos la hora de inicio del rango de horas
    hora_inicio = int(hora.split('-')[0].split(':')[0])

    # Definir los rangos de momentos del día
    if 0 <= hora_inicio < 6:
        return 'Madrugada'
    elif 6 <= hora_inicio < 12:
        return 'Mañana'
    elif 12 <= hora_inicio < 18:
        return 'Tarde'
    elif 18 <= hora_inicio < 24:  # Asegura que solo valores válidos sean categorizados
      return 'Noche'
    else:
        return 'Hora no válida'
    
def rename_crimes(df):
    # Convertir los nombres de las columnas a minúsculas
    df = df.rename(columns = str.lower)
    # por si la letra ñ despues genera problemas:
    df = df.rename(columns={ 'año_num': 'year',
                            'tipología':'tipologia'})
    return df

def data_processing_dtype_crimes(df):
    df.loc[:, 'fecha_hecho'] = pd.to_datetime(df['fecha_hecho']).dt.date
    df.loc[:, 'hora_hecho'] = pd.to_datetime(df['hora_hecho'], format='%H:%M:%S').dt.strftime('%H:%M')
    df.loc[:, 'edad'] = pd.to_numeric(df['edad'], errors='coerce')
    

    df.loc[:, 'year'] = pd.to_numeric(df['year'], errors='coerce')
    df.loc[:, 'mes_num'] = pd.to_numeric(df['mes_num'], errors='coerce')
    df.loc[:, 'dia_num'] = pd.to_numeric(df['dia_num'], errors='coerce')
    df.loc[:, 'num_com'] = pd.to_numeric(df['num_com'], errors='coerce')

    return df

def handling_missing_data_crimes(df):
    # Imputar la edad con la mediana
    df.loc[:, 'edad'] = df['edad'].fillna(df['edad'].median())

    # Eliminar filas con NaN
    df = df.dropna() 
    return df

def  handling_inconsistent_text(df):
    # Zonas que no se consideraran:
    categorias_a_eliminar = [
        'NO DISPONIBLE',
        'CORREGIMIENTO 1',
        'CORREGIMIENTO 2',
        'CORREGIMIENTO 3'
    ]

    # Eliminar filas con esas categorías
    df = df[~df['localidad'].isin(categorias_a_eliminar)]


    df.loc[:,'movil_victima'] = df['movil_victima'].map(TRANSPORT_MODE_DICT)

    df.loc[:, 'movil_agresor'] = df['movil_agresor'].map(TRANSPORT_MODE_DICT)

    # Definir el orden de las categorías
# Definir el orden de las categorías


    df['curso_vida'] = df['curso_vida'].map(AGE_GROUP_DICT)

    orden_categorico = [
        'Primera Infancia (0-5 años)',
        'Infancia (6-11 años)',
        'Adolescencia (12-18 años)',
        'Juventud (14-26 años)',
        'Adultez (27-59 años)',
        'Persona Mayor (60 años o más)',
        'No disponible'
    ]
    # Convertir la columna en categórica con orden
    df['curso_vida'] = pd.Categorical(df['curso_vida'], 
                                    categories=orden_categorico, ordered=True)

    # Crear la columna de orden numérico
    df['curso_vida_orden'] = df['curso_vida'].cat.codes
    
    return df

def handling_duplicate_rows_crimes(df):
    df = df.drop_duplicates() 
    return df

def handling_missing_numerical_values(df):

    # manejar valores faltantes edad:
    mean_edad = np.mean(df.edad)
    sd_edad= np.std(df.edad)
    [edad for edad in df.edad 
    if (edad < mean_edad-5*sd_edad) or (edad > mean_edad + 5*sd_edad) ]

    # Eliminar valores tipicos en relacion  a la edad
    df = df[~((df.edad < (mean_edad - 4 * sd_edad)) |
               (df.edad > (mean_edad + 4 * sd_edad)))]
    
    return df

def handling_missing_categorical_values(df):

   # Eliminar fila con categorias "movil_victima" poco frecuentes.
   df = df[~df["movil_victima"].isin(["No Disponible",
                                      "Transporte Aéreo",
                                      "Transporte Marítimo"])]
   
   # Eliminar fila con categorias "movil_agresor" poco frecuentes.
   df = df[~df['movil_agresor'].isin(['Transporte Marítimo','Transporte Aéreo'])]

   return df


def create_new_columns_crimes(df):

    df['categoria_delito'] = df['delito_solo'].map(CRIME_CATEGORY_DICT)

    df['momento_del_dia'] = df['rango_horario'].map(lambda x: assign_time_of_day(x))

    df['tipo_amenaza'] = df['armas_medios'].map(WEAPON_THREAT_DICT).fillna("Otros y Sin Información")

    return df

def drop_columns_crimes(df):

    columnas_a_borrar = ['descripcion_conducta' ,
                        'armas_medios' ,
                        'barrios_hecho',
                        'edad',
                        'clase_sitio',
                        'articulo',
                        'delito_solo',
                        'rango_horario',
                        'rango_horario_orden',
                        'cantidad_unica',
                        'tipologia',
                        'localidad'
                     ]
    df = df.drop(columns=columnas_a_borrar, axis=1)
    return df
    

def eda_crimes(df):
    df = rename_crimes(df)
    df = data_processing_dtype_crimes(df)
    df = handling_missing_data_crimes(df)
    df = handling_inconsistent_text(df)
    df = handling_duplicate_rows_crimes(df)
    df = handling_missing_numerical_values(df)
    df = handling_missing_categorical_values(df)
    df = create_new_columns_crimes(df)
    df = drop_columns_crimes(df)


    return df