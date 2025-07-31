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
        """Get all products with pagination and department information"""
        offset = (page - 1) * page_size
        
        with self.get_connection() as conn:
            # Get total count
            count_result = conn.execute("SELECT COUNT(*) FROM products").fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get products for current page with department information
            query = """
            SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.cost, 
                   p.department, p.sku, p.distribution_center_id,
                   d.id as department_id, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            ORDER BY p.id 
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
        """Get a specific product by ID with department information"""
        with self.get_connection() as conn:
            query = """
            SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.cost, 
                   p.department, p.sku, p.distribution_center_id,
                   d.id as department_id, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.id = ?
            """
            
            cursor = conn.execute(query, (product_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def search_products(self, search_term: str, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """Search products by name, category, or brand with department information"""
        offset = (page - 1) * page_size
        search_pattern = f"%{search_term}%"
        
        with self.get_connection() as conn:
            # Get total count for search
            count_query = """
            SELECT COUNT(*) FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.name LIKE ? OR p.category LIKE ? OR p.brand LIKE ? OR d.name LIKE ?
            """
            count_result = conn.execute(count_query, (search_pattern, search_pattern, search_pattern, search_pattern)).fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get search results with department information
            query = """
            SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.cost, 
                   p.department, p.sku, p.distribution_center_id,
                   d.id as department_id, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.name LIKE ? OR p.category LIKE ? OR p.brand LIKE ? OR d.name LIKE ?
            ORDER BY p.id 
            LIMIT ? OFFSET ?
            """
            
            cursor = conn.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, page_size, offset))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "search_term": search_term,
                "total_pages": (total_count + page_size - 1) // page_size
            }
    
    def get_departments(self) -> List[Dict[str, Any]]:
        """Get all departments"""
        with self.get_connection() as conn:
            query = """
            SELECT id, name
            FROM departments
            ORDER BY name
            """
            
            cursor = conn.execute(query)
            departments = [dict(row) for row in cursor.fetchall()]
            return departments
    
    def get_products_by_department(self, department_id: int, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """Get products by department ID with pagination"""
        offset = (page - 1) * page_size
        
        with self.get_connection() as conn:
            # Get total count for department
            count_query = """
            SELECT COUNT(*) FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE d.id = ?
            """
            count_result = conn.execute(count_query, (department_id,)).fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get products for department
            query = """
            SELECT p.id, p.name, p.category, p.brand, p.retail_price, p.cost, 
                   p.department, p.sku, p.distribution_center_id,
                   d.id as department_id, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE d.id = ?
            ORDER BY p.id 
            LIMIT ? OFFSET ?
            """
            
            cursor = conn.execute(query, (department_id, page_size, offset))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "department_id": department_id,
                "total_pages": (total_count + page_size - 1) // page_size
            } 