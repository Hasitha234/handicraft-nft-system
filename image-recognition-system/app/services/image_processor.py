"""
Image preprocessing service
Handles image normalization, resizing, and format conversion
"""

from PIL import Image
import numpy as np
import io


class ImageProcessor:
    """Handles image preprocessing tasks"""
    
    def __init__(self, target_size: int = 384):
        """
        Initialize image processor
        
        Args:
            target_size: Target size for the shorter edge (maintains aspect ratio)
        """
        self.target_size = target_size
    
    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess uploaded image for CLIP model
        
        Steps:
        1. Load image from bytes
        2. Convert to RGB (handles RGBA, grayscale, etc.)
        3. Resize maintaining aspect ratio (shorter edge = target_size)
        4. Convert to numpy array (RGB format, values 0-255)
        
        Args:
            image_bytes: Raw image file bytes
            
        Returns:
            numpy array of shape (H, W, 3) with RGB values 0-255
        """
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed (handles RGBA, grayscale, etc.)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Resize maintaining aspect ratio (shorter edge = target_size)
        image = self._resize_with_aspect_ratio(image, self.target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        return image_array
    
    def _resize_with_aspect_ratio(self, image: Image.Image, target_size: int) -> Image.Image:
        """
        Resize image maintaining aspect ratio
        
        Resizes so that the shorter edge equals target_size
        """
        width, height = image.size
        
        # Determine which edge is shorter
        if width < height:
            # Width is shorter, scale based on width
            new_width = target_size
            new_height = int(height * (target_size / width))
        else:
            # Height is shorter, scale based on height
            new_height = target_size
            new_width = int(width * (target_size / height))
        
        # Resize with high-quality resampling
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return resized



