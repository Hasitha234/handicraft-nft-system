"""
Enhanced Vector Store with Multi-Feature Support
Stores CLIP embeddings + all physical features
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Optional

from app.models.search import SearchResult
from app.services.similarity_scorer import SimilarityScorer


class EnhancedVectorStore:
    """Enhanced vector store supporting multiple feature types"""
    
    def __init__(self, index_path: str = "data/faiss_index.idx", 
                 metadata_path: str = "data/metadata.pkl",
                 features_path: str = "data/features.pkl"):
        """
        Initialize enhanced vector store
        
        Args:
            index_path: Path to FAISS index (for CLIP embeddings)
            metadata_path: Path to product metadata
            features_path: Path to store all extracted features
        """
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.features_path = features_path
        
        # Create data directory
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        self.index: Optional[faiss.Index] = None  # CLIP index
        self.products: List[Dict] = []  # Product metadata
        self.features: Dict[str, Dict] = {}  # All extracted features per product
        self.embedding_dim: Optional[int] = None
        self.similarity_scorer = SimilarityScorer()
    
    def load_or_create_index(self, clip_encoder, create_sample_data: bool = True):
        """Load or create index"""
        self.embedding_dim = clip_encoder.embedding_dim
        
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print(f"[INFO] Loading existing index from {self.index_path}")
            self._load_index()
        else:
            print("[INFO] Creating new FAISS index")
            self._create_index()
            if create_sample_data and len(self.products) == 0:
                print("[INFO] Creating sample products...")
                self._create_sample_data(clip_encoder)
    
    def _create_index(self):
        """Create new FAISS index"""
        self.index = faiss.IndexFlatL2(self.embedding_dim)
    
    def _load_index(self):
        """Load index and metadata"""
        self.index = faiss.read_index(self.index_path)
        
        with open(self.metadata_path, 'rb') as f:
            metadata = pickle.load(f)
            self.products = metadata.get('products', [])
        
        # Load features if available
        if os.path.exists(self.features_path):
            with open(self.features_path, 'rb') as f:
                self.features = pickle.load(f)
        
        print(f"[OK] Loaded {len(self.products)} products from index")
        print(f"[OK] Loaded features for {len(self.features)} products")
    
    def _save_index(self):
        """Save index, metadata, and features"""
        faiss.write_index(self.index, self.index_path)
        
        metadata = {'products': self.products}
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        with open(self.features_path, 'wb') as f:
            pickle.dump(self.features, f)
        
        print(f"[OK] Saved index with {len(self.products)} products")
    
    def add_product(self, product_id: str, clip_embedding: np.ndarray, 
                   all_features: Dict, metadata: Dict):
        """
        Add product with all features
        
        Args:
            product_id: Unique product ID
            clip_embedding: CLIP embedding
            all_features: All extracted features (geometric, color, etc.)
            metadata: Product metadata
        """
        if self.index is None:
            raise RuntimeError("Index not initialized")
        
        # Add CLIP embedding to FAISS
        embedding = clip_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        
        # Store metadata
        product_data = {
            'id': product_id,
            'metadata': metadata
        }
        self.products.append(product_data)
        
        # Store all features
        self.features[product_id] = all_features
        
        self._save_index()
    
    def search_with_features(self, query_clip: np.ndarray, query_features: Dict, 
                            top_k: int = 5) -> List[SearchResult]:
        """
        Search using CLIP + all physical features
        
        Args:
            query_clip: CLIP embedding
            query_features: All extracted features from query
            top_k: Number of results
            
        Returns:
            List of SearchResult with per-feature scores
        """
        if self.index is None or len(self.products) == 0:
            return []
        
        # Step 1: Fast CLIP search to get candidates
        query = query_clip.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query)
        
        # Get more candidates than needed for re-ranking
        candidate_k = min(top_k * 3, len(self.products))
        distances, indices = self.index.search(query, candidate_k)
        
        # Step 2: Re-rank using all features
        scored_results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx >= len(self.products):
                continue
            
            product = self.products[idx]
            product_id = product['id']
            
            # Get stored features for this product
            if product_id not in self.features:
                # Fallback to CLIP-only similarity
                similarity = max(0.0, 1.0 - (distance / 2.0))
                scored_results.append({
                    'product': product,
                    'similarity': similarity,
                    'per_feature': {'clip': similarity}
                })
                continue
            
            # Convert stored features back to numpy arrays
            db_features_raw = self.features[product_id]
            db_features = self._convert_features_to_numpy(db_features_raw)
            
            # Compute similarity using all features
            similarity_result = self.similarity_scorer.compute_similarity(
                query_features, db_features
            )
            
            scored_results.append({
                'product': product,
                'similarity': similarity_result['final_score'],
                'per_feature': similarity_result['per_feature_scores'],
                'material': db_features.get('material', {}).get('predicted_material'),
                'object_type': db_features.get('object_type', {}).get('predicted_type')
            })
        
        # Sort by final score
        scored_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Convert to SearchResult objects
        results = []
        for i, result in enumerate(scored_results[:top_k]):
            product = result['product']
            metadata = product.get('metadata', {}) or {}
            filename = metadata.get('filename')
            image_url = f"/images/{filename}" if filename else None
            results.append(SearchResult(
                product_id=product['id'],
                title=metadata.get('title', 'Unknown'),
                description=metadata.get('description', ''),
                similarity_score=result['similarity'],
                rank=i + 1,
                per_feature_scores=result.get('per_feature', {}),
                predicted_material=result.get('material'),
                predicted_object_type=result.get('object_type'),
                image_filename=filename,
                image_url=image_url
            ))
        
        return results
    
    def _create_sample_data(self, clip_encoder):
        """Create sample data (for testing)"""
        sample_products = [
            {"id": "MASK_001", "title": "Traditional Sanni Mask", 
             "description": "Hand-carved wooden mask painted in traditional colors"},
            {"id": "WOOD_001", "title": "Carved Elephant Statue", 
             "description": "Small wooden elephant carving with intricate details"},
        ]
        
        for product in sample_products:
            random_embedding = np.random.randn(clip_encoder.embedding_dim).astype('float32')
            random_embedding = random_embedding / np.linalg.norm(random_embedding)
            
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
        
        self._save_index()
        print(f"[OK] Created {len(sample_products)} sample products")
    
    def _convert_features_to_numpy(self, features: Dict) -> Dict:
        """Convert stored features (lists) back to numpy arrays"""
        converted = {}
        
        for key, value in features.items():
            if key == 'clip':
                converted[key] = np.array(value, dtype=np.float32)
            elif isinstance(value, dict):
                if 'feature_vector' in value:
                    # Convert feature vector
                    converted[key] = {
                        **{k: v for k, v in value.items() if k != 'feature_vector'},
                        'feature_vector': np.array(value['feature_vector'], dtype=np.float32)
                    }
                else:
                    # Recursively convert nested dicts
                    converted[key] = self._convert_features_to_numpy(value)
            else:
                converted[key] = value
        
        return converted

