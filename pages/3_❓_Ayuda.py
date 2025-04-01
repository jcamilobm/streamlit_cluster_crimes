import streamlit as st

st.set_page_config(
    page_title="Ayuda",
    page_icon="❓",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.info('Revisa el alcance de la App', icon="ℹ️")



# Ayuda – Agrupamiento de Comunas de Bucaramanga

Bienvenido a la aplicación de análisis de agrupamiento de comunas de Bucaramanga. Esta herramienta utiliza técnicas de machine learning no supervisado para clasificar y agrupar las 17 comunas de la ciudad, facilitando la identificación de patrones y similitudes entre ellas.

---

## 1. Objetivos y Funcionalidades Principales

### Agrupamiento mediante Clustering

- **Modelos Utilizados:**
  - **K-means:** Divide las comunas en grupos (clusters) basándose en la cercanía de los datos, optimizando la suma de las distancias al centroide de cada grupo.
  - **Agrupamiento Jerárquico:** Crea una estructura de árbol (dendrograma) para observar cómo se relacionan las comunas entre sí en distintos niveles de similitud.

### Experimentación Interactiva

- **Filtrado de Datos:** En la página inicial puedes experimentar aplicando filtros según diferentes variables. Esto te permite observar cómo varían los clusters al modificar los parámetros.
- **Selección de Parámetros:** Ajusta valores y opciones específicas para cada modelo y observa en tiempo real cómo afectan la formación de los grupos.

### Asistente de Inteligencia Artificial

- **Generación de Insights:** Un asistente de IA integrado te ayuda a interpretar los resultados, generar conclusiones y plantear nuevas preguntas de análisis.
- **Personalización en la Página LLM:**
  - **Contexto del Prompt:** Define qué tipo de insight buscas y cuál es el enfoque analítico del asistente.
  - **Selección del Modelo LLM:** Elige el modelo de lenguaje que mejor se adapte a tus necesidades.
  - **Descripciones de las 17 Comunas:** Proporciona información detallada sobre cada comuna, lo que permite al asistente contextualizar correctamente los clusters y ofrecer recomendaciones basadas en las características específicas de cada zona.

---

## 2. Cómo Utilizar la Aplicación

### Navegación y Uso Básico

- **Página Inicial:**
  - Utiliza los paneles y controles para filtrar datos según criterios específicos (por ejemplo, indicadores socioeconómicos o delictivos).
  - Selecciona entre los modelos de clustering disponibles (K-means y agrupamiento jerárquico) y ajusta sus parámetros para observar diferentes configuraciones de agrupamiento.
  
- **Visualizaciones Dinámicas:**
  - Los resultados se muestran en gráficos y mapas interactivos que facilitan la interpretación de los clusters.
  - Al interactuar con las visualizaciones, puedes profundizar en los detalles de cada cluster para conocer las comunas agrupadas y sus características.

### Uso del Asistente de IA

- **Interacción con el Asistente:**
  - Realiza preguntas o solicita interpretaciones sobre los clusters obtenidos.
  - El asistente te ayudará a generar insights basados en los datos filtrados y en las descripciones de las comunas.
  
- **Personalización del Asistente (Ajustes LLM):**
  - Accede a la página de ajustes para modificar el prompt del asistente.
  - Configura el **contexto** y la **metodología** que se desea aplicar en el análisis.
  - Selecciona el **modelo LLM** a utilizar (por ejemplo, GPT-4 u otro disponible).
  - Ingresa o revisa las **descripciones de las 17 comunas** para asegurar que el asistente tenga la información necesaria para contextualizar los resultados.

---

## 3. Preguntas Frecuentes (FAQ)

**¿Cuál es el objetivo principal de la aplicación?**  
La aplicación busca agrupar las comunas de Bucaramanga utilizando técnicas de clustering para identificar patrones y similitudes, facilitando el análisis y la toma de decisiones en ámbitos como seguridad, planificación urbana o estudios socioeconómicos.

**¿Cómo se selecciona el modelo de clustering?**  
En la interfaz inicial puedes elegir entre K-means y agrupamiento jerárquico. Cada modelo tiene sus propias características y se puede ajustar mediante parámetros para obtener diferentes agrupaciones.

**¿Qué puedo hacer si no entiendo los resultados?**  
Utiliza el asistente de IA, el cual está diseñado para ayudarte a interpretar los clusters y generar insights a partir de los datos. Además, revisa las descripciones de cada comuna en la sección de ajustes LLM para entender mejor el contexto de los clusters.

**¿Cómo actualizo o personalizo el prompt del asistente de IA?**  
En la página de ajustes LLM, encontrarás opciones para:
- Modificar el **contexto del prompt** y definir claramente qué tipo de análisis esperas del asistente.
- Seleccionar el **modelo LLM** a utilizar.
- Revisar y editar las **descripciones de las 17 comunas** para asegurar que el asistente tenga la información necesaria.
