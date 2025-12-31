"""
Script to re-index all images with new feature extractors
Extracts all physical features and stores them alongside CLIP embeddings
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.image_processor import ImageProcessor
from app.services.clip_encoder import CLIPEncoder
from app.services.feature_extractors.master_extractor import MasterFeatureExtractor
from app.services.enhanced_vector_store import EnhancedVectorStore


def reindex_images(images_folder: str = "images"):
    """Re-index all images with full feature extraction"""
    print("=" * 60)
    print("Re-indexing Images with Full Feature Extraction")
    print("=" * 60)
    
    # Initialize services
    print("\n[INFO] Initializing services...")
    image_processor = ImageProcessor()
    clip_encoder = CLIPEncoder()
    feature_extractor = MasterFeatureExtractor()
    vector_store = EnhancedVectorStore()
    
    # Load or create index
    vector_store.load_or_create_index(clip_encoder, create_sample_data=False)
    
    # Clear existing data if re-indexing
    print("\n[INFO] Clearing existing index...")
    vector_store.products = []
    vector_store.features = {}
    if vector_store.index:
        vector_store.index.reset()
    vector_store._create_index()
    
    # Get images
    images_path = Path(images_folder)
    if not images_path.exists():
        print(f"[ERROR] Images folder '{images_folder}' not found!")
        return
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_path.glob(f'*{ext}'))
        image_files.extend(images_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"[ERROR] No images found in '{images_folder}'")
        return
    
    print(f"[INFO] Found {len(image_files)} images to process")
    print("-" * 60)
    
    # Process each image
    success_count = 0
    error_count = 0
    
    for idx, image_path in enumerate(image_files, 1):
        try:
            print(f"[{idx}/{len(image_files)}] Processing: {image_path.name}")
            
            # Read and preprocess image
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            processed_image = image_processor.preprocess(image_bytes)
            
            # Extract CLIP embedding
            clip_embedding = clip_encoder.encode_image(processed_image)
            
            # Extract all physical features
            all_features = feature_extractor.extract_all(processed_image)
            
            # Prepare features for storage (convert numpy arrays to lists)
            stored_features = {
                'geometric': {
                    'feature_vector': all_features['geometric']['feature_vector'].tolist(),
                    **{k: v for k, v in all_features['geometric'].items() if k != 'feature_vector'}
                },
                'color': {
                    'feature_vector': all_features['color']['feature_vector'].tolist(),
                    **{k: v for k, v in all_features['color'].items() if k != 'feature_vector'}
                },
                'texture': {
                    'feature_vector': all_features['texture']['feature_vector'].tolist(),
                    **{k: v for k, v in all_features['texture'].items() if k != 'feature_vector'}
                },
                'pattern': {
                    'feature_vector': all_features['pattern']['feature_vector'].tolist(),
                    **{k: v for k, v in all_features['pattern'].items() if k != 'feature_vector'}
                },
                'material': all_features['material'],
                'object_type': all_features['object_type'],
                'clip': clip_embedding.tolist()  # Store CLIP for compatibility
            }
            
            # Generate product ID
            product_id = image_path.stem
            parts = product_id.split('_')
            if len(parts) >= 2:
                product_id = parts[0]
                title = ' '.join(parts[1:])
            else:
                title = product_id.replace('_', ' ').title()
            
            # Add to vector store
            vector_store.add_product(
                product_id=product_id,
                clip_embedding=clip_embedding,
                all_features=stored_features,
                metadata={
                    "title": title,
                    "description": f"Handicraft product from {image_path.name}",
                    "filename": image_path.name,
                    "filepath": str(image_path)
                }
            )
            
            success_count += 1
            print(f"   [OK] Indexed: {product_id} - {title}")
            print(f"        Material: {all_features['material']['predicted_material']}, "
                  f"Type: {all_features['object_type']['predicted_type']}")
            
        except Exception as e:
            error_count += 1
            print(f"   [ERROR] Error processing {image_path.name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("-" * 60)
    print(f"[OK] Successfully indexed: {success_count} products")
    if error_count > 0:
        print(f"[ERROR] Errors: {error_count} products")
    print(f"[INFO] Total products in database: {len(vector_store.products)}")
    print(f"[INFO] Total features stored: {len(vector_store.features)}")


if __name__ == "__main__":
    images_folder = sys.argv[1] if len(sys.argv) > 1 else "images"
    reindex_images(images_folder)


