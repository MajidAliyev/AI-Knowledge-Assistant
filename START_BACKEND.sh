#!/bin/bash

# Simple script to start the backend server
# This ensures the backend is running before you access the frontend

cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./install.sh first"
    exit 1
fi

source venv/bin/activate

echo "🚀 Starting backend server..."
echo "📍 Backend will be available at http://localhost:8000"
echo "📝 API docs will be at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py

