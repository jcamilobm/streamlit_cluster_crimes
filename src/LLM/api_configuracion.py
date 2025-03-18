from src.utils.config_loader import load_config
from openai import OpenAI

import os
from dotenv import load_dotenv
# Carga las variables definidas en .env


load_dotenv()
# Obtén la API key
api_key_llm = os.getenv("API_KEY")


config = load_config() 
system_prompt = config["llm"]["system_prompt"]
model = config["llm"]["model"]

import streamlit as st
import json
from openai import OpenAI  # Asegúrate de tener la importación correcta para OpenRouter
# Asegúrate de tener definida la variable `config` en el contexto de tu aplicación.

def send_llm_request(user_prompt_dinamico, system_prompt = system_prompt, 
                     model= model ,
                     temperature=0.3, top_p=0.8, 
                     frequency_penalty=0.5, presence_penalty=0.3):
    """
    Envía una solicitud a la API (OpenRouter) usando el modelo especificado y devuelve la respuesta generada.
    
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
    user_prompt = config["llm"].get("user_prompt", "") + "\n\n" + user_prompt_dinamico

    # Instanciar el cliente OpenAI (utilizando OpenRouter)
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key= api_key_llm
    )
    
    # Construir los mensajes de la conversación
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Mostrar un spinner de carga mientras se llama a la API
    #with st.spinner("Cargando respuesta del modelo de lenguaje. Espera un momento por favor"):
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>",   # Opcional
        "X-Title": "<YOUR_SITE_NAME>"          # Opcional
      },
      extra_body={},
      model=model,
      messages=messages,
      temperature=temperature,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty,
    )
    
    # Retornar el contenido del primer mensaje de la respuesta
    return completion.choices[0].message.content

# Ejemplo de uso en Streamlit:
# response_text = send_llm_request(user_prompt_dinamico)
# st.write(response_text)

