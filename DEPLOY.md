# Deployment

## Local Development

Just run:
```bash
./install.sh
./start.sh
```

Or manually:
- Backend: `cd backend && source venv/bin/activate && python run.py`
- Frontend: `cd frontend && npm run dev`

## Production Build

For the frontend:
```bash
cd frontend
npm run build
```

Output goes to `frontend/dist/`

## Environment Variables

Create `backend/.env` if you want to customize:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3
EMBEDDING_MODEL=nomic-embed-text
DOCUMENTS_DIR=documents
CHROMA_DB_PATH=chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
```

## Docker

Maybe I'll add Docker support later. For now, it's meant to run locally.
