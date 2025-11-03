"""
Vector store management using ChromaDB for embedding storage and retrieval.
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
from config import Config

class VectorStore:
    """Manages vector storage and retrieval using ChromaDB."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.PersistentClient(
            path=str(Config.CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None
    ) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            texts: List of text chunks
            metadatas: List of metadata dicts for each chunk
            embeddings: Optional pre-computed embeddings
            
        Returns:
            List of document IDs
        """
        # Generate IDs based on content and metadata
        ids = []
        for i, (text, metadata) in enumerate(zip(texts, metadatas)):
            # Create unique ID from content hash and metadata
            content_hash = hashlib.md5(
                f"{text}_{metadata.get('source', '')}_{metadata.get('chunk_index', i)}".encode()
            ).hexdigest()
            ids.append(content_hash)
        
        # Add to collection
        # Note: ChromaDB requires embeddings to be provided if using custom embeddings
        # If embeddings are None, we'll let ChromaDB handle it (but we're using custom embeddings)
        if embeddings and len(embeddings) > 0:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
        else:
            # ChromaDB will compute embeddings if not provided (requires embedding function)
            # For now, we always provide embeddings from Ollama
            raise ValueError("Embeddings must be provided for this implementation")
        
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Query vector embedding
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of search results with documents, metadatas, and distances
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            'total_documents': count
        }
    
    def delete_by_source(self, source: str) -> bool:
        """
        Delete all documents from a specific source.
        
        Args:
            source: Source file path
            
        Returns:
            True if successful
        """
        try:
            # Get all documents with this source
            results = self.collection.get(
                where={"source": source}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            
            return True
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
    
    def reset(self):
        """Reset the entire collection (use with caution!)."""
        try:
            self.client.delete_collection(name="documents")
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error resetting collection: {e}")

# Global instance
vector_store = VectorStore()

