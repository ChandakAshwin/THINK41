from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from models import ProductResponse, ProductListResponse, DepartmentResponse, DepartmentListResponse, ErrorResponse
from database import DatabaseManager

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Products API",
    description="API for accessing e-commerce product data with department information",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database manager
db = DatabaseManager()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "E-commerce Products API",
        "version": "1.0.0",
        "description": "API with department information after Milestone 4 refactoring",
        "endpoints": {
            "GET /api/products": "List all products with pagination and department info",
            "GET /api/products/{id}": "Get a specific product by ID with department info",
            "GET /api/products/search": "Search products by name, category, brand, or department",
            "GET /api/departments": "List all departments",
            "GET /api/departments/{id}/products": "Get products by department ID"
        }
    }

@app.get("/api/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Number of products per page"),
    search: Optional[str] = Query(None, description="Search term for products")
):
    """
    Get all products with optional pagination and search.
    Now includes department information after Milestone 4 refactoring.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of products per page (default: 50, max: 100)
    - **search**: Optional search term to filter products by name, category, brand, or department
    """
    try:
        if search:
            result = db.search_products(search, page, page_size)
        else:
            result = db.get_all_products(page, page_size)
        
        # Convert to ProductResponse objects
        products = [ProductResponse(**product) for product in result["products"]]
        
        return ProductListResponse(
            products=products,
            total_count=result["total_count"],
            page=result["page"],
            page_size=result["page_size"],
            search_term=result.get("search_term")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/products/search", response_model=ProductListResponse)
async def search_products(
    search: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Number of products per page")
):
    """
    Search products by name, category, brand, or department.
    Now includes department information after Milestone 4 refactoring.
    
    - **search**: Search term (required)
    - **page**: Page number (default: 1)
    - **page_size**: Number of products per page (default: 50, max: 100)
    """
    try:
        result = db.search_products(search, page, page_size)
        
        # Convert to ProductResponse objects
        products = [ProductResponse(**product) for product in result["products"]]
        
        return ProductListResponse(
            products=products,
            total_count=result["total_count"],
            page=result["page"],
            page_size=result["page_size"],
            search_term=result.get("search_term")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    Get a specific product by ID with department information.
    Now includes department information after Milestone 4 refactoring.
    
    - **product_id**: The ID of the product to retrieve
    """
    try:
        product = db.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found"
            )
        
        return ProductResponse(**product)
    
    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/departments", response_model=DepartmentListResponse)
async def get_departments():
    """
    Get all departments.
    New endpoint added after Milestone 4 refactoring.
    """
    try:
        departments = db.get_departments()
        
        return DepartmentListResponse(
            departments=[DepartmentResponse(**dept) for dept in departments],
            total_count=len(departments)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/departments/{department_id}/products", response_model=ProductListResponse)
async def get_products_by_department(
    department_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Number of products per page")
):
    """
    Get products by department ID with pagination.
    New endpoint added after Milestone 4 refactoring.
    
    - **department_id**: The ID of the department
    - **page**: Page number (default: 1)
    - **page_size**: Number of products per page (default: 50, max: 100)
    """
    try:
        result = db.get_products_by_department(department_id, page, page_size)
        
        # Convert to ProductResponse objects
        products = [ProductResponse(**product) for product in result["products"]]
        
        return ProductListResponse(
            products=products,
            total_count=result["total_count"],
            page=result["page"],
            page_size=result["page_size"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 