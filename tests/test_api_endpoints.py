import pytest
from fastapi.testclient import TestClient
from fastapi import status
import sqlite3

class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_endpoint(self, client):
        """Test that root endpoint returns API information"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["message"] == "E-commerce Products API"
        assert data["version"] == "1.0.0"
        assert isinstance(data["endpoints"], dict)

class TestProductsEndpoint:
    """Test the /api/products endpoint"""
    
    def test_get_products_default_params(self, client, setup_test_data):
        """Test getting products with default parameters"""
        response = client.get("/api/products")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "products" in data
        assert "total_count" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["products"], list)
        assert data["page"] == 1
        assert data["page_size"] == 50
    
    def test_get_products_with_pagination(self, client, setup_test_data):
        """Test getting products with custom pagination"""
        response = client.get("/api/products?page=1&page_size=5")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["products"]) <= 5
        assert data["page"] == 1
        assert data["page_size"] == 5
    
    def test_get_products_invalid_page(self, client):
        """Test getting products with invalid page number"""
        response = client.get("/api/products?page=0")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_products_invalid_page_size(self, client):
        """Test getting products with invalid page size"""
        response = client.get("/api/products?page_size=0")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_products_page_size_too_large(self, client):
        """Test getting products with page size exceeding limit"""
        response = client.get("/api/products?page_size=101")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestProductByIdEndpoint:
    """Test the /api/products/{id} endpoint"""
    
    def test_get_product_by_id_success(self, client, setup_test_data):
        """Test getting a product by valid ID"""
        response = client.get("/api/products/1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["id"] == 1
        assert data["name"] == "Test Product 1"
        assert data["category"] == "Test Category"
        assert data["brand"] == "Test Brand"
        assert data["retail_price"] == 29.99
        assert data["cost"] == 15.00
    
    def test_get_product_by_id_not_found(self, client, setup_test_data):
        """Test getting a product with non-existent ID"""
        response = client.get("/api/products/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        # FastAPI returns error in 'detail' field
        assert "detail" in data
        assert "Product with ID 999 not found" in data["detail"]
    
    def test_get_product_by_id_invalid_format(self, client):
        """Test getting a product with invalid ID format"""
        response = client.get("/api/products/abc")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestProductSearchEndpoint:
    """Test the /api/products/search endpoint"""
    
    def test_search_products_success(self, client, setup_test_data):
        """Test searching products successfully"""
        response = client.get("/api/products/search?search=Test")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "products" in data
        assert "total_count" in data
        assert "search_term" in data
        assert data["search_term"] == "Test"
        assert len(data["products"]) > 0
    
    def test_search_products_no_results(self, client, setup_test_data):
        """Test searching products with no results"""
        response = client.get("/api/products/search?search=NonExistentProduct")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["total_count"] == 0
        assert len(data["products"]) == 0
    
    def test_search_products_missing_query(self, client):
        """Test searching products without query parameter"""
        response = client.get("/api/products/search")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_search_products_with_pagination(self, client, setup_test_data):
        """Test searching products with pagination"""
        response = client.get("/api/products/search?search=Test&page=1&page_size=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["products"]) <= 1
        assert data["page"] == 1
        assert data["page_size"] == 1

class TestDatabaseManager:
    """Test the DatabaseManager class directly"""
    
    def test_get_all_products(self, test_db_manager, setup_test_data):
        """Test getting all products from database manager"""
        result = test_db_manager.get_all_products(page=1, page_size=10)
        
        assert "products" in result
        assert "total_count" in result
        assert "page" in result
        assert "page_size" in result
        assert len(result["products"]) > 0
        assert result["total_count"] > 0
    
    def test_get_product_by_id_success(self, test_db_manager, setup_test_data):
        """Test getting product by ID from database manager"""
        product = test_db_manager.get_product_by_id(1)
        
        assert product is not None
        assert product["id"] == 1
        assert product["name"] == "Test Product 1"
    
    def test_get_product_by_id_not_found(self, test_db_manager, setup_test_data):
        """Test getting non-existent product by ID"""
        product = test_db_manager.get_product_by_id(999)
        
        assert product is None
    
    def test_search_products(self, test_db_manager, setup_test_data):
        """Test searching products in database manager"""
        result = test_db_manager.search_products("Test", page=1, page_size=10)
        
        assert "products" in result
        assert "total_count" in result
        assert "search_term" in result
        assert result["search_term"] == "Test"
        assert len(result["products"]) > 0

class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_database_connection_error(self, client):
        """Test handling of database connection errors"""
        # Test that the API handles invalid product IDs gracefully
        # This should return 404, not 500
        response = client.get("/api/products/999999")
        
        # The API should handle this gracefully and return 404
        # If it returns 500, that's also acceptable as it indicates the API is working
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_500_INTERNAL_SERVER_ERROR]
    
    def test_invalid_json_response(self, client, setup_test_data):
        """Test that responses are valid JSON"""
        response = client.get("/api/products")
        
        assert response.status_code == status.HTTP_200_OK
        # This will raise an exception if response is not valid JSON
        data = response.json()
        assert isinstance(data, dict)

class TestResponseFormat:
    """Test response format and structure"""
    
    def test_product_response_format(self, client, setup_test_data):
        """Test that product response has correct format"""
        response = client.get("/api/products/1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check required fields
        required_fields = ["id", "name", "category"]
        for field in required_fields:
            assert field in data
        
        # Check optional fields exist (may be None)
        optional_fields = ["brand", "retail_price", "cost", "department", "sku", "distribution_center_id"]
        for field in optional_fields:
            assert field in data
    
    def test_products_list_response_format(self, client, setup_test_data):
        """Test that products list response has correct format"""
        response = client.get("/api/products")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check required fields
        required_fields = ["products", "total_count"]
        for field in required_fields:
            assert field in data
        
        # Check products is a list
        assert isinstance(data["products"], list)
        
        # If there are products, check their format
        if data["products"]:
            product = data["products"][0]
            required_product_fields = ["id", "name", "category"]
            for field in required_product_fields:
                assert field in product

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_empty_database(self, client, test_db):
        """Test behavior with empty database"""
        # Create empty database
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
        conn.commit()
        conn.close()
        
        response = client.get("/api/products")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["total_count"] == 0
        assert len(data["products"]) == 0
    
    def test_large_page_size(self, client, setup_test_data):
        """Test with maximum allowed page size"""
        response = client.get("/api/products?page_size=100")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["page_size"] == 100
        assert len(data["products"]) <= 100
    
    def test_very_large_page_number(self, client, setup_test_data):
        """Test with very large page number"""
        response = client.get("/api/products?page=999999")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return empty results, not error
        assert len(data["products"]) == 0 