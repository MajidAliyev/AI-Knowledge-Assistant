"""
Retrieval-Augmented Generation (RAG) pipeline for generating cited answers.
"""
import ollama
from typing import List, Dict, Any, Optional
from config import Config
from vector_store import vector_store

# Configure Ollama client
ollama_client = ollama.Client(host=Config.OLLAMA_BASE_URL)

class RAGPipeline:
    """Handles RAG queries with citation extraction."""
    
    def __init__(self):
        """Initialize RAG pipeline."""
        self.model = Config.OLLAMA_MODEL
        self.embedding_model = Config.EMBEDDING_MODEL
        self.top_k = Config.TOP_K
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for query text."""
        try:
            response = ollama_client.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def retrieve_context(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context chunks for a query.
        
        Args:
            query: User query string
            top_k: Number of chunks to retrieve (defaults to config value)
            
        Returns:
            List of relevant chunks with metadata
        """
        if top_k is None:
            top_k = self.top_k
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return []
        
        # Search vector store
        results = vector_store.search(query_embedding, top_k=top_k)
        
        return results
    
    def format_context_with_citations(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Format retrieved chunks into context string with citations.
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get('metadata', {})
            source = metadata.get('filename', metadata.get('source', 'Unknown'))
            chunk_index = metadata.get('chunk_index', 0)
            text = chunk.get('text', '')
            
            context_parts.append(
                f"[Citation {i}] Source: {source}\n"
                f"Chunk {chunk_index + 1}: {text}\n"
            )
        
        return "\n".join(context_parts)
    
    def extract_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract citation information from retrieved chunks.
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        seen_sources = set()
        
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get('metadata', {})
            source = metadata.get('source', '')
            filename = metadata.get('filename', 'Unknown')
            
            # Create unique citation key
            citation_key = f"{source}_{metadata.get('chunk_index', 0)}"
            
            if citation_key not in seen_sources:
                citations.append({
                    'id': i,
                    'source': source,
                    'filename': filename,
                    'chunk_index': metadata.get('chunk_index', 0),
                    'text_preview': chunk.get('text', '')[:200] + '...' if len(chunk.get('text', '')) > 200 else chunk.get('text', ''),
                    'file_type': metadata.get('file_type', '')
                })
                seen_sources.add(citation_key)
        
        return citations
    
    def generate_answer(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate answer using LLM with context.
        
        Args:
            query: User query
            context: Retrieved context with citations
            conversation_history: Previous conversation messages
            
        Returns:
            Generated answer string
        """
        # Build prompt - simplified for faster generation
        system_prompt = """You are a helpful AI assistant. Answer based on the provided context. Use [Citation X] when referencing sources. Be concise."""
        
        user_prompt = f"""Context:
{context}

Question: {query}

Answer briefly based on the context. Cite sources with [Citation X]."""
        
        # Add conversation history if available
        messages = []
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                messages.append({
                    'role': msg.get('role', 'user'),
                    'content': msg.get('content', '')
                })
        
        messages.append({
            'role': 'system',
            'content': system_prompt
        })
        messages.append({
            'role': 'user',
            'content': user_prompt
        })
        
        try:
            # Use options to speed up generation
            response = ollama_client.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.7,
                    'num_predict': 256,  # Shorter responses for faster generation
                    'num_ctx': 2048,  # Limit context window
                }
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"Error generating answer: {e}")
            import traceback
            traceback.print_exc()
            # Provide helpful error message
            error_msg = str(e)
            if 'timeout' in error_msg.lower() or 'connection' in error_msg.lower():
                return "The request took too long or couldn't connect to Ollama. Please ensure Ollama is running and try again. If this persists, the model might be slow - try a simpler question."
            return f"I encountered an error: {error_msg}. Please try again."
    
    def query(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Complete RAG query pipeline.
        
        Args:
            query: User query
            conversation_history: Previous conversation messages
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with 'answer', 'sources', and 'model'
        """
        try:
            # Retrieve relevant context
            chunks = self.retrieve_context(query, top_k=top_k)
            
            if not chunks:
                # If no documents indexed, provide a quick helpful response without slow RAG
                return {
                    'answer': "I don't have any documents indexed yet to answer your question. Please upload some documents using the 'Upload Documents' button first. Supported formats include PDFs, Markdown files, text files, and email (.eml) files. Once you've uploaded documents, I'll be able to help answer questions about them!",
                    'sources': [],
                    'model': self.model
                }
            
            # Format context
            context = self.format_context_with_citations(chunks)
            
            # Generate answer
            answer = self.generate_answer(query, context, conversation_history)
            
            # Extract citations
            citations = self.extract_citations(chunks)
            
            return {
                'answer': answer,
                'sources': citations,
                'model': self.model
            }
        except Exception as e:
            print(f"Error in RAG query: {e}")
            import traceback
            traceback.print_exc()
            return {
                'answer': f"I encountered an error processing your query: {str(e)}. Please try again or check if Ollama is running properly.",
                'sources': [],
                'model': self.model
            }

# Global instance
rag_pipeline = RAGPipeline()

