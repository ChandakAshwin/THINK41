import requests
import json
import time

def test_api_endpoints():
    """Test the FastAPI endpoints"""
    base_url = "http://localhost:8000"
    
    print("=== Testing FastAPI E-commerce Products API ===\n")
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test 1: Root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test 2: Get all products (first page)
        print("2. Testing GET /api/products...")
        response = requests.get(f"{base_url}/api/products?page=1&page_size=5")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total products: {data['total_count']}")
            print(f"Products returned: {len(data['products'])}")
            print("Sample products:")
            for i, product in enumerate(data['products'][:3]):
                print(f"  {i+1}. {product['name']} - ${product.get('retail_price', 'N/A')}")
        print()
        
        # Test 3: Get specific product by ID
        print("3. Testing GET /api/products/1...")
        response = requests.get(f"{base_url}/api/products/1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            product = response.json()
            print(f"Product: {product['name']}")
            print(f"Category: {product['category']}")
            print(f"Price: ${product.get('retail_price', 'N/A')}")
        elif response.status_code == 404:
            print("Product not found (this is expected if ID 1 doesn't exist)")
        print()
        
        # Test 4: Search products
        print("4. Testing GET /api/products/search?q=jeans...")
        response = requests.get(f"{base_url}/api/products/search?q=jeans&page=1&page_size=3")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Search results: {data['total_count']} products found")
            print("Sample results:")
            for i, product in enumerate(data['products'][:3]):
                print(f"  {i+1}. {product['name']} - {product['category']}")
        print()
        
        # Test 5: Test error handling - invalid product ID
        print("5. Testing error handling with invalid product ID...")
        response = requests.get(f"{base_url}/api/products/999999")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("Correctly returned 404 for non-existent product")
        print()
        
        print("✅ API testing completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: cd src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_api_endpoints() 