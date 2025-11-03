"""
Configuration management for the AI Knowledge Assistant.
Loads settings from environment variables with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Ollama settings
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "phi3")  # Changed to phi3 for faster responses
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    
    # Document storage
    BASE_DIR: Path = Path(__file__).parent.parent  # Project root
    # Allow absolute paths or relative to project root
    docs_dir = os.getenv("DOCUMENTS_DIR", "documents")
    chroma_dir = os.getenv("CHROMA_DB_PATH", "chroma_db")
    DOCUMENTS_DIR: Path = Path(docs_dir) if Path(docs_dir).is_absolute() else BASE_DIR / docs_dir
    CHROMA_DB_PATH: Path = Path(chroma_dir) if Path(chroma_dir).is_absolute() else BASE_DIR / chroma_dir
    
    # RAG configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        cls.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

# Initialize directories
Config.ensure_directories()

