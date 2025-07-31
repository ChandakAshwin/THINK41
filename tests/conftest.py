import pytest
import sqlite3
import tempfile
import shutil
import os
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from database import DatabaseManager

@pytest.fixture
def test_db():
    """Create a temporary test database"""
    # Create a temporary database file
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    yield temp_db.name
    
    # Cleanup
    if os.path.exists(temp_db.name):
        os.unlink(temp_db.name)

@pytest.fixture
def test_db_manager(test_db):
    """Create a database manager with test database"""
    return DatabaseManager(test_db)

@pytest.fixture
def client(test_db):
    """Create a test client with test database"""
    # Temporarily modify the database path in the app
    from main import db
    original_db_path = db.db_path
    db.db_path = test_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Restore original database path
    db.db_path = original_db_path

@pytest.fixture
def sample_products():
    """Sample product data for testing"""
    return [
        {
            "id": 1,
            "name": "Test Product 1",
            "category": "Test Category",
            "brand": "Test Brand",
            "retail_price": 29.99,
            "cost": 15.00,
            "department": "Test Department",
            "sku": "TEST001",
            "distribution_center_id": 1
        },
        {
            "id": 2,
            "name": "Test Product 2",
            "category": "Test Category",
            "brand": "Test Brand",
            "retail_price": 49.99,
            "cost": 25.00,
            "department": "Test Department",
            "sku": "TEST002",
            "distribution_center_id": 1
        }
    ]

@pytest.fixture
def setup_test_data(test_db, sample_products):
    """Setup test data in the database"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    # Create products table
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
    
    # Insert sample data
    for product in sample_products:
        cursor.execute("""
            INSERT INTO products (id, name, category, brand, retail_price, cost, department, sku, distribution_center_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product["id"], product["name"], product["category"], product["brand"],
            product["retail_price"], product["cost"], product["department"],
            product["sku"], product["distribution_center_id"]
        ))
    
    conn.commit()
    conn.close()
    
    return sample_products 