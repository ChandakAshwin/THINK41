from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    id: int
    name: str
    category: str
    brand: Optional[str] = None
    retail_price: Optional[float] = None
    cost: Optional[float] = None
    department: Optional[str] = None
    sku: Optional[str] = None
    distribution_center_id: Optional[int] = None

class ProductResponse(ProductBase):
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total_count: int
    page: Optional[int] = None
    page_size: Optional[int] = None
    search_term: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int 