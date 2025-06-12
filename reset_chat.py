import streamlit as st

def reset_chat():
    system_message = next((m for m in st.session_state.messages if m["role"] == "system"), None)
    st.session_state.messages = []
    if system_message:
        st.session_state.messages.append(system_message)
    st.rerun()