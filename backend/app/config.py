import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# We build an absolute path to the .env file to ensure it's found consistently.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Central Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Validation ---
# We check for the key here, so the app fails fast if it's missing.
if not OPENAI_API_KEY:
    raise ValueError("FATAL ERROR: OPENAI_API_KEY is not set in your .env file.")
if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
    raise ValueError("FATAL ERROR: Pinecone API key or index name is not set in your .env file.")
if not DATABASE_URL:
    raise ValueError("FATAL ERROR: DATABASE_URL is not set in your .env file.")

# --- Job Role Mapping (remains the same) ---
JOB_ROLE_MAPPING = {
    "data_analyst": {
        "pdf_filename": "Data-Analyst-Job-Description.pdf",
        "sql_position_name": "Analyst",
        "friendly_name": "Data Analyst",
        "aliases": ["data analyst", "analyst", "data analytics"]
    },
    "ml_engineer": {
        "pdf_filename": "Machine-Learning-Engineer-092016.pdf",
        "sql_position_name": "ML",
        "friendly_name": "Machine Learning Engineer",
        "aliases": ["ml engineer", "machine learning engineer", "ml"]
    },
    "python_developer": {
        "pdf_filename": "PythonDeveloperJobDescription.pdf",
        "sql_position_name": "Python Dev",
        "friendly_name": "Python Developer",
        "aliases": ["python developer", "python dev", "python software engineer"]
    },
    "sql_developer": {
        "pdf_filename": "SrSQLDeveloperJD.pdf",
        "sql_position_name": "Sql Dev",
        "friendly_name": "Senior SQL Developer",
        "aliases": ["sql developer", "sr sql dev", "sql dev", "database developer", "senior sql developer"]
    }
}
