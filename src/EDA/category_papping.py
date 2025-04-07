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




import pandas as pd

# Diccionario de mapeo reducido a 8 grupos
SITE_GROUP_DICT = {
    # Grupo 1: Vías y Espacios Públicos
    "VIAS PUBLICAS": "Vías y Espacios Públicos",
    "CALLEJÓN": "Vías y Espacios Públicos",
    "CARRETERA": "Vías y Espacios Públicos",
    "PERIMETRO URBANO": "Vías y Espacios Públicos",
    "ZONAS AZULES - VIA PUBLICA": "Vías y Espacios Públicos",
    "RODANDO SOBRE VIA - VIA PUBLICA": "Vías y Espacios Públicos",
    "SOBRE ANDEN - VIA PUBLICA": "Vías y Espacios Públicos",
    "SENDERO PEATONAL": "Vías y Espacios Públicos",
    "TRAMO DE VIA": "Vías y Espacios Públicos",
    "PUENTE": "Vías y Espacios Públicos",
    "PUENTE PEATONAL": "Vías y Espacios Públicos",
    "GLORIETA": "Vías y Espacios Públicos",
    "CORREDORES FLUVIALES": "Vías y Espacios Públicos",
    "CALETA": "Vías y Espacios Públicos",
    
    # Grupo 2: Transporte (Público y Privado)
    "PARADERO DE BUSES": "Transporte",
    "ESTACION TRANSMILENIO AV SUBA  CALLE 116": "Transporte",
    "BUS METROLINEA": "Transporte",
    "ESTACION METROLÍNEA": "Transporte",
    "TERMINAL DE TRANSPORTES": "Transporte",
    "ESTACION DEL METRO": "Transporte",
    "TRANSPORTE PÚBLICO": "Transporte",
    "ALIMENTADOR METROLÍNEA": "Transporte",
    "BUS METROPLUS": "Transporte",
    "ESTACION TRANSMILENIO PARQUE": "Transporte",
    "ESTACION DE ARTICULADO": "Transporte",
    "PEAJE": "Transporte",
    "ALIMENTADOR BUS M.I.O.": "Transporte",
    "ALIMENTADOR BUS TRANSMILENIO": "Transporte",
    "ESTACION TRANSMILENIO UNIVERSIDADES": "Transporte",
    "ESTACION TRANSMILENIO AV EL DORADO": "Transporte",
    "ESTACION TRANSPORTE MASIVO": "Transporte",
    "CARRIL EXCLUSIVO TRANSPORTE MASIVO": "Transporte",
    "TRANSPORTE INTERMUNICIPAL": "Transporte",
    "TRANSPORTE MASIVO": "Transporte",
    "BUS TRANSMETRO": "Transporte",
    "BUS MEGABUS": "Transporte",
    "ALIMENTADOR BUS TRANSMETRO": "Transporte",
    "ESTACION TRANSMILENIO SIMON BOLIVAR": "Transporte",
    "ESTACION TRANSMILENIO SENA": "Transporte",
    "EL METRO": "Transporte",
    "ESTACION TRANSMETRO": "Transporte",
    "ESTACION M.I.O.": "Transporte",
    "AEROPUERTO": "Transporte",
    "INTERIOR VEHICULO PARTICULAR": "Transporte",
    "VEHICULO": "Transporte",
    "VEHICULO TAXI": "Transporte",
    "VEHICULO UBER": "Transporte",
    "VEHICULO MOTO": "Transporte",
    "VEHICULO PICAP": "Transporte",
    "VEHICULO INDRIVER": "Transporte",
    "MÓVIL": "Transporte",
    "VEHICULO BEAT": "Transporte",
    "GARAJE": "Transporte",
    
    # Grupo 3: Áreas Residenciales
    "FRENTE A RESIDENCIAS - VIA PUBLICA": "Áreas Residenciales",
    "SECTOR RESIDENCIAS": "Áreas Residenciales",
    "CASAS DE HABITACION": "Áreas Residenciales",
    "HOTELES, RESIDENCIAS, Y SIMILARES.": "Áreas Residenciales",
    "CONJUNTO RESIDENCIAL": "Áreas Residenciales",
    "APARTAMENTO EN CONJUNTO CERRADO": "Áreas Residenciales",
    "APARTAMENTO": "Áreas Residenciales",
    "CASA EN CONJUNTO CERRADO": "Áreas Residenciales",
    "ALOJAMIENTO": "Áreas Residenciales",
    "CASA DE LENOCINIO": "Áreas Residenciales",
    "HOGARES / GERIATRICO": "Áreas Residenciales",
    
    # Grupo 4: Comercio y Servicios
    "CENTRO COMERCIAL": "Comercio y Servicios",
    "ALMACENES": "Comercio y Servicios",
    "SUPERMERCADOS": "Comercio y Servicios",
    "TIENDA": "Comercio y Servicios",
    "LOCAL COMERCIAL": "Comercio y Servicios",
    "BODEGAS Y SIMILARES": "Comercio y Servicios",
    "PANADERIAS": "Comercio y Servicios",
    "CAFETERIAS": "Comercio y Servicios",
    "FRUTERIA": "Comercio y Servicios",
    "DISCOTECAS": "Comercio y Servicios",
    "RESTAURANTES": "Comercio y Servicios",
    "PLAZAS DE MERCADO": "Comercio y Servicios",
    "CASINOS": "Comercio y Servicios",
    "BARES, CANTINAS Y SIMILARES": "Comercio y Servicios",
    "LICORERA/ESTANCO 24 HORAS": "Comercio y Servicios",
    "SECTOR COMERCIO": "Comercio y Servicios",
    "MATADEROS, CARNICERIA Y SIMILARES": "Comercio y Servicios",
    "JOYERIAS": "Comercio y Servicios",
    "LIBRERIAS": "Comercio y Servicios",
    "SALAS DE CINE": "Comercio y Servicios",
    "COMPRAVENTA": "Comercio y Servicios",
    
    # Grupo 5: Servicios (talleres, establecimientos de apoyo, etc.)
    "TALLERES MECANICA": "Servicios",
    "LAVA-AUTOS": "Servicios",
    "BOMBA DE GASOLINA": "Servicios",
    "CAJERO AUTOMATICO": "Servicios",
    "ESTACIONES DE SERVICIO": "Servicios",
    "TALLERES": "Servicios",
    "ESTABLECIMIENTO DE MENSAJERIA": "Servicios",
    "FUNERARIA": "Servicios",
    "TALLERES LATONERIA": "Servicios",
    "TALLERES ELECTRICIDAD": "Servicios",
    "CAFE INTERNET": "Servicios",
    "PELUQUERIA Y SIMILARES": "Servicios",
    "AREA DE VACUNACION": "Servicios",
    "LAVANDERIAS": "Servicios",
    "EMISORAS": "Servicios",
    
    # Grupo 6: Instituciones (educativas, de salud y similares)
    "COLEGIOS, ESCUELAS": "Instituciones",
    "UNIVERSIDADES": "Instituciones",
    "ESTABLECIMIENTO EDUCATIVO": "Instituciones",
    "AUDITORIOS": "Instituciones",
    "HOSPITALES": "Instituciones",
    "CLINICAS Y SIMILARES": "Instituciones",
    "ESTABLECIMIENTO DE SALUD": "Instituciones",
    "CONSULTORIOS MEDICOS": "Instituciones",
    "DROGUERIAS, FARMACIAS": "Instituciones",
    "CONSULTORIOS  ODONTOLOGICOS": "Instituciones",
    "LABORATORIO-TOMA DE MUESTRAS": "Instituciones",
    "LABORATORIO DE BASE": "Instituciones",
    "CONSULTORIOS JURIDICOS": "Instituciones",
    
    # Grupo 7: Recreación y Deportes
    "CENTRO RECREACIONAL": "Recreación y Deportes",
    "CANCHA DE FUTBOL": "Recreación y Deportes",
    "ESCENARIOS DEPORTIVOS": "Recreación y Deportes",
    "ESTADIO": "Recreación y Deportes",
    "PARQUES": "Recreación y Deportes",
    "GIMNASIO": "Recreación y Deportes",
    "COLISEO": "Recreación y Deportes",
    "CANCHAS DE TEJO": "Recreación y Deportes",
    "PLAYA": "Recreación y Deportes",
    "PISCINA": "Recreación y Deportes",
    "CANCHAS DE RANA": "Recreación y Deportes",
    
    # Grupo 8: Infraestructura Gubernamental y Seguridad
    "FRENTE OFICINA": "Infraestructura Gubernamental y Seguridad",
    "SECTOR INDUSTRIA": "Infraestructura Gubernamental y Seguridad",
    "FRENTE A BANCO - VIA PUBLICA": "Infraestructura Gubernamental y Seguridad",
    "OFICINAS": "Infraestructura Gubernamental y Seguridad",
    "EMPRESA": "Infraestructura Gubernamental y Seguridad",
    "EDIFICIO": "Infraestructura Gubernamental y Seguridad",
    "INSTALACIONES DEL EJERCITO": "Infraestructura Gubernamental y Seguridad",
    "FABRICAS": "Infraestructura Gubernamental y Seguridad",
    "CASETA COMUNAL": "Infraestructura Gubernamental y Seguridad",
    "GOBERNACION": "Infraestructura Gubernamental y Seguridad",
    "INSTALACIONES GUBERNAMENTALES": "Infraestructura Gubernamental y Seguridad",
    "CARCELES": "Infraestructura Gubernamental y Seguridad",
    "BANCOS": "Infraestructura Gubernamental y Seguridad",
    "ENTIDAD PUBLICA / ESTATAL": "Infraestructura Gubernamental y Seguridad",
    "ALCALDIA": "Infraestructura Gubernamental y Seguridad",
    "INSTALACIONES DE LA POLICIA": "Infraestructura Gubernamental y Seguridad",
    "SEDE POLITICA": "Infraestructura Gubernamental y Seguridad",
    "CASETA VIGILANCIA CONJUNTO RESIDENCIAL": "Infraestructura Gubernamental y Seguridad",
    "PUESTO DE CONTROL": "Infraestructura Gubernamental y Seguridad",
    "GUARDIA-PUNTOS FACCION": "Infraestructura Gubernamental y Seguridad",
    "CASETA VIGILANCIA EMPRESAS": "Infraestructura Gubernamental y Seguridad",
    
    # Si no coincide, se asigna "Otros"
}

