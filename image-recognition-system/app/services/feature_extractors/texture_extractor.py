"""
Texture Feature Extractor
Extracts: LBP (Local Binary Patterns), surface roughness, grain direction, texture patterns
"""

import cv2
import numpy as np
from typing import Dict


class TextureExtractor:
    """Extracts texture features from images"""
    
    def __init__(self, lbp_radius: int = 3, lbp_points: int = 24):
        """
        Initialize texture extractor
        
        Args:
            lbp_radius: Radius for LBP computation
            lbp_points: Number of points for LBP
        """
        self.lbp_radius = lbp_radius
        self.lbp_points = lbp_points
    
    def extract(self, image: np.ndarray) -> Dict:
        """
        Extract all texture features from image
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with texture features and feature vector
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Local Binary Patterns (LBP)
        lbp = self._compute_lbp(gray)
        lbp_histogram = self._compute_lbp_histogram(lbp)
        
        # Surface roughness (variance of gradients)
        roughness = self._calculate_roughness(gray)
        
        # Grain direction (orientation analysis)
        grain_direction = self._analyze_grain_direction(gray)
        
        # Texture uniformity
        texture_uniformity = self._calculate_texture_uniformity(lbp)
        
        # Repeating patterns (autocorrelation)
        pattern_strength = self._detect_repeating_patterns(gray)
        
        # Surface irregularities
        irregularities = self._detect_irregularities(gray)
        
        # Create feature vector
        feature_vector = np.concatenate([
            lbp_histogram.flatten() / max(lbp_histogram.sum(), 1),  # Normalized LBP histogram
            np.array([
                roughness,
                grain_direction,
                texture_uniformity,
                pattern_strength,
                irregularities
            ])
        ]).astype(np.float32)
        
        # Normalize to unit vector
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return {
            'lbp_histogram': lbp_histogram.tolist(),
            'roughness': float(roughness),
            'grain_direction': float(grain_direction),
            'texture_uniformity': float(texture_uniformity),
            'pattern_strength': float(pattern_strength),
            'irregularities': float(irregularities),
            'feature_vector': feature_vector
        }
    
    def _compute_lbp(self, gray: np.ndarray) -> np.ndarray:
        """Compute Local Binary Pattern"""
        # Simplified LBP implementation
        # For production, consider using scikit-image's local_binary_pattern
        h, w = gray.shape
        lbp = np.zeros_like(gray)
        
        for i in range(self.lbp_radius, h - self.lbp_radius):
            for j in range(self.lbp_radius, w - self.lbp_radius):
                center = gray[i, j]
                binary = 0
                for k in range(self.lbp_points):
                    angle = 2 * np.pi * k / self.lbp_points
                    x = int(i + self.lbp_radius * np.cos(angle))
                    y = int(j + self.lbp_radius * np.sin(angle))
                    if 0 <= x < h and 0 <= y < w:
                        if gray[x, y] >= center:
                            binary |= (1 << k)
                lbp[i, j] = binary
        
        return lbp
    
    def _compute_lbp_histogram(self, lbp: np.ndarray) -> np.ndarray:
        """Compute histogram of LBP values"""
        # Use 256 bins for 8-bit LBP
        hist, _ = np.histogram(lbp.flatten(), bins=256, range=(0, 256))
        return hist.astype(np.float32)
    
    def _calculate_roughness(self, gray: np.ndarray) -> float:
        """Calculate surface roughness (variance of gradients)"""
        # Compute gradients
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Roughness = variance of gradient magnitudes
        roughness = np.var(gradient_magnitude) / (255.0 ** 2)
        return min(roughness, 1.0)
    
    def _analyze_grain_direction(self, gray: np.ndarray) -> float:
        """Analyze grain direction/orientation"""
        # Use gradient orientation
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate orientation
        orientation = np.arctan2(grad_y, grad_x)
        
        # Analyze dominant direction (simplified)
        # More uniform orientation = stronger grain direction
        orientation_std = np.std(orientation)
        grain_strength = 1.0 - min(orientation_std / np.pi, 1.0)
        
        return grain_strength
    
    def _calculate_texture_uniformity(self, lbp: np.ndarray) -> float:
        """Calculate texture uniformity"""
        # Lower variance in LBP = more uniform texture
        lbp_variance = np.var(lbp)
        uniformity = 1.0 - min(lbp_variance / (256.0 ** 2), 1.0)
        return uniformity
    
    def _detect_repeating_patterns(self, gray: np.ndarray) -> float:
        """Detect repeating patterns using autocorrelation"""
        # Simplified: use FFT to detect periodic patterns
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shift)
        
        # Look for strong periodic components
        # (excluding DC component at center)
        h, w = magnitude_spectrum.shape
        center_h, center_w = h // 2, w // 2
        
        # Sample points away from center
        mask = np.ones_like(magnitude_spectrum)
        mask[center_h-5:center_h+5, center_w-5:center_w+5] = 0
        
        pattern_strength = np.mean(magnitude_spectrum[mask > 0]) / np.max(magnitude_spectrum)
        return min(pattern_strength, 1.0)
    
    def _detect_irregularities(self, gray: np.ndarray) -> float:
        """Detect surface irregularities"""
        # Use Laplacian to detect irregularities
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        irregularities = np.mean(np.abs(laplacian)) / 255.0
        return min(irregularities, 1.0)


