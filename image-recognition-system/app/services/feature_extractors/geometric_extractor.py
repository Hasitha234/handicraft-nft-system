"""
Geometric and Structural Feature Extractor
Extracts: edges, vertices, contours, shape complexity, aspect ratio, symmetry
"""

import cv2
import numpy as np
from typing import Dict


class GeometricExtractor:
    """Extracts geometric and structural features from images"""
    
    def __init__(self):
        """Initialize geometric feature extractor"""
        pass
    
    def extract(self, image: np.ndarray) -> Dict:
        """
        Extract all geometric features from image
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with geometric features and feature vector
        """
        # Convert to grayscale for edge/contour detection
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Edge detection
        edges = self._detect_edges(gray)
        edge_count = np.sum(edges > 0)
        edge_density = edge_count / (image.shape[0] * image.shape[1])
        
        # Contour detection
        contours = self._detect_contours(edges)
        vertex_count = sum(len(cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)) 
                          for contour in contours)
        
        # Shape analysis
        aspect_ratio = self._calculate_aspect_ratio(image)
        compactness = self._calculate_compactness(contours, image.shape)
        symmetry_score = self._calculate_symmetry(gray)
        
        # Curvature estimation (simplified)
        curvature_score = self._estimate_curvature(contours)
        
        # Structural complexity (based on contour hierarchy)
        complexity = len(contours) / max(1, image.shape[0] * image.shape[1] / 10000)
        
        # Create feature vector (normalized values)
        feature_vector = np.array([
            min(edge_density, 1.0),  # Edge density (0-1)
            min(vertex_count / 1000.0, 1.0),  # Normalized vertex count
            min(aspect_ratio, 1.0),  # Aspect ratio (normalized)
            min(compactness, 1.0),  # Compactness (0-1)
            min(symmetry_score, 1.0),  # Symmetry (0-1)
            min(curvature_score, 1.0),  # Curvature (0-1)
            min(complexity, 1.0),  # Structural complexity (0-1)
        ], dtype=np.float32)
        
        # Normalize vector to unit length
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return {
            'edge_count': int(edge_count),
            'edge_density': float(edge_density),
            'vertex_count': int(vertex_count),
            'contour_count': len(contours),
            'aspect_ratio': float(aspect_ratio),
            'compactness': float(compactness),
            'symmetry': float(symmetry_score),
            'curvature': float(curvature_score),
            'complexity': float(complexity),
            'feature_vector': feature_vector
        }
    
    def _detect_edges(self, gray: np.ndarray) -> np.ndarray:
        """Detect edges using Canny edge detector"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Canny edge detection with adaptive thresholds
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    def _detect_contours(self, edges: np.ndarray) -> list:
        """Detect contours from edges"""
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filter small contours (noise)
        min_area = edges.shape[0] * edges.shape[1] * 0.001
        contours = [c for c in contours if cv2.contourArea(c) > min_area]
        return contours
    
    def _calculate_aspect_ratio(self, image: np.ndarray) -> float:
        """Calculate aspect ratio (width/height)"""
        height, width = image.shape[:2]
        return width / max(height, 1)
    
    def _calculate_compactness(self, contours: list, image_shape: tuple) -> float:
        """Calculate compactness (how close shape is to a circle)"""
        if not contours:
            return 0.0
        
        # Use largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        
        if perimeter == 0:
            return 0.0
        
        # Compactness = 4π * area / perimeter²
        # Circle has compactness = 1.0
        compactness = (4 * np.pi * area) / (perimeter ** 2)
        return min(compactness, 1.0)
    
    def _calculate_symmetry(self, gray: np.ndarray) -> float:
        """Calculate symmetry score (horizontal and vertical)"""
        h, w = gray.shape
        
        # Horizontal symmetry
        top_half = gray[:h//2, :]
        bottom_half = cv2.flip(gray[h//2:, :], 0)
        if top_half.shape != bottom_half.shape:
            min_h = min(top_half.shape[0], bottom_half.shape[0])
            top_half = top_half[:min_h, :]
            bottom_half = bottom_half[:min_h, :]
        h_symmetry = 1.0 - np.mean(np.abs(top_half.astype(float) - bottom_half.astype(float))) / 255.0
        
        # Vertical symmetry
        left_half = gray[:, :w//2]
        right_half = cv2.flip(gray[:, w//2:], 1)
        if left_half.shape != right_half.shape:
            min_w = min(left_half.shape[1], right_half.shape[1])
            left_half = left_half[:, :min_w]
            right_half = right_half[:, :min_w]
        v_symmetry = 1.0 - np.mean(np.abs(left_half.astype(float) - right_half.astype(float))) / 255.0
        
        # Average symmetry
        return (h_symmetry + v_symmetry) / 2.0
    
    def _estimate_curvature(self, contours: list) -> float:
        """Estimate overall curvature of contours"""
        if not contours:
            return 0.0
        
        curvature_scores = []
        for contour in contours:
            if len(contour) < 3:
                continue
            
            # Approximate contour with fewer points
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # More points = more curved
            curvature = len(approx) / max(len(contour), 1)
            curvature_scores.append(curvature)
        
        return np.mean(curvature_scores) if curvature_scores else 0.0


