"""
Color Feature Extractor
Extracts: HSV histograms, dominant colors, color distribution, brightness, saturation
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Tuple


class ColorExtractor:
    """Extracts color features from images"""
    
    def __init__(self, n_dominant_colors: int = 5, histogram_bins: int = 32):
        """
        Initialize color extractor
        
        Args:
            n_dominant_colors: Number of dominant colors to extract
            histogram_bins: Number of bins for HSV histogram
        """
        self.n_dominant_colors = n_dominant_colors
        self.histogram_bins = histogram_bins
    
    def extract(self, image: np.ndarray) -> Dict:
        """
        Extract all color features from image
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Dictionary with color features and feature vector
        """
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # HSV Histogram
        h_hist, s_hist, v_hist = self._compute_hsv_histogram(hsv)
        
        # Dominant colors
        dominant_colors = self._extract_dominant_colors(image)
        
        # Color statistics
        brightness = np.mean(hsv[:, :, 2]) / 255.0  # Value channel
        saturation = np.mean(hsv[:, :, 1]) / 255.0  # Saturation channel
        contrast = self._calculate_contrast(hsv[:, :, 2])  # Contrast in value channel
        
        # Color distribution (uniformity)
        color_uniformity = self._calculate_color_uniformity(hsv)
        
        # Color transitions (gradient analysis)
        color_transitions = self._analyze_color_transitions(hsv)
        
        # Create feature vector
        # Combine histogram features, dominant colors, and statistics
        feature_vector = np.concatenate([
            h_hist.flatten() / max(h_hist.sum(), 1),  # Normalized H histogram
            s_hist.flatten() / max(s_hist.sum(), 1),  # Normalized S histogram
            v_hist.flatten() / max(v_hist.sum(), 1),  # Normalized V histogram
            dominant_colors.flatten() / 255.0,  # Normalized dominant colors (RGB)
            np.array([brightness, saturation, contrast, color_uniformity, color_transitions])
        ]).astype(np.float32)
        
        # Normalize to unit vector
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return {
            'hsv_histogram': {
                'h': h_hist.tolist(),
                's': s_hist.tolist(),
                'v': v_hist.tolist()
            },
            'dominant_colors': dominant_colors.tolist(),
            'brightness': float(brightness),
            'saturation': float(saturation),
            'contrast': float(contrast),
            'color_uniformity': float(color_uniformity),
            'color_transitions': float(color_transitions),
            'feature_vector': feature_vector
        }
    
    def _compute_hsv_histogram(self, hsv: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute HSV histograms"""
        h_hist = cv2.calcHist([hsv], [0], None, [self.histogram_bins], [0, 180])
        s_hist = cv2.calcHist([hsv], [1], None, [self.histogram_bins], [0, 256])
        v_hist = cv2.calcHist([hsv], [2], None, [self.histogram_bins], [0, 256])
        return h_hist, s_hist, v_hist
    
    def _extract_dominant_colors(self, image: np.ndarray) -> np.ndarray:
        """Extract dominant colors using k-means clustering"""
        # Reshape image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Sample pixels for faster computation (if image is large)
        if len(pixels) > 10000:
            indices = np.random.choice(len(pixels), 10000, replace=False)
            pixels = pixels[indices]
        
        # Apply k-means
        try:
            kmeans = KMeans(n_clusters=self.n_dominant_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            dominant_colors = kmeans.cluster_centers_.astype(np.uint8)
        except:
            # Fallback: use simple color quantization
            dominant_colors = self._simple_color_quantization(pixels)
        
        # Sort by frequency (approximate)
        return dominant_colors
    
    def _simple_color_quantization(self, pixels: np.ndarray) -> np.ndarray:
        """Simple color quantization when k-means fails"""
        # Divide color space into bins and find most common colors
        quantized = (pixels // 64) * 64  # Quantize to 4 levels per channel
        unique_colors, counts = np.unique(quantized, axis=0, return_counts=True)
        top_indices = np.argsort(counts)[-self.n_dominant_colors:]
        return unique_colors[top_indices]
    
    def _calculate_contrast(self, channel: np.ndarray) -> float:
        """Calculate contrast (standard deviation)"""
        return np.std(channel) / 255.0
    
    def _calculate_color_uniformity(self, hsv: np.ndarray) -> float:
        """Calculate how uniform/distributed colors are"""
        # Lower std = more uniform
        h_std = np.std(hsv[:, :, 0])
        s_std = np.std(hsv[:, :, 1])
        v_std = np.std(hsv[:, :, 2])
        
        # Normalize and combine
        uniformity = 1.0 - min((h_std / 180.0 + s_std / 255.0 + v_std / 255.0) / 3.0, 1.0)
        return uniformity
    
    def _analyze_color_transitions(self, hsv: np.ndarray) -> float:
        """Analyze color transitions/gradients"""
        # Calculate gradients in H, S, V channels
        h_gradient = np.mean(np.abs(cv2.Sobel(hsv[:, :, 0], cv2.CV_64F, 1, 1, ksize=3)))
        s_gradient = np.mean(np.abs(cv2.Sobel(hsv[:, :, 1], cv2.CV_64F, 1, 1, ksize=3)))
        v_gradient = np.mean(np.abs(cv2.Sobel(hsv[:, :, 2], cv2.CV_64F, 1, 1, ksize=3)))
        
        # Normalize
        transitions = (h_gradient / 180.0 + s_gradient / 255.0 + v_gradient / 255.0) / 3.0
        return min(transitions, 1.0)


