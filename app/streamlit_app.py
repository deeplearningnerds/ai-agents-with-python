from __future__ import annotations

import os
import uuid

import requests
import streamlit as st

AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="AI Agent Demo", page_icon="AI", layout="wide")
st.title("AI Agent Demo")
st.caption("Streamlit-Frontend fuer einen FastAPI-Agenten mit LangChain und MCP-Tools.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.subheader("Konfiguration")
    st.write(f"Agent API: `{AGENT_API_URL}`")
    st.write(f"Session: `{st.session_state.session_id}`")
    if st.button("Chat zuruecksetzen", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Stelle eine Frage zu den Bestelldaten ...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent arbeitet ..."):
                response = requests.post(
                    AGENT_API_URL,
                    json={
                        "message": user_prompt,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                answer = response.json()["answer"]
        except requests.RequestException as error:
            answer = (
                "Die Agent API konnte nicht erreicht werden. "
                f"Pruefe bitte den FastAPI-Dienst. Fehler: {error}"
            )

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
