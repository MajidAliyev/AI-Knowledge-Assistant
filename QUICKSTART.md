# Quick Start

Get it running in like 5 minutes.

## Check You Have Everything

Run these to make sure:
- `python3 --version` (needs 3.9+)
- `node --version` (needs 18+)
- `ollama --version` (if not installed, get it from [ollama.ai](https://ollama.ai))

## Setup

Run the script:
```bash
./install.sh
```

It does everything - sets up the Python environment, installs packages, pulls the AI models, creates directories.

## Manual Setup (If You Prefer)

1. **Get the models:**
   ```bash
   ollama pull phi3
   ollama pull nomic-embed-text
   ```

2. **Backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend:**
   ```bash
   cd frontend
   npm install
   ```

## Start It

Either:
```bash
./start.sh
```

Or manually:
- Terminal 1: `cd backend && source venv/bin/activate && python run.py`
- Terminal 2: `cd frontend && npm run dev`

Then go to http://localhost:5173

## First Steps

1. Upload a document (click the button or drag a file)
2. Ask it something like "What's this document about?"
3. Check the sources to see where the answer came from

## Common Issues

**Ollama not running?**
```bash
ollama serve
```

**Port taken?**
Change it in `backend/.env` or `frontend/vite.config.js`

**Models missing?**
```bash
ollama pull phi3
ollama pull nomic-embed-text
```

**Import errors?**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

- Add more documents to the `documents/` folder
- Play with settings in `backend/.env`
- Check out the API docs at http://localhost:8000/docs
