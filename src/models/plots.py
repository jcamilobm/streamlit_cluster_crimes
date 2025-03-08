from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def display_model_metrics_table(df, title='📊 Comparación de métricas'):
    """
    Renders an interactive table with single-row selection using AgGrid.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing model metrics.
    - title (str): Title of the table.
    
    Returns:
    - list: Selected row data (if any).
    """
    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=False,
        filter=True,
        sortable=True,
        resizable=True,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )

    # Center numeric columns
    numeric_columns = ['Clusters', 'Inercia', 'Silhouette Score', 'Calinski-Harabasz', 'Davies-Bouldin']
    for col in numeric_columns:
        if col in df.columns:
            gb.configure_column(col, cellStyle={'textAlign': 'center'})

    # Enable single row selection with checkbox
    gb.configure_selection('single', use_checkbox=True)

    # Build grid options
    grid_options = gb.build()

    # Calculate dynamic table height
    row_count = max(1, df.shape[0])  # Ensure at least 1 row
    row_height = 60
    min_height = 140  # Minimum height for small dataframes
    calculated_height = max(min_height, row_count * row_height)

    # Render the table
    #st.title(title)
    response = AgGrid(
        df,
        gridOptions=grid_options,
        theme='streamlit',
        height=calculated_height,
        fit_columns_on_grid_load=True,
        domLayout='autoHeight'
    )

    # Return selected row data
    return response