import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Career Assistant", page_icon="🤖")

st.title("🤖 AI Career Assistant")

# Simple configuration
BACKEND_URL = "http://localhost:8000"

# Session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    welcome_message = (
        "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
        "- Data Analyst\n"
        "- Machine Learning Engineer\n"
        "- Python Developer\n"
        "- Senior SQL Developer\n\n"
        "Which role are you interested in learning more about?"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            payload = {"session_id": st.session_state.session_id, "user_message": prompt}
            response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            bot_response = response_data.get("bot_response", "Sorry, something went wrong.")
            
        except Exception as e:
            bot_response = f"I'm having trouble connecting to the backend: {str(e)}"
        
        message_placeholder.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Debug info
st.sidebar.markdown("### 🔧 Debug Info")
st.sidebar.markdown(f"**Backend:** {BACKEND_URL}")
st.sidebar.markdown(f"**Session:** {st.session_state.session_id[:8]}...")
st.sidebar.markdown(f"**Messages:** {len(st.session_state.messages)}")
