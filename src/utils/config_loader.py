# src/utils/config_loader.py

import yaml
from pathlib import Path

import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Lee un archivo YAML y retorna un diccionario con la configuración.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}  # Retorna un diccionario vacío si el archivo está vacío
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error al parsear el archivo YAML: {e}")

def update_config(clave: str, nuevo_valor, config_path: str = "config/config.yaml"):
    """Actualiza una clave anidada dentro del archivo YAML sin perder otras configuraciones."""
    config = load_config(config_path)  # Cargar configuración actual

    # Desglosar claves anidadas (ej. "llm.model" → ["llm", "model"])
    keys = clave.split(".")
    sub_config = config

    # Navegar por las claves anidadas excepto la última
    for key in keys[:-1]:
        if key not in sub_config:
            sub_config[key] = {}  # Crear el nivel si no existe
        sub_config = sub_config[key]

    # Actualizar el valor de la clave final
    sub_config[keys[-1]] = nuevo_valor

    # Guardar nuevamente el archivo
    with open(config_path, "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
