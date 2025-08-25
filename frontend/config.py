"""
Configuration management for the frontend application.
Handles environment-specific settings in an industry-standard way.
"""

import os
import streamlit as st
from typing import Optional

class Config:
    """Configuration class for managing environment-specific settings."""
    
    def __init__(self):
        # Initialize with defaults first
        self._environment = None
        self._backend_url = None
        self._debug = None
    
    def _get_environment(self) -> str:
        """Get the current environment."""
        if self._environment is None:
            # Priority: Streamlit secrets > Environment variable > Default
            try:
                self._environment = (
                    st.secrets.get("ENVIRONMENT") or 
                    os.getenv("ENVIRONMENT") or 
                    "development"
                )
            except Exception:
                self._environment = "development"
        return self._environment
    
    def _get_backend_url(self) -> str:
        """Get the backend URL based on environment."""
        if self._backend_url is None:
            # Priority: Streamlit secrets > Environment variable > Environment-specific defaults
            try:
                # Check Streamlit secrets first
                if st.secrets.get("BACKEND_URL"):
                    self._backend_url = st.secrets.get("BACKEND_URL")
                # Check environment variable
                elif os.getenv("BACKEND_URL"):
                    self._backend_url = os.getenv("BACKEND_URL")
                # Environment-specific defaults
                else:
                    environment = self._get_environment()
                    if environment == "production":
                        self._backend_url = "http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000"
                    elif environment == "staging":
                        self._backend_url = "http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000"
                    else:  # development
                        self._backend_url = "http://localhost:8000"
            except Exception:
                self._backend_url = "http://localhost:8000"
        return self._backend_url
    
    def _get_debug_mode(self) -> bool:
        """Get debug mode setting."""
        if self._debug is None:
            try:
                debug_str = (
                    st.secrets.get("DEBUG") or 
                    os.getenv("DEBUG") or 
                    "false"
                )
                self._debug = debug_str.lower() in ("true", "1", "yes", "on")
            except Exception:
                self._debug = False
        return self._debug
    
    @property
    def environment(self) -> str:
        return self._get_environment()
    
    @property
    def backend_url(self) -> str:
        return self._get_backend_url()
    
    @property
    def debug(self) -> bool:
        return self._get_debug_mode()
    
    def get_backend_endpoint(self, endpoint: str = "") -> str:
        """Get full backend endpoint URL."""
        base_url = self.backend_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base_url}/{endpoint}" if endpoint else base_url
    
    def get_chat_endpoint(self) -> str:
        """Get the chat endpoint URL."""
        return self.get_backend_endpoint("chat")
    
    def get_health_endpoint(self) -> str:
        """Get the health endpoint URL."""
        return self.get_backend_endpoint("health")
    
    def get_env_test_endpoint(self) -> str:
        """Get the environment test endpoint URL."""
        return self.get_backend_endpoint("env-test")
    
    def log_config(self):
        """Log current configuration (without sensitive data)."""
        st.sidebar.markdown("### 🔧 Configuration")
        st.sidebar.markdown(f"**Environment:** {self.environment}")
        st.sidebar.markdown(f"**Backend:** {self.backend_url}")
        st.sidebar.markdown(f"**Debug:** {self.debug}")
        
        if self.debug:
            st.sidebar.markdown("### 🔗 Endpoints")
            st.sidebar.markdown(f"**Health:** {self.get_health_endpoint()}")
            st.sidebar.markdown(f"**Chat:** {self.get_chat_endpoint()}")

# Global configuration instance
config = Config()
