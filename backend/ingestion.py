"""
Document ingestion pipeline for processing PDFs, Markdown, text files, and emails.
"""
import os
import fitz  # PyMuPDF
import email
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
from config import Config
from vector_store import vector_store

# Configure Ollama client
ollama_client = ollama.Client(host=Config.OLLAMA_BASE_URL)

class DocumentIngester:
    """Handles ingestion of various document types."""
    
    def __init__(self):
        """Initialize the ingester with text splitter."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def extract_text_from_markdown(self, file_path: Path) -> str:
        """Extract text from Markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading Markdown {file_path}: {e}")
            return ""
    
    def extract_text_from_text(self, file_path: Path) -> str:
        """Extract text from plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""
    
    def extract_text_from_email(self, file_path: Path) -> str:
        """Extract text from .eml email file."""
        try:
            with open(file_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)
            
            text_parts = []
            
            # Get subject
            subject = msg.get('Subject', '')
            if subject:
                text_parts.append(f"Subject: {subject}")
            
            # Get sender
            sender = msg.get('From', '')
            if sender:
                text_parts.append(f"From: {sender}")
            
            # Get date
            date = msg.get('Date', '')
            if date:
                text_parts.append(f"Date: {date}")
            
            text_parts.append("\n")
            
            # Get body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            text_parts.append(payload.decode('utf-8', errors='ignore'))
                    elif content_type == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            html = payload.decode('utf-8', errors='ignore')
                            soup = BeautifulSoup(html, 'html.parser')
                            text_parts.append(soup.get_text())
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    content_type = msg.get_content_type()
                    if content_type == "text/html":
                        html = payload.decode('utf-8', errors='ignore')
                        soup = BeautifulSoup(html, 'html.parser')
                        text_parts.append(soup.get_text())
                    else:
                        text_parts.append(payload.decode('utf-8', errors='ignore'))
            
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error reading email {file_path}: {e}")
            return ""
    
    def extract_text(self, file_path: Path) -> Optional[str]:
        """Extract text from file based on extension."""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif suffix in ['.md', '.markdown']:
            return self.extract_text_from_markdown(file_path)
        elif suffix == '.txt':
            return self.extract_text_from_text(file_path)
        elif suffix == '.eml':
            return self.extract_text_from_email(file_path)
        else:
            print(f"Unsupported file type: {suffix}")
            return None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text chunks using Ollama."""
        embeddings = []
        for text in texts:
            try:
                response = ollama_client.embeddings(
                    model=Config.EMBEDDING_MODEL,
                    prompt=text
                )
                embeddings.append(response['embedding'])
            except Exception as e:
                print(f"Error generating embedding: {e}")
                # Return zero vector as fallback
                embeddings.append([0.0] * 384)  # Default dimension
        
        return embeddings
    
    def ingest_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Ingest a single file into the vector store.
        
        Returns:
            Dict with 'success', 'chunks_created', and 'message'
        """
        try:
            # Extract text
            text = self.extract_text(file_path)
            if not text or not text.strip():
                return {
                    'success': False,
                    'chunks_created': 0,
                    'message': f"No text extracted from {file_path.name}"
                }
            
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            
            if not chunks:
                return {
                    'success': False,
                    'chunks_created': 0,
                    'message': f"No chunks created from {file_path.name}"
                }
            
            # Prepare metadata
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadatas.append({
                    'source': str(file_path),
                    'filename': file_path.name,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'file_type': file_path.suffix.lower()
                })
            
            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)
            
            # Store in vector database
            vector_store.add_documents(
                texts=chunks,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            return {
                'success': True,
                'chunks_created': len(chunks),
                'message': f"Successfully ingested {file_path.name}"
            }
        except Exception as e:
            return {
                'success': False,
                'chunks_created': 0,
                'message': f"Error ingesting {file_path.name}: {str(e)}"
            }
    
    def ingest_directory(self, directory: Path) -> Dict[str, Any]:
        """
        Ingest all supported files from a directory.
        
        Returns:
            Dict with 'files_processed', 'total_chunks', 'success', and 'errors'
        """
        supported_extensions = ['.pdf', '.md', '.markdown', '.txt', '.eml']
        files_processed = 0
        total_chunks = 0
        errors = []
        
        # Recursively find all supported files
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                result = self.ingest_file(file_path)
                if result['success']:
                    files_processed += 1
                    total_chunks += result['chunks_created']
                else:
                    errors.append(result['message'])
        
        return {
            'files_processed': files_processed,
            'total_chunks': total_chunks,
            'success': files_processed > 0,
            'errors': errors
        }

# Global instance
ingester = DocumentIngester()

