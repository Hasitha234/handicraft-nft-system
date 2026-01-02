"""
Script to build product relationship graph from indexed products
Run this after indexing products to create the relationship graph
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.clip_encoder import CLIPEncoder
from app.services.enhanced_vector_store import EnhancedVectorStore
from app.services.graph_service import GraphService


def build_graph():
    """Build product relationship graph from indexed products"""
    print("=" * 60)
    print("Building Product Relationship Graph")
    print("=" * 60)
    
    # Load products and features
    print("\n[INFO] Loading products and features...")
    clip_encoder = CLIPEncoder()
    vector_store = EnhancedVectorStore()
    vector_store.load_or_create_index(clip_encoder, create_sample_data=False)
    
    if len(vector_store.products) == 0:
        print("[ERROR] No products found! Index products first.")
        return
    
    if len(vector_store.features) == 0:
        print("[ERROR] No features found! Run reindex_with_features.py first.")
        return
    
    print(f"[OK] Loaded {len(vector_store.products)} products")
    print(f"[OK] Loaded features for {len(vector_store.features)} products")
    
    # Initialize graph service
    print("\n[INFO] Initializing graph service...")
    graph_service = GraphService()
    
    # Convert features to the format expected by graph service
    # (convert numpy arrays back to dict format)
    features_dict = {}
    for product_id, features in vector_store.features.items():
        # Features are already in dict format from storage
        features_dict[product_id] = features
    
    # Build relationships
    print("\n[INFO] Building product relationships...")
    graph_service.build_relationships_from_features(
        vector_store.products,
        features_dict
    )
    
    # Print statistics
    stats = graph_service.get_statistics()
    print("\n" + "=" * 60)
    print("Graph Statistics:")
    print("=" * 60)
    print(f"Total Products: {stats['total_products']}")
    print(f"Total Relationships: {stats['total_relationships']}")
    print(f"Total Outlets: {stats['total_outlets']}")
    print(f"Products with Outlets: {stats['products_with_outlets']}")
    print("\n[OK] Graph built successfully!")
    print("\nNext steps:")
    print("1. Add outlets using: POST /api/v1/outlets")
    print("2. Query related products: GET /api/v1/products/{id}/related")
    print("3. Find outlets: GET /api/v1/products/{id}/outlets")


if __name__ == "__main__":
    build_graph()


