"""
Vector Embedding Service for Islamic Texts
Uses sentence-transformers to create embeddings for semantic search
"""
import os
import json
import pickle
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingService:
    """Handles text embeddings for semantic search"""
    
    def __init__(self):
        self.model = None
        self.embeddings_cache = {}
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        try:
            print("📥 Loading embedding model...")
            # Using a multilingual model that supports Arabic
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("✅ Embedding model loaded")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            print("Using fallback keyword search")
    
    def embed_text(self, text: str) -> Optional[List[float]]:
        """Create embedding for a single text"""
        if not self.model:
            return None
        
        # Check cache first
        cache_key = hash(text)
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            embedding_list = embedding.tolist()
            self.embeddings_cache[cache_key] = embedding_list
            return embedding_list
        except Exception as e:
            print(f"Embedding error: {e}")
            return None
    
    def embed_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Create embeddings for multiple texts"""
        if not self.model:
            return None
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            print(f"Batch embedding error: {e}")
            return None
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def search_similar(self, query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """Search for most similar documents to query"""
        query_embedding = self.embed_text(query)
        if not query_embedding:
            return []
        
        results = []
        for doc in documents:
            if 'embedding' in doc and doc['embedding']:
                similarity = self.cosine_similarity(query_embedding, doc['embedding'])
                results.append({
                    'document': doc,
                    'similarity': float(similarity)
                })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

# Global instance
embedding_service = EmbeddingService()