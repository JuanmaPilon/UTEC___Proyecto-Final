# streamlit run app.py
import streamlit as st
from model import chat_completions
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG)

# Título de la aplicación
st.title("Asistente virtual WMS")

# Agrega estilo para manejar texto con saltos de línea
st.markdown(
    """
    <style>
    .chat-response {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializa el estado de los mensajes
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Muestra los mensajes anteriores (usuario y asistente)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-response'>{msg['content']}</div>", unsafe_allow_html=True)

# Entrada de usuario y procesamiento de respuesta del asistente
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Añade el mensaje del usuario a la lista
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-response'>{prompt}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtiene la respuesta del asistente
    with st.chat_message("assistant"):
        response = chat_completions(st.session_state.messages)
        assistant_response = response.get("choices")[0].get("message").get("content")
        
        # Log de depuración para inspeccionar la respuesta
        logging.debug(f"Respuesta bruta del asistente: {assistant_response}")
        
        # Formatear respuesta para mostrar correctamente saltos de línea
        formatted_response = assistant_response.replace("\\n", "\n").strip()
        st.markdown(f"<div class='chat-response'>{formatted_response}</div>", unsafe_allow_html=True)

    # Añade la respuesta del asistente a la lista de mensajes
    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
