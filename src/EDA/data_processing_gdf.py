import pandas as pd

############### TABLA DE GEODATAFRAME: COMUNAS #########################
def eda_gdf(gdf):

    gdf['cod_comuna']  = gdf['cod_comuna'].astype(int)

    # Seleccionar columnas a mantener del GEODATAFRAME
    columnas_a_mantener = [ 'nombre_com',
                            'cod_comuna' ,
                             'geometry',

                     ]
    gdf = gdf[columnas_a_mantener]

    return gdf