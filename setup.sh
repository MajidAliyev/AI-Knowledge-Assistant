#!/bin/bash

echo "🚀 Setting up Personal AI Knowledge Assistant..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.ai"
    exit 1
fi

echo "✅ Ollama found"

# Setup backend
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p documents
mkdir -p chroma_db

# Check if models are available
echo "🔍 Checking Ollama models..."
if ! ollama list | grep -q "mistral\|llama3\|phi3"; then
    echo "⚠️  No models found. Pulling mistral model..."
    ollama pull mistral
fi

# Pull embedding model if needed
if ! ollama list | grep -q "nomic-embed-text"; then
    echo "📥 Pulling embedding model..."
    ollama pull nomic-embed-text
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  2. Start frontend: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"

