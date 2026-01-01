"""
Material Classifier
Classifies material type: wood, clay, fabric, metal, stone, mixed
Uses rule-based approach for MVP (can be upgraded to CNN later)
"""

import cv2
import numpy as np
from typing import Dict, List


class MaterialClassifier:
    """Classifies material type from image features"""
    
    def __init__(self):
        """Initialize material classifier"""
        self.material_classes = ['wood', 'clay', 'fabric', 'metal', 'stone', 'mixed']
    
    def classify(self, image: np.ndarray) -> Dict:
        """
        Classify material type
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with material classification and probabilities
        """
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Extract features for material classification
        features = self._extract_material_features(image, hsv, gray)
        
        # Classify using rule-based approach
        probabilities = self._classify_material(features)
        
        # Get predicted class
        predicted_class = self.material_classes[np.argmax(probabilities)]
        
        # Create probability vector (normalized)
        prob_vector = np.array(probabilities, dtype=np.float32)
        prob_vector = prob_vector / max(prob_vector.sum(), 1.0)
        
        return {
            'predicted_material': predicted_class,
            'probabilities': {
                cls: float(prob) for cls, prob in zip(self.material_classes, probabilities)
            },
            'confidence': float(np.max(probabilities)),
            'feature_vector': prob_vector
        }
    
    def _extract_material_features(self, image: np.ndarray, hsv: np.ndarray, gray: np.ndarray) -> Dict:
        """Extract features relevant for material classification"""
        # Color features
        mean_hue = np.mean(hsv[:, :, 0])
        mean_saturation = np.mean(hsv[:, :, 1])
        mean_value = np.mean(hsv[:, :, 2])
        
        # Texture features
        texture_variance = np.var(gray)
        edge_density = np.mean(cv2.Canny(gray, 50, 150) > 0)
        
        # Reflectivity (brightness distribution)
        brightness_std = np.std(hsv[:, :, 2])
        
        # Surface properties
        laplacian_var = np.var(cv2.Laplacian(gray, cv2.CV_64F))
        
        return {
            'mean_hue': mean_hue,
            'mean_saturation': mean_saturation,
            'mean_value': mean_value,
            'texture_variance': texture_variance,
            'edge_density': edge_density,
            'brightness_std': brightness_std,
            'laplacian_var': laplacian_var
        }
    
    def _classify_material(self, features: Dict) -> List[float]:
        """Classify material using rule-based approach"""
        scores = {
            'wood': 0.0,
            'clay': 0.0,
            'fabric': 0.0,
            'metal': 0.0,
            'stone': 0.0,
            'mixed': 0.0
        }
        
        # Wood: brown/orange hues, moderate texture, organic patterns
        if 10 < features['mean_hue'] < 30:  # Orange/brown range
            scores['wood'] += 0.3
        if 0.3 < features['mean_saturation'] < 0.7:
            scores['wood'] += 0.2
        if features['texture_variance'] > 500:
            scores['wood'] += 0.3
        if 0.1 < features['edge_density'] < 0.3:
            scores['wood'] += 0.2
        
        # Clay: earthy tones, low reflectivity, smooth texture
        if 15 < features['mean_hue'] < 25 or 0 < features['mean_hue'] < 10:
            scores['clay'] += 0.3
        if features['mean_value'] < 150:  # Not too bright
            scores['clay'] += 0.2
        if features['texture_variance'] < 1000:
            scores['clay'] += 0.3
        if features['brightness_std'] < 30:
            scores['clay'] += 0.2
        
        # Fabric: varied colors, texture patterns, moderate reflectivity
        if features['mean_saturation'] > 0.4:
            scores['fabric'] += 0.2
        if features['texture_variance'] > 300:
            scores['fabric'] += 0.3
        if 0.2 < features['edge_density'] < 0.4:
            scores['fabric'] += 0.3
        if features['laplacian_var'] > 100:
            scores['fabric'] += 0.2
        
        # Metal: high reflectivity, sharp edges, cool colors
        if features['mean_value'] > 180:  # Bright
            scores['metal'] += 0.3
        if features['brightness_std'] > 40:  # High variance (reflections)
            scores['metal'] += 0.3
        if features['edge_density'] > 0.3:  # Sharp edges
            scores['metal'] += 0.2
        if 100 < features['mean_hue'] < 130:  # Blue/gray range
            scores['metal'] += 0.2
        
        # Stone: gray tones, moderate texture, low reflectivity
        if 0 < features['mean_saturation'] < 0.3:  # Low saturation (gray)
            scores['stone'] += 0.3
        if 100 < features['mean_value'] < 180:
            scores['stone'] += 0.2
        if 200 < features['texture_variance'] < 800:
            scores['stone'] += 0.3
        if features['edge_density'] < 0.25:
            scores['stone'] += 0.2
        
        # Mixed: if no strong signal, likely mixed
        max_score = max(scores.values())
        if max_score < 0.5:
            scores['mixed'] = 0.5
        
        # Convert to probabilities (softmax-like)
        score_values = np.array(list(scores.values()))
        # Add small epsilon to avoid zeros
        score_values = score_values + 0.1
        probabilities = score_values / score_values.sum()
        
        return probabilities.tolist()


