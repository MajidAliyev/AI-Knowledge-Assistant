# Troubleshooting

## Backend Won't Start

**Getting "Cannot connect to backend server"?**

Check if it's actually running:
```bash
curl http://localhost:8000/api/status
```

If that fails, start it manually:
```bash
cd backend
source venv/bin/activate
python run.py
```

You should see something like:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

If you see errors:
- Check Ollama is running: `ollama list`
- Check Python version: `python --version` (needs 3.9+)
- Look at the error messages in the terminal

### Port Already in Use

See what's using port 8000:
```bash
lsof -i :8000
```

Kill it:
```bash
kill <PID>
```

Or just use a different port in `backend/.env`:
```
PORT=8001
```

### Ollama Not Running

Start it:
```bash
ollama serve
```

Or just open the Ollama app if you installed it that way.

### Virtual Environment Issues

Sometimes the venv gets messed up. Recreate it:
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

Make sure you're in the right directory and venv is activated:
```bash
cd backend
source venv/bin/activate
python -c "from main import app; print('OK')"
```

## Frontend Not Connecting

**Frontend shows connection error?**

1. Make sure backend is running first
2. Backend should be at `http://localhost:8000`
3. Check browser console for CORS errors
4. Verify `CORS_ORIGINS` in `backend/config.py` includes `http://localhost:5173`

## Installation Problems

**Script fails?**

Do it manually:

Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

Make sure you have:
- Python 3.9+: `python3 --version`
- Node.js 18+: `node --version`
- Ollama: `ollama --version`

## Still Having Issues?

1. Check the logs:
   - Backend: terminal output from `python run.py`
   - Frontend: browser console (F12)

2. Verify everything is running:
   ```bash
   ollama list
   curl http://localhost:8000/api/status
   ```

3. Try restarting:
   ```bash
   pkill -f "python.*run.py"
   pkill -f "vite"
   ./start.sh
   ```
