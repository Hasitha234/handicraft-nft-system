"""
Pattern and Detail Feature Extractor
Extracts: SIFT/ORB keypoints, local descriptors, pattern density, decorative details
"""

import cv2
import numpy as np
from typing import Dict, Tuple


class PatternExtractor:
    """Extracts pattern and detail features from images"""
    
    def __init__(self, max_keypoints: int = 500):
        """
        Initialize pattern extractor
        
        Args:
            max_keypoints: Maximum number of keypoints to detect
        """
        self.max_keypoints = max_keypoints
        # Initialize ORB detector (faster than SIFT, good for real-time)
        self.orb = cv2.ORB_create(nfeatures=max_keypoints)
    
    def extract(self, image: np.ndarray) -> Dict:
        """
        Extract all pattern features from image
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with pattern features and feature vector
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Detect keypoints and compute descriptors
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        
        if descriptors is None or len(keypoints) == 0:
            # Return zero vector if no keypoints found
            feature_vector = np.zeros(256, dtype=np.float32)
            return {
                'keypoint_count': 0,
                'pattern_density': 0.0,
                'descriptor_vector': feature_vector,
                'feature_vector': feature_vector
            }
        
        # Convert descriptors to fixed-length vector (VLAD-like approach)
        descriptor_vector = self._descriptors_to_vector(descriptors)
        
        # Pattern density
        pattern_density = len(keypoints) / (image.shape[0] * image.shape[1] / 10000.0)
        pattern_density = min(pattern_density / 100.0, 1.0)  # Normalize
        
        # Pattern distribution (how spread out keypoints are)
        pattern_distribution = self._calculate_pattern_distribution(keypoints, image.shape)
        
        # Decorative detail strength
        detail_strength = self._calculate_detail_strength(keypoints, descriptors)
        
        # Create feature vector
        feature_vector = np.concatenate([
            descriptor_vector,
            np.array([pattern_density, pattern_distribution, detail_strength])
        ]).astype(np.float32)
        
        # Normalize to unit vector
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return {
            'keypoint_count': len(keypoints),
            'pattern_density': float(pattern_density),
            'pattern_distribution': float(pattern_distribution),
            'detail_strength': float(detail_strength),
            'descriptor_vector': descriptor_vector.tolist(),
            'feature_vector': feature_vector
        }
    
    def _descriptors_to_vector(self, descriptors: np.ndarray) -> np.ndarray:
        """
        Convert variable-length descriptors to fixed-length vector
        Uses a simplified VLAD (Vector of Locally Aggregated Descriptors) approach
        """
        if len(descriptors) == 0:
            return np.zeros(256, dtype=np.float32)
        
        # Simple approach: compute statistics of descriptors
        # Mean, std, min, max of each descriptor dimension
        desc_mean = np.mean(descriptors, axis=0)
        desc_std = np.std(descriptors, axis=0)
        desc_min = np.min(descriptors, axis=0)
        desc_max = np.max(descriptors, axis=0)
        
        # Combine statistics
        stats_vector = np.concatenate([desc_mean, desc_std, desc_min, desc_max])
        
        # If too long, truncate; if too short, pad
        target_length = 256
        if len(stats_vector) > target_length:
            stats_vector = stats_vector[:target_length]
        elif len(stats_vector) < target_length:
            padding = np.zeros(target_length - len(stats_vector))
            stats_vector = np.concatenate([stats_vector, padding])
        
        # Normalize
        stats_vector = stats_vector.astype(np.float32)
        norm = np.linalg.norm(stats_vector)
        if norm > 0:
            stats_vector = stats_vector / norm
        
        return stats_vector
    
    def _calculate_pattern_distribution(self, keypoints: list, image_shape: Tuple[int, int]) -> float:
        """Calculate how evenly distributed keypoints are"""
        if len(keypoints) == 0:
            return 0.0
        
        # Get keypoint positions
        positions = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints])
        
        # Calculate spread (standard deviation of positions)
        x_std = np.std(positions[:, 0]) / image_shape[1]
        y_std = np.std(positions[:, 1]) / image_shape[0]
        
        # Higher spread = better distribution
        distribution = (x_std + y_std) / 2.0
        return min(distribution, 1.0)
    
    def _calculate_detail_strength(self, keypoints: list, descriptors: np.ndarray) -> float:
        """Calculate strength of decorative details"""
        if len(keypoints) == 0:
            return 0.0
        
        # Use response strength of keypoints (how strong the feature is)
        responses = np.array([kp.response for kp in keypoints])
        detail_strength = np.mean(responses) / 255.0  # Normalize
        
        return min(detail_strength, 1.0)


