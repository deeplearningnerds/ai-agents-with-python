import streamlit as st
from agent import query_agent

# ------------------------------
# Streamlit App Setup
# ------------------------------
st.title("Stocky Rocky")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.header("Stocky Rocky")

# ------------------------------
# Display Chat History
# ------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------
# Capture User Input
# ------------------------------
if prompt := st.chat_input("Your question"):
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # ------------------------------
    # Get Agent Response
    # ------------------------------
    # Send the user input to the agent and get the response
    with st.spinner("Thinking..."):
        response = query_agent(prompt)
        print(response)

    # Display assistant response in chat
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
