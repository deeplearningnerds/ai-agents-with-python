import os
import uuid

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="E-Commerce-KI-Assistent", layout="wide")
st.title("E-Commerce-KI-Assistent")
st.caption("KI-Assistent zur Analyse von Verkaufsdaten.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.subheader("Konfiguration")
    st.write(f"Agenten-API: `{AGENT_API_URL}`")
    st.write(f"Sitzung: `{st.session_state.session_id}`")
    if st.button("Chat zurücksetzen", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input(
    "Stellen Sie eine Frage zu Umsatz, Produkten, Kategorien oder Kunden ..."
)

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Der KI-Agent arbeitet ..."):
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
        except requests.RequestException:
            answer = (
                "Die Agenten-API konnte nicht erreicht werden. "
                "Prüfen Sie, ob die Agenten-API gestartet wurde."
            )

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
