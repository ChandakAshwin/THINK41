from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from database import DatabaseManager

router = APIRouter()
db = DatabaseManager()

# Department response models
class Department(BaseModel):
    id: int
    name: str
    product_count: int

class DepartmentDetail(Department):
    products: List[dict]

@router.get("/departments", response_model=List[Department])
async def get_departments():
    """
    Get list of all departments with product counts.
    """
    try:
        with db.get_connection() as conn:
            # Get departments with product counts
            query = """
            SELECT 
                d.id,
                d.name,
                COUNT(p.id) as product_count
            FROM departments d
            LEFT JOIN products p ON d.id = p.department_id
            GROUP BY d.id, d.name
            ORDER BY d.name
            """
            
            cursor = conn.execute(query)
            departments = []
            for row in cursor.fetchall():
                departments.append({
                    "id": row[0],
                    "name": row[1],
                    "product_count": row[2]
                })
            
            return departments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments/{department_id}", response_model=DepartmentDetail)
async def get_department(department_id: int):
    """
    Get specific department details and its products.
    """
    try:
        with db.get_connection() as conn:
            # Get department details
            dept_query = """
            SELECT 
                d.id,
                d.name,
                COUNT(p.id) as product_count
            FROM departments d
            LEFT JOIN products p ON d.id = p.department_id
            WHERE d.id = ?
            GROUP BY d.id, d.name
            """
            
            dept_result = conn.execute(dept_query, (department_id,)).fetchone()
            if not dept_result:
                raise HTTPException(status_code=404, detail="Department not found")
                
            # Get products for this department
            products_query = """
            SELECT 
                p.id,
                p.name,
                p.category,
                p.brand,
                p.retail_price,
                p.cost,
                p.sku
            FROM products p
            WHERE p.department_id = ?
            ORDER BY p.name
            """
            
            cursor = conn.execute(products_query, (department_id,))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "id": dept_result[0],
                "name": dept_result[1],
                "product_count": dept_result[2],
                "products": products
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments/{department_id}/products")
async def get_department_products(
    department_id: int,
    page: int = 1,
    page_size: int = 50
):
    """
    Get products for a specific department with pagination.
    """
    try:
        offset = (page - 1) * page_size
        
        with db.get_connection() as conn:
            # Get total count
            count_query = """
            SELECT COUNT(*) 
            FROM products p
            WHERE p.department_id = ?
            """
            count_result = conn.execute(count_query, (department_id,)).fetchone()
            total_count = count_result[0] if count_result else 0
            
            if total_count == 0:
                return {"products": [], "total_count": 0, "page": page, "page_size": page_size}
                
            # Get paginated products
            query = """
            SELECT 
                p.id,
                p.name,
                p.category,
                p.brand,
                p.retail_price,
                p.cost,
                p.sku
            FROM products p
            WHERE p.department_id = ?
            ORDER BY p.name
            LIMIT ? OFFSET ?
            """
            
            cursor = conn.execute(query, (department_id, page_size, offset))
            products = [dict(row) for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": (total_count + page_size - 1) // page_size
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
