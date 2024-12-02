# streamlit run app.py
import streamlit as st
from model import chat_completions

st.title("Asistente virtual WMS")

# Inicializa el estado de los mensajes
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Para mostrar un mensaje inicial del asistente al iniciar
if 'first_message' not in st.session_state:
    st.session_state.first_message = True

# Muestra los mensajes anteriores (usuario y asistente)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario y procesamiento de respuesta del asistente
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Añade el mensaje del usuario a la lista
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtiene la respuesta del asistente
    with st.chat_message("assistant"):
        response = chat_completions(st.session_state.messages)
        assistant_response = response.get("choices")[0].get("message").get("content")
        st.markdown(assistant_response)

    # Añade la respuesta del asistente a la lista de mensajes
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
