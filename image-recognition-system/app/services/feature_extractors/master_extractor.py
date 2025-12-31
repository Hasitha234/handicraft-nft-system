"""
Master Feature Extractor
Combines all feature extractors into a single pipeline
"""

import numpy as np
from typing import Dict

from .geometric_extractor import GeometricExtractor
from .color_extractor import ColorExtractor
from .texture_extractor import TextureExtractor
from .pattern_extractor import PatternExtractor
from .material_classifier import MaterialClassifier
from .object_type_classifier import ObjectTypeClassifier


class MasterFeatureExtractor:
    """Master feature extractor that combines all feature types"""
    
    def __init__(self):
        """Initialize all feature extractors"""
        self.geometric = GeometricExtractor()
        self.color = ColorExtractor()
        self.texture = TextureExtractor()
        self.pattern = PatternExtractor()
        self.material = MaterialClassifier()
        self.object_type = ObjectTypeClassifier()
    
    def extract_all(self, image: np.ndarray) -> Dict:
        """
        Extract all features from image
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with all extracted features
        """
        # Extract geometric features first (needed for object type)
        geometric_features = self.geometric.extract(image)
        
        # Extract all other features
        color_features = self.color.extract(image)
        texture_features = self.texture.extract(image)
        pattern_features = self.pattern.extract(image)
        material_features = self.material.classify(image)
        object_type_features = self.object_type.classify(image, geometric_features)
        
        # Combine all feature vectors
        fused_vector = self._fuse_vectors([
            geometric_features['feature_vector'],
            color_features['feature_vector'],
            texture_features['feature_vector'],
            pattern_features['feature_vector'],
            material_features['feature_vector'],
            object_type_features['feature_vector']
        ])
        
        return {
            'geometric': geometric_features,
            'color': color_features,
            'texture': texture_features,
            'pattern': pattern_features,
            'material': material_features,
            'object_type': object_type_features,
            'fused_vector': fused_vector
        }
    
    def _fuse_vectors(self, vectors: list) -> np.ndarray:
        """
        Fuse multiple feature vectors into one
        
        Args:
            vectors: List of feature vectors
            
        Returns:
            Fused feature vector
        """
        # Simple concatenation (can be improved with learned weights)
        fused = np.concatenate(vectors)
        
        # Normalize to unit vector
        norm = np.linalg.norm(fused)
        if norm > 0:
            fused = fused / norm
        
        return fused.astype(np.float32)


