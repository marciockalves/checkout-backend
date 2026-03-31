from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product


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
    
    