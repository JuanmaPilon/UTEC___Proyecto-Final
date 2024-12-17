# streamlit run app.py
import streamlit as st
from model import chat_completions
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG)

# Título de la aplicación
st.title("Asistente virtual WIS")

# Agrega estilo para manejar texto con saltos de línea y botones
st.markdown(
    """
    <style>
    .chat-response {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .remake-button {
        float: right;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        color: #4a4a4a;
        background-color: #f0f0f0;
        border: 1px solid #d0d0d0;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .remake-button:hover {
        background-color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializa el estado de los mensajes
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Inicializa el estado para controlar la regeneración de respuestas
if 'regenerate' not in st.session_state:
    st.session_state.regenerate = None

# Función para mostrar mensajes con formato
def display_message(role, content, message_index=None):
    with st.chat_message(role):
        if role == "assistant" and message_index is not None:
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"<div class='chat-response'>{content}</div>", unsafe_allow_html=True)
            with col2:
                if st.button("↺", key=f"remake_{message_index}", help="Rehacer esta respuesta"):
                    st.session_state.regenerate = message_index
        else:
            st.markdown(f"<div class='chat-response'>{content}</div>", unsafe_allow_html=True)

# Función para rehacer una respuesta
def remake_answer(message_index):
    # Obtener el contexto de la conversación hasta este punto
    context = st.session_state.messages[:message_index]
    
    # Obtener una nueva respuesta del asistente
    response = chat_completions(context)
    new_answer = response.get("choices")[0].get("message").get("content")
    
    # Formatear la nueva respuesta
    formatted_response = new_answer.replace("\n", "\n").strip()
    
    # Actualizar la respuesta en el historial de mensajes
    st.session_state.messages[message_index]["content"] = formatted_response

# Muestra los mensajes anteriores (usuario y asistente)
for idx, msg in enumerate(st.session_state.messages):
    display_message(msg["role"], msg["content"], idx if msg["role"] == "assistant" else None)

# Comprueba si se debe regenerar una respuesta
if st.session_state.regenerate is not None:
    remake_answer(st.session_state.regenerate)
    st.session_state.regenerate = None
    st.rerun()

# Entrada de usuario y procesamiento de respuesta del asistente
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Añade el mensaje del usuario a la lista
    display_message("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtiene la respuesta del asistente
    response = chat_completions(st.session_state.messages)
    assistant_response = response.get("choices")[0].get("message").get("content")
    
    # Log de depuración para inspeccionar la respuesta
    logging.debug(f"Respuesta bruta del asistente: {assistant_response}")
    
    # Formatear respuesta para mostrar correctamente saltos de línea
    formatted_response = assistant_response.replace("\n", "\n").strip()
    display_message("assistant", formatted_response, len(st.session_state.messages))

    # Añade la respuesta del asistente a la lista de mensajes
    st.session_state.messages.append({"role": "assistant", "content": formatted_response})

