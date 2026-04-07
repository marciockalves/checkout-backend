from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_product_service
from app.schemas.product_schema import ProductPaginationResponse, ProductRead, ProductUpdate
from app.repository.product_repository import ProductRepository
from app.db.session import get_db
from app.services.product_service import ProductService
from app.services.storage_service import StorageService


router =APIRouter()

@router.post("/", response_model=ProductRead)
async def create_product(
    name: str = Form(...),
    barcode: str = Form(...),
    price: float = Form(...),
    stock_quantity: int =  Form(...),
    file: UploadFile = File(...),
    db: AssertionError = Depends(get_db)
    ):
    repo = ProductRepository(db)
    storage = StorageService()

    existing = await repo.get_by_barcode(barcode)

    if existing:
        raise HTTPException(status_code=400, detail= "Barcode already registred")
    
    image_url = await storage.upload_image(file)

    product_data = {
        "name": name,
        "barcode": barcode,
        "price": price,
        "stock_quantity": stock_quantity,
        "image_url": image_url
    }


    return await repo.create(product_data)

@router.get("/{barcode}", response_model=ProductRead)
async def get_product(barcode: str, db:AsyncSession= Depends(get_db)):
    repo= ProductRepository(db)
    product = await repo.get_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product

@router.put("/{barcode}", response_model=ProductUpdate)
async def update_produtct(barcode: str, 
                        payload: ProductUpdate, 
                        db: AsyncSession = Depends(get_db)):

    repo = ProductRepository(db)
    updated = await repo.update_by_barcode(barcode, payload)

    print(f"DEBUG: O que o repositório retornou? {updated}")

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Produto {barcode} não encontrado"
        )

    return updated


@router.get("/", response_model = ProductPaginationResponse)
async def list_products(
    page: int =  Query(1, ge=1, description = "número de página"),
    size: int = Query(20, ge=1, le=100, description="Itens por página"),
    sort_by: str = Query("name", description="Coluna de Ordenação"),
    order: str = Query("asc", regex="(asc|desc)$"),
    service: ProductService = Depends(get_product_service)
):
    return await service.get_all_paginated(
        page=page,
        size=size,
        sort_by=sort_by,
        order=order
    )