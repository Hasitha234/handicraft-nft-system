"""
Script to batch load product images from the images folder into the vector database
Usage: python scripts/load_images.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.image_processor import ImageProcessor
from app.services.clip_encoder import CLIPEncoder
from app.services.vector_store import VectorStore


def load_images_from_folder(images_folder: str = "images"):
    """
    Load all images from a folder and add them to the vector database
    
    Args:
        images_folder: Path to folder containing product images
    """
    # Initialize services
    print("[INFO] Initializing services...")
    image_processor = ImageProcessor()
    clip_encoder = CLIPEncoder()
    vector_store = VectorStore()
    
    # Load or create index
    vector_store.load_or_create_index(clip_encoder, create_sample_data=False)
    
    # Get images folder path
    images_path = Path(images_folder)
    if not images_path.exists():
        print(f"[ERROR] Images folder '{images_folder}' not found!")
        print(f"   Please create the folder and add your product images.")
        return
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    # Find all image files
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_path.glob(f'*{ext}'))
        image_files.extend(images_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"[ERROR] No image files found in '{images_folder}'")
        print(f"   Supported formats: {', '.join(image_extensions)}")
        return
    
    print(f"[INFO] Found {len(image_files)} image(s) to process")
    print("-" * 50)
    
    # Process each image
    success_count = 0
    error_count = 0
    
    for idx, image_path in enumerate(image_files, 1):
        try:
            print(f"[{idx}/{len(image_files)}] Processing: {image_path.name}")
            
            # Read image
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Preprocess
            processed_image = image_processor.preprocess(image_bytes)
            
            # Extract CLIP embedding
            embedding = clip_encoder.encode_image(processed_image)
            
            # Generate product ID from filename (remove extension)
            product_id = image_path.stem
            
            # Try to extract metadata from filename
            # Expected format: "PRODUCT_ID_TITLE_DESCRIPTION.jpg" or just "PRODUCT_ID.jpg"
            parts = product_id.split('_')
            if len(parts) >= 2:
                product_id = parts[0]
                title = ' '.join(parts[1:]) if len(parts) > 1 else "Unknown Product"
            else:
                title = product_id.replace('_', ' ').title()
            
            # Add to vector store
            vector_store.add_product(
                product_id=product_id,
                embedding=embedding,
                metadata={
                    "title": title,
                    "description": f"Handicraft product from {image_path.name}",
                    "filename": image_path.name,
                    "filepath": str(image_path)
                }
            )
            
            success_count += 1
            print(f"   [OK] Added: {product_id} - {title}")
            
        except Exception as e:
            error_count += 1
            print(f"   [ERROR] Error processing {image_path.name}: {str(e)}")
    
    print("-" * 50)
    print(f"[OK] Successfully loaded: {success_count} products")
    if error_count > 0:
        print(f"[ERROR] Errors: {error_count} products")
    print(f"[INFO] Total products in database: {len(vector_store.products)}")


if __name__ == "__main__":
    # Check if images folder path is provided as argument
    images_folder = sys.argv[1] if len(sys.argv) > 1 else "images"
    
    print("=" * 50)
    print("Image Loading Script")
    print("=" * 50)
    print(f"[INFO] Loading images from: {images_folder}")
    print()
    
    load_images_from_folder(images_folder)

