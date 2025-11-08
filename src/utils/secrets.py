import os
import streamlit as st
from dotenv import load_dotenv

'''
# Cargar .env automáticamente al iniciar
load_dotenv()

def get_secret(key: str, default=None):
    """
    Devuelve un secreto desde st.secrets o .env.
    """
    return st.secrets.get(key) or os.getenv(key, default)
    #return os.getenv(key, default)
'''



# Cargar variables desde .env si existe
load_dotenv()

def get_secret(key: str, default=None):
    """
    Devuelve un secreto desde st.secrets (en producción)
    o desde .env (en desarrollo local).
    """
    try:
        # Solo si Streamlit ya cargó secrets correctamente
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Si st.secrets falla o no existe el archivo .streamlit/secrets.toml
        pass

    # Fallback a variables de entorno locales (.env o sistema)
    return os.getenv(key, default)
