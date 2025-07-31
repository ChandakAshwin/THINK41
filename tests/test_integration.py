import pytest
import sqlite3
from fastapi.testclient import TestClient
from fastapi import status

class TestIntegrationWorkflow:
    """Integration tests for complete API workflow"""
    
    def test_complete_product_workflow(self, client, test_db):
        """Test complete workflow: create data, query via API, verify results"""
        # Setup test data
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Create table and insert test data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                brand TEXT,
                retail_price REAL,
                cost REAL,
                department TEXT,
                sku TEXT,
                distribution_center_id INTEGER
            )
        """)
        
        # Clear any existing data
        cursor.execute("DELETE FROM products")
        
        # Insert multiple test products
        test_products = [
            (1, "Nike Running Shoes", "Shoes", "Nike", 89.99, 45.00, "Athletic", "NIKE001", 1),
            (2, "Adidas T-Shirt", "Tops & Tees", "Adidas", 29.99, 15.00, "Athletic", "ADIDAS001", 1),
            (3, "Levi's Jeans", "Jeans", "Levi's", 79.99, 40.00, "Casual", "LEVIS001", 1),
            (4, "Apple iPhone Case", "Accessories", "Apple", 19.99, 8.00, "Electronics", "APPLE001", 1),
            (5, "Samsung Galaxy Case", "Accessories", "Samsung", 15.99, 6.00, "Electronics", "SAMSUNG001", 1)
        ]
        
        cursor.executemany("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_products)
        
        conn.commit()
        conn.close()
        
        # Test 1: Get all products
        response = client.get("/api/products?page=1&page_size=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_count"] == 5
        assert len(data["products"]) == 5
        
        # Test 2: Get specific product
        response = client.get("/api/products/1")
        assert response.status_code == status.HTTP_200_OK
        product = response.json()
        assert product["name"] == "Nike Running Shoes"
        assert product["brand"] == "Nike"
        assert product["retail_price"] == 89.99
        
        # Test 3: Search products
        response = client.get("/api/products/search?search=Nike")
        assert response.status_code == status.HTTP_200_OK
        search_data = response.json()
        assert search_data["total_count"] == 1
        assert search_data["products"][0]["name"] == "Nike Running Shoes"
        
        # Test 4: Search by category
        response = client.get("/api/products/search?search=Jeans")
        assert response.status_code == status.HTTP_200_OK
        search_data = response.json()
        assert search_data["total_count"] == 1
        assert search_data["products"][0]["name"] == "Levi's Jeans"
        
        # Test 5: Search by brand
        response = client.get("/api/products/search?search=Apple")
        assert response.status_code == status.HTTP_200_OK
        search_data = response.json()
        assert search_data["total_count"] == 1
        assert search_data["products"][0]["brand"] == "Apple"
    
    def test_pagination_workflow(self, client, test_db):
        """Test pagination workflow with multiple pages"""
        # Setup test data with more products
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                brand TEXT,
                retail_price REAL,
                cost REAL,
                department TEXT,
                sku TEXT,
                distribution_center_id INTEGER
            )
        """)
        
        # Clear any existing data
        cursor.execute("DELETE FROM products")
        
        # Insert 15 test products
        test_products = []
        for i in range(1, 16):
            test_products.append((
                i, f"Product {i}", f"Category {i % 3}", f"Brand {i % 4}",
                float(10 + i), float(5 + i), f"Department {i % 2}",
                f"SKU{i:03d}", 1
            ))
        
        cursor.executemany("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_products)
        
        conn.commit()
        conn.close()
        
        # Test pagination: page 1
        response = client.get("/api/products?page=1&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_count"] == 15
        assert len(data["products"]) == 5
        assert data["page"] == 1
        assert data["page_size"] == 5
        
        # Test pagination: page 2
        response = client.get("/api/products?page=2&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["products"]) == 5
        assert data["page"] == 2
        
        # Test pagination: page 3
        response = client.get("/api/products?page=3&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["products"]) == 5
        assert data["page"] == 3
        
        # Test pagination: last page (should have remaining items)
        response = client.get("/api/products?page=4&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["products"]) == 0  # No more products
    
    def test_error_handling_workflow(self, client, test_db):
        """Test error handling workflow"""
        # Setup minimal test data
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                brand TEXT,
                retail_price REAL,
                cost REAL,
                department TEXT,
                sku TEXT,
                distribution_center_id INTEGER
            )
        """)
        
        # Clear any existing data
        cursor.execute("DELETE FROM products")
        
        cursor.execute("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (1, 'Test Product', 'Test Category', 'Test Brand', 29.99, 15.00, 'Test Department', 'TEST001', 1)
        """)
        
        conn.commit()
        conn.close()
        
        # Test 1: Valid product ID
        response = client.get("/api/products/1")
        assert response.status_code == status.HTTP_200_OK
        
        # Test 2: Invalid product ID (non-existent)
        response = client.get("/api/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        # FastAPI returns error in 'detail' field
        assert "detail" in error_data
        assert "Product with ID 999 not found" in error_data["detail"]
        
        # Test 3: Invalid product ID format
        response = client.get("/api/products/abc")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test 4: Invalid pagination parameters
        response = client.get("/api/products?page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.get("/api/products?page_size=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.get("/api/products?page_size=101")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test 5: Missing required search parameter
        response = client.get("/api/products/search")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_data_consistency_workflow(self, client, test_db):
        """Test data consistency across different endpoints"""
        # Setup test data
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                brand TEXT,
                retail_price REAL,
                cost REAL,
                department TEXT,
                sku TEXT,
                distribution_center_id INTEGER
            )
        """)
        
        # Clear any existing data
        cursor.execute("DELETE FROM products")
        
        cursor.execute("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (1, 'Consistent Product', 'Test Category', 'Test Brand', 29.99, 15.00, 'Test Department', 'TEST001', 1)
        """)
        
        conn.commit()
        conn.close()
        
        # Test 1: Get product by ID
        response1 = client.get("/api/products/1")
        assert response1.status_code == status.HTTP_200_OK
        product1 = response1.json()
        
        # Test 2: Get product from list
        response2 = client.get("/api/products?page=1&page_size=10")
        assert response2.status_code == status.HTTP_200_OK
        products = response2.json()["products"]
        product2 = next((p for p in products if p["id"] == 1), None)
        
        # Test 3: Search for the product
        response3 = client.get("/api/products/search?search=Consistent")
        assert response3.status_code == status.HTTP_200_OK
        search_results = response3.json()["products"]
        product3 = search_results[0] if search_results else None
        
        # Verify data consistency across all endpoints
        assert product1["id"] == product2["id"] == product3["id"]
        assert product1["name"] == product2["name"] == product3["name"]
        assert product1["category"] == product2["category"] == product3["category"]
        assert product1["brand"] == product2["brand"] == product3["brand"]
        assert product1["retail_price"] == product2["retail_price"] == product3["retail_price"]
        assert product1["cost"] == product2["cost"] == product3["cost"]
        assert product1["department"] == product2["department"] == product3["department"]
        assert product1["sku"] == product2["sku"] == product3["sku"]
        assert product1["distribution_center_id"] == product2["distribution_center_id"] == product3["distribution_center_id"]

class TestPerformanceWorkflow:
    """Test performance aspects of the API"""
    
    def test_large_dataset_handling(self, client, test_db):
        """Test handling of large datasets"""
        # Setup large test dataset
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                brand TEXT,
                retail_price REAL,
                cost REAL,
                department TEXT,
                sku TEXT,
                distribution_center_id INTEGER
            )
        """)
        
        # Clear any existing data
        cursor.execute("DELETE FROM products")
        
        # Insert 1000 test products
        test_products = []
        for i in range(1, 1001):
            test_products.append((
                i, f"Product {i}", f"Category {i % 10}", f"Brand {i % 20}",
                float(10 + (i % 100)), float(5 + (i % 50)), f"Department {i % 5}",
                f"SKU{i:04d}", 1
            ))
        
        cursor.executemany("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_products)
        
        conn.commit()
        conn.close()
        
        # Test performance with large dataset
        import time
        start_time = time.time()
        
        response = client.get("/api/products?page=1&page_size=50")
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_count"] == 1000
        assert len(data["products"]) == 50
        
        # Response should be reasonably fast (less than 1 second)
        assert end_time - start_time < 1.0
        
        # Test search performance
        start_time = time.time()
        response = client.get("/api/products/search?search=Product&page=1&page_size=20")
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_count"] == 1000  # All products contain "Product"
        
        # Search should also be reasonably fast
        assert end_time - start_time < 1.0 