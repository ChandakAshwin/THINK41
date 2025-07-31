import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test the search endpoint
print("Testing search endpoint...")
response = client.get("/api/products/search?search=Test")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test the main products endpoint
print("\nTesting main products endpoint...")
response = client.get("/api/products")
print(f"Status: {response.status_code}")
print(f"Response keys: {list(response.json().keys())}") 