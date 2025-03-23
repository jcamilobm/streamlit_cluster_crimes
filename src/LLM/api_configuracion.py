import os
from dotenv import load_dotenv
from openai import OpenAI
from src.utils.config_loader import load_config
from src.utils.secrets import get_secret
import streamlit as st



def send_llm_request(
    user_prompt_dinamico: str,
    system_prompt: str = None,
    model: str = None,
    api_key_llm: str = None,
    base_url: str = None,
    temperature: float = None,
    top_p: float = 0.8,
    frequency_penalty: float = 0.5,
    presence_penalty: float = 0.3
) -> str:
    """
    Envía una solicitud a un modelo LLM vía API (como OpenRouter) con configuración flexible.

    Parámetros:
      user_prompt_dinamico (str): Entrada del usuario a concatenar al prompt base.
      system_prompt (str): Prompt del sistema. Se carga de config si no se pasa.
      model (str): Modelo LLM a usar. Se carga de config si no se pasa.
      api_key_llm (str): Clave de API. Se carga de .env si no se pasa.
      base_url (str): URL base del proveedor. Se carga de config si no se pasa.
      temperature, top_p, frequency_penalty, presence_penalty: Parámetros de control del LLM.

    Retorna:
      str: Respuesta del modelo.
    """

    # Cargar configuración si faltan parámetros
    config = load_config()
    system_prompt = system_prompt or config.get("llm", {}).get("system_prompt", "Eres un asistente de IA.")
    model = model or config.get("llm", {}).get("model", "meta-llama/llama-3.3-70b-instruct:free")
    temperature = temperature if temperature is not None else config.get("llm", {}).get("temperature", 0.7)
    base_url = base_url or config.get("llm", {}).get("base_url", "https://openrouter.ai/api/v1")


    api_key_llm = api_key_llm or  get_secret("API_KEY")

    if not api_key_llm:
        return "❌ Error: No se encontró una API Key válida."

    # Construir el prompt final
    user_prompt_base = config.get("llm", {}).get("user_prompt", "")
    user_prompt = f"{user_prompt_base}\n\n{user_prompt_dinamico}".strip()

    try:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key_llm
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>"
            }
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error al conectar con el modelo: {str(e)}"



# send_llm_request("Analiza la comuna 3")
# Usa modelo, prompt, temperatura, etc. desde la configuración


# o mayor control:

# send_llm_request(
 #   user_prompt_dinamico="Analiza la comuna 3",
 #   model="gpt-4-turbo",
  #  temperature=0.3,
   # api_key_llm="sk-mi-clave-personal"
#)
