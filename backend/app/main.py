import logging
from dotenv import load_dotenv

# --- Configure Logging FIRST ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Output to stdout for container logs
    ]
)
logger = logging.getLogger(__name__)

# --- Load environment variables FIRST ---
# This ensures that the .env file is loaded before any other application
# modules are imported, preventing configuration errors.
load_dotenv()

import os
from typing import List, Optional
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

# --- Environment Variable Validation ---
def validate_environment_variables():
    """Validate all required environment variables are present."""
    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_INDEX_NAME": os.getenv("PINECONE_INDEX_NAME")
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"❌ MISSING ENVIRONMENT VARIABLES: {missing_vars}")
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    # Log presence (not values) for security
    logger.info("✅ Environment variables loaded successfully:")
    for var, value in required_vars.items():
        logger.info(f"   {var}: {'✅ Present' if value else '❌ Missing'}")
    
    return required_vars

# Validate environment variables on startup
try:
    env_vars = validate_environment_variables()
    logger.info("🚀 Environment validation completed successfully")
except Exception as e:
    logger.error(f"💥 Environment validation failed: {str(e)}")
    raise

# Import our compiled graph and config AFTER loading .env
from .graph import compiled_graph, GraphState
from .config import JOB_ROLE_MAPPING

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    bot_response: str
    logs: Optional[List[str]] = None
    new_session_required: Optional[bool] = False
    new_session_id: Optional[str] = None
    welcome_message: Optional[str] = None

app = FastAPI(
    title="Production-Ready Chatbot API",
    version="1.0.0",
)

origins = ["http://localhost", "http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    # Keep local dev
    allow_origins=["http://localhost", "http://localhost:8501"],
    # Allow Streamlit Cloud subdomains
    allow_origin_regex=r"^https://.*\.streamlit\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS = {}

@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("🚀 FastAPI application starting up...")
    logger.info(f"📊 Environment: {'Production' if os.getenv('ENVIRONMENT') == 'production' else 'Development'}")
    logger.info(f"🔧 Debug mode: {os.getenv('DEBUG', 'False')}")
    logger.info("✅ Application startup completed")

@app.get("/")
def read_root():
    logger.info("📡 Root endpoint called")
    return {"status": "API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint."""
    logger.info("🏥 Health check endpoint called")
    
    # Check environment variables
    env_status = {
        "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        "database_url": bool(os.getenv("DATABASE_URL")),
        "pinecone_api_key": bool(os.getenv("PINECONE_API_KEY")),
        "pinecone_index_name": bool(os.getenv("PINECONE_INDEX_NAME"))
    }
    
    # Check if all required services are available
    all_healthy = all(env_status.values())
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "environment_variables": env_status,
        "timestamp": str(uuid4()),
        "version": "1.0.0"
    }

@app.get("/env-test")
async def environment_test():
    """Test endpoint to verify environment variables (without exposing values)."""
    logger.info("🔍 Environment test endpoint called")
    
    env_info = {
        "openai_api_key_present": bool(os.getenv("OPENAI_API_KEY")),
        "database_url_present": bool(os.getenv("DATABASE_URL")),
        "pinecone_api_key_present": bool(os.getenv("PINECONE_API_KEY")),
        "pinecone_index_name_present": bool(os.getenv("PINECONE_INDEX_NAME")),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "False")
    }
    
    return {
        "environment_status": env_info,
        "all_variables_present": all([
            env_info["openai_api_key_present"],
            env_info["database_url_present"],
            env_info["pinecone_api_key_present"],
            env_info["pinecone_index_name_present"]
        ])
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"💬 Chat endpoint called - Session: {request.session_id[:8]}...")
    
    try:
        session_id = request.session_id
        if session_id not in SESSIONS:
            SESSIONS[session_id] = {
                "conversation_history": [],
                "current_job_role": None,
                "booking_status": None
            }
            logger.info(f"🆕 New session created: {session_id[:8]}...")
        
        conversation_history = SESSIONS[session_id]["conversation_history"]
        conversation_history.append(HumanMessage(content=request.user_message))

        inputs = {
            "user_message": request.user_message,
            "conversation_history": conversation_history,
            "logs": [],
            "current_job_role": SESSIONS[session_id].get("current_job_role"),
            "booking_status": SESSIONS[session_id].get("booking_status")
        }
        
        config = {
            "configurable": {"session_id": session_id},
            "recursion_limit": 25  # Increase recursion limit for debugging
        }
        
        logger.info(f"🔄 Invoking graph for session: {session_id[:8]}...")
        response_state: GraphState = compiled_graph.invoke(inputs, config)
        
        bot_response = response_state.get("bot_response", "Sorry, I encountered an error.")
        logs = response_state.get("logs", [])
        
        conversation_history.append(AIMessage(content=bot_response))
        
        # Check if conversation has ended and new session is required
        conversation_ended = response_state.get("conversation_ended", False)
        new_session_required = response_state.get("new_session_required", False)

        new_session_id: Optional[str] = None
        welcome_message: Optional[str] = None

        if conversation_ended and new_session_required:
            # Clean up the current session
            if session_id in SESSIONS:
                del SESSIONS[session_id]
            logs.append(f"Session {session_id} cleaned up - creating a new session")
            logger.info(f"🔄 Session ended and cleanup completed: {session_id[:8]}...")

            # Create a brand new session id and initialize empty state
            new_session_id = str(uuid4())
            SESSIONS[new_session_id] = {
                "conversation_history": [],
                "current_job_role": None,
                "booking_status": None
            }
            logs.append(f"New session created: {new_session_id}")

            # Build a standard welcome message with available roles
            friendly_names = [role['friendly_name'] for role in JOB_ROLE_MAPPING.values()]
            welcome_message = (
                "Hello! I'm an AI career assistant. I can help you with the following open positions:\n"
                f"- {'\n- '.join(friendly_names)}\n\n"
                "Which role are you interested in learning more about?"
            )
        else:
            # Update session state with the new values from the graph (only if session still exists)
            if session_id in SESSIONS:
                SESSIONS[session_id].update({
                    "current_job_role": response_state.get("current_job_role"),
                    "booking_status": response_state.get("booking_status")
                })

        logger.info(f"✅ Chat response generated successfully for session: {session_id[:8]}...")
        return ChatResponse(
            bot_response=bot_response,
            logs=logs,
            new_session_required=new_session_required,
            new_session_id=new_session_id,
            welcome_message=welcome_message,
        )
    except Exception as e:
        import traceback
        error_msg = f"Error in chat endpoint: {str(e)}"
        logger.error(f"💥 Chat endpoint error: {error_msg}")
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        return ChatResponse(
            bot_response="I'm sorry, I encountered an error. Please try again.",
            logs=[error_msg]
        )
