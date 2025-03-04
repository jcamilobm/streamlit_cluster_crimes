import streamlit as st

import pandas as pd
from sklearn.preprocessing import StandardScaler



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



def get_model_data(df_crimesf, df_poblacion , df_geo):
    df_pivot = prepare_rows(df_crimesf, df_poblacion , df_geo)

    return df_pivot