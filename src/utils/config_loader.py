# src/utils/config_loader.py

import yaml
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Lee un archivo YAML y retorna un diccionario con la configuración.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error al parsear el archivo YAML: {e}")
