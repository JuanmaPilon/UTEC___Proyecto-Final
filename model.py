import requests
import logging
from rag import find_relevant_context, augment_prompt_with_context

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://localhost:1234"  # LMStudio está corriendo en este puerto

def chat_completions(messages, temperature=0.8):
    bot_name = "Asistente WIS"
    system_prompt = {
        "role": "system",
        "content": f"Eres un asistente virtual llamado {bot_name}, especializado en responder preguntas y resolver dudas relacionadas con el sistema WIS (Warehouse Management System). Tu objetivo principal es proporcionar respuestas claras y detalladas basándote en información de los manuales del sistema y ejemplos prácticos. Mantén un tono profesional, amigable y accesible. Siempre busca guiar al usuario con instrucciones paso a paso o explicaciones concretas, adaptándote a su nivel de conocimiento técnico. Si no tienes la información solicitada, sugiere consultar otras fuentes o contactar soporte técnico."
    }
    messages_with_prompt = [system_prompt] + messages

    try:
        # Find relevant context based on the user's last message
        user_query = messages[-1]["content"]
        relevant_context = find_relevant_context(user_query)
        
        # Augment the prompt with the relevant context
        augmented_messages = augment_prompt_with_context(messages_with_prompt, relevant_context)

        # Realiza la solicitud al endpoint de chat completions
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": "llama-3.1-wis-v6.5",  # Nombre del modelo que estás utilizando
                "messages": augmented_messages,
                "temperature": temperature,
                "max_tokens": -1,  # Usa el máximo de tokens permitidos
                "stream": False  # No usaremos streaming en esta implementación
            },
        )
        response.raise_for_status()
        result = response.json()
        logging.info(f"Respuesta del modelo: {result}")
        return result
    except requests.RequestException as e:
        logging.error(f"Error al obtener la respuesta del modelo: {e}")
        return {"choices": [{"message": {"content": "Error al comunicarse con el servidor."}}]}

