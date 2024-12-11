import requests
import logging
from rag import find_relevant_context, augment_prompt_with_context

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://localhost:1234"  # LMStudio está corriendo en este puerto
MAX_CONTEXT_MESSAGES = 1  # Limitar el contexto al último mensaje del usuario

def chat_completions(messages, temperature=0.5):  # Set temperature to 0 for maximum consistency
    bot_name = "Asistente WIS"
    system_prompt = {
        "role": "system",
        "content": f"Eres un asistente virtual llamado {bot_name}, especializado en responder preguntas y resolver dudas relacionadas con el sistema WIS (Warehouse Information System). Tu objetivo principal es proporcionar respuestas precisas y detalladas basándote ÚNICAMENTE en la información proporcionada en el contexto relevante. Si no encuentras información específica en el contexto proporcionado, indica que no tienes suficiente información para responder. NO inventes ni inferencias información que no esté explícitamente en el contexto. Mantén un tono profesional y conciso. Si la pregunta no está relacionada con WIS o no tienes contexto relevante, sugiere contactar al soporte técnico."
    }
    
    # Limitar el contexto al último mensaje del usuario
    limited_messages = messages[-MAX_CONTEXT_MESSAGES:]
    messages_with_prompt = [system_prompt] + limited_messages

    try:
        # Find relevant context based on the user's last message
        user_query = limited_messages[-1]["content"]
        relevant_context = find_relevant_context(user_query)
        
        if not relevant_context.strip():
            return {"choices": [{"message": {"content": "Lo siento, no tengo información específica para responder a esa pregunta. Por favor, contacta al soporte técnico para obtener más información sobre el sistema WIS."}}]}
        
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
            }
        )
        response.raise_for_status()
        result = response.json()
        
        # Check if the response is not the system prompt
        assistant_response = result["choices"][0]["message"]["content"]
        if assistant_response.strip() == system_prompt["content"].strip():
            assistant_response = "Lo siento, no puedo proporcionar información específica basada en el contexto disponible. Por favor, contacta al soporte técnico para obtener más detalles sobre el sistema WIS."
            result["choices"][0]["message"]["content"] = assistant_response
        
        logging.info(f"Respuesta del modelo: {result}")
        return result
    
    except requests.RequestException as e:
        logging.error(f"Error al obtener la respuesta del modelo: {e}")
        return {"choices": [{"message": {"content": "Error al comunicarse con el servidor. Por favor, intenta de nuevo más tarde."}}]}
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return {"choices": [{"message": {"content": "Ocurrió un error inesperado. Por favor, contacta al soporte técnico para obtener ayuda."}}]}

