import streamlit as st
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# Función para calcular las métricas de clustering
def calculate_clustering_metrics(df_model, labels, model=None):
    silhouette = silhouette_score(df_model, labels)
    calinski_harabasz = calinski_harabasz_score(df_model, labels)
    davies_bouldin = davies_bouldin_score(df_model, labels)
    inertia = model.inertia_ if model and hasattr(model, 'inertia_') else 'N/A'

    return {
        'Inercia': inertia,
        'Silhouette Score': silhouette,
        'Calinski-Harabasz': calinski_harabasz,
        'Davies-Bouldin': davies_bouldin
    }
