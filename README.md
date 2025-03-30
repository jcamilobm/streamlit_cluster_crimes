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

## 📚 Documentación

Visita nuestra documentación [here](https://google.com)


## 📑 Tabla de contenido

- [Introducción](#-introduccion)
- [Arquitectura](#-arquitectura)

---

## - Introducción

En **Clustering por Comunas en Bucaramanga** se utiliza la inteligencia de dos modelos de clustering (k-means y jerárquico) para agrupar datos de crímenes reportados en la ciudad. La aplicación se centra en:
- Analizar datos de incidentes delictivos.
- Visualizar clusters en un mapa interactivo.
- Ofrecer información relevante para autoridades y ciudadanos.
- Assitencia con LLM para insights

Esta herramienta ayuda a identificar patrones delictivos, permitiendo focalizar estrategias de prevención y optimización de recursos en las comunas con mayor incidencia.

---

## - Arquitectura

La arquitectura del proyecto se compone de los siguientes módulos:

- **EDA:** Recopilación y preprocesamiento de datos de Datos Abiertos Colombia
- **models:** preparacion de datos apra modelos de machine learning supervisado(k-means y jerarquico).
- **notebook:** Resumen de limpieza de datos.
- **LLM:** Consumo de API modelos de lenguaje para generar insight de los resultados de clustering.
- **utils** Carga de de config.yaml
---