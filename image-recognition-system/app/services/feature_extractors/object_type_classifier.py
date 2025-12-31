"""
Object Type Classifier
Classifies object type: Mask, Pottery, Jewelry, Textile, Sculpture, Utility
Uses rule-based approach for MVP (can be upgraded to CNN later)
"""

import cv2
import numpy as np
from typing import Dict, List


class ObjectTypeClassifier:
    """Classifies object type from image features"""
    
    def __init__(self):
        """Initialize object type classifier"""
        self.object_types = ['mask', 'pottery', 'jewelry', 'textile', 'sculpture', 'utility']
    
    def classify(self, image: np.ndarray, geometric_features: Dict = None) -> Dict:
        """
        Classify object type
        
        Args:
            image: RGB image array (H, W, 3)
            geometric_features: Optional pre-computed geometric features
            
        Returns:
            Dictionary with object type classification and probabilities
        """
        # Extract features
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        h, w = image.shape[:2]
        aspect_ratio = w / max(h, 1)
        
        # Get geometric features if not provided
        if geometric_features is None:
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                compactness = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
            else:
                compactness = 0
        else:
            compactness = geometric_features.get('compactness', 0)
            aspect_ratio = geometric_features.get('aspect_ratio', aspect_ratio)
        
        # Classify using rule-based approach
        probabilities = self._classify_object_type(image, gray, aspect_ratio, compactness)
        
        # Get predicted class
        predicted_type = self.object_types[np.argmax(probabilities)]
        
        # Create probability vector
        prob_vector = np.array(probabilities, dtype=np.float32)
        prob_vector = prob_vector / max(prob_vector.sum(), 1.0)
        
        return {
            'predicted_type': predicted_type,
            'probabilities': {
                obj_type: float(prob) for obj_type, prob in zip(self.object_types, probabilities)
            },
            'confidence': float(np.max(probabilities)),
            'feature_vector': prob_vector
        }
    
    def _classify_object_type(self, image: np.ndarray, gray: np.ndarray, 
                             aspect_ratio: float, compactness: float) -> List[float]:
        """Classify object type using rule-based approach"""
        scores = {
            'mask': 0.0,
            'pottery': 0.0,
            'jewelry': 0.0,
            'textile': 0.0,
            'sculpture': 0.0,
            'utility': 0.0
        }
        
        h, w = image.shape[:2]
        area = h * w
        
        # Mask: Face-like proportions, moderate size, often symmetrical
        if 0.7 < aspect_ratio < 1.3:  # Roughly square
            scores['mask'] += 0.3
        if 0.5 < compactness < 0.9:  # Moderate compactness
            scores['mask'] += 0.3
        if 50000 < area < 500000:  # Moderate size
            scores['mask'] += 0.2
        # Check for face-like features (simplified)
        if self._has_face_like_features(gray):
            scores['mask'] += 0.2
        
        # Pottery: Often round/oval, high compactness, container-like
        if compactness > 0.7:  # Round shapes
            scores['pottery'] += 0.4
        if aspect_ratio < 1.5:  # Not too elongated
            scores['pottery'] += 0.2
        if 30000 < area < 400000:
            scores['pottery'] += 0.2
        # Check for container-like shape (hollow center)
        if self._has_container_shape(gray):
            scores['pottery'] += 0.2
        
        # Jewelry: Small, intricate, high detail density
        if area < 100000:  # Small objects
            scores['jewelry'] += 0.4
        if self._has_high_detail_density(gray):
            scores['jewelry'] += 0.3
        if aspect_ratio < 2.0:  # Not too elongated
            scores['jewelry'] += 0.2
        if compactness > 0.6:
            scores['jewelry'] += 0.1
        
        # Textile: Flat, low compactness, often rectangular
        if aspect_ratio > 1.5 or aspect_ratio < 0.7:  # Rectangular
            scores['textile'] += 0.3
        if compactness < 0.6:  # Low compactness (flat)
            scores['textile'] += 0.3
        if area > 50000:
            scores['textile'] += 0.2
        if self._has_textile_pattern(gray):
            scores['textile'] += 0.2
        
        # Sculpture: 3D appearance, moderate to large size
        if 100000 < area < 1000000:
            scores['sculpture'] += 0.3
        if 0.4 < compactness < 0.8:
            scores['sculpture'] += 0.2
        if self._has_3d_appearance(gray):
            scores['sculpture'] += 0.3
        if aspect_ratio < 2.0:
            scores['sculpture'] += 0.2
        
        # Utility: Functional objects, varied shapes
        # Default category if no strong signal
        max_score = max(scores.values())
        if max_score < 0.4:
            scores['utility'] = 0.5
        else:
            scores['utility'] = 0.1  # Low default
        
        # Convert to probabilities
        score_values = np.array(list(scores.values()))
        score_values = score_values + 0.1  # Add epsilon
        probabilities = score_values / score_values.sum()
        
        return probabilities.tolist()
    
    def _has_face_like_features(self, gray: np.ndarray) -> bool:
        """Check for face-like features (simplified)"""
        # Look for two eye-like regions (dark areas)
        # This is a very simplified check
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # If we have multiple distinct regions, might be face-like
        return len(contours) >= 2
    
    def _has_container_shape(self, gray: np.ndarray) -> bool:
        """Check for container-like shape (hollow center)"""
        # Look for darker center (hollow)
        h, w = gray.shape
        center_region = gray[h//4:3*h//4, w//4:3*w//4]
        center_brightness = np.mean(center_region)
        edge_brightness = np.mean(np.concatenate([
            gray[0, :], gray[-1, :], gray[:, 0], gray[:, -1]
        ]))
        return center_brightness < edge_brightness * 0.9
    
    def _has_high_detail_density(self, gray: np.ndarray) -> bool:
        """Check for high detail density"""
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (gray.shape[0] * gray.shape[1])
        return edge_density > 0.15
    
    def _has_textile_pattern(self, gray: np.ndarray) -> bool:
        """Check for textile-like patterns"""
        # Look for repeating patterns using FFT
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        # Textiles often have periodic patterns
        h, w = magnitude.shape
        center_h, center_w = h // 2, w // 2
        mask = np.ones_like(magnitude)
        mask[center_h-10:center_h+10, center_w-10:center_w+10] = 0
        pattern_strength = np.mean(magnitude[mask > 0])
        return pattern_strength > np.mean(magnitude) * 1.2
    
    def _has_3d_appearance(self, gray: np.ndarray) -> bool:
        """Check for 3D appearance (shading, depth cues)"""
        # Look for gradual brightness changes (shading)
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        # 3D objects have more gradual gradients
        gradient_std = np.std(gradient_magnitude)
        return gradient_std > 20


