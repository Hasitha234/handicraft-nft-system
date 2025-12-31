"""
Test script to verify the basic CLIP + FAISS pipeline works
Run this to ensure everything is set up correctly
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.image_processor import ImageProcessor
from app.services.clip_encoder import CLIPEncoder
from app.services.vector_store import VectorStore
import numpy as np
from PIL import Image

def test_basic_pipeline():
    """Test that all components work together"""
    print("=" * 60)
    print("Testing Basic CLIP + FAISS Pipeline")
    print("=" * 60)
    
    try:
        # Step 1: Initialize services
        print("\n[1/6] Initializing services...")
        image_processor = ImageProcessor()
        print("   [OK] ImageProcessor initialized")
        
        clip_encoder = CLIPEncoder()
        print("   [OK] CLIPEncoder initialized")
        
        vector_store = VectorStore()
        print("   [OK] VectorStore initialized")
        
        # Step 2: Create test image
        print("\n[2/6] Creating test image...")
        test_image = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
        pil_image = Image.fromarray(test_image)
        # Convert PIL image to bytes properly
        import io
        img_bytes = io.BytesIO()
        pil_image.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        print("   [OK] Test image created")
        
        # Step 3: Preprocess image
        print("\n[3/6] Preprocessing image...")
        processed = image_processor.preprocess(image_bytes)
        print(f"   [OK] Image preprocessed: shape {processed.shape}")
        
        # Step 4: Extract CLIP embedding
        print("\n[4/6] Extracting CLIP embedding...")
        embedding = clip_encoder.encode_image(processed)
        print(f"   [OK] Embedding extracted: shape {embedding.shape}, dim={len(embedding)}")
        
        # Step 5: Initialize vector store
        print("\n[5/6] Initializing vector store...")
        vector_store.load_or_create_index(clip_encoder, create_sample_data=True)
        print(f"   [OK] Vector store ready with {len(vector_store.products)} products")
        
        # Step 6: Test search
        print("\n[6/6] Testing similarity search...")
        results = vector_store.search(embedding, top_k=3)
        print(f"   [OK] Search completed: found {len(results)} results")
        for result in results:
            print(f"      - {result.product_id}: {result.title} (score: {result.similarity_score:.3f})")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL TESTS PASSED! System is ready to use.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_pipeline()
    sys.exit(0 if success else 1)

