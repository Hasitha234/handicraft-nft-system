"""Test script for graph endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_graph_endpoints():
    print("=" * 60)
    print("Testing Graph Endpoints")
    print("=" * 60)
    
    # Test 1: Graph Statistics
    print("\n1. Testing Graph Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   [OK] Graph Stats:")
            print(f"        Products: {stats.get('total_products')}")
            print(f"        Relationships: {stats.get('total_relationships')}")
            print(f"        Outlets: {stats.get('total_outlets')}")
        else:
            print(f"   [ERROR] Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 2: Related Products
    print("\n2. Testing Related Products...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/products/1/related")
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Found {data.get('total_related')} related products")
            for i, rel in enumerate(data.get('related_products', [])[:3], 1):
                print(f"        {i}. {rel.get('product_id')} - {rel.get('relationship')} (weight: {rel.get('weight'):.2f})")
        else:
            print(f"   [ERROR] Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 3: Product Outlets (should be empty initially)
    print("\n3. Testing Product Outlets...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/products/1/outlets")
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Found {data.get('total_outlets')} outlets")
            if data.get('total_outlets') == 0:
                print("        (No outlets added yet - this is expected)")
        else:
            print(f"   [ERROR] Status: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 4: Add Sample Outlet
    print("\n4. Testing Add Outlet...")
    try:
        outlet_data = {
            "outlet_id": "shop_001",
            "name": "Traditional Handicrafts Shop",
            "location": "Kandy, Sri Lanka",
            "latitude": 7.2906,
            "longitude": 80.6337,
            "products": ["1", "2", "3", "15"]
        }
        response = requests.post(f"{BASE_URL}/api/v1/outlets", params=outlet_data)
        if response.status_code == 200:
            print(f"   [OK] Outlet added: {response.json().get('outlet_id')}")
        else:
            print(f"   [ERROR] Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 5: Check outlets for product 1
    print("\n5. Testing Outlets for Product 1...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/products/1/outlets")
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Found {data.get('total_outlets')} outlets")
            for outlet in data.get('outlets', []):
                print(f"        - {outlet.get('name')} at {outlet.get('location')}")
        else:
            print(f"   [ERROR] Status: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_graph_endpoints()


