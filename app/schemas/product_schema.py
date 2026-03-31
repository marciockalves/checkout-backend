from pydantic import BaseModel, Field
from uuid import UUID


class ProductBase(BaseModel):
    name: str = Field(..., mmin_length=1)
    barcode: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: UUID
    class Config:
        from_attributes = True
        