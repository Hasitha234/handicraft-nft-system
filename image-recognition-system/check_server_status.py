"""Check if server is using enhanced features"""

import requests
import json

try:
    # Test search endpoint
    url = "http://localhost:8000/api/v1/search"
    with open("images/1.png", "rb") as f:
        files = {"file": ("1.png", f, "image/png")}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        print("=" * 60)
        print("Server Status Check")
        print("=" * 60)
        
        if data.get('query_features'):
            print("\n[OK] Enhanced features are ACTIVE!")
            print(f"Query Material: {data['query_features'].get('material')}")
            print(f"Query Object Type: {data['query_features'].get('object_type')}")
        else:
            print("\n[WARNING] Enhanced features NOT active")
            print("Server is using basic CLIP search")
            print("\nTo enable enhanced features:")
            print("1. Stop server (Ctrl+C)")
            print("2. Restart: python run.py")
            print("3. Look for: 'Enhanced features loaded for 95 products'")
        
        if data['results'] and data['results'][0].get('per_feature_scores'):
            print("\n[OK] Per-feature scores available!")
            print("Sample scores:", data['results'][0]['per_feature_scores'])
        else:
            print("\n[INFO] Per-feature scores not in response")
            print("This means enhanced search is not active")
        
        print("\n" + "=" * 60)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error connecting to server: {e}")
    print("Make sure server is running: python run.py")

