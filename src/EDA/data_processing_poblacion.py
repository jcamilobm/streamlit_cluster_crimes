import pandas as pd


def reaamplazar_coma_en_columnas_numericas(df_poblacion):
    columnas_a_modificar = df_poblacion.columns[6:] # desde personas

    # Reemplazar comas por nada y convertir a numero
    for col in columnas_a_modificar:
        df_poblacion[col] = df_poblacion[col].str.replace(',', '', regex=True)
        df_poblacion[col] = pd.to_numeric(df_poblacion[col] , errors="coerce")
    
    return df_poblacion

def nuevas_columnas(df_poblacion):
    # Separar número y texto directamente con str.extract
    df_poblacion.loc[:,'cod_comuna'] = df_poblacion['Comunas_poligonos'].str.extract(r'(\d+)')
    df_poblacion.loc[:,'Comunas_poligonos'] = df_poblacion['Comunas_poligonos'].str.replace(r'^\d+\. ', '', regex=True).str.strip()

    # Convertir Comuna_id a enteros para que el merge con tabla de hechos no falle
    df_poblacion['cod_comuna'] = pd.to_numeric(df_poblacion['cod_comuna'], errors='coerce')
                                               
    return df_poblacion

def borrar_filas(df_poblacion):
    # Separar número y texto directamente con str.extract
    df_poblacion = (df_poblacion [~df_poblacion ["Comunas_poligonos"]
                    .isin(['CORREG. 1', 'CORREG. 2', 'CORREG. 3'])]
                )

    df_poblacion
                                                
    return df_poblacion

def elegir_columnas(df_poblacion):
    columnas_a_mantener = ['cod_comuna',
                        #'Comunas_poligonos',
                        'manzanas',
                        'personas'
                        ]
    return df_poblacion[columnas_a_mantener]



def agrupar_por_comunas(df_poblacion):
  return df_poblacion.groupby('cod_comuna', as_index=False).sum()



def eda_pobl(df_poblacion):
    df_poblacion = reaamplazar_coma_en_columnas_numericas(df_poblacion)
    df_poblacion = nuevas_columnas(df_poblacion)
    df_poblacion = borrar_filas(df_poblacion)
    df_poblacion = elegir_columnas(df_poblacion)
    df_poblacion = agrupar_por_comunas(df_poblacion)

    return df_poblacion