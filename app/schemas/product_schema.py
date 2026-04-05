from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ProductBase(BaseModel):
    name: str = Field(..., mmin_length=1)
    barcode: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(0, ge=0)
    image_url: str = Field(..., min_length=3)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: UUID
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Caneca de Café"])
    price: Optional[float] = Field(None, examples=[29.90])
    stock_quantity: Optional[int] = Field(None, examples=[15])
    image_url: Optional[str] = Field(None, examples=["http://.../123455.jpg"])

    class config:
        from_attributes = True
