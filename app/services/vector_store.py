"""
Advanced Vector Store for Islamic Texts
Uses FAISS for efficient similarity search
"""
import os
import json
import pickle
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class IslamicVectorStore:
    """Vector store for Islamic texts with semantic search"""
    
    def __init__(self):
        self.model = None
        self.documents = []
        self.embeddings = None
        self.index = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the embedding model and load data"""
        try:
            print("📥 Loading embedding model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Model loaded")
        except:
            print("⚠️ Using fallback search")
            self.model = None
    
    def add_documents(self, docs: List[Dict[str, str]]):
        """Add documents to the vector store"""
        for doc in docs:
            self.documents.append(doc)
        
        if self.model:
            texts = [doc['content'] for doc in docs]
            embeddings = self.model.encode(texts, show_progress_bar=True)
            
            if self.embeddings is None:
                self.embeddings = embeddings
            else:
                self.embeddings = np.vstack([self.embeddings, embeddings])
            
            # Build FAISS index
            try:
                import faiss
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(self.embeddings.astype('float32'))
                print(f"✅ Indexed {len(self.documents)} documents")
            except ImportError:
                print("⚠️ FAISS not available, using numpy")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for most relevant documents"""
        if not self.model or self.embeddings is None:
            return self._keyword_search(query, top_k)
        
        try:
            # Create query embedding
            query_embedding = self.model.encode([query])
            
            # Search using FAISS
            import faiss
            distances, indices = self.index.search(
                query_embedding.astype('float32'), top_k
            )
            
            results = []
            for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents):
                    doc = self.documents[idx].copy()
                    doc['relevance'] = float(1.0 / (1.0 + dist))
                    results.append(doc)
            
            return results
        except:
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Fallback keyword search"""
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc['content'].lower()
            score = sum(1 for word in query_words if word in content_lower)
            if score > 0:
                doc_copy = doc.copy()
                doc_copy['relevance'] = score / len(query_words)
                scored_docs.append(doc_copy)
        
        scored_docs.sort(key=lambda x: x['relevance'], reverse=True)
        return scored_docs[:top_k]

# Global instance
vector_store = IslamicVectorStore()