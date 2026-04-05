from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product_schema import ProductUpdate

from typing import Optional



class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_barcode(self, barcode: str):
        result = await self.db.execute(select(Product).filter(Product.barcode == barcode))
        return result.scalars().first()
    
    async def create(self, product_data: dict):
        new_product = Product(**product_data)
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product
    
    async def update_by_barcode(self, barcode: str, update_data: ProductUpdate) -> Optional[Product]:

        query = select(Product).where(Product.barcode == barcode)
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()

        if product:
           
            data_dict = update_data.model_dump(exclude_unset=True)
            
            for key, value in data_dict.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            await self.db.commit()
            
            await self.db.refresh(product) 
            return product
    
        return None
        