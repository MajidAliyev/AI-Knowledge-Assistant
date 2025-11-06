# Personal AI Knowledge Assistant

I built this because I wanted a way to chat with my own documents - PDFs, notes, emails, everything - without sending anything to the cloud. Everything runs locally on your machine.

## Quick Start

Super simple setup:

```bash
# Clone it
git clone https://github.com/MajidAliyev/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant      

# Install everything
./install.sh

# Start it up
./start.sh

# Open http://localhost:5173
```

That's literally it. The script handles all the setup.

## What It Does

- **Reads your docs**: PDFs, Markdown files, text files, emails - just drop them in
- **Answers questions**: Ask it anything about your documents and it'll find the relevant parts
- **Shows sources**: It tells you exactly where each answer came from
- **100% local**: Nothing leaves your computer. No API calls, no cloud storage, nothing.

## What You Need

- Python 3.9 or newer
- Node.js 18 or newer  
- Ollama installed ([get it here](https://ollama.ai))

## Installation

### Automatic (Easiest)

Just run:
```bash
./install.sh
```

It checks everything, installs dependencies, pulls the AI models, and sets up the whole thing.

### Manual (If You Want Control)

First, install Ollama and pull the models:
```bash
ollama pull phi3
ollama pull nomic-embed-text
```

Then set up the backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

And the frontend:
```bash
cd frontend
npm install
```

### Configuration (Optional)

The defaults work fine, but if you want to customize, create `backend/.env`:

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

## Running It

### Easy Way
```bash
./start.sh
```

Starts both backend and frontend for you.

### Manual Way

In one terminal:
```bash
cd backend
source venv/bin/activate
python run.py
```

In another terminal:
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Adding Documents

You've got a few options:

1. **Through the UI**: Click "Upload Documents" and drag files in
2. **Via API**: `curl -X POST http://localhost:8000/api/ingest -F "file=@your-doc.pdf"`
3. **Just drop files**: Put them in the `documents/` folder and they'll get indexed

## Supported File Types

- PDFs (`.pdf`) - uses PyMuPDF to extract text
- Markdown (`.md`, `.markdown`) - processed as-is
- Text files (`.txt`) - plain text
- Emails (`.eml`) - extracts body and attachments

## Customization

### Switch Models

I default to `phi3` because it's fast. If you want better quality (but slower), edit `backend/.env`:

```
OLLAMA_MODEL=mistral
```

Or try `llama3` if you have the RAM and patience.

### Tweak Chunking

If answers feel disconnected, try bigger chunks:

```
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

### More Context

To get more sources per answer:

```
TOP_K=10
```

## Project Structure

```
.
├── backend/          # FastAPI server
│   ├── main.py       # API endpoints
│   ├── ingestion.py  # Document processing
│   ├── rag.py        # The AI magic
│   ├── vector_store.py
│   └── ...
├── frontend/         # React UI
│   ├── src/
│   └── ...
├── documents/        # Put your docs here
└── chroma_db/        # Vector database (auto-created)
```

## Troubleshooting

**Backend won't start?**
- Make sure Ollama is running: `ollama serve`
- Check the port isn't taken: `lsof -i :8000`
- Verify Python version: `python --version` (needs 3.9+)

**Can't find models?**
- Pull them: `ollama pull phi3`
- Check the model name in `.env` matches what you have

**Import errors?**
- Reinstall: `pip install -r requirements.txt`
- Make sure you activated the venv

## Future Ideas

Stuff I'm thinking about adding:
- Multi-user support
- Cloud sync (optional)
- Better topic tagging
- Document summaries
- Export chat history

## License

MIT - do whatever you want with it.

## Contributing

Found a bug or want to add something? Open an issue or send a PR. Check [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Thanks

Built with:
- [Ollama](https://ollama.ai) - for running models locally
- [ChromaDB](https://www.trychroma.com/) - vector storage
- [FastAPI](https://fastapi.tiangolo.com/) - backend
- [React](https://react.dev/) - frontend

---

If you find this useful, give it a star ⭐
