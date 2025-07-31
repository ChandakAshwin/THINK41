#!/usr/bin/env python3
"""
FastAPI E-commerce Products API Demonstration
This script demonstrates the API endpoints and walks through the implementation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from main import app
import json

def demo_api_endpoints():
    """Demonstrate the API endpoints"""
    print("🚀 FastAPI E-commerce Products API Demonstration")
    print("=" * 60)
    
    # Create test client
    client = TestClient(app)
    
    # 1. Test GET /api/products endpoint
    print("\n1️⃣ Testing GET /api/products endpoint")
    print("-" * 40)
    
    response = client.get("/api/products?page=1&page_size=5")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total Products: {data['total_count']}")
    print(f"Products Returned: {len(data['products'])}")
    print(f"Page: {data['page']}")
    print(f"Page Size: {data['page_size']}")
    
    if data['products']:
        print("\nSample Products:")
        for i, product in enumerate(data['products'][:3], 1):
            print(f"  {i}. {product['name']} - ${product.get('retail_price', 'N/A')}")
    
    # 2. Test GET /api/products/{id} endpoint
    print("\n2️⃣ Testing GET /api/products/{id} endpoint")
    print("-" * 40)
    
    # Test with a valid product ID (assuming ID 1 exists)
    response = client.get("/api/products/1")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        product = response.json()
        print(f"Product ID: {product['id']}")
        print(f"Product Name: {product['name']}")
        print(f"Category: {product['category']}")
        print(f"Brand: {product.get('brand', 'N/A')}")
        print(f"Price: ${product.get('retail_price', 'N/A')}")
    else:
        print(f"Error: {response.json()}")
    
    # 3. Test error handling with invalid product ID
    print("\n3️⃣ Testing Error Handling (Invalid Product ID)")
    print("-" * 40)
    
    response = client.get("/api/products/999999")
    print(f"Status Code: {response.status_code}")
    error_data = response.json()
    print(f"Error Response: {error_data}")
    
    # 4. Test search functionality
    print("\n4️⃣ Testing Search Functionality")
    print("-" * 40)
    
    response = client.get("/api/products/search?search=jeans&page=1&page_size=3")
    print(f"Status Code: {response.status_code}")
    search_data = response.json()
    print(f"Search Results: {search_data['total_count']} products found")
    print(f"Search Term: {search_data['search_term']}")
    
    if search_data['products']:
        print("\nSearch Results:")
        for i, product in enumerate(search_data['products'][:3], 1):
            print(f"  {i}. {product['name']} - {product['category']}")
    
    # 5. Test pagination
    print("\n5️⃣ Testing Pagination")
    print("-" * 40)
    
    response = client.get("/api/products?page=2&page_size=3")
    print(f"Status Code: {response.status_code}")
    pagination_data = response.json()
    print(f"Page: {pagination_data['page']}")
    print(f"Page Size: {pagination_data['page_size']}")
    print(f"Products on this page: {len(pagination_data['products'])}")
    
    print("\n✅ API Demonstration Complete!")

def walkthrough_implementation():
    """Walk through the API implementation"""
    print("\n🔍 API Implementation Walkthrough")
    print("=" * 60)
    
    print("\n📁 Project Structure:")
    print("src/")
    print("├── main.py          # FastAPI application")
    print("├── models.py         # Pydantic models")
    print("├── database.py       # Database operations")
    print("└── data_loader.py    # Data loading script")
    
    print("\n🏗️ Key Components:")
    
    print("\n1. FastAPI Application (main.py):")
    print("   - FastAPI app initialization with CORS middleware")
    print("   - Route definitions for all endpoints")
    print("   - Error handling with proper HTTP status codes")
    print("   - Pydantic models for request/response validation")
    
    print("\n2. Database Manager (database.py):")
    print("   - SQLite database operations")
    print("   - Connection management with context managers")
    print("   - Pagination support")
    print("   - Search functionality across multiple fields")
    
    print("\n3. Pydantic Models (models.py):")
    print("   - ProductResponse: Individual product data structure")
    print("   - ProductListResponse: Paginated product list structure")
    print("   - ErrorResponse: Standardized error response format")
    
    print("\n4. API Endpoints:")
    print("   - GET /: API information and documentation")
    print("   - GET /api/products: List all products with pagination")
    print("   - GET /api/products/{id}: Get specific product by ID")
    print("   - GET /api/products/search: Search products by name/category/brand")
    
    print("\n🛡️ Error Handling:")
    print("   - 404 Not Found: Product not found")
    print("   - 400 Bad Request: Invalid input parameters")
    print("   - 422 Unprocessable Entity: Validation errors")
    print("   - 500 Internal Server Error: Server-side errors")
    
    print("\n📊 Features:")
    print("   - Pagination with customizable page size")
    print("   - Search across product name, category, and brand")
    print("   - CORS support for frontend integration")
    print("   - Automatic API documentation at /docs")
    print("   - Comprehensive input validation")
    print("   - Performance optimized for large datasets")

if __name__ == "__main__":
    demo_api_endpoints()
    walkthrough_implementation() 