import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI  # Cliente OpenRouter
from src.utils.config_loader import load_config

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener credenciales desde .env
api_key_llm = os.getenv("API_KEY")

# Cargar configuración desde YAML
config = load_config()

# Configuración de parámetros LLM
system_prompt = config.get("llm", {}).get("system_prompt", "Eres un asistente de IA.")
model = config.get("llm", {}).get("model", "gpt-4")
temperature = config.get("llm", {}).get("temperature", 0.7)
base_url = config.get("llm", {}).get("base_url", "https://openrouter.ai/api/v1")  # Permite compatibilidad con otros proveedores


def send_llm_request(user_prompt_dinamico, system_prompt=system_prompt,
                     model=model, temperature=temperature, top_p=0.8, 
                     frequency_penalty=0.5, presence_penalty=0.3):
    """
    Envía una solicitud a la API OpenRouter (u otro proveedor) usando el modelo especificado y devuelve la respuesta generada.

    Parámetros:
      system_prompt (str): Instrucciones del sistema que configuran el comportamiento del LLM.
      user_prompt_dinamico (str): Mensaje dinámico del usuario, que puede incluir instrucciones adicionales o datos.
      model (str): Identificador del modelo a utilizar.
      temperature (float): Controla la creatividad de la respuesta.
      top_p (float): Probabilidad acumulada para la generación de tokens.
      frequency_penalty (float): Penaliza la repetición de palabras.
      presence_penalty (float): Penaliza la repetición de temas.
      
    Retorna:
      str: El contenido del mensaje de la respuesta generada por el LLM.
    """
    # Concatenar el prompt del usuario a partir del config y el prompt dinámico
    user_prompt = config.get("llm", {}).get("user_prompt", "") + "\n\n" + user_prompt_dinamico

    try:
        # Instanciar el cliente OpenAI (compatible con OpenRouter u otros)
        client = OpenAI(
            base_url=base_url,  # Permite cambiar de proveedor fácilmente
            api_key=api_key_llm
        )

        # Construir los mensajes de la conversación
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Llamada a la API con manejo de cabeceras personalizadas
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Opcional
                "X-Title": "<YOUR_SITE_NAME>"       # Opcional
            }
        )

        # Retornar el contenido del primer mensaje de la respuesta
        return completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error al conectar con la API: {str(e)}"


# Ejemplo de uso en Streamlit:
# response_text = send_llm_request(user_prompt_dinamico)
# st.write(response_text)
