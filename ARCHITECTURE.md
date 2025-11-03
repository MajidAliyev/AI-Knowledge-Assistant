# Architecture

This is how it all fits together.

## The Big Picture

```
Frontend (React) → Backend (FastAPI) → ChromaDB + Ollama
```

The frontend is just the UI. The backend does all the heavy lifting - it talks to Ollama for AI stuff and ChromaDB for storing document embeddings.

## Components

### Frontend
- React with Vite
- TailwindCSS for styling
- Chat interface, upload UI, settings

### Backend
- FastAPI for the API
- Handles document ingestion
- Runs the RAG pipeline
- Manages vector storage

### Storage
- ChromaDB: stores document embeddings (vectors)
- Local files: your actual documents
- Ollama: runs the AI models locally

## How It Works

### Adding Documents

1. You upload a file (PDF, Markdown, etc.)
2. Backend extracts the text
3. It splits the text into chunks
4. Each chunk gets converted to an embedding (vector) using Ollama
5. Embeddings are stored in ChromaDB with metadata (source file, chunk number, etc.)

### Asking Questions

1. You type a question
2. Question gets converted to an embedding
3. Backend searches ChromaDB for similar chunks
4. It grabs the top matches
5. Sends those chunks + your question to Ollama
6. Ollama generates an answer
7. Answer comes back with source citations
8. You see it in the UI

## Tech Stack

**Backend:**
- FastAPI - web framework
- ChromaDB - vector database
- Ollama - AI models
- PyMuPDF - PDF extraction
- BeautifulSoup - HTML parsing
- langchain - text splitting

**Frontend:**
- React - UI
- Vite - build tool
- TailwindCSS - styling
- Axios - HTTP requests
- React Markdown - rendering markdown

## Privacy

Everything stays on your machine:
- Documents are on your disk
- Embeddings are in a local ChromaDB
- Ollama runs locally
- No internet required (except to download models initially)

## Configuration

You can tweak stuff in `backend/.env`:
- Which Ollama model to use
- Chunk sizes
- How many chunks to retrieve
- File paths
