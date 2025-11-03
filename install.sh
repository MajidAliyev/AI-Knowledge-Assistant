#!/bin/bash

# Professional AI Knowledge Assistant - Installation Script
# This script makes installation super easy - just download and run!

set -e  # Exit on error

echo "🚀 AI Knowledge Assistant - Installation Script"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9+ from https://www.python.org/${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama is not installed.${NC}"
    echo -e "${YELLOW}   Please install from https://ollama.ai${NC}"
    echo -e "${YELLOW}   After installation, run: ollama pull mistral && ollama pull nomic-embed-text${NC}"
else
    echo -e "${GREEN}✅ Ollama found${NC}"
fi

echo ""
echo -e "${BLUE}📦 Installing backend dependencies...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt --quiet

echo -e "${GREEN}✅ Backend dependencies installed${NC}"
cd ..

echo ""
echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
cd frontend

# Install npm dependencies
npm install --silent

echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
cd ..

# Create necessary directories
echo ""
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p documents
mkdir -p chroma_db
echo -e "${GREEN}✅ Directories created${NC}"

# Check Ollama models
echo ""
echo -e "${BLUE}🔍 Checking Ollama models...${NC}"
if command -v ollama &> /dev/null; then
    if ! ollama list 2>/dev/null | grep -q "mistral"; then
        echo -e "${YELLOW}⚠️  Mistral model not found. Pulling...${NC}"
        ollama pull mistral || echo -e "${YELLOW}⚠️  Could not pull mistral. Please run manually: ollama pull mistral${NC}"
    else
        echo -e "${GREEN}✅ Mistral model found${NC}"
    fi
    
    if ! ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
        echo -e "${YELLOW}⚠️  Embedding model not found. Pulling...${NC}"
        ollama pull nomic-embed-text || echo -e "${YELLOW}⚠️  Could not pull embedding model. Please run manually: ollama pull nomic-embed-text${NC}"
    else
        echo -e "${GREEN}✅ Embedding model found${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo -e "${BLUE}🚀 To start the application:${NC}"
echo ""
echo -e "   ${YELLOW}Option 1: Use the start script${NC}"
echo "   ./start.sh"
echo ""
echo -e "   ${YELLOW}Option 2: Manual start${NC}"
echo "   Terminal 1 (Backend):"
echo "   cd backend && source venv/bin/activate && python run.py"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   cd frontend && npm run dev"
echo ""
echo -e "   Then open ${GREEN}http://localhost:5173${NC} in your browser"
echo ""

