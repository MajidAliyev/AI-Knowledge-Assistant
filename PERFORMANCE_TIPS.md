# Performance Tips

## Why Is It Slow?

If queries are taking forever (30-60+ seconds), here's what's happening:

### First Query Takes Forever

The very first query after starting Ollama can take 30-60 seconds. That's normal - Ollama needs to load the model into memory. After that, it's much faster (usually 10-30 seconds).

### Use Faster Models

I default to `phi3` because it's fast. If you changed it to something bigger, that's why it's slow.

Edit `backend/.env`:
```
OLLAMA_MODEL=phi3  # This is the fastest
```

Models from fastest to slowest:
- `phi3` - Fastest, still good quality (3.8GB)
- `mistral` - Balanced (4.4GB)
- `llama3` - Better quality but slower (varies by size)

### Response Length

I already limit responses to 256 tokens to keep things snappy. If you want longer answers, you can change it in `backend/rag.py`, but it'll be slower.

### No Documents Yet?

If you haven't uploaded any documents, responses are instant (1-2 seconds). Once you add docs and it starts using RAG, it takes longer because it has to search and generate.

### System Requirements

- 8GB+ RAM recommended
- Close other heavy apps
- SSD helps a lot

### Check Ollama

See what's going on:
```bash
ollama list  # See what models you have
ollama ps    # See what's running
```

### GPU Acceleration

If you have a decent GPU, Ollama will use it automatically. Makes a huge difference.

## Expected Times

- **No documents**: 1-2 seconds
- **First query with docs**: 30-60 seconds (model loading)
- **Subsequent queries**: 10-30 seconds

## If It Always Times Out

1. Check Ollama: `ollama list`
2. Try phi3: `ollama pull phi3`
3. Update `.env`: `OLLAMA_MODEL=phi3`
4. Restart backend
