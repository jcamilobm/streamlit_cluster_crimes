import os
import streamlit as st
from dotenv import load_dotenv

# Cargar .env automáticamente al iniciar
load_dotenv()

def get_secret(key: str, default=None):
    """
    Devuelve un secreto desde st.secrets o .env.
    """
    return st.secrets.get(key) or os.getenv(key, default)
