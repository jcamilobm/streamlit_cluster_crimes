# Diccionario con la clasificación mejorada de delitos
# Categorias clustering:

# - 'Robos y Hurtos'
# - 'Violencia Familiar'
# - 'Delitos Sexuales'
#- 'Crimen Organizado'
#- 'Delitos Violentos'

CRIME_CATEGORY_DICT  = {

    # 🟠 Robos y Hurtos (requieren patrullaje intensivo en calles, comercios y viviendas)
    # Separa hurtos comunes de delitos más graves como extorsión.
    'HURTO PERSONAS': 'Robos y Hurtos',
    'HURTO RESIDENCIAS': 'Robos y Hurtos',
    'HURTO MOTOCICLETAS': 'Robos y Hurtos',
    'HURTO AUTOMOTORES': 'Robos y Hurtos',
    'HURTO ENTIDADES COMERCIALES': 'Robos y Hurtos',
    'ABIGEATO': 'Robos y Hurtos',  # Robo de ganado, similar a hurto,
    'DAÑO EN BIEN AJENO': 'Robos y Hurtos',

    # 🟢 Violencia Familiar (requiere protección de víctimas y prevención)
    'VIOLENCIA INTRAFAMILIAR': 'Violencia Familiar',

    # 🟡 Delitos Sexuales (requieren intervención especializada y atención a víctimas)
    # Facilita la persecución de agresores y la protección de víctimas.
    'ACTOS SEXUALES CON MENOR DE 14 AÑOS': 'Delitos Sexuales',
    'ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS': 'Delitos Sexuales',
    'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON INCAPAZ DE RESISTIR': 'Delitos Sexuales',
    'ACCESO CARNAL VIOLENTO': 'Delitos Sexuales',
    'ACOSO SEXUAL': 'Delitos Sexuales',
    'ACTO SEXUAL VIOLENTO': 'Delitos Sexuales',
    'PORNOGRAFÍA CON MENORES': 'Delitos Sexuales',
    'PROXENETISMO CON MENOR DE EDAD': 'Delitos Sexuales',
    'UTILIZACIÓN O FACILITACIÓN DE MEDIOS DE COMUNICACIÓN PARA OFRECER SERVICIOS SEXUALES DE MENORES': 'Delitos Sexuales',
    'INDUCCIÓN A LA PROSTITUCIÓN': 'Delitos Sexuales',
    'CONSTREÑIMIENTO A LA PROSTITUCIÓN': 'Delitos Sexuales',
    'DEMANDA DE EXPLOTACION SEXUAL COMERCIAL DE PERSONA MENOR DE 18 AÑOS DE EDAD': 'Delitos Sexuales',
    'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR (CIRCUNSTANC)': 'Delitos Sexuales',
    'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR': 'Delitos Sexuales',
    'ESTÍMULO A LA PROSTITUCIÓN DE MENORES': 'Delitos Sexuales',
    'ACTOS SEXUALES CON MENOR DE 14 AÑOS (CIRCUNSTANCIAS DE AGRAVACIÓN)': 'Delitos Sexuales',
    'ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS (CIRCUNSTANCIAS AGRAVACIÓN)': 'Delitos Sexuales',
    'ACCESO CARNAL VIOLENTO (CIRCUNSTANCIAS AGRAVACIÓN)': 'Delitos Sexuales',
    'ACTO SEXUAL VIOLENTO (CIRCUNSTANCIAS DE AGRAVACIÓN)': 'Delitos Sexuales',
    'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR  (CIRCUNSTANC': 'Delitos Sexuales',
    'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON INCAPAZ DE RESISTIR (CIRCUNSTANCIAS AGRAVACIÓN)': 'Delitos Sexuales',


    # 🔵 Crimen Organizado (Extorsión, amenazas y delitos de alto impacto)
    # Agrupa delitos que requieren inteligencia policial y operativos tácticos.
    'EXTORSIÓN': 'Crimen Organizado',
    'TERRORISMO': 'Crimen Organizado',
    'AMENAZAS': 'Crimen Organizado',
    'INCENDIO': 'Crimen Organizado',

    # 🔴 Delitos Violentos (requieren patrullaje táctico y operativos de alto impacto)
    # Permite focalizar patrullaje en zonas de alta violencia letal.
    'HOMICIDIO': 'Delitos Violentos',
    'FEMINICIDIO': 'Delitos Violentos',
    'LESIONES PERSONALES': 'Delitos Violentos',
    'LESIONES CULPOSAS': 'Delitos Violentos',
    'HOMICIDIO CULPOSO ( EN ACCIDENTE DE TRÁNSITO)': 'Delitos Violentos',
    'VIOLENCIA CONTRA SERVIDOR PÚBLICO': 'Delitos Violentos',
    'LESIONES AL FETO': 'Delitos Violentos',
    'LESIONES CULPOSAS ( EN ACCIDENTE DE TRANSITO )': 'Delitos Violentos',
}



TRANSPORT_MODE_DICT = {
    "A PIE": "A pie",
    "CONDUCTOR MOTOCICLETA": "Motocicleta",
    "PASAJERO MOTOCICLETA": "Motocicleta",
    "CONDUCTOR VEHICULO": "Vehículo Privado",
    "PASAJERO VEHICULO": "Vehículo Privado",
    "CONDUCTOR TAXI": "Taxi",
    "PASAJERO TAXI": "Taxi",
    "CONDUCTOR BUS": "Bus",
    "PASAJERO BUS": "Bus",
    "PASAJERO METRO": "Metro",
    "BICICLETA": "Bicicleta",
    "PASAJERO AERONAVE": "Transporte Aéreo",
    "PASAJERO BARCO": "Transporte Marítimo",
    "NO DISPONIBLE": "No Disponible"
    }

WEAPON_THREAT_DICT = {
    # Alta prioridad: Riesgo letal, requiere respuesta inmediata
    "ARMA DE FUEGO": "Violencia Letal",
    "ARMA TRAUMATICA": "Violencia Letal",
    "GRANADA DE MANO": "Violencia Letal",
    "PAQUETE BOMBA": "Violencia Letal",
    "ARTEFACTO EXPLOSIVO/CARGA DINAMITA": "Violencia Letal",
    "PAPA EXPLOSIVA": "Violencia Letal",
    "ARMA BLANCA / CORTOPUNZANTE": "Violencia Letal",
    "CORTANTES": "Violencia Letal",
    "PUNZANTES": "Violencia Letal",
    "CONTUNDENTES": "Violencia Letal",
    "CORTOPUNZANTES": "Violencia Letal",

    # Prioridad media: Puede causar daño, pero con menor letalidad
    "ESCOPOLAMINA": "Violencia No Letal",
    "ACIDO": "Violencia No Letal",
    "VENENO": "Violencia No Letal",
    "QUIMICOS": "Violencia No Letal",
    "GASES": "Violencia No Letal",
    "LICOR ADULTERADO": "Violencia No Letal",
    "AGUA CALIENTE": "Violencia No Letal",
    "MEDICAMENTOS": "Violencia No Letal",
    "CUERDA/SOGA/CADENA": "Violencia No Letal",
    "PERRO": "Violencia No Letal",
    "JERINGA": "Violencia No Letal",
    "SUSTANCIAS TOXICAS": "Violencia No Letal",

    # Prevención: Robo y acceso no autorizado
    "LLAVE MAESTRA": "Robo y Acceso Forzado",
    "PALANCAS": "Robo y Acceso Forzado",
    "CARTA EXTORSIVA": "Robo y Acceso Forzado",
    "LLAMADA TELEFONICA": "Robo y Acceso Forzado",
    "REDES SOCIALES": "Robo y Acceso Forzado",
    "VEHICULO": "Robo y Acceso Forzado",
    "MOTO": "Robo y Acceso Forzado",
    "BICICLETA": "Robo y Acceso Forzado",

    # Incendios y explosivos: Pueden causar daños materiales y humanos
    "ARTEFACTO INCENDIARIO": "Incendios y Explosivos",
    "COMBUSTIBLE": "Incendios y Explosivos",
    "ARTEFACTO EXPLOSIVO/CARGA DINAMITA": "Incendios y Explosivos",
    "PAPA EXPLOSIVA": "Incendios y Explosivos",
    "GRANADA DE MANO": "Incendios y Explosivos",
    "PAQUETE BOMBA": "Incendios y Explosivos",

    # Casos sin empleo de armas o sin información clara
    "SIN EMPLEO DE ARMAS": "Sin Empleo de Armas",
    "NO DISPONIBLE": "Sin Empleo de Armas",
    "NO REPORTADO": "Sin Empleo de Armas",
    "DIRECTA": "Sin Empleo de Armas",
    "MIXTA": "Sin Empleo de Armas",
    "PRENDAS DE VESTIR": "Sin Empleo de Armas",
    "BOLSA PLASTICA": "Sin Empleo de Armas"
}


# Fuente: https://www.minsalud.gov.co/proteccionsocial/Paginas/ciclovida.aspx
AGE_GROUP_DICT = {
    '0-4': 'Primera Infancia (0-5 años)',
    '5-9': 'Primera Infancia (0-5 años)',
    '10-14': 'Infancia (6-11 años)',
    '15-19': 'Adolescencia (12-18 años)',
    '20-24': 'Juventud (14-26 años)',
    '25-29': 'Juventud (14-26 años)',
    '30-34': 'Adultez (27-59 años)',
    '35-39': 'Adultez (27-59 años)',
    '40-44': 'Adultez (27-59 años)',
    '45-49': 'Adultez (27-59 años)',
    '50-54': 'Adultez (27-59 años)',
    '55-59': 'Adultez (27-59 años)',
    '60-64': 'Persona Mayor (60 años o más)',
    '65-69': 'Persona Mayor (60 años o más)',
    '70-74': 'Persona Mayor (60 años o más)',
    '75-79': 'Persona Mayor (60 años o más)',
    '80-84': 'Persona Mayor (60 años o más)',
    '85 o más': 'Persona Mayor (60 años o más)',
    'NO DISPONIBLE': 'No disponible'
}