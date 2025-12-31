"""
Simple script to test the image search API
Usage: python test_api.py <image_path>
"""

import sys
import requests
from pathlib import Path

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print(f"[OK] Health check passed: {response.json()}")
            return True
        else:
            print(f"[ERROR] Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        print("Make sure the server is running: python run.py")
        return False

def test_search(image_path: str):
    """Test image search endpoint"""
    print(f"\nTesting image search with: {image_path}")
    
    if not Path(image_path).exists():
        print(f"[ERROR] Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/png')}
            response = requests.post(f"{API_URL}/api/v1/search", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Search successful!")
            print(f"\nQuery ID: {data['query_id']}")
            print(f"Total matches: {data['total_matches']}")
            print("\nTop Results:")
            print("-" * 60)
            for i, result in enumerate(data['results'], 1):
                print(f"{i}. {result['title']}")
                print(f"   Product ID: {result['product_id']}")
                print(f"   Final Similarity: {result['similarity_score']:.2%}")
                
                # Show per-feature scores if available
                if result.get('per_feature_scores'):
                    print("   Per-Feature Scores:")
                    for feature, score in result['per_feature_scores'].items():
                        print(f"      {feature:12s}: {score:.2%}")
                
                # Show predictions if available
                if result.get('predicted_material'):
                    print(f"   Material: {result['predicted_material']}")
                if result.get('predicted_object_type'):
                    print(f"   Object Type: {result['predicted_object_type']}")
                
                print(f"   Description: {result['description'][:50]}...")
                print()
            
            # Show query features if available
            if data.get('query_features'):
                print("\nQuery Image Analysis:")
                print("-" * 60)
                qf = data['query_features']
                print(f"   Material: {qf.get('material', 'N/A')}")
                print(f"   Object Type: {qf.get('object_type', 'N/A')}")
                print(f"   Edge Count: {qf.get('edge_count', 'N/A')}")
                print(f"   Dominant Colors: {qf.get('dominant_colors', 'N/A')}")
                print()
            return True
        else:
            print(f"[ERROR] Search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Error during search: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Image Recognition API Test Script")
    print("=" * 60)
    
    # Test health first
    if not test_health():
        sys.exit(1)
    
    # Test search if image provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_search(image_path)
    else:
        print("\n[INFO] No image provided for search test.")
        print("Usage: python test_api.py <image_path>")
        print("\nExample:")
        print("  python test_api.py images/1.png")
        print("\nOr test via API docs at: http://localhost:8000/docs")

