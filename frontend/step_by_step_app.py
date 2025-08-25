import streamlit as st

st.set_page_config(page_title="Step by Step Debug", page_icon="🔍")

st.title("🔍 Step by Step Debug")

# Step 1: Basic imports
st.header("Step 1: Basic Imports")
try:
    import requests
    st.success("✅ requests imported")
except Exception as e:
    st.error(f"❌ requests import failed: {e}")
    st.stop()

try:
    import uuid
    st.success("✅ uuid imported")
except Exception as e:
    st.error(f"❌ uuid import failed: {e}")
    st.stop()

try:
    import sys
    import os
    st.success("✅ sys and os imported")
except Exception as e:
    st.error(f"❌ sys/os import failed: {e}")
    st.stop()

# Step 2: Path setup
st.header("Step 2: Path Setup")
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    st.success("✅ Path setup completed")
except Exception as e:
    st.error(f"❌ Path setup failed: {e}")
    st.stop()

# Step 3: Config import
st.header("Step 3: Config Import")
try:
    from config import config
    st.success("✅ Config imported")
    st.write(f"Environment: {config.environment}")
    st.write(f"Backend URL: {config.backend_url}")
    st.write(f"Debug: {config.debug}")
except Exception as e:
    st.error(f"❌ Config import failed: {e}")
    st.stop()

# Step 4: Backend config import
st.header("Step 4: Backend Config Import")
try:
    from backend.app.config import JOB_ROLE_MAPPING
    st.success("✅ Backend config imported")
    st.write(f"Job roles: {list(JOB_ROLE_MAPPING.keys())}")
except Exception as e:
    st.error(f"❌ Backend config import failed: {e}")
    st.stop()

# Step 5: Basic app structure
st.header("Step 5: Basic App Structure")
try:
    # Session state initialization
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.new_session = True
    st.success("✅ Session state initialized")
    
    # Welcome message
    friendly_names = [role['friendly_name'] for role in JOB_ROLE_MAPPING.values()]
    welcome_message = (
        "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
        "- {}\n\n".format("\n- ".join(friendly_names)) +
        "Which role are you interested in learning more about?"
    )
    st.success("✅ Welcome message created")
    
    # Display welcome message
    st.markdown(welcome_message)
    
except Exception as e:
    st.error(f"❌ App structure failed: {e}")
    st.stop()

# Step 6: Configuration display
st.header("Step 6: Configuration Display")
try:
    if config.debug:
        config.log_config()
        st.success("✅ Configuration displayed")
    else:
        st.info("Debug mode is off, skipping config display")
except Exception as e:
    st.error(f"❌ Configuration display failed: {e}")

st.success("🎉 All steps completed successfully!")
st.write("The main app should work now. Try running `streamlit run app.py`")
