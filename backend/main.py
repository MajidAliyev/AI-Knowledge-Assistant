"""
FastAPI application for the Personal AI Knowledge Assistant.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import aiofiles
import os
from typing import List, Optional

from config import Config
from models import (
    ChatRequest, ChatResponse, SearchRequest, SearchResponse,
    IngestResponse, StatusResponse
)
from rag import rag_pipeline
from ingestion import ingester
from vector_store import vector_store

app = FastAPI(
    title="Personal AI Knowledge Assistant",
    description="A fully local, privacy-safe AI assistant for your personal documents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Personal AI Knowledge Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get system status and statistics."""
    try:
        stats = vector_store.get_collection_stats()
        return StatusResponse(
            status="operational",
            documents_indexed=stats['total_documents'],
            chunks_stored=stats['total_documents'],
            model=Config.OLLAMA_MODEL,
            embedding_model=Config.EMBEDDING_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat queries with RAG."""
    try:
        # Convert conversation history format if needed
        conversation_history = None
        if request.conversation_history:
            conversation_history = [
                {
                    'role': msg.role,
                    'content': msg.content
                }
                for msg in request.conversation_history
            ]
        
        # Process query through RAG pipeline
        result = rag_pipeline.query(
            query=request.message,
            conversation_history=conversation_history
        )
        
        return ChatResponse(
            message=result['answer'],
            sources=result['sources'],
            model=result['model']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Semantic search across documents."""
    try:
        # Retrieve relevant chunks
        chunks = rag_pipeline.retrieve_context(
            query=request.query,
            top_k=request.top_k or Config.TOP_K
        )
        
        # Format results
        results = []
        for chunk in chunks:
            metadata = chunk.get('metadata', {})
            results.append({
                'text': chunk.get('text', ''),
                'source': metadata.get('source', ''),
                'filename': metadata.get('filename', 'Unknown'),
                'chunk_index': metadata.get('chunk_index', 0),
                'similarity': 1 - chunk.get('distance', 0) if chunk.get('distance') else None
            })
        
        return SearchResponse(
            results=results,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_file(file: Optional[UploadFile] = File(None)):
    """Ingest a single uploaded file."""
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Save uploaded file temporarily
        temp_path = Config.DOCUMENTS_DIR / file.filename
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Ingest file
        result = ingester.ingest_file(temp_path)
        
        # Optionally delete temp file (keep it for now)
        # temp_path.unlink()
        
        return IngestResponse(
            success=result['success'],
            message=result['message'],
            files_processed=1 if result['success'] else 0,
            chunks_created=result['chunks_created']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting file: {str(e)}")

@app.post("/api/ingest/directory", response_model=IngestResponse)
async def ingest_directory():
    """Ingest all files from the configured documents directory."""
    try:
        result = ingester.ingest_directory(Config.DOCUMENTS_DIR)
        
        return IngestResponse(
            success=result['success'],
            message=f"Processed {result['files_processed']} files. {len(result['errors'])} errors.",
            files_processed=result['files_processed'],
            chunks_created=result['total_chunks']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting directory: {str(e)}")

@app.post("/api/ingest/path", response_model=IngestResponse)
async def ingest_path(path: str):
    """Ingest files from a specific path."""
    try:
        target_path = Path(path)
        if not target_path.exists():
            raise HTTPException(status_code=404, detail="Path does not exist")
        
        if target_path.is_file():
            result = ingester.ingest_file(target_path)
            return IngestResponse(
                success=result['success'],
                message=result['message'],
                files_processed=1 if result['success'] else 0,
                chunks_created=result['chunks_created']
            )
        else:
            result = ingester.ingest_directory(target_path)
            return IngestResponse(
                success=result['success'],
                message=f"Processed {result['files_processed']} files.",
                files_processed=result['files_processed'],
                chunks_created=result['total_chunks']
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting path: {str(e)}")

@app.delete("/api/reset")
async def reset_database():
    """Reset the vector database (use with caution!)."""
    try:
        vector_store.reset()
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        reload_exclude=["venv/*", "*.pyc", "__pycache__/*", ".git/*", "chroma_db/*"]
    )

