# Aplicación crimenes por comuna en Bucaramanga

<p align="center">
  <a href="" target="_blank">
    <img src="assets/banner.svg" alt="App Streamlit Clustering por Comunas de Bucaramanga" width="450px">
  </a>
</p>

<p align="center">
  <a href="https://appclustercrimes-hps7f8ushwdyf2bvx9b6k8.streamlit.app/" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit application">
  </a>
  <a href="https://google.com" target="_blank">
    <img src="https://img.shields.io/badge/Documentation-📘-blueviolet" alt="App Documentation">
  </a>
</p>

## 🔥 Demo

Visita la App en [our website](https://appclustercrimes-hps7f8ushwdyf2bvx9b6k8.streamlit.app/)

![Tweet Generator](assets/demo_app_cluster_crimen_1.gif)

Puedes generar insight con ayuda de IA:

![Tweet Generator](assets/demo_app_cluster_crimen_2_llm.gif)

## 📚 Documentación

Visita nuestra documentación [here](https://google.com)


## 📑 Tabla de contenido

- [Introducción](#introduccion)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Flujograma](#flujograma)

---

## Introducción

En **Clustering por Comunas en Bucaramanga** se utiliza la inteligencia de dos modelos de clustering (k-means y jerárquico) para agrupar datos de crímenes reportados en la ciudad. La aplicación se centra en:
- Analizar datos de incidentes delictivos.
- Visualizar clusters en un mapa interactivo.
- Ofrecer información relevante para autoridades y ciudadanos.
- Asistencia con LLM para insights

Esta herramienta ayuda a identificar patrones delictivos, permitiendo focalizar estrategias de prevención y optimización de recursos en las comunas con mayor incidencia.

---

## Estructura de carpetas

El proyecto se compone de los siguientes módulos:

- **EDA:** Recopilación y preprocesamiento de datos de Datos Abiertos Colombia.
- **models:** Preparación de datos para modelos de machine learning supervisado (k-means y jerárquico).
- **notebook:** Resumen de limpieza de datos.
- **LLM:** Consumo de API de modelos de lenguaje para generar insights a partir de los resultados del clustering.
- **utils:** Carga de `config.yaml`.
---

## Flujograma

En resumen sigue la siguiente secuencia de ejecucion:

![flujograma-app](assets/flujograma_app.png)
---
