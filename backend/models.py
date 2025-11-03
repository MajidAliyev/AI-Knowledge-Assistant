"""
Pydantic models for API request/response schemas.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Individual chat message."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
    sources: Optional[List[Dict[str, Any]]] = None

class ChatRequest(BaseModel):
    """Request model for chat queries."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    """Response model for chat queries."""
    message: str
    sources: List[Dict[str, Any]]
    model: str

class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str
    top_k: Optional[int] = None

class SearchResponse(BaseModel):
    """Response model for semantic search."""
    results: List[Dict[str, Any]]
    query: str

class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    file_path: Optional[str] = None
    directory: Optional[str] = None

class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    success: bool
    message: str
    files_processed: int
    chunks_created: int

class StatusResponse(BaseModel):
    """Response model for system status."""
    status: str
    documents_indexed: int
    chunks_stored: int
    model: str
    embedding_model: str

