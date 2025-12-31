"""
Similarity Scorer
Computes per-feature similarity scores and weighted fusion
"""

import numpy as np
from typing import Dict, List
from scipy.spatial.distance import cosine


class SimilarityScorer:
    """Computes similarity scores between query and database items"""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize similarity scorer
        
        Args:
            weights: Feature weights for fusion (default weights provided)
        """
        self.weights = weights or {
            'geometric': 0.30,
            'spatial': 0.15,  # Using geometric for now
            'color': 0.15,
            'texture': 0.15,
            'pattern': 0.10,
            'material': 0.10,
            'object_type': 0.05
        }
        
        # Normalize weights
        total = sum(self.weights.values())
        self.weights = {k: v / total for k, v in self.weights.items()}
    
    def compute_similarity(self, query_features: Dict, db_features: Dict) -> Dict:
        """
        Compute similarity scores between query and database item
        
        Args:
            query_features: Features extracted from query image
            db_features: Features from database item
            
        Returns:
            Dictionary with per-feature scores and final score
        """
        scores = {}
        
        # Geometric similarity
        if 'geometric' in query_features and 'geometric' in db_features:
            scores['geometric'] = self._cosine_similarity(
                query_features['geometric']['feature_vector'],
                db_features['geometric']['feature_vector']
            )
        
        # Color similarity
        if 'color' in query_features and 'color' in db_features:
            scores['color'] = self._cosine_similarity(
                query_features['color']['feature_vector'],
                db_features['color']['feature_vector']
            )
        
        # Texture similarity
        if 'texture' in query_features and 'texture' in db_features:
            scores['texture'] = self._cosine_similarity(
                query_features['texture']['feature_vector'],
                db_features['texture']['feature_vector']
            )
        
        # Pattern similarity
        if 'pattern' in query_features and 'pattern' in db_features:
            scores['pattern'] = self._cosine_similarity(
                query_features['pattern']['feature_vector'],
                db_features['pattern']['feature_vector']
            )
        
        # Material similarity (probability overlap)
        if 'material' in query_features and 'material' in db_features:
            scores['material'] = self._probability_similarity(
                query_features['material']['feature_vector'],
                db_features['material']['feature_vector']
            )
        
        # Object type similarity
        if 'object_type' in query_features and 'object_type' in db_features:
            scores['object_type'] = self._probability_similarity(
                query_features['object_type']['feature_vector'],
                db_features['object_type']['feature_vector']
            )
        
        # CLIP similarity (if available)
        if 'clip' in query_features and 'clip' in db_features:
            scores['clip'] = self._cosine_similarity(
                query_features['clip'],
                db_features['clip']
            )
        
        # Compute weighted final score
        final_score = self._weighted_fusion(scores)
        
        return {
            'per_feature_scores': scores,
            'final_score': final_score
        }
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        # Normalize vectors
        vec1 = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2 = vec2 / (np.linalg.norm(vec2) + 1e-8)
        
        # Cosine similarity
        similarity = np.dot(vec1, vec2)
        
        # Convert from [-1, 1] to [0, 1]
        return (similarity + 1.0) / 2.0
    
    def _probability_similarity(self, prob1: np.ndarray, prob2: np.ndarray) -> float:
        """Compute similarity between probability distributions"""
        # Use dot product (Bhattacharyya coefficient)
        similarity = np.dot(np.sqrt(prob1), np.sqrt(prob2))
        return float(similarity)
    
    def _weighted_fusion(self, scores: Dict[str, float]) -> float:
        """Compute weighted fusion of similarity scores"""
        final = 0.0
        total_weight = 0.0
        
        for feature, score in scores.items():
            weight = self.weights.get(feature, 0.0)
            final += weight * score
            total_weight += weight
        
        # Normalize by total weight used
        if total_weight > 0:
            final = final / total_weight
        
        return float(final)


