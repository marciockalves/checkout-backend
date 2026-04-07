from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db import get_db 
from app.repository.product_repository import ProductRepository
from app.services.product_service import ProductService


async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:

    repository = ProductRepository(db)
    

    service = ProductService(repository)
    

    return service