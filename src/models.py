from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DepartmentBase(BaseModel):
    id: int
    name: str

class ProductBase(BaseModel):
    id: int
    name: str
    category: str
    brand: Optional[str] = None
    retail_price: Optional[float] = None
    cost: Optional[float] = None
    department: Optional[str] = None  # Keep for backward compatibility
    sku: Optional[str] = None
    distribution_center_id: Optional[int] = None
    # New department fields
    department_id: Optional[int] = None
    department_name: Optional[str] = None

class ProductResponse(ProductBase):
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total_count: int
    page: Optional[int] = None
    page_size: Optional[int] = None
    search_term: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    class Config:
        from_attributes = True

class DepartmentListResponse(BaseModel):
    departments: List[DepartmentResponse]
    total_count: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int 