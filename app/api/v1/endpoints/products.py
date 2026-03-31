from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from shemas.product_schema import ProductCreate, ProductRead
from repository.product_repository import ProductRepository
from db.session import get_db


router =APIRouter()

@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, db: AssertionError = Depends(get_db)):
    repo = ProductRepository(db)

    existing = await repo.get_by_barcode(product.barcode)

    if existing:
        raise HTTPException(status_code=400, datail= "Barcode already registred")
    
    return await repo.create(product_data=product.model_dump())

@router.get("/{barcode}", response_model=ProductRead)
async def get_product(barcode: str, db:AsyncSession= Depends(get_db)):
    repo= ProductRepository(db)
    product = await repo.get_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product