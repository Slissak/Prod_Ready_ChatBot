import streamlit as st
import requests
import uuid
import sys
import os

# Add project root to sys.path to allow importing from backend config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our configuration management with fallback
try:
    from config import config
except Exception as e:
    st.error(f"Configuration error: {e}")
    # Fallback configuration
    class FallbackConfig:
        def get_chat_endpoint(self):
            return "http://localhost:8000/chat"
        def get_health_endpoint(self):
            return "http://localhost:8000/health"
        def get_env_test_endpoint(self):
            return "http://localhost:8000/env-test"
        @property
        def environment(self):
            return "development"
        @property
        def backend_url(self):
            return "http://localhost:8000"
        @property
        def debug(self):
            return True
        def log_config(self):
            st.sidebar.markdown("### ⚠️ Using Fallback Configuration")
            st.sidebar.markdown("**Environment:** development")
            st.sidebar.markdown("**Backend:** http://localhost:8000")
    
    config = FallbackConfig()

try:
    from backend.app.config import JOB_ROLE_MAPPING
except Exception as e:
    st.error(f"Backend config error: {e}")
    # Fallback job role mapping
    JOB_ROLE_MAPPING = {
        "data_analyst": {"friendly_name": "Data Analyst"},
        "ml_engineer": {"friendly_name": "Machine Learning Engineer"},
        "python_developer": {"friendly_name": "Python Developer"},
        "sql_developer": {"friendly_name": "Senior SQL Developer"}
    }

st.set_page_config(page_title="AI Career Assistant", page_icon="🤖")

# --- Page Title ---
st.title("🤖 AI Career Assistant")

# --- Browser Compatibility Notice ---
st.info("💡 **Browser Tip**: For best experience, use Chrome or Firefox. Safari users may need to disable cross-site tracking.")

# --- Configuration Display (in debug mode) ---
if config.debug:
    config.log_config()

# --- Session State Initialization & Welcome Message ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.new_session = True

if "messages" not in st.session_state:
    friendly_names = [role['friendly_name'] for role in JOB_ROLE_MAPPING.values()]
    welcome_message = (
        "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
        "- {}\n\n".format("\n- ".join(friendly_names)) +
        "Which role are you interested in learning more about?"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_message, "new_session": True, "session_id": st.session_state.session_id}]

# Check if we need to add a welcome message for a new session
if st.session_state.get("new_session") and st.session_state.messages and not any(msg.get("new_session") for msg in st.session_state.messages):
    # Add welcome message for new session
    friendly_names = [role['friendly_name'] for role in JOB_ROLE_MAPPING.values()]
    welcome_message = (
        "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
        "- {}\n\n".format("\n- ".join(friendly_names)) +
        "Which role are you interested in learning more about?"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_message, "new_session": True, "session_id": st.session_state.session_id})
    st.session_state.new_session = False

# --- Render Chat History ---
for message in st.session_state.messages:
    if message.get("new_session"):
        st.markdown("---")
        st.info("New Chat Session Started")
        
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "logs" in message and message["logs"]:
            log_title = f"Show logs for session: {message.get('session_id', st.session_state.session_id)}"
            with st.expander(log_title):
                st.code("\n".join(message["logs"]), language="log")

# --- User Input Handling ---
if prompt := st.chat_input("Ask me anything..."):
    if st.session_state.get("new_session"):
        st.session_state.new_session = False

    st.session_state.messages.append({"role": "user", "content": prompt, "session_id": st.session_state.session_id})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            request_session_id = st.session_state.session_id
            payload = {"session_id": request_session_id, "user_message": prompt}
            response = requests.post(config.get_chat_endpoint(), json=payload, timeout=60)
            response.raise_for_status()
            
            response_data = response.json()
            bot_response = response_data.get("bot_response", "Sorry, something went wrong.")
            logs = response_data.get("logs", [])
            new_session_required = response_data.get("new_session_required", False)
            backend_new_session_id = response_data.get("new_session_id")
            backend_welcome_message = response_data.get("welcome_message")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend: {e}")
            bot_response = "I'm having trouble connecting to my brain. Please make sure the backend is running and the URL is correct."
            logs = []
            new_session_required = False
        
        message_placeholder.markdown(bot_response)
        if logs:
            log_title = f"Show logs for session: {st.session_state.session_id}"
            with st.expander(log_title):
                st.code("\n".join(logs), language="log")

    st.session_state.messages.append({
        "role": "assistant", "content": bot_response, "logs": logs, "session_id": request_session_id
    })
    
    # Check if we need to start a new session (based on explicit backend signal)
    if new_session_required:
        # Use backend-provided new session id if available, otherwise fallback
        st.session_state.session_id = backend_new_session_id or str(uuid.uuid4())

        # Prepare welcome message (prefer backend-provided to keep in sync)
        if not backend_welcome_message:
            friendly_names = [role['friendly_name'] for role in JOB_ROLE_MAPPING.values()]
            backend_welcome_message = (
                "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
                "- {}\n\n".format("\n- ".join(friendly_names)) +
                "Which role are you interested in learning more about?"
            )

        # Append a new-session welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": backend_welcome_message,
            "new_session": True,
            "session_id": st.session_state.session_id,
        })
        st.session_state.new_session = False

        # Force a rerun so the UI immediately shows the new-session banner and welcome message
        try:
            st.rerun()
        except Exception:
            try:
                st.experimental_rerun()
            except Exception:
                pass
