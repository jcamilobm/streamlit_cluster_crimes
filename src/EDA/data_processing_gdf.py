import pandas as pd

############### TABLA DE GEODATAFRAME: COMUNAS #########################
def eda_df_geo(df_geo):

    df_geo['cod_comuna']  = df_geo['cod_comuna'].astype(int)

    # Seleccionar columnas a mantener del GEODATAFRAME
    columnas_a_mantener = [ 'nombre_com',
                            'cod_comuna' ,
                             'geometry',
                             'area'

                     ]
    
    df_geo = df_geo[columnas_a_mantener]

    return df_geo