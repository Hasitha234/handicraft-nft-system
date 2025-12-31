"""
CLIP encoder service for extracting semantic embeddings
Uses OpenAI CLIP model for image-to-vector conversion
"""

import torch
import clip
import numpy as np
from PIL import Image


class CLIPEncoder:
    """CLIP-based image encoder for semantic embeddings"""
    
    def __init__(self, model_name: str = "ViT-B/32", device: str = None):
        """
        Initialize CLIP encoder
        
        Args:
            model_name: CLIP model variant (ViT-B/32, ViT-L/14, etc.)
            device: Device to run on ('cuda', 'cpu', or None for auto-detect)
        """
        self.model_name = model_name
        
        # Auto-detect device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        print(f"[INFO] Loading CLIP model: {model_name} on {self.device}")
        
        # Load CLIP model and preprocessing
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.model.eval()  # Set to evaluation mode
        
        # Get embedding dimension
        with torch.no_grad():
            dummy_input = torch.zeros(1, 3, 224, 224).to(self.device)
            dummy_output = self.model.encode_image(dummy_input)
            self.embedding_dim = dummy_output.shape[1]
        
        print(f"[OK] CLIP model loaded (embedding_dim={self.embedding_dim})")
    
    def encode_image(self, image: np.ndarray) -> np.ndarray:
        """
        Extract CLIP embedding from image
        
        Args:
            image: numpy array of shape (H, W, 3) with RGB values 0-255
            
        Returns:
            Normalized embedding vector (L2 normalized, shape: (embedding_dim,))
        """
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(image.astype('uint8'))
        
        # Preprocess for CLIP (resize to 224x224, normalize, etc.)
        preprocessed = self.preprocess(pil_image).unsqueeze(0).to(self.device)
        
        # Extract embedding
        with torch.no_grad():
            embedding = self.model.encode_image(preprocessed)
            
            # Normalize to unit vector (L2 normalization)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)
            
            # Convert to numpy and squeeze batch dimension
            embedding_np = embedding.cpu().numpy().flatten()
        
        return embedding_np
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Extract CLIP embedding from text (for future text-based search)
        
        Args:
            text: Text description
            
        Returns:
            Normalized embedding vector
        """
        # Tokenize text
        text_tokens = clip.tokenize([text]).to(self.device)
        
        # Extract embedding
        with torch.no_grad():
            embedding = self.model.encode_text(text_tokens)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)
            embedding_np = embedding.cpu().numpy().flatten()
        
        return embedding_np



