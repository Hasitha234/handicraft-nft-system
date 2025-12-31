"""
Vector database service using FAISS
Stores product embeddings and performs similarity search
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Optional
from pathlib import Path

from app.models.search import SearchResult


class VectorStore:
    """FAISS-based vector store for product embeddings"""
    
    def __init__(self, index_path: str = "data/faiss_index.idx", metadata_path: str = "data/metadata.pkl"):
        """
        Initialize vector store
        
        Args:
            index_path: Path to save/load FAISS index
            metadata_path: Path to save/load product metadata
        """
        self.index_path = index_path
        self.metadata_path = metadata_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        self.index: Optional[faiss.Index] = None
        self.products: List[Dict] = []  # Product metadata list
        self.embedding_dim: Optional[int] = None
    
    def load_or_create_index(self, clip_encoder, create_sample_data: bool = True):
        """
        Load existing index or create new one
        
        Args:
            clip_encoder: CLIPEncoder instance (to get embedding dimension)
            create_sample_data: If True and index is empty, create sample products
        """
        self.embedding_dim = clip_encoder.embedding_dim
        
        # Try to load existing index
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print(f"[INFO] Loading existing index from {self.index_path}")
            self._load_index()
        else:
            print("[INFO] Creating new FAISS index")
            self._create_index()
            
            # Create sample data if requested (for testing without real products)
            if create_sample_data and len(self.products) == 0:
                print("[INFO] Creating sample products for testing...")
                self._create_sample_data(clip_encoder)
                # Note: _create_sample_data already saves via add_product calls
    
    def _create_index(self):
        """Create a new FAISS index"""
        # Use L2 (Euclidean) distance index
        # Since embeddings are normalized, L2 distance is equivalent to cosine distance
        self.index = faiss.IndexFlatL2(self.embedding_dim)
    
    def _load_index(self):
        """Load index and metadata from disk"""
        # Load FAISS index
        self.index = faiss.read_index(self.index_path)
        
        # Load metadata
        with open(self.metadata_path, 'rb') as f:
            metadata = pickle.load(f)
            self.products = metadata.get('products', [])
        
        print(f"[OK] Loaded {len(self.products)} products from index")
    
    def _save_index(self):
        """Save index and metadata to disk"""
        # Save FAISS index
        faiss.write_index(self.index, self.index_path)
        
        # Save metadata
        metadata = {'products': self.products}
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"[OK] Saved index with {len(self.products)} products")
    
    def add_product(self, product_id: str, embedding: np.ndarray, metadata: Dict):
        """
        Add a product to the vector store
        
        Args:
            product_id: Unique product identifier
            embedding: CLIP embedding vector (should be normalized)
            metadata: Product metadata (title, description, etc.)
        """
        if self.index is None:
            raise RuntimeError("Index not initialized. Call load_or_create_index() first.")
        
        # Ensure embedding is the right shape and type
        embedding = embedding.reshape(1, -1).astype('float32')
        
        # Ensure embedding is normalized (L2 norm = 1)
        faiss.normalize_L2(embedding)
        
        # Add to FAISS index
        self.index.add(embedding)
        
        # Store metadata
        product_data = {
            'id': product_id,
            'metadata': metadata
        }
        self.products.append(product_data)
        
        # Save after each addition (simple for MVP, batch saves better for production)
        self._save_index()
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """
        Search for similar products
        
        Args:
            query_embedding: Query image embedding (should be normalized)
            top_k: Number of results to return
            
        Returns:
            List of SearchResult objects sorted by similarity (highest first)
        """
        if self.index is None or len(self.products) == 0:
            return []
        
        # Prepare query embedding
        query = query_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query)  # Ensure normalization
        
        # Search
        k = min(top_k, len(self.products))  # Don't ask for more than we have
        distances, indices = self.index.search(query, k)
        
        # Convert to SearchResult objects
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.products):  # Valid index
                product = self.products[idx]
                metadata = product.get('metadata', {}) or {}
                filename = metadata.get('filename')
                image_url = f"/images/{filename}" if filename else None
                
                # Convert L2 distance to similarity score (0-1)
                # For normalized vectors, L2 distance = 2 * (1 - cosine similarity)
                # So similarity = 1 - (distance / 2)
                similarity = max(0.0, 1.0 - (distance / 2.0))
                
                result = SearchResult(
                    product_id=product['id'],
                    title=metadata.get('title', 'Unknown'),
                    description=metadata.get('description', ''),
                    similarity_score=float(similarity),
                    rank=i + 1,
                    image_filename=filename,
                    image_url=image_url
                )
                results.append(result)
        
        return results
    
    def _create_sample_data(self, clip_encoder):
        """
        Create sample product data for testing
        This generates random embeddings - in production, use real product images
        """
        # Generate random normalized embeddings for 5 sample products
        sample_products = [
            {"id": "MASK_001", "title": "Traditional Sanni Mask", "description": "Hand-carved wooden mask painted in traditional colors"},
            {"id": "WOOD_001", "title": "Carved Elephant Statue", "description": "Small wooden elephant carving with intricate details"},
            {"id": "BATIK_001", "title": "Traditional Batik Wall Hanging", "description": "Hand-painted batik with peacock design"},
            {"id": "BRASS_001", "title": "Brass Oil Lamp", "description": "Traditional brass oil lamp with decorative engravings"},
            {"id": "POT_001", "title": "Terracotta Pot", "description": "Handcrafted clay pot with natural finish"},
        ]
        
        for product in sample_products:
            # Generate random normalized embedding
            # In production, replace this with actual CLIP encoding of product images
            random_embedding = np.random.randn(clip_encoder.embedding_dim).astype('float32')
            random_embedding = random_embedding / np.linalg.norm(random_embedding)
            
            # Add product directly (without saving each time)
            embedding = random_embedding.reshape(1, -1).astype('float32')
            faiss.normalize_L2(embedding)
            self.index.add(embedding)
            
            product_data = {
                'id': product["id"],
                'metadata': {
                    "title": product["title"],
                    "description": product["description"]
                }
            }
            self.products.append(product_data)
        
        # Save all sample products at once
        self._save_index()
        print(f"[OK] Created {len(sample_products)} sample products")

