import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str = "database/ecommerce.db"):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        try:
            yield conn
        finally:
            conn.close()
    
    def get_all_products(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """Get all products with pagination"""
        offset = (page - 1) * page_size
        
        with self.get_connection() as conn:
            # Get total count
            count_result = conn.execute("SELECT COUNT(*) FROM products").fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get products for current page
            query = """
            SELECT id, name, category, brand, retail_price, cost, 
                   department, sku, distribution_center_id
            FROM products 
            ORDER BY id 
            LIMIT ? OFFSET ?
            """
            
            cursor = conn.execute(query, (page_size, offset))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": (total_count + page_size - 1) // page_size
            }
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific product by ID"""
        with self.get_connection() as conn:
            query = """
            SELECT id, name, category, brand, retail_price, cost, 
                   department, sku, distribution_center_id
            FROM products 
            WHERE id = ?
            """
            
            cursor = conn.execute(query, (product_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def search_products(self, search_term: str, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """Search products by name, category, or brand"""
        offset = (page - 1) * page_size
        search_pattern = f"%{search_term}%"
        
        with self.get_connection() as conn:
            # Get total count for search
            count_query = """
            SELECT COUNT(*) FROM products 
            WHERE name LIKE ? OR category LIKE ? OR brand LIKE ?
            """
            count_result = conn.execute(count_query, (search_pattern, search_pattern, search_pattern)).fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get search results
            query = """
            SELECT id, name, category, brand, retail_price, cost, 
                   department, sku, distribution_center_id
            FROM products 
            WHERE name LIKE ? OR category LIKE ? OR brand LIKE ?
            ORDER BY id 
            LIMIT ? OFFSET ?
            """
            
            cursor = conn.execute(query, (search_pattern, search_pattern, search_pattern, page_size, offset))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "search_term": search_term,
                "total_pages": (total_count + page_size - 1) // page_size
            } 