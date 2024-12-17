import requests
import logging
from rag import find_relevant_context, split_context

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://localhost:1234"  # LMStudio está corriendo en este puerto
MAX_CONTEXT_MESSAGES = 1  # Limitar el contexto al último mensaje del usuario

def chat_completions(messages, temperature=0.3):
    bot_name = "Asistente WIS"
    system_prompt = {
        "role": "system",
        "content": f"""Eres un asistente virtual llamado {bot_name}, especializado en responder preguntas y resolver dudas relacionadas con el sistema WIS (Warehouse Management System). 

Tu objetivo principal es proporcionar respuestas precisas y detalladas basándote ÚNICAMENTE en la información proporcionada en el contexto relevante. Sigue estas pautas estrictamente:

1. Utiliza SOLO la información del contexto relevante proporcionado. No agregues información externa.
2. Si el contexto no contiene información específica para responder la pregunta, di explícitamente: "Lo siento, no tengo información suficiente en el contexto proporcionado para responder a esta pregunta específica."
3. NO inventes ni inferencias información que no esté explícitamente en el contexto.
4. Cita o parafrasea directamente del contexto proporcionado siempre que sea posible.
5. Si la pregunta no está relacionada con WIS o no tienes contexto relevante, sugiere contactar al soporte técnico.
6. Estructura tu respuesta en párrafos para mejorar la legibilidad.
7. Si es apropiado, utiliza viñetas o enumeraciones para presentar información de manera clara.

Recuerda, tu objetivo es ser lo más preciso posible, proporcionando SOLO información que esté presente en el contexto proporcionado sobre el sistema WIS."""
    }
    
    # Limitar el contexto al último mensaje del usuario
    limited_messages = messages[-MAX_CONTEXT_MESSAGES:]
    messages_with_prompt = [system_prompt]

    try:
        # Find relevant context based on the user's last message
        user_query = limited_messages[-1]["content"]
        relevant_context = find_relevant_context(user_query, n_results=5, max_tokens=3000)
        
        if relevant_context:
            # Split the context if it's too long
            context_parts = split_context(relevant_context, max_tokens=2000)
            for part in context_parts:
                context_prompt = {
                    "role": "system",
                    "content": f"Contexto relevante para la pregunta:\n\n{part}\n\nUtiliza ÚNICAMENTE esta información para responder a la pregunta del usuario. Si la información no es suficiente, indícalo claramente."
                }
                messages_with_prompt.append(context_prompt)
        else:
            context_prompt = {
                "role": "system",
                "content": "No se encontró contexto relevante para esta pregunta. Indica al usuario que no tienes información suficiente para responder y sugiere contactar al soporte técnico."
            }
            messages_with_prompt.append(context_prompt)
        
        messages_with_prompt.extend(limited_messages)
        
        # Realiza la solicitud al endpoint de chat completions
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": "llama-3.1-wis-v6.5",  # Nombre del modelo que estás utilizando
                "messages": messages_with_prompt,
                "temperature": temperature,
                "max_tokens": 2000,  # Aumentado a 2000 para permitir respuestas más largas
                "stream": False  # No usaremos streaming en esta implementación
            }
        )
        response.raise_for_status()
        result = response.json()
        
        logging.info(f"Total tokens: {result['usage']['total_tokens']}")
        logging.info(f"Prompt tokens: {result['usage']['prompt_tokens']}")
        logging.info(f"Completion tokens: {result['usage']['completion_tokens']}")
        logging.info(f"Respuesta del modelo: {result['choices'][0]['message']['content']}")
        
        return result
    except requests.RequestException as e:
        logging.error(f"Error al obtener la respuesta del modelo: {e}")
        return {"choices": [{"message": {"content": "Error al comunicarse con el servidor. Por favor, intenta de nuevo más tarde."}}]}
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return {"choices": [{"message": {"content": "Ocurrió un error inesperado. Por favor, contacta al soporte técnico para obtener ayuda."}}]}

